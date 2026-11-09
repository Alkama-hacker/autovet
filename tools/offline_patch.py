#!/usr/bin/env python3
"""Turn the repaired smali tree into an offline / privacy build.

Run AFTER `apktool d` and BEFORE `apktool b`:

    python3 tools/offline_patch.py <apktool-dir>

Design principle: never invent new data flow. Wherever the app talks to a
remote server we make the existing "server unreachable" branch happen, which
the original code already handles (null checks, catch blocks, OFFLINE labels).
That keeps the UI stable instead of silently changing what it displays.

Changes
-------
1. CaptureUploader.init()          -> early return
   Kills the 2 s loop that POSTs every captured HTTP/WS entry -- URLs,
   request/response bodies, headers, cookies -- to
   apiapk.eip.lat/api/public/captures-ingest.

2. CaptureStore.add()              -> drop the CaptureUploader.enqueue(...) call
   Second door into the same uploader.

3. WinGoAiClient.postJson()        -> return null
   PredictionClient.postJson()     -> return null
   Callers already do `if (text == null) return null`, so the signal simply
   comes back empty/offline. No more apiapk.eip.lat traffic at all.

4. NotificationStore.fetch()       -> early return
   Stops polling apiapk.eip.lat for operator messages ("submit a review or we
   lock your account", etc.).

5. WinGoStore.start()              -> early return
   Stops the 3 s polling of draw.ar-lottery01.com. You can still open WinGo in
   the built-in browser; it just no longer runs in the background.

6. BrowserFragment.onViewCreated() -> force ws_relay_enabled = false
   The shipped build defaults this pref to TRUE (`getBoolean(key, true)`),
   which proxies every WebSocket of whatever page you open -- auth tokens
   included -- through netsniffer.198-54-121-62.sslip.io.

7. AndroidManifest                 -> android:debuggable="false"
   The shipped APK was a debuggable build, which lets any app on the device
   attach to the process and read memory.
"""

import re
import sys
from pathlib import Path

PKG = Path("smali_classes3/com/eip/netsniffer")
REPORT = []


def note(msg):
    REPORT.append(msg)


def read(p):
    return p.read_text(encoding="utf-8")


def write(p, s):
    p.write_text(s, encoding="utf-8")


def replace_method(text, signature_re, new_body, label):
    """Swap out a whole .method ... .end method block."""
    m = re.search(signature_re, text, re.M)
    if not m:
        note(f"  FAIL not found: {label}")
        return text
    # skip to the end of the DECLARATION line first, otherwise a regex that
    # matches mid-line will make us eat the previous method's .end method
    decl_end = text.find("\n", m.end() if text[m.end() - 1] != "\n" else m.end() - 1)
    end = text.find("\n.end method", decl_end)
    if end < 0:
        note(f"  FAIL no .end method for: {label}")
        return text
    note(f"  ok  {label}")
    return text[: m.start()] + new_body + text[end + len("\n.end method"):]


POSTJSON_STUB = """.method private final postJson(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .locals 0

    # OFFLINE BUILD: remote endpoint is never contacted.
    # Every caller already handles a null response, so the app takes its
    # normal "signal unavailable" path instead of asking the server.
    const/4 p1, 0x0

    return-object p1
.end method"""


def main(root):
    root = Path(root)
    base = root / PKG
    if not base.is_dir():
        sys.exit(f"not an apktool dir: {base} missing")

    # ---- 1. CaptureUploader.init() -------------------------------------
    p = base / "CaptureUploader.smali"
    t = read(p)
    t = replace_method(
        t,
        r"^\.method public final init\(Landroid/content/Context;\)V$",
        """.method public final init(Landroid/content/Context;)V
    .locals 0

    # OFFLINE BUILD: capture uploader disabled. Nothing captured by this app
    # is ever sent anywhere.
    return-void
.end method""",
        "CaptureUploader.init() disabled",
    )
    write(p, t)

    # ---- 2. CaptureStore.add() : drop enqueue --------------------------
    p = base / "CaptureStore.smali"
    lines = read(p).split("\n")
    out, removed = [], 0
    for line in lines:
        if "CaptureUploader;->enqueue(" in line:
            removed += 1
            if out and "CaptureUploader;->INSTANCE" in out[-1]:
                out.pop()
            continue
        out.append(line)
    write(p, "\n".join(out))
    note(f"  ok  CaptureStore.add(): removed {removed} enqueue call(s)")

    # ---- 3. postJson() -> null ----------------------------------------
    for name in ("WinGoAiClient", "PredictionClient"):
        p = base / f"{name}.smali"
        t = read(p)
        t = replace_method(
            t,
            r"^\.method private final postJson\(Ljava/lang/String;Ljava/lang/String;\)Ljava/lang/String;$",
            POSTJSON_STUB,
            f"{name}.postJson() -> null",
        )
        write(p, t)

    # ---- 4. NotificationStore.fetch() ---------------------------------
    p = base / "NotificationStore.smali"
    t = read(p)
    t = replace_method(
        t,
        r"^\.method private final fetch\(Landroid/content/Context;\)V$",
        """.method private final fetch(Landroid/content/Context;)V
    .locals 0

    # OFFLINE BUILD: operator notification feed is not fetched.
    return-void
.end method""",
        "NotificationStore.fetch() disabled",
    )
    write(p, t)

    # ---- 5. WinGoStore.start() ----------------------------------------
    p = base / "WinGoStore.smali"
    t = read(p)
    t = replace_method(
        t,
        r"^\.method public final start\(\)V$",
        """.method public final start()V
    .locals 0

    # OFFLINE BUILD: no background polling of the lottery draw server.
    return-void
.end method""",
        "WinGoStore.start() disabled",
    )
    write(p, t)

    # ---- 6. ws_relay_enabled default TRUE -> FALSE --------------------
    # The original reads the pref as getBoolean("ws_relay_enabled", true).
    # Flip the default constant: no new branches, no new labels, and any user
    # choice previously saved in SharedPreferences still wins.
    p = base / "BrowserFragment.smali"
    lines = read(p).split("\n")
    patched = False
    for i, line in enumerate(lines):
        if 'const-string v3, "ws_relay_enabled"' not in line:
            continue
        for j in range(i + 1, min(i + 4, len(lines))):
            if "SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z" in lines[j]:
                # v5 holds the `true` default; replace its assignment above
                for k in range(i - 1, max(i - 200, -1), -1):
                    if re.match(r"\s*const/4 v5, 0x1\s*$", lines[k]):
                        lines[k] = "    const/4 v5, 0x0\n\n" \
                                   "    # OFFLINE BUILD: relay is opt-in, never on by default."
                        patched = True
                        break
                break
        if patched:
            break
    if patched:
        note("  ok  BrowserFragment: ws_relay_enabled default forced to false")
    else:
        note("  FAIL BrowserFragment: relay default `const/4 v5, 0x1` not found")
    write(p, "\n".join(lines))

    # ---- 7. manifest: not debuggable ----------------------------------
    mf = root / "AndroidManifest.xml"
    if mf.is_file():
        m = read(mf)
        if 'android:debuggable="true"' in m:
            m = m.replace('android:debuggable="true"', 'android:debuggable="false"')
            note("  ok  AndroidManifest: debuggable=false")
        else:
            note("  --  AndroidManifest: no debuggable=true found")
        write(mf, m)

    print("\n".join(REPORT))


if __name__ == "__main__":
    main(sys.argv[1])

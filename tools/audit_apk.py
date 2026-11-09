#!/usr/bin/env python3
"""Audit an APK for the class of bug that made this app crash on launch:
classes that the code references but that no dex actually defines.

Usage:
    python3 tools/audit_apk.py <apk> [original.apk]

With a second argument it also checks that every member reference into the
8 previously-missing stub classes is satisfied.

Needs: pip install androguard
"""
import re
import sys
import zipfile

STUBS = {
    "Lcom/eip/netsniffer/TamperGuard;",
    "Lcom/eip/netsniffer/VersionChecker;",
    "Lcom/eip/netsniffer/LicenseGate;",
    "Lcom/eip/netsniffer/LicenseGate$State;",
    "Lcom/eip/netsniffer/DepositGate;",
    "Lcom/eip/netsniffer/DepositGate$State;",
    "Lcom/eip/netsniffer/LicenseLockOverlay;",
    "Lcom/eip/netsniffer/DepositLockOverlay;",
}
MEMBER = re.compile(
    r"L[a-zA-Z0-9_/$]+;->[A-Za-z0-9_$<>]+"
    r"(?:\([^)]*\)[A-Za-z0-9_/\[;$]*|:[A-Za-z0-9_/\[;$]+)?"
)


def dex_names(z):
    return [n for n in z.namelist() if n.startswith("classes") and n.endswith(".dex")]


def main():
    from androguard.core.dex import DEX

    apk = sys.argv[1]
    z = zipfile.ZipFile(apk)

    defined, referenced = set(), set()
    for n in dex_names(z):
        d = DEX(z.read(n))
        for c in d.get_classes():
            defined.add(str(c.get_name()))
        for s in d.get_strings():
            # only the app's own classes: a missing platform/library class is
            # normal, a missing app class means the APK will die on startup.
            if s.startswith("Lcom/eip/") and s.endswith(";"):
                referenced.add(s)

    missing = sorted(referenced - defined)
    print(f"[1] app classes: referenced={len(referenced)} defined={len(defined & referenced)} "
          f"missing={len(missing)}")
    for m in missing:
        print("    MISSING CLASS", m)

    if len(sys.argv) > 2:
        src = zipfile.ZipFile(sys.argv[2])
        need = set()
        for n in dex_names(src):
            d = DEX(src.read(n))
            for c in d.get_classes():
                if not str(c.get_name()).startswith("Lcom/eip"):
                    continue
                for k in c.get_methods():
                    code = k.get_code()
                    if code is None:
                        continue
                    for ins in code.get_bc().get_instructions():
                        for tok in MEMBER.findall(ins.get_output()):
                            if tok.split("->")[0] in STUBS:
                                need.add(tok)

        have, field_only = set(), set()
        for n in dex_names(z):
            d = DEX(z.read(n))
            for c in d.get_classes():
                cn = str(c.get_name())
                if cn not in STUBS:
                    continue
                for k in c.get_methods():
                    have.add(f"{cn}->{k.get_name()}{k.get_descriptor()}")
                for f in c.get_fields():
                    have.add(f"{cn}->{f.get_name()}:{f.get_descriptor()}")
                    field_only.add(f"{cn}->{f.get_name()}")

        unresolved = [
            r for r in sorted(need)
            if r not in have and not ("(" not in r and r in field_only)
        ]
        print(f"[2] refs into stubs: need={len(need)} unresolved={len(unresolved)}")
        for u in unresolved:
            print("    UNRESOLVED", u)
        return 1 if (missing or unresolved) else 0

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

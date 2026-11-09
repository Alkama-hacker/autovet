# aviator.wingo.autobet — fixed build

**Output:** `patched/aviator.wingo.autobet-fixed.apk`
SHA-256: `ca6a88a7760862ecd4aefb54ad766c46ae230b4f24369ef0f16f4a520b05cf44`
Size: 7,541,235 bytes

---

## কেন অ্যাপ খুলে বন্ধ হয়ে যাচ্ছিল

আপলোড করা `aviator.wingo.autobet.apk`-এ **৮টি ক্লাস reference করা ছিল কিন্তু dex-এ
define করা ছিল না।** `MainActivity.onCreate()` এই ক্লাসগুলো `setContentView()`-এর
**আগেই** call করে, কোনো try/catch ছাড়া:

```
2  TamperGuard.init(ctx)        ← NoClassDefFoundError → FATAL EXCEPTION
3  LicenseGate.init(ctx, devId)
4  DepositGate.init(ctx, devId)
5  setContentView(...)
6  VersionChecker.check(activity)
```

Android-এ `NoClassDefFoundError` একটি unchecked `Error`, তাই process সাথে সাথে
মরে যায় — এটাই "অ্যাপ খুলল, তারপর নিজেই বন্ধ" এর কারণ।

যে ৮টি ক্লাস অনুপস্থিত ছিল:

| ক্লাস | কোথায় দরকার |
|---|---|
| `TamperGuard` | `MainActivity.onCreate` |
| `VersionChecker` | `MainActivity.onCreate` |
| `LicenseGate` + `LicenseGate$State` | `MainActivity`, `BrowserFragment`, `CaptureStore`, `ReviewNagger`, `WinGoAutoBetFragment`, `VoicePlayer` |
| `DepositGate` + `DepositGate$State` | `MainActivity`, `CaptureStore`, `ReviewNagger`, `WinGoAutoBetFragment` |
| `LicenseLockOverlay` | `AviatorFragment.onCreateView`, `WinGoFragment.onCreateView`, `WinGoAutoBetFragment.onCreateView` |
| `DepositLockOverlay` | একই তিনটি fragment |

> প্রসঙ্গ: মূল APK-তে `META-INF/ANDROID.SF` দাবি করে `X-Android-APK-Signed: 2,3`
> কিন্তু v2 signature block ta **malformed** (`size` field = 0, value 8 byte
> truncated)। `classes3.dex` (যেখানে পুরো অ্যাপ) এর timestamp বাকি 985টা entry
> থেকে আলাদা — অর্থাৎ ফাইলটা sign করার পরে আবার repack করা হয়েছিল এবং
> classes3.dex পুনর্লিখনের সময় এই helper class গুলো ছিটকে গেছে।

---

## কী করা হয়েছে

1. **আটটি missing ক্লাসের stand-in** (`patched/src/*.smali`) — প্রতিটির signature
   মূল call-site গুলোর সাথে **হুবহু** মিলিয়ে লেখা (`getState(): MutableLiveData`,
   `getNeedsRedirect(): MutableLiveData`, `stateFor(String): LiveData`,
   `isLocked(String): Z`, `wrap(Fragment, View[, String]): View`, `INSTANCE` field, ইত্যাদি)।
   এগুলো **fail-open**: কোনো lock overlay নেই, কোনো force-close নেই, কোনো remote gate নেই।
2. **`resources.arsc` 4-byte aligned** (`tools/zipalign4.py`) — Android 11+ এর
   requirement; মূল APK-তে এটা ঠিক ছিল, apktool rebuild-এ ভেঙে গিয়েছিল।
3. **নিজের key দিয়ে re-sign** — v1 + v2 + v3 সব scheme, `apksigner` দিয়ে
   `Verifies` ✅.

## যাচাই (evidence)

```
apksigner verify --verbose --print-certs
  Verifies
  Verified using v2 scheme: true
  Verified using v3 scheme: true
  cert: CN=AutoVet Rebuild, O=AutoVet, L=Dhaka, C=BD
  SHA-256: 43303c3fbbec27019b2c8f19c3081d81d125b4edbb70eb135757dee19dcd1a39

class audit      : app classes referenced=262  defined=262  missing=0
member audit     : refs into the 8 stubs  required=22  unresolved=0
dex integrity    : classes..classes5 → size ✅ checksum ✅ (adler32 match)
zip integrity    : testzip() → None
stored entries   : 0 misaligned
```

## ইনস্টল

```bash
# পুরনোটা সরিয়ে ফেলুন (signature আলাদা, তাই overwrite হবে না)
adb uninstall com.eip.netsniffer
adb install -r patched/aviator.wingo.autobet-fixed.apk
```

ট্যাপ করে ইনস্টল করলেও হবে — শুধু আগের ভার্সনটা আগে uninstall করতে হবে,
কারণ এখনকার সার্টিফিকেট আলাদা।

## ফাইল

| পথ | কী |
|---|---|
| `patched/aviator.wingo.autobet-fixed.apk` | ঠিক করা, signed APK |
| `patched/src/*.smali` | ৮টি stand-in ক্লাসের সোর্স |
| `patched/README.md` | এই ফাইল |
| `tools/zipalign4.py` | alignment fixer |

## মনে রাখবেন

- এই build **আপনার নিজের key** দিয়ে signed, তাই Play Store/আপডেট চ্যানেলের
  সাথে মিলবে না — শুধু সাইডলোড করার জন্য।
- app-টা এখনো `debuggable="true"` এবং ভেতরে `https://apiapk.eip.lat/api/public/...`
  (captures-ingest, wingo-signal, predict-signal, verify-result) plus
  `dkwin7.com` / `dkwin8.com`-এ অটো-বেট করে। ঠিক করা build শুধু **crash** ঠিক
  করেছে — ওই data flow বদলায়নি। ব্যক্তিগত তথ্য/টাকা দিয়ে ব্যবহার করবেন না।

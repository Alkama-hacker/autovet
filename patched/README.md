# aviator.wingo.autobet — offline-safe build

| ফাইল | কী |
|---|---|
| `aviator.wingo.autobet-offline.apk` | **এটাই চালান** — crash fix + সব network egress বন্ধ |
| `aviator.wingo.autobet-fixed.apk` | শুধু crash fix, network আগের মতোই |
| `src/*.smali` | ৮টি missing class-এর stand-in (দুই build-এই আছে) |
| `../tools/offline_patch.py` | offline build বানানোর script |
| `../tools/audit_apk.py` | missing-class + reference auditor |

```
offline.apk  sha256  89437d30f245e9801eb8ab293ec2bd9302a1d5848da79e453aef5924ffd51a5e
fixed.apk    sha256  ca6a88a7760862ecd4aefb54ad766c46ae230b4f24369ef0f16f4a520b05cf44
```

## ইনস্টল

```bash
adb uninstall com.eip.netsniffer        # signature আলাদা, তাই আগে uninstall
adb install -r aviator.wingo.autobet-offline.apk
```

---

## ১ম ধাপ — crash fix (দুই build-এই আছে)

মূল APK-তে ৮টি ক্লাস reference ছিল কিন্তু dex-এ defined ছিল না।
`MainActivity.onCreate()` এগুলো `setContentView()`-এর **আগেই** call করে,
try/catch ছাড়া → `NoClassDefFoundError` → process সাথে সাথে মরে।

`: TamperGuard, VersionChecker, LicenseGate(+State), DepositGate(+State),
LicenseLockOverlay, DepositLockOverlay`

এখন fail-open stand-in বসানো আছে — কোনো lock overlay নেই, force-close নেই,
remote version-gate নেই।

## ২য় ধাপ — offline / privacy hardening

| # | কী বন্ধ হলো | কীভাবে |
|---|---|---|
| 1 | **capture upload** — আপনার প্রতিটা HTTP/WS request-এর URL, headers, **body, cookie** `apiapk.eip.lat/api/public/captures-ingest`-এ যাচ্ছিল | `CaptureUploader.init()` → `return-void` |
| 2 | একই uploader-এর ২য় দরজা | `CaptureStore.add()` থেকে `enqueue(...)` call মুছে দেওয়া |
| 3 | **remote signal** (taka-wala prediction) `apiapk.eip.lat/api/public/{wingo-signal, predict-signal, verify-result}` | `WinGoAiClient.postJson()` + `PredictionClient.postJson()` → `null` |
| 4 | **operator notification feed** ("রিভিউ দিন নয়তো account lock") | `NotificationStore.fetch()` → `return-void` |
| 5 | **background polling** — প্রতি ৩ সেকেন্ডে `draw.ar-lottery01.com` | `WinGoStore.start()` → `return-void` |
| 6 | **WebSocket relay** — ডিফল্টে **ON** ছিল, আপনার WinGo login token `198-54-121-62.sslip.io` দিয়ে যাচ্ছিল | `getBoolean("ws_relay_enabled", false)` |
| 7 | **debuggable build** — যে কেউ process-এ attach করে memory পড়তে পারত | `android:debuggable="false"` |

> **নোট ৬:** মূল কোডে `getBoolean("ws_relay_enabled", true)` — অর্থাৎ relay
> **default চালু**। আমি শুধু default `true` → `false` করেছি, পুরো relay code
> সরাইনি — তাই আপনি Browser tab-এর checkbox থেকে নিজে চাইলে এখনো চালু করতে পারবেন।

## যাচাই (evidence)

```
apksigner verify        → Verifies ✅  v2 ✅  v3 ✅
class audit             → app classes referenced=262 defined=262 missing=0
member audit            → refs into stubs need=22 unresolved=0
dex integrity           → classes..classes5 size ✅ adler32 ✅
zip integrity           → testzip() = None
stored entries          → 0 misaligned (resources.arsc 4-byte aligned)
manifest                → debuggable = false
relay default           → getBoolean("ws_relay_enabled", Z) এর আগে const/4 v5, 0x0
```

**Socket খুলতে পারে এমন method — আগে vs পরে:**

```
BEFORE: CaptureUploader.flush          NotificationStore.fetch
        PredictionClient.postJson      WinGoAiClient.postJson
        WinGoStore.safeFetch           SniffingWebViewClient.shouldInterceptRequest

AFTER : CaptureUploader.flush          ← caller (init/enqueue) সব dead
        WinGoStore.safeFetch           ← caller (start + lambdas) সব dead
        SniffingWebViewClient.shouldInterceptRequest  ← যা আপনি ব্রাউজার খুললেন, সেটাই
```

`CaptureUploader$$ExternalSyntheticLambda1`, `WinGoStore$$ExternalSyntheticLambda0/1`
— **কোথাও instantiate হয় না**, তাই ওই scheduled loops আর চলে না।

## যেটা এখনো **সচল** (ইচ্ছাকৃত)

- **Browser tab** — আপনি নিজে যেমন URL দেবেন, তেমন লোড হবে।
  `SniffingWebViewClient` ওখানকার request গুলো এখনো **দেখে** (filter/patch করতে),
  কিন্তু কিচ্ছু **পাঠায় না** — ফোনের ভেতরেই থাকে।
- **SiteLogin / Aviator / WinGo / Profile** tab ও UI — আগের মতোই দেখাবে,
  শুধু "remote signal" জায়গাগুলোতে signal আসবে না (`OFFLINE` দেখাবে)।
- Telegram/review নাগ — মেসেজ আসবে না, কিন্তু crash করবে না।

## ঝুঁকি যেটা থেকে যায়

এই app স্বভাবতই একটা real-money betting site-এর ভেতরে auto-bet করার tool।
offline build আপনার **data বের হওয়া** বন্ধ করেছে, কিন্তু:

- আপনার নিজের ব্রাউজার ট্রাফিক (WinGo/`dkwin8.com`) এখনো সেই সাইটেই যাবে — স্বাভাবিক।
- `dkwin8.com`-এ লগইন করলে token সেই সাইটের কাছেই থাকবে — এটা যেকোনো ব্রাউজারের মতোই।
- এই build **আপনার নিজের key দিয়ে signed**, তাই Play Store/auto-update আসবে না।
- ভবিষ্যতে কেউ (অ্যাডমিন) নতুন build দিলে সেটা আবার এই ফাঁদে ফেলতে পারে — নতুন করে
  `tools/audit_apk.py` চালিয়ে দেখে নিন।

**সর্বোপরি:** টাকা জড়িত auto-bet নিজে চালাবেন না। signal এখন offline, তাই
"AI prediction" বলে কিছু কাজ করবে না — যা থাকবে সেটা আপনাকে হাতে বাজি ধরতে দেবে।

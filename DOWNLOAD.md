# ⬇️ APK download

দুটো signed build, দুটোই `patched/` ফোল্ডারে আছে।

| # | ফাইল | কী | সরাসরি লিংক |
|---|---|---|---|
| 1 | `aviator.wingo.autobet-offline.apk` | **এটাই চালান** — crash fix + সব network egress বন্ধ | [⬇ download](https://github.com/Alkama-hacker/autovet/raw/arena/3bb81279-autovet/patched/aviator.wingo.autobet-offline.apk) |
| 2 | `aviator.wingo.autobet-fixed.apk` | শুধু crash fix (network আগের মতোই) | [⬇ download](https://github.com/Alkama-hacker/autovet/raw/arena/3bb81279-autovet/patched/aviator.wingo.autobet-fixed.apk) |

> `raw.githubusercontent.com`-এ DNS আটকে থাকলে উপরের লিংক কাজ নাও করতে পারে।
> সেক্ষেত্রে GitHub-এর ফাইল পেজে গিয়ে **Download** চাপুন:
>
> - [patched/aviator.wingo.autobet-offline.apk](https://github.com/Alkama-hacker/autovet/blob/arena/3bb81279-autovet/patched/aviator.wingo.autobet-offline.apk)
> - [patched/aviator.wingo.autobet-fixed.apk](https://github.com/Alkama-hacker/autovet/blob/arena/3bb81279-autovet/patched/aviator.wingo.autobet-fixed.apk)

## checksum

```
offline  sha256  89437d30f245e9801eb8ab293ec2bd9302a1d5848da79e453aef5924ffd51a5e
fixed    sha256  ca6a88a7760862ecd4aefb54ad766c46ae230b4f24369ef0f16f4a520b05cf44
```

ডাউনলোডের পরে মিলিয়ে নিন:

```bash
sha256sum aviator.wingo.autobet-offline.apk
```

## ইনস্টল

```bash
adb uninstall com.eip.netsniffer        # signature বদলেছে, তাই আগে uninstall
adb install -r aviator.wingo.autobet-offline.apk
```

ফোনে সরাসরি: আগের অ্যাপটা uninstall করুন → ফাইলটা tap করে install দিন
(Unknown sources চালু রাখতে হবে)।

## বিস্তারিত

কী কী ঠিক করা হয়েছে, কী কী বন্ধ করা হয়েছে, আর যাচাইয়ের ফলাফল —
[`patched/README.md`](patched/README.md)

#!/usr/bin/env python3
"""Minimal zipalign: align STORED entries so they can be mmap()ed.

Android 11+ (API 30+) expects resources.arsc to be 4-byte aligned inside the
APK; zipalign normally handles this. This script does the same thing without
needing the Android SDK.

Usage: zipalign4.py <in.apk> <out.apk> [alignment]
"""
import struct
import sys
import zipfile

ALIGN_EXTRA_ID = 0xD935  # matches zipalign's padding extra-field id


def strip_align_extra(extra):
    out = bytearray()
    i = 0
    while i + 4 <= len(extra):
        hid, hlen = struct.unpack("<HH", extra[i:i + 4])
        if hid == ALIGN_EXTRA_ID:
            i += 4 + hlen
            continue
        out += extra[i:i + 4 + hlen]
        i += 4 + hlen
    return bytes(out)


def aligned_extra(base_extra, local_header_offset, name_len, align):
    """Extra field that makes the entry's data start on an `align` boundary."""
    base_extra = strip_align_extra(base_extra)
    head = local_header_offset + 30 + name_len + len(base_extra)
    need = (align - head % align) % align
    if need:
        if need < 4:
            need += align
        return base_extra + struct.pack("<HH", ALIGN_EXTRA_ID, need - 4) + b"\x00" * (need - 4)
    return base_extra


def main():
    src, dst = sys.argv[1], sys.argv[2]
    align = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    zin = zipfile.ZipFile(src)
    with open(dst, "wb") as fh:
        zout = zipfile.ZipFile(fh, "w", zipfile.ZIP_DEFLATED)
        for info in zin.infolist():
            data = zin.read(info.filename)
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.internal_attr = info.internal_attr
            zi.create_system = info.create_system
            zi.comment = info.comment
            zi.extra = strip_align_extra(info.extra)
            if info.compress_type == zipfile.ZIP_STORED:
                zi.extra = aligned_extra(
                    info.extra, fh.tell(), len(info.filename.encode("utf-8")), align
                )
            with zout.open(zi, "w") as entry:
                entry.write(data)
        zout.comment = zin.comment
        zout.close()
    zin.close()
    print("wrote", dst)


if __name__ == "__main__":
    main()

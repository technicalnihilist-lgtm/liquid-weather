#!/usr/bin/env python3
"""Check that the committed APK is the app this repository describes.

Two things can go wrong with the APK committed at the repository root, and
neither of them was checked by anything before this script:

  * it can bundle an *older* page than ``web/index.html``. ``android/build.sh``
    compares ``android/assets/index.html`` with ``web/index.html`` at build
    time, which stops a build made from a stale copy, but nothing compares the
    page inside the APK that is actually committed and published. A pass that
    edited ``web/index.html``, copied it to ``android/assets/`` and then
    committed without rebuilding leaves a page-parity mismatch on the source
    side and ships the previous app under a new version number — the 1.8.4 APK
    carried 1.8.3's page exactly this way.

  * it can carry a different ``versionCode``/``versionName`` than
    ``android/AndroidManifest.xml`` declares, if the manifest was bumped and the
    APK was not rebuilt (or an old APK was restored over a new one). The
    manifest is the single home of the version; the APK has to agree with it.

``CHECKSUMS.txt`` cannot catch either: it only proves the committed APK is the
file the checksum was taken from, and a stale APK has a perfectly valid checksum
of its own.

Usage: verify_apk.py [repo-root]   (defaults to the current directory)
Exit status 0 when everything agrees, 1 when it does not.
"""

import hashlib
import os
import struct
import sys
import zipfile

APK = "LiquidWeather.apk"
MANIFEST = os.path.join("android", "AndroidManifest.xml")
PAGE = os.path.join("web", "index.html")
APK_PAGE = "assets/index.html"


def _string_pool(data, start, header_size):
    """Read a RES_STRING_POOL chunk into a list of strings."""
    count, _styles, flags, strings_start, _styles_start = struct.unpack_from(
        "<IIIII", data, start + 8
    )
    offsets = [struct.unpack_from("<I", data, start + header_size + 4 * i)[0]
               for i in range(count)]
    base = start + strings_start
    out = []
    for off in offsets:
        pos = base + off
        if flags & 0x100:  # UTF-8
            n = data[pos]
            pos += 1
            if n & 0x80:
                pos += 1
            length = data[pos]
            pos += 1
            if length & 0x80:
                length = ((length & 0x7F) << 8) | data[pos]
                pos += 1
            out.append(data[pos:pos + length].decode("utf-8", "replace"))
        else:  # UTF-16
            n = struct.unpack_from("<H", data, pos)[0]
            pos += 2
            if n & 0x8000:
                n = struct.unpack_from("<H", data, pos)[0]
                pos += 2
            out.append(data[pos:pos + 2 * n].decode("utf-16-le", "replace"))
    return out


def apk_version(apk_path):
    """Return (versionCode, versionName) from an APK's binary AndroidManifest."""
    with zipfile.ZipFile(apk_path) as z:
        data = z.read("AndroidManifest.xml")

    strings = []
    pos = 8  # skip the XML chunk header
    while pos + 8 <= len(data):
        chunk_type, header_size, chunk_size = struct.unpack_from("<HHI", data, pos)
        if chunk_size == 0:
            break
        if chunk_type == 0x0001:  # string pool
            strings = _string_pool(data, pos, header_size)
        elif chunk_type == 0x0102:  # START_TAG
            _ns, name, attr_start, attr_size, attr_count = struct.unpack_from(
                "<IIHHH", data, pos + header_size
            )
            if strings[name] == "manifest":
                found = {}
                for i in range(attr_count):
                    off = pos + header_size + attr_start + i * attr_size
                    _ans, aname, _raw, _vsize, _res0, vtype, vdata = struct.unpack_from(
                        "<IIiHBBI", data, off
                    )
                    attr = strings[aname]
                    if attr == "versionCode" and vtype == 0x10:
                        found["versionCode"] = vdata
                    elif attr == "versionName":
                        found["versionName"] = strings[vdata] if vtype == 0x03 else str(vdata)
                if "versionCode" in found and "versionName" in found:
                    return found["versionCode"], found["versionName"]
                raise SystemExit("ERROR: %s declares no versionCode/versionName." % apk_path)
        pos += chunk_size
    raise SystemExit("ERROR: could not read the manifest out of %s." % apk_path)


def manifest_version(path):
    """Return (versionCode, versionName) from the source AndroidManifest.xml."""
    import re

    text = open(path, encoding="utf-8").read()
    code = re.search(r'android:versionCode="(\d+)"', text)
    name = re.search(r'android:versionName="([^"]+)"', text)
    if not code or not name:
        raise SystemExit("ERROR: %s declares no versionCode/versionName." % path)
    return int(code.group(1)), name.group(1)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    apk_path = os.path.join(root, APK)
    if not os.path.isfile(apk_path):
        print("ERROR: %s is missing; there is no published APK to check." % APK,
              file=sys.stderr)
        return 1

    failures = []

    apk_code, apk_name = apk_version(apk_path)
    man_code, man_name = manifest_version(os.path.join(root, MANIFEST))
    print("APK     : versionCode %s / versionName %s" % (apk_code, apk_name))
    print("manifest: versionCode %s / versionName %s" % (man_code, man_name))
    if (apk_code, apk_name) != (man_code, man_name):
        failures.append(
            "%s carries versionCode %s / versionName %s but %s declares %s / %s.\n"
            "       Rebuild the APK from this source: ./android/build.sh"
            % (APK, apk_code, apk_name, MANIFEST, man_code, man_name)
        )

    with zipfile.ZipFile(apk_path) as z:
        apk_page = sha256(z.read(APK_PAGE))
    src_page = sha256(open(os.path.join(root, PAGE), "rb").read())
    print("APK page: %s" % apk_page)
    print("web page: %s" % src_page)
    if apk_page != src_page:
        failures.append(
            "%s bundles an %s that is not %s.\n"
            "       The published APK shows an older app than the source; rebuild it."
            % (APK, APK_PAGE, PAGE)
        )

    for message in failures:
        print("ERROR: " + message, file=sys.stderr)
    if failures:
        return 1
    print("OK: the committed APK matches the manifest and the current page.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

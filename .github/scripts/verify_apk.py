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

``CHECKSUMS.txt`` cannot catch either: it only proves the committed APK is
the file the checksum was taken from, and a stale APK has a perfectly valid
checksum of its own.

A third thing went unchecked, and it is the only one that can make an APK
*uninstallable*: **who signed it**. ``android/build.sh`` verifies the key of the
APK it has just built and refuses to publish anything signed by another key, but
that gate runs on a build, and the file users download is the one committed
here. Nothing read the signature of the committed APK at all, so replacing it
with a re-signed — or an unsigned — build passed every check: same
``versionCode``, same bundled page, and a ``CHECKSUMS.txt`` digest taken from
the new file. Android then refuses the install over the released app
("signatures do not match"), and the certificate digest ``CHECKSUMS.txt`` prints
for a reader to compare is describing a file that is no longer there. That
digest was the third hand-written copy of one value that nothing read; it is now
compared with the certificate actually inside the APK, and with the copy
``build.sh`` insists on.

Usage: verify_apk.py [repo-root]   (defaults to the current directory)
Exit status 0 when everything agrees, 1 when it does not.
"""

import hashlib
import os
import re
import struct
import sys
import zipfile

APK = "LiquidWeather.apk"
MANIFEST = os.path.join("android", "AndroidManifest.xml")
PAGE = os.path.join("web", "index.html")
APK_PAGE = "assets/index.html"
CHECKSUMS = "CHECKSUMS.txt"
BUILD_SH = os.path.join("android", "build.sh")

# The digest a downloader is told to expect from `apksigner verify --print-certs`,
# and the one build.sh refuses to sign with anything else. Same value, two files.
CERT_CLAIM = re.compile(
    r"expected SHA-256 of the signer certificate:\s*\n\s*#?\s*([0-9a-fA-F]{64})")
BUILD_CERT = re.compile(r'EXPECTED_CERT_SHA256="([0-9a-fA-F]{64})"')


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


def _tlvs(buf, start=0, end=None):
    """Split a DER blob into [(tag, whole_tlv, body), ...].

    Only what a PKCS#7 SignedData needs: definite lengths, no construction rules.
    A malformed length raises ValueError, which the caller reports as a damaged
    signature rather than a traceback.
    """
    if end is None:
        end = len(buf)
    out = []
    pos = start
    while pos < end:
        begin = pos
        tag = buf[pos]
        pos += 1
        if pos >= end:
            raise ValueError("truncated tag")
        length = buf[pos]
        pos += 1
        if length & 0x80:
            count = length & 0x7F
            if count == 0 or count > 4 or pos + count > end:
                raise ValueError("unsupported length")
            length = int.from_bytes(buf[pos:pos + count], "big")
            pos += count
        body = pos
        pos += length
        if pos > end:
            raise ValueError("truncated value")
        out.append((tag, buf[begin:pos], buf[body:pos]))
    return out


def signer_cert_sha256(apk_path):
    """(sha256 of the DER signer certificate in the APK's v1 signature, why not).

    `apksigner verify --print-certs` reports exactly this digest, and the project
    key is 2035d69f…. apksigner is not available everywhere this script runs (CI
    installs the SDK after this step), so the certificate is read straight out of
    META-INF/*.RSA — a PKCS#7 SignedData whose first certificate in [0] is the
    signer's. The digest is None when there is nothing to read, and the second
    value says which of the two reasons it was.
    """
    with zipfile.ZipFile(apk_path) as z:
        blocks = sorted(
            name for name in z.namelist()
            if name.upper().startswith("META-INF/")
            and name.upper().endswith((".RSA", ".DSA", ".EC")))
        if not blocks:
            return None, "the APK carries no JAR signature"
        data = z.read(blocks[0])
    unreadable = "the APK's JAR signature block could not be read"
    try:
        content_info = _tlvs(data)
        if len(content_info) != 1 or content_info[0][0] != 0x30:
            return None, unreadable
        explicit = [t for t in _tlvs(content_info[0][2]) if t[0] == 0xA0]
        signed_data = _tlvs(explicit[0][2])[0]
        certificates = [t for t in _tlvs(signed_data[2]) if t[0] == 0xA0][0]
        certificate = _tlvs(certificates[2])[0]
        if certificate[0] != 0x30:
            return None, unreadable
        return sha256(certificate[1]), None
    except (ValueError, IndexError):
        return None, unreadable


def claimed_cert(path):
    """The certificate digest a document tells a reader to expect, or None."""
    if not os.path.isfile(path):
        return None
    found = CERT_CLAIM.search(open(path, encoding="utf-8").read())
    return found.group(1).lower() if found else None


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    apk_path = os.path.join(root, APK)
    if not os.path.isfile(apk_path):
        print("ERROR: %s is missing; there is no published APK to check." % APK,
              file=sys.stderr)
        return 1

    failures = []

    try:
        apk_code, apk_name = apk_version(apk_path)
        with zipfile.ZipFile(apk_path) as z:
            apk_page = sha256(z.read(APK_PAGE))
        apk_cert, cert_problem = signer_cert_sha256(apk_path)
    except (zipfile.BadZipFile, KeyError, struct.error, ValueError) as exc:
        # A damaged or half-written APK used to end in a traceback out of
        # zipfile (KeyError: no item named 'AndroidManifest.xml'), which reads as
        # a crash in the checker rather than as the broken APK it is.
        print("ERROR: %s cannot be read as an APK (%s: %s).\n"
              "       Rebuild it from this source: ./android/build.sh"
              % (APK, type(exc).__name__, exc), file=sys.stderr)
        return 1

    man_code, man_name = manifest_version(os.path.join(root, MANIFEST))
    print("APK     : versionCode %s / versionName %s" % (apk_code, apk_name))
    print("manifest: versionCode %s / versionName %s" % (man_code, man_name))
    if (apk_code, apk_name) != (man_code, man_name):
        failures.append(
            "%s carries versionCode %s / versionName %s but %s declares %s / %s.\n"
            "       Rebuild the APK from this source: ./android/build.sh"
            % (APK, apk_code, apk_name, MANIFEST, man_code, man_name)
        )

    src_page = sha256(open(os.path.join(root, PAGE), "rb").read())
    print("APK page: %s" % apk_page)
    print("web page: %s" % src_page)
    if apk_page != src_page:
        failures.append(
            "%s bundles an %s that is not %s.\n"
            "       The published APK shows an older app than the source; rebuild it."
            % (APK, APK_PAGE, PAGE)
        )

    # The signature: the one property of the APK that decides whether it can
    # install at all. Unchecked until now, so a re-signed or unsigned build
    # passed every gate; and CHECKSUMS.txt's certificate digest — the value a
    # reader compares with `apksigner verify --print-certs` — was never read by
    # anything, which is how a digest goes stale without a single failure.
    checksums_cert = claimed_cert(os.path.join(root, CHECKSUMS))
    build_cert_path = os.path.join(root, BUILD_SH)
    build_cert = None
    if os.path.isfile(build_cert_path):
        found = BUILD_CERT.search(open(build_cert_path, encoding="utf-8").read())
        build_cert = found.group(1).lower() if found else None
    print("APK cert: %s" % (apk_cert or "none — %s" % cert_problem))
    print("claimed : %s" % (checksums_cert or "none"))
    if apk_cert is None:
        failures.append(
            "%s is not signed by a key this repository can name: %s.\n"
            "       An APK whose signature cannot be confirmed will not install over\n"
            "       the published app. Rebuild it with ./android/build.sh."
            % (APK, cert_problem))
    else:
        if checksums_cert is None:
            failures.append(
                "%s prints no 'expected SHA-256 of the signer certificate', so a\n"
                "       downloader cannot confirm who signed the APK." % CHECKSUMS)
        elif checksums_cert != apk_cert:
            failures.append(
                "%s tells the reader to expect certificate %s but %s is signed by\n"
                "       %s. Either the APK was signed with another key — it will not\n"
                "       install over the published app — or the advertised digest is stale."
                % (CHECKSUMS, checksums_cert, APK, apk_cert))
        if build_cert is None:
            failures.append(
                "%s no longer names EXPECTED_CERT_SHA256, so a build can be signed\n"
                "       with any key and still pass its own check." % BUILD_SH)
        elif build_cert != apk_cert:
            failures.append(
                "%s builds with key %s but %s is signed by %s."
                % (BUILD_SH, build_cert, APK, apk_cert))

    for message in failures:
        print("ERROR: " + message, file=sys.stderr)
    if failures:
        return 1
    print("OK: the committed APK matches the manifest, the current page and the project key.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

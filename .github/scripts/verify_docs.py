#!/usr/bin/env python3
"""Check that the checksum README.md hands a downloader is the published one.

The install instructions in ``README.md`` end with a copy-paste verification::

    sha256sum LiquidWeather.apk
    # 042f58b6…

That digest is a *third* copy of the same value — ``CHECKSUMS.txt`` has one and
the committed ``LiquidWeather.apk`` is the file both describe — and nothing ever
read it. ``CHECKSUMS.txt`` is checked by ``.github/workflows/build.yml`` and the
APK is checked against the sources by ``verify_apk.py``, so both of those could
be perfectly current while the README still told every reader to expect an older
build's digest. It did: through seven releases (1.8, 1.8.1 … 1.9) the README
kept advertising ``f8a52080…``, the 1.7 APK, so a reader who followed the
instructions got

    LiquidWeather.apk: FAILED

on a download that was exactly the file the repository publishes. A checksum
that fails on a good file is worse than no checksum: it reads as a corrupted or
tampered download.

``CHECKSUMS.txt`` cannot catch this, because it says nothing about what the
README prints; neither can ``verify_apk.py``, which never opens the README.

Usage: verify_docs.py [repo-root]   (defaults to the current directory)
Exit status 0 when the README, CHECKSUMS.txt and the APK agree, 1 when they do
not.
"""

import hashlib
import os
import re
import sys

README = "README.md"
CHECKSUMS = "CHECKSUMS.txt"
APK = "LiquidWeather.apk"

DIGEST = re.compile(r"\b[0-9a-f]{64}\b")
# The fenced block that holds the verification instructions, and the digest line
# inside it (`# 042f58b6…`, the output of the command above it).
README_BLOCK = re.compile(r"```[^\n]*\n(.*?)```", re.S)
README_LINE = re.compile(r"^[ \t]*#?[ \t]*([0-9a-f]{64})[ \t]*$", re.M)
CHECKSUMS_LINE = re.compile(r"^([0-9a-f]{64})  LiquidWeather\.apk$", re.M)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def main(argv):
    root = argv[1] if len(argv) > 1 else "."

    readme_path = os.path.join(root, README)
    checksums_path = os.path.join(root, CHECKSUMS)
    apk_path = os.path.join(root, APK)
    for path in (readme_path, checksums_path, apk_path):
        if not os.path.isfile(path):
            print("ERROR: %s is missing." % path, file=sys.stderr)
            return 1

    readme = open(readme_path, encoding="utf-8").read()
    checksums = open(checksums_path, encoding="utf-8").read()

    failures = []

    apk_digest = sha256(apk_path)
    advertised = CHECKSUMS_LINE.search(checksums)
    if not advertised:
        failures.append("%s carries no digest line for %s." % (CHECKSUMS, APK))
        checksums_digest = None
    else:
        checksums_digest = advertised.group(1)
        if checksums_digest != apk_digest:
            failures.append(
                "%s advertises %s for %s but the committed file is %s."
                % (CHECKSUMS, checksums_digest, APK, apk_digest)
            )

    printed = []
    for block in README_BLOCK.findall(readme):
        if "sha256sum %s" % APK in block:
            printed.extend(README_LINE.findall(block))
    if not printed:
        failures.append(
            "%s prints no `sha256sum %s` digest, so a downloader has nothing to\n"
            "       compare against; the install instructions must show one." % (README, APK)
        )
        readme_digest = None
    else:
        readme_digest = printed[0]
        if len(set(printed)) > 1:
            failures.append(
                "%s prints more than one digest for %s (%s); only the published\n"
                "       one may appear." % (README, APK, ", ".join(sorted(set(printed))))
            )
        # Every other 64-hex value in the README is a stale digest left behind by
        # an edit that changed the line but not the prose around it.
        strays = sorted({d for d in DIGEST.findall(readme) if d != readme_digest})
        if strays:
            failures.append(
                "%s still prints %d other digest(s) (%s).\n"
                "       Only the published APK's digest belongs in the install instructions."
                % (README, len(strays), ", ".join(strays))
            )
        if readme_digest != apk_digest:
            failures.append(
                "%s tells the reader to expect %s but the published %s is %s.\n"
                "       Anyone following the instructions sees 'FAILED' on a good download."
                % (README, readme_digest, APK, apk_digest)
            )

    print("APK       : %s" % apk_digest)
    print("CHECKSUMS : %s" % (checksums_digest or "none"))
    print("README    : %s" % (readme_digest or "none"))

    for message in failures:
        print("ERROR: " + message, file=sys.stderr)
    if failures:
        return 1
    print("OK: the README advertises the digest of the APK this repository publishes.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

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

A fourth copy of a release value lives in ``STORE.md``, the copy-paste listing
a store publishes: its header says "Everything here matches the current
release, ``v1.11``". Nothing read it either, and it drifted exactly the way the
README's digest did — on 14 November the README named v1.11 while STORE.md
still said v1.10 and still quoted the 1.10 APK's size, so the listing copy for
the next submission advertised a version that had already been superseded. The
two labels are now compared with each other: they are the same hand-written
value in two files, and the README's is the one the maintainer updates at a
release, so a bump that touches one and not the other fails here. The manifest
is deliberately not the reference — it runs ahead of the last release for the
whole day between a version bump and the 22:00 cut.

Usage: verify_docs.py [repo-root]   (defaults to the current directory)
Exit status 0 when the README, STORE.md, CHECKSUMS.txt and the APK agree, 1
when they do not.
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

STORE = "STORE.md"
# The release both docs name. This is the fourth copy of one value, and the
# third one nothing read: the README says "Latest APK: v1.11" and STORE.md says
# "Everything here matches the current release, `v1.11`", and only one of them
# got updated — on 14 November the README named v1.11 while STORE.md still told
# a store its listing matched v1.10 (and still quoted the 1.10 APK's size).
# The two labels are compared with *each other*, not with
# AndroidManifest.xml: the manifest runs ahead of the last release for the whole
# day between a version bump and the 22:00 cut, so a manifest check would fail
# every afternoon. Two hand-written copies of one label can only agree or be
# wrong, and a release bump that updates one file and not the other fails here.
README_RELEASE = re.compile(r"\*\*Latest APK:\*\*[^\n]*?\bv(\d+(?:\.\d+)*)")
STORE_RELEASE = re.compile(r"matches the current\s+release,\s*`v(\d+(?:\.\d+)*)`")


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
    store_path = os.path.join(root, STORE)
    for path in (readme_path, checksums_path, apk_path, store_path):
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

    store = open(store_path, encoding="utf-8").read()
    readme_named = README_RELEASE.search(readme)
    store_named = STORE_RELEASE.search(store)
    readme_release = readme_named.group(1) if readme_named else None
    store_release = store_named.group(1) if store_named else None
    if not readme_release:
        failures.append(
            "%s no longer names the release it publishes ('**Latest APK:** [vX.Y]').\n"
            "       With no label there is nothing to keep %s in step with." % (README, STORE)
        )
    if not store_release:
        failures.append(
            "%s no longer says which release it matches ('matches the current release,\n"
            "       `vX.Y`'), so the store listing it holds cannot be checked.\n"
            "       Restore the sentence with the version of the published release." % STORE
        )
    if readme_release and store_release and readme_release != store_release:
        failures.append(
            "%s says its store listing matches v%s but %s publishes v%s.\n"
            "       The listing copy would advertise a version that is not the release."
            % (STORE, store_release, README, readme_release)
        )

    print("APK       : %s" % apk_digest)
    print("CHECKSUMS : %s" % (checksums_digest or "none"))
    print("README    : %s" % (readme_digest or "none"))
    print("README v  : %s" % (readme_release or "none"))
    print("STORE  v  : %s" % (store_release or "none"))

    for message in failures:
        print("ERROR: " + message, file=sys.stderr)
    if failures:
        return 1
    print("OK: the README advertises the digest of the APK this repository publishes,")
    print("    and the README and the store listing name the same release.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

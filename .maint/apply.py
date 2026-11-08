#!/usr/bin/env python3
"""Prepare (apply the pass's fix) or finish (fold in the build) — 2026-11-09.

Run from the repository root:  python3 .maint/apply.py prepare|finish
Every edit asserts the text it replaces, so a source that has moved on fails
loudly instead of committing a half-applied change.
"""
import hashlib
import os
import re
import shutil
import sys
import zipfile

ROOT = os.getcwd()
M = os.path.join(ROOT, ".maint")

UV_COMMENT = """/* `daily.uv_index_max` was the one daily field the renderer indexed without a
   guard: `usableForecast()` requires every array the cards and the strip read,
   but not this one, so a 200 payload that arrived without the block threw a
   TypeError inside render() — which show() catches as a link failure, so a
   complete forecast was discarded and the retry card took its place, and
   because the payload had already been cached every repaint threw again. The
   `|| 0` the UV card already carried is the intended reading for a missing
   value, so an absent array now reads as 0 there and in summarise(). */
const uvAt = (d, ti) => {
  const a = (d && Array.isArray(d.uv_index_max)) ? d.uv_index_max : null;
  const v = a ? +a[ti] : NaN;
  return isFinite(v) ? v : 0;
};
"""

COMMONS_COMMENT = """/* Every other request in the app runs against a deadline; this one had none.
   Its AbortController is the one fetchCityPhoto() creates, and only a newer city
   aborts it, so a Commons API that accepted the connection and then went quiet
   left the fetch pending for minutes: no city photo, no retry, a controller and
   a radio wake-lock held, and no photoStore record written either way. A
   deadline that fires is a lookup that could not be made, not a city without
   photos, so it takes the `failed` path fetchCityPhoto() already has for an
   HTTP error and nothing is cached. */
const COMMONS_TIMEOUT = 10000;
async function commonsCityPhoto(term, signal) {
  const ctl = new AbortController();
  const id = setTimeout(() => ctl.abort(), COMMONS_TIMEOUT);
  const relay = () => ctl.abort();
  if (signal) {
    if (signal.aborted) ctl.abort();
    else signal.addEventListener('abort', relay, { once: true });
  }
  try { return await commonsCityPhotoWith(term, ctl.signal); }
  finally { clearTimeout(id); if (signal) signal.removeEventListener('abort', relay); }
}
async function commonsCityPhotoWith(term, signal) {
"""


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
        f.write(s)


def sub1(s, old, new, what):
    n = s.count(old)
    assert n == 1, f"{what}: expected exactly one match, found {n}"
    return s.replace(old, new)


def prepare():
    web = read("web/index.html")

    web = sub1(web, "function todayIndex(w) {", UV_COMMENT + "function todayIndex(w) {", "uvAt insertion")
    web = sub1(web, "else if (cond === 'sun' && (+d.uv_index_max[ti] || 0) >= 8)",
               "else if (cond === 'sun' && uvAt(d, ti) >= 8)", "summarise uv read")
    web = sub1(web, "const uv = +(d.uv_index_max[ti] || 0);", "const uv = uvAt(d, ti);", "render uv read")
    web = sub1(web, "async function commonsCityPhoto(term, signal) {", COMMONS_COMMENT, "commons deadline")
    write("web/index.html", web)

    shutil.copyfile(os.path.join(ROOT, "web/index.html"), os.path.join(ROOT, "android/assets/index.html"))

    man = read("android/AndroidManifest.xml")
    man = sub1(man, 'android:versionCode="44"', 'android:versionCode="45"', "manifest versionCode")
    man = sub1(man, 'android:versionName="1.8"', 'android:versionName="1.8.1"', "manifest versionName")
    write("android/AndroidManifest.xml", man)

    bs = read("android/build.sh")
    bs = sub1(bs, "--version-code 44 --version-name 1.8", "--version-code 45 --version-name 1.8.1", "build.sh version")
    write("android/build.sh", bs)

    cl = read("CHANGELOG.md")
    entry = read(".maint/changelog.md")
    assert cl.count("## [Unreleased]") == 1, "CHANGELOG anchor is not unique"
    assert "## [1.8.1]" not in cl, "CHANGELOG already carries 1.8.1"
    write("CHANGELOG.md", cl.replace("## [Unreleased]", entry + "## [Unreleased]"))

    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", web, re.S)
    assert len(scripts) == 1, f"expected one script block, found {len(scripts)}"
    with open("/tmp/extracted.js", "w", encoding="utf-8") as f:
        f.write(scripts[0])
    print("prepare: ok")


def finish():
    apk = os.path.join(ROOT, "android/build/LiquidWeather.apk")
    data = open(apk, "rb").read()
    digest = hashlib.sha256(data).hexdigest()

    with zipfile.ZipFile(apk) as z:
        bundled = z.read("assets/index.html")
    source = open(os.path.join(ROOT, "web/index.html"), "rb").read()
    assert bundled == source, "the APK's bundled index.html does not match web/index.html"

    shutil.copyfile(apk, os.path.join(ROOT, "LiquidWeather.apk"))

    cs = read("CHECKSUMS.txt")
    cs, n = re.subn(r"(?m)^[0-9a-f]{64}  LiquidWeather\.apk$", digest + "  LiquidWeather.apk", cs)
    assert n == 1, f"CHECKSUMS digest line: {n} matches"
    write("CHECKSUMS.txt", cs)

    kib = round(len(data) / 1024)
    rd = read("README.md")
    rd, n = re.subn(r"\]\(LiquidWeather\.apk\)\*\* \(\d+ KB\)",
                    f"](LiquidWeather.apk)** ({kib} KB)", rd)
    assert n == 1, f"README size: {n} matches"
    write("README.md", rd)

    src8 = hashlib.sha256(source).hexdigest()[:8]
    cl = read("CHANGELOG.md")
    for token, value in (("__SRC8__", src8), ("__APK8__", digest[:8]), ("__KIB__", str(kib))):
        assert cl.count(token) == 1, f"CHANGELOG placeholder {token}: {cl.count(token)} matches"
        cl = cl.replace(token, value)
    write("CHANGELOG.md", cl)

    shutil.rmtree(M)
    os.remove(os.path.join(ROOT, ".github/workflows/maint-apply.yml"))
    print(f"finish: ok  apk={len(data)} bytes  sha256={digest}  readme={kib} KB")


if __name__ == "__main__":
    {"prepare": prepare, "finish": finish}[sys.argv[1]]()

#!/usr/bin/env python3
"""Audited edits for the 2026-11-05 16:00 IST maintenance pass (area 1:
network & API robustness). Asserted and idempotent: every replacement must
match exactly once (or already be applied), otherwise the run fails loudly.
"""
import sys

WEB = 'web/index.html'
MANIFEST = 'android/AndroidManifest.xml'
BUILD = 'android/build.sh'

EDITS = [
    # ---- 1. the search owns its request, so a replaced query is cancelled ----
    (
        "let stT, qTimer, qSeq = 0;      // qSeq: every keystroke, open and close invalidates older searches",
        "let stT, qTimer, qSeq = 0, searchCtl = null;   // qSeq: every keystroke, open and close invalidates older searches",
    ),
    (
        """  clearTimeout(qTimer);        // a pending debounce would fire a search into a closed sheet
  qSeq++;                      // and a request already in flight must not repaint the sheet later
""",
        """  clearTimeout(qTimer);        // a pending debounce would fire a search into a closed sheet
  qSeq++;                      // and a request already in flight must not repaint the sheet later
  /* qSeq only stopped a late answer from being *painted*: the download it was
     waiting for kept running to its 9s deadline, and on to the second
     geocoder after that. Dropping the request itself is the point. */
  if (searchCtl) { searchCtl.abort(); searchCtl = null; }
""",
    ),
    (
        """async function remoteSearch(term) {
  try {
    const j = await getJSON('https://geocoding-api.open-meteo.com/v1/search?count=8&language=en&format=json&name=' + encodeURIComponent(term), 9000);""",
        """async function remoteSearch(term, signal) {
  try {
    const j = await getJSON('https://geocoding-api.open-meteo.com/v1/search?count=8&language=en&format=json&name=' + encodeURIComponent(term), 9000, signal);""",
    ),
    (
        """    if (list.length) return list;
  } catch (e) {}
  try {
    const j = await getJSON('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=8&q=' + encodeURIComponent(term), 9000);""",
        """    if (list.length) return list;
  } catch (e) {}
  /* An abandoned query must not start the second service. Aborting the first
     request threw out of the try above and fell straight through to the
     fallback, which fired a fresh Nominatim request — for a search nobody was
     waiting for any more. */
  if (signal && signal.aborted) return [];
  try {
    const j = await getJSON('https://nominatim.openstreetmap.org/search?format=jsonv2&limit=8&q=' + encodeURIComponent(term), 9000, signal);""",
    ),
    (
        """async function search(q) {
  const seq = ++qSeq;
  const term = q.trim();
  if (term.length < 2) { paintSheet(q, localMatches(term)); return; }
  paintSheet(q, null);                                  // "Searching…"
  /* Belt and braces: whatever a geocoder hands back, the sheet must never be
     left on "Searching…". */
  let list = [];
  try { list = dedupe(await remoteSearch(term)); } catch (e) { list = []; }
  const byCountry = countryMatches(term);""",
        """async function search(q) {
  const seq = ++qSeq;
  /* Every keystroke past the debounce started its own geocoder request and left
     the previous one running: typing "mumbai" with a pause in it put two
     requests in flight at once, the free geocoding tier answers a burst with
     429, and a request for a query the reader had already replaced kept a
     radio awake for up to 18s (9s per geocoder). The older request is now
     cancelled, so only the query in the box is being asked about. */
  if (searchCtl) { searchCtl.abort(); searchCtl = null; }
  const term = q.trim();
  if (term.length < 2) { paintSheet(q, localMatches(term)); return; }
  const ctl = new AbortController();
  searchCtl = ctl;
  paintSheet(q, null);                                  // "Searching…"
  /* Belt and braces: whatever a geocoder hands back, the sheet must never be
     left on "Searching…". */
  let list = [];
  try { list = dedupe(await remoteSearch(term, ctl.signal)); } catch (e) { list = []; }
  if (ctl.signal.aborted) return;                       // superseded or sheet closed: nothing to paint
  const byCountry = countryMatches(term);""",
    ),
    # ---- 2. a truncated payload must not be drawn as NaN ----
    (
        """  const c = w.current, h = w.hourly, d = w.daily;
  return typeof c.temperature_2m === 'number' && typeof c.weather_code === 'number'
    && typeof c.is_day === 'number'
    && Array.isArray(h.time) && h.time.length > 0
    && Array.isArray(h.temperature_2m) && Array.isArray(h.weather_code) && Array.isArray(h.is_day)
    && Array.isArray(d.time) && d.time.length > 0""",
        """  const c = w.current, h = w.hourly, d = w.daily;
  /* Only three of the numbers the renderer prints were checked. Every other
     field it reads was taken on trust, and a payload that had lost one printed
     NaN where the reading should be: a body cut before `wind_gusts_10m` gave
     "gusts NaN" in the wind card, and an hourly block cut short of the current
     hour gave eight "NaN°" cells in the strip (the hourly arrays were only
     tested with Array.isArray, never for the length of h.time — the daily
     block had the length check all along). Every field the cards and the strip
     index is now required, so a truncated payload is rejected here, before it
     is cached, and the retry card replaces a screen of NaN. */
  const num = v => typeof v === 'number' && isFinite(v);
  return num(c.temperature_2m) && num(c.weather_code) && num(c.is_day)
    && num(c.relative_humidity_2m) && num(c.apparent_temperature)
    && num(c.pressure_msl) && num(c.wind_speed_10m) && num(c.wind_gusts_10m)
    && Array.isArray(h.time) && h.time.length > 0
    && Array.isArray(h.temperature_2m) && h.temperature_2m.length === h.time.length
    && Array.isArray(h.weather_code) && h.weather_code.length === h.time.length
    && Array.isArray(h.is_day) && h.is_day.length === h.time.length
    && Array.isArray(d.time) && d.time.length > 0""",
    ),
    # ---- 3. version bump (versionCode only ever increases) ----
    ('android:versionCode="26"', 'android:versionCode="27"'),
    ('android:versionName="1.5.2"', 'android:versionName="1.5.3"'),
    ('--version-code 26 --version-name 1.5.2', '--version-code 27 --version-name 1.5.3'),
]


def main():
    src = open(WEB, encoding='utf-8').read()
    for old, new in EDITS[:6]:
        if new in src:
            print('already applied:', old.splitlines()[0][:60])
            continue
        n = src.count(old)
        if n != 1:
            sys.exit('anchor matched %d times, expected 1: %r' % (n, old[:80]))
        src = src.replace(old, new)
        print('applied:', old.splitlines()[0][:60])
    open(WEB, 'w', encoding='utf-8').write(src)

    for path, pairs in ((MANIFEST, EDITS[6:8]), (BUILD, EDITS[8:])):
        txt = open(path, encoding='utf-8').read()
        for old, new in pairs:
            if new in txt:
                print('already applied:', new)
                continue
            if txt.count(old) != 1:
                sys.exit('%s: anchor matched %d times: %r' % (path, txt.count(old), old))
            txt = txt.replace(old, new)
            print('applied:', path, new)
        open(path, 'w', encoding='utf-8').write(txt)

    # android/assets/index.html is a byte copy of the web app
    open('android/assets/index.html', 'w', encoding='utf-8').write(
        open(WEB, encoding='utf-8').read())
    print('synced android/assets/index.html')

    # CHANGELOG: the dated entry goes above the Unreleased section
    cl = open('CHANGELOG.md', encoding='utf-8').read()
    entry = open('.github/maintenance/changelog_entry.md', encoding='utf-8').read()
    if '## [1.5.3]' in cl:
        print('changelog already has 1.5.3')
    else:
        if cl.count('## [Unreleased]') != 1:
            sys.exit('CHANGELOG: Unreleased anchor not found once')
        cl = cl.replace('## [Unreleased]', entry.rstrip('\n') + '\n\n## [Unreleased]')
        open('CHANGELOG.md', 'w', encoding='utf-8').write(cl)
        print('changelog entry added')


if __name__ == '__main__':
    main()

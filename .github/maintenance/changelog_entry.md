## [1.4.4] — 2026-11-04

### Fixed
- **A search could repaint the sheet after it was closed, showing results for a
  query nobody had typed.** The debounce timer was cancelled when the sheet
  closed, but a request already on the wire was not: it still resolved, still
  matched the sequence number (`qSeq` only moves when a *new* search starts) and
  still called `paintSheet()`. Reopening the sheet therefore painted "Popular",
  and a second or two later the late answer replaced it with a "Results" block
  for the previous query while the search box stood empty. Opening and closing
  the sheet now bump `qSeq` as well, so an in-flight search is invalidated
  exactly the way a newer keystroke invalidates it.
- **The same city was listed twice when a country search met an accented name.**
  Country queries merge the bundled list with the geocoder's answer and drop
  duplicates by name — but by `toLowerCase()` only. The geocoder returns
  "İstanbul" (capital dotted İ) for "turkiye", and lowercasing that yields
  "i̇stanbul" with a combining dot, which never matched the bundled "Istanbul":
  the sheet showed "Istanbul — Türkiye" and "İstanbul — Istanbul, Türkiye" one
  under the other. Both sides are now compared with the same `fold()` the local
  matcher already uses, so the duplicate collapses to the geocoder's row.
- **The city name was dead on the offline screen and on the loading skeleton.**
  `render()` wires `#openSearch` to `openSheet()`, but `renderSkeleton()` and
  `renderError()` build the same button and never bound it — so the app's
  "change city" control did nothing exactly when it mattered: with no
  connection (the only other route was the Cities tab) and while a forecast was
  loading. Both renders now bind it the same way.

### Notes
- Nothing visible changes: layout, spacing, colours, typography, gradients,
  glass values, wording and animation timings are untouched, and the three
  fixes live on a stale-response path, a duplicate-filter and an unbound click
  handler.
- Verified in headless Chromium against the previous file with the geocoders,
  the forecast API and the geolocation API stubbed: the rendered `#main` is
  byte-identical to 1.4.3 in the loaded, skeleton and offline states (same node
  count, same computed styles for every element), a full interactive pass
  (search, add city, remove city, settings slider, unit toggle, "Use my current
  location") logs zero console errors, and `node --check` is clean on the
  extracted script.
- Each fix has its own before/after check: the stale repaint shows `q: ""` with
  a `RESULTS London …` list on 1.4.3 and the untouched "Popular" list on 1.4.4;
  "turkiye" lists three Istanbul/İstanbul name hits on 1.4.3 and two (one row)
  on 1.4.4; the offline screen's city button leaves the sheet shut on 1.4.3 and
  opens it on 1.4.4, with identical markup in both.
- `versionCode 23` / `versionName 1.4.4` in `AndroidManifest.xml` and
  `build.sh` (up from 22 / 1.4.3), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical
  to `web/index.html`, the APK built from this tree bundles that same file byte
  for byte (`cmp` on the extracted asset), reports 23 / 1.4.4, and its digest is
  the one in `CHECKSUMS.txt`.
- Left alone deliberately: a search still falls through to the second geocoder
  when the first answers with a valid but empty list, so a typo can sit on
  "Searching…" for up to 18 s (2 × 9 s) before the "No place called …" message.
  Cutting that short would change which provider answers a query, and so which
  results appear — a behaviour change, not a bug fix.
- Left alone deliberately: a superseded geocoding request is still not aborted,
  only ignored (it is now ignored on the closed-sheet path too). It is a single
  short JSON call per keystroke burst, and aborting it would mean threading a
  controller through both providers for no visible gain.
- Left alone deliberately: the bundled "Goa" row carries the Panaji coordinates
  (15.2993, 74.124), which is what the list has always used and what the
  forecast is fetched for; the label is a state name, and renaming it is frozen
  wording.


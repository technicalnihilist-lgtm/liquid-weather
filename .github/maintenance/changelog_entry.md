## [1.5.3] — 2026-11-05

### Fixed
- **Every keystroke's search left its geocoder request running.** The debounced
  search started a request and only remembered a sequence number, so the number
  could stop an old answer from being *painted* but nothing stopped the download
  it was waiting for. Typing "mum", pausing, then finishing "mumbai" put two
  geocoder requests in flight at once, and a query the reader had already
  replaced went on to the second geocoder as well — up to 18s of radio time for
  an answer nobody would see, on a free tier that answers a burst with 429.
  Closing the sheet did the same: the sequence number was bumped, the request
  kept running. The search now owns an `AbortController`; a new query, a
  shorter one, or a closed sheet cancels the previous request, and an abandoned
  query no longer falls through to the Nominatim fallback (aborting the first
  request threw out of the `try` and straight into the second service).
- **A forecast payload that had lost a field printed NaN where a reading
  belongs.** `usableForecast()` checked the three numbers behind the hero and
  then took the rest on trust: a body cut before `wind_gusts_10m` rendered
  "gusts NaN" in the wind card, and an hourly block cut short of the current
  hour rendered eight "NaN°" cells in the hourly strip — the hourly arrays were
  only tested with `Array.isArray`, never for the length of `hourly.time`, while
  the daily block had that length check all along. Every field the cards and the
  strip index is now required (and must be a finite number, or an array exactly
  as long as its time axis), so a truncated payload is rejected before it is
  cached instead of being drawn. Nothing the API returns in full is affected.

### Notes
- Nothing visible changes for a complete payload. The rendered `#main` and
  `#nav` markup is byte-identical to 1.5.2 (same 3,128-byte `#main`, same hash)
  and **0 differences across 126 computed-style checks** (7 elements × 18
  properties, sampled after the entry animation had settled).
- Verified in headless Chromium with the forecast and both geocoders stubbed:
  `node --check` clean on the extracted script, zero console errors on load,
  and zero console errors through a full interactive pass (°C/°F both ways,
  open sheet, type, pick a result, remove a saved city, move the blur slider,
  close the panel) — every step identical to 1.5.2.
- Targeted checks, each on both files. "mum" then "mumbai" 700ms apart with a
  1.5s geocoder: **2** requests started, **0** cancelled on 1.5.2; **2** started,
  **1** cancelled on 1.5.3, with the same two results painted. Superseded while
  the first geocoder was still thinking: **4** geocoder requests on 1.5.2,
  **3** on 1.5.3 — the abandoned query's fallback never fires. Sheet closed with
  a search in flight: the request ran to completion on 1.5.2 and is cancelled on
  1.5.3. A query that is *not* superseded still makes both calls and still falls
  back to the bundled list (4 requests, identical results on both files).
- Payload checks, both files, same stub. Body without `wind_gusts_10m`: "gusts
  NaN" on 1.5.2, no NaN on 1.5.3. Hourly block of 8 hours instead of 168: 8
  `NaN°` cells on 1.5.2, none on 1.5.3. A payload with no hourly block at all
  behaves exactly as before (retry card on both).
- `versionCode 27` / `versionName 1.5.3` in `AndroidManifest.xml` and
  `build.sh` (up from 26 / 1.5.2), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html`.
- Left alone deliberately: the reverse geocoder in `locate()` still runs
  without a signal. Its promise is deliberately kept alive after the 2.5s name
  budget so a late name can be filled in, so cancelling it would change what the
  row is called; a superseded location request is already prevented from writing
  its name or its coordinates.
- Left alone deliberately: the hourly strip still repeats the last available
  hour when the block ends early. Dropping the cells would change the width of
  the strip, which the frozen UI does not allow; noted for a release that can
  re-check it on a device.

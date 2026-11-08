## [1.8.1] — 2026-11-09

### Fixed
- **A forecast that arrived without its UV block took the whole weather screen
  down.** `usableForecast()` requires every array the cards and the hourly strip
  index, but `daily.uv_index_max` was left out of that list while both of its
  readers took the array on trust: `summarise()` read `d.uv_index_max[ti]` on the
  clear-sky branch and `render()` read `+(d.uv_index_max[ti] || 0)` for the UV
  card. A 200 payload that arrived without that block — a proxy trimming the
  body, a field the model stops serving — therefore threw a `TypeError` halfway
  through `render()`, and `show()` catches a throw from `render()` as a *link*
  failure: a complete forecast was discarded and the reader got the "tap to try
  again" card instead of the weather. Because the payload had already been
  written to the cache before the render, every later repaint threw again, so
  the card stayed until the entry aged out ten minutes later and the next fetch
  repeated it. The `|| 0` that was already on the UV card is the app's own answer
  for a missing reading, so `uvAt()` now checks the array and an absent one reads
  as 0 — the same number a missing element produced — and both call sites go
  through it. Payloads that carry the field are untouched.
- **The city-photo lookup had no deadline, so a Commons API that went quiet left
  a request — and the radio — open for as long as the browser would wait.** Every
  other request in the app runs against one (`getJSON()` aborts at 8–12s);
  `commonsCityPhoto()` took the `AbortController` from `fetchCityPhoto()`, which
  only a newer city aborts. A Commons cluster that accepted the connection and
  then stopped answering, a middlebox holding the socket open, or a radio that
  dropped mid-request therefore left that fetch pending for minutes: the sky
  photo stayed up with no city photo and no retry, the fetch and its controller
  stayed alive, and the `photoStore` record was never written either way. The
  lookup now has its own 10s deadline on a controller relayed from the caller's
  signal, so a superseded lookup is still cancelled instantly. A deadline that
  fires takes the `failed` path `fetchCityPhoto()` already has for an HTTP
  error — nothing is cached as "this city has no photo", and the sky stays up —
  which is what a timeout means, unlike the "none" record a real empty answer
  still writes.

### Notes
- Measured on 1.8 first, in headless Chromium with the geocoders and the forecast
  stubbed. Payload with `daily.uv_index_max` deleted: 1.8 renders the retry card
  (`#main` 521 characters, no UV card, no photo); 1.8.1 renders the full screen
  with "UV index 0 Low". The same payload with the field present renders
  byte-identically before and after — `#main` 3,201 characters, hash
  `1883057677`, 231 nodes, same UV card "3 Moderate".
- Commons that accepts and never answers (a stubbed `fetch` whose only exit is
  the abort signal): 1.8 is still pending after 14s and nothing is ever written;
  1.8.1 aborts at 10,000 ms. A Commons lookup superseded by a newer city aborts
  at 800 ms — the deadline did not slow the supersede path down. A normal answer
  still paints the photo layer (`#photo.on`), and no abort fires.
- `node --check` is clean on the extracted script; a headless load of
  `web/index.html` and of the APK's own bundled `assets/index.html` report zero
  console errors and zero page errors, and a 54-action pass (search, pick a city,
  refresh, close, both settings tabs, all five sliders, reset, unit toggle,
  remove a saved city) reports none either, at a flat 282 nodes.
- `versionCode 45` / `versionName 1.8.1` in `AndroidManifest.xml` and `build.sh`
  (up from 44 / 1.8), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `__SRC8__…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`__APK8__…`), and the size quoted in the README follows it
  (`__KIB__ KB`).
- Left alone deliberately: `getJSON()` still does not consume the body of a
  response it is about to retry (a 429 body is a few hundred bytes and the
  browser releases it at the next collection — a real but tiny cost, and draining
  it changes the retry path for no gain); `Retry-After` is still read as seconds
  only, so the HTTP-date form falls back to the 300 ms floor it already used,
  capped at 2s either way; the retry still does not re-arm the 12s deadline,
  which is what keeps a retry from doubling the reader's wait; and
  `showPhoto()`'s `Image` load has no timeout, because an image request cannot be
  aborted and a late load is dropped by its token anyway.


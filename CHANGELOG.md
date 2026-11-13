# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1] — 2026-10-30

### Added
- **Glass & motion settings** — transparency, blur and bounce sliders (plus
  "Reset to default"), so the glass look can be tuned to taste on any screen.
  Choices persist between launches.
- **Draggable pill navigation** with a springy indicator and three tabs:
  **Weather**, **Cities** and **Glass**.

### Changed
- The bottom nav is now tab-based rather than one button per saved city; saved
  places live behind the Cities tab, and the city name in the top bar still
  opens the picker directly.
- Version bumped to 1.1 (`versionCode 2`), signed with the same key, so it
  installs straight over 1.0.

### Fixed
- The night-time summary no longer suggests going outside for the day — clear
  nights now read "Light winds and no rain expected overnight."

## [1.2] — 2026-10-31

### Added
- **4D depth & parallax across the whole app.** The sky gradient, sun/moon and
  clouds, particles, glass cards and the pill nav now sit at different depths
  and move at different rates. Motion follows the device tilt (gyroscope), your
  finger/mouse position, and scrolling.
- **Two new settings** in *Glass & motion*: **Depth** (how far apart the layers
  sit) and **Parallax** (how much they follow you). Both persist, and *Reset to
  default* restores them.

### Changed
- Version bumped to 1.2 (`versionCode 3`), same signing key, installs over 1.1.
- Settings sliders now show their saved positions the moment the app opens,
  instead of only after the panel is opened once.

### Notes
- With *Reduce motion* enabled in Android accessibility settings the depth
  effect switches itself off, and both sliders default to 0.
- Tilt parallax needs a device with a gyroscope; on anything without one the
  finger and scroll parallax still work.

## [1.2.1] — 2026-11-01

### Fixed
- **Keyboard and screen-reader access to the closed panels.** The search sheet
  and the *Glass & motion* panel were only hidden with `aria-hidden`, so their
  search field, sliders and buttons stayed in the tab order while invisible:
  tabbing walked through controls nobody could see, and the accessibility tree
  hid focusable content. Both panels are now `inert` while closed, and the
  search sheet is marked up as a dialog with a label.
- **Focus is no longer dropped to `<body>`.** Closing the search sheet or the
  settings panel now returns focus to the control that opened it (the city
  button, or the *Glass* tab), and opening the settings panel moves focus to
  its first slider instead of leaving it behind the panel.
- **The offline "tap here to try again" card works without a pointer** — it is
  a button role with Enter/Space handling, so the only route back online is no
  longer mouse-only.
- **Spoken names:** the °C/°F toggle announces "Temperature unit: Celsius /
  Fahrenheit", the search field has a label instead of relying on its
  placeholder, the refresh button has an accessible name, and the decorative
  particle canvas is hidden from assistive technology.
- **7-day range bar markup.** The bar was drawn with `<s>`, which means
  "no longer accurate" and can be announced as struck-through text; it is now a
  `<span>` with identical styling.

### Notes
- No visual change: layout, spacing, colours, gradients and animation timings
  are untouched — verified by pixel-identical screenshots of the old and new
  build.
- `versionCode 4` / `versionName 1.2.1`, same signing key, installs over 1.2.

## [1.2.2] — 2026-11-01

### Fixed
- **A damaged saved-places list could leave the app on a blank screen.** The
  places array read back from local storage was only checked with
  `Array.isArray(...) && length`, so a single unusable row (`null`, a string, an
  object with no name and no coordinates) reached the first render, where
  `places[cur].name` threw and nothing was ever painted. Rows are now validated
  on load: entries are dropped unless they are objects with usable coordinates
  (or the "My Location" row), coordinates stored as strings from an older build
  are converted to numbers, and a place with no `id` gets one derived from its
  coordinates. If nothing survives, the default "My Location" row is restored.
- **A bad `lw_cur` index blanked the app.** The saved current-place index was
  clamped only at the top (`Math.min`), so a negative value from a corrupt or
  truncated write made `places[cur]` undefined and the boot render threw. It is
  now parsed and clamped to `0 … places.length - 1`.
- **Out-of-range or non-numeric glass settings broke the CSS.** The stored
  settings object was merged into the defaults without checking it, so a value
  such as `{"bl": 500, "tr": "abc"}` reached the stylesheet as
  `backdrop-filter: blur(184px)` and `--k: NaN` — the glass lost its blur
  entirely and every glass card paid for a 184px backdrop blur. Each of the five
  settings is now accepted only if it parses to a finite number and is clamped to
  the slider's own 0–100 range; anything else falls back to the default.

### Notes
- No visual change: with valid saved state the rendered DOM and the computed
  styles of every major element are identical to 1.2.1 (checked in headless
  Chromium against the previous file, with default and non-default settings).
- `versionCode 5` / `versionName 1.2.2`, same signing key, installs over 1.2.1.

## [1.2.3] — 2026-11-01

### Fixed
- **Keyboard focus was thrown away by every re-render.** `render()` replaces the
  whole of `#main`, which destroys the control that had focus and drops focus to
  `<body>`. Toggling °C/°F with the keyboard, or picking a city, left keyboard and
  screen-reader users at the top of the document with no way back except tabbing
  through everything again. The id of the focused control is now remembered for a
  few seconds — a short window, so a later background refresh cannot steal focus —
  and put back on the new copy of the same control.
- **Deleting a saved city was pointer-only, and the ✕ in search results did
  nothing.** The remove control was a `role="button"` span with no `tabindex`, so
  it could not be focused or pressed from the keyboard, and it announced itself as
  "Remove" with no indication of what would be removed. In the Popular/Results
  rows it carried `data-rm="-1"`, which no handler ever read: it was announced as
  a Remove button and performed no removal at all. Both are now real controls:
  focusable, named after the city ("Remove Mumbai"), activated by Enter/Space, and
  wired to the same removal path as the Saved-places list.
- **Removing a city while a search was typed threw an error and left the stale
  row on screen.** The repaint after a removal was called without a results list,
  so `results.length` raised a `TypeError` — before the forecast refresh and the
  repaint ran. The sheet now reuses the results it last painted.
- **Tab walked into the page hidden behind the search sheet.** The sheet covers
  the whole screen but only hid itself from assistive technology, so tabbing past
  the last result went through the city bar, the unit button and the forecast
  behind it. `#main` is now `inert` while the sheet is open. The pill nav stays
  live: it floats above the sheet and is how you leave it.
- **Focus was dropped to `<body>` after a removal in the search sheet.** It now
  moves to the next ✕ in the repainted list (or the location button), instead of
  falling out of the panel.

### Notes
- No visual change: the rendered DOM and the computed styles of every element are
  identical to 1.2.2 in all four states checked (loaded, search sheet open,
  settings open, offline) — same node count, same structure, same styles.
- `versionCode 6` / `versionName 1.2.3`, same signing key, installs over 1.2.2.

## [1.2.4] — 2026-11-01

### Fixed
- **A truncated forecast response could wedge the app on the loading skeleton
  for good.** Open-Meteo can answer `200` with a body that is missing its
  `hourly`/`daily` blocks — a proxy cutting the response short, or a field list
  that changed. `render()` threw on `d.temperature_2m_max[0]` part-way through,
  and because the payload had already been written to the cache before it was
  drawn, every later attempt for that city re-threw the same error. `#main` kept
  the "Loading forecast…" skeleton and the dimmed `loading` state, with no retry
  card, so the only way out was to kill the app. Payloads are now validated
  before they are cached (`usableForecast`), and the failure path can no longer
  throw out of its own `catch`: a bad body is discarded and the normal offline
  card with its retry is shown instead.
- **A single rate-limited request threw the app into "Offline".** The free
  Open-Meteo tiers answer `429` under a burst — several cities switched quickly,
  or a few devices behind one address — and every non-2xx response was treated
  as a permanent failure, so the user had to tap the retry card by hand. A
  request the server was merely too busy to serve (`408`, `425`, `429`, `5xx`)
  now gets one more attempt after a short pause that honours `Retry-After`
  (capped at 2s). A rejected request (`400`, `404`), a network error and a
  timeout are still not repeated, so an offline device still fails at the normal
  deadline instead of waiting three times as long.
- **Superseded forecast requests were left running.** `show()` only ignored the
  answer of a request it had replaced (`showSeq`); the request itself kept
  downloading to its 12s timeout. Switching cities three times on a slow link
  left four forecast downloads open at once, three of them useless. The
  in-flight request is now cancelled through an `AbortController` as soon as a
  newer one starts — four concurrent downloads became two, three of them
  cancelled.

### Notes
- No visual change: with the same payload the rendered DOM is byte-identical to
  1.2.3 (same node count, same markup) and the only computed-style differences
  are the randomly generated cloud widths.
- `versionCode 7` / `versionName 1.2.4`, same signing key, installs over 1.2.3.

## [1.3] — 2026-11-01

### Fixed
- **A corrected device clock could freeze the forecast on screen.** Elapsed time
  was measured with `Date.now()`, so a wall clock that was set forward at boot
  (a flat battery, a first boot with no time source yet) and then corrected
  backwards by the network made the cached forecast look fresh for as long as
  the skew lasted: `show()` reused the cache instead of refetching, and the
  ten-minute refresh in `autoRefresh()` compared against a timestamp in the
  future, so it returned early every time. The app sat on one forecast — one
  "Now" column, one set of hour labels — until the clock caught up, which can be
  hours. Elapsed time for both the cache TTL and the refresh interval is now
  read from the monotonic clock (`performance.now()`), which cannot run
  backwards; the cache is in memory for a single session, so its timestamps stay
  comparable.

### Notes
- This is the day's release and carries the day's earlier fixes: keyboard and
  screen-reader access to the closed panels and across re-renders (1.2.1,
  1.2.3), validation of saved state so a bad write cannot blank the app (1.2.2),
  and the network hardening — truncated payloads rejected before caching, one
  retry on a busy server, superseded requests cancelled (1.2.4).
- No visual change: with the same payload the rendered DOM is byte-identical to
  1.2.4 (same node count, same markup, same hour and day labels).
- `versionCode 8` / `versionName 1.3`, same signing key, installs over 1.2.4.

## [1.3.1] — 2026-11-02

### Fixed
- **A location request that never answered left the app on the "Locating…"
  skeleton for good.** `getCurrentPosition`'s own `timeout` only starts once a
  permission decision exists, so a prompt that is never answered — or an Android
  WebView whose `onGeolocationPermissions` callback is never invoked because the
  activity was torn down while the system dialog was up — left the promise
  pending for ever. Nothing else ran: no forecast, no retry card, no way out but
  killing the app. A 15 s watchdog now settles the promise, and the existing
  failure path (a short toast plus the default city) takes over.
- **A position object without usable coordinates hung the same way.** The
  success callback read `p.coords.latitude` directly, so a partial or malformed
  position threw inside the browser's callback — outside every `try` — and the
  promise never settled. Coordinates are now checked before they are accepted;
  anything that is not two finite numbers is rejected into the normal failure
  path.
- **A failed location left the screen empty when "My Location" was not the first
  saved place.** After a refusal the row is given New Delhi's coordinates, but
  the repaint was guarded by `cur === 0` rather than by the row's own index, so
  with My Location anywhere but first nothing was ever drawn and the skeleton
  stayed up. It now repaints when the row it just filled is the one on screen.
- **Coordinates of exactly 0 were treated as "no location yet".** The equator and
  the prime meridian are real coordinates but falsy, and every "do we have a fix?"
  test used a bare `!p.lat`: such a place was never fetched, showed "Locating…"
  for ever, and was missing from the saved-places list and its refresh button.
  A single `hasFix()` test (two finite numbers) is now used everywhere.
- **Approximate location was reported as a refusal on Android 12+.** The
  permission result was read from `results[0]`, which is the fine-location
  answer only; a user who chose "Approximate location" (coarse granted, fine
  denied) was told location was blocked and dropped to New Delhi even though a
  coarse fix was available. Any granted result now counts, with a re-check of
  the manifest permission as a backstop.

### Notes
- No visual change: with a granted fix the rendered `#main` is byte-identical to
  1.3 (same node count, same markup, same hour and day labels), checked in
  headless Chromium against the previous file with a fixed forecast payload.
- `versionCode 9` / `versionName 1.3.1`, same signing key, installs over 1.3.

## [1.3.2] — 2026-11-02

### Fixed
- **An unrecognised weather code was drawn as a thunderstorm while everything
  around it said "Cloudy".** `iconFor()` picks the glyph with range tests
  (`code >= 95`, `code >= 61`, …), so a code with no entry in the WMO table — one
  added to the model after this build, or a stray value in a response — fell
  through to the icon of the highest range it happened to match: 97, 100, 120 and
  200 all drew ⛈️ beside the hero's "Cloudy" and over the plain cloudy sky that
  `scene()` had already chosen, and any code from 61 to 94 drew rain. The icon is
  now taken from the same table the description and the scene come from, so an
  unknown code reads as a coherent cloudy day in all three places it appears —
  hero, hourly strip and 7-day row.

### Notes
- No visual change for any real forecast: all 28 documented WMO codes render
  byte-identical DOM before and after, in both day and night states, checked in
  headless Chromium with a fixed payload (56 states, zero console errors).
- `versionCode 10` / `versionName 1.3.2`, same signing key, installs over 1.3.1.

## [1.3.3] — 2026-11-02

### Fixed
- **A reverse geocoder that never answered held the forecast back for sixteen
  seconds.** `locate()` awaited `reverseName()` before it did anything else, and
  `reverseName()` gives each of its two services a full 8 s deadline, so with a
  geocoder that hangs (a blocked domain, a captive portal, a DNS blackhole on a
  hotel network) the screen sat on "Locating…" for 16.4 s before the forecast
  request had even been made. A forecast needs nothing but the coordinates, so
  it is now requested the moment the fix arrives, alongside the name lookup, and
  the name is given 2.5 s to turn up before the app paints with the same
  coordinate label `reverseName()` itself returns when both services fail; a
  name that arrives after that is filled into the header instead of being
  dropped. Measured on a geocoder that never answers: forecast on screen in
  2.9 s instead of 16.4 s, and in the ordinary case the first paint no longer
  waits for the geocoder at all (the fetch overlaps it).
- **The My Location row never took its coordinates as its id, so the city it
  resolved to could be saved a second time.** The row kept the id `loc` for the
  rest of the session while carrying real coordinates, so the de-duplication in
  `addPlace()` could not recognise it: with My Location resolved to Pune,
  searching "Pune" and tapping the result added a *second* Pune row — two
  identical entries in a list that holds five, and one slot gone. The row is now
  keyed by its coordinates (`c18.520,73.857`), the same key every other place
  uses, so the search result selects the existing row. The forecast cache entry
  under the old id is dropped at the same time, so the cache no longer keeps one
  entry per city the device has passed through.
- **A superseded location request could overwrite a newer one.** Nothing
  sequenced `locate()` calls — boot, the city pill, the search sheet's "Use my
  current location" and a removal all start one — so an older request that
  answered last replaced a fresh fix with a stale position, and an older request
  that *failed* last toasted "Could not reach your location. Tap the city name to
  retry." over a screen that had just located successfully. `locate()` now
  carries a sequence number, the same guard `show()` already uses for forecast
  requests: only the newest request may write its result or report its failure.
- **A failed pre-fetch no longer costs a second full timeout.** When the forecast
  requested during `locate()` fails, the render that follows would otherwise ask
  again and make the user wait out a second 12 s deadline before the retry card
  appeared. A pre-fetch failure is remembered for five seconds and the retry card
  is drawn straight away; a user-initiated retry (`force`) always tries again.
  Checked against a forecast endpoint that never answers: the card appears at
  12.4 s, the same as before (12.2 s).

### Notes
- No visual change: with the same payload the rendered `#main` is byte-identical
  to 1.3.2 (124 nodes, same markup), and the computed styles of 17 key elements
  (hero, bar, cards, hourly, 7-day, nav, pill, sun, moon) are identical, checked
  in headless Chromium against the previous file.
- Failure paths re-checked with the fix: denied, timeout, a malformed position
  and a prompt that is never answered all still end on a rendered screen (New
  Delhi with the matching toast, and the 15 s watchdog for the unanswered
  prompt), with zero console errors in every scenario.
- `versionCode 11` / `versionName 1.3.3`, same signing key, installs over 1.3.2.

## [1.3.4] — 2026-11-02

### Fixed
- **The particle canvas ran an animation frame for the entire session, whether
  or not there was anything to draw.** `tick()` re-armed itself unconditionally
  at the end of every frame, so the loop never ended: a clear, cloudy or foggy
  scene seeds no particles at all, yet the app kept waking the main thread on
  every animation frame — forever — to clear a canvas that was already blank.
  With *Reduce motion* on it did the same, for ever, after the single clear it
  needed. Nothing stopped it while the page was hidden either: a browser pauses
  rAF for a hidden tab, but a WebView does not always, so a backgrounded app
  kept scheduling frames and kept its lightning timer armed. The loop now ends
  as soon as the canvas is blank and nothing is falling, and while the page is
  hidden; it restarts when a scene seeds particles, when the canvas is resized,
  or when the page becomes visible again, and the storm flash chain is paused
  with it. Measured in headless Chromium with a fixed payload: a clear-sky day
  went from 27 animation callbacks a second to 0, the same scene while hidden
  from 36 to 0, and a rain scene still animates (10–14 a second, canvas still
  painting) and still blanks the canvas when you switch to a clear city.

### Notes
- No visual change: rendered `#main` markup is byte-identical to 1.3.3 in four
  states (clear day, rain, storm night, snow with reduce-motion), 222 nodes each,
  and the computed styles of 20 key elements (sky layers, sun, moon, clouds,
  cards, hourly, 7-day, nav, pill, canvas) are identical too — animation-phase
  and randomly generated cloud properties aside. Zero console errors in every
  scenario, and switching rain → clear leaves 0 painted pixels on the canvas.
- Particle counts, speeds, drift and timings are untouched: only frames with
  nothing to draw are no longer requested.
- `versionCode 12` / `versionName 1.3.4`, same signing key, installs over 1.3.3.

## [1.3.5] — 2026-11-02

### Fixed
- **One unusable row from a geocoder froze the search sheet on "Searching…".**
  Results were passed straight from the response into `dedupe()`, which keys
  every row by `pid()` — and `pid()` calls `lat.toFixed(3)`. A row that arrived
  without coordinates (a partial payload, or a place the model has no point
  for), or with the coordinates as strings, threw inside `search()`, outside
  every `try`: the promise rejected, nothing painted, and the sheet sat on
  "Searching…" until the next keystroke. Rows are now normalised to numbers and
  checked (a name, two finite coordinates inside their ranges) before
  `dedupe()`, `row()` or `addPlace()` see them, and the wait for the geocoder is
  wrapped so the sheet always ends on a list or on the "No place called …"
  message.
- **The bundled list could not be found by the name people type.** Matching
  compared the accented characters themselves, so "bogota", "sao paulo",
  "cancun" and "turkiye" all answered "No place called …" although Bogotá,
  São Paulo, Cancún and Türkiye are in `POPULAR` — and with the geocoder
  unreachable that message was the only answer the offline list could give.
  Both sides are folded to plain letters before comparing (the displayed name
  keeps its accents), so the accented query still works too.
- **A pending search could fire after the sheet was closed.** The 320 ms
  debounce was never cancelled on close, so tapping a result or the ✕ while
  typing still sent a geocoder request for a list nobody could see. The timer
  is cleared when the sheet closes.

### Notes
- No visual change: the rendered `#main` is byte-identical to 1.3.4 (same
  3128-character markup, same FNV hash) with a fixed forecast payload, and so is
  the result list for every query that already matched — checked in headless
  Chromium against the previous file in four states (boot, online results,
  empty geocoder payload, geocoder unreachable), zero console errors in each.
- The malformed-payload case now renders the usable rows and logs nothing,
  where 1.3.4 rejected with `TypeError: Cannot read properties of undefined
  (reading 'toFixed')` and left the sheet on "Searching…".
- `versionCode 13` / `versionName 1.3.5`, same signing key, installs over 1.3.4.

## [1.3.6] — 2026-11-02

### Fixed
- **A location fix — or the New Delhi fallback — could put the same city in the
  list twice.** The pinned "My Location" row is keyed by its coordinates once a
  fix arrives, and `fallbackPlace()` writes New Delhi's coordinates into it;
  neither checked whether another row already carried that key. With New Delhi
  already saved, a refused location left two identical "New Delhi" rows, and
  with Pune saved, locating to Pune left the pinned row and the saved row side
  by side. Both showed in the Cities list and both counted towards the five-place
  limit, so a slot was gone for a place the user already had. A duplicate copy is
  now dropped: the pinned row keeps the id (so a search result still selects it)
  and `cur` stays on the row that was on screen. With New Delhi already saved the
  pinned row is dropped instead and the saved row selected, so the automatic
  default never displaces a place the user chose.
- **A superseded location request left its forecast download running.**
  `locate()` pre-fetches the forecast beside the name lookup (1.3.3), but that
  pre-fetch had no controller: a second location request — "Use my current
  location" tapped again, a removal, the retry after a failed fix — started its
  own download while the first ran on to its 12s deadline. The pre-fetch now
  carries an `AbortController` that the next location request cancels, the same
  rule `show()` already applies to forecasts, and an abandoned pre-fetch is no
  longer recorded as a failed link, so the render that follows cannot show the
  offline card over a request nobody wants. Measured against a forecast endpoint
  that never answers: two concurrent downloads became one, the superseded one
  reporting `AbortError`.
- **A superseded location request could still paint.** `locate()` checked its
  sequence number before writing the fix but not after awaiting the pre-fetch, so
  a request that had been replaced could render its city over the newer one. It
  re-checks after the wait.

### Notes
- No visual change: with the same payload the rendered `#main` is byte-identical
  to 1.3.5, and the computed styles of ten key elements (hero, bar, cards,
  hourly, 7-day, nav, canvas, sky layers, sun, moon) are identical, checked in
  headless Chromium against the previous file. Zero console errors in nine
  scenarios: granted fix, denied, no geolocation API, malformed position object,
  a prompt that never answers, a geocoder that hangs, forecast unreachable,
  search plus city switch, and the unit toggle.
- The 1.3.1 fix for a failed location with "My Location" anywhere but first
  still holds: denying while that row is on screen renders New Delhi, denying
  while another city is on screen leaves that city alone.
- `versionCode 14` / `versionName 1.3.6`, same signing key, installs over 1.3.5.

## [1.3.7] — 2026-11-02

### Fixed
- **A forecast with no usable clock in its `current` block was thrown away as
  "Offline".** The hourly strip works out which hour is "now" from
  `current.time`, and `hourIndex()` read it with `current.time.slice(0, 13)`
  without checking it was there. A payload whose `current` block arrived
  without `time` — a partial body, which `usableForecast()` accepted because it
  only required the three values the hero prints — threw a `TypeError` out of
  `render()`. The throw was caught by `show()` as if the *link* had failed, so
  the app discarded a complete, perfectly good forecast and showed the offline
  card; tapping that card re-fetched the same payload and failed the same way,
  which left the retry as a dead end. `hourIndex()` is now total: it reads the
  hourly block defensively, and a payload with no usable `current.time` renders
  from the first hour it has instead of throwing.
- **The cell marked "Now" could show midnight's weather.** When the hourly block
  ended before the current hour (a truncated array, or an older payload still on
  screen), the search for the current hour found nothing and the function
  returned `0` — the first hour of the block. The strip then opened on 00:00's
  temperature, labelled "Now", beside a hero drawn from the live current values
  (27° in the hero, 20° in the "Now" cell), and the dew point, visibility and
  "chance of precipitation in the next hour" all came from midnight as well. It
  now falls back to the *last* hour the block actually contains — the nearest
  available reading — instead of the start of the day.
- **The focus-restore window was measured on the wall clock.** Every other
  elapsed-time test in the app moved to the monotonic clock in 1.3, but the
  four-second window that keeps a re-render from stealing focus still compared
  `Date.now()` with a `Date.now()` deadline. A device whose clock the network
  corrected backwards (a cold boot that guessed the date, a manual change) kept
  that "few seconds" window open for as long as the skew lasted, so a background
  refresh ten minutes later moved focus to the city button out from under a
  screen-reader user; a clock corrected forwards closed the window before the
  re-render it was meant for, and focus was dropped to `<body>` after all. The
  window now uses the same `mono()` clock as the cache TTL and the refresh
  interval.

### Notes
- No visual change: the rendered `#main` is byte-identical to 1.3.6 in seven
  states (22:07 and 10:12 local, 00:05 just after midnight, 23:59, a New York
  city read from an Indian device, a London DST-transition night, and a Sydney
  city read from an Indian device) — same markup hash, same 248 nodes, same
  hour labels, same "Today" row and weekday labels, identical computed styles of
  14 key elements, zero console errors in every state.
- Targeted checks, old file against new: with an hourly block that ends at 02:00
  the "Now" cell goes from 20° (midnight) to 23° (the newest hour it has); with a
  `current` block that has no `time` the screen goes from the offline card to the
  full forecast; with the clock corrected 20 s backwards the focus window no
  longer restores focus (it does with the clock corrected forwards), while a
  hold taken a moment ago is still honoured.
- Left alone deliberately: the "Today" label on the 7-day list stays index-based.
  A payload left on screen across midnight shows yesterday as "Today", but the
  only thing that could be compared against is the payload's own `current.date`
  (stale in exactly that case) or the device's date (wrong for a city in another
  timezone, e.g. New York seen from India at 00:30), so a "fix" here would trade
  a rare wrong label for a common one.
- `versionCode 15` / `versionName 1.3.7` in `AndroidManifest.xml` and
  `build.sh`, same signing key. `android/assets/index.html` is byte-identical to
  `web/index.html` (verified with `cmp`). The APK artifact itself was **not**
  rebuilt by this pass — the maintenance run had no Android SDK or JDK available
  — so the published `LiquidWeather.apk` and `CHECKSUMS.txt` are unchanged and
  still match each other; CI builds 15/1.3.7 from these sources on push.

## [1.3.8] — 2026-11-03

### Fixed
- **"Today" sat on yesterday's row, and the day's high, low and UV came from
  yesterday.** The 7-day list labelled its first row "Today" by position, and
  the hero's `H:`/`L:`, the summary's "High of … and a low of …" and the UV card
  all read `daily[0]`, on the assumption that Open-Meteo's daily block always
  starts on the city's current date. It does not, for the first hour or so after
  local midnight: at 00:05 IST on 3 November a fresh Mumbai payload carries
  `current.time` 2026-11-03T00:00 while `daily.time` still starts 2026-11-02 (the
  same happens at 00:15 in Kathmandu; by 02:30 in Singapore the API has caught
  up). The app then showed "Today" over Monday's weather with today — Tuesday —
  labelled "Tue", and read the hero, summary and UV card from Monday: Mumbai
  displayed a low of 27° when the coming night's low was 26°, and its UV card
  carried Monday's 6.8 instead of Tuesday's 6.75. The row that is today is now
  found by comparing `daily.time` with the date in the payload's own
  `current.time` (`todayIndex()`), which is right for the city whether the
  payload is fresh or stale, and the label, hero, summary and UV card all follow
  it.

### Notes
- No visual change outside that window: with the payloads for London, New York,
  Sydney and Kiritimati (all fetched live, all with `daily[0]` equal to the
  city's today) the rendered `#main` is byte-identical to 1.3.7 — same markup
  hash, same labels, same hero. Only the payload whose daily block starts on
  yesterday changes, and there it changes to the correct row: the list reads
  `Mon, Today, Wed, …`, the hero low goes 27° → 26° and the summary follows.
- Zero console errors in every state, `node --check` clean on the extracted
  script. Payloads with no `current.time`, and stale payloads whose daily block
  does not contain today at all, resolve to row 0 exactly as before (identical
  markup hash), so nothing regresses when the clock is missing.
- Left alone deliberately: an hourly block that stops before the current hour
  still fills the remaining cells with its last hour (a truncated block shows the
  same hour repeatedly), `null` values in the hourly arrays still render as 0°,
  and a malformed `daily.time` entry still prints "Invalid Date". All three need
  a broken payload rather than a broken clock, so they belong to the payload
  validation pass, not this one.
- Left alone deliberately: a duplicate wall-clock hour on a DST fall-back day
  would be matched to its first occurrence. Checked against the live API: on
  1 November 2026 in New York the hourly block carries one entry per wall-clock
  hour (00:00 … 23:00, 24 entries) with a single `utc_offset_seconds`, so no
  duplicate is ever served and there is nothing to disambiguate.
- `versionCode 16` / `versionName 1.3.8` in `AndroidManifest.xml` and
  `build.sh`, same signing key. `android/assets/index.html` is byte-identical to
  `web/index.html` (verified with `cmp`). The APK artifact was **not** rebuilt by
  this pass — the maintenance run had no Android SDK or JDK available — so the
  published `LiquidWeather.apk` and `CHECKSUMS.txt` are unchanged and still match
  each other; CI builds 16/1.3.8 from these sources on push.

## [1.3.9] — 2026-11-03

### Fixed
- **A resize event reallocated the particle canvas even when nothing had
  resized.** `size()` is bound to `resize`, and a phone browser fires that event
  every time its URL bar hides, the on-screen keyboard opens, or a WebView
  reports a viewport change — none of which move the canvas. Each event
  reassigned `canvas.width`/`height`, which throws away and reallocates the whole
  backing store (430×900 at DPR 2 is about 3 MB of pixels), blanks whatever was
  drawn, and re-seeded every particle. `size()` now measures first and returns
  when the box, the device pixel ratio and the backing store are the ones it
  already has. Measured in headless Chromium: ten `resize` events that changed
  nothing went from ten `canvas.width` assignments and 20 828 `Math.random()`
  calls (twenty particle sets built and thrown away) to zero and 47.
- **Every re-render re-randomised the whole particle field.** `render()` calls
  `scene()`, `scene()` calls `seed()`, and `seed()` rebuilt the particle array
  unconditionally — so toggling °C/°F, or the ten-minute background refresh
  landing on the same weather, teleported every raindrop and snowflake to a new
  random position under the reader's eyes and allocated a fresh array of up to
  260 objects each time. The set is now keyed by the scene and the canvas size
  and only rebuilt when one of those actually changes. Measured: a unit toggle
  went from 683 `Math.random()` calls to 7, a same-scene refresh from 690 to 11,
  while a real scene change (rain → thunderstorm) and a real canvas resize still
  rebuild it (1 049 and 1 081 calls, unchanged).
- **The parallax engine forced a layout on every pointermove.** The handler
  measured `.phone` with `getBoundingClientRect()` on each pointer event, and
  because the frame before had just written `--mx`/`--my` on the root the style
  was dirty, so every read flushed a fresh layout — at the pointer's full event
  rate, which on a 120 Hz screen is 120 forced layouts a second while the finger
  moves. The box is now measured once and dropped on `resize` and
  `orientationchange`. Measured: 100 pointermove events went from 100 box reads
  to 1, and the `--mx`/`--my` values written for four fixed pointer positions
  (and again after a viewport change) are byte-identical to 1.3.8.

### Notes
- No visual change: the rendered `#main` is byte-identical to 1.3.8 in eleven
  states — clear, cloudy, overcast, fog, rain and snow by day, clear, rain and
  thunderstorm by night, a thunderstorm with *Reduce motion* on, and the offline
  card — same markup hash, same 222 nodes (111 on the offline card), same canvas
  size, identical computed styles of twelve key elements, zero console errors in
  every state (`node --check` clean on the extracted script).
- The scene's particles, counts, speeds and timings are untouched: what changed
  is when they are rebuilt, not what is drawn.
- `versionCode 17` / `versionName 1.3.9` in `AndroidManifest.xml` and
  `build.sh`, same signing key. `android/assets/index.html` is byte-identical to
  `web/index.html` (verified with `cmp`). The APK artifact was **not** rebuilt by
  this pass — the maintenance run had no Android SDK or JDK available — so the
  published `LiquidWeather.apk` and `CHECKSUMS.txt` are unchanged and still match
  each other; CI builds 17/1.3.9 from these sources on push.
- Left alone deliberately: the backdrop blur on the glass cards (`blur(22px)` on
  ten cards plus the nav and the sheet) is the single largest paint cost in the
  app, but cutting it or reducing the blurred area would visibly change the glass
  — it stays as it is, and the Blur slider is the user's own control over it.
- Left alone deliberately: `--mx`/`--my` are still written while *Parallax* is at
  0, where every transform multiplies them away. Skipping that needs a hook from
  `applySettings()` into the depth engine (and a flush when the slider comes back
  up); it is a real saving but only at one slider position, so it is noted rather
  than rushed.

## [1.3.10] — 2026-11-03

### Fixed
- **Tab walked out of the *Glass & motion* panel into the page behind the
  scrim.** The panel floats above a scrim that covers the page, and the scrim
  stops the pointer, but the page itself stayed in the tab order: from *Reset to
  default* the next Tab left the panel and landed on the city button, the °C/°F
  toggle and the hourly strip, all of them dimmed behind the scrim and none of
  them visible where the focus ring was. Measured in headless Chromium, ten Tab
  presses with the panel open reached three controls inside `#main`. `#main` is
  now `inert` while the panel is open and comes back to the tab order when it
  closes — the treatment the search sheet already had — so the same ten presses
  now reach nothing behind it (the nav stays live, because it sits above the
  scrim and is how you leave the panel).
- **Every slider in the panel was announced with no name at all.** Each one is
  wrapped in `<label class="rowr">`, but `<output>` is a labelable element and
  sits before the range inside that label, so the label bound itself to the
  output: `input.labels.length` was 0 for all five ranges, and the accessibility
  tree showed five sliders named "" at 50, 50, 70, 60 and 55. A screen-reader
  user could not tell Transparency from Parallax, Depth from Blur. Each range
  now carries an `aria-label` matching the label printed beside it, so the tree
  reads Transparency, Blur, Bounce, Depth and Parallax; the `<output>` keeps its
  own association, so the live percentage is unchanged.

### Notes
- No visual change: with the same payload and a fixed random seed, the rendered
  page and the open panel are **pixel-identical** to 1.3.9 (430×900 at DPR 2,
  `prefers-reduced-motion` so nothing is mid-animation), `#main`'s markup is
  byte-identical, and `#set`'s markup differs only by the five new `aria-label`
  attributes. Computed styles of the hero, cards, nav, panel and sliders are
  unchanged.
- Zero console errors in every state checked — loaded, search sheet open,
  settings panel open, offline card, offline retry by Enter, a typed search —
  and `node --check` clean on the extracted script.
- `versionCode 18` / `versionName 1.3.10` in `AndroidManifest.xml` and
  `build.sh`, same signing key. `android/assets/index.html` is byte-identical to
  `web/index.html` (verified with `cmp`). The APK artifact was **not** rebuilt by
  this pass — the maintenance run had no Android SDK or JDK available — so the
  published `LiquidWeather.apk` and `CHECKSUMS.txt` are unchanged and still match
  each other; CI builds 18/1.3.10 from these sources on push.
- Left alone deliberately: the 7-day rows read "Today ⛅ 22° 32°" with nothing to
  say which figure is the low and which the high. Naming them needs a role (an
  `aria-label` on a bare `<div>` is not exposed) and that changes the structure
  the rows are announced in, so it is noted for a pass that can decide the
  markup rather than rushed here.
- Left alone deliberately: white text at `--tx2` (72% opacity) over the light
  end of the *Snow* and *Clear* day gradients is the weakest contrast in the app,
  and the white focus ring is hard to see over those same scenes. Any fix
  changes colours or the ring, which this programme forbids.
- Left alone deliberately: the ✕ in a search row is a `role="button"` span
  nested inside the row's `<button>`, which is interactive content inside a
  button. It is exposed and reachable (checked in the accessibility tree and the
  tab order), and separating the two means restructuring the row, so it waits.

## [1.4] — 2026-11-03

### Fixed
- **On any fractional device pixel ratio the canvas was still reallocated on
  every resize event.** `size()` compares the box, the ratio and the backing
  store before it touches `canvas.width`, but it compared the stored attribute
  with the *fractional* product `w * dpr`. `canvas.width` is an unsigned long,
  so assigning 430 × 1.25 stores 537, and `537 === 537.5` is never true: on a
  screen at 125% or 150% scaling (Windows at 125%, any browser zoom, a DPR of
  1.25 or 1.75) the guard never matched, and each resize event — the URL bar
  hiding, the keyboard opening — threw away and reallocated the whole backing
  store again, which is the exact work the guard was added for. The comparison
  is now made against the integer that is actually stored (`Math.trunc(w * dpr)`),
  so nothing is assigned differently; only the test is right. Measured in
  headless Chromium at DPR 1.25: ten no-op `resize` events went from ten
  `canvas.width` assignments to zero, with the canvas still 537 × 1125.

### Changed
- **The particle canvas submitted one path and one paint per drop.** Every
  raindrop called `beginPath`/`moveTo`/`lineTo`/`stroke` of its own, every
  snowflake `beginPath`/`arc`/`fill` of its own, and `strokeStyle`, `lineWidth`
  and `fillStyle` were re-assigned inside the loop although they never change
  within a frame: 1 020 canvas calls for a 170-drop rain frame, 1 560 for a
  260-drop thunderstorm, 440 for a snow frame, at 60 frames a second. The
  geometry is now submitted as one path per frame and painted with a single
  stroke or fill — 344 calls for rain, 524 for thunderstorm, 223 for snow —
  and the style is set once. Measured on a seeded particle field in headless
  Chromium, the cost of recording a frame fell from 0.096 to 0.029 ms for rain,
  0.280 to 0.099 ms for thunderstorm and 0.538 to 0.145 ms for snow (third
  smallest of fifteen 200-frame batches, three runs each). Particle positions,
  speeds, counts, colours, line width and the star field's per-star alpha are
  untouched.

### Notes
- This is the day's release and carries the day's earlier fixes: the 7-day list,
  hero, summary and UV card now find the row that is actually today instead of
  assuming it is `daily[0]` (1.3.8); a resize event no longer reallocates the
  canvas or re-seeds the particles when nothing moved, and the parallax engine
  no longer forces a layout on every pointermove (1.3.9); Tab stays inside the
  *Glass & motion* panel and its five sliders have names (1.3.10).
- No visible change to the page. With the same payload the rendered `#main` is
  byte-identical to 1.3.10 (same markup hash, 222 nodes), so is the settings
  panel and the search sheet, the computed styles of the hero, cards, nav,
  summary and 7-day range bar are identical, and a full-page screenshot at
  430 × 900 with *Reduce motion* is pixel-identical.
- The particles are drawn from the same geometry: over forty seeded frames the
  `moveTo`/`lineTo` sequence for rain and thunderstorm and the 4 400 `arc`
  coordinates for snow are identical to 1.3.10. What differs is how the
  translucent layer is rasterised where two drops overlap — one stroke per frame
  blends the overlap once instead of twice — so 0.2% (snow) to 1.1%
  (thunderstorm) of the canvas's pixels differ, all of them in alpha and none by
  more than 64/255; no position, size, colour or timing changed.
- Zero console errors in every state checked — loaded, search sheet open,
  settings panel open, °C/°F toggled, parallax slider dragged to 0 and back, and
  the offline card — and `node --check` clean on the extracted script.
- `versionCode 19` / `versionName 1.4` in `AndroidManifest.xml` and `build.sh`,
  same signing key. `android/assets/index.html` is byte-identical to
  `web/index.html` (verified with `cmp`), and the APK in the repo and on the
  release page is CI's `Build APK` run for this commit: its bundled
  `assets/index.html` matches the source byte for byte, it reports 19 / 1.4, it
  is signed with the project's key (certificate SHA-256
  `2035d69f…9e3b8b`, unchanged), and its digest is the one in `CHECKSUMS.txt`.
- Left alone deliberately: the backdrop blur on the glass cards is still the
  largest single paint cost, and reducing it would visibly change the glass.
- Left alone deliberately: toggling °C/°F still rebuilds the whole of `#main`
  rather than updating the numbers in place. Doing that properly means keeping
  the entry animation and the held focus working across a partial update, which
  is a restructure rather than a fix, so it is noted.
- Left alone deliberately: the parallax engine still writes `--mx`/`--my` when
  the value it computes is the one already on the root (a scroll past the
  700 px clamp, a slider at 0). Skipping the write needs a hook from
  `applySettings()` into the depth engine and a flush when the slider comes back
  up; the saving is real but smaller than the canvas work above.
- Left alone deliberately: `placePill()` reads `offsetWidth`/`offsetLeft` on
  every `nav()`, which forces a layout. It runs on city changes and panel opens
  only, not per frame.

## [1.4.1] — 2026-11-04

### Fixed
- **An unrecognised weather code was described as "Partly cloudy with a few
  sunny spells" while the rest of the screen said cloudy.** The summary card
  picked its cloudy sentence with a two-way test — `code === 3 ? overcast :
  partly cloudy` — so every code that was not exactly 3 fell into the "partly
  cloudy" arm. Only 2 and 3 reach that arm from the WMO table, but an
  unrecognised code does too, and 1.3.2 had already made the hero ("Cloudy"),
  the sky (`bg-*-cloud`) and the icons (☁️) agree with each other for such a
  code: the summary card was the one place left contradicting them, and at
  night it promised sunny spells after dark. The sentence is now chosen from the
  code itself — overcast for 3, partly cloudy for 2 — and anything else falls
  back to the generic "Mixed conditions." the function already uses when it has
  nothing better to say.

### Notes
- No visual change for any real forecast: all 28 documented WMO codes, day and
  night (56 states, fixed payload), render a byte-identical `#main` before and
  after — same markup hash — checked in headless Chromium by calling the app's
  own `render()` against each payload. For codes 4, 68, 69, 100, 200 and 300 the
  summary now reads "Mixed conditions." beside the hero's "Cloudy", the cloudy
  sky and the ☁️ icons, where it previously read "Partly cloudy with a few sunny
  spells."
- Zero console errors in a full headless load (intercepted forecast response):
  initial paint, °C/°F toggle, search sheet open and close, settings panel open,
  a blur slider dragged and released, Escape to close — and `node --check` clean
  on the extracted script.
- `versionCode 20` / `versionName 1.4.1` in `AndroidManifest.xml` and
  `build.sh`, same signing key (certificate SHA-256 `2035d69f…9e3b8b`).
  `android/assets/index.html` is byte-identical to `web/index.html`, the APK
  built from this tree bundles that same file byte for byte (`cmp`), reports
  20 / 1.4.1, and its digest is the one in `CHECKSUMS.txt`.
- Left alone deliberately, because the only fix is visible wording: code 2 at
  night still reads "Partly cloudy with a few sunny spells"; 63 to 67 at night
  still say "Steady rain through the day"; code 80 ("Light showers") still says
  "heavy at times", and 77 (snow grains) and 85 (snow showers) still say "Heavy
  snow falling and settling" because the snow sentence is chosen with
  `code >= 75`.
- Left alone deliberately, because icon choices are frozen: 85 and 86 draw 🌨️ at
  night where 71 to 77 draw ❄️, and the 7-day rows always use the daytime glyph
  (the daily block carries no `is_day`).
- Left alone deliberately: `usableForecast()` still does not check that the
  hourly `weather_code` / `is_day` arrays are as long as `hourly.time`, so a
  truncated payload paints ☁️ and "NaN°" past the point where the arrays stop.
  That is a payload-validation gap (network area), not a code-coverage one, and
  it is noted for that pass.

## [1.4.2] — 2026-11-04

### Fixed
- **The app kept working in the background after you left it.** The activity
  never told its WebView that it had been paused: `MainActivity` had no
  `onPause()`/`onResume()`, so `WebView.onPause()` — the documented call that
  pauses layout, parsing and JavaScript timers for a WebView that is not
  visible — was never made. Everything the page keeps running therefore kept
  running while the app sat in the background: the 60-second forecast re-check
  (`setInterval(autoRefresh, 60 * 1000)`), the WebView's layout and parsing
  work, and the compositor animations (drifting clouds, the pulsing sun, the
  shimmer on a loading card) went on waking the device for as long as the
  activity was stopped instead of only while it was on screen. The two
  overrides now bracket the activity's life and hand the pause to the WebView;
  `onResume()` restores the timers, and the page's own `visibilitychange`
  handling starts the particle loop again exactly as it did before.
- **The WebView was destroyed while it was still attached to the window.**
  `onDestroy()` called `web.loadUrl("about:blank")` and then `web.destroy()` on
  a WebView that was still the activity's content view, which the platform
  documents as unsupported (it logs *"WebView.destroy() called while still
  attached"* and leaves the compositor and the native `AwContents` tied to a
  window that is being torn down), and it started a fresh navigation on a
  WebView that was one line away from being destroyed. Teardown now removes the
  view from its parent, stops the load in flight, then destroys, and drops the
  reference.
- **A location prompt left open when the activity went away held its callback.**
  `geoCallback` (and with it the WebView) stayed referenced until the activity
  was collected, and the page's `getCurrentPosition()` was never answered.
  `onDestroy()` now hands the callback back as a refusal — the same answer a
  denied prompt gives, which the page already handles by falling back to a
  city — and clears it.

### Notes
- Nothing visible changes: no layout, colour, wording, timing or feature is
  touched, and `web/index.html` is not modified by this entry.
- `versionCode 21` / `versionName 1.4.2` in `AndroidManifest.xml` and
  `build.sh` (up from 20 / 1.4.1), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is still
  byte-identical to `web/index.html`, the APK built from this tree bundles that
  same file byte for byte (`cmp` on the extracted asset), reports 21 / 1.4.2,
  and its digest is the one in `CHECKSUMS.txt`.
- Verified: `javac`/`d8` clean, `apksigner verify` green with the same
  certificate, and the shipped `classes.dex` disassembles to the intended
  bodies — `MainActivity.onPause` → `WebView.onPause`, `onResume` →
  `WebView.onResume`, and `onDestroy` in the order
  `GeolocationPermissions$Callback.invoke` → `getParent` → `removeView` →
  `stopLoading` → `destroy` → `super.onDestroy`.
- Left alone deliberately: a second location prompt raised while the first is
  still open overwrites `geoCallback`, so the first request goes unanswered
  until the page's own 15-second watchdog settles it. It needs a double tap on
  "Use my current location" and the watchdog already covers it, so it was noted
  rather than changed.
- Left alone deliberately: the web app's memory and lifecycle path itself was
  re-audited (listeners, timers, canvas backing store, visibility transitions)
  and found clean — 31 event listeners and 222 DOM nodes before and after 25
  search-sheet/settings cycles and 200 re-renders, no `requestAnimationFrame`
  callbacks while hidden, no canvas reallocation on a no-op resize.

## [1.4.3] — 2026-11-04

### Fixed
- **"Use my current location" could leave the spinner turning for good.** The
  button in the city sheet repaints the "Loading forecast…" skeleton and then
  asks the device for a position. When the request came back without one — the
  permission denied, the 12-second deadline missed, a device with no GPS — the
  failure path only repainted the screen if the pinned row had *no* coordinates
  yet (`if (!hasFix(el)) fallbackPlace()`). A row that already carried a fix
  from an earlier launch therefore kept the skeleton on screen: `--°`, a
  spinning ring, no forecast, no retry card, nothing to tap. The forecast for
  the coordinates the row already held is now drawn again, exactly as a
  successful request would draw it — cached and instant when the cache is
  warm, the usual offline card when it is not.
- **A superseded location request could rename the place.** `locate()` guards
  the coordinates of an older request with a sequence number, but the write
  that follows the reverse geocoder had no such guard. Tapping "Use my current
  location" twice — the first fix still being named when the second arrives —
  let the older request finish last and stamp its own city name over the newer
  fix: the pinned row, the Cities list and the toast said the place you had
  just left while the forecast on screen was the one for where you now are.
  A request that is no longer the newest one now returns before it writes the
  name, so the newest fix owns the name as well as the coordinates.

### Notes
- Nothing visible changes: no layout, spacing, colour, typography, gradient,
  glass value, wording or animation timing is touched. Both changes live on
  paths that only run when a location request fails or is overtaken.
- Verified in headless Chromium against the previous file with the network and
  the geolocation API stubbed: the normal load renders byte-identical `#main`
  markup and identical computed state, with no console error and no unhandled
  rejection in either build. The first bug reproduces on the old file
  (`--°` / "Loading forecast…" / spinner still up 900 ms after a denied
  request on a row that already had a fix) and is gone on the new one (27° /
  "Partly cloudy"). The second reproduces as `name: "Pune"` beside
  `lat: 19.076` — the newer Mumbai coordinates under the older Pune name — and
  is gone on the new one (`name: "Mumbai"`, `lat: 19.076`).
- `versionCode 22` / `versionName 1.4.3` in `AndroidManifest.xml` and
  `build.sh` (up from 21 / 1.4.2), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical
  to `web/index.html`, the APK built from this tree bundles that same file
  byte for byte, reports 22 / 1.4.3, and its digest is the one in
  `CHECKSUMS.txt`.
- Left alone deliberately: `getCurrentPosition` is still called with
  `maximumAge: 10 * 60 * 1000`, so a fix the platform cached up to ten minutes
  ago is accepted. That is what makes a second tap feel instant, and changing
  it would alter how long "Use my current location" takes on every device.
- Left alone deliberately: the toast wording on both failure paths, which the
  frozen UI rules cover.

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

## [1.5] — 2026-11-04

### Fixed
- **Reduce motion was read once at launch, so a device that changed the setting
  kept the answer it gave on the first run.** The particle field is the one
  animation CSS cannot switch off — clouds, the sun, spinners, skeletons and
  the entry animations all follow `prefers-reduced-motion` through their own
  media queries — so the frame loop consults the setting itself. It consulted
  it exactly once, at load. Turn “Remove animations” on while the app was in
  the background and rain, snow and stars went on falling for the rest of the
  session; turn it off and the particles never came back, because the loop had
  already stopped and only a scene change or a return from the background could
  start it again. The media query is watched now: switching it on clears the
  field with one last frame — the same blank canvas a launch with the setting on
  shows, rather than a frozen frame of rain — and switching it off starts the
  loop again.
- **A place the device had been located in left a failure marker behind for the
  rest of the session.** When a fix lands, the pinned row is re-keyed by its
  coordinates and the forecast cached under the old key is dropped
  (`delete cache[wasId]`). The `preFail` map — which remembers a pre-fetch that
  failed, so the next render skips a second 12-second deadline — was keyed the
  same way and never pruned, so every location whose forecast failed to
  download added one entry that nothing removed. It is pruned with the cache
  now.

### Notes
- Nothing visible changes: layout, spacing, colours, typography, gradients,
  glass values, wording and animation timings are untouched. Both fixes live on
  a media-query change handler and on the location-failure path; the rendered
  `#main` for the default (no Reduce motion) path is byte-identical to 1.4.4.
- Verified in headless Chromium against the 1.4.4 file with the forecast and
  geocoding APIs stubbed: the loaded, skeleton and offline screens render
  byte-identical `#main` markup and **0 differences across 680 computed-style
  checks** (34 elements × 20 properties, sampled after every entry animation had
  finished), a full interactive pass (unit toggle, search, add city, slider,
  settings) logs zero console errors, and `node --check` is clean on the
  extracted script.
- Targeted checks, each on both files: with the forecast endpoint answering
  503 and four successive location fixes, `preFail` held five keys on 1.4.4 and
  holds one (the current fix, matching the pruned cache) on 1.5. Switching
  `prefers-reduced-motion` on at runtime in a rain scene left the frame loop
  running at 14 rAF/s on 1.4.4 with the canvas still changing every frame, and
  stops it at 0 rAF/s on 1.5 with a cleared, static canvas; switching it off
  again restarts the loop (0 → 6 rAF/s).
- `versionCode 24` / `versionName 1.5` in `AndroidManifest.xml` and `build.sh`
  (up from 23 / 1.4.4), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html`.
- Left alone deliberately: the lightning flash still runs under Reduce motion.
  It is a Web Animations call, not a CSS animation, so no media query reaches
  it — but silencing it would visibly change the thunderstorm scene for those
  users, and the UI is frozen; noted for a future release.
- Left alone deliberately: the 60-second refresh interval is still armed while
  the app is in the background (`WebView.onPause()` stops rendering, not JS
  timers). `WebView.pauseTimers()` would stop it, but it is a process-wide call
  and there is no way to verify it here without an Android device.
- Left alone deliberately: a second `onGeolocationPermissionsShowPrompt` still
  overwrites a pending callback instead of answering the first one. Two prompts
  cannot overlap in practice — the page asks once at a time — and the page's own
  15-second watchdog already covers the hang.

## [1.5.1] — 2026-11-05

### Fixed
- **The parallax engine kept recalculating the whole document for a value that
  had not moved.** `flush()` wrote `--mx` and `--my` on the root element on every
  animation frame that the pointer, the tilt sensor or the scroll position asked
  for, whether or not the numbers had changed. A finger resting on the glass, a
  mouse that has stopped, and a page scrolled past the end of its range (the
  scroll term is clamped at −1 after 700px) all produce the same two numbers
  frame after frame. Those are inherited custom properties, so each write
  invalidates the style of the entire document and with it the transforms of the
  sky, the clouds, the particle layer, ten glass cards and the nav — for a value
  that is already on the element. The rounded value is now compared with the one
  last written and the write is skipped when it matches.
- **Reduce motion was still read once at load, for the depth engine.** 1.5 made
  the particle field follow the setting at runtime; the parallax engine was left
  sampling it at load, in both directions. Switched on while the app was open,
  the engine went on queueing a frame and writing both custom properties every
  frame while the stylesheet forces `transform: none` on every layer it drives,
  so all of that work recalculated styles that could not move anything.
  Switched off, the engine had already returned at load and the parallax never
  came back for the rest of the session. It now watches the same media query the
  particle field watches: a change to `reduce` cancels the pending frame and
  stops the writes, and a change back to `no-preference` resumes them. The iOS
  sensor prompt is armed only while the effect is running, so a device with
  Reduce motion on is not asked for gyroscope data it will not use.

### Notes
- Nothing visible changes. The rendered `#main`, `#nav` and `#bgs` markup is
  byte-identical to 1.5 and **0 differences across 342 computed-style checks**
  (19 elements × 18 properties, sampled once the entry and card transitions had
  settled); the parallax values themselves are unchanged — four pointer
  positions (0.1/0.2, 0.9/0.8, 0.5/0.5, 0.25/0.75 of the phone box) give
  exactly the same `--mx`/`--my` pairs on both files. A launch with Reduce
  motion already on renders byte-identically too (`#bgs`, `.card` and `#nav`
  all `transform: none`, `--mx` unset).
- Verified in headless Chromium against the 1.5 file with the forecast and
  geocoding APIs stubbed: `node --check` clean on the extracted script, zero
  console errors on load, after a pointer burst, a scroll burst and a unit
  toggle.
- Targeted checks, each on both files. Thirty pointermoves at one fixed
  coordinate made **60** `--mx`/`--my` writes on 1.5 and **2** on 1.5.1 (the
  first frame, which has nothing to compare against). Switching
  `prefers-reduced-motion` on at runtime in a rain scene: `--mx` went on
  changing (`0.0000` → `0.0033`) and the trace showed 41 style recalculations
  over 40 pointer frames on 1.5; `--mx` stays `0.0000`, the engine queues no
  frames and the trace shows 14 on 1.5.1. Switching it off again after a launch
  with it on left `--mx` empty and `#bgs` at `matrix(1.08,…)` on 1.5; on 1.5.1
  the engine starts and `#bgs` carries the translate again.
- `versionCode 25` / `versionName 1.5.1` in `AndroidManifest.xml` and
  `build.sh` (up from 24 / 1.5), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html`.
- Left alone deliberately: a drag across the nav still measures all three tab
  buttons with `getBoundingClientRect()` on every `pointermove`. Caching them
  would be wrong — the strip scrolls horizontally, so the boxes move — and the
  reads do not force a layout unless a style write has just landed, which only
  happens when the nearest tab changes.
- Left alone deliberately: the nine cloud elements keep their `drift` animation
  running while their opacity is 0. Pausing them would change the position a
  cloud reappears at when the scene asks for more clouds, which is a change to
  animation behaviour, not just cost; noted for a release that can re-check it
  on a device.

## [1.5.2] — 2026-11-05

### Fixed
- **One tab's saved city was thrown away by the other tab.** The saved list lived
  in local storage but every document kept its own copy in memory and wrote that
  copy out whole, so the tab that wrote last decided the list: with the app open
  in two tabs, tab A saved Mumbai, tab B — opened before that — saved Chennai,
  and Mumbai was gone at the next launch. A write made by another document now
  arrives as a `storage` event and is adopted through the same validation a cold
  load uses, so the two copies cannot drift apart. This document's own writes
  never raise that event, so a single tab behaves exactly as it did. When the
  adopted list still holds the city on screen nothing is repainted, so the entry
  animation is not replayed; when the other tab removed the city being viewed,
  the page moves to the row that took its place.
- **The saved list had no length limit when it was read back.** Every field of a
  stored row was validated, but the number of rows was not: a restored or
  hand-edited `lw_places` of 3,000 rows was accepted whole, and opening the
  Cities sheet built 3,008 rows and blocked the main thread for 3.4 s. Loading
  now applies the same ceiling `addPlace()` already enforces — at most one
  "My Location" row and five saved ones — which nothing reachable through the
  UI can exceed.

### Notes
- Nothing visible changes. The rendered `#main`, `#nav` and `#bgs` markup is
  identical to 1.5.1 and **0 differences across 342 computed-style checks**
  (19 elements × 18 properties).
- Verified in headless Chromium with the forecast and geocoding APIs stubbed:
  `node --check` clean on the extracted script, zero console errors on load.
- Targeted checks, each on both files. Two tabs, one adding Mumbai and one
  adding Chennai: storage held `New Delhi, Chennai` on 1.5.1 and
  `New Delhi, Mumbai, Chennai` on 1.5.2; removing Mumbai in the second tab
  removed it from the first tab's saved list too, with no resurrection.
  3,000 stored rows: the sheet built 3,008 rows in 3,373 ms on 1.5.1 and 13 rows
  in 89 ms on 1.5.2, while a legitimate five-city list still renders all of it
  (14 rows, unchanged). Corrupt `lw_places`, `lw_cur` and `lw_set` values, an
  empty array, an object instead of an array and a place at 0°/0° all still
  boot cleanly.
- `versionCode 26` / `versionName 1.5.2` in `AndroidManifest.xml` and
  `build.sh` (up from 25 / 1.5.1), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html` (same SHA-256 inside the built APK).
- Left alone deliberately: a failed write is still silent. When storage is full
  or blocked, `LS.set` swallows the error and a city the reader just saved is
  gone at the next launch; saying so needs a new message on screen, which the
  frozen UI does not allow — it is queued for a release that can add the words.
- Left alone deliberately: `lw_set` and `lw_unit` are not synced between tabs
  either. Two tabs changing different sliders still lose one of the two
  settings, but applying another tab's settings live would visibly change the
  glass under the reader, which is a UI change rather than a data fix.

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

## [1.5.4] — 2026-11-05

### Fixed
- **"Today" sat on yesterday's row for as long as a forecast from before the
  city's midnight stayed on screen.** `todayIndex()` reads the date out of the
  payload's own `current.time`, which is right for the city but stops moving the
  moment the payload does: a forecast cached at 23:55 is still drawn at 00:05
  (the cache holds ten minutes), and one whose refresh failed is drawn for as
  long as the reader leaves it there. The 7-day list kept labelling yesterday
  "Today", and the hero's `H:`/`L:`, the summary's high and low and the UV card
  all came from yesterday — measured on a payload carrying
  `current.time 2026-11-05T23:00` still on screen at 00:05, the list read
  `Today, Fri, Sat…` with a hero of `H:30° L:20°` and a UV card of 6 when the
  city's today was Friday, `H:31° L:21°`, UV 7. The payload's clock is now
  cross-checked against the city's own date, computed from the device's UTC
  clock plus the payload's `utc_offset_seconds` — the device's *timezone* cannot
  be used (a New York city read from India at 00:30 is still on the previous
  day there), but its UTC clock plus the payload's offset is the city's
  wall-clock date whatever timezone the device is set to. The later date is
  adopted only if the daily block actually contains it *and* the two clocks
  agreed on the payload's date when it was fetched, so a fresh payload, a
  payload without `utc_offset_seconds`, and a device whose clock is a day or a
  week out all render exactly as they did before.
- **Time spent asleep did not count as elapsed time, so the forecast could sit
  on screen for hours.** Every elapsed-time test in the app reads the monotonic
  clock, which is the right choice for a wall clock that gets corrected — but
  `performance.now()` does not tick while the device is asleep (Chrome reads
  `CLOCK_MONOTONIC`, which stops during suspend on Android and Linux). A phone
  that slept through the night came back looking as if no time had passed: the
  visibility handler saw "less than ten minutes since the last refresh" and
  skipped, the sixty-second interval saw the same and skipped again, and the
  forecast on screen stayed hours old until ten minutes of *awake* time had gone
  by. The same clock decided whether a cached payload was still fresh, so a city
  switched to after a sleep reused a payload from before it. Elapsed time is now
  the larger of the two clocks — the wall clock counts the hours spent asleep,
  the monotonic one still covers a clock corrected backwards, and both are
  compared against the same mark, so a single correction can cost at most one
  extra fetch.

### Notes
- Nothing visible changes. With a fresh payload the rendered `#main` is
  byte-identical to 1.5.3 in five scenarios (an Indian city at 18:05, a New York
  city read from an Indian device at 00:30, a payload with no
  `utc_offset_seconds`, a payload with no `current.time`, and a device clock six
  days fast) and **0 differences across 342 computed-style checks** (19 elements
  × 18 properties, sampled with animation and transition disabled).
- Verified in headless Chromium with the forecast and geocoders stubbed:
  `node --check` clean on the extracted script, zero console errors on load, and
  zero console errors through an interactive pass (°C/°F both ways, the settings
  panel and the search sheet opened and closed, all three tabs) — every step
  identical to 1.5.3.
- Targeted checks, each on both files. A payload carrying
  `current.time 2026-11-05T23:00` fetched at 23:55 and still on screen at 00:05
  after a failed refresh: the list goes from `Today, Fri, …` to
  `Thu, Today, …`, the hero from `H:30° L:20°` to `H:31° L:21°`, the UV card
  from 6 to 7, and the summary follows. Three hours of simulated sleep (the wall
  clock moved on, `performance.now()` frozen): returning to the app made **0**
  forecast requests on 1.5.3 and **1** on 1.5.4, and a plain re-render after the
  same sleep reused the three-hour-old cache entry on 1.5.3 (0 requests) and
  re-fetched it on 1.5.4 (1 request). A device clock six days fast changes
  nothing on either file.
- `versionCode 28` / `versionName 1.5.4` in `AndroidManifest.xml` and
  `build.sh` (up from 27 / 1.5.3), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html` and so is the copy inside the rebuilt APK (same SHA-256,
  `15735cf7…`), and `CHECKSUMS.txt` points at the new build.
- Left alone deliberately: the hourly strip still opens on the payload's hour
  when the city has crossed midnight since it was fetched, so the cell marked
  "Now" can be an hour behind the corrected "Today" row. Moving it would put the
  strip out of step with the hero's live `current` values on the same screen,
  and the honest fix is the refresh this pass restores, not a second guess at
  the hour.
- Left alone deliberately: a payload older than a day still labels its own first
  row "Today" once the date has fallen out of the daily block. There is nothing
  left to compare against at that point, and the refresh above is what stops a
  payload getting that old in the first place.

## [1.5.5] — 2026-11-06

### Fixed
- **The thunderstorm flash kept animating in the background.** The visibility
  handler stops the lightning chain when the app goes away, but it can only
  stop a chain that already exists: a forecast that finished downloading after
  the reader left — a city tapped and the phone put down, which is the ordinary
  way a fetch outlives the screen — ran `scene()`, which calls `lightning()`,
  and the timer was armed again for a page nobody was looking at. The
  backgrounded WebView then woke every 2.5–7.5s to start a 600ms flash
  animation on an invisible element, for as long as it stayed in the
  background, while the particle loop beside it correctly stayed stopped.
  `lightning()` now refuses to arm while the page is hidden, which is exactly
  the rule the visibility handler was already written to enforce; the handler
  starts the chain again on return. Measured on a storm city with the forecast
  landing while hidden: **4 flashes in 16s before, 0 after**, and 2 flashes in
  the 12s after coming back, as before.
- **A deleted city's forecast stayed in memory for the rest of the session.**
  The forecast cache and the pre-fetch failure map are keyed by the place id
  and nothing removed an entry: removing a city from the Cities sheet dropped
  the row and left its whole payload — current conditions, forty-eight hours
  and seven days, tens of kilobytes each — held for as long as the app stayed
  open, with no row left that could ever read it again. `locate()` already
  pruned by hand when a row took a new key; the same rule now lives in one
  `pruneCache()` that both the removal and the other-tab adoption path call.
  Measured with five cities visited and two of them deleted: the cache went
  from **5 entries / 14 957 bytes to 3 entries / 8 982 bytes**.

### Notes
- Nothing visible changes: the rendered `#main` is byte-identical to 1.5.4 and
  there are **0 differences across 594 computed-style checks** (33 elements × 18
  properties), the only sampled difference being the phase of the sun's 6s
  pulse. `node --check` is clean on the extracted script, and a headless load
  with the forecast stubbed reports zero console errors on both files, as does
  an interactive pass (°C/°F both ways, the Cities sheet opened, searched and
  closed, the *Glass & motion* panel with a blur change, all three tabs) with
  identical results on 1.5.4 and 1.5.5.
- `versionCode 29` / `versionName 1.5.5` in `AndroidManifest.xml` and
  `build.sh` (up from 28 / 1.5.4), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html`, and so is the copy inside the rebuilt APK (same SHA-256,
  `b5f6f79c…`); `CHECKSUMS.txt` points at the new build.
- Left alone deliberately: the sixty-second refresh interval still ticks while
  the page is hidden. It returns immediately unless the page is visible, so it
  costs one no-op wake a minute, and the activity already pauses the WebView
  (`onPause`); stopping and restarting it on every visibility change would add
  a second place for the ten-minute staleness rule to go wrong for no real
  saving.
- Left alone deliberately: a fetch that is still in flight when its city is
  deleted writes its payload into the cache after the prune has run, so that one
  entry survives until the session ends. Cancelling it instead would mean
  aborting a request the reader may still be waiting for on another tab of the
  sheet, and it is a single entry, not one per deleted city.

## [1.5.6] — 2026-11-06

### Fixed
- **A city already in the list could be saved a second time.** Every place is
  keyed by `pid()`, which rounds its coordinates to three decimals (~110 m), and
  the search rows tested that key against the stored id. Two providers place the
  same city on slightly different coordinates — the bundled Mumbai sits at
  19.076, 72.8777 and the fallback geocoder returns it at 19.0550, 72.8692, 2.5
  km apart — so a city picked from the bundled list was not recognised when a
  geocoder answered for it: the result row offered "add" instead of "saved", and
  tapping it stored the city twice, two of the five slots for one place and two
  rows of the same name in the Cities sheet. Measured: saving Mumbai from the
  bundled list and then picking the same city from the geocoder left
  `New Delhi, Mumbai, Mumbai` in the list on 1.5.5 and leaves `New Delhi,
  Mumbai` on 1.5.6.
- **The same city was listed twice inside one set of results.** `dedupe()`
  compared the rounded keys only, so a geocoder answering with one city under
  two near-by coordinate sets (a city row and its district row) put two
  identical rows in the sheet: searching "mumbai" with the geocoder returning
  19.076, 72.8777 and 19.0550, 72.8692 listed `Mumbai, Mumbai, Chennai` before
  and `Mumbai, Chennai` now.
- **The default New Delhi row never matched the bundled Delhi row.** The
  location fallback stores its row with a four-decimal id
  (`c28.6139,77.2090`) while every search row is keyed at three, so the two
  keys could never be equal: with the app showing New Delhi, the Popular list
  still offered to add Delhi at exactly those coordinates, and taking it stored
  a second row for the same point. The comparison now recomputes both keys at
  the same precision, so the Delhi row shows as saved (📍 with its ✕) instead.
  Both of these are one rule, `samePlace()`: two rows are the same place when
  their keys match, or when their folded names match and they lie within 25 km
  of each other — which holds for every bundled city against both geocoders
  (offsets measured at 0.6–10 km) and keeps same-named cities in different
  regions apart (Portland OR/ME 4000 km apart, the two Springfields 1100 km
  apart, both still listed and both still saveable as separate places).

### Notes
- Nothing visible changes: with a fresh forecast the rendered `#main` is
  byte-identical to 1.5.5 (3113 characters) and so is the sheet markup for 9 of
  10 probe queries; the tenth ("india") differs only by the Delhi row's 📍 and
  its ✕, which is the third fix above. `node --check` is clean on the extracted
  script and a headless load reports zero console errors on both files, as does
  an interactive pass (°C/°F both ways, the *Glass* tab with a slider change,
  the search sheet opened, searched, a city added and removed, all tabs) with
  identical results on 1.5.5 and 1.5.6.
- Verified in headless Chromium with the geocoders, the forecast API and the
  geolocation API stubbed, using the fallback geocoder's real coordinates for
  Mumbai, Portland, Springfield and Paris.
- `versionCode 30` / `versionName 1.5.6` in `AndroidManifest.xml` and
  `build.sh` (up from 29 / 1.5.5), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged. `android/assets/index.html` is byte-identical to
  `web/index.html`, and so is the copy inside the rebuilt APK (same SHA-256,
  `32a59ea0…`); `CHECKSUMS.txt` points at the new build.
- Left alone deliberately: a one-character query still never reaches a
  geocoder — it is answered from the bundled list only. Sending it would double
  the requests of an ordinary typing burst and the local list answers it well
  enough.
- Left alone deliberately: the bundled country prefix still matches more than
  the reader may mean — offline, "uk" resolves to Kyiv through "Ukraine" before
  anything else. Tightening that to country codes would change which results
  appear for a query, which is a behaviour change rather than a bug fix.

## [1.5.7] — 2026-11-06

### Fixed
- **The summary card described daylight at night.** Only the clear-sky sentence
  was ever told the time of day; the rest of the table was written for noon and
  used whatever the clock said. A city at 23:00 under partly cloudy skies (code
  2) read "Partly cloudy with a few sunny spells" beside a ☁️ icon on a night
  sky, overcast (3) read "with little direct sun", and steady rain (63–67) read
  "through the day" — all of it contradicted by the hero line, the icons and the
  night background drawn around it. The cloud and steady-rain sentences now
  follow `day`, exactly as the clear-sky one already did, so 23:00 reads
  "Partly cloudy overnight, with clearer spells at times", "Overcast overnight,
  with little clear sky" and "Steady rain through the night". Every daytime
  sentence these replace is unchanged.
- **Four codes were described as something they are not.** The intensity
  thresholds were coarse enough to contradict the hero label sitting above the
  card: light showers (80) were called "heavy at times" while the hero said
  "Light showers" and the icon drew 🌦️; heavy drizzle (55, and 57, dense
  freezing drizzle) was called "light rain"; and snow grains (77) plus snow
  showers (85, 86) all fell into one `code >= 75` branch and were called "Heavy
  snow falling and settling" — the heaviest sentence in the table — under a
  "Snow grains" / "Snow showers" hero. Each now gets the sentence its own WMO
  entry promises: "A few light showers passing through", "Heavy drizzle through
  the day/night", "Snow grains falling", "Snow showers passing through".
  Heavy snow (75), showers (81) and heavy showers (82) keep exactly what they
  said before.

### Notes
- Nothing visible changes apart from those sentences: for six probe scenarios
  (clear day, cloudy night, steady rain at night, light showers, thunderstorm,
  unknown code at night) the rendered `#main` is byte-identical to 1.5.6 with
  the summary text taken out, and the scene background, hero condition and all
  15 icons are unchanged. Across all 28 WMO codes plus an unknown code, day and
  night, **18 of 62 summary strings changed and no icon, condition label or
  scene key did**; the only computed-style difference found is `opacity` on the
  randomly seeded clouds, which the same old-vs-old baseline shows too.
  `node --check` is clean on the extracted script, and a headless load with the
  forecast stubbed reports zero console errors on both files.
- `versionCode 31` / `versionName 1.5.7` in `AndroidManifest.xml` and
  `build.sh` (up from 30 / 1.5.6), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1, v2 and v3
  schemes. `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `76057d2a…`) and so is the copy inside the rebuilt APK.
  `MainActivity.java` is untouched, so the packaged `classes.dex` is
  byte-identical to 1.5.6's (SHA-256 `de209f1f…`); the build ran the same
  aapt2 → zipalign → apksigner steps as `android/build.sh`, which cannot compile
  the Java in this pass's environment (no JDK compiler available), and the dex
  was carried over unchanged rather than recompiled. `CHECKSUMS.txt` points at
  the new build (`1d3e1c62…`).
- Left alone deliberately: "Drizzle" (53) and light freezing drizzle (56) still
  read "Light rain on and off", and freezing rain (66, 67) still reads "Steady
  rain". Saying "freezing" would need a new sentence and an ice warning the app
  does not have, and the existing wording is not wrong about the precipitation
  itself.
- Left alone deliberately: moderate snow (73) still reads "Light snow falling
  and settling" — understated, but not false, and rewriting it would change a
  sentence that was never contradicted by anything else on screen.
- Left alone deliberately: the 7-day strip still uses the daytime glyph for
  every row, including today. A daily row describes a whole day, so the
  night-time variants do not belong there.
- Left alone deliberately: the forecast request still asks for `precipitation`,
  `cloud_cover`, `sunrise`, `sunset` and `precipitation_probability_max`, none
  of which the renderer reads. Dropping them would shrink every payload, but
  that is the network pass's area, not this one.

## [1.5.8] — 2026-11-06

### Fixed
- **A location fix for a row that no longer existed was still written, named and
  cached.** `locate()` only ever asked whether a newer location request had
  superseded it. The pinned row itself can be gone by the time the fix arrives:
  a city picked from the search sheet takes the row over when it is the only
  place in the list and still has no fix, and another tab's saved list can
  replace it. The fix was written to the orphaned row anyway, so the app
  downloaded a forecast nobody could see, cached it under coordinates no row
  owned — where it stayed for the rest of the session — asked a geocoder to name
  a place nobody had asked about, and announced "Updated to your location" over
  a screen showing the city the reader had just picked. The two guards now also
  require the row to still be in the list.
- **A forecast could be cached under a key no row owned.** Both cache writes
  happen after an `await`, and the row can stop existing in between — a fix
  arriving for the pinned row re-keys it, the reader deletes a city, a picked
  city replaces the pinned row. `pruneCache()`'s rule (an entry survives only
  while its city is in the list) held at every delete but not at every write, so
  such a payload was stored and never read again. Both writes now prune, so the
  rule holds everywhere.

### Notes
- Measured on the previous build first: with a fix pending, picking a city from
  the sheet left `cache` holding `c18.520,73.857` beside a list of
  `c18.520,73.860`, cost two forecast requests instead of one and one
  reverse-geocode request for a row that no longer existed. After the change the
  same scenario ends with one cache entry, one forecast request and no geocoder
  request.
- Nothing visible changes: for a stubbed forecast, the rendered `#main`, `#nav`,
  the settings panel (closed and open) and the search sheet are byte-identical
  to 1.5.7, and so is the scene state (`mode`, particle count, background
  classes, `--cc`). No CSS, markup, wording or timing was touched.
- No leak was found in the rest of the area this pass covered: over 40 searches,
  40 forced re-renders, 20 panel cycles, 15 add/remove cycles and 8 locate
  cycles the live listener count, node count and JS heap all plateau (listeners
  56, heap ≈1.84 MB, no orphan nodes after GC), no timer is left pending at rest,
  and with the page hidden the particle loop and the lightning chain both stop
  and pick up again on return.
- `node --check` is clean on the extracted script; a headless Chromium load
  reports zero console errors.
- `versionCode 32` / `versionName 1.5.8` in `AndroidManifest.xml` and
  `build.sh` (up from 31 / 1.5.7), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1, v2 and v3
  schemes. `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `097635b7…`) and so is the copy inside the rebuilt APK.
  `MainActivity.java` is untouched, so the packaged `classes.dex` is
  byte-identical to 1.5.7's (SHA-256 `de209f1f…`). `CHECKSUMS.txt` points at the
  new build (`81df4ef2…`).
- Left alone deliberately: the `setInterval(autoRefresh, 60 * 1000)` still ticks
  in the background, throttled by the browser and returning immediately unless
  the page is visible. Replacing it with a timer that is armed on return would
  be tidier but changes nothing measurable.
- Left alone deliberately: `getPosition()`'s losing 2.5 s `GEO_NAME_WAIT` timer
  is not cleared when the geocoder answers first. It fires once, resolves an
  already-settled `Promise.race` and is gone; no timer survives at rest.

## [1.5.9] — 2026-11-06

### Fixed
- **A forecast request outlived the screen that started it and painted over the
  next one.** Only `show()` ever invalidated a pending forecast, and the three
  paths that draw the "Locating…" skeleton — picking a row that has no fix yet
  from the Cities sheet, "Use my current location", another tab's saved list —
  never call it. So the abandoned download ran to completion and rendered when
  it landed: with Mumbai's forecast in flight, tapping "Use my current
  location" put Mumbai's city bar, hero, temperature, condition, summary and
  cards back on screen on top of the "Locating…" the reader had just asked for,
  while `cur` was on "My Location" — and it stayed that way until a fix arrived
  or the 15-second geolocation watchdog fired. `renderSkeleton()` now takes the
  screen over: it bumps `showSeq`, so a late answer can never paint, and aborts
  the request it superseded instead of leaving it to finish.

### Notes
- Measured on the previous build first: the same two scenarios (picking the
  pinned row from the sheet, and the "Use my current location" button, each
  with a 2.5 s forecast in flight) ended with `#main` showing "Mumbai /
  27° / Light rain / 📍 Mumbai, India" while `places[cur]` was "My Location".
  After the change both end with the skeleton still up — "My Location / --° /
  Locating…" — and one fewer forecast download runs to completion.
- Nothing visible changes: for a stubbed forecast the rendered `#main`, `#nav`,
  the pill, the search sheet and the settings panel (closed and open) are
  identical to 1.5.8 across the rain, clear-day, clear-night and snow scenes,
  and so is every settings variable (`--k`, `--glass`, `--blur`, `--dp`,
  `--pr`, `--spring`); only `--mx`/`--my`, which follow the pointer, vary from
  run to run — the same two fields differ between two runs of the *unchanged*
  build. No CSS, markup, wording or timing was touched.
- No other leak was found in this pass's area: every `addEventListener` in the
  page is registered once at load, no timer survives at rest, the particle loop
  and the lightning chain stop while the page is hidden and resume on return
  (measured: 0 frames while hidden, 16 in the first 1.2 s after return), and
  `MainActivity` already hands the WebView its `onPause`/`onResume` and detaches
  it before `destroy()`.
- `node --check` is clean on the extracted script; a headless Chromium load
  reports zero console errors.
- `versionCode 33` / `versionName 1.5.9` in `AndroidManifest.xml` and
  `build.sh` (up from 32 / 1.5.8), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1, v2 and v3
  schemes. `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `88d5ddf4…`) and so is the copy inside the rebuilt APK.
  `MainActivity.java` is untouched, so the packaged `classes.dex` is
  byte-identical to 1.5.8's (SHA-256 `de209f1f…`). `CHECKSUMS.txt` points at the
  new build (`5354f308…`).
- Left alone deliberately: `removeSaved()` still repaints nothing on the main
  screen when the row it leaves selected has no fix — the deleted city's
  forecast stays on screen until `locate()` or `show()` repaints. It shows the
  same city the request belongs to, so no wrong city is ever painted, and
  giving that path its own skeleton would change what the screen does between
  the tap and the fix.
- Left alone deliberately, as in 1.5.8: the `setInterval(autoRefresh, 60 * 1000)`
  and `getPosition()`'s losing 2.5 s `GEO_NAME_WAIT` timer.

## [1.6] — 2026-11-06

The day's release: the five fixes committed during the day (1.5.5 to 1.5.9) plus
one more, found on the day's last pass.

### Fixed
- **Text an input method was still composing was searched.** An Indic, Japanese
  or Korean keyboard — and Android's own composition — fires an `input` event
  for every intermediate string it builds, and the search box treated each one
  as a finished query: composing "मुंबई" put six geocoder requests on the wire,
  five of them for "मु", "मुं", "मुंब" and the rest of the text nobody had
  committed yet, each after the same 320 ms debounce. The sheet repainted for
  every fragment too — with a geocoder that answers nothing, it flashed
  "No place called “मु”" at the reader while they were still typing — and the
  burst landed on the free geocoding tiers that answer a burst with 429, which
  is exactly what the abort-and-supersede logic beside the handler exists to
  avoid. Enter pressed to commit a candidate searched the unfinished text as
  well, before the browser had committed it. The box is now quiet while a
  composition is open (`compositionstart`/`compositionend`, plus `isComposing`
  on the `input` and `keydown` events) and searches the committed text once,
  through the same debounce; `openSheet()` and `closeSheet()` clear the flag, so
  a composition abandoned by closing the sheet cannot leave the box deaf.
  Nothing changes for a keyboard that commits as it types — every Latin layout,
  and any autocomplete that replaces the word outright — because `composing`
  and `isComposing` are both false there.

### Also in this release
- 1.5.5 — the thunderstorm flash no longer re-arms itself while the app is in
  the background, and a deleted city's forecast no longer stays in memory.
- 1.5.6 — one place is recognised as one place: `samePlace()` compares names
  within 25 km as well as the rounded coordinate key, so a city could no longer
  be saved twice, listed twice in one set of results, or offered again after
  the New Delhi fallback.
- 1.5.7 — the summary card describes night as night, and four weather codes
  (55/57, 77, 80, 85/86) get the sentence their own WMO entry promises.
- 1.5.8 — a location fix for a row that had already gone is dropped, and a
  forecast is never cached under a key no row owns.
- 1.5.9 — a forecast that outlived the screen that started it can no longer
  paint over the "Locating…" the reader asked for.

### Notes
- Verified on both files in headless Chromium with the forecast, geocoding and
  geolocation APIs stubbed. Targeted check: one composed query issued **6**
  geocoder requests on 1.5.9 and issues **1** now, for the committed text;
  ordinary typing ("pun"), Enter ("goa") and the commit itself still issue
  exactly one request each, and a composition abandoned by closing the sheet
  leaves the box working (typing "delhi" after reopening searches as before).
- Nothing visible changes: `#main` markup is byte-identical to 1.5.9 (3115
  characters), 23 elements × 20 computed properties and 7 sheet probes (Popular
  plus six queries) are identical, and the only two values that differ —
  `.cloud` geometry and the sun's pulse phase — differ between two runs of the
  unchanged file as well, because both are seeded at load.
- `node --check` is clean on the extracted script; a headless load reports zero
  console errors, and so does a 400-action random pass (tabs, sliders, sheet,
  removals, unit toggle, four geocoder behaviours) on both builds.
- `versionCode 34` / `versionName 1.6` in `AndroidManifest.xml` and `build.sh`
  (up from 33 / 1.5.9), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1, v2 and v3
  schemes. `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `b5e5e395…`) and so is the copy inside the rebuilt APK.
  `CHECKSUMS.txt` points at the new build (`16cf4f42…`).
- Left alone deliberately, as in 1.5.6: a one-character query still never
  reaches a geocoder, and the bundled country prefix still matches more than
  the reader may mean ("uk" resolves to Kyiv through "Ukraine"). Both would
  change which results appear for a query — a behaviour change, not a bug fix.

## [1.6.1] — 2026-11-07

### Fixed
- **A city an older build saved twice stayed in the list twice.** 1.5.6 stopped
  `addPlace()` and the search results from writing one place into the list twice
  — once under the same key, once under each geocoder's own coordinates for it
  (Bundled and Nominatim answer 0.6–10 km apart) — but the copies already in
  local storage were never touched, because the restored list was only checked
  field by field. A reader who hit that bug still saw Mumbai listed twice in the
  Cities sheet, still had two of the five slots spent on one city, and could be
  told "You can save up to 5 cities" while the list showed the same city twice.
  The restored list is now deduped once at boot with the same `samePlace()` rule
  the rest of the app uses, and written back, so the repair happens once rather
  than at every launch. The row on screen is followed to its new index (the
  surviving twin, if it was the copy that went), and the pinned "My Location"
  row is never the copy that is dropped.
- **One tab silently undid another tab's glass settings.** The settings object is
  written whole, so a document that moved one slider put its own stale copies of
  the other four back: with the app and a browser tab open, setting Blur to 20 in
  one and then moving Transparency in the other left Blur at 50 on disk, and the
  next launch opened with the wrong glass. The `storage` event that already keeps
  the saved-places list in step now adopts `lw_set` the same way — validated by
  `cleanSet()`, applied to the document, and reflected on the panel's sliders
  when the panel is open. A document never receives its own writes, so a single
  tab behaves exactly as it did.

### Notes
- Measured on the previous build first. Duplicate list (`lw_places` = Mumbai,
  Mumbai, New Delhi, current index 0): the Cities sheet painted three saved rows
  with Mumbai twice, and storage kept all three. Now two rows — Mumbai, New
  Delhi — and storage holds two. The same list with Mumbai at 19.076/72.877 and
  at 19.055/72.869 (the two geocoders' answers for one city), current index 2:
  the sheet painted Mumbai twice and the index pointed at New Delhi; now one
  Mumbai row, current index 1, still New Delhi on screen. A clean list and a list
  whose pinned row duplicates a saved one are both left exactly as they were.
- Two-tab settings check: on 1.6, tab B's Blur 20 became 50 in storage as soon
  as tab A moved Transparency, and tab A's `--blur` stayed at 22.0px; now storage
  keeps `bl:20` and tab A's `--blur` follows it to 11.2px. With the panel open,
  the slider and its readout follow the adopted value (35 / 35%).
- Nothing visible changes: the `<style>` block and every line of markup before
  the script are byte-identical to 1.6 (20,792 characters), and for each of the
  four stored lists above the rendered `#main` markup and 23 elements' computed
  styles (radius, backdrop blur, colour, size, padding, gradient, shadow) and the
  six settings variables are identical to 1.6's.
- `node --check` is clean on the extracted script; a headless Chromium load
  reports zero console errors, and so does a 400-action random pass (tabs,
  sliders, sheet, removals, unit toggle, Escape) on both builds.
- `versionCode 35` / `versionName 1.6.1` in `AndroidManifest.xml` and `build.sh`
  (up from 34 / 1.6), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `fddedb6b…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`feb62e53…`).
- Left alone deliberately: `LS.set()` still swallows a quota error, so a full
  storage quota loses a saved city silently — the list is a few hundred bytes and
  nothing reachable through the UI comes close to the quota, and every way of
  telling the reader would add wording the UI freeze forbids. Also left alone: a
  stored list that holds the pinned row *and* the same city saved is not repaired
  (the pin wins, the duplicate stays), because dropping either row would change
  what the app does with "Use my current location".

## [1.6.2] — 2026-11-07

### Fixed
- **The search sheet answered a query in silence.** Nothing inside it was a live
  region, so a screen-reader user who typed a search heard their own letters and
  then nothing at all: not "Searching…", not the results that appeared below
  the box, not the "No place called …" card. The only live region in the whole
  app was the toast. The sheet now carries a status line — clipped out of the
  layout, painting nothing — that says what the list holds: "Searching…",
  "2 results for “mum”", "No place found for “zzz”", and nothing at all when the
  box is empty. A sentence that has not changed is not announced again, so the
  repaint after a removal stays quiet, and closing the sheet leaves no stale
  text behind for the next visit.
- **A saved row was announced as the delete action.** The row's spoken name was
  computed from its contents, and its contents include the ✕: a saved city was
  read as "Mumbai India Remove Mumbai", so the row itself sounded like a delete
  button, and the name was read twice — once inside the row and once for the ✕,
  which is a control of its own in Chrome's accessibility tree. The name is now
  stated explicitly ("Mumbai, Maharashtra, India"), the way the °C/°F button's
  is; the ✕ keeps its own "Remove Mumbai" label, and the row's visible text is
  untouched.

### Notes
- Measured on 1.6.1 first: typing "mum" with a slow geocoder left the sheet with
  **no** status node at all, and the first saved row was announced as
  "🏙️ New Delhi India Remove New Delhi". Now the status reads "" →
  "Searching…" → "2 results for “mum”", and "No place found for “zzz”" for a
  query that matches nothing; the row is announced as "New Delhi, India" beside a
  separate "Remove New Delhi" button. The ✕ still removes the city when Enter is
  pressed on it, and focus lands back on "Use my current location".
- Nothing visible changes: with animations frozen and `Math.random` seeded,
  screenshots of the forecast page, the open sheet, a query with results and a
  query with no match are byte-identical to 1.6.1's (the only pixels that differ
  between any two runs — including two runs of the *same* file — are the
  blinking caret and the nav pill's animation phase). Twenty-three elements'
  computed styles, their geometry and the rendered `#main` markup are unchanged,
  and the new status node is 1×1, clipped and absolutely positioned, so it takes
  no space and paints nothing.
- `node --check` is clean on the extracted script, and a headless Chromium load
  reports zero console errors on both builds.
- `versionCode 36` / `versionName 1.6.2` in `AndroidManifest.xml` and `build.sh`
  (up from 35 / 1.6.1), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `856d20ca…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`f36dea85…`).
- Left alone deliberately: **the ✕ is still nested inside the row's `<button>`** —
  invalid markup that axe reports as `nested-interactive` on every saved row and
  every saved search result. Fixing it means moving the ✕ out into a wrapper that
  carries the row's glass box, which changes the row's tap target (the 12/14px
  padding would no longer select the city) and the element the press animation
  runs on. That is a visible, behavioural change, so only the name was fixed.
- Also left alone: the hourly strip, which axe flags as
  `scrollable-region-focusable`; Chrome already makes an `overflow-x:auto` box
  focusable and scrollable with the arrow keys (verified: it is in the tab order,
  and ArrowRight moves it 40px), so a `tabindex` would be a no-op here. Text
  contrast over the scenes was not touched either — every way of raising it is a
  colour change, which the freeze forbids.

## [1.6.3] — 2026-11-07

### Fixed
- **Dragging the nav lens forced a layout of the whole document on every
  pointermove.** `nearestBtn()` measured all three tabs with
  `getBoundingClientRect()` each time the finger moved, and the frame before had
  just written `--mx`/`--my` on the root (the parallax engine), so the style was
  dirty and each measurement flushed a fresh style recalc and a fresh layout of
  the entire page — at the pointer's own rate, which on a 120 Hz screen is above
  the frame rate, for three boxes that had not moved. A drag is the one gesture
  where the app spends its whole frame budget on this: the tab centres are now
  measured once and reused, and the cache is dropped when the bar can actually
  have moved under them — a resize, a rotation, a rebuilt tab set, a scroll of
  the strip, or the parallax itself having shifted the bar (it rides
  `--mx`/`--my`, so the cache is dropped once `--mx` has moved by 0.1, which is
  under a pixel of travel at any slider setting). Measured in headless Chromium,
  forty pointermoves of a drag: 120 box measurements and 766 ms of synchronous
  handler time before, 24 measurements and 143 ms after; the median handler cost
  fell from 12.4 ms to 0.1 ms.

### Notes
- Nothing visible changes. The rendered `#main` is byte-identical (same markup
  hash, 223 nodes), so are 23 elements' computed styles, the six glass variables
  and the frozen transforms of the cards and the nav, and a 430 × 900 screenshot
  with *Reduce motion* on is pixel-identical. Two runs of the same file are
  identical too, so the comparison is meaningful.
- The tab the drag lands on is unchanged: over four drags (60→360, 360→60,
  150→300 in 30 steps, and a sub-threshold 40→45 wiggle) the per-move hover
  sequence, the final tab and the pill's `left`/`width` are identical to 1.6.2.
- `node --check` is clean on the extracted script; a headless Chromium load
  reports zero console errors, and so does a 400-action random pass (tabs,
  sliders, sheet, searches, removals, unit toggle, 32 nav drags) on both builds
  in rain, thunderstorm and clear scenes.
- `versionCode 37` / `versionName 1.6.3` in `AndroidManifest.xml` and
  `build.sh` (up from 36 / 1.6.2), same signing key — certificate SHA-256
  `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1, v2 and v3
  schemes. `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `d711bf90…`) and so is the copy inside the rebuilt APK.
  `CHECKSUMS.txt` points at the new build (`86f811f8…`).
- Left alone deliberately: `placePill()` still reads `offsetLeft`,
  `offsetWidth` and the strip's `scrollWidth`/`clientWidth` when the hovered tab
  changes — at most three times per drag, and again on a tab change; folding it
  into the same cache would mean caching the pill's geometry as well as the
  buttons', for a saving of three flushes per gesture.
- Left alone deliberately: the drag hit test still re-measures when the parallax
  has moved the bar by more than a pixel (a handful of times per drag). Removing
  that means computing the bar's `translate3d` from `--mx`/`--my`/`--pr`/`--dp`
  in JavaScript, i.e. duplicating the stylesheet's own 9px multiplier in the
  script — worse than the flush it saves.
- Also left alone, still: the backdrop blur on the glass cards (the largest
  paint cost, and any cut visibly changes the glass), the °C/°F toggle rebuilding
  the whole of `#main` (a restructure, not a fix), and the particle loop running
  at the display's refresh rate rather than a capped 60 Hz (capping it would slow
  the rain on a 120 Hz screen, which the freeze forbids).

## [1.7] — 2026-11-07

### Added
- **Real photo backdrop from Wikimedia Commons.** Behind the glass there is now
  a real photograph: the city you are looking at when Commons has a freely
  licensed one for it, otherwise a CC-licensed sky for the weather on screen
  (partly cloudy, fog/overcast, rain, thunderstorm, snow). The city is looked up
  by name through the Commons API, the picture comes from `upload.wikimedia.org`,
  and the choice is remembered on the phone for three weeks so it is not looked
  up again. Only free licences are accepted (CC0, CC BY, CC BY-SA, public
  domain) — a file Commons marks as fair use is skipped — and a lookup that
  could not be made (no network, 5xx, timeout) is never cached as "no photo",
  so one launch in a tunnel does not leave the backdrop empty for three weeks.
- **Photo credits in *Glass & motion*.** A *Photos* block names the source
  (Wikimedia Commons) and, for whichever picture is on screen, the author and
  the licence — the attribution the CC BY / CC BY-SA files require. It follows
  the city and the weather as they change.
- **Real clouds.** The number of drifting clouds is now the cloud cover the
  forecast reports for that city (0–100%), scaled around each scene's own count,
  so an overcast sky still reads as overcast and a clear one is bare. A payload
  without a usable `cloud_cover` keeps the old fixed count.
- **Real sunset (and sunrise).** The day/night scene, the hero and the summary
  now switch at the city's own sunrise and sunset rather than at a fixed hour,
  and the summary card shows today's real times ("Sunrise 6:30 AM · Sunset
  6:04 PM"). The city's wall clock is the payload's `utc_offset_seconds` applied
  to the device's UTC clock, used only while the two clocks agree on the
  payload's date, so a device with a wrong clock still gets the payload's own
  `is_day`; a payload without sunrise/sunset also falls back to `is_day`, which
  is what every earlier version showed.

### Fixed
- **The hourly strip stayed on the payload's clock, so its "Now" cell drifted
  away from the rest of the screen.** `hourIndex()` anchored the eight cells at
  the hour the forecast was fetched at, while the day rows, the hero's H:/L:,
  the summary and the UV card are matched against the city's own date. A payload
  cached at 23:55 and still drawn at 00:05 showed a first cell reading "Now"
  over yesterday's 23:00 beside a "Today" row that was already today, and an app
  left open offline for three hours showed "Now" over a three-hour-old hour and
  temperature. The strip now adopts the city's wall clock when that hour is
  later than the payload's, under the same trust rule as the date.

### Notes
- **This release breaks the maintenance programme's UI freeze on purpose** — it
  adds a photo layer, a sunrise/sunset line and a credits block, which the
  scheduled passes were not allowed to do. The pass-level rule (bug, crash,
  performance and correctness fixes only) resumes with the next scheduled pass;
  nothing else in the layout, spacing, colours, typography, gradients, glass
  values or animation timings was touched.
- Verified in headless Chromium (mocked Open-Meteo and Commons): the photo layer
  fades in with the city photo and the credit block names its author and
  licence; with no Commons match the scene's sky photo takes over and the credit
  lists only that; a 404 on the image, a fully offline launch and an empty
  Commons answer each leave the layer invisible with no page errors — the app
  renders exactly as 1.6.3 does. Day/night follows the payload's own sunrise and
  sunset: at 17:50 the scene is `bg-d-cloud`, at 18:10 (sunset 18:04) it is
  `bg-n-cloud`. An older payload without `sunrise`/`sunset`/`cloud_cover` renders
  with no sun line and the scene's fixed cloud count. The midnight case still
  behaves: at 00:10 the strip reads `Now=0°` with "Today" on the new row. A
  stored photo record is used without any Commons request. An 80-action random
  pass (tabs, sliders, searches, removals, unit toggle, nav drags, reset) reports
  zero console errors and zero page errors.
- Caught before shipping: the photo store is read at load time, and its first
  version called `toNum()` — a `const` declared further down — so the whole boot
  threw `Cannot access 'toNum' before initialization` and the app opened blank.
  The parse is now local to `cleanPhoto()`.
- `node --check` is clean on the extracted script and the APK's own bundled
  `assets/index.html` loads with zero console errors.
- `versionCode 39` / `versionName 1.7` in `AndroidManifest.xml` and `build.sh`
  (up from 37 / 1.6.3), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `1951e6e5…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`f8a52080…`).
- `PRIVACY.md`, `README.md` and `STORE.md` now name Wikimedia Commons and
  `upload.wikimedia.org` as network endpoints, say that only the city name is
  sent (never coordinates, and never for "My Location"), and list each sky
  photo's author and licence.

## [1.7.1] — 2026-11-07

### Fixed
- **One document silently threw away the city photo another had just cached.**
  The remembered photo store (`lw_photos`) is a single map, keyed per city and
  written whole, and nothing listened for it — the two bugs fixed for the
  settings and the saved-places list in 1.6.1 were never closed for the store
  added in 1.7. Tab A cached Mumbai's photo; tab B, opened before that, still
  held a map with only the default city in it, so when B cached Bengaluru and
  wrote its copy, Mumbai's record was gone from storage. Nothing on screen
  broke — the photo was still in A's memory — but the next launch had to look
  Mumbai up on Commons all over again, and with two documents open it could
  happen to a city again and again. Every write is now a read-modify-write of
  the union of this document's map and the stored one, and a `storage` event
  for `lw_photos` is adopted through the same `cleanPhoto()` validation a cold
  load uses (taking the newer of two copies of one city), so the two maps
  cannot drift apart.
- **A photo lookup that landed after its city was deleted left a record on
  disk for ever.** `prunePhotos()` runs when a city is removed, but a Commons
  request already in flight wrote its record back afterwards — for a key no row
  could ever read again. One record per deleted city stayed in storage, taking
  up the twelve slots the loader keeps. The record is now only written while a
  row still owns its key.

### Notes
- Measured on 1.7 first, in headless Chromium with Commons mocked to answer one
  photo. Two documents, A caching Mumbai's photo and then B (stale) caching
  Bengaluru's: 1.7 left storage with two keys and Mumbai's gone; 1.7.1 leaves
  three, Mumbai's intact, and both documents' in-memory maps hold all three.
  Orphan check — Mumbai added, its lookup held for 1.5s, the row deleted before
  the answer arrived: 1.7 wrote `c19.076,72.878` to storage with no row behind
  it, 1.7.1 writes nothing.
- No visual change: nothing before the `<script>` block differs from 1.7 (the
  `<style>` block is byte-identical, 18,944 characters), and the diff is three
  hunks inside the script. For the default city and for a second city the
  rendered `#main` text and node count, the computed styles of eleven elements
  (radius, backdrop blur, colour, size, padding, gradient, shadow), the photo
  layer's background and opacity, and the six settings variables are identical
  to 1.7's.
- `node --check` is clean on the extracted script; a headless Chromium load and
  a 120-action random pass (tabs, sliders, sheet, saves, removals, unit toggle,
  Escape, scrolling) both report zero console errors on 1.7.1.
- `versionCode 40` / `versionName 1.7.1` in `AndroidManifest.xml` and `build.sh`
  (up from 39 / 1.7), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `c43872ea…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`105b43bb…`).
- Left alone deliberately: `lw_unit` is still not adopted across documents, so a
  tab that was open when the other one switched to °F keeps showing °C — making
  it follow would change the unit label in a document that was not touched, which
  the UI freeze rules out; and `LS.set()` still swallows a quota error (as noted
  in 1.6.1, nothing reachable through the UI comes near the quota, and any
  message about it would add wording the freeze forbids).

## [1.7.2] — 2026-11-08

### Fixed
- **A search answered by the fallback geocoder could list the same row twice.**
  When Open-Meteo's geocoder is unreachable or rate-limited, `remoteSearch()`
  asks Nominatim, and Nominatim answers a city query with the settlement *and*
  with the region that carries the same name — both mapped to the same name and
  the same subtitle. `dedupe()` keys rows with `samePlace()`, which merges two
  rows only within 25 km (deliberately: that is what keeps Portland, Maine and
  Portland, Oregon apart), so the pair survived and the sheet showed two rows a
  reader could not tell apart: **"sao paulo"** listed "São Paulo, Região
  Sudeste, Brasil" at -23.55 (the city) and, 160 km inland at -22.07, the state
  of São Paulo's centroid under the identical label — picking the second one
  saved a city named São Paulo and showed the weather of open country. Two rows
  with the same folded name *and* the same folded subtitle are now one row, and
  the best-ranked one — the one the geocoder meant — is the one kept.

### Notes
- No visual change: the `<style>` block is untouched, and with a fixed payload
  the rendered `#main` markup is byte-identical to 1.7.1 (3,241 characters, 229
  nodes), as are the computed radius, blur, colour, size, padding, shadow and
  gradient of the bar, the hero, the nav, the selected tab, the pill, the toast
  and a glass card, the six settings variables, and the whole Popular list the
  sheet paints when it opens.
- Measured on 1.7.1 first, in headless Chromium with the fallback geocoder
  answering Nominatim's real payload for the query: 1.7.1 rendered 3 result rows
  for "sao paulo", the first two identical apart from the 160 km between them;
  1.7.2 renders 2 (the city, and the genuine "São Paulo, Capanema, Pará").
  The rule does not touch rows that merely share a name: "springfield" still
  renders all 8 (Illinois, Massachusetts, Missouri, Ohio, Oregon, Vermont,
  Kentucky, Georgia), and rows that differ only in their subtitle — "Bogotá
  ciudad, Bogotá, Distrito Capital" against "Bogota, Bergen County, New Jersey"
  — are still both listed. A query with no answer still ends on "No place
  called …", and an empty geocoder payload still falls back to the bundled list.
- `node --check` is clean on the extracted script; a headless load and a
  10-query pass over the sheet (including a geocoder answering with HTML in a
  name, string coordinates, missing coordinates, out-of-range coordinates and
  duplicate rows) report zero console errors and zero page errors.
- `versionCode 41` / `versionName 1.7.2` in `AndroidManifest.xml` and `build.sh`
  (up from 40 / 1.7.1), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `75a223ea…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`910bb187…`).
- Left alone deliberately: rows that are not settlements at all — a county, a
  river, an airport, a state — still come through, because the geocoder returns
  them in its own relevance order and a state is a legitimate pick ("Goa" is
  one); dropping them would be a behaviour change, not a bug fix. Also left:
  the Popular row "Delhi" is recognised as the saved "New Delhi" (identical
  coordinates), so its ✕ removes that row while reading "Remove Delhi" — naming
  it after the saved row would change visible wording, which the freeze forbids.

## [1.7.3] — 2026-11-08

### Fixed
- **Switching Reduce motion off while the app was open left the Bounce setting
  dead until the next launch.** Every spring in the app — the pill lens, the
  sheets, the cards, the entry animation — is derived in `applySettings()` from
  the Bounce slider, and that function skipped the springs when the OS asked for
  reduced motion. It decided that by reading the `prefers-reduced-motion` query
  **once, at load** (`const noMotion`). A reader whose phone had Reduce motion
  on when the app started, and who then turned it off, kept the launch-time
  answer for the rest of the session: `--spring` and `--spring-soft` were never
  written on `:root`, the stylesheet's default curve was used instead, and
  moving Bounce — or *Reset to default* — changed nothing on screen. The query is
  now watched through `motionMQ`, the same object the particle field and the
  parallax engine already follow, and the springs are re-derived when it
  changes, so the setting works in both directions. Nothing is written while
  Reduce motion is on (`applySettings()` still returns before the springs), so a
  reduced-motion session renders exactly as it did.

### Notes
- Measured on 1.7.2 first, in headless Chromium with the query emulated: launch
  with `prefers-reduced-motion: reduce`, set Bounce to 0, then emulate
  `no-preference`. 1.7.2 left `--spring` unset on `:root`, and Bounce 0 → 100
  after the switch wrote nothing at all; 1.7.3 adopts `linear(0,0.005,…)`
  (Bounce 0) the moment the setting flips, and Bounce 100 then writes
  `linear(0,0.036,…)` — the same values a launch with the setting off produces.
  The control run, launched with the setting off, is byte-identical before and
  after.
- No visual change in any default session: with Reduce motion off, the rendered
  `#main` markup (2,984 characters), the computed radius, blur, colour, size,
  padding, shadow and gradient of the bar, the hero, a glass card, the nav and
  the pill, the photo layer's background and opacity, and the settings variables
  `--k`, `--glass`, `--blur`, `--dp` and `--pr` are identical to 1.7.2. (`--mx`
  and `--my` differ between any two runs — before the change as well — because
  they follow the pointer.)
- The rest of this pass's area (memory and lifecycle) was re-audited end to end
  and found clean: 240 random actions (tabs, sliders, sheet, searches, saves,
  removals, unit toggle, Escape, resize, visibility flips) leave the listener
  count flat at 38, DOM nodes bounded at 231–283, one interval, at most three
  pending timers and the JS heap flat at about 1.2 MB; no frame is requested and
  no timer is armed while the page is hidden; 20 no-op resize events reallocate
  the particle canvas zero times, a real geometry change and the DPR cap behave
  as before; and the WebView shell still pauses, resumes, hands back a pending
  geolocation callback and detaches before destroying.
- `node --check` is clean on the extracted script; a headless load and the
  240-action pass report zero console errors and zero page errors, and the APK's
  own bundled `assets/index.html` loads with none either.
- `versionCode 42` / `versionName 1.7.3` in `AndroidManifest.xml` and `build.sh`
  (up from 41 / 1.7.2), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `c7531c9f…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`162a8045…`).
- Left alone deliberately: the 60-second refresh interval still ticks while the
  page is hidden (it returns immediately, and the alternatives were weighed in
  1.5.6); the `deviceorientation` listener stays subscribed while the parallax is
  halted by Reduce motion (each event does two clamps and a no-op queue — under a
  pixel of work, and unsubscribing risks the tilt never coming back); and the
  photo layer still builds a fresh `Image` on every render — measured at 0.035 ms
  on a picture the browser has already decoded, so there is nothing there to fix.

## [1.7.4] — 2026-11-08

### Fixed
- **A geocoder row that carries no coordinates could still be listed, saved and
  shown as a place at 0°N 0°E.** `remoteSearch()` normalised both services'
  answers with a bare unary plus — `lat: +r.latitude` for Open-Meteo,
  `lat: +r.lat` for the Nominatim fallback — and `+null`, `+''` and `+false` are
  all the number `0`. `usableResult()` then saw two finite numbers inside range
  and kept the row, so a row with a name and no position arrived in the sheet as
  an ordinary result: it listed "Pune, Maharashtra, India" at 0,0, tapping it
  saved a city whose coordinates are in the Gulf of Guinea, and the app fetched
  and displayed *that* forecast under the city's name. Two such rows also landed
  on the same point, where `pid()` merged them, so a second city vanished from
  the results altogether. Coordinates now go through `toNum()`, which answers
  `NaN` for anything that is not a number or a non-empty numeric string —
  exactly what `usableResult()` already rejects — and passes a real coordinate,
  numeric or numeric-string (Nominatim's shape), through untouched.

### Notes
- No visual change: the `<style>` block is untouched, and the Popular list the
  sheet paints on open and the rendered `#main` markup hash identically to
  1.7.3 (`08009f482561` and `2434ed77a049`, same viewport, same payload).
- Measured on 1.7.3 first, in headless Chromium, with a geocoder answering one
  honest row plus rows whose coordinates are `null`, `""`, `true/false` and a
  numeric string: 1.7.3 listed 4 rows — "Pune" at 0,0 and "Surat" at 1,0 among
  them — and tapping "Pune" saved `0,0` and put "Pune" on the hero over the
  wrong forecast; 1.7.4 lists the 2 honest rows (the number and the
  numeric-string one), and the phantom row is not there to tap.
- No regression on real payloads: 24 live Nominatim answers (sao paulo,
  springfield, san jose, victoria, richmond, portland, cambridge, male and the
  rest) render the same 105 rows before and after, row for row.
- `node --check` is clean on the extracted script; a headless load of
  `web/index.html` and one of the APK's own bundled `assets/index.html` report
  zero console errors and zero page errors.
- `versionCode 43` / `versionName 1.7.4` in `AndroidManifest.xml` and `build.sh`
  (up from 42 / 1.7.3), same signing key — certificate SHA-256 `2035d69f…9e3b8b`,
  unchanged, and the APK verifies against v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html` (SHA-256
  `c0644ebb…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`f0ace7d1…`).
- Left alone deliberately: `countryMatches()` still prefix-matches the country
  label, so "uk" answers with Kyiv (Ukraine) and "turkey" finds nothing in the
  bundled list (the label is "Türkiye") — both are gaps in the *data*, not in the
  matching code, and closing them means an alias table, which is new content
  rather than a fix. Also left: localized names ("münchen", "bombay") only ever
  resolve through the geocoder, and rows that are not settlements — a county, a
  state, a metro area — still come through, as weighed in 1.7.2.

## [1.8] — 2026-11-08

### Fixed
- **The build's last step printed the signature but never checked it, so
  a broken — or wrongly signed — APK still left `build.sh` with exit
  status 0.** The final line was `apksigner verify --print-certs
  build/LiquidWeather.apk | head -4`. A pipeline reports `head`'s
  status, so the script's `set -e` never saw apksigner fail: an APK that
  printed `DOES NOT VERIFY` / `ERROR: Missing META-INF/MANIFEST.MF`
  finished the build "successfully" and CI uploaded it as the artifact.
  Nothing compared the signer with this project's key either, so a build
  made with any other keystore also passed — an APK that cannot install
  over the released app, which is the one thing "the signing key never
  changes" exists to prevent. Verification output is now captured to
  `build/verify.txt`, its exit status is the build's, and the signer's
  SHA-256 digest is compared with the certificate named in
  `CHECKSUMS.txt` (`2035d69f…9e3b8b`); anything else fails the build with
  a message saying not to publish it. `set -e` also gained `-o pipefail`,
  so a future pipeline cannot reintroduce the same swallowing.

### Notes
- Measured on 1.7.4 first, against the real toolchain (JDK 17,
  build-tools 34.0.0, platform 34): the old last line, run on an
  unsigned APK, printed `DOES NOT VERIFY` and exited 0; run on an APK
  signed with a throwaway keystore, it printed `CN=Someone Else` and
  `7e26d7b8…` and exited 0. With the fix those same two builds exit 1 —
  `ERROR: APK is not signed by the project key` — while the real build
  still exits 0 and prints the usual certificate.
- This release carries the whole day: 1.7.2 (a fallback-geocoder row
  listed twice), 1.7.3 (Bounce dead after switching Reduce motion off),
  1.7.4 (a coordinate-less geocoder row saved as a place at 0,0) and 1.8
  (this build gate).
- No visual change: `web/index.html` is untouched (SHA-256 `c0644ebb…`),
  and the rebuilt APK's bundled `assets/index.html` is byte-identical to
  it; a headless Chromium load of the source and of the APK's own copy
  each render the same 230 nodes and the same 3,215-character `#main`,
  with zero console errors and zero page errors. `node --check` is clean
  on the extracted script.
- `versionCode 44` / `versionName 1.8` in `AndroidManifest.xml` and
  `build.sh` (up from 43 / 1.7.4), same signing key — certificate
  SHA-256 `2035d69f…9e3b8b`, unchanged, and the APK verifies against v1,
  v2 and v3 schemes. `android/assets/index.html` is byte-identical to
  `web/index.html`, and so is the copy inside the rebuilt APK.
  `CHECKSUMS.txt` points at the new build (`e98c4a3e…`).
- Left alone deliberately: `build.sh` still passes `--version-code 43
  --version-name 1.7.4 --min-sdk-version 23 --target-sdk-version 34`,
  which duplicate the manifest. Bumping only the manifest to 44 / 1.8 was
  measured to produce an APK reporting 44 / 1.8, so aapt2 takes the
  manifest's values and the flags are inert duplication — not the drift
  bug they look like, so they were left rather than "fixed" for churn.
  Also left: the script still mints a fresh keystore when
  `android/release.keystore` is missing (the new certificate check now
  stops such a build at the end instead of letting it ship), and there is
  still no build-time comparison of `android/assets/index.html` with
  `web/index.html` — the two are identical today, and adding that guard
  is a change of policy rather than a fix.

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
  `a8f408fe…`) and so is the copy inside the rebuilt APK. `CHECKSUMS.txt` points
  at the new build (`1fcc2ec0…`), and the size quoted in the README follows it
  (`89 KB`).
- Left alone deliberately: `getJSON()` still does not consume the body of a
  response it is about to retry (a 429 body is a few hundred bytes and the
  browser releases it at the next collection — a real but tiny cost, and draining
  it changes the retry path for no gain); `Retry-After` is still read as seconds
  only, so the HTTP-date form falls back to the 300 ms floor it already used,
  capped at 2s either way; the retry still does not re-arm the 12s deadline,
  which is what keeps a retry from doubling the reader's wait; and
  `showPhoto()`'s `Image` load has no timeout, because an image request cannot be
  aborted and a late load is dropped by its token anyway.

## [1.8.2] — 2026-11-09

### Fixed
- **With Depth or Parallax at 0 the depth engine went on computing and writing a
  parallax value for every frame, for a screen that could not move.** Both
  sliders say "0 turns it off", and the stylesheet makes that literally true:
  every layer the engine drives — `#bgs`, `#orbLayer`, `#clouds`, `#fx`, `.card`
  and `nav` — multiplies `--mx`/`--my` by `--dp` *and* by `--pr`, so with either
  slider at 0 the whole transform resolves to `translate3d(0,0,0)` and no pixel
  can change. The engine wrote the pair anyway, once per pointer move, tilt event
  and scroll frame, and `--mx`/`--my` are inherited custom properties: each write
  invalidated the style of the entire document — the sky, the clouds, the
  particles, ten glass cards and the nav — and set those layers up for a raster
  that had nothing new to paint. A reader who turned Parallax (or Depth) to 0,
  the obvious thing to do on a phone that felt slow, therefore kept paying the
  full per-frame cost of the effect with none of it visible. Nothing is scheduled
  now while either slider sits at 0: the pointer, tilt and scroll handlers still
  record their positions, so the effect resumes at the next input event with the
  numbers it would have written, and the values already on the root stay there.
  Sliders above 0 behave exactly as before.

### Notes
- Measured in headless Chromium (forecast, geocoder and Commons stubbed) on the
  depth engine itself, by counting `setProperty('--mx')` calls: 30 pointer moves
  with Parallax at 0 wrote 30 pairs before and 0 after; 20 scroll steps wrote 8
  before and 0 after; Depth at 0 with Parallax at 55 wrote 30 before and 0 after.
  With Parallax back at 55 the same 20 moves write again, and `#bgs`'s computed
  transform follows the pointer as it did.
- A trace of 60 pointer moves at Parallax 0 (devtools.timeline, same stub, same
  pointer path): `UpdateLayoutTree` 2,454 ms → 227 ms, `RasterTask` 1,285 ms →
  66 ms, `Paint` 347 ms → 0.6 ms. The remaining style work is the pointer's own
  hit-testing and the nav's hover state, which is what a still screen costs.
- Nothing on screen changed. With the mocks held fixed, `#main` renders to the
  same markup hash (`c1f57c19d652`, 231 nodes) before and after, and the settled
  computed transforms of `#bgs`, `#orbLayer`, `#clouds`, `#fx`, the first `.card`
  and `nav` are identical at Parallax 55 *and* at Parallax 0. `node --check` is
  clean on the extracted script; a headless load of `web/index.html` reports zero
  console and zero page errors, and so does a 49-action pass (both unit toggles,
  scroll, search and pick a city, both settings tabs, all five sliders to 20 and
  to 70, reset, home, and a pointer sweep).
- `versionCode 46` / `versionName 1.8.2` in `AndroidManifest.xml` and `build.sh`
  (up from 45 / 1.8.1), same signing key — certificate SHA-256 `2035d69f…9e3b8b`
  — and the APK verifies against the v1, v2 and v3 schemes.
  `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `70b7314a…`) and so is the copy inside the rebuilt APK.
  `CHECKSUMS.txt` points at the new build (`92dada80…`), and the size quoted in
  the README follows it (`93 KB`; the new HTML crossed a 4 KB alignment boundary
  inside the archive, which is why the APK is one page larger than 1.8.1's).
- Left alone deliberately: `#pill` still animates `left`/`width`, so a tab change
  lays out the nav bar on every frame for 850 ms — doing it with a transform
  would squash the lens's 28 px corners and its inset shadows, which is a visible
  change; `showPhoto()` still builds a fresh `Image` for a photo already on
  screen (one per render — five for five unit toggles, no long task), which the
  browser answers from its memory cache and which does not repaint, since the
  `background-image` string is unchanged; `scene()` still rewrites `--cc` and the
  twenty `.bg` classes and nine cloud opacities on every render even when the
  scene is the same, but a render is a user action or the ten-minute refresh and
  never on a frame path; `applySettings()` still rewrites all seven root
  properties on every slider `input` event, which measures at 5 style
  recalculations for a 40-step drag; and the ten glass cards are still rebuilt by
  one `innerHTML` assignment per render, which is what makes a unit toggle cost
  ~100 ms of blurred-backdrop raster in headless Chromium — patching the text
  nodes instead is a structural change with a real risk of drifting markup, and
  the UI is frozen.

## [1.8.4] — 2026-11-09

### Fixed
- **The °C/°F toggle could not be operated by voice — its spoken name did not
  contain the only text on it.** The button shows `°C` or `°F` and nothing else,
  and `bindUnit()` gave it the spoken name "Temperature unit: Celsius" so a
  screen reader would not announce a bare symbol. That name left the visible
  label out, which is a WCAG 2.5.3 (Label in Name, Level A) failure: speech
  input and voice control match the words the user can see, so "°C" matched no
  control, and the unit toggle was the one button in the app that a voice user
  could not reach at all. axe 4.14 reports it as
  `label-content-name-mismatch` (serious) on every screen, in both units. The
  name now ends with the visible label as its own phrase — "Temperature unit:
  Celsius, °C" — so the visible text is part of the accessible name; the
  description that 1.2.1 added is still there, and the visible label itself is
  untouched. A bracketed form ("Temperature unit: Celsius (°C)") was tried
  first and does not work: the label-in-name comparison strips parenthetical
  asides as pronunciation hints before matching, so the mismatch survived it.

### Notes
- Verified: `node --check` on the extracted script is clean; headless Chromium
  loads of `web/index.html` and of the APK's own bundled `assets/index.html`
  report zero console and zero page errors, and so does a 36-action pass (both
  unit toggles twice, six scrolls, all five sliders to 20, reset, the Cities
  tab, a search and a clear, home, a pointer sweep, Tab and Escape). axe 4.14's
  `label-content-name-mismatch` is gone on the forecast screen in both units.
- Nothing on screen changed: `#main` holds the same 125 elements, the same
  text, and the same 145 measured boxes, the computed styles of the hero, a
  glass card, a label, the hourly strip, a day row, the nav and the unit button
  are identical, and a screenshot of the old and new build differs only in the
  sky band — which differs by the same amount between two runs of the *same*
  file, because the clouds and particles are not deterministic.
- `versionCode 48` / `versionName 1.8.4` in `AndroidManifest.xml` and
  `build.sh` (up from 47 / 1.8.3), same signing key — certificate SHA-256
  `2035d69f…9e3b8b` — and the rebuilt APK verifies. `android/assets/index.html`
  is byte-identical to `web/index.html` (SHA-256 `838c4157…`) and so is the
  copy inside the APK, which is 93 KB like 1.8.3's. `CHECKSUMS.txt` points at
  the new build (`eb1ff1cf…`).
- Left alone deliberately: the remove `✕` in the Cities list is a focusable
  `role="button"` span *inside* the row's `<button>` (axe: `nested-interactive`,
  serious). De-nesting it moves the row's glass background, its press-scale and
  its active state onto different elements — a visible change — so it stays as
  it is; Chrome exposes and focuses the ✕ correctly today, and its Enter/Space
  handling is its own. The hourly strip (`.hrs`) is scrollable but carries no
  `tabindex`; Chromium 127 and later make a scroll region focusable on their
  own (156 does here, and Tab reaches it), so only an older WebView needs it —
  and adding it would draw the app's white focus ring around the strip, which
  the frozen design does not have. And each 7-day row still announces two
  temperatures with no "low"/"high" wording and no text alternative for its
  range bar; fixing that means adding hidden text or roles to markup the
  rotation is not allowed to restructure.

## [1.8.3] — 2026-11-09

### Fixed
- **Deleting a saved city never actually removed its photo record — the prune
  undid itself.** `prunePhotos()` dropped the record from the in-memory store and
  then called `savePhotos()`, which exists to stop one document clobbering
  another's additions and therefore writes the *union* of memory and disk: it
  read the stored map, put every key memory no longer had straight back, and
  wrote it out. The record for a deleted city was therefore still in `lw_photos`
  after the delete, unchanged, and nothing else ever removed it — the twelve
  records `readPhotoStore()` keeps filled up with rows no city could read again.
  Because that cap is applied in insertion order, the first twelve records win
  and the newest city's record is the one dropped: once a few cities had been
  added and deleted, a live city was looked up on Commons again at every launch
  instead of being answered from storage, which is the request the store exists
  to avoid. `savePhotos()` now takes the keys that were pruned on purpose and
  drops them from the stored copy before the union is taken, so the prune is
  what the function always claimed to be; additions made by another document are
  still preserved, and every other write path is unchanged.

### Notes
- Measured on 1.8.2 first, in headless Chromium with the forecast, geocoder and
  Commons stubbed. Two saved cities with a photo record each, the second deleted
  through the Cities sheet: 1.8.2 leaves `lw_photos` with both records
  (`["c19.076,72.878","c18.520,73.856"]`); 1.8.3 leaves only the city still in
  the list (`["c19.076,72.878"]`).
- The cap: twelve records for cities that are not in the list plus one for the
  city on screen — 1.8.2 stores 13 records after a render, so the store keeps
  growing past the cap it is read back under; 1.8.3 prunes the twelve dead ones
  at the same point and stores the one record that belongs to a saved city.
- Nothing on screen changed: `#main` renders to the same markup hash
  (`3189:618222501`, 230 nodes) before and after, and the computed styles of the
  hero, a glass card, the nav, `#bgs` and `#orbLayer` and the root's `--k`,
  `--blur`, `--dp`, `--pr`, `--glass` are identical. `node --check` is clean on
  the extracted script; a headless load of `web/index.html` and of the APK's own
  bundled `assets/index.html` report zero console and zero page errors, and so
  does a 50-action pass (both unit toggles, scroll, settings panel, all five
  sliders to 20, reset, the Cities tab, a search, home, and a pointer sweep).
- `versionCode 47` / `versionName 1.8.3` in `AndroidManifest.xml` and `build.sh`
  (up from 46 / 1.8.2), same signing key — certificate SHA-256 `2035d69f…9e3b8b`
  — and the APK verifies. `android/assets/index.html` is byte-identical to
  `web/index.html` (SHA-256 `a30dc806…`) and so is the copy inside the rebuilt
  APK, which is the same size as 1.8.2's (93 KB). `CHECKSUMS.txt` points at the
  new build (`d3673800…`).
- Left alone deliberately: the `lw_photos` `storage` handler still adopts another
  document's records but never drops one it removed, so a second open document
  can write a pruned record back; the record is pruned again at the next delete
  or render, and adopting removals would risk discarding a record this document
  cached but has not yet written. A cleared `lw_photos` (`newValue === null`) is
  still ignored rather than adopted, which is what keeps a stray clear from
  wiping the map. And the store is still pruned only on a render, a delete or a
  `storage` event, not at boot, so an offline launch keeps the records it loaded
  until the next successful render.

## [1.8.5] — 2026-11-09

### Fixed
- **A response that arrived with a 200 but an unreadable body was thrown away
  after one attempt, and the app claimed to be offline.** `getJSON()` retries a
  busy server once (408/425/429/5xx, honouring `Retry-After`) and then reads the
  body with `r.json()`. That read is the one step that can still fail after the
  headers said 200 — a response cut short by a dropped connection, a proxy's
  error page, or a Wi-Fi sign-in page answering for the API on a captive portal
  — and its `SyntaxError` went straight out of the function: `show()` caught it
  as a link failure and drew the "Offline" card over a link that was working, the
  payload was never cached, and the only way back was to tap the retry card by
  hand. Reading the body now gets the same single retry the busy statuses get,
  300ms later and only while the request is still wanted (an aborted read, or a
  read of a request whose city has been left, is not repeated). A body that is
  still unreadable on the second attempt fails exactly as before, so the retry
  card and the offline path are unchanged; so is a genuinely offline device,
  which still fails at the normal deadline because the fetch itself never
  answered.
- **A city-photo lookup that could not be made was repeated on every repaint.**
  `fetchCityPhoto()` deliberately does not cache a failed lookup as "this city
  has no photo" (one launch in a tunnel would empty the backdrop for three
  weeks), but nothing stopped the next render asking again: `applyPhoto()` runs
  on every render, so toggling °C/°F, pulling a refresh, or the ten-minute auto
  refresh each started two fresh Commons requests of up to ten seconds, beside
  the forecast, on a link that was already struggling — against an API that
  rate-limits anonymous use, which is what made the lookups fail in the first
  place. A failed lookup is now remembered in memory for five minutes
  (`photoFail`, pruned with the rest of the per-city state when a city goes), so
  a busy API is asked once instead of on every repaint. Nothing is written to
  storage: the next launch, or the next render after the window, tries again,
  and a lookup that answers clears its mark and caches the photo exactly as
  before.

### Notes
- Verified: `node --check` on the extracted script is clean; a headless Chromium
  load of `web/index.html` reports zero console messages and zero page errors.
  The fixes were proved by driving the page with mocked responses: a 200 with a
  body cut mid-JSON (`{"current": {"time": … , "temp`) and a 200 that is a Wi-Fi
  sign-in page both used to give the "Offline" card after **1** forecast request
  and now render the forecast after **2**, while a body that is unreadable twice
  still gives the offline card after exactly 2 requests. With Commons answering
  500, the boot plus two unit toggles used to fire **3** lookups and now fires
  **1**, with the sky photo still on screen; with Commons answering normally the
  photo is still cached and shown after a re-render, in one request. The 429
  retry is unchanged (2 requests, forecast drawn).
- Nothing on screen changed: `#main`'s rendered HTML is byte-identical to
  1.8.4's for the same payload, and the computed styles of the page, bar, hero,
  temperature, condition line, a glass card, an hourly cell, a day row, a range
  bar, the nav, the pill and the photo layer are identical (only the live
  animation opacity differs between runs of the *same* file).
- `versionCode 49` / `versionName 1.8.5` in `AndroidManifest.xml` and `build.sh`
  (up from 48 / 1.8.4), same signing key. `android/assets/index.html` is
  byte-identical to `web/index.html` (SHA-256 `d7e40a66…`, 148 KB). **The APK
  itself was not rebuilt on this pass**: the environment it ran in has no JDK
  and no Android SDK, so `android/build.sh` cannot run there. `LiquidWeather.apk`
  and `CHECKSUMS.txt` are therefore untouched and still point at the 1.8.4 build
  (`eb1ff1cf…`, `versionCode 48`), which is one pass behind the source until a
  build machine runs `build.sh`. Nothing is published at 1.8.5 yet and the day's
  release is held until that build exists.
- Left alone deliberately: there is still no `online` event handler, so a device
  that reconnects after the offline card is drawn waits for the ten-minute
  auto-refresh (or a tap on the retry card) instead of refetching at once.
  Adding one changes *when* a screen repaints, which is a behaviour change the
  rotation's rules put behind a decision rather than a bug fix. The abandoned
  `Image()` in `showPhoto()` is also left as it is: its download cannot be
  cancelled, but the token guard already stops it from painting, and cancelling
  it would mean keeping a reference to every image the app has shown.

## [1.8.6] — 2026-11-10

### Fixed
- **The published APK was older than the source it was built from.**
  `LiquidWeather.apk` was still the 1.8.4 build (`versionCode 48`) and its
  bundled `assets/index.html` hashed to `838c4157…`, while `web/index.html` had
  already moved to `d7e40a66…` with the 1.8.5 network fixes. Anyone installing
  the APK got the app as it was two passes earlier, without the parse-retry and
  photo-lookup corrections it was supposed to carry. The 1.8.5 pass could not
  build — that environment had no JDK and no Android SDK — so the source moved
  and the artifact did not. This pass built the APK from the current source
  (`versionCode 50` / `versionName 1.8.6`, same signing key); the APK's bundled
  page now hashes to `d7e40a66…`, identical to `web/index.html`.
- **`android/build.sh` packaged whatever was in `android/assets` without ever
  comparing it with `web/index.html`.** That is how the drift above went
  unnoticed: the page is copied across by hand, so a build that ran after an
  edit but before the copy shipped the previous app under a new `versionCode`
  and said nothing. The script now stops before linking (step `[0/6]`) unless
  the two files are byte-identical, naming the copy to make. When they already
  match, the APK is unchanged.

### Notes
- `web/index.html` is untouched: the UI, layout, spacing, wording, gradients and
  animation timings are exactly what 1.8.5 shipped, and the file is
  byte-identical to that commit.
- Verified: `node --check` on the page's script; a headless Chromium load with
  mocked forecast, geocode and photo responses reporting zero console messages
  and zero page errors; the new gate failing the build on a stale asset and
  passing on matching ones; `apksigner verify --print-certs` showing the project
  certificate (`2035d69f…`); `zipalign -c -p 4` passing; `aapt2 dump badging`
  reporting `versionCode 50` / `versionName 1.8.6`.
- `CHECKSUMS.txt` updated to the new digest (`d2ae1074…`, 93 KB).
- Left alone deliberately: `build.sh` still passes `--version-code 50
  --version-name 1.8.6` next to the manifest. Measured again on this pass — a
  manifest reading `999` / `9.9.9` builds an APK reporting `999` / `9.9.9`, so
  `aapt2 link` takes the manifest's values and the flags are inert; they were
  kept in step with the manifest rather than deleted, since removing them cannot
  change behaviour. Also left: no CI step compares the committed APK with
  `web/index.html` (making that a gate would redden `main` between a source edit
  and the next build, which is a policy decision, not a fix), and the script
  still mints a keystore when `release.keystore` is missing — the certificate
  check at the end stops such a build from shipping.

## [1.8.7] — 2026-11-10

### Fixed
- **A failed location request could leave the app on "Locating…" for good, with
  a forecast for the city beside it never drawn.** When a position request fails
  and the pinned "My Location" row has no fix, `fallbackPlace()` fills it with
  New Delhi — but if New Delhi is already saved, the pinned row is dropped in
  favour of the saved copy. `cur` was only corrected when the dropped row sat
  *before* the one on screen (`if (at < cur) cur--`), so when the pinned row was
  itself the row on screen the index stayed put and now pointed at whatever slid
  into its place: the app jumped to a city the reader had not chosen. Worse, with
  the saved New Delhi sitting after the pinned row the repaint test
  `places.indexOf(target) === cur` was false, so `show()` was never called and
  the "Locating…" skeleton stayed on screen permanently — no forecast, no retry
  card, nothing to tap — even though the next city in the list had a perfectly
  good forecast. Reachable without any unusual state: tap "Use my current
  location" with Mumbai and New Delhi saved and refuse the prompt, or relaunch
  after doing so (the list is saved with the pinned row first and no fix).
  `cur` now follows the row the fix was merged into, the same way `removeSaved()`
  keeps pointing at the same city after a removal, so the fallback is drawn.

### Notes
- Verified: `node --check` on the page's script; headless Chromium loads with
  mocked storage, geolocation and forecast responses reporting zero console
  messages and zero page errors in every scenario below. The fix was proved by
  driving both builds through the same scenarios: with the list
  `[My Location (no fix), Mumbai, New Delhi]` and a denied prompt, the 1.8.6 page
  rendered the "Locating…" skeleton with **0** forecast requests and left it
  there, while 1.8.7 renders New Delhi's forecast with `cur` on that row; the
  same holds on the 15s watchdog path (a geolocation callback that never
  answers). The control cases are unchanged: New Delhi saved *before* the pinned
  row still repaints, a pinned row that already has a fix still redraws its own
  forecast on a refusal, and a successful fix still renders and resolves its
  name. For the same payload `#main`'s rendered HTML is byte-identical between
  1.8.6 and 1.8.7 (SHA-256 `daf7c893…`), so nothing on screen changed.
- `versionCode 51` / `versionName 1.8.7` in `AndroidManifest.xml` and
  `build.sh` (up from 50 / 1.8.6), same signing key. `android/assets/index.html`
  is byte-identical to `web/index.html` (SHA-256 `1fdffc7a…`). **The APK was not
  rebuilt on this pass**: this environment has no JDK and no Android SDK, so
  `android/build.sh` cannot run here. `LiquidWeather.apk` and `CHECKSUMS.txt` are
  therefore untouched and still describe the 1.8.6 build (`d2ae1074…`,
  `versionCode 50`, carrying the `d7e40a66…` page), which is one pass behind the
  source until a build machine runs `build.sh`. Nothing is published at 1.8.7 yet
  and the day's release is held until that build exists.
- Left alone deliberately: `android/build.sh` exits **silently** with status 2
  when the SDK is missing — `set -e` aborts on the failing `BT=$(ls -d …)` before
  the "Android SDK not found" message can print, which is why this pass's build
  attempt produced no diagnostic at all. That is a build-hygiene defect, not a
  geolocation one, so it is recorded here rather than fixed in this pass.
  Also left: a pinned row's coordinates are never refreshed after the first fix
  (the ten-minute auto-refresh re-fetches the forecast but not the position), so
  a phone carried across a city keeps the forecast for where it was — changing
  that alters when a permission-gated call happens, which the rotation's rules
  put behind a decision rather than a bug fix.

## [1.8.8] — 2026-11-10

### Fixed
- **Tapping a saved city in the Cities sheet could throw, and wrote a bad index
  to storage.** The sheet's saved rows carry the index of the row they select
  (`data-go`), and the list behind them is rewritten by the location code, which
  never repainted the sheet: `locate()` re-keys the pinned row and `dropTwin()`
  merges a saved copy of the city it landed on away, and `fallbackPlace()` drops
  the pinned row in favour of the saved copy. So the sheet went on listing a row
  that no longer existed, with the index it used to have. With "My Location"
  selected and one city saved, a fix arriving on that city leaves a one-row list
  while the sheet still offers its old row at index 1; tapping it ran
  `selectCity(1)`, which has no bounds check (unlike `removeSaved()`),
  `places[1]` was undefined, `cur` was saved as 1, and the skeleton built from
  the missing row threw `TypeError: Cannot read properties of undefined
  (reading 'name')` out of the tap handler. Reachable without unusual state:
  launch with "My Location" showing, open the Cities tab while it is locating,
  and tap the saved city once the fix lands. The sheet is now repainted wherever
  the list it indexes changes under it (`repaintSheet()`, the same rule the
  `storage` handler already followed for another document's write), and
  `selectCity()` returns early for an index the list no longer holds, the guard
  `removeSaved()` has always had. A failed location request takes the same path
  through `fallbackPlace()`, so the denial case is fixed with it.

### Notes
- No visual change: for the same payload the rendered `#main` HTML, the sheet's
  saved list and its search results are byte-identical to 1.8.7's in three
  control scenarios (location denied with and without a saved city, location
  granted), and the computed layout, colours, gradients, wording and animation
  timings are untouched — the only new code runs when the saved list actually
  changes under an open sheet.
- Verified: `node --check` on the page's script; headless Chromium loads with
  zero console messages and zero page errors; and the fix was proved by driving
  1.8.7 and 1.8.8 through the scenario above — 1.8.7 keeps `data-go="1"` in the
  sheet, throws the `TypeError` on the tap and persists `lw_cur=1` against a
  one-row list, while 1.8.8 repaints the row at `data-go="0"`, selects it with no
  exception and leaves `lw_cur=0`. The same check on the denied path
  (`fallbackPlace()`) shows 1.8.7 leaving the stale index and 1.8.8 repainting
  it, with the app on the same city either way.
- `versionCode 52` / `versionName 1.8.8` in `AndroidManifest.xml` and
  `build.sh` (up from 51 / 1.8.7), same signing key. `android/assets/index.html`
  is byte-identical to `web/index.html` (SHA-256 `37a19636…`). **The APK was not
  rebuilt on this pass**: this environment has no JDK and no Android SDK
  (`android/build.sh` exits 2 before its own diagnostic), so `LiquidWeather.apk`
  and `CHECKSUMS.txt` still describe the 1.8.6 build (`d2ae1074…`, `versionCode
  50`), which is two passes behind the source until a build machine runs
  `build.sh`. Nothing is published at 1.8.8 yet and the day's release is held
  until that build exists.
- Left alone deliberately: `countryMatches()` collapses a bundled city the
  geocoder already returned by comparing names only, so a geocoder that answers a
  country query with the same city under another spelling (Roma for Rome) would
  still list it twice — measured against the live services this pass could not
  reach a payload that does it (Nominatim answers a country query with the
  country itself, and Open-Meteo is asked for English names, which match the
  bundled ones), so nothing was changed on a guess. Also left: an offline device
  waits the full 9s + 9s geocoder budget before the bundled list appears, and
  painting the bundled matches first would change what a search shows the moment
  it is typed — a behaviour decision, not a bug fix. The sheet also keeps its
  scroll position when it is reopened; resetting it would move what the reader
  sees on open, which is a UI decision.

## [Unreleased]

### Fixed — render performance (2026-11-13, 22:00 IST pass)
- **Every parallax frame recalculated the style of the whole document.** The
  depth engine moved the sky, the orbs, the clouds, the particle canvas and the
  ten glass cards by writing two custom properties, `--mx`/`--my`, on
  `documentElement` once per animation frame. Custom properties are inherited,
  so each write invalidated every element in the document — each had to
  re-resolve an inherited value, and the six rules that consume them re-resolved
  their transforms with it — for two numbers only those six selectors ever read.
  Measured in headless Chromium on 1.10.3, one 40-move drag across the bar cost
  **2 466 ms of style recalculation** (55 recalcs, ~45 ms each) plus 311 ms of
  paint, 1 171 ms of raster and 1 233 ms of compositor commit; a 25-step scroll
  cost 747 ms of style and 46 ms of paint. The five layers that are not the bar
  now carry their transform inline, written straight onto each element, so a
  frame touches the sixteen elements that actually move: the same drag costs
  **1 018 ms of style, 46 ms of paint, 266 ms of raster and 879 ms of commit**,
  and the same scroll 466 ms of style and 13 ms of paint. The bar keeps
  `--mx`/`--my` on itself — its own rule in the stylesheet is what draws it, and
  the drag measures the buttons it carries (see `centres()` below) — so nothing
  about how it rides changed. Nothing about the *values* changed either: the
  ride distances (7/22/11/14/-4/-9 px), the `scale(1.08)` on the sky, the
  `translateZ(0)` on the bar and the ±1.5° card rotation are the numbers the
  stylesheet's own `calc()` resolved to, and the rules stay in the stylesheet as
  they were, so with the inline transform cleared — Reduce motion, or a slider
  at 0 — they draw the layers exactly as before.
- **The three tab centres were re-measured while the bar was only sliding.**
  The drag path caches the tabs' centres and drops the cache when the bar can
  have moved under them, which included "the parallax has moved by 0.1" — but
  the parallax is the one thing that moves the bar *without* moving its boxes,
  and it moves on every frame of a drag, so the cache was dropped anyway:
  measured on 1.10.3, one 40-move drag re-measured the bar **8 times**, each a
  forced layout of the whole document (the previous frame had just written
  `--mx`, so the style was dirty), against **1** for the same drag with Parallax
  at 0. The ride is now applied to the cached centres as arithmetic — exact, and
  free — and the cache is rebuilt only when the bar's layout or the ride's scale
  can have changed (resize, rotation, a scroll of the strip, a slider move, the
  end of the intro, which scales the bar). The tab chosen for a given pointer
  position is unchanged, move for move.
- **Two smaller consequences of the same change, handled here rather than
  left.** (1) The Depth and Parallax sliders used to change the layers by
  rewriting the properties the stylesheet read; with the transform inline,
  `applySettings()` now pushes the change to the layers, so a slider moved with
  the finger at rest still moves them at once. (2) Every `render()` replaces
  `#main`, so the cards it paints are new nodes; a `MutationObserver` on `#main`
  hands a freshly painted card the tilt the frame already carries, which
  otherwise would have dropped out until the next pointer, tilt or scroll event
  — visible to anyone tapping °C/°F with the phone lying still.
- Nothing visible changed. Full-page screenshots of the 430×900 phone at DPR 2,
  with every animation and transition removed and `Math.random` seeded, are
  **pixel-identical — 0 differing pixels of 6 192 000** — in four parallax
  states (`--mx` −0.3093, 0.0000, 0.2767, 0.5698, the same four numbers the
  engine writes in both builds); the `#fx` canvas is hidden for the comparison
  because its drops advance with time. Every layer's computed transform matrix
  was also checked against the stylesheet's own formula, and the drag's hovered
  tab was recorded at each of 41 pointer positions and is identical in both
  builds, ending on the same tab.
- **Left alone deliberately.** (1) The lens still animates `left`/`width`, which
  are not compositable, inside a `backdrop-filter` bar — a transform would have
  to stretch the lens and its inset shadows to keep the same look, which is a
  visual change. (2) The cards' 3D transform over `backdrop-filter` is still
  about half of what remains of the style cost per frame; it is the design.
  (3) `placePill()` still reads the target tab's `offsetWidth` per pill move —
  the 12:00 pass measured that and declined it, and the same measurement holds.
  (4) The photo layer still builds an `Image` per render (0.035 ms on an already
  decoded picture, deferred by 1.8.10).
- Verified: `node --check` on the page's script; headless Chromium loads of
  `web/index.html` with mocked forecast, geocoder, Commons and image responses
  reporting **zero console messages, warnings and page errors**, through the
  tabs, the search sheet with a typed query, the °C/°F toggle, the settings
  panel with Depth and Parallax moved, a 400×780 resize and Reduce motion
  switched on, off and launched with; the pixel and matrix comparisons above;
  and, for the APK, `python3 .github/scripts/verify_apk.py .`, `python3
  .github/scripts/verify_docs.py .` and `sha256sum -c` on the committed APK, all
  green, with `apksigner verify --print-certs` still reporting the project key
  (`2035d69f…`, `CN=Liquid Weather`). `versionCode 68` / `versionName 1.10.4` in
  `android/AndroidManifest.xml` (up from 67 / 1.10.3), same signing key; the APK
  was rebuilt from this tree with `android/build.sh` (JDK 17, build-tools
  34.0.0, platform 34), bundles `assets/index.html` byte-identical to
  `web/index.html`, and carries that version. `CHECKSUMS.txt` and the
  `sha256sum` block in `README.md` carry the new digest,
  `78ed4ffb1d6a1bd54d6d50854052b589b3892b4a43b28a6318c3db2bbd6f0626` (105 KB).

### Fixed — accessibility & semantics (2026-11-13, 16:00 IST pass)
- **The ✕ that deletes a saved city was a control nested inside another
  control.** Each row in the Cities sheet was a `<button>`, and the delete
  control inside it was a `<span role="button" tabindex="0">` — interactive
  content inside interactive content, which HTML does not allow and which
  assistive technology is free to flatten. On a phone that is the whole problem:
  the row is exposed as one button and the ✕ inside it has no reliable identity
  of its own, so the only way to remove a city can disappear from the
  accessibility tree entirely. It also put the visible "✕" inside the row's
  text, so the row's spoken name no longer matched what the row says on screen.
  The row is now a plain container with two sibling controls — the place
  (`.tap`) and the ✕ (`.rm`, a real `<button>`) — which is what the markup
  always meant. Both keep their own name and their own tab stop, and a click on
  the ✕ still removes without selecting, exactly as before.
- **The row icons were part of the spoken name.** The 📍/🔎/🏙️ glyph is
  decoration; the row's name is stated explicitly, so the glyph is now
  `aria-hidden`. The visible text is untouched.
- **The hourly strip could not be scrolled without a pointer on WebViews that
  do not make scroll containers focusable by themselves.** Chromium has put a
  scrollable box in the tab order since 132, and the app's focus-restore code
  already treats `#main .hrs` as a tab stop — on an older WebView (Android 6–10
  devices whose WebView cannot be updated) that code path was dead and the next
  8 hours could not be reached by keyboard or switch access. It carries
  `tabindex="0"` now, so it is a tab stop everywhere, and it looks identical
  where it already was one.
- Nothing visible changed. In-page A/B — the old row markup and the new one
  rendered in the *same* page session, so backdrop blur, scene and scroll are
  identical — gives **0 differing pixels of 1 548 000** for the saved-places
  list and for a search-results list, with every element's layout box
  (`offsetLeft/Top/Width/Height`) and computed style identical apart from
  `appearance`/`unicode-bidi` on the elements that changed tag and the flex
  `margin-left:auto` the new sibling layout replaces. The press animation, the
  row's lit background and its hit area are unchanged: the place control keeps
  the row's padding under its own negative margin, so a tap anywhere on the row
  still lands on the place (measured: `elementFromPoint` at the row's corner
  returns `.tap`).
- Verified: `node --check` on the page's script; headless Chromium loads with
  **zero console messages, warnings and page errors** across seven payloads
  (clear, cloudy, rain, snow, storm, fog, an unknown WMO code) through a smoke
  run of the tabs, the sheet with a typed query, a removal, the °C/°F toggle,
  the settings panel and a 400×780 resize at DPR 3. The fix itself, measured
  with the sheet settled and its list scrolled to the top (axe skips rows that
  are off screen, so an unsettled sheet reports nothing at all — the first
  reading of this pass was a false clean): axe-core goes from
  `nested-interactive` ×3 to **none** in the sheet, and from
  `scrollable-region-focusable` ×1 to **none** on the forecast screen. The ✕ is
  a sibling `<button>` now, reachable by Tab in its own right; Enter and Space
  on it remove **exactly one** city per press (the old `keydown` shim is skipped
  for a real button, so a native activation cannot fire twice); a click on it
  removes without selecting; and the row's spoken name is "Pune, Maharashtra,
  India" against visible text "Pune Maharashtra, India".
- `versionCode 67` / `versionName 1.10.3` in `android/AndroidManifest.xml` (up
  from 66 / 1.10.2), same signing key. `android/assets/index.html` is
  byte-identical to `web/index.html` (SHA-256 `2df0eb7d…`). The APK **was**
  rebuilt from this tree with `android/build.sh` (JDK 17, build-tools 34.0.0,
  platform 34), bundles the current page, carries `versionCode 67` /
  `versionName 1.10.3`, and `.github/scripts/verify_apk.py` agrees on all three.
  `CHECKSUMS.txt` and the `sha256sum` block in `README.md` carry the new digest,
  `3ce265eae573fa9c63e74985c518e5b73cc0c294bc327c04f158155f62a0b329`
  (`verify_docs.py` green), and `apksigner verify --print-certs` still reports
  the project key (`2035d69f…`, `CN=Liquid Weather`).
- Left alone deliberately. (1) The ten rows axe still flags for
  `label-content-name-mismatch` keep their decorative glyph: the check compares
  the row's spoken name with *all* the text painted in it, emoji included, so
  the only way to silence it is to put "🏙️"/"🔎"/"📍" into the spoken name —
  which is exactly what a screen reader should not be read. A decorative icon
  is not a text label for WCAG 2.5.3 (voice control says "Pune", not the
  glyph), so the finding stays as a known heuristic, not a defect. (2) The five
  sliders still have no `aria-valuetext`,
  so a range is announced as "Transparency, 50" without the "%" the panel shows
  next to it; the value is announced and the unit is visible, so this is a
  preference rather than a defect, and it is the settings panel's own pass.
  (3) The top bar's city name is still 2.97:1 on the fog scene, as the 11
  November pass recorded — a contrast fix is a colour change and the UI is
  frozen. (4) The forecast screen still has no live region announcing that a
  load finished; `#main` is replaced wholesale, and a polite region around it
  would re-announce the whole page on every refresh, so that needs a pass that
  can measure the announcement order rather than a guess. (5) The two dialogs
  still do not trap Tab: the nav sits above both panels and is deliberately how
  you leave them (recorded when the panels were made `inert`). (6) The
  `#gear` click handler in `openSettings` still names an element that the
  markup no longer contains — dead code, not an accessibility defect, and
  removing it belongs to a hygiene pass.

### Fixed — render performance (2026-11-13, 12:00 IST pass)
- **A blank particle canvas kept 6.2 MB of pixels for the whole session.** The
  `#fx` backing store is 430×900 at the device pixel ratio, so 860×1800 at DPR 2
  — 1 548 000 pixels, 6.19 MB — and it was allocated once at launch and never
  given back. Clear, mainly-clear, cloudy and foggy skies seed **no particles at
  all** (`seed()` returns an empty field for them), so a reader whose city is
  clear paid 6.19 MB of WebView memory, and a 6.19 MB compositor texture for a
  layer that carries `will-change: transform`, for a canvas that is blank from
  launch to launch and never draws a pixel. Measured in headless Chromium on
  `1.10.1`: `#fx` is `860×1800` with `P.length === 0` on a clear sky, a cloudy
  sky and a foggy one. The store is now released (attributes set to 0, which
  drops the bitmap; the element's CSS size is untouched, so nothing moves) when
  a scene seeds nothing, and taken again — `fitCanvas()` at the same W/H/DPR,
  with the same `setTransform` — the moment a scene seeds particles. On the same
  measurements: clear, cloudy and foggy skies now hold a `0×0` canvas, rain
  keeps `860×1800` with its 170 drops, rain → clear gives the pixels back, and
  clear → rain allocates and paints again (0 → 22 sampled non-transparent
  pixels). A resize on a clear sky no longer reallocates either: ten `size()`
  calls and a 430×900 → 390×844 viewport change leave the canvas at `0×0`.
- **Reduce motion paid for a picture it never draws.** With the setting on, the
  loop cleared the canvas once and stopped, but the 6.19 MB stayed allocated for
  a field that cannot be drawn until the setting changes. Dropping the store
  blanks the canvas in one go — exactly what that single clearing frame did — so
  the pixels are now released instead, and `startFx()` sizes the canvas again
  when the setting is turned off, which resumes the same drops in the same
  places (measured: `0×0` with 170 drops held while the setting is on, then
  `860×1800` and 24 painted samples after switching it off, zero re-seeds).
- **Nine blurred cloud layers and the sun kept animating while invisible.** The
  number of drifting clouds follows the forecast's cloud cover, so a clear sky
  holds eight of the nine at `opacity: 0`; the sun is at `opacity: 0` for every
  rain, snow, fog and storm scene and for the whole night. Both carry a
  compositor animation that ran regardless — each cloud is a
  `will-change: transform` layer over a `blur(16px)` drifting on a 50–110 s
  loop, the sun a 220px radial gradient pulsing through a 12% scale every 6 s —
  so the app was animating up to nine invisible layers from launch to launch.
  A hidden one is now paused (`animation-play-state`, after its 1.2 s opacity
  fade has finished, so nothing is ever frozen while any part of it is on
  screen) and a shown one resumed immediately, so a cloud still fades in while
  drifting. Measured on a clear day: 8 of 9 drift animations paused, 1 running;
  on a cloudy, rainy or stormy day all nine keep running; the sun's pulse is
  paused in rain, snow and storm and running in clear and cloudy skies.
- Nothing visible changed. `#main`'s markup is byte-identical to 1.10.1 across
  four payloads (clear day, cloudy day, rain, snow), the nine settings variables
  are identical, and the computed styles of 24 selectors (bar, hero, cards,
  hourly strip, daily rows, nav, pill, photo layer, active scene, clouds,
  canvas, orbs, panels) match — the only difference is `#sun`'s transform, which
  is the phase of its infinite 6 s pulse, frozen behind `opacity: 0` where it is
  paused and unobservable either way. Full-page screenshots of the 430×900 phone
  at DPR 2 are **pixel-identical** (0 differing pixels of 1 548 000) for the
  clear and cloudy skies with `Math.random` seeded and the animation clock
  pinned, and the particle field is unchanged where it matters: one deterministic
  frame through the real `tick()` hashes identically before and after — rain
  `68c71c9` with 211 painted samples, snow `1d7d0001` with 97. Cloud geometry
  (width, top, duration, negative delay) is identical under a seeded RNG; the
  only difference in a cloud's style attribute is the paused play-state of the
  ones at `opacity: 0`.
- **Left alone deliberately.** (1) The photo layer still builds a fresh `Image`
  per render — re-measured at 0.035 ms on an already-decoded picture, which is
  the number 1.8.10 recorded when it deferred this to a render pass; the
  assignment that follows is a full-screen layer the reader is already looking
  at, and skipping it would need a cache keyed on URL + scrim + cover for a cost
  that does not show. (2) `placePill()` still forces one style recalculation per
  pill move by reading the target tab's `offsetLeft`/`offsetWidth` after the
  previous move wrote the pill's; moving the strip's `scrollWidth` read ahead of
  the writes was tried and measured **8 → 7 recalcs per eight moves**, because
  the read that costs is the tab measurement, not the strip's, so the change was
  reverted rather than shipped as churn. (3) The canvas keeps its store while
  the page is hidden: releasing it there would free 6.19 MB in the background
  but reallocate on return for a field that is already correct. (4) The 60-second
  refresh interval and the `deviceorientation` subscription that 1.8.10 weighed
  are unchanged.
- Verified: `node --check` on the page's script; headless Chromium loads of
  `web/index.html` with mocked forecast, geocoder and Commons responses
  reporting **zero console errors, warnings and page errors** across clear,
  cloudy, rain, snow and storm payloads, and through a smoke run of every panel
  (tabs, search sheet with a typed query, °C/°F toggle, three scene switches,
  a resize to 400×780 at DPR 3, six pill moves, the settings panel and a
  visibility flip) that ends with the storm's 260 particles drawn on a correctly
  sized `800×1560` canvas. `versionCode 66` / `versionName 1.10.2` in
  `android/AndroidManifest.xml` (up from 65 / 1.10.1), same signing key. The APK
  was rebuilt from this tree with `android/build.sh` (JDK 17, build-tools
  34.0.0, platform 34); it bundles `assets/index.html` byte-identical to
  `web/index.html` (SHA-256 `c12d598d…`), carries `versionCode 66` /
  `versionName 1.10.2`, and `.github/scripts/verify_apk.py` agrees on all three.
  `apksigner verify --print-certs` still reports the project key (`2035d69f…`,
  `CN=Liquid Weather`). `CHECKSUMS.txt` carries the new digest,
  `adbc03572aca4c478cbf00da6a2ae30f41d780f924467d3c8621db4a8c6c80e1` (101 KB),
  as does the `sha256sum` block in `README.md` (`verify_docs.py` green).

### Fixed — network & API robustness (2026-11-13, 08:00 IST pass)
- **A busy city-photo lookup was remembered as "this city has no photo" for
  three weeks.** MediaWiki reports an API-level failure with **HTTP 200 and an
  `error` object in the body** — a rate limit, an internal error, a parameter it
  no longer accepts — so the status says nothing and only the body knows.
  `commonsCityPhotoWith()` checked `r.ok` and then read the body as data: the
  missing `query.pages` became an empty page list, the function returned `null`
  with `failed` still `false`, and `fetchCityPhoto()` cached `{none:1}` for the
  city — the record that means "the API answered, and this city has no usable
  file". That record is honoured for the whole 21-day `PHOTO_TTL`, and no
  `photoFail` marker was left either, so the API was not asked again: one
  rate-limited answer kept that city without a backdrop until 3 December. The
  record also takes one of the twelve slots `readPhotoStore()` keeps, so a few
  of them start evicting cities that do have photos. An `error` body is now
  thrown, which is the path an HTTP error already took — a lookup that could
  not be made: nothing cached, the five-minute `photoFail` backoff applies, and
  the second (bare-term) query is skipped exactly as it is for a non-2xx
  answer, because a busy API is not asked twice in the same breath.
- Measured in headless Chromium, one city with no stored photo and Commons
  answering `{"error":{"code":"ratelimited","info":"…"}}` to both queries:
  before the change `localStorage.lw_photos` ended as
  `{"c19.076,72.878":{"none":1,…}}` with `photoFail` empty; after it,
  `lw_photos` is untouched and `photoFail` holds that key (retry in five
  minutes). Nothing regressed on the two answers that must stay cached: a valid
  Commons page still stores the photo (URL, author, licence, title and the
  credit line unchanged) and an empty-but-valid `query.pages` still stores
  `{none:1}`, so "there is no photo for this city" does not turn into a retry
  loop.
- **Left alone deliberately.** `getJSON()` still runs one deadline for the whole
  call, retry included, so a server that answers 503 at 11.5s gets its retry
  aborted at 12s — that is the behaviour 1.2.4 chose on purpose ("an offline
  device still fails at the normal deadline instead of waiting three times as
  long"), and widening it would leave the loading skeleton up for up to 24s.
  Also left alone: `Retry-After` is read in its numeric form only (the
  HTTP-date form falls back to the 300ms default), and the body of a retried
  non-2xx response is neither read nor cancelled, which costs one keep-alive
  connection for a few hundred milliseconds and nothing a reader can see.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder and Commons responses
  reporting **zero console errors and zero page errors**; a before/after
  comparison of the rendered `#main` markup, twelve elements' computed styles
  and the nine settings variables, **byte-identical** for the same payload; and
  the targeted checks above. `versionCode 65` / `versionName 1.10.1` in
  `android/AndroidManifest.xml` (up from 64 / 1.10), same signing key. The APK
  was rebuilt from this tree with `android/build.sh` (JDK 17, build-tools
  34.0.0, platform 34); it bundles `assets/index.html` byte-identical to
  `web/index.html` (SHA-256 `71377649…`), carries `versionCode 65` /
  `versionName 1.10.1`, and `.github/scripts/verify_apk.py` agrees on all
  three. `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`). `CHECKSUMS.txt` carries the new digest,
  `88745efda02010ca27975b31182ae9a73b2ac60d502a20f68fe8f15d7edcaeb8` (101 KB),
  as does the `sha256sum` block in `README.md` (`verify_docs.py` green).

### Clean — weather-code coverage (2026-11-12, 22:00 IST pass)
- **Nothing shippable found in the area; the page is unchanged.** The whole
  code path was read end to end and then exercised rather than eyeballed: the
  `WMO` table, `codeInfo()`, `iconFor()`, `scene()` and the six `SCENES`
  entries, `summarise()`, `applyPhoto()`'s choice of scene photo, and both
  sources of the day/night answer — `isDayNow()`'s sunrise/sunset comparison
  and the payload's own `is_day`.
- **What was checked, and came back consistent.** All 28 documented codes plus
  seven the table does not know (4, 30, 60, 70, 90, 100, 200), day and night —
  70 states, each rendered through the app's own `render()` — with the hero
  label, the `bg-*` element left on, the sun and moon opacities, all eight
  hourly glyphs, all seven daily glyphs, the particle mode and count, `--cc`
  and the cloud-host opacity recorded. The table is complete (28 of 28), every
  code reaches a scene, every scene carries its day and night fields, and an
  unknown code renders "Cloudy" / `bg-*-cloud` / ☁️ / "Mixed conditions." in
  both halves of the day, which is the fallback 1.3.2 and 1.4.1 put in place.
- **No scene leaves state behind.** Sixty sequential renders (every code, day
  then night, in order) were compared with sixty rendered from a neutral state:
  identical in all eleven observed fields, and the particle canvas holds no
  paint after a scene that seeds no particles (`getImageData` over the backing
  store), so switching from rain or snow to a clear or cloudy sky clears the
  field instead of freezing one frame of it.
- **Real payloads render consistently.** Four live Open-Meteo responses —
  Reykjavík, Singapore (a city that has crossed midnight), Mumbai and Tromsø
  (a polar one) — drew strip, daily rows, hero, summary and sunline that agree
  with their own codes and `is_day`, with zero console and page errors. The five
  scene-photo URLs all answer 200 `image/jpeg`.
- **Left alone deliberately, because a fix would visibly change the screen:**
  (1) **85 and 86 draw 🌨️ at night** where 71–77 draw ❄️ — a sun-behind-cloud
  glyph over a night sky; recorded as frozen in 1.4.1 and still frozen, since
  the only fix is a different icon. (2) **The 7-day rows always use the daytime
  glyph**, because Open-Meteo's daily block carries no `is_day`; choosing one
  would be a new rule, not a fix. (3) **The "Now" cell takes its day/night from
  the payload's hourly `is_day`, not from `isDayNow()`**, so within an hour of
  sunrise or sunset it can show the other half's glyph while the sky behind it
  has already switched; the mismatch is visible, so it is written down here.
  (4) **The snow sentence still calls code 73 ("Snow") "Light snow"** and 81
  ("Showers") "heavy at times" — wording, and wording is frozen.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder and Commons responses
  reporting **zero console errors and zero page errors** (hero "Clear sky", the
  night sky `bg-n-sun`, eight hourly cells, seven daily rows, the °C/°F toggle
  and the search sheet driven in the same run).

### Fixed — geolocation edge cases (2026-11-12, 20:00 IST pass)
- **Two location prompts open at once left the first one unanswered for good.**
  `onGeolocationPermissionsShowPrompt()` kept a single callback pair in
  `geoCallback`/`geoOrigin`, and the page can have two `getCurrentPosition()`
  calls out at the same time: the silent `locate()` at boot, and a tap on "Use
  my current location" while that system dialog is still up (the search sheet
  is reachable from the "Locating…" skeleton, so that is exactly where a reader
  lands when a cold fix is slow). The later prompt overwrote the earlier
  callback, that callback was never invoked, and the WebView therefore never
  answered the page's first request: `locate()` sat on its watchdog and gave up
  — toasting "Could not reach your location" and rewriting the pinned row as a
  saved "New Delhi" with `myLoc:false`, after which location is never asked for
  again. The waiting callbacks are now kept in arrival order and answered
  together by `answerGeo()` on the permission result and on teardown, and a
  second prompt joins the system request already out instead of calling
  `requestPermissions()` again — a request issued while another is being
  answered is dropped by the platform, so its result would never arrive.
- This pass changed Java only, so `versionCode`, the committed APK and
  `CHECKSUMS.txt` were left alone and still agreed with each other; the fix
  reaches the published APK with the 22:00 rebuild below, which also carries
  this entry into the changelog.
### Fixed — search & geocoding (2026-11-12, 16:00 IST pass)
- **A country query listed the same place twice, once under each of its two
  names.** The bundled rows a country query adds ("Japan" → Tokyo, Osaka,
  Sapporo) were merged with the geocoder's answer by folded *name* alone, while
  every other pair of rows in the sheet — two geocoder rows, two saved rows, a
  result and a saved row — is compared with `samePlace()`/`sameLabel()`, the
  rule for "two rows a reader cannot tell apart". Name alone misses the case
  that matters: the bundled **Delhi** sits at 28.6139, 77.209, exactly where
  Open-Meteo puts **New Delhi**, so typing "india" listed that one point twice
  — "Delhi, India" and "New Delhi, Delhi, India". Both rows were flagged as the
  saved place (📍, because `samePlace()` says they are the same place) and both
  carried a ✕ that deleted the same saved row, so the sheet showed one place as
  two, with two delete controls for it. The bundled rows are now also dropped
  when they are the same place as a row already listed, using the same
  `samePlace()`/`sameLabel()` pair `dedupe()` applies to the geocoder's own
  rows; rows that merely share a name keep exactly the behaviour they had.
- Version bumped to 1.9.3 (`versionCode 63`), same signing key, so it installs
  over 1.9.2; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `43d5df71…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0 + platform 34), bundles that same page, carries
  `versionCode 63` / `versionName 1.9.3` (`.github/scripts/verify_apk.py` agrees
  on all three), and `CHECKSUMS.txt` carries the new digest (`ff91d34c…`), as
  does the `sha256sum` block in `README.md` (checked by `verify_docs.py`).
  `apksigner verify --print-certs` still reports the project key (`2035d69f…`,
  `CN=Liquid Weather`).

### Notes
- No visual change: the edit is one filter inside `search()`; no markup, CSS,
  wording, colours, spacing, gradients, glass values or animation timings were
  touched, and the row that a reader sees is the geocoder's own (same title,
  same subtitle, same icon, same position in the list) — only the duplicate
  above it is gone.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` at an `https` origin with mocked forecast, geocoder,
  Nominatim and Commons responses reporting **zero console errors and zero page
  errors**; and the fix proved old-against-new with the same mocks and
  Open-Meteo's real answers for eight queries — "india" 8 rows → 7 (the
  duplicate "Delhi, India" gone, status "8 results" → "7 results"), while
  "japan", "united states", "australia", "singapore", "korea", "mumbai" and
  "mumbai india" came back **identical in rows, order, subtitles, icons and
  status text**, so the merge rule changed nothing else.
- Left alone deliberately: (1) **the country list still matches only the start
  of a country's name** (`countryMatches()`), so "korea" or "emirates" gets no
  bundled cities from it and relies on the wider token rule in
  `localMatches()` — widening it changes what a country query returns, which is
  a behaviour decision, not a bug fix. (2) **Typing "uk" offline answers Kyiv**,
  because the token rule matches "uk" as the start of "Ukraine"; "UK" is not a
  country label anywhere in the bundled list, and the obvious fixes all change
  which cities other queries find. (3) **"st." matches every US city**, for the
  same reason ("States"). (4) **A country query still drops a geocoder row that merely
  shares its name with a bundled one, even when it is a different city far
  away** — that name rule is what stops the sheet printing a country's own
  cities twice, and making it distance-aware changes what a country query
  returns, so it waits for its own pass.

### Fixed — geolocation edge cases (2026-11-12, 10:00 IST pass)
- **A fix that arrived inside the time the app had asked for was thrown away
  whenever the reader took a few seconds to answer the location prompt.** The
  watchdog that guarantees `getPosition()` settles counts from the call, but the
  `timeout: 12000` handed to `navigator.geolocation.getCurrentPosition` only
  starts once a permission decision exists, so the two were never the same
  clock and the watchdog could fire *before* the deadline it exists to back up.
  A prompt answered after ten seconds and a first fix eight seconds later —
  inside the 12s the page asks for, and an ordinary wait for both — arrives at
  eighteen, three seconds after the watchdog had given up. Giving up is not
  harmless: `locate()` then calls `fallbackPlace()`, which rewrites the pinned
  row as a saved "New Delhi" with `myLoc:false`, and every later launch sees a
  row that already has coordinates and never asks for a position again — one
  slow but successful fix disabled "My Location" for the app for good, with no
  prompt, no retry and nothing on screen to say so. `getPosition()` now asks
  the browser once, at the start, whether that decision is still pending
  (`navigator.permissions.query({name:'geolocation'})`) and, when it is, allows
  the reader's answer plus the browser's own 12s before expiring. Nothing on
  screen changes: the same skeleton, the same toast, the same fallback — only
  later, and only when a fix is still legitimately in flight.
- Version bumped to 1.9.2 (`versionCode 62`), same signing key, so it installs
  over 1.9.1; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `1d6cf1fa…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0 + platform 34), bundles that same page, carries
  `versionCode 62` / `versionName 1.9.2` (`.github/scripts/verify_apk.py` agrees
  on all three), and `CHECKSUMS.txt` carries the new digest
  (`0f7cc77e…`), as does the `sha256sum` block in `README.md` (checked by
  `verify_docs.py`). `apksigner verify --print-certs` still reports the project
  key (`2035d69f…`, `CN=Liquid Weather`).

### Notes
- No visual change: the edit is inside `getPosition()` and adds one helper
  (`geoDecisionPending()`, `GEO_PROMPT_ALLOW`); no markup, CSS, wording,
  colours or animation timings were touched, and the expiry path still ends in
  the same `Error('timeout')` the old watchdog produced, so the toast, the
  fallback and the skeleton are exactly what 1.9.1 shows — only later.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` at an `https` origin with mocked forecast, geocoder, Commons
  and position responses reporting **zero console errors and zero page errors**
  in five states (fast fix, denial, geocoder 500 on both services, a prompt
  never answered, a fix at 18s). The fix itself was proved old-against-new with
  the same mocks and a `navigator.permissions` stub: a prompt answered at 10s
  with the fix at 18s leaves 1.9.1 on `New Delhi`, `myLoc:false`, with "Could
  not reach your location" and the fix discarded, and 1.9.2 on `Pune`,
  `myLoc:true`, with no toast and the forecast drawn. The regression cases were
  re-run on the new build: permission already granted and no position ever
  delivered still falls back at the 15s deadline (measured: skeleton at 14s,
  fallback by 17s); no Permissions API at all behaves exactly as 1.9.1; a
  denial still toasts "Location is blocked" immediately; a fast fix renders as
  before.
- Left alone deliberately: (1) **an unanswered prompt now holds the skeleton up
  to 35s instead of 15s.** That is the price of not expiring before the
  browser's own deadline, it only happens while the system dialog is up, and
  the screen is still escapable — the city name in the skeleton opens the
  search sheet. (2) **A failed location attempt still turns the pinned row into
  a saved "New Delhi"**, including a timeout that is not a permission answer;
  keeping the row pinned instead would change what the Cities list shows, and
  the UI is frozen. (3) **The app still never asks for a position again after
  that**, even if the reader later grants permission in Android settings;
  re-prompting is a behaviour decision, not a bug fix. (4) **A second
  `onGeolocationPermissionsShowPrompt` while the first is pending still
  overwrites the stored callback** (recorded in 1.9.1); the watchdog still
  bounds the request it abandons, and answering the abandoned callback is a
  Java change this pass did not need. (5) **A pinned row's coordinates are
  still never refreshed** by the ten-minute auto-refresh, which re-fetches the
  forecast, not the position.

### Fixed — build & release hygiene (2026-11-12, 08:00 IST pass)
- **The install instructions told every downloader to expect an older build's
  checksum.** The verification block in `README.md` printed `f8a52080…` — the
  1.7 APK — while `CHECKSUMS.txt`, the committed `LiquidWeather.apk` and every
  release since 1.8 carried `042f58b6…` (the 1.9.1 build). A reader who ran the
  two commands exactly as printed got `LiquidWeather.apk: FAILED` on a download
  that was precisely the file this repository publishes, and a checksum that
  fails on a good file reads as a corrupted or tampered download — worse than
  printing none. The block now prints the digest of the committed APK, the same
  value as `CHECKSUMS.txt`, and nothing else in the README prints a digest.
- **The version and size the same docs advertise had drifted too.** `README.md`
  said `Latest APK: v1.7` (the latest release is v1.9) and "93 KB";
  `STORE.md` said everything in it "matches the current release, `v1.2`" and
  quoted 65 KB in three places, including the short description a store would
  publish. The committed APK is 99,176 bytes (97 KB). Both files now name v1.9
  and 97 KB.
- **Why it cannot drift again:** a new `.github/scripts/verify_docs.py` reads
  the digest out of the README's `sha256sum LiquidWeather.apk` block and
  requires it to equal both `CHECKSUMS.txt`'s digest and the SHA-256 of the
  committed APK; a README with no digest, with two different digests, or with a
  stray digest left in the prose fails the build. `.github/workflows/build.yml`
  runs it next to the existing `CHECKSUMS.txt` and `verify_apk.py` steps, before
  anything is built. This is the third copy of one value — `CHECKSUMS.txt` and
  the APK were already checked, the README never was — which is the same defect
  family as the duplicate-version and stale-asset checks added on 10 November.

### Notes
- No page change: `web/index.html` is byte-identical to 1.9.1 (SHA-256
  `d3902694…`), so there is no APK rebuild, no `versionCode` bump and no
  `CHECKSUMS.txt` change on this pass; the day's release is still cut from the
  22:00 IST pass.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder, Commons and image responses
  reporting **zero console errors and zero page errors**, with the hero
  rendering the mocked 29°; `python3 .github/scripts/verify_docs.py .` on this
  tree (exit 0); the same script against the pre-fix README (exit 1, naming
  `f8a52080…` against the published `042f58b6…`) and against a deliberately
  stale `CHECKSUMS.txt` (exit 1); and the reader's own command,
  `sha256sum -c` with 1.7's digest, reporting `FAILED` — the symptom this pass
  removes.
- Left alone deliberately: (1) **the "97 KB" figure stays a hand-written
  number.** It is prose, and a machine check would fail CI on every rebuild that
  moves the size by a kilobyte — for a value nobody verifies, unlike the
  digest. (2) **The `Latest APK: vX.Y` label stays manual.** It names the newest
  *release*, which legitimately differs from the manifest's unreleased
  `versionName` (1.9.1 against 1.9), and the workflow cannot see tags at
  `fetch-depth: 1`, so any check would either be wrong or need a fetch this pass
  is not entitled to add. (3) **`CHANGELOG.md`'s own ordering.** `[Unreleased]`
  sits between 1.8.8 and 1.9 rather than at the top, so the newest entry is not
  where a reader looks first; reordering 3,300 lines of release history is not
  something one hygiene pass should risk, and it is written down here instead.

### Clean — time & timezone correctness (2026-11-11, 22:00 IST pass)
- **Nothing shippable found; no code changed.** The whole time path was read end
  to end and exercised: `hourIndex()` (the "Now" cell, including the midnight
  correction), `todayIndex()` (which daily row is "Today", and the hero's
  `H:`/`L:`, the summary's high and low and the UV card that follow it),
  `cityNow()`/`cityDate()` (`utc_offset_seconds` applied to the device's UTC
  clock), `cityClock()`, `sunTimes()`/`isDayNow()` (the scene, the summary's
  night sentences and the sun line), `clock()`/`hl()`/`dayName()` (the labels),
  `uvAt()`, and the two elapsed-time clocks (`mono()`/`aged()` with the
  ten-minute refresh, the ten-minute cache TTL and the focus-restore window).
- Proved, not just read: the eight helpers were lifted out of the page and run
  against 8,640 generated states — every clock hour and the minutes 00/07/15/
  30/45/59, twelve city offsets from -11:00 to +14:00 (including +05:30,
  +05:45 and +09:30), each payload drawn at fetch, +10 min, +1 h, +7 h and
  +25 h — comparing `hourIndex()` and `todayIndex()` with an independent
  oracle (the city's wall clock applied to the payload's own blocks): **zero
  divergences**. The same helpers were then driven through the real page in
  headless Chromium with a mocked forecast, geocoder and Commons: a fresh
  22:07 IST payload, a payload drawn across midnight (fetched 23:50, read at
  00:05 — "Today" moves to the new day, the strip opens on 12 AM, the scene and
  the summary turn to night), the post-midnight window where the API's daily
  block still starts yesterday (labels read `Tue, Today, Thu…` and the hero
  comes from today's row), a London spring-forward night with no 02:00 hour
  (the strip reads 1 AM → 3 AM, nothing repeats, nothing stalls), a New York
  fall-back payload read from an Indian device, a payload with no
  `utc_offset_seconds`, and an hourly block that ends before the current hour.
  Every one renders the correct hour, the correct "Today" row and the correct
  day/night state, with zero console errors and zero page errors.
- Left alone deliberately: (1) **a DST transition inside the cache window.**
  `utc_offset_seconds` is a single number for the whole payload, so a payload
  fetched an hour before a transition and still on screen an hour after it is
  one hour off until the next fetch — at most ten minutes in normal use, and
  fixable only with a timezone database the app deliberately does not carry.
  (2) **"tonight"/"overnight" wording in the small hours.** Every night-time
  sentence is chosen from `isDayNow()` alone, so a clear 03:00 sky reads "Clear
  and calm tonight — good stargazing" and "no rain expected overnight". It is
  the wrong word for the hour, but the sentences are visible copy and the UI is
  frozen; it needs a wording decision, not a bug fix. (3) **A payload more than
  seven days old** (an app left open and offline): its hourly block ends before
  the city's clock, so the strip fills with its last hour and the 7-day list
  falls back to row 0, which is then labelled "Today" over a week-old row.
  Reachable only by leaving the page alive for a week with no successful
  refresh, and the whole screen is that stale by then. (4) **A payload with no
  usable `current.time`** still anchors the strip on the first hour it has,
  which is the documented fallback from 1.3.7 and needs a broken payload, not a
  broken clock.
- No visual change and no behaviour change: `web/index.html` is byte-identical
  to 1.8.15 (SHA-256 `39fb9deb…`). The APK was rebuilt only because this is the
  day's release (see 1.9 below).

### Fixed — network & API robustness (2026-11-11, 20:00 IST pass)
- **Every repaint of the screen cancelled the city-photo lookup and started it
  again.** `render()` calls `applyPhoto()`, which calls `fetchCityPhoto()` for a
  city with no stored photo, and `fetchCityPhoto()` had no idea a lookup was
  already running: it bumped `photoSeq`, aborted `photoCtl` and issued an
  identical request. A lookup in flight for the city on screen was
  indistinguishable from one for a city the reader had left, so the abort that
  exists to supersede a *different* city fired on every repaint — a °C/°F
  toggle, a trip to the Cities tab and back, the ten-minute refresh, a
  forecast landing after its own pre-fetch. Measured in headless Chromium
  against 1.8.14, one city with no stored photo and a 2s Commons response:
  **1 request at load, then 2, then 3 as two unit toggles were tapped**, each
  one cancelling the one before it (`net::ERR_ABORTED`), and the backdrop stayed
  empty until the reader stopped touching the screen; on a slow link the lookup
  could be restarted indefinitely, with the Commons API asked once per repaint
  for the same file and a fresh 10s deadline each time. The same run on this
  build: **1 request, no cancellation, the photo painted at the usual time.**
  The lookup in flight is now remembered by the city it belongs to (`photoKey`,
  cleared in a `finally` when it settles, answered or not), and a render for
  that same city leaves it alone. A request for a different city still
  supersedes it, which is what `photoSeq` and the abort are for: measured on
  this build, a second city asked while Mumbai's lookup was out made 2 requests
  and aborted 1, exactly as before; and with Commons answering 500 the failure
  is still remembered for five minutes and the marker is still released, so the
  next render after the window asks again.
- Version bumped to 1.8.15 (`versionCode 59`), same signing key, so it installs
  over 1.8.14; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `39fb9deb…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0), bundles that same page, carries `versionCode
  59` / `versionName 1.8.15` (`verify_apk.py` agrees on all three), and
  `CHECKSUMS.txt` carries the new digest (`7447e38a…`). `apksigner
  verify --print-certs` still reports the project key (`2035d69f…`, `CN=Liquid
  Weather`).

### Notes
- No visual change: the edit touches only `fetchCityPhoto()`'s bookkeeping —
  no markup, no style, no timing constant. For the same payload, `#main`'s
  markup is byte-identical to 1.8.14's, the visible text is identical, the
  `--k/--glass/--blur/--dp/--pr/--cc` variables are identical, and the computed
  styles of 16 static elements (bar, hero, temperature, condition, cards, the
  hourly strip, a day row, the UV grid, the unit button, the range bar, the
  sunrise line) match on all 20 properties sampled.
- Verified: `node --check` on the page's script; a headless Chromium load with
  mocked forecast, geocoder, Commons and image responses reporting zero page
  errors and zero console errors; 140 random actions over the tabs, the sheet,
  searches, picks, removals, the unit toggle, refresh, the settings slider and
  Escape — once clean, once with 10% of every API response replaced by a 500 and
  6% by an HTML sign-in page — leaving no page error, no `NaN`/`undefined` in
  `#main` and no stuck "Searching…"; and the before/after request counts above.
- Left alone deliberately: `showPhoto()` still sets `img.src` with no way to
  cancel it, so a photo superseded by a newer city finishes downloading (a
  cancelled `<img>` needs its `src` cleared, which fires an error event on a
  layer that is being kept deliberately quiet — worth doing, but it needs its
  own proof); a retried response's body is not consumed or cancelled in
  `getJSON()`, which no measurement here could tie to a real cost; and the
  `online`/`offline` listener noted by the 00:00 pass is still absent for the
  same reason it was then — repainting on a link event is a behaviour decision,
  not a bug fix.

### Fixed — accessibility & semantics (2026-11-11, 18:00 IST pass)
- **Focus on the hourly strip was thrown away by the next render.** The strip is
  a scroll container with no focusable children, so Chrome puts it in the tab
  order — the third stop on the forecast screen, as the 08:00 pass recorded. The
  held-focus mechanism that carries a control across a re-render only remembered
  controls that have an `id`, and the strip has none, so every repaint of `#main`
  dropped focus to `<body>`: a background refresh ten minutes in, a unit toggle
  from the keyboard, a new city's forecast landing. Measured in headless
  Chromium: focus on `.hrs`, then `show(true)` — `document.activeElement` was
  `BODY` before, `.hrs` after.
- **The offline retry card lost focus as soon as the retry worked.** The card is
  a `div` carrying `role="button"` (it has to be reachable without a pointer, so
  it is in the tab order), and it has no `id` either: pressing Enter on it
  fetched the forecast, the retry card was replaced by the new screen, and focus
  went to `<body>` — the reader was left at the top of the document with no way
  back except tabbing the whole page again. Measured: focus on the card, Enter,
  forecast painted — `BODY` before, the city button (`#openSearch`, the first
  control of the new screen) after, the same rule `paintSheet()` already
  follows when the row a reader was on disappears.
  Both are one cause, fixed once: a control is now named across a render by
  whatever still identifies it in the new markup — its `id`, or, for the two
  that have none, the class that marks them out (`focusKeyOf()`) — and if the
  control itself is gone, the first control of the new screen takes the focus
  instead of the document. Focus on every control that already had an `id`
  (unit toggle, city button, settings sliders, sheet rows) behaves exactly as it
  did.
- **The search sheet's section labels were not headings.** "Saved places",
  "Results" and "Popular" are styled as headings and read as ordinary text, so a
  screen reader had no way to jump between the three groups of a list that can
  hold a dozen rows. Each now carries `role="heading"` / `aria-level="2"`; the
  markup and the computed style of `.sh-h` are unchanged (the attributes paint
  nothing), and Chrome's accessibility tree now shows `heading "SAVED PLACES"`
  and `heading "RESULTS"` where it showed no headings at all.
- Version bumped to 1.8.14 (`versionCode 58`), same signing key, so it installs
  over 1.8.13; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `4dea5d41…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0), bundles that same page, carries `versionCode
  58` / `versionName 1.8.14`, and `CHECKSUMS.txt` carries the new digest
  (`54de7b34…`). `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`).

### Notes
- No visual change: for four payloads (clear day, rain at night, thunderstorm,
  fog) `#main`'s markup is byte-identical to 1.8.13's; the sheet's markup
  differs only by the two new attributes per section label; and the computed
  styles of 219-220 elements per scene differ only in the animated layers
  (`#clouds` transforms, the parallax offsets, in-flight opacities), by the same
  amount as the same build differs from itself between two runs. Screenshots are
  not a usable witness here for the same reason — the randomly-seeded layers and
  the glass repaint differ run to run.
- Verified: `node --check` on the page's script; a headless Chromium load with
  mocked forecast, geocoder, Commons and image responses reporting zero page
  errors; 140 random actions over the tabs, the sheet, searches, picks,
  removals, the unit toggle, the settings sliders and Escape with every ninth API
  response replaced by a 500 or a non-JSON body, leaving no page error, no
  `NaN`/`undefined` in `#main` and no stuck "Searching…"; and the before/after
  focus readings above on both builds, plus the six focus paths that already
  worked (unit toggle, sheet opened from the Cities tab and dismissed, sheet
  opened from the city bar and dismissed, picking a city, removing a saved row,
  opening and closing the settings panel) returning identical answers on 1.8.13
  and this build.
- Left alone deliberately: **text contrast over the scenes**, unchanged from the
  08:00 pass — the top bar's city name still falls to 2.97:1 on the fog scene
  where a bright cloud drifts behind it, and every way of raising it (a text
  shadow, a darker glass under the bar) is a visible change. Also left: the 7-day
  rows still announce "Today ☀️ 21° 31°" with no low/high words and the range bar
  still carries no accessible value (both need a visually-hidden text style or a
  restructured row, and a clipped-out `span` per cell is a DOM change I could not
  prove paint-free for a defect a reader can still work out from the order); and
  the ✕ is still a focusable `role="button"` span nested inside the row's
  `<button>`, invalid nesting that Chrome nevertheless exposes with its own name
  and that Enter/Space operate correctly. This pass also could not fix the build
  script for a 2 GB machine — `d8` and `apksigner` ask for more address space
  than this sandbox's `ulimit -v` allows, and the build here needed
  `ulimit -v unlimited` in the shell; that is build hygiene, not this area, so
  `android/build.sh` is unchanged.

### Fixed — accessibility & semantics (2026-11-11, 08:00 IST pass)
- **The search sheet threw keyboard focus away every time it repainted itself.**
  `paintSheet()` replaces the whole list with `innerHTML`, which destroys the
  control that had focus. Only `removeSaved()` ever put focus back, so every
  other repaint — a geocoder answer landing, the pinned row's name arriving,
  another document's saved-list write — dropped focus to `<body>`. The common
  case is the answer: type a query, Tab into the sheet while "Searching…" is on
  screen, and the results replace the list under the keyboard. Measured in
  headless Chromium with the geocoder held for 1.8s, focus on "Use my current
  location" and the answer released: `document.activeElement` was `BODY` after
  the paint, so the next Tab started again from the top of the page, outside the
  sheet, and the list could not be reached without walking the whole document
  again. `paintSheet()` now names the focused control by its own attributes
  before the list is replaced (`#shLoc`, `#shRefresh`, or the row's
  `data-go`/`data-rm2`/`data-rm` value — never its position, which the repaint
  is free to change) and puts focus back on the same control afterwards; if the
  thing they were on is gone, the sheet's first control takes the focus rather
  than the document. Same run on this build: focus is still on
  "Use my current location" after the results are painted.
- **Closing the sheet moved focus out of the nav.** The sheet's own rule is
  "return focus to the control that opened it", but `closeSheet()` always aimed
  at the city button in the top bar. A reader who opened the sheet from the
  Cities tab with the keyboard and closed it with Escape or ✕ was therefore moved
  out of the nav and into the page, onto a control they had never touched — and
  from there Tab walked the forecast instead of the tabs. Two causes, both fixed:
  `setTab('cities')` calls `closeSettings()` first, and `closeSettings()` moved
  focus to the Weather tab whether or not the panel was ever open (so the sheet
  recorded the Weather tab as its opener); and `closeSheet()` had no idea what it
  was opened from. `closeSettings()` now only moves focus when the panel was
  actually open, `openSheet()` records the control it was opened from, and a
  dismissal that is not a city pick returns focus there. Measured: Escape or ✕
  after opening from the Cities tab left focus on "openSearch" in `#main` before,
  on the Cities tab now; picking a city, dismissing a sheet opened by tapping the
  city name, removing a saved row and closing the settings panel all land exactly
  where they did (measured on both builds, same answers).
- **The hourly strip was a focusable control with no accessible name.** Chrome
  puts a scroll container in the tab order when it holds no focusable children,
  so the strip is the third stop on the forecast screen — and it was a bare
  `<div>`: a screen reader announced an unnamed group and nothing about what the
  eight cells were, while the visible heading right above it says "Hourly
  forecast". It now carries `role="group"` and `aria-label="Hourly forecast"`,
  the same words as the heading. Chrome's accessibility tree: before, a focusable
  node with an empty name; now `group "Hourly forecast"`. Tab order is unchanged
  (city button, unit button, strip, tabs), and the attributes paint nothing.
- Version bumped to 1.8.13 (`versionCode 57`), same signing key, so it installs
  over 1.8.12; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `713b0358…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0), bundles that same page, carries `versionCode
  57` / `versionName 1.8.13`, and `CHECKSUMS.txt` carries the new digest
  (`a7d40587…`). `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`).

### Notes
- No visual change: for five payloads (clear day, cloudy day, rain at night,
  thunderstorm, fog) the `#main` markup is identical apart from the two
  attributes added to the strip, the computed styles of the hero, temperature,
  condition, glass card, nav and the `--k/--glass/--blur/--dp/--pr/--cc`
  variables are identical, and full-screen screenshots with the randomly-seeded
  layers (`#fx`, `#clouds`, `#photo`) hidden are byte-identical between 1.8.12
  and this build.
- Verified: `node --check` on the page's script; a headless Chromium load with
  mocked storage, forecast, geocoder, Commons and image responses reporting zero
  console messages and zero page errors; 140 random actions over the tabs, the
  sheet, searches, picks, removals, the unit toggle, the settings sliders and
  Escape with every ninth API response replaced by a 500, a 429 with
  `Retry-After`, `{"current":{}}`, non-JSON or a sign-in page, leaving no console
  error, no page error, no `NaN`/`undefined` in `#main` and no stuck
  "Searching…"; and the three fixes proved by the before/after focus and
  accessibility-tree readings above.
- Left alone deliberately: **text contrast over the scenes.** Every text style
  was measured against its own painted background on all six scenes by day and
  night (108 readings): all pass 4.5:1 except the top bar's city name on the fog
  scene, which fell to **2.97:1** where a bright drifting cloud sat behind it
  (next lowest: 5.86:1). Fixing it means a text shadow or a darker glass under
  the bar — a visible change, so it is written down instead. Also left: the 7-day
  rows announce "Today ☀️ 21° 31°" with no low/high words and the range bar
  carries no accessible value; the sheet's "Saved places" / "Results" / "Popular"
  labels are styled as headings but are not headings, so a screen reader cannot
  jump between them; and the ✕ is a focusable `role="button"` span nested inside
  the row's `<button>` (invalid nesting, though Chrome exposes it with its own
  name and Enter/Space works) — restructuring the rows risks the row layout for a
  defect no reader can currently hear or press wrongly.

### Fixed — network & API robustness (2026-11-11, 00:00 IST pass)
- **The reverse-geocode pair was the one request in the app that could not be
  cancelled, so an abandoned location request kept talking to both geocoders.**
  Every other request takes a signal and every superseded one is aborted: the
  forecast fetch (`fcCtl`), the forecast pre-fetch a location request starts
  (`prefCtl`), the photo lookup (`photoCtl`) and the search (`searchCtl`).
  `reverseName()` was called with none, so a location request that a newer one
  had replaced went on asking anyway. Tapping "Use my current location" twice a
  moment apart left four requests in flight for one place: the abandoned pair
  ran to its own 8s deadline (16s when the first service failed and the second
  was tried), holding the radio awake for an answer nothing would read, and it
  fired Nominatim's reverse endpoint for a place nobody had asked about — a
  service whose usage policy is one request a second, which answers a burst by
  blocking. Measured in headless Chromium against 1.8.11 with a 4s geocoder and
  two taps 600ms apart: **three reverse requests started, none cancelled, all
  three delivered**. `locate()` now keeps the controller for the name lookup it
  starts (`nameCtl`) beside the one for its pre-fetch, aborts it when a newer
  request takes over, and `reverseName()` takes the signal and returns `null`
  once it is aborted — the same "no name came back" answer the 2.5s name budget
  already hands the caller, so a superseded request paints nothing and the row
  keeps the coordinates the request that replaced it will name. The same run on
  this build: **three started, the two abandoned ones aborted within
  milliseconds (`net::ERR_ABORTED`), one delivered**, and with the first service
  answering 400 so the second is asked: three Nominatim requests on 1.8.11, all
  three delivered, against one delivered and two aborted here.
- Version bumped to 1.8.12 (`versionCode 56`), same signing key, so it installs
  over 1.8.11; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `0e342a7c…`), the APK was rebuilt from it with `android/build.sh`
  (JDK 17 + build-tools 34.0.0), bundles that same page, carries `versionCode
  56` / `versionName 1.8.12`, and `CHECKSUMS.txt` carries the new digest
  (`6ef002dc…`). `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`).

### Notes
- No visual change: for the same payload the rendered `#main` markup, the
  `--k/--glass/--blur/--dp/--pr/--cc` variables and the computed styles of the
  hero, the cards, the nav, the pill, the photo layer and the active scene are
  byte-identical to 1.8.11 across five control payloads (clear day, partly
  cloudy, rain at night, thunderstorm, fog), and the name still fills in on the
  same schedule when it arrives after the 2.5s budget (`My Location` →
  `My Location, 19.08, 72.88` → `Mumbai, India`, sampled at 1/2.5/3.6/6/9s, the
  same timeline on both builds).
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked storage, forecast, geocoder, Commons and image
  responses reporting zero console messages and zero page errors in all five
  control scenarios; 90 random actions over the tabs, the
  sheet, searches, saves, removals, the unit toggle, refresh and Escape with
  10% of every API response replaced by a 408/429/500/502/503 (some with
  `Retry-After`) and 6% by an HTML sign-in page, a truncated payload, `{}`, `[]`
  or non-JSON, leaving no console error, no page error, no `NaN` in the DOM and
  no stuck "Searching…"; and the fix itself proved by the before/after
  cancellation counts above.
- Left alone deliberately: a device that loses the link keeps the retry card
  until the reader taps it or the ten-minute refresh comes round — there is no
  `online` listener, and adding one would repaint the screen at a moment the
  reader did not ask for, which is a behaviour decision rather than a bug fix.
  Also left: `autoRefresh()` moves its own mark even when the refresh it started
  fails, so a failed automatic refresh is not retried for ten minutes (the same
  deliberate brake on hammering a link that is down); `getJSON()`'s one retry
  shares the caller's single deadline, so a 429 that arrives late in the budget
  leaves the retry little time (capping `Retry-After` at 2s is the documented
  trade); and the city photo's `thumburl` is stored sliced to 400 characters,
  which no live Commons URL reached this pass (the longest of twelve city
  queries was 271).

### Fixed — build & release hygiene (2026-11-10, 20:00 IST pass)
- **Nothing compared the committed APK with the sources it claims to be built
  from.** `CHECKSUMS.txt` only proves that the `LiquidWeather.apk` in the repo is
  the file the digest was taken from — a stale APK has a perfectly valid
  checksum of its own — so two failures were invisible until someone installed
  the release. First, the APK can bundle an older `assets/index.html` than
  `web/index.html`: `android/build.sh` compares those two files at build time,
  which stops a build made from a stale copy, but nothing looked at the page
  inside the APK that is committed and published, so a pass that edited the
  page, copied it into `android/assets/` and committed without rebuilding left
  every source-side check green and shipped the previous app under a new
  version number — exactly how the 1.8.4 APK came to carry 1.8.3's page.
  Second, the APK's `versionCode`/`versionName` can disagree with
  `android/AndroidManifest.xml` if the manifest was bumped and the APK was not
  rebuilt (or an older APK was restored over a newer one), and the manifest is
  the single home of the version. A new gate,
  `.github/scripts/verify_apk.py`, reads both versions out of the APK's binary
  manifest, compares them with `android/AndroidManifest.xml`, and compares the
  SHA-256 of the APK's bundled `assets/index.html` with `web/index.html`; the
  CI build job runs it before it builds anything, so the mismatch fails the
  push instead of a downloader.

### Notes
- No app change of any kind: `web/index.html` is untouched (SHA-256 still
  `220d3a5d…`, byte-identical to `android/assets/index.html`), so there is no
  new APK, no version bump and no change to `CHECKSUMS.txt` on this pass.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder, Commons and image responses
  reporting zero console errors or warnings, zero page errors and zero failed
  requests
  (282 DOM nodes, the forecast drawn); the new gate exits 0 on the tree as
  committed and 1 on each of the three failures it guards — a manifest bumped
  to 56/1.8.12 with the 55/1.8.11 APK left in place, one byte appended to
  `web/index.html` after the build, and a missing APK — each naming the file and
  the mismatch; and `build.yml` still parses as YAML.
- Left alone deliberately: the shipped `LiquidWeather.apk` is 1.8.11
  (`versionCode 55`) while the latest release is still v1.8 (`versionCode 44`) —
  today's release is cut from the 22:00 pass, and this environment has no JDK or
  Android SDK, so nothing here can be rebuilt or re-signed anyway. Also left:
  `README.md` still advertises "Latest APK: v1.7" on line 8 while v1.8 is the
  latest release (a doc line that moves with each release), `build.sh` still
  does not copy its APK to the repository root or rewrite `CHECKSUMS.txt` (a
  behaviour change for the maintainer, recorded in 1.8.8), and "`versionCode`
  only ever increases" still has no gate — that needs the history of published
  APKs, not the single committed one.

### Fixed — search & geocoding (2026-11-10, 18:00 IST pass)
- **A query in the form the search sheet itself prints found nothing.** Every
  row in that sheet is labelled "city, country" — "Mumbai, India", which is also
  the row's accessible name — and the bundled list that answers when the
  geocoders cannot could not be found by that label. `localMatches()` tested the
  whole query as the *start* of one city name or one country, and that is all it
  tested, so "mumbai india", "mumbai, india" and even "mumbai," each answered
  "No place called …" with Mumbai sitting in `POPULAR`; the same was true of
  every "city country" query, and of a country named by a word that is not its
  first — "korea" matched nothing although Seoul, South Korea is in the list,
  because the country is filed under "South Korea". It shows only when the
  geocoders cannot answer, since this list *is* the fallback — which is exactly
  when it is the whole answer a reader can get. When the old rule finds nothing
  the query is now split into words and a place matches when every word starts a
  word of its city name or of its country: "mumbai, india" finds Mumbai,
  "korea" finds Seoul, "london paris" still finds nothing because no place
  carries both, and a word shorter than two letters leaves the query unanswered
  as before. Anything the old rule already answered is untouched — it is tried
  first and returns before the new one runs.
- Version bumped to 1.8.11 (`versionCode 55`), same signing key, so it installs
  over 1.8.10; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `220d3a5d…`), the APK rebuilt from it bundles that same page and
  carries `versionCode 55` / `versionName 1.8.11`, and `CHECKSUMS.txt` carries
  the new digest (`446e2c70…`).

### Notes
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked storage, forecast, Commons and geocoder responses
  reporting zero console messages and zero page errors; and the fix measured on
  281 queries against the previous build with both geocoders failing — 11
  answered differently and every one of them went from "no results" to the right
  city, while the other 270 returned byte-identical rows (all 26 single letters,
  all 140 bundled city names, all 70 country names, and 45 partial and odd
  queries). Tapping the new row for "mumbai, india" saves Mumbai at
  19.076, 72.8777 and the app draws its forecast; "london paris" still says
  "No place found"; and 100 random actions over the sheet (typing, removals,
  result taps, Enter, close and reopen) leave no console error, no stuck
  "Searching…", no duplicate row inside a section and no stale `data-go` /
  `data-rm` index.
- Left alone deliberately: the alias gaps — "usa", "us", "britain",
  "bangalore", "bombay" and "new delhi" (the list holds Delhi, and its Delhi
  entry sits on New Delhi's coordinates, so the app already treats the two as
  one place) — are entries in the data, not rules: adding aliases or a city
  would change which rows the sheet lists for queries that already work, so they
  are written down instead of shipped. Also left: `search()` prepends the
  bundled cities for a country query and filters them against the geocoder's
  rows by *name*, not by place, so a differently-named row for the same city can
  sit beside it; running `dedupe()` after that prepend would remove a row a
  reader can see, which wants its own measurement. And the `.rm` on a result row
  for a co-located city (searching "delhi" offers "Remove Delhi", which removes
  the saved "New Delhi") is the same data question, not a code one.

### Fixed — memory & lifecycle (2026-11-10, 16:00 IST pass)
- **Reduce motion stopped the rain but not the lightning.** The thunderstorm
  scene's flash is the one animation in the app that the stylesheet cannot
  reach: every other animation follows `prefers-reduced-motion` through a media
  query, and the particle field follows it through the `still` flag, but the
  flash is built in script with `Element.animate()`, and `lightning()` never
  looked at the setting. So a reader who had asked the system for no motion —
  and who, by the same setting, got no rain, no snow, no drifting parallax and
  no springs — still had the whole screen flash white every 2.5–7.5 seconds in
  a storm, and a timer waking the WebView to start each one. Measured in
  headless Chromium with the query emulated: **3 flashes in 14 s on 1.8.9,
  0 on this build**, while the same storm with the setting off flashes in both
  (2 and 4 in 14 s — the interval is random) and the frame loop is untouched
  (rAF callbacks 104 vs 102 in the same window). `lightning()` now returns
  after it has cleared its timer when the setting is on, and `onMotionChange()`
  calls it in both directions, so turning the setting off mid-storm starts the
  chain again (2 flashes in the 14 s after the switch) and turning it back on
  stops it (0 in the next 14 s). Nothing is drawn, worded or timed differently
  in a session that does not ask for reduced motion: `#main`'s markup and every
  computed style of the bar, hero, cards, nav, pill, photo layer, active scene
  and the `--k/--glass/--blur/--dp/--pr/--cc` variables are byte-identical to
  1.8.9 across four payloads (storm day, rain night, clear day, cloudy day).
- Version bumped to 1.8.10 (`versionCode 54`), same signing key, so it installs
  over 1.8.9; `android/assets/index.html` is byte-identical to `web/index.html`
  (SHA-256 `4f3e76fc…`), the APK rebuilt from it bundles that same page and
  carries `versionCode 54` / `versionName 1.8.10`, and `CHECKSUMS.txt` carries
  the new digest (`29fc7bc8…`).

### Notes
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked storage, forecast, Commons and geocoder
  responses reporting zero console messages and zero page errors; and the fix
  proved against 1.8.9 by counting `Element.animate()` calls in the same four
  scenarios above. The rest of the area was re-audited and found clean on this
  build: 180 random actions (tabs, sliders, sheet opens and closes, searches,
  saves, removals, unit toggles, Escape, resizes, visibility flips, reset)
  leave the listener count flat at 48, DOM nodes bounded at 231–297, one
  interval, at most four pending timers and the JS heap flat at about 1.3 MB;
  ten visibility flips leave exactly one frame request in flight and one
  lightning timer (no second loop); six `prefers-reduced-motion` flips leave
  the same; 20 no-op resize events reallocate the particle canvas zero times
  and one real geometry change reallocates it once; and the WebView shell still
  pauses, resumes, hands back a pending geolocation callback and detaches
  before destroying.
- Left alone deliberately: the three items 1.7.3 recorded — the 60-second
  refresh interval still ticking while the page is hidden (it returns
  immediately; every alternative weighed in 1.5.6), the `deviceorientation`
  listener staying subscribed while the parallax is halted by Reduce motion
  (two clamps and a no-op queue per event, and unsubscribing risks the tilt
  never coming back), and the photo layer building a fresh `Image` per render
  (0.035 ms on an already-decoded picture) — were re-measured here and are
  still not worth a change. Also left: the nine `.cloud` elements keep their
  CSS drift animation running while a clear sky holds them at `opacity: 0`, and
  the `#fx` canvas keeps its full backing store on scenes that seed no
  particles; pausing the first or releasing the second would move cloud phases
  and repaint the canvas, so both belong to a render-performance pass with its
  own measurements, not to this one.

### Fixed — geolocation edge cases (2026-11-10, 12:00 IST pass)
- **A fix that merged a duplicate city away left the app pointing at a
  different city than the one on screen.** When a location fix resolves to a
  place that is already in the saved list, `locate()` re-keys the pinned row and
  `dropTwin()` removes the saved copy. If that copy was the row on screen — a
  slow fix, or a permission dialog answered late, is exactly when the reader has
  already picked that city from the Cities sheet — `dropTwin()` spliced it out
  and left `cur` on whatever slid into its index. With a city still after it,
  the app then pointed at that other city while the screen still showed the
  located one, and the next repaint (the sheet's refresh button, the tab coming
  back after ten minutes) silently drew a city the reader never chose. `cur` now
  follows the row the copy was merged into, the way `fallbackPlace()` and
  `removeSaved()` already keep it on the same city. Nothing on screen changes:
  the two rows are the same place, so the repaint that follows is the located
  city that was already displayed.
- Version bumped to 1.8.9 (`versionCode 53`), same signing key, so it installs
  over 1.8.8; `CHECKSUMS.txt` carries the new digest.

### Fixed — build & release hygiene (2026-11-10, 10:00 IST pass)
- **`android/build.sh` failed with no output at all when the Android SDK was
  missing.** The two SDK probes (`BT=$(ls -d "$SDK"/build-tools/* | sort -V |
  tail -1)`) sat under `set -e -o pipefail`, and a missing directory makes `ls`
  exit 2 — so the script died inside the assignment, two lines before the
  "Android SDK not found" message it was written to print. The whole failure was
  `exit 2` with empty stdout *and* empty stderr, indistinguishable from a crash
  or a killed process; the previous two passes hit exactly this and could only
  report "build.sh exits 2 before its own diagnostic". Both probes now end in
  `|| true` — a failed probe is not an error, the `-z` test below it is — so the
  message prints (naming the path it looked in) and the build exits 1.
- **The version number was written twice and only one copy shipped.**
  `AndroidManifest.xml` declares `android:versionCode`/`android:versionName`, and
  `build.sh` passed its own hardcoded `--version-code 52 --version-name 1.8.8` to
  `aapt2 link`; aapt2's flags override the manifest, so the copy in the build
  script is the one that reached the APK. A pass that bumped the manifest alone
  built an APK still stamped with the old versionCode — and one that bumped only
  the script left the repo advertising a version the APK did not carry. The
  script now reads both values out of the manifest (and fails loudly if they are
  absent), so the two cannot disagree.
- **Nothing ever checked `CHECKSUMS.txt` against the APK it describes.** A
  rebuilt `LiquidWeather.apk` could be committed with the old digest left in
  place and the repo would go on publishing a checksum that fails for every
  downloader. The CI build job now verifies the digest before it builds
  anything.

### Notes
- No UI change of any kind: `web/index.html` is untouched (SHA-256 still
  `37a19636…`, byte-identical to `android/assets/index.html`), so there is no new
  APK, no version bump and no change to `CHECKSUMS.txt` on this pass.
- Verified: `bash -n android/build.sh`; the page's script still passes
  `node --check` and a headless Chromium load of `web/index.html` still produces
  zero console messages and zero page errors; and both fixes were proved with a
  stub SDK — HEAD's script exits 2 with 0 bytes on stdout and stderr where the
  fixed one prints its diagnostic and exits 1, and with the manifest bumped to
  `53`/`1.8.9` HEAD hands aapt2 `--version-code 52 --version-name 1.8.8` while
  the fixed script hands it `53`/`1.8.9`, and still passes `52`/`1.8.8` for the
  unchanged manifest. The new CI gate was run on the real tree (`OK`) and on a
  deliberately altered APK (`FAILED`, exit 1).
- Left alone deliberately: the shipped `LiquidWeather.apk` is still the 1.8.6
  build (`versionCode 50`, `d2ae1074…`) while the source is at 1.8.8 — this
  environment has no JDK or Android SDK, so nothing can be rebuilt or re-signed
  here. Also left: `build.sh` writes the APK to `android/build/` and nothing
  copies it to the repo root or rewrites `CHECKSUMS.txt`, which is how the two
  drifted apart; auto-publishing on every build is a behaviour change for the
  maintainer rather than a bug fix. And a CI gate on the committed APK's
  versionCode (to enforce "only ever increases") would need a hand-rolled parser
  for the APK's binary manifest, which is more risk than the defect it guards.

Ideas that would be welcome: a language switch, sleet/haze scenes,
a home-screen widget, and a "feels like" curve on the hourly strip.

## [1.9.1] — 2026-11-12

### Fixed
- **A refused location prompt put "New Delhi" in the saved list twice.** When
  the position request fails and the pinned "My Location" row has no fix,
  `fallbackPlace()` fills it with New Delhi — but not before looking for a saved
  New Delhi to merge it into, and that lookup compared ids with a string written
  out by hand, `'c28.6139,77.2090'` (four decimals). Every other place is keyed
  by `pid()` at three decimals (`'c28.614,77.209'`), so the only row it could
  ever recognise was one an earlier fallback had written itself: a New Delhi the
  reader had saved from search was not found, and refusing the prompt (or a
  device with no GPS, or the 15s watchdog) left "New Delhi" listed twice and cost
  one of the five slots. The fallback row is now keyed with `pid()` like every
  other place and the saved copy is looked up with `samePlace()`, the rule
  `addPlace()`, `row()` and `repairSaved()` have always used, so a row saved
  under either spelling — including an older build's four-decimal id — is merged
  instead of duplicated.
- **"Use my current location" in the city you had already saved left it in the
  list twice.** `dropTwin()` recognised the duplicate by id alone, and the keys
  are 3-decimal coordinates: the device's fix for Mumbai (19.0550, 72.8692) is
  2.4 km from the bundled Mumbai a reader saved (19.076, 72.8777), so the ids
  differed, nothing was merged, and the Cities sheet showed Mumbai twice with a
  fifth city refused — the same defect the search path had (1.6.x) but on the
  location path. The merge now uses `samePlace()` as well: an exact key still
  merges immediately, and the name-based half of the rule is applied once more
  when the geocoder has said which city the fix is in — on both the on-time and
  the late-name paths, since the row is still called "My Location" until then.

### Notes
- No visual change: for the same payload the rendered `#main` HTML is
  byte-identical to 1.9's in all ten scenarios below, including both fixed ones
  — the only other difference in saved state is the fallback row's id string,
  which is never displayed.
- Verified: `node --check` on the page's script; a DOM run of `web/index.html`
  with mocked storage, geolocation, forecast and geocoder responses reporting
  **zero console errors and zero page errors** in ten scenarios (denied, no
  geolocation API, NaN position, geocoder down, granted fix, fix on the exact
  saved key, fix 2.4 km from a saved city, fix 1200 km from a saved city,
  denial with New Delhi saved under each of the two id spellings). Targeted
  check, old page against new: with New Delhi saved from search and the prompt
  refused, 1.9 ends with two rows `c28.6139,77.2090 | c28.614,77.209` and 1.9.1
  with one (`c28.614,77.209`); with Mumbai saved and a fix 2.4 km away, 1.9 ends
  with `c19.055,72.869 | c19.076,72.878` and 1.9.1 with one row, still on
  screen. The late-name path was driven with a geocoder that answers after the
  2.5s budget: 1.9 ends with two Mumbai rows, 1.9.1 with one. Superseded
  requests, a slow fix and an open Cities sheet were re-run for console errors
  (none).
- Headless Chromium could not be used for the load check on this pass: the
  binary in this environment dies at startup with `SIGTRAP` (exit 133) even for
  `--version`, before it prints anything, so the DOM checks ran in jsdom with
  the same mocks (fetch, `navigator.geolocation`, canvas 2D) the earlier passes
  used in Chromium. That is a limitation of this sandbox, not of the page.
- `versionCode 61` / `versionName 1.9.1` in `android/AndroidManifest.xml` (up
  from 60 / 1.9), same signing key. The APK was rebuilt from this tree with
  `android/build.sh` (JDK 17, build-tools 34.0.0, platform 34); it bundles
  `assets/index.html` byte-identical to `web/index.html` (SHA-256
  `d3902694…`), carries `versionCode 61` / `versionName 1.9.1`, and
  `.github/scripts/verify_apk.py` agrees on all three. `CHECKSUMS.txt` carries
  the digest of the APK committed with this entry, and `apksigner
  verify --print-certs` still reports the project key (`2035d69f…`,
  `CN=Liquid Weather`). Nothing is released yet: the day's release is cut from
  the 22:00 IST pass, as usual.
- Left alone deliberately: a second `onGeolocationPermissionsShowPrompt` raised
  while the first is still pending still overwrites the stored callback (the
  page's 15s watchdog covers the request it abandons, as recorded in 1.4.5), and
  a pinned row's coordinates are still never refreshed after the first fix — the
  ten-minute auto-refresh re-fetches the forecast, not the position — because
  changing when a permission-gated call happens is a decision, not a bug fix.

## [1.9] — 2026-11-11

The day's release, cut from the 22:00 IST pass. It publishes the whole run of
fixes the programme made since 1.8 — 1.8.1 through 1.8.15 plus the 11 November
passes — as one version, which is what "a release a day, from the day's last
pass" is for: the published app is now the app in the repository.

### Fixed (carried in this release)
- **Focus survives a re-render, for every control.** The search sheet's repaints
  no longer drop focus to `<body>` (08:00 pass), and neither does a repaint of
  the forecast screen for the two controls that have no `id` — the hourly strip
  and the offline retry card (18:00 pass). A control is named by whatever still
  identifies it in the new markup, and if it is gone the new screen's first
  control takes the focus.
- **The search sheet's section labels are headings** (`role="heading"`,
  `aria-level="2"`), so a screen reader can jump between "Saved places",
  "Results" and "Popular".
- **A repaint no longer restarts the city-photo lookup** (20:00 pass): the
  lookup in flight is remembered by the city it belongs to, so a °C/°F toggle, a
  trip to the Cities tab or the ten-minute refresh no longer aborts it and asks
  Commons again — measured at 1 request instead of 1-then-2-then-3.
- Everything else since 1.8, in detail above: the reverse-geocode pair is
  cancelled with the request that owns it, the thunderstorm flash honours
  Reduce motion, `prunePhotos()` deletes the record it prunes, the geocoder's
  duplicate rows and the `<city>, <country>` label lookup are fixed, and the
  build refuses a stale `assets/index.html` or a version that disagrees with the
  manifest.

### Notes
- `versionCode 60` / `versionName 1.9` in `android/AndroidManifest.xml` (up from
  59 / 1.8.15), same signing key, so it installs over every 1.8 build.
- The APK was rebuilt from this tree with `android/build.sh` (JDK 17,
  build-tools 34.0.0, platform 34). It bundles `assets/index.html` byte-identical
  to `web/index.html` (SHA-256 `39fb9deb…`), carries `versionCode 60` /
  `versionName 1.9`, and `.github/scripts/verify_apk.py` agrees on all three.
  `CHECKSUMS.txt` carries its digest, `c36954f2c231e14d498b5c04cd5ab8971b8ebf56b35e87914d685f5de87448ea`,
  and `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`).
- The 22:00 pass itself found nothing shippable in its area (time & timezone),
  so the page in this release is the same page as 1.8.15; only the version
  metadata changed.
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder, Commons and image responses
  reporting zero console errors and zero page errors in three time-of-day
  states; `bash -n android/build.sh`; and the APK checks above.

## [1.10] — 2026-11-12

The day's release, cut from the 22:00 IST pass. It publishes everything the
programme fixed on 12 November — the 08:00, 10:00, 16:00 and 20:00 passes — as
one version, and rebuilds the APK so the published app is the app in the
repository (the 20:00 pass changed Java only, so the fix it shipped had not
reached the APK until now).

### Fixed (carried in this release)
- **Two location prompts open at once left the first one unanswered for good**
  (20:00 pass, `MainActivity`): the activity kept a single geolocation callback,
  so the later of two `getCurrentPosition()` calls overwrote the earlier one,
  which was never invoked — the page then gave up on its watchdog and turned
  the pinned row into a saved "New Delhi" while a fix was available. Every
  waiting prompt is now answered, oldest first, and a second prompt joins the
  permission request already out.
- **A fix that arrived inside the time the app had asked for was thrown away
  whenever the reader took a few seconds to answer the location prompt** (10:00
  pass): the watchdog counted from the call while the browser's own `timeout`
  only starts once a decision exists, so a prompt answered at 10s and a first
  fix at 18s arrived after the watchdog had given up — and giving up disables
  "My Location" for good. The watchdog now allows the pending prompt plus the
  browser's deadline.
- **A country query listed the same place twice, once under each of its two
  names** (16:00 pass): the bundled rows a country query adds were merged with
  the geocoder's answer by name alone, so "india" listed the bundled **Delhi**
  and Open-Meteo's **New Delhi** — the same point — as two rows with two delete
  controls for one saved place. They are now merged with the same
  `samePlace()`/`sameLabel()` rule every other pair of rows uses.
- **The install instructions told every downloader to expect an older build's
  checksum** (08:00 pass): `README.md` printed the 1.7 digest while
  `CHECKSUMS.txt`, the committed APK and every release since 1.8 carried
  another, so a reader who followed the instructions got "FAILED" on a good
  download. The README now prints the published digest, the version and size the
  docs advertise were brought up to date, and `.github/workflows/build.yml`
  checks the README's digest beside the two existing guards so it cannot drift
  again.
- The 22:00 pass itself found nothing shippable in its area (weather-code
  coverage), so the page in this release is the same page as 1.9.3; only the
  version metadata and the Java shell changed. See the entry above for what was
  audited and what was deliberately left alone.

### Notes
- `versionCode 64` / `versionName 1.10` in `android/AndroidManifest.xml` (up
  from 63 / 1.9.3), same signing key, so it installs over every 1.9 build.
- The APK was rebuilt from this tree with `android/build.sh` (JDK 17,
  build-tools 34.0.0, platform 34). It bundles `assets/index.html`
  byte-identical to `web/index.html` (SHA-256 `43d5df71…`), carries
  `versionCode 64` / `versionName 1.10`, and `.github/scripts/verify_apk.py`
  agrees on all three. `classes.dex` contains `answerGeo`, so the 20:00 Java
  fix is in the published app. `CHECKSUMS.txt` carries the new digest,
  `6b5a8e28928f340b4335e109eedcd5d7e796ef611ea3536839e1dce5568d8ba3` (101 KB),
  as does the `sha256sum` block in `README.md` (checked by `verify_docs.py`),
  and `apksigner verify --print-certs` still reports the project key
  (`2035d69f…`, `CN=Liquid Weather`).
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder and Commons responses
  reporting **zero console errors and zero page errors**; `python3
  .github/scripts/verify_apk.py .`, `python3 .github/scripts/verify_docs.py .`
  and `sha256sum -c` on the committed APK, all green; `apksigner verify
  --print-certs` on the committed APK.
## [1.11] — 2026-11-13

The day's release, cut from the 22:00 IST pass. It publishes everything the
programme fixed on 13 November — the 08:00, 12:00, 16:00 and 22:00 passes — as
one version, and rebuilds the APK so the published app is the app in the
repository.

### Fixed (carried in this release)
- **Every parallax frame recalculated the style of the whole document** (22:00
  pass, render performance): the depth engine wrote `--mx`/`--my` on
  `documentElement` once per frame, and because those are inherited custom
  properties each write invalidated every element in the document for two
  numbers only six selectors read. The five layers that are not the bar now
  carry their transform inline. One 40-move drag in headless Chromium goes from
  2 466 ms of style recalculation, 311 ms of paint, 1 171 ms of raster and
  1 233 ms of commit to 1 018 / 46 / 266 / 879 ms, and a 25-step scroll from
  747 ms of style and 46 ms of paint to 466 ms and 13 ms. The tab centres the
  drag caches were also re-measured on every 0.1 of parallax drift (8 forced
  document layouts per drag, against 1 with Parallax at 0); the ride is now
  applied to them as arithmetic. Pixel-identical: 0 differing pixels of
  6 192 000 across four parallax states.
- **A blank particle canvas kept 6.19 MB of pixels for the whole session**
  (12:00 pass): a clear, cloudy or foggy sky seeds no particles, yet the
  `#fx` backing store (860×1800 at DPR 2) stayed allocated, with its compositor
  texture, from launch to launch. The store is given back when a scene seeds
  nothing and taken again when one does. With Reduce motion on, the pixels go
  back too, instead of being held for a picture that cannot be drawn.
- **Nine blurred cloud layers and the sun kept animating while invisible**
  (12:00 pass): up to eight of the nine clouds sit at `opacity: 0` on a clear
  sky, and the sun is invisible in every rain, snow, fog and storm scene and all
  night. A hidden one is now paused after its 1.2 s fade, a shown one resumed at
  once.
- **A busy city-photo lookup was cached as "this city has no photo" for three
  weeks** (08:00 pass): MediaWiki reports a rate limit or internal error with
  HTTP 200 and an `error` object in the body, which the reader took for an empty
  result and stored as `{none:1}` for the whole 21-day `PHOTO_TTL`. It is now
  thrown, so the lookup is retried in five minutes and nothing is cached.
- **The ✕ that deletes a saved city was a control nested inside another
  control** (16:00 pass): each Cities row was a `<button>` with a
  `<span role="button">` inside it, which HTML forbids and assistive technology
  may flatten — the only way to remove a city could vanish from the
  accessibility tree. The row is a plain container with two sibling buttons now,
  and the row icons are `aria-hidden` so the spoken name matches the visible
  one. The hourly strip also carries `tabindex="0"`, so it can be scrolled
  without a pointer on WebViews that do not make scroll containers focusable.
- The 22:00 pass left the lens's `left`/`width` animation and the cards'
  3D-transform cost alone: both are what the frozen UI looks like.

### Notes
- `versionCode 69` / `versionName 1.11` in `android/AndroidManifest.xml` (up
  from 68 / 1.10.4), same signing key, so it installs over every 1.10 build.
- The APK was rebuilt from this tree with `android/build.sh` (JDK 17,
  build-tools 34.0.0, platform 34). It bundles `assets/index.html`
  byte-identical to `web/index.html` (SHA-256 `8a8b118c…`), carries
  `versionCode 69` / `versionName 1.11`, and `.github/scripts/verify_apk.py`
  agrees on all three. `CHECKSUMS.txt` carries the new digest,
  `397900bc27f5539aa664db1d60447fcd1cd4307a0d8cc8499b10f3d1bdcb3a01`
  (105 KB), as does the `sha256sum` block in `README.md` (checked by
  `verify_docs.py`), and `apksigner verify --print-certs` still reports the
  project key (`2035d69f…`, `CN=Liquid Weather`).
- Verified: `node --check` on the page's script; a headless Chromium load of
  `web/index.html` with mocked forecast, geocoder, Commons and image responses
  reporting **zero console messages and zero page errors**; the pixel and matrix
  comparisons recorded in the 22:00 entry; `python3
  .github/scripts/verify_apk.py .`, `python3 .github/scripts/verify_docs.py .`
  and `sha256sum -c` on the committed APK, all green.

## [1.0] — 2026-10-26

First public release.

### Added
- **Web app** (`web/index.html`, single file, no build step): live forecasts from
  Open-Meteo — current conditions, next 8 hours, full 7 days.
- **Location awareness** — asks once via `navigator.geolocation`, resolves the
  coordinates to a city name, falls back to a default city when denied.
- **Worldwide search** — any city or country by name, with a built-in list of
  ~140 cities used as an offline fallback and for country queries ("Japan" →
  Tokyo, Osaka, Sapporo).
- **Up to 5 saved places** in the bottom pill navigation, stored in local storage.
- **Real metrics** — UV index, wind and gusts, humidity with dew point,
  feels-like, visibility, pressure.
- **°C / °F toggle**, remembered between launches.
- **Animated scenes** driven by real WMO weather codes: drifting blurred clouds,
  sun and moon orbs, rain and snow particles, lightning flashes, and a separate
  darker palette for each condition at night.
- **Android APK** (`android/`) — a WebView shell that serves the HTML from an
  `https` origin, with runtime location permission handling.
- **Gradle-free build** (`android/build.sh`) using `aapt2`, `javac`, `d8`,
  `zipalign` and `apksigner`, plus a GitHub Actions workflow that builds the APK
  on every push and attaches it to tag releases.
- **Original design mockup** kept in `design/Liquid_Weather.html` for reference.

### Notes
- APK is self-signed; Android shows the "unknown developer" prompt on install.
- Verified signature schemes: v1, v2 and v3. `minSdk 23`, `targetSdk 34`.

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.10...HEAD
[1.10]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.10
[1.9.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.9.1
[1.9]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.9
[1.5.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.5.2
[1.5]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.5
[1.3.4]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.4
[1.3.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.2
[1.3.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.1
[1.3]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3
[1.2.4]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.4
[1.2.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.2
[1.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2
[1.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.1
[1.0]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.0

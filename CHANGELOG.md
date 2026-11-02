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

## [Unreleased]

Nothing yet. Ideas that would be welcome: a language switch, sleet/haze scenes,
a home-screen widget, and a "feels like" curve on the hourly strip.

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

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.3.4...HEAD
[1.3.4]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.4
[1.3.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.2
[1.3.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3.1
[1.3]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3
[1.2.4]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.4
[1.2.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.2
[1.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2
[1.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.1
[1.0]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.0

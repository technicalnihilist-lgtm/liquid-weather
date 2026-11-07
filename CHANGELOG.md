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

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.5.2...HEAD
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

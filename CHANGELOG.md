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

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.3...HEAD
[1.3]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.3
[1.2.4]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.4
[1.2.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2.2
[1.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2
[1.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.1
[1.0]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.0

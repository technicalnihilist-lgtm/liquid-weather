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

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.2...HEAD
[1.2]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.2
[1.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.1
[1.0]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.0

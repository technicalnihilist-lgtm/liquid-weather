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

[Unreleased]: https://github.com/technicalnihilist-lgtm/liquid-weather/compare/v1.1...HEAD
[1.1]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.1
[1.0]: https://github.com/technicalnihilist-lgtm/liquid-weather/releases/tag/v1.0

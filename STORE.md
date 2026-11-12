# Store listing

Copy-paste values for app stores that read a project from GitHub (Orion, F-Droid
submissions, Play Store console, etc.). Everything here matches the current
release, `v1.10`.

## Fields

| Field | Value |
|---|---|
| **Repo URL** | `https://github.com/technicalnihilist-lgtm/liquid-weather` |
| **Name** | Liquid Weather |
| **Category** | Weather — use *Utility* where a weather category isn't offered |
| **Author** | technicalnihilist-lgtm |
| **App ID / Package name** | `com.liquidweather.app` |
| **Icon URL** | `https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-weather/main/screenshots/icon.png` (512×512 PNG) |
| **Release keyword** | leave on *auto* — each release contains exactly one APK, `LiquidWeather.apk` |
| **Latest release** | `https://github.com/technicalnihilist-lgtm/liquid-weather/releases/latest` |
| **License** | MIT |
| **Min Android** | 6.0 (API 23), target SDK 34 |
| **APK size** | 101 KB |
| **Price** | Free, no ads, no in-app purchases, no account |

## Short description (under 160 characters)

> Live weather for any city on Earth, in a glassy animated interface. No ads, no account, no tracking. 101 KB.

## Full description

> **Liquid Weather — the weather, without the noise.**
>
> A glass-and-blur weather app with live forecasts for anywhere on the planet.
> Open it, allow location (or pick a city), and read the weather — nothing else
> is asked of you. No account, no ads, no analytics, no tracking, no Play
> Services.
>
> **What you get**
>
> • Live conditions, the next 8 hours and a full 7-day forecast
> • Location-aware — shows the weather where you are, by name
> • Search any city or country worldwide ("Srinagar", "Reykjavik", or "Japan"
>   for its main cities); a built-in list of ~140 cities keeps search working
>   even offline
> • Save up to 5 places and switch between them instantly
> • Real metrics: UV index, wind with gusts, humidity and dew point,
>   feels-like temperature, visibility, pressure
> • °C / °F toggle, remembered between launches
>
> **The look**
>
> Animated scenes follow the actual weather: drifting clouds, a sun or moon
> that tracks day and night, rain and snow particles, lightning flashes, and a
> separate darker palette for every condition after dark. The whole interface
> sits on several depth layers that follow your tilt, your finger and your
> scrolling — tune that with the **Depth** and **Parallax** sliders, and adjust
> the glass with the **Transparency**, **Blur** and **Bounce** sliders.
>
> **Privacy**
>
> Your location never leaves the device as anything but a latitude/longitude
> pair in the weather request. Saved places stay in local storage on the phone.
> The only network calls in the source are to Open-Meteo (forecasts and city
> search) and OpenStreetMap/BigDataCloud (turning coordinates into a place
> name). You can read every line: the entire app is MIT licensed and lives in
> this repository.
>
> **Small on purpose**
>
> The APK is 101 KB, has no dependencies, no ad SDKs and no background services.
> The same file runs in any browser from `web/index.html`.

## Screenshot URLs (direct links, 4 available — stores usually ask for 3)

1. `https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-weather/main/screenshots/home.png` — clear night, current conditions
2. `https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-weather/main/screenshots/rain.png` — rainy afternoon scene
3. `https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-weather/main/screenshots/search.png` — searching any city or country
4. `https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-weather/main/screenshots/settings.png` — glass, depth and parallax settings

All four are 860×1800 PNG (a 430×900 layout at 2× density).

## What a reviewer should check

- **No network tracking:** grep the source for `http` — the only endpoints are
  `api.open-meteo.com`, `geocoding-api.open-meteo.com`, `api.bigdatacloud.net`,
  `nominatim.openstreetmap.org`, `commons.wikimedia.org` (photo lookup by city
  name) and `upload.wikimedia.org` (the photos themselves). Only freely licensed
  Commons files are used and each is credited by author and licence in
  *Glass & motion → Photos*.
- **No ads or accounts:** there is no ad SDK, no login, no analytics, no
  crash reporter, and no `INTERNET`-using service other than the weather APIs.
- **Permissions:** `INTERNET`, `ACCESS_COARSE_LOCATION`, `ACCESS_FINE_LOCATION`
  — location is optional; denying it still leaves a fully working app.
- **Build:** `android/build.sh` produces the APK from the committed sources with
  `aapt2`, `javac`, `d8` and `apksigner`; CI runs the same script on every push.

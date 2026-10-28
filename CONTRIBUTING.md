# Contributing to Liquid Weather

Thanks for wanting to help. This is a small, deliberately simple project — one HTML file and a thin Android shell — so most changes are easy to reason about.

## The one hard rule

Liquid Weather is **ad-free, account-free and tracker-free**. That is the whole point of the app, not a preference. Pull requests that add advertising, analytics, telemetry, crash reporting SDKs, login/accounts, or any third-party tracking will be closed. Dependencies that phone home are treated the same way.

Also please don't add a build system that requires Android Studio or Gradle: the whole APK is built with `aapt2` + `javac` + `d8` + `apksigner` in one script, on purpose.

## Ways to help

- **Bug reports** — open an issue with your Android version, phone model, and what you expected vs. what happened. A screenshot helps a lot.
- **Translations / wording** — the UI text is all in `web/index.html`; a language switch would be a welcome addition.
- **New scenes** — the weather scenes live in the `SCENES` object. If you want to add something (sleet, haze, a proper sunrise palette), match the existing palette and keep it cheap on the GPU.
- **Docs** — if something in the README confused you, fix it.

## Running it locally

The web app needs no build step:

```bash
python3 -m http.server 8000     # from the repo root
# then open http://localhost:8000/web/
```

Serve it over `http://` or `https://` — browsers block geolocation for pages opened straight from disk, and the app falls back to a default city in that case.

## Building the APK

You need JDK 17 and the Android SDK (platform `android-34`, build-tools `34.0.0`):

```bash
export ANDROID_SDK_ROOT=/path/to/android-sdk
cd android
./build.sh
```

That produces `android/build/LiquidWeather.apk`, signed with `android/release.keystore`. The same script runs in CI (`.github/workflows/build.yml`) on every push, so a PR that breaks the build will show up red.

## Making changes

1. Fork, then branch: `git checkout -b fix/night-scene-contrast`.
2. Keep the diff focused — one change per PR.
3. If you touch the UI, include a screenshot in the PR description (light and night scenes if relevant).
4. If you touch the app in `web/index.html`, copy it into the APK too:
   ```bash
   cp web/index.html android/assets/index.html
   ```
   The two files are meant to stay identical.
5. Rebuild the APK and confirm it still installs and runs.

## Code style

- Plain ES2017 JavaScript, no frameworks, no bundler. The file must stay readable and openable in a text editor.
- CSS keeps the existing custom-property/glass conventions.
- Java stays minimal — the shell should do as little as possible.
- Prefer clear names over comments; comment only where the reason isn't obvious.

## Commits and PRs

- Commit messages: a short imperative subject line, then a body explaining *why* if it isn't obvious.
- No need to squash or sign commits.
- By contributing you agree your work is released under the project's [MIT license](LICENSE).

## Where things came from

The visual design started as a static mockup, kept unmodified in [`design/Liquid_Weather.html`](design/Liquid_Weather.html). The working app is `web/index.html`. If you're changing the look, check both — the mockup is the reference for the intended design.

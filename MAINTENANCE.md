# Maintenance programme — 1 to 20 November 2026

Ten scheduled passes a day, every day, for twenty days. The goal is **no new
features and no visual change** — the app should look and behave exactly as it
does today, only faster, steadier and less likely to break.

## The hard rules

1. **The UI is frozen.** No changes to layout, spacing, typography, colours,
   gradients, glass values, icon choices, wording of visible labels, animation
   timings or the settings panel's appearance. If a fix would visibly change
   anything, it doesn't ship — it gets written down instead.
2. **Only four kinds of change are allowed:** a bug fix, a crash/hang fix, a
   performance or memory improvement, or a correctness fix (wrong data shown,
   wrong time, wrong units, wrong city). Anything else waits.
3. **Every change is verified before it is committed:** `node --check` on the
   script, a headless Chromium load with no console errors, and — if
   `web/index.html` changed — a fresh APK build so the bundled copy stays
   identical to the source.
4. **No noise.** If a pass finds nothing real, it reports "clean" and commits
   nothing. Inventing churn to hit a number defeats the point.
5. **Never break installs.** `versionCode` only ever increases; the signing key
   never changes; `CHECKSUMS.txt` always matches the published APK.

## The rotation

Each pass takes one area from this list, in order, and goes deep on it rather
than wide. A pass that finds several problems in its area may fix them all, but
only within that area.

| # | Area | What "better" means here |
|---|---|---|
| 1 | Network & API robustness | timeouts, retries, partial payloads, HTTP errors, rate limits, slow networks, `AbortController` leaks |
| 2 | Geolocation edge cases | denied, blocked, timeout, stale fix, re-prompting, reverse-geocode failures, no-GPS devices |
| 3 | Time & timezone correctness | DST, hour indexing across midnight, day labels, "Today" boundaries, device clock skew |
| 4 | Weather-code coverage | all 28 WMO codes, unknown/future codes, day/night icon mapping, scene fallbacks |
| 5 | Render performance | forced reflows, layout thrash, paint cost of blur, canvas DPR handling, rAF budget |
| 6 | Memory & lifecycle | listener/interval leaks, canvas resizes, visibility changes, WebView teardown |
| 7 | Storage robustness | quota exceeded, corrupt JSON, missing keys, settings migration, multi-tab writes |
| 8 | Search & geocoding | dedupe, diacritics, partial words, offline list accuracy, empty/odd queries |
| 9 | Accessibility & semantics | aria-live regions, focus order, screen-reader labels, text contrast over every scene |
| 10 | Build & release hygiene | version monotonicity, checksums, APK/source parity, CI reliability |

After the tenth pass the rotation starts again, so day 1 and day 11 cover the
same area — the second visit is expected to find the leftovers from the first.

## Per-pass checklist

- [ ] Pull `main`, confirm the working tree is clean.
- [ ] Read the area's code path end to end (HTML/CSS/JS, and the Java shell if relevant).
- [ ] List candidate problems; pick the ones that are demonstrably real.
- [ ] Fix, then verify: syntax, headless run, and a targeted check that proves the fix.
- [ ] If `web/index.html` changed: copy to `android/assets/index.html`, bump
      `versionCode`/`versionName`, rebuild, confirm the APK's bundled HTML
      matches the source and the signature still verifies.
- [ ] Update `CHECKSUMS.txt` and `CHANGELOG.md` ("Unreleased" → dated entry).
- [ ] Commit with a message that says what was wrong and why the change fixes it.
- [ ] Report: area, what was found, what changed, what was deliberately left alone.

## Releases

A release is cut **once a day**, from the day's last pass, so the repo doesn't
fill with two hundred releases. The daily version bumps the minor number
(1.3, 1.4, … 1.22) and carries the day's fixes in its notes. The published APK
is always the maintainer build, and `CHECKSUMS.txt` is updated with it.

## Stopping

The programme ends after the pass on **20 November 2026**. The scheduled job
deletes itself then, and the repo keeps the full history of what was fixed.

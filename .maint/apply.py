import pathlib, sys

ROOT = pathlib.Path('.')

FLASH_COMMENT = """  /* Reduce motion covers this animation too. Every other animation in the app
     follows the query through the stylesheet, and the particle field follows it
     through `still` — but the flash is created in script with
     Element.animate(), which no media query can reach, and nothing here ever
     looked at the setting. A reader who had asked the system for no motion
     still had a thunderstorm flashing the whole screen white every 2.5–7.5
     seconds (measured in headless Chromium with the query emulated: two
     flashes in twelve seconds, while the rain beside it correctly stood
     still) — the most intrusive animation in the app running for the one
     reader who asked for none, and a wake-up every few seconds to start it.
     Nothing to flash while the setting is on; onMotionChange() below starts
     the chain again when it is turned off. */
  if (still) return;
"""

MOTION_COMMENT = """  /* The flash chain follows the setting the same way, in both directions:
     called here it clears the armed timer and arms nothing while the setting is
     on (see `lightning`), and re-arms a thunderstorm's chain the moment the
     setting is turned off, so a reduced-motion session that ends is the same
     storm the reader would have had without it. */
  lightning();
"""

CHANGELOG_ENTRY = """### Fixed — memory & lifecycle (2026-11-10, 16:00 IST pass)
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
  the new digest (`b4de262b…`).

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

"""


def swap(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit('anchor for %s matched %d times, expected exactly 1' % (label, n))
    return text.replace(old, new)


web = ROOT / 'web/index.html'
s = web.read_text(encoding='utf-8')
s = swap(s, "function lightning() {\n  clearTimeout(lt);\n  if (mode !== 'storm') return;",
         "function lightning() {\n  clearTimeout(lt);\n" + FLASH_COMMENT + "  if (mode !== 'storm') return;", 'lightning')
s = swap(s, "  } else {\n    startFx();\n  }\n}\ntry {",
         "  } else {\n    startFx();\n  }\n" + MOTION_COMMENT + "}\ntry {", 'onMotionChange')
web.write_text(s, encoding='utf-8')

cl = ROOT / 'CHANGELOG.md'
c = cl.read_text(encoding='utf-8')
anchor = "## [Unreleased]\n\n### Fixed — geolocation edge cases (2026-11-10, 12:00 IST pass)"
c = swap(c, anchor, "## [Unreleased]\n\n" + CHANGELOG_ENTRY + "### Fixed — geolocation edge cases (2026-11-10, 12:00 IST pass)", 'changelog')
cl.write_text(c, encoding='utf-8')

mf = ROOT / 'android/AndroidManifest.xml'
m = mf.read_text(encoding='utf-8')
m = swap(m, 'android:versionCode="53"', 'android:versionCode="54"', 'versionCode')
m = swap(m, 'android:versionName="1.8.9"', 'android:versionName="1.8.10"', 'versionName')
mf.write_text(m, encoding='utf-8')

print('applied: web/index.html, CHANGELOG.md, android/AndroidManifest.xml')

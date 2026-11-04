#!/usr/bin/env python3
"""One-off source edits for the 2026-11-04 14:00 IST maintenance pass (area 8:
search & geocoding). Every replacement is exact and asserted, so the job fails
loudly instead of committing a half-applied tree."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def edit(path, pairs):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    for old, new in pairs:
        if s.count(old) == 1:
            s = s.replace(old, new)
        elif new in s:          # already applied (idempotent re-run)
            continue
        else:
            sys.exit(f'{path}: expected exactly one match for: {old[:60]!r} (found {s.count(old)})')
    p.write_text(s, encoding='utf-8')


# --- 1. the city-name button was dead on the skeleton and offline screens -----
edit('web/index.html', [
    ("""  bindUnit();
  $('#main .page').classList.add('enter'); prepEnter();""",
     """  bindUnit();
  /* the city name is the app's "change city" control in every other state; in
     the skeleton it was never wired, so it did nothing while a forecast was
     being fetched */
  const openBtn = $('#openSearch');
  if (openBtn) openBtn.onclick = openSheet;
  $('#main .page').classList.add('enter'); prepEnter();"""),
    ("""  bindUnit();
  /* the retry card is the only way back online""",
     """  bindUnit();
  /* same control as on the forecast screen: without this the offline screen's
     city name was dead, so a user with no connection could not search for
     another city from it (only the Cities tab still worked) */
  const openBtn = $('#openSearch');
  if (openBtn) openBtn.onclick = openSheet;
  /* the retry card is the only way back online"""),
])

# --- 2. a search in flight when the sheet closed still painted ---------------
edit('web/index.html', [
    ("""const sheet = $('#sheet'), qEl = $('#q'), listEl = $('#shList');
let stT;""",
     """const sheet = $('#sheet'), qEl = $('#q'), listEl = $('#shList');
let stT, qTimer, qSeq = 0;      // qSeq: every keystroke, open and close invalidates older searches"""),
    ("""  if (mEl) mEl.setAttribute('inert', '');
  qEl.value = '';
  paintSheet('');""",
     """  if (mEl) mEl.setAttribute('inert', '');
  qSeq++;                     // a search started before the sheet opened must not paint into it
  qEl.value = '';
  paintSheet('');"""),
    ("""  clearTimeout(qTimer);        // a pending debounce would fire a search into a closed sheet""",
     """  clearTimeout(qTimer);        // a pending debounce would fire a search into a closed sheet
  qSeq++;                      // and a request already in flight must not repaint the sheet later"""),
    ("""let qTimer, qSeq = 0;

/* A geocoder can answer 200 with a row""",
     """/* A geocoder can answer 200 with a row"""),
])

# --- 3. country search listed the same city twice ---------------------------
edit('web/index.html', [
    ("""    const names = new Set(list.map(o => o.name.toLowerCase()));
    list = [...byCountry.filter(o => !names.has(o.name.toLowerCase())), ...list];""",
     """    /* compared folded, not lowercased: the geocoder answers "İstanbul" (capital
       dotted İ) for a country query, and lowercasing that gives "i̇stanbul" —
       with a combining dot — so it never matched the bundled "Istanbul" and the
       sheet listed the same city twice. */
    const names = new Set(list.map(o => fold(o.name)));
    list = [...byCountry.filter(o => !names.has(fold(o.name))), ...list];"""),
])

# --- 4. android shell: bundled copy, version bump ---------------------------
(ROOT / 'android/assets/index.html').write_bytes((ROOT / 'web/index.html').read_bytes())

edit('android/AndroidManifest.xml', [
    ('android:versionCode="22"', 'android:versionCode="23"'),
    ('android:versionName="1.4.3"', 'android:versionName="1.4.4"'),
])

edit('android/build.sh', [
    ('--version-code 22 --version-name 1.4.3', '--version-code 23 --version-name 1.4.4'),
])

# --- 5. changelog entry ------------------------------------------------------
entry = (ROOT / '.github/maintenance/changelog_entry.md').read_text(encoding='utf-8')
cp = ROOT / 'CHANGELOG.md'
cs = cp.read_text(encoding='utf-8')
if '## [1.4.4] — 2026-11-04' not in cs:
    if cs.count('## [Unreleased]') != 1:
        sys.exit('CHANGELOG.md: expected exactly one "## [Unreleased]" heading')
    cp.write_text(cs.replace('## [Unreleased]', entry + '## [Unreleased]', 1), encoding='utf-8')

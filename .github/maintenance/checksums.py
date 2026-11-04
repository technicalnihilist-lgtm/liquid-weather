#!/usr/bin/env python3
"""Point CHECKSUMS.txt at the APK that was just built."""
import hashlib, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
digest = hashlib.sha256((root / 'LiquidWeather.apk').read_bytes()).hexdigest()
p = root / 'CHECKSUMS.txt'
s = p.read_text(encoding='utf-8')
s2, n = re.subn(r'^[0-9a-f]{64}  LiquidWeather\.apk$', f'{digest}  LiquidWeather.apk', s, flags=re.M)
if n != 1:
    sys.exit(f'CHECKSUMS.txt: expected one digest line, found {n}')
p.write_text(s2, encoding='utf-8')
print('CHECKSUMS.txt ->', digest)

import pathlib, sys

p = pathlib.Path('CHANGELOG.md')
s = p.read_text(encoding='utf-8')
old = 'the new digest (`b4de262b…`)'
new = 'the new digest (`29fc7bc8…`)'
if old not in s:
    sys.exit('digest anchor not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('digest recorded')

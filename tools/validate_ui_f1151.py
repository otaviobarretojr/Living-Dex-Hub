#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'app/src/main/assets/ui-stability-f1151.js').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/ui-stability-f1151.css').read_text(encoding='utf-8')
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f11.5.1'" in js
for marker in ['persistentThirdDock:true','legacyDockClassPreserved:true','androidSafeHeader:true','compactBoxAction:true','detailSourceReadable:true','mutationRecovery:true']:
    assert marker in js, marker
assert 'repeat(3,minmax(0,1fr))' in js
assert "b.className='ld79-extra'" in js
assert 'ui-stability-f1151.js' in loader and 'ui-stability-f1151.css' in loader
assert 'calc(14px + env(safe-area-inset-top))' in css
assert 'width:88px!important' in css
assert 'max-width:48%!important' in css
print('UI F11.5.1 VALIDATION: PASS • persistent Living Dex dock • Android safe header • compact Box action • readable detail source')

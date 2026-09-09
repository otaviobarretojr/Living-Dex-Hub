#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'app/src/main/assets/livingdex-global-v8.js').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/livingdex-global-v8.css').read_text(encoding='utf-8')
assert "version:'8.0-f11.2'" in js
assert "data-ld79='livingdex'" in js or 'data-ld79="livingdex"' in js or "b.dataset.ld79='livingdex'" in js
assert 'Living Dex</span>' in js
assert "grid-template-columns','repeat(3,minmax(0,1fr))'" in js
assert 'data-ld-action="next-missing"' in js
assert 'data-ld-action="refresh"' in js
assert 'filterCounters:true' in js
assert 'quickNextMissing:true' in js
assert 'availabilityRefresh:true' in js
assert 'mobileFirstRework:true' in js
assert 'compactSummary:true' in js
assert 'bottomDockLivingDex:true' in js
assert 'position:sticky' in css
assert '.ld8ld-progressbar' in css
assert '.ld8ld-filter-row button b' in css
assert '@media(max-width:520px)' in css
assert 'repeat(3,minmax(0,1fr))' in css
print('LIVING DEX F11.2 VALIDATION: PASS • bottom dock=3 items • mobile-first • counters • quick actions • sticky filters')

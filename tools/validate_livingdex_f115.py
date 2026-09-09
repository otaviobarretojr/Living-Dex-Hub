#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'app/src/main/assets/livingdex-experience-v8.js').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/livingdex-experience-v8.css').read_text(encoding='utf-8')
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f11.5'" in js
for marker in ['f114VisualRework:true','f115PokemonDetail:true','statusLegend:true','generationBadges:true','searchClear:true','routeSnapshot:true','recommendedGameVisible:true','recommendedActionVisible:true','recommendedLocationVisible:true','nonDestructiveOverlay:true']:
 assert marker in js, marker
for marker in ['ld8ld-status-legend','ld8ld-gen-badge','ld8ld-detail-summary','ld8ld-route-snapshot','MELHOR OPÇÃO NOS SEUS JOGOS']:
 assert marker in (js + css + (ROOT/'app/src/main/assets/livingdex-encounter-guide-v8.js').read_text(encoding='utf-8')), marker
assert "style('livingdex-experience-v8.css','livingdex-experience')" in loader
assert "script('livingdex-experience-v8.js','livingdex-experience')" in loader
assert '@media(max-width:520px)' in css
print('LIVING DEX F11.5 VALIDATION: PASS • F11.4 visual polish • F11.5 acquisition detail • non-destructive overlay')

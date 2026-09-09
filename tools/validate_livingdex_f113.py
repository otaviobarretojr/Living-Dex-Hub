#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'app/src/main/assets/livingdex-encounter-guide-v8.js').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/livingdex-encounters-v8.css').read_text(encoding='utf-8')
assert "version:'8.0-f11.3'" in js
for marker in ['multiOwnedGameRanking:true','bestGameResolver:true','bestRouteResolver:true','collectionAwareRanking:true','selectedVersionPriority:true','otherOwnedGamesVisible:true','alternativesCollapsed:true','data-ld8ld-game','MELHOR OPÇÃO NOS SEUS JOGOS','ROTA RECOMENDADA']:
 assert marker in js, marker
assert 'providerCandidates(id)' in js
assert 'rankedCandidates(id)' in js
assert '.ld8ld-smart-head' in css
assert '.ld8ld-other-games' in css
assert '.ld8ld-best-route' in css
print('LIVING DEX F11.3 VALIDATION: PASS • best owned game • best route • version + collection aware • alternate owned games')

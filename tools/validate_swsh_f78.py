#!/usr/bin/env python3
"""Structural validation for Sword/Shield F7.8 DLC encounter ingestion."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
text=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('F7.8 validation: DATA payload not found')
data=json.loads(m.group(1))
assert data.get('version')=='8.0-f7.8',data.get('version')
assert data.get('gameId')=='swsh'
dexes=data.get('dexes') or {}
expected={'galar':400,'isle-of-armor':211,'crown-tundra':210}
for scope,n in expected.items():
    d=dexes.get(scope) or {}
    assert d.get('dexSpecies')==n,(scope,d)
    assert 0<=int(d.get('coveredSpecies',-1))<=n,(scope,d)
assert (dexes.get('galar') or {}).get('coveredSpecies')==400,dexes.get('galar')
assert (dexes.get('galar') or {}).get('missingSpecies')==[],dexes.get('galar')
assert data.get('uniqueSwordShieldSpecies')==584,data.get('uniqueSwordShieldSpecies')
covered=int(data.get('coveredSpecies',0));assert covered>508,covered
outside=data.get('obtainableOutsideDexSpecies') or [];assert int(data.get('obtainableOutsideDexCount',0))==len(outside)==48
assert int(data.get('totalObtainableSpecies',0))==covered+48
added=int(data.get('dlcEncounterSpeciesAddedCount',0));routes=int(data.get('dlcEncounterRoutesAdded',0));assert added>0 and routes>=added
assert int(data.get('regionalFormRoutes',0))==6
assert 'dlcVersionSlugIngestion:true' in text and 'regionalFormAware:true' in text and 'outsideDexObtainability:true' in text
guide=(ROOT/'app/src/main/assets/livingdex-encounter-guide-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f11.3'" in guide
assert 'multiOwnedGameRanking:true' in guide
assert 'bestGameResolver:true' in guide
assert 'selectedVersionPriority:true' in guide
print('SWSH F7.8 VALIDATION: PASS • '+', '.join(f"{s}={dexes[s]['coveredSpecies']}/{dexes[s]['dexSpecies']}" for s in expected)+f" • tracked={covered}/584 • dlc_added={added} • routes_added={routes} • outside=48 • total_obtainable={data['totalObtainableSpecies']}")

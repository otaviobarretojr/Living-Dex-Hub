#!/usr/bin/env python3
"""Structural validation for Sword/Shield F7.7 regional-form routes."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
text=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('F7.7 validation: DATA payload not found')
data=json.loads(m.group(1))
assert data.get('version')=='8.0-f7.7',data.get('version')
assert data.get('gameId')=='swsh'
dexes=data.get('dexes') or {}
expected={'galar':400,'isle-of-armor':211,'crown-tundra':210}
for scope,n in expected.items():
    d=dexes.get(scope) or {}
    assert d.get('dexSpecies')==n,(scope,d)
assert (dexes.get('galar') or {}).get('coveredSpecies')==400,dexes.get('galar')
assert (dexes.get('galar') or {}).get('missingSpecies')==[],dexes.get('galar')
assert data.get('uniqueSwordShieldSpecies')==584,data.get('uniqueSwordShieldSpecies')
assert int(data.get('coveredSpecies',0))==508,data.get('coveredSpecies')
outside=data.get('obtainableOutsideDexSpecies') or []
assert int(data.get('obtainableOutsideDexCount',0))==len(outside)==48,data.get('obtainableOutsideDexCount')
assert int(data.get('totalObtainableSpecies',0))==508+len(outside),data.get('totalObtainableSpecies')
assert int(data.get('regionalFormRoutes',0))==6,data.get('regionalFormRoutes')
regional=set(data.get('regionalFormSpecies') or [])
assert regional=={77,83,222,263,554,618},regional
pokemon=data.get('pokemon') or {}
for pid in regional:
    p=pokemon.get(str(pid)) or {}
    assert p.get('regionalForm')=='galarian',(pid,p)
    routes=p.get('encounters') or []
    assert any(r.get('regionalForm')=='galarian' for r in routes),(pid,routes)
assert 'regionalFormAware:true' in text
assert 'galarDexRegionalFormsComplete:true' in text
bridge=(ROOT/'app/src/main/assets/acquisition-availability-bridge-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f7.6'" in bridge
scope=(ROOT/'app/src/main/assets/swsh-dex-scope-ui-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f7.6'" in scope
print('SWSH F7.7 VALIDATION: PASS • galar=400/400 • tracked=508/584 • outside=48 • total_obtainable='+str(data['totalObtainableSpecies'])+' • regional_forms=6')

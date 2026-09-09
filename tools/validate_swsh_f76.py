#!/usr/bin/env python3
"""Structural validation for Sword/Shield F7.6 obtainability outside tracked dexes."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
text=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('F7.6 validation: DATA payload not found')
data=json.loads(m.group(1))
assert data.get('version')=='8.0-f7.6',data.get('version')
assert data.get('gameId')=='swsh'
dexes=data.get('dexes') or {}
expected={'galar':400,'isle-of-armor':211,'crown-tundra':210}
for scope,n in expected.items():
    d=dexes.get(scope) or {}
    assert d.get('dexSpecies')==n,(scope,d)
assert data.get('uniqueSwordShieldSpecies')==584,data.get('uniqueSwordShieldSpecies')
assert int(data.get('coveredSpecies',0))==502,data.get('coveredSpecies')
outside=data.get('obtainableOutsideDexSpecies') or []
assert int(data.get('obtainableOutsideDexCount',0))==len(outside)>0
assert int(data.get('totalObtainableSpecies',0))==502+len(outside)
pokemon=data.get('pokemon') or {}
# Keldeo and representative Dynamax Adventures species must exist without dex membership.
for pid in (647,150,243,384):
    p=pokemon.get(str(pid)) or {}
    assert p.get('obtainableOutsideDex') is True,(pid,p)
    assert p.get('dexScopes')==[],(pid,p.get('dexScopes'))
    assert p.get('encounters'),pid
assert 'outsideDexObtainability:true' in text
assert 'dexMembershipSeparatedFromObtainability:true' in text
bridge=(ROOT/'app/src/main/assets/acquisition-availability-bridge-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f7.6'" in bridge
assert 'outsideDexVisibleToLivingDex:true' in bridge
scope=(ROOT/'app/src/main/assets/swsh-dex-scope-ui-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f7.6'" in scope
assert 'Obtível no jogo · Fora da Pokédex' in scope
print(f"SWSH F7.6 VALIDATION: PASS • tracked=502/584 • outside={len(outside)} • total_obtainable={data['totalObtainableSpecies']}")

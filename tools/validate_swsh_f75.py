#!/usr/bin/env python3
"""Structural validation for the generated Sword/Shield F7.5 acquisition payload."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
text=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('F7.5 validation: DATA payload not found')
data=json.loads(m.group(1))
assert data.get('version')=='8.0-f7.5',data.get('version')
assert data.get('gameId')=='swsh'
dexes=data.get('dexes') or {}
expected={'galar':400,'isle-of-armor':211,'crown-tundra':210}
for scope,n in expected.items():
    d=dexes.get(scope) or {}
    assert d.get('dexSpecies')==n,(scope,d)
    assert 0<=int(d.get('coveredSpecies',-1))<=n
assert data.get('uniqueSwordShieldSpecies')==584,data.get('uniqueSwordShieldSpecies')
assert int(data.get('coveredSpecies',0))>=502,data.get('coveredSpecies')
assert int(data.get('verifiedDlcSpecialRoutes',0))>=17,data.get('verifiedDlcSpecialRoutes')
assert int(data.get('dynamaxAdventureRoutes',0))>=3,data.get('dynamaxAdventureRoutes')
pokemon=data.get('pokemon') or {}
# Validate only species that are actual entries in one of the three tracked dexes.
# Keldeo and many Dynamax Adventure bosses are obtainable in Crown Tundra but are
# intentionally outside these dex denominators and belong to the next extra-catalog phase.
required={
    891:'Master Dojo',       # Kubfu — Isle of Armor dex
    893:'Evento / Pokémon HOME', # Zarude — Isle of Armor dex
    894:'Split-Decision Ruins',   # Regieleki — Crown Tundra dex
    898:'Crown Shrine',      # Calyrex — Crown Tundra dex
    144:'The Crown Tundra',  # Galarian Articuno — Crown Tundra dex
}
for pid,needle in required.items():
    routes=(pokemon.get(str(pid)) or {}).get('encounters') or []
    assert any(needle in str(r.get('location','')) for r in routes),(pid,needle)
assert 'verifiedDlcSpecialAcquisition:true' in text
assert 'dynamaxAdventures:true' in text
print('SWSH F7.5 VALIDATION: PASS • '+', '.join(f"{s}={dexes[s]['coveredSpecies']}/{dexes[s]['dexSpecies']}" for s in expected)+f" • union={data['coveredSpecies']}/584 • special={data['verifiedDlcSpecialRoutes']} • dynamax={data['dynamaxAdventureRoutes']}")

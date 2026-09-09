#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/sv-encounters-v8.js'
s=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',s,re.S)
assert m,'SV DATA payload missing'
d=json.loads(m.group(1))
assert d['version']=='8.0-f10.0'
assert d['gameId']=='sv'
assert d['dexes']['paldea']['size']==400
assert d['dexes']['kitakami']['size']==200
assert d['dexes']['blueberry']['size']==243
assert d['uniqueTrackedSpecies']>400
assert d['coveredSpecies']>0
assert d['pkhexLegalityImport'] is True
assert d['threeDexScopes'] is True
assert '906' in d['pokemon'] and '909' in d['pokemon'] and '912' in d['pokemon']
print(f"SV F10.0 VALIDATION: PASS • paldea={d['dexes']['paldea']['covered']}/400 • kitakami={d['dexes']['kitakami']['covered']}/200 • blueberry={d['dexes']['blueberry']['covered']}/243 • tracked={d['coveredSpecies']}/{d['uniqueTrackedSpecies']} • missing={len(d['missingSpecies'])}")

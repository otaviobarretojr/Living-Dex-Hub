#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/sv-encounters-v8.js'
s=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',s,re.S)
assert m,'SV DATA payload missing'
d=json.loads(m.group(1))
assert d['version']=='8.0-f10.1'
assert d['gameId']=='sv'
assert d['dexes']['paldea']['size']==400 and d['dexes']['paldea']['covered']==400
assert d['dexes']['kitakami']['size']==200 and d['dexes']['kitakami']['covered']==200
assert d['dexes']['blueberry']['size']==243 and d['dexes']['blueberry']['covered']==243
assert d['uniqueTrackedSpecies']==664
assert d['coveredSpecies']==664
assert d['missingSpecies']==[]
assert d['pkhexLegalityImport'] is True
assert d['threeDexScopes'] is True
assert d['eventAvailabilityAware'] is True
assert d['versionExclusiveDlcParadox'] is True
for sid in ('442','999','1007','1008','1009','1010','1020','1021','1022','1023','1024','1025'):
 assert sid in d['pokemon'] and d['pokemon'][sid].get('encounters'),sid
print('SV F10.1 VALIDATION: PASS • paldea=400/400 • kitakami=200/200 • blueberry=243/243 • tracked=664/664 • missing=0')

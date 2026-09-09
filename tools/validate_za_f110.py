#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'app/src/main/assets/za-encounters-v8.js'
text=P.read_text(encoding='utf-8')
m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('ZA F11.0 validation: DATA payload not found')
d=json.loads(m.group(1))
assert d.get('version')=='8.0-f11.0'
assert d.get('gameId')=='za'
assert d['dexes']['lumiose']['size']==232 and d['dexes']['lumiose']['covered']==232
assert d['dexes']['hyperspace']['size']==132 and d['dexes']['hyperspace']['covered']==132
assert d.get('uniqueTrackedSpecies')==364
assert d.get('coveredSpecies')==364
assert d.get('missingSpecies')==[]
assert d.get('partialCoverage') is False
assert d.get('pkhexLegalityImport') is True
assert d.get('megaDimensionDlc') is True
assert d.get('threeSixtyFourAvailableSpecies') is True
assert int(d.get('pkhexWildRoutesAdded',0))>0
assert int(d.get('pkhexSpecialRoutesAdded',0))>0
# Representative Lumiose + Hyperspace + special species.
for pid in ('152','498','158','718','719','150','56','979','807'):
 assert pid in (d.get('pokemon') or {}),pid
 assert (d['pokemon'][pid].get('encounters') or []),pid
reg=(ROOT/'app/src/main/assets/acquisition-provider-registry-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f11.0'" in reg and 'legendsZaAdapter:' in reg
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8')
assert "script('za-encounters-v8.js','za-data')" in loader
print(f"ZA F11.0 VALIDATION: PASS • Lumiose=232/232 • Hyperspace=132/132 • tracked=364/364 • missing=0 • wild={d['pkhexWildRoutesAdded']} • special={d['pkhexSpecialRoutesAdded']}")

#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'app/src/main/assets/bdsp-encounters-v8.js'
text=P.read_text(encoding='utf-8');m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('BDSP F8.0 validation: DATA payload not found')
data=json.loads(m.group(1));assert data.get('version')=='8.0-f8.0';assert data.get('gameId')=='bdsp';assert data.get('dexSpecies')==151
covered=int(data.get('coveredSpecies',0));assert 80<=covered<=151,covered
missing=data.get('missingSpecies') or [];assert len(missing)==151-covered,(covered,len(missing));assert bool(data.get('partialCoverage'))==(covered<151)
for pid in ('387','390','393'):assert pid in (data.get('pokemon') or {}),pid
reg=(ROOT/'app/src/main/assets/acquisition-provider-registry-v8.js').read_text(encoding='utf-8');assert "version:'8.0-f8.0'" in reg;assert 'bdspAdapter:' in reg
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8');assert "script('bdsp-encounters-v8.js','bdsp-data')" in loader
print(f'BDSP F8.0 VALIDATION: PASS • Sinnoh={covered}/151 • missing={len(missing)} • partial={covered<151}')

#!/usr/bin/env python3
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'app/src/main/assets/bdsp-encounters-v8.js'
text=P.read_text(encoding='utf-8');m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
if not m:raise SystemExit('BDSP F8.1 validation: DATA payload not found')
data=json.loads(m.group(1));assert data.get('version')=='8.0-f8.1';assert data.get('gameId')=='bdsp';assert data.get('dexSpecies')==151
covered=int(data.get('coveredSpecies',0));missing=data.get('missingSpecies') or []
assert covered==151,(covered,missing);assert missing==[],missing;assert data.get('partialCoverage') is False
assert data.get('pkhexLegalityImport') is True
assert data.get('grandUndergroundRoutes') is True
assert data.get('verifiedBdspSpecialRoutes') is True
assert int(data.get('pkhexWildRoutesAdded',0))>0
assert int(data.get('pkhexSpeciesAddedCount',0))>0
assert data.get('pkhexImportFailures')==[],data.get('pkhexImportFailures')
for pid in ('387','390','393','408','410','425','440','442','447','480','481','482','483','484','490'):
 assert pid in (data.get('pokemon') or {}),pid
reg=(ROOT/'app/src/main/assets/acquisition-provider-registry-v8.js').read_text(encoding='utf-8');assert "version:'8.0-f11.0'" in reg;assert 'bdspAdapter:' in reg;assert 'scarletVioletAdapter:' in reg;assert 'legendsZaAdapter:' in reg
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8');assert "script('bdsp-encounters-v8.js','bdsp-data')" in loader;assert "script('sv-encounters-v8.js','sv-data')" in loader;assert "script('za-encounters-v8.js','za-data')" in loader
assert 'pkhexLegalityImport:true' in text and 'completeSinnohDex:' in text
print(f"BDSP F8.1 VALIDATION: PASS • Sinnoh={covered}/151 • missing=0 • pkhex_wild={data['pkhexWildRoutesAdded']} • pkhex_special={data['pkhexSpecialRoutesAdded']}")
# Compatibility chain: keep newer providers and global Living Dex UX gated in the
# workflow's existing structural validation stage.
subprocess.run([sys.executable,str(ROOT/'tools/validate_sv_f100.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'tools/validate_za_f110.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'tools/validate_livingdex_f112.py')],check=True)

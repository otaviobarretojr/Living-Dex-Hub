#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
OUT=ROOT/'app/src/main/assets/pokemon-offline-core-data-v8.js'

data=json.loads(SRC.read_text(encoding='utf-8'))
assert data.get('count')==1025 and len(data.get('pokemon',{}))==1025
payload=json.dumps(data,ensure_ascii=False,separators=(',',':'),sort_keys=True)
OUT.write_text('/* Living Dex Hub — embedded offline core for file:// Android WebView */\nwindow.__LD8_OFFLINE_DATA__='+payload+';\n',encoding='utf-8')
print(f'Embedded offline core: 1025/1025 • {OUT.stat().st_size} bytes')

# Build richer game acquisition caches in the same offline-data stage.
# Each builder preserves its committed fallback and returns success when the
# public endpoint is unavailable, so release builds do not depend on network.
for script in ('build_letsgo_encounters.py','build_swsh_encounters.py','enrich_swsh_dlc_scopes.py','enrich_swsh_special_routes.py','enrich_swsh_outside_dex.py','enrich_swsh_regional_forms.py','enrich_swsh_dlc_encounters.py','build_bdsp_encounters.py'):
    subprocess.run([sys.executable, str(ROOT/'tools'/script)], check=True)

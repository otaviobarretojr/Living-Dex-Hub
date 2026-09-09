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

# Build the richer Let’s Go encounter cache in the same offline-data stage.
# The encounter builder intentionally preserves the committed verified seed and
# returns success when the public endpoint is unavailable, so release builds do
# not become dependent on network availability.
subprocess.run([sys.executable, str(ROOT/'tools/build_letsgo_encounters.py')], check=True)

#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'app/src/main/assets';H=(A/'index.html').read_text(encoding='utf-8')
critical=['game-context-v8.js','game-selector-v8.js','home-v8.js','pokemon-offline-core-v8.js','pokemon-detail-v8.js','pokemon-evolution-v8.js','pokemon-data-v8.js','pokemon-about-v8.js','collection-reliability-v8.js','product-ux-v8.js']
styles=['design-system-v8.css','home-v8.css','shell-v8.css','game-selector-v8.css','pokemon-detail-v8.css','pokemon-evolution-v8.css','pokemon-data-v8.css','pokemon-about-v8.css','product-ux-v8.css','pokemon-reference-theme-v8.css']
for f in critical:
    if H.count(f)!=1: raise SystemExit(f'RUNTIME BUDGET FAIL: {f} injected {H.count(f)}x')
for f in styles:
    if H.count(f)!=1: raise SystemExit(f'RUNTIME BUDGET FAIL: {f} injected {H.count(f)}x')
off=A/'pokemon-offline-core-v8.json';offline_size=off.stat().st_size
js_size=sum((A/f).stat().st_size for f in critical);css_size=sum((A/f).stat().st_size for f in styles)
if offline_size>2_000_000: raise SystemExit(f'RUNTIME BUDGET FAIL: offline core {offline_size} bytes')
if js_size>750_000: raise SystemExit(f'RUNTIME BUDGET FAIL: critical JS {js_size} bytes')
if css_size>450_000: raise SystemExit(f'RUNTIME BUDGET FAIL: critical CSS {css_size} bytes')
legacy=['pokemon-alive-beta-v8','pokemon-3d-v8','pokemon-frame-animation-v8','model-viewer-f3101']
if any(x in H for x in legacy): raise SystemExit('RUNTIME BUDGET FAIL: abandoned experiment reference')
print(f'RUNTIME BUDGET: PASS • single injection • offline {offline_size} B • JS {js_size} B • CSS {css_size} B • no abandoned runtime')

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "app" / "src" / "main" / "assets" / "index.html"
IMG = ROOT / "app" / "src" / "main" / "assets" / "assets" / "pokemon"
PACK = ROOT / "data" / "embedded-dex-pack.json"

html = HTML.read_text(encoding="utf-8")
pack = json.loads(PACK.read_text(encoding="utf-8"))
manifest = json.loads((IMG / "manifest.json").read_text(encoding="utf-8"))
expected_dex = {
    'letsgo:kanto','swsh:galar','swsh:isle-of-armor','swsh:crown-tundra',
    'bdsp:sinnoh','bdsp:national-bdsp','arceus:hisui',
    'sv:paldea','sv:kitakami','sv:blueberry','za:lumiose','za:hyperspace'
}
checks = {
    "core_title": "Living Dex Hub — Core 1.0" in html,
    "national_1025": "length:1025" in html,
    "six_games": all(x in html for x in ["id:'letsgo'","id:'swsh'","id:'bdsp'","id:'arceus'","id:'sv'","id:'za'"]),
    "twelve_dexes": {k for k,v in pack.get('dexes',{}).items() if v} == expected_dex,
    "embedded_complete": all(f"'{k}'" in html or f'"{k}"' in html for k in expected_dex),
    "images_1025": manifest.get('count') == 1025 and not manifest.get('missing'),
    "physical_png_count": len(list(IMG.glob('*.png'))) == 1025,
    "local_image_first": "assets/pokemon/${id}.png" in html,
    "no_unknown_method": "Método ainda não fechado" not in html and "kind:'unavailable'" in html,
    "backup": "function backup()" in html and "normalizeState" in html,
    "snapshots": "function createSnapshot" in html and "function restoreSnapshot" in html,
    "specimen_storage": "specimenInstances" in html and "function addSpecimenInstance" in html,
    "form_dex": "function ensureFormDex" in html and "function renderFormDex" in html,
    "runtime_smoke": "async function runRuntimeSmokeTest" in html,
    "reopen_harness": "data.reopenPass" in html and "livingdex-ci-reopen" in html,
    "mobile_pass": "Core 1.0 — mobile usability pass" in html,
    "apk_markers": "OFFLINE_POKEMON_ASSET_COUNT=1025" in html and "ANDROID_BUILD_READY=true" in html,
}
failed = [k for k,v in checks.items() if not v]
print(json.dumps({"checks": checks, "passed": len(checks)-len(failed), "total": len(checks), "failed": failed}, indent=2, ensure_ascii=False))
if failed:
    raise SystemExit("Core 1.0 validation failed: " + ", ".join(failed))

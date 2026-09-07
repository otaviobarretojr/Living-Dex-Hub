from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "app" / "src" / "main" / "assets" / "index.html"
PACK = ROOT / "data" / "embedded-dex-pack.json"

if not HTML.exists():
    raise SystemExit(f"HTML não encontrado: {HTML}")
if not PACK.exists():
    raise SystemExit(f"Data Pack não encontrado: {PACK}")

html = HTML.read_text(encoding="utf-8")
pack = json.loads(PACK.read_text(encoding="utf-8"))

expected = {
    "letsgo:kanto",
    "swsh:galar", "swsh:isle-of-armor", "swsh:crown-tundra",
    "bdsp:sinnoh", "bdsp:national-bdsp",
    "arceus:hisui",
    "sv:paldea", "sv:kitakami", "sv:blueberry",
    "za:lumiose", "za:hyperspace",
}

dexes = pack.get("dexes", {})
missing = sorted(expected - set(dexes))
empty = sorted(k for k in expected if not dexes.get(k))
if missing or empty:
    raise SystemExit(f"Data Pack incompleto. missing={missing} empty={empty}")

js_pack = json.dumps(dexes, ensure_ascii=False, separators=(",", ":"))
replacement = f"const EMBEDDED_DEX_PACK={js_pack};"

pattern = re.compile(r"const EMBEDDED_DEX_PACK=\{.*?\n\};", re.S)
updated, count = pattern.subn(replacement, html, count=1)
if count != 1:
    raise SystemExit(f"Bloco EMBEDDED_DEX_PACK não encontrado de forma única: {count}")

meta_pattern = re.compile(r"verifiedKeys:\[[^\]]*\]")
verified = ",".join(json.dumps(k) for k in sorted(expected))
updated, meta_count = meta_pattern.subn(f"verifiedKeys:[{verified}]", updated, count=1)
if meta_count != 1:
    raise SystemExit(f"verifiedKeys não encontrado de forma única: {meta_count}")

HTML.write_text(updated, encoding="utf-8")
print(f"Data Pack injetado: {len(expected)}/12 dexes em {HTML}")

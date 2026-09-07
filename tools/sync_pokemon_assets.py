from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pokemon"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png",
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png",
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png",
]

manifest = {"version": 1, "count": 0, "missing": [], "files": {}}

for poke_id in range(1, 1026):
    target = OUT / f"{poke_id}.png"
    if target.exists() and target.stat().st_size > 0:
        manifest["count"] += 1
        manifest["files"][str(poke_id)] = target.stat().st_size
        continue

    saved = False
    for template in SOURCES:
        url = template.format(id=poke_id)
        try:
            req = Request(url, headers={"User-Agent": "Living-Dex-Hub/1.0"})
            with urlopen(req, timeout=25) as response:
                data = response.read()
            if data:
                target.write_bytes(data)
                manifest["count"] += 1
                manifest["files"][str(poke_id)] = len(data)
                saved = True
                break
        except (HTTPError, URLError, TimeoutError):
            pass

    if not saved:
        manifest["missing"].append(poke_id)

    # Evita bombardear a origem e mantém o processo amigável à infraestrutura pública.
    time.sleep(0.03)

(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Assets locais: {manifest['count']}/1025")
if manifest["missing"]:
    print("Sem imagem:", ", ".join(map(str, manifest["missing"])))
    raise SystemExit(2)

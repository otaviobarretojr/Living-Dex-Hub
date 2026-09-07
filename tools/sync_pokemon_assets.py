from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "src" / "main" / "assets" / "assets" / "pokemon"
OUT.mkdir(parents=True, exist_ok=True)

# Standard sprites are intentionally preferred for the offline APK: they are
# much smaller than official artwork while still guaranteeing an image for
# every National Dex entry. The UI keeps higher-resolution remote fallbacks.
SOURCES = [
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png",
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png",
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png",
]

PNG = b"\x89PNG\r\n\x1a\n"

def fetch_one(poke_id):
    target = OUT / f"{poke_id}.png"
    if target.exists() and target.stat().st_size > 8 and target.read_bytes()[:8] == PNG:
        return poke_id, target.stat().st_size, None
    for template in SOURCES:
        try:
            req = Request(template.format(id=poke_id), headers={"User-Agent": "Living-Dex-Hub/1.0"})
            with urlopen(req, timeout=25) as response:
                data = response.read()
            if len(data) > 8 and data[:8] == PNG:
                target.write_bytes(data)
                return poke_id, len(data), None
        except (HTTPError, URLError, TimeoutError):
            pass
    return poke_id, 0, "missing"

files, missing = {}, []
with ThreadPoolExecutor(max_workers=16) as pool:
    futures = [pool.submit(fetch_one, i) for i in range(1, 1026)]
    for future in as_completed(futures):
        poke_id, size, error = future.result()
        if error:
            missing.append(poke_id)
        else:
            files[str(poke_id)] = size

manifest = {
    "version": 2,
    "count": len(files),
    "missing": sorted(missing),
    "totalBytes": sum(files.values()),
    "files": dict(sorted(files.items(), key=lambda x: int(x[0]))),
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Assets locais no APK: {manifest['count']}/1025 • {manifest['totalBytes']} bytes")
if manifest["count"] != 1025 or manifest["missing"]:
    raise SystemExit(f"Pacote de imagens incompleto: {manifest['count']}/1025; missing={manifest['missing']}")

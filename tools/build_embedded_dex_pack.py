from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "embedded-dex-pack.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

API = "https://pokeapi.co/api/v2/pokedex/{slug}/"
DEXES = {
    "letsgo:kanto": ["letsgo-kanto"],
    "swsh:galar": ["galar"],
    "swsh:isle-of-armor": ["isle-of-armor"],
    "swsh:crown-tundra": ["crown-tundra"],
    "bdsp:sinnoh": ["original-sinnoh"],
    "arceus:hisui": ["hisui"],
    "sv:paldea": ["paldea"],
    "sv:kitakami": ["kitakami"],
    "sv:blueberry": ["blueberry"],
    "za:lumiose": ["lumiose-city"],
    "za:hyperspace": ["hyperspace"],
}

pack = {
    "version": 1,
    "source": "PokeAPI v2 pokedex endpoints + deterministic BDSP National Dex",
    "dexes": {
        "bdsp:national-bdsp": [[i, i] for i in range(1, 494)]
    },
    "unresolved": []
}

for key, slugs in DEXES.items():
    rows = None
    used = None
    for slug in slugs:
        try:
            req = Request(API.format(slug=slug), headers={"User-Agent": "Living-Dex-Hub/1.0"})
            with urlopen(req, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            candidate = []
            for entry in payload.get("pokemon_entries", []):
                url = entry.get("pokemon_species", {}).get("url", "")
                match = re.search(r"/pokemon-species/(\d+)/", url)
                if not match:
                    continue
                candidate.append([int(match.group(1)), int(entry["entry_number"])])
            if candidate:
                rows = candidate
                used = slug
                break
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            pass

    if rows:
        pack["dexes"][key] = rows
    else:
        pack["unresolved"].append({"key": key, "tried": slugs})

OUT.write_text(json.dumps(pack, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Pokédexes embutíveis geradas: {len(pack['dexes'])}/12")
if pack["unresolved"]:
    print("Ainda sem fonte automatizada:")
    for item in pack["unresolved"]:
        print(" -", item["key"], "=>", ", ".join(item["tried"]))
    raise SystemExit(2)

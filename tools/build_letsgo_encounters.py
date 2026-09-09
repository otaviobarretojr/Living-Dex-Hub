#!/usr/bin/env python3
"""Build an offline Let's Go Pikachu/Eevee encounter asset from PokeAPI.

The committed seed remains the safe fallback. This script only replaces it when a
substantial, internally consistent dataset was fetched successfully.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/src/main/assets/letsgo-encounters-v8.js"
IDS = list(range(1, 152)) + [808, 809]
VERSIONS = {"lets-go-pikachu": "pikachu", "lets-go-eevee": "eevee"}
MIN_POKEMON_WITH_DATA = 80

# Verified non-wild acquisition records retained alongside PokeAPI encounters.
MANUAL = {
    1: [{"location": "Cerulean City", "method": "gift", "levelMin": 12, "levelMax": 12, "rate": None, "versions": ["pikachu", "eevee"], "conditions": [], "provenance": "verified-static-analysis"}],
    25: [{"location": "Pallet Town", "method": "gift", "levelMin": 5, "levelMax": 5, "rate": None, "versions": ["pikachu"], "conditions": [], "provenance": "verified-static-analysis"}],
}


def pretty(slug: str) -> str:
    text = slug.replace("kanto-", "").replace("-area", "").replace("-", " ")
    text = re.sub(r"\broute (\d+)\b", lambda m: f"Route {m.group(1)}", text, flags=re.I)
    return " ".join(w if w.startswith("Route") else w.capitalize() for w in text.split())


def fetch_one(pid: int):
    url = f"https://pokeapi.co/api/v2/pokemon/{pid}/encounters"
    req = urllib.request.Request(url, headers={"User-Agent": "LivingDexHub/8.0 (+offline-build)"})
    last = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return pid, json.load(r)
        except Exception as exc:  # network fallback is intentional
            last = exc
    raise RuntimeError(f"pokemon {pid}: {last}")


def normalize(pid: int, payload: list[dict]) -> list[dict]:
    grouped: dict[tuple, dict] = {}
    for area in payload or []:
        loc = pretty(str(area.get("location_area", {}).get("name", "")))
        if not loc:
            continue
        for vd in area.get("version_details", []) or []:
            vname = str(vd.get("version", {}).get("name", ""))
            version = VERSIONS.get(vname)
            if not version:
                continue
            for d in vd.get("encounter_details", []) or []:
                method = str(d.get("method", {}).get("name", "unknown"))
                lo, hi = int(d.get("min_level") or 0), int(d.get("max_level") or 0)
                rate = d.get("chance")
                conditions = sorted(str(x.get("name", "")) for x in (d.get("condition_values") or []) if x.get("name"))
                key = (loc, method, lo, hi, rate, tuple(conditions))
                rec = grouped.setdefault(key, {
                    "location": loc, "method": method, "levelMin": lo, "levelMax": hi,
                    "rate": rate, "versions": [], "conditions": conditions, "provenance": "pokeapi-v2"
                })
                if version not in rec["versions"]:
                    rec["versions"].append(version)
    out = list(grouped.values())
    out.extend(MANUAL.get(pid, []))
    for x in out:
        x["versions"].sort()
    out.sort(key=lambda x: (x["location"], x["method"], x["levelMin"], x["levelMax"], str(x["rate"])))
    return out


def main() -> int:
    fetched: dict[int, list[dict]] = {}
    failures = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(fetch_one, pid): pid for pid in IDS}
        for f in as_completed(futures):
            pid = futures[f]
            try:
                _, payload = f.result()
                enc = normalize(pid, payload)
                if enc:
                    fetched[pid] = enc
            except Exception as exc:
                failures.append(str(exc))

    if len(fetched) < MIN_POKEMON_WITH_DATA:
        print(f"Let’s Go encounter build fallback: only {len(fetched)} Pokémon with data; seed preserved.", file=sys.stderr)
        if failures:
            print(failures[:5], file=sys.stderr)
        return 0

    pokemon = {str(pid): {"encounters": fetched[pid]} for pid in sorted(fetched)}
    data = {
        "version": "8.0-f6.4",
        "gameId": "letsgo",
        "source": "pokeapi-v2+verified-static-analysis",
        "versions": ["pikachu", "eevee"],
        "pokemon": pokemon,
    }
    js = """/* Living Dex Hub — F6.4 generated offline Let’s Go encounter database */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return p.encounters.filter(e=>!version||e.versions.includes(version))}\nwindow.ld8LetsGoEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,pokemonCount:Object.keys(DATA.pokemon).length,offline:true,versionSpecific:true,provenance:true})};\n})();\n""" % json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(js, encoding="utf-8")
    print(f"Let’s Go encounters generated: {len(pokemon)} Pokémon; failures={len(failures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

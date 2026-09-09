#!/usr/bin/env python3
"""F7.4 — expand the Sword/Shield acquisition provider with Isle of Armor and Crown Tundra.

The existing validated Galar generator remains the baseline. This stage reuses the
repository's embedded dex pack for membership, fetches routes only for DLC species not
already present, and annotates every species with its validated dex scopes.
"""
from __future__ import annotations

import json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
PACK=ROOT/'data/embedded-dex-pack.json'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
sys.path.insert(0,str(ROOT/'tools'))
import build_swsh_encounters as base

SCOPES={
    'galar':'swsh:galar',
    'isle-of-armor':'swsh:isle-of-armor',
    'crown-tundra':'swsh:crown-tundra',
}
EXPECTED={'galar':400,'isle-of-armor':211,'crown-tundra':210}


def read_data():
    text=OUT.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise RuntimeError('Sword/Shield DATA payload not found')
    return json.loads(m.group(1))


def scope_ids(pack):
    out={}
    for scope,key in SCOPES.items():
        rows=(pack.get('dexes') or {}).get(key) or []
        ids={int(row[0]) for row in rows if isinstance(row,list) and row}
        if len(ids)!=EXPECTED[scope]:
            raise RuntimeError(f'{key}: expected {EXPECTED[scope]}, got {len(ids)}')
        out[scope]=ids
    return out


def main():
    if not OUT.exists() or not PACK.exists():
        print('Sword/Shield F7.4 fallback: baseline or embedded dex pack missing',file=sys.stderr);return 0
    data=read_data();pack=json.loads(PACK.read_text(encoding='utf-8'));scopes=scope_ids(pack)
    union=set().union(*scopes.values());pokemon=data.setdefault('pokemon',{})
    missing_from_payload=sorted(pid for pid in union if str(pid) not in pokemon)
    failures=[];fetched={}
    with ThreadPoolExecutor(max_workers=14) as ex:
        futures={ex.submit(base.fetch_encounters,pid):pid for pid in missing_from_payload}
        for f in as_completed(futures):
            pid=futures[f]
            try:
                _,payload=f.result();enc=base.normalize(payload)
                if enc:fetched[pid]=enc
            except Exception as exc:failures.append(str(exc))
    core={}
    if CORE.exists():core=json.loads(CORE.read_text(encoding='utf-8')).get('pokemon',{})
    for pid in missing_from_payload:
        records=fetched.setdefault(pid,[])
        evo=base.evolution_record(pid,core) if core else None
        if evo:records.append(evo)
        base.add_version_trade_route(records)
        if records:pokemon[str(pid)]={'encounters':records}

    for pid in union:
        p=pokemon.get(str(pid))
        if not p:continue
        p['dexScopes']=[scope for scope in SCOPES if pid in scopes[scope]]

    dexes={}
    for scope,ids in scopes.items():
        covered=sorted(pid for pid in ids if str(pid) in pokemon and (pokemon[str(pid)].get('encounters') or []))
        missing=sorted(ids-set(covered))
        dexes[scope]={'dexSpecies':len(ids),'coveredSpecies':len(covered),'missingSpecies':missing}

    data.update({
        'version':'8.0-f7.4',
        'source':str(data.get('source',''))+'+embedded-dex-pack-dlc-scopes',
        'dexes':dexes,
        'uniqueSwordShieldSpecies':len(union),
        'coveredSpecies':len([pid for pid in union if str(pid) in pokemon and (pokemon[str(pid)].get('encounters') or [])]),
        'missingSpecies':sorted(pid for pid in union if str(pid) not in pokemon or not (pokemon[str(pid)].get('encounters') or [])),
    })
    js="""/* Living Dex Hub — F7.4 Sword/Shield + Isle of Armor + Crown Tundra acquisition database */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,dexes:DATA.dexes,uniqueSwordShieldSpecies:DATA.uniqueSwordShieldSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true,verifiedSpecialAcquisition:true,threeDexScopes:true,dlcDexScopes:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print('Sword/Shield F7.4 scopes: '+', '.join(f"{s}={d['coveredSpecies']}/{d['dexSpecies']}" for s,d in dexes.items())+f"; union={data['coveredSpecies']}/{data['uniqueSwordShieldSpecies']}; added={len([p for p in missing_from_payload if str(p) in pokemon])}; failures={len(failures)}")
    return 0

if __name__=='__main__':raise SystemExit(main())

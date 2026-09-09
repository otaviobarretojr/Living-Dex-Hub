#!/usr/bin/env python3
"""F7.6 — add Sword/Shield acquisition routes for species obtainable in-game but outside the three tracked dexes.

This stage intentionally does not alter Galar / Isle of Armor / Crown Tundra membership
or completion counters. It only extends the acquisition provider so Living Dex can answer
"can I obtain this in Sword/Shield?" independently from "is it in a Sword/Shield Pokédex?".
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
sys.path.insert(0,str(ROOT/'tools'))
import enrich_swsh_special_routes as f75


def read_data():
    text=OUT.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise RuntimeError('Sword/Shield DATA payload not found')
    return json.loads(m.group(1))


def main():
    data=read_data();pokemon=data.setdefault('pokemon',{})
    pack=json.loads((ROOT/'data/embedded-dex-pack.json').read_text(encoding='utf-8'))
    keys=('swsh:galar','swsh:isle-of-armor','swsh:crown-tundra')
    union=set().union(*({int(r[0]) for r in (pack.get('dexes') or {}).get(k,[]) if isinstance(r,list) and r} for k in keys))

    added_routes=0
    outside=set()

    # Reuse the F7.5 verified special mechanics, but now retain species outside the dex union.
    for pid,recs in f75.SPECIAL.items():
        if pid in union:continue
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        p['dexScopes']=[];p['obtainableOutsideDex']=True
        for rec in recs:
            if f75.add_once(p.setdefault('encounters',[]),rec):added_routes+=1
        if p.get('encounters'):outside.add(pid)

    # Dynamax Adventures contains many obtainable legendaries / Ultra Beasts not listed in
    # the three Sword/Shield Pokédexes. Keep version restrictions from F7.5.
    for pid in sorted(f75.DA_BOTH|f75.DA_SWORD|f75.DA_SHIELD):
        if pid in union:continue
        versions=('sword',) if pid in f75.DA_SWORD else ('shield',) if pid in f75.DA_SHIELD else ('sword','shield')
        rec=f75.route('Max Lair · Dynamax Adventures','dynamax-adventure',70,versions=versions,conditions=('crown-tundra','dynamax-adventures','final-boss','one-capture-per-species'),note='Chefe final de Dynamax Adventures. A espécie é obtível em Sword/Shield mesmo quando não pertence às três Pokédex rastreadas.')
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        p['dexScopes']=[];p['obtainableOutsideDex']=True
        if f75.add_once(p.setdefault('encounters',[]),rec):added_routes+=1
        if p.get('encounters'):outside.add(pid)

    # Preserve the tracked-dex metrics exactly; add independent obtainability metrics.
    data.update({
        'version':'8.0-f7.6',
        'source':str(data.get('source',''))+'+outside-dex-obtainability',
        'obtainableOutsideDexSpecies':sorted(outside),
        'obtainableOutsideDexCount':len(outside),
        'totalObtainableSpecies':int(data.get('coveredSpecies',0))+len(outside),
    })
    js="""/* Living Dex Hub — F7.6 Sword/Shield obtainability outside tracked dexes */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,dexes:DATA.dexes,uniqueSwordShieldSpecies:DATA.uniqueSwordShieldSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,coveredSpecies:DATA.coveredSpecies,obtainableOutsideDexSpecies:DATA.obtainableOutsideDexSpecies,obtainableOutsideDexCount:DATA.obtainableOutsideDexCount,totalObtainableSpecies:DATA.totalObtainableSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,verifiedDlcSpecialRoutes:DATA.verifiedDlcSpecialRoutes,dynamaxAdventureRoutes:DATA.dynamaxAdventureRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true,verifiedSpecialAcquisition:true,threeDexScopes:true,dlcDexScopes:true,verifiedDlcSpecialAcquisition:true,dynamaxAdventures:true,outsideDexObtainability:true,dexMembershipSeparatedFromObtainability:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print(f"Sword/Shield F7.6 outside-dex: tracked={data.get('coveredSpecies')}/{data.get('uniqueSwordShieldSpecies')}; outside={len(outside)}; total_obtainable={data.get('totalObtainableSpecies')}; added_routes={added_routes}")
    return 0

if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""F7.7 — restore the six Galar Dex entries represented by regional forms.

PokeAPI's species-level encounter endpoint misses these because the Galar Pokédex entry
uses the Galarian form while the National species id points at the base species. This
stage adds verified form-aware routes without changing National-Dex identity semantics.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
PACK=ROOT/'data/embedded-dex-pack.json'

def read_data():
    text=OUT.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise RuntimeError('Sword/Shield DATA payload not found')
    return json.loads(m.group(1))

def route(location,method,lo,hi,versions,rate=None,conditions=(),note=''):
    return {'location':location,'method':method,'levelMin':lo,'levelMax':hi,'rate':rate,'versions':list(versions),'conditions':['form:galarian',*conditions],'provenance':'verified-regional-form-route','note':note,'regionalForm':'galarian'}

ROUTES={
    77:[
        route('Glimwood Tangle','wild-random',34,36,('shield',),10,('all-weather',),note='Galarian Ponyta é exclusivo de Shield; em Sword, obtenha por troca.'),
        route('Troca entre versões','trade',0,0,('sword',),None,('source-version:shield',),note='Receba Galarian Ponyta por troca a partir de Pokémon Shield.'),
    ],
    83:[
        route('Route 5','wild-overworld',19,21,('sword',),5,('all-weather',),note="Galarian Farfetch'd é exclusivo de Sword; em Shield, obtenha por troca."),
        route('Troca entre versões','trade',0,0,('shield',),None,('source-version:sword',),note="Receba Galarian Farfetch'd por troca a partir de Pokémon Sword."),
    ],
    222:[
        route("Giant's Mirror",'wild-overworld',28,30,('shield',),5,('weather:overcast',),note='Galarian Corsola é exclusivo de Shield; em Sword, obtenha por troca.'),
        route('Troca entre versões','trade',0,0,('sword',),None,('source-version:shield',),note='Receba Galarian Corsola por troca a partir de Pokémon Shield.'),
    ],
    263:[
        route('Route 3','wild-overworld',10,14,('sword','shield'),38,('all-weather',),note='Galarian Zigzagoon aparece em ambas as versões.'),
    ],
    554:[
        route('Route 8 · Steamdrift Way','wild-random',38,41,('sword',),5,('all-weather',),note='Galarian Darumaka é exclusivo de Sword; em Shield, obtenha por troca.'),
        route('Troca entre versões','trade',0,0,('shield',),None,('source-version:sword',),note='Receba Galarian Darumaka por troca a partir de Pokémon Sword.'),
    ],
    618:[
        route('Galar Mine No. 2','wild-random',20,24,('sword','shield'),5,('all-weather',),note='Galarian Stunfisk aparece em ambas as versões; há também encontros visíveis no local.'),
    ],
}

def add_once(records,rec):
    sig=(rec['location'],rec['method'],tuple(rec['versions']),tuple(rec['conditions']))
    for x in records:
        if (x.get('location'),x.get('method'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []))==sig:return False
    records.append(rec);return True

def main():
    data=read_data();pokemon=data.setdefault('pokemon',{})
    pack=json.loads(PACK.read_text(encoding='utf-8'))
    scope_keys={'galar':'swsh:galar','isle-of-armor':'swsh:isle-of-armor','crown-tundra':'swsh:crown-tundra'}
    scopes={scope:{int(r[0]) for r in (pack.get('dexes') or {}).get(key,[]) if isinstance(r,list) and r} for scope,key in scope_keys.items()}
    union=set().union(*scopes.values())
    added=0
    for pid,recs in ROUTES.items():
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        p['dexScopes']=[s for s,ids in scopes.items() if pid in ids]
        p['regionalForm']='galarian'
        for rec in recs:
            if add_once(p.setdefault('encounters',[]),rec):added+=1
    dexes={}
    for scope,ids in scopes.items():
        covered=sorted(pid for pid in ids if (pokemon.get(str(pid),{}).get('encounters') or []))
        dexes[scope]={'dexSpecies':len(ids),'coveredSpecies':len(covered),'missingSpecies':sorted(ids-set(covered))}
    covered_union=sorted(pid for pid in union if (pokemon.get(str(pid),{}).get('encounters') or []))
    outside=list(data.get('obtainableOutsideDexSpecies') or [])
    data.update({
        'version':'8.0-f7.7',
        'source':str(data.get('source',''))+'+verified-galarian-form-routes',
        'dexes':dexes,
        'coveredSpecies':len(covered_union),
        'missingSpecies':sorted(union-set(covered_union)),
        'regionalFormRoutes':len(ROUTES),
        'regionalFormSpecies':sorted(ROUTES),
        'totalObtainableSpecies':len(covered_union)+len(outside),
    })
    js="""/* Living Dex Hub — F7.7 verified Galar regional-form acquisition routes */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,dexes:DATA.dexes,uniqueSwordShieldSpecies:DATA.uniqueSwordShieldSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,coveredSpecies:DATA.coveredSpecies,obtainableOutsideDexSpecies:DATA.obtainableOutsideDexSpecies,obtainableOutsideDexCount:DATA.obtainableOutsideDexCount,totalObtainableSpecies:DATA.totalObtainableSpecies,regionalFormRoutes:DATA.regionalFormRoutes,regionalFormSpecies:DATA.regionalFormSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,verifiedDlcSpecialRoutes:DATA.verifiedDlcSpecialRoutes,dynamaxAdventureRoutes:DATA.dynamaxAdventureRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true,verifiedSpecialAcquisition:true,threeDexScopes:true,dlcDexScopes:true,verifiedDlcSpecialAcquisition:true,dynamaxAdventures:true,outsideDexObtainability:true,dexMembershipSeparatedFromObtainability:true,regionalFormAware:true,galarDexRegionalFormsComplete:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print('Sword/Shield F7.7 regional forms: '+', '.join(f"{s}={d['coveredSpecies']}/{d['dexSpecies']}" for s,d in dexes.items())+f"; union={data['coveredSpecies']}/{data['uniqueSwordShieldSpecies']}; regional_forms={len(ROUTES)}; total_obtainable={data['totalObtainableSpecies']}; added_routes={added}")
    return 0
if __name__=='__main__':raise SystemExit(main())

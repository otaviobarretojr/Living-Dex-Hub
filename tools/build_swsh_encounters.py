#!/usr/bin/env python3
"""Build an offline Pokémon Sword/Shield acquisition asset for the base Galar Pokédex.

Species membership comes from PokeAPI's Galar Pokédex endpoint. Wild encounters are
filtered to Sword/Shield; indirect evolution routes come from the existing offline
Pokémon core. Version-exclusive direct encounters automatically receive a trade route
for the opposite version. If public data is unavailable, the committed fallback asset
is kept.
"""
from __future__ import annotations

import json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
VERSIONS={'sword':'sword','shield':'shield'}
MIN_SUBSTANTIAL=180


def request_json(url:str):
    req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/8.0 (+offline-build)'})
    last=None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
        except Exception as e:last=e
    raise RuntimeError(f'{url}: {last}')


def species_id(url:str)->int:
    m=re.search(r'/pokemon-species/(\d+)/?$',str(url))
    return int(m.group(1)) if m else 0


def load_galar_ids():
    data=request_json('https://pokeapi.co/api/v2/pokedex/galar')
    ids=[]
    for e in data.get('pokemon_entries',[]) or []:
        sid=species_id((e.get('pokemon_species') or {}).get('url',''))
        if sid:ids.append(sid)
    return sorted(set(ids))


def pretty(slug:str)->str:
    text=slug.replace('-area','').replace('-',' ')
    text=re.sub(r'\broute (\d+)\b',lambda m:f'Route {m.group(1)}',text,flags=re.I)
    return ' '.join(w if w.startswith('Route') else w.capitalize() for w in text.split())


def fetch_encounters(pid:int):
    return pid,request_json(f'https://pokeapi.co/api/v2/pokemon/{pid}/encounters')


def normalize(payload):
    grouped={}
    for area in payload or []:
        loc=pretty(str((area.get('location_area') or {}).get('name','')))
        if not loc:continue
        for vd in area.get('version_details',[]) or []:
            vname=str((vd.get('version') or {}).get('name',''))
            version=VERSIONS.get(vname)
            if not version:continue
            for d in vd.get('encounter_details',[]) or []:
                method=str((d.get('method') or {}).get('name','unknown'))
                lo,hi=int(d.get('min_level') or 0),int(d.get('max_level') or 0)
                rate=d.get('chance')
                conditions=sorted(str(x.get('name','')) for x in (d.get('condition_values') or []) if x.get('name'))
                key=(loc,method,lo,hi,rate,tuple(conditions))
                rec=grouped.setdefault(key,{'location':loc,'method':method,'levelMin':lo,'levelMax':hi,'rate':rate,'versions':[],'conditions':conditions,'provenance':'pokeapi-v2'})
                if version not in rec['versions']:rec['versions'].append(version)
    out=list(grouped.values())
    for x in out:x['versions'].sort()
    out.sort(key=lambda x:(x['location'],x['method'],x['levelMin'],x['levelMax'],str(x['rate'])))
    return out


def evolution_record(pid:int,core:dict):
    p=core.get(str(pid),{});parent=p.get('evolvesFrom')
    if not parent:return None
    details=p.get('evolutionDetails') or [{}]
    d=sorted(details,key=lambda x:(not bool(x.get('min_level') or x.get('item') or x.get('trigger')=='trade' or x.get('known_move') or x.get('location')),))[0]
    trigger=d.get('trigger') or 'level-up';conditions=[f'from:{int(parent)}']
    if d.get('min_level') is not None:conditions.append(f"min-level:{int(d['min_level'])}")
    if d.get('item'):conditions.append(f"item:{d['item']}")
    if d.get('held_item'):conditions.append(f"held-item:{d['held_item']}")
    if d.get('known_move'):conditions.append(f"known-move:{d['known_move']}")
    if d.get('known_move_type'):conditions.append(f"known-move-type:{d['known_move_type']}")
    if d.get('location'):conditions.append(f"location:{d['location']}")
    if d.get('min_happiness') is not None:conditions.append(f"min-happiness:{int(d['min_happiness'])}")
    if d.get('min_beauty') is not None:conditions.append(f"min-beauty:{int(d['min_beauty'])}")
    if d.get('min_affection') is not None:conditions.append(f"min-affection:{int(d['min_affection'])}")
    if d.get('time_of_day'):conditions.append(f"time:{d['time_of_day']}")
    if d.get('gender') is not None:conditions.append(f"gender:{int(d['gender'])}")
    if d.get('relative_physical_stats') is not None:conditions.append(f"relative-stats:{int(d['relative_physical_stats'])}")
    if d.get('needs_overworld_rain'):conditions.append('overworld-rain')
    if d.get('turn_upside_down'):conditions.append('turn-upside-down')
    method='trade-evolution' if trigger=='trade' else 'item-evolution' if trigger=='use-item' else 'evolution'
    lvl=int(d.get('min_level') or 0)
    return {'location':'Evolução','method':method,'levelMin':lvl,'levelMax':lvl,'rate':None,'versions':['shield','sword'],'conditions':conditions,'provenance':'offline-evolution-core','sourcePokemon':int(parent),'specialEvolution':len(conditions)>2}


def add_version_trade_route(records:list[dict]):
    direct=[r for r in records if r.get('provenance')=='pokeapi-v2']
    seen=set()
    for r in direct:seen.update(r.get('versions') or [])
    if seen=={'sword'}:
        records.append({'location':'Troca entre versões','method':'trade','levelMin':0,'levelMax':0,'rate':None,'versions':['shield'],'conditions':['source-version:sword'],'provenance':'derived-version-exclusive','note':'Sem encontro direto registrado em Shield; obtenha por troca a partir de Sword.'})
        return 'sword'
    if seen=={'shield'}:
        records.append({'location':'Troca entre versões','method':'trade','levelMin':0,'levelMax':0,'rate':None,'versions':['sword'],'conditions':['source-version:shield'],'provenance':'derived-version-exclusive','note':'Sem encontro direto registrado em Sword; obtenha por troca a partir de Shield.'})
        return 'shield'
    return ''


def main():
    try:ids=load_galar_ids()
    except Exception as e:
        print(f'Sword/Shield fallback: Galar Pokédex unavailable: {e}',file=sys.stderr);return 0
    if len(ids)<350:
        print(f'Sword/Shield fallback: unexpected Galar dex size {len(ids)}',file=sys.stderr);return 0
    fetched={};failures=[]
    with ThreadPoolExecutor(max_workers=14) as ex:
        futures={ex.submit(fetch_encounters,pid):pid for pid in ids}
        for f in as_completed(futures):
            pid=futures[f]
            try:
                _,payload=f.result();enc=normalize(payload)
                if enc:fetched[pid]=enc
            except Exception as e:failures.append(str(e))
    special_evolutions=0
    if CORE.exists():
        core=json.loads(CORE.read_text(encoding='utf-8')).get('pokemon',{})
        for pid in ids:
            evo=evolution_record(pid,core)
            if evo:
                fetched.setdefault(pid,[]).append(evo)
                if evo.get('specialEvolution'):special_evolutions+=1
    exclusives={'sword':0,'shield':0}
    for pid in ids:
        side=add_version_trade_route(fetched.setdefault(pid,[]))
        if side:exclusives[side]+=1
    if len([x for x in fetched.values() if x])<MIN_SUBSTANTIAL:
        print(f'Sword/Shield fallback: only {len([x for x in fetched.values() if x])} covered; seed preserved.',file=sys.stderr);return 0
    pokemon={str(pid):{'encounters':fetched[pid]} for pid in sorted(fetched) if fetched[pid]}
    missing=[pid for pid in ids if str(pid) not in pokemon]
    data={'version':'8.0-f7.2','gameId':'swsh','source':'pokeapi-v2+offline-evolution-core+derived-version-exclusive-trades','versions':['sword','shield'],'dexSpecies':len(ids),'coveredSpecies':len(pokemon),'missingSpecies':missing,'exclusiveDirectSpecies':exclusives,'specialEvolutionRoutes':special_evolutions,'pokemon':pokemon}
    js="""/* Living Dex Hub — F7.2 generated offline Sword/Shield acquisition database */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print(f"Sword/Shield acquisitions generated: {len(pokemon)}/{len(ids)} Pokémon; missing={len(missing)}; exclusives={exclusives}; special_evolutions={special_evolutions}; failures={len(failures)}")
    return 0

if __name__=='__main__':raise SystemExit(main())

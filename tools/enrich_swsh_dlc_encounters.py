#!/usr/bin/env python3
"""F7.8 — ingest Isle of Armor / Crown Tundra encounter rows from PokeAPI.

PokeAPI publishes the Gen 8 expansion encounters under separate version slugs
(the-isle-of-armor-sword/shield and the-crown-tundra-sword/shield). Earlier stages
filtered only the base `sword` / `shield` slugs, which explains the remaining DLC gaps.
This stage only fills tracked species that still have no route after F7.7.
"""
from __future__ import annotations
import json,re,sys,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
PACK=ROOT/'data/embedded-dex-pack.json'

DLC_VERSIONS={
    'the-isle-of-armor-sword':('sword','isle-of-armor'),
    'the-isle-of-armor-shield':('shield','isle-of-armor'),
    'the-crown-tundra-sword':('sword','crown-tundra'),
    'the-crown-tundra-shield':('shield','crown-tundra'),
}

def read_data():
    text=OUT.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise RuntimeError('Sword/Shield DATA payload not found')
    return json.loads(m.group(1))

def request_json(url:str):
    req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/8.0 (+offline-build)'})
    last=None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
        except Exception as e:last=e
    raise RuntimeError(f'{url}: {last}')

def pretty(slug:str)->str:
    text=str(slug or '').replace('-area','').replace('-',' ')
    text=re.sub(r'\broute (\d+)\b',lambda m:f'Route {m.group(1)}',text,flags=re.I)
    return ' '.join(w if w.startswith('Route') else w.capitalize() for w in text.split())

def fetch(pid:int):
    return pid,request_json(f'https://pokeapi.co/api/v2/pokemon/{pid}/encounters')

def normalize(payload,allowed_scopes:set[str]):
    grouped={}
    for area in payload or []:
        loc=pretty((area.get('location_area') or {}).get('name',''))
        if not loc:continue
        for vd in area.get('version_details') or []:
            slug=str((vd.get('version') or {}).get('name',''))
            mapped=DLC_VERSIONS.get(slug)
            if not mapped:continue
            version,scope=mapped
            if scope not in allowed_scopes:continue
            for d in vd.get('encounter_details') or []:
                method=str((d.get('method') or {}).get('name','unknown'))
                lo=int(d.get('min_level') or 0);hi=int(d.get('max_level') or 0)
                rate=d.get('chance')
                conditions=sorted(str(x.get('name','')) for x in (d.get('condition_values') or []) if x.get('name'))
                # Scope is first-class route metadata and also a translated condition in the guide.
                cond=sorted(set([scope,*conditions]))
                key=(scope,loc,method,lo,hi,rate,tuple(cond))
                rec=grouped.setdefault(key,{'location':loc,'method':method,'levelMin':lo,'levelMax':hi,'rate':rate,'versions':[],'conditions':cond,'provenance':'pokeapi-v2-dlc','dexScope':scope,'sourceVersionSlugs':[]})
                if version not in rec['versions']:rec['versions'].append(version)
                if slug not in rec['sourceVersionSlugs']:rec['sourceVersionSlugs'].append(slug)
    out=list(grouped.values())
    for r in out:
        r['versions'].sort();r['sourceVersionSlugs'].sort()
    out.sort(key=lambda x:(x.get('dexScope',''),x['location'],x['method'],x['levelMin'],x['levelMax'],str(x['rate'])))
    return out

def add_once(records,rec):
    sig=(rec.get('dexScope'),rec.get('location'),rec.get('method'),tuple(rec.get('versions') or []),tuple(rec.get('conditions') or []),rec.get('levelMin'),rec.get('levelMax'),rec.get('rate'))
    for x in records:
        xs=(x.get('dexScope'),x.get('location'),x.get('method'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []),x.get('levelMin'),x.get('levelMax'),x.get('rate'))
        if xs==sig:return False
    records.append(rec);return True

def main():
    data=read_data();pokemon=data.setdefault('pokemon',{})
    pack=json.loads(PACK.read_text(encoding='utf-8'))
    scope_keys={'galar':'swsh:galar','isle-of-armor':'swsh:isle-of-armor','crown-tundra':'swsh:crown-tundra'}
    scopes={scope:{int(r[0]) for r in (pack.get('dexes') or {}).get(key,[]) if isinstance(r,list) and r} for scope,key in scope_keys.items()}
    union=set().union(*scopes.values())
    missing=sorted(pid for pid in union if not (pokemon.get(str(pid),{}).get('encounters') or []))
    fetched={};failures=[]
    with ThreadPoolExecutor(max_workers=14) as ex:
        futures={ex.submit(fetch,pid):pid for pid in missing}
        for f in as_completed(futures):
            pid=futures[f]
            try:
                _,payload=f.result();allowed={s for s in ('isle-of-armor','crown-tundra') if pid in scopes[s]}
                rows=normalize(payload,allowed)
                if rows:fetched[pid]=rows
            except Exception as e:failures.append(f'{pid}:{e}')
    added_routes=0;covered_ids=[]
    for pid,recs in fetched.items():
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        p['dexScopes']=[s for s,ids in scopes.items() if pid in ids]
        before=len(p.get('encounters') or [])
        for rec in recs:
            if add_once(p.setdefault('encounters',[]),rec):added_routes+=1
        if len(p.get('encounters') or [])>before:covered_ids.append(pid)
    dexes={}
    for scope,ids in scopes.items():
        covered=sorted(pid for pid in ids if (pokemon.get(str(pid),{}).get('encounters') or []))
        dexes[scope]={'dexSpecies':len(ids),'coveredSpecies':len(covered),'missingSpecies':sorted(ids-set(covered))}
    covered_union=sorted(pid for pid in union if (pokemon.get(str(pid),{}).get('encounters') or []))
    outside=list(data.get('obtainableOutsideDexSpecies') or [])
    data.update({
        'version':'8.0-f7.8',
        'source':str(data.get('source',''))+'+pokeapi-v2-dlc-version-slugs',
        'dexes':dexes,
        'coveredSpecies':len(covered_union),
        'missingSpecies':sorted(union-set(covered_union)),
        'dlcEncounterSpeciesAdded':sorted(covered_ids),
        'dlcEncounterSpeciesAddedCount':len(covered_ids),
        'dlcEncounterRoutesAdded':added_routes,
        'dlcEncounterFailures':len(failures),
        'totalObtainableSpecies':len(covered_union)+len(outside),
    })
    js="""/* Living Dex Hub — F7.8 Sword/Shield DLC encounter version ingestion */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,dexes:DATA.dexes,uniqueSwordShieldSpecies:DATA.uniqueSwordShieldSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,coveredSpecies:DATA.coveredSpecies,obtainableOutsideDexSpecies:DATA.obtainableOutsideDexSpecies,obtainableOutsideDexCount:DATA.obtainableOutsideDexCount,totalObtainableSpecies:DATA.totalObtainableSpecies,regionalFormRoutes:DATA.regionalFormRoutes,regionalFormSpecies:DATA.regionalFormSpecies,dlcEncounterSpeciesAdded:DATA.dlcEncounterSpeciesAdded,dlcEncounterSpeciesAddedCount:DATA.dlcEncounterSpeciesAddedCount,dlcEncounterRoutesAdded:DATA.dlcEncounterRoutesAdded,dlcEncounterFailures:DATA.dlcEncounterFailures,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,verifiedDlcSpecialRoutes:DATA.verifiedDlcSpecialRoutes,dynamaxAdventureRoutes:DATA.dynamaxAdventureRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true,verifiedSpecialAcquisition:true,threeDexScopes:true,dlcDexScopes:true,verifiedDlcSpecialAcquisition:true,dynamaxAdventures:true,outsideDexObtainability:true,dexMembershipSeparatedFromObtainability:true,regionalFormAware:true,galarDexRegionalFormsComplete:true,dlcVersionSlugIngestion:true,dlcEncounterProvider:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print('Sword/Shield F7.8 DLC encounters: '+', '.join(f"{s}={d['coveredSpecies']}/{d['dexSpecies']}" for s,d in dexes.items())+f"; union={data['coveredSpecies']}/{data['uniqueSwordShieldSpecies']}; added_species={len(covered_ids)}; added_routes={added_routes}; remaining={len(data['missingSpecies'])}; failures={len(failures)}; total_obtainable={data['totalObtainableSpecies']}")
    return 0
if __name__=='__main__':raise SystemExit(main())

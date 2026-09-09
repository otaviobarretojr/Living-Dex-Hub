#!/usr/bin/env python3
"""Build the first offline Brilliant Diamond/Shining Pearl acquisition provider.

F8.0 starts with the 151-entry Sinnoh Pokédex. Membership comes from PokeAPI's
original-sinnoh dex, wild encounters from the brilliant-diamond/shining-pearl
version slugs, and indirect routes from the existing offline evolution core.
Partial coverage is intentionally emitted so CI can audit and close unsupported
special-acquisition gaps instead of hiding them behind a seed fallback.
"""
from __future__ import annotations
import json,re,sys,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/bdsp-encounters-v8.js'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
VERSIONS={'brilliant-diamond':'diamond','shining-pearl':'pearl'}
MANUAL={
  387:[{'location':'Lake Verity · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['diamond','pearl'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Turtwig é uma das três escolhas iniciais. Se escolheu outro neste save, obtenha por troca.'}],
  390:[{'location':'Lake Verity · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['diamond','pearl'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Chimchar é uma das três escolhas iniciais. Se escolheu outro neste save, obtenha por troca.'}],
  393:[{'location':'Lake Verity · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['diamond','pearl'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Piplup é uma das três escolhas iniciais. Se escolheu outro neste save, obtenha por troca.'}],
}
def request_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/8.0 (+offline-build)'})
 last=None
 for _ in range(3):
  try:
   with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
  except Exception as e:last=e
 raise RuntimeError(f'{url}: {last}')
def species_id(url):
 m=re.search(r'/pokemon-species/(\d+)/?$',str(url));return int(m.group(1)) if m else 0
def load_ids():
 data=request_json('https://pokeapi.co/api/v2/pokedex/original-sinnoh');ids=[]
 for e in data.get('pokemon_entries',[]) or []:
  sid=species_id((e.get('pokemon_species') or {}).get('url',''))
  if sid:ids.append(sid)
 return sorted(set(ids))
def pretty(slug):return ' '.join(x.capitalize() for x in str(slug).replace('-area','').replace('-',' ').split())
def fetch(pid):return pid,request_json(f'https://pokeapi.co/api/v2/pokemon/{pid}/encounters')
def normalize(payload):
 grouped={}
 for area in payload or []:
  loc=pretty((area.get('location_area') or {}).get('name',''))
  for vd in area.get('version_details',[]) or []:
   version=VERSIONS.get((vd.get('version') or {}).get('name',''))
   if not version:continue
   for d in vd.get('encounter_details',[]) or []:
    method=str((d.get('method') or {}).get('name','unknown'));lo=int(d.get('min_level') or 0);hi=int(d.get('max_level') or 0);rate=d.get('chance')
    cond=sorted(str(x.get('name','')) for x in (d.get('condition_values') or []) if x.get('name'))
    key=(loc,method,lo,hi,rate,tuple(cond));rec=grouped.setdefault(key,{'location':loc,'method':method,'levelMin':lo,'levelMax':hi,'rate':rate,'versions':[],'conditions':cond,'provenance':'pokeapi-v2'})
    if version not in rec['versions']:rec['versions'].append(version)
 out=list(grouped.values())
 for r in out:r['versions'].sort()
 return out
def evolution_record(pid,core):
 p=core.get(str(pid),{});parent=p.get('evolvesFrom')
 if not parent:return None
 d=(p.get('evolutionDetails') or [{}])[0];trigger=d.get('trigger') or 'level-up';c=[f'from:{int(parent)}']
 for key,prefix in [('min_level','min-level'),('item','item'),('held_item','held-item'),('known_move','known-move'),('location','location'),('time_of_day','time')]:
  if d.get(key) not in (None,''):c.append(f'{prefix}:{d[key]}')
 if d.get('min_happiness') is not None:c.append(f"min-happiness:{int(d['min_happiness'])}")
 method='trade-evolution' if trigger=='trade' else 'item-evolution' if trigger=='use-item' else 'evolution';lvl=int(d.get('min_level') or 0)
 return {'location':'Evolução','method':method,'levelMin':lvl,'levelMax':lvl,'rate':None,'versions':['diamond','pearl'],'conditions':c,'provenance':'offline-evolution-core','sourcePokemon':int(parent)}
def add_trade(records):
 direct=[r for r in records if r.get('provenance')=='pokeapi-v2'];seen=set()
 for r in direct:seen.update(r.get('versions') or [])
 if seen=={'diamond'}:records.append({'location':'Troca entre versões','method':'trade','levelMin':0,'levelMax':0,'rate':None,'versions':['pearl'],'conditions':['source-version:diamond'],'provenance':'derived-version-exclusive','note':'Sem encontro direto registrado em Shining Pearl; obtenha por troca a partir de Brilliant Diamond.'});return 'diamond'
 if seen=={'pearl'}:records.append({'location':'Troca entre versões','method':'trade','levelMin':0,'levelMax':0,'rate':None,'versions':['diamond'],'conditions':['source-version:pearl'],'provenance':'derived-version-exclusive','note':'Sem encontro direto registrado em Brilliant Diamond; obtenha por troca a partir de Shining Pearl.'});return 'pearl'
 return ''
def main():
 try:ids=load_ids()
 except Exception as e:print('BDSP fallback:',e,file=sys.stderr);return 0
 if len(ids)!=151:print('BDSP fallback: unexpected Sinnoh dex size',len(ids),file=sys.stderr);return 0
 fetched={};failures=[]
 with ThreadPoolExecutor(max_workers=14) as ex:
  fut={ex.submit(fetch,p):p for p in ids}
  for f in as_completed(fut):
   p=fut[f]
   try:_,raw=f.result();fetched[p]=normalize(raw)
   except Exception as e:failures.append(str(e));fetched[p]=[]
 core=json.loads(CORE.read_text(encoding='utf-8')).get('pokemon',{}) if CORE.exists() else {}
 for p in ids:
  evo=evolution_record(p,core)
  if evo:fetched[p].append(evo)
  for r in MANUAL.get(p,[]):fetched[p].append(dict(r))
 exclusives={'diamond':0,'pearl':0}
 for p in ids:
  side=add_trade(fetched[p])
  if side:exclusives[side]+=1
 pokemon={str(p):{'encounters':fetched[p]} for p in ids if fetched[p]};missing=[p for p in ids if not fetched[p]]
 data={'version':'8.0-f8.0','gameId':'bdsp','source':'pokeapi-v2+offline-evolution-core+verified-starters+derived-version-exclusive-trades','versions':['diamond','pearl'],'dexSpecies':151,'coveredSpecies':len(pokemon),'missingSpecies':missing,'exclusiveDirectSpecies':exclusives,'partialCoverage':bool(missing),'pokemon':pokemon}
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F8.0 generated offline BDSP acquisition database */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8BdspEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexSpecies:DATA.dexSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,partialCoverage:DATA.partialCoverage,offline:true,versionSpecific:true,indirectAcquisition:true,exclusiveTradeRoutes:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8');print(f"BDSP acquisitions generated: {len(pokemon)}/151; missing={len(missing)}; exclusives={exclusives}; failures={len(failures)}")
 return 0
if __name__=='__main__':raise SystemExit(main())

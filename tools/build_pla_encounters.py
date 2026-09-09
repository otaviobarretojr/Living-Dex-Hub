#!/usr/bin/env python3
"""F9.0 — build offline Pokémon Legends: Arceus acquisition provider.

Starts from the 242-entry Hisui Pokédex, imports direct PokeAPI encounter data for
Legends: Arceus, reuses the offline evolution core, and adds verified story/gift
routes for the three starters. Coverage stays explicit so CI can expose the exact
special-acquisition gaps for the next enrichment pass.
"""
from __future__ import annotations
import json,re,sys,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/pla-encounters-v8.js'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
VERSION='legends-arceus'

def request_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/9.0 (+offline-build)'})
 last=None
 for _ in range(3):
  try:
   with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
  except Exception as e:last=e
 raise RuntimeError(f'{url}: {last}')

def species_id(url):
 m=re.search(r'/pokemon-species/(\d+)/?$',str(url));return int(m.group(1)) if m else 0

def load_ids():
 data=request_json('https://pokeapi.co/api/v2/pokedex/hisui');ids=[]
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
   if (vd.get('version') or {}).get('name')!=VERSION:continue
   for d in vd.get('encounter_details',[]) or []:
    method=str((d.get('method') or {}).get('name','unknown'));lo=int(d.get('min_level') or 0);hi=int(d.get('max_level') or 0);rate=d.get('chance')
    cond=sorted(str(x.get('name','')) for x in (d.get('condition_values') or []) if x.get('name'))
    key=(loc,method,lo,hi,rate,tuple(cond))
    grouped.setdefault(key,{'location':loc,'method':method,'levelMin':lo,'levelMax':hi,'rate':rate,'versions':['arceus'],'conditions':cond,'provenance':'pokeapi-v2'})
 return list(grouped.values())

def evolution_record(pid,core):
 p=core.get(str(pid),{});parent=p.get('evolvesFrom')
 if not parent:return None
 d=(p.get('evolutionDetails') or [{}])[0];trigger=d.get('trigger') or 'level-up';c=[f'from:{int(parent)}']
 for key,prefix in [('min_level','min-level'),('item','item'),('held_item','held-item'),('known_move','known-move'),('location','location'),('time_of_day','time')]:
  if d.get(key) not in (None,''):c.append(f'{prefix}:{d[key]}')
 if d.get('min_happiness') is not None:c.append(f"min-happiness:{int(d['min_happiness'])}")
 method='trade-evolution' if trigger=='trade' else 'item-evolution' if trigger=='use-item' else 'evolution';lvl=int(d.get('min_level') or 0)
 return {'location':'Evolução','method':method,'levelMin':lvl,'levelMax':lvl,'rate':None,'versions':['arceus'],'conditions':c,'provenance':'offline-evolution-core','sourcePokemon':int(parent)}

STARTERS={
 722:{'location':'Jubilife Village · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['arceus'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Rowlet é uma das três escolhas iniciais; os outros iniciais ficam disponíveis novamente após a história principal.'},
 155:{'location':'Jubilife Village · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['arceus'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Cyndaquil é uma das três escolhas iniciais; os outros iniciais ficam disponíveis novamente após a história principal.'},
 501:{'location':'Jubilife Village · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['arceus'],'conditions':['choose-one-starter'],'provenance':'verified-game-mechanic','note':'Oshawott é uma das três escolhas iniciais; os outros iniciais ficam disponíveis novamente após a história principal.'},
}

def main():
 try:ids=load_ids()
 except Exception as e:print('PLA fallback:',e,file=sys.stderr);return 0
 if len(ids)!=242:print('PLA fallback: unexpected Hisui dex size',len(ids),file=sys.stderr);return 0
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
  if p in STARTERS:fetched[p].append(dict(STARTERS[p]))
 pokemon={str(p):{'encounters':fetched[p]} for p in ids if fetched[p]};missing=[p for p in ids if not fetched[p]]
 data={'version':'8.0-f9.0','gameId':'arceus','source':'pokeapi-v2+offline-evolution-core+verified-starters','versions':['arceus'],'dexSpecies':242,'coveredSpecies':len(pokemon),'missingSpecies':missing,'partialCoverage':bool(missing),'pokemon':pokemon,'hisuiDex':True}
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F9.0 generated offline Legends Arceus acquisition database */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8PlaEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexSpecies:DATA.dexSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,partialCoverage:DATA.partialCoverage,hisuiDex:true,offline:true,indirectAcquisition:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8');print(f"PLA acquisitions generated: {len(pokemon)}/242; missing={len(missing)}; failures={len(failures)}");print('PLA missing:',missing)
 return 0
if __name__=='__main__':raise SystemExit(main())

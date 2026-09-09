#!/usr/bin/env python3
"""F10.0 — Scarlet/Violet acquisition provider from PKHeX Gen9 legality data.

Tracks Paldea, Kitakami and Blueberry independently while exposing one SV provider.
Wild encounters come from PKHeX encounter_wild_paldea.pkl; indirect evolution
routes come from the existing 1025-species offline evolution core.
"""
from __future__ import annotations
import json,re,struct,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/sv-encounters-v8.js'
PACK=ROOT/'data/embedded-dex-pack.json'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
URL='https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Resources/legality/wild/Gen9/encounter_wild_paldea.pkl'
SCOPES={'paldea':'sv:paldea','kitakami':'sv:kitakami','blueberry':'sv:blueberry'}
EXPECTED={'paldea':400,'kitakami':200,'blueberry':243}

def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/10.0 (+PKHeX-legality-import)'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read()

def parse_binlinker32(raw:bytes):
 if len(raw)<12:raise ValueError('short BinLinker')
 ident=raw[:2];count=struct.unpack_from('<H',raw,2)[0]
 offs=list(struct.unpack_from('<'+'I'*(count+1),raw,4))
 out=[]
 for i in range(count):
  a,b=offs[i],offs[i+1]
  if not (0<=a<=b<=len(raw)):raise ValueError('offset range')
  out.append(raw[a:b])
 return ident,out

def dex_ids(pack,key):
 rows=(pack.get('dexes') or {}).get(key) or []
 return {int(r[0] if isinstance(r,list) else r.get('species')) for r in rows}

def evo_route(pid,core):
 p=core.get(str(pid),{});parent=p.get('evolvesFrom')
 if not parent:return None
 d=(p.get('evolutionDetails') or [{}])[0];trigger=d.get('trigger') or 'level-up';c=[f'from:{int(parent)}']
 for key,prefix in [('min_level','min-level'),('item','item'),('held_item','held-item'),('known_move','known-move'),('location','location'),('time_of_day','time')]:
  if d.get(key) not in (None,''):c.append(f'{prefix}:{d[key]}')
 if d.get('min_happiness') is not None:c.append(f"min-happiness:{int(d['min_happiness'])}")
 method='trade-evolution' if trigger=='trade' else 'item-evolution' if trigger=='use-item' else 'evolution'
 lvl=int(d.get('min_level') or 0)
 return {'location':'Evolução','method':method,'levelMin':lvl,'levelMax':lvl,'rate':None,'versions':['scarlet','violet'],'conditions':c,'provenance':'offline-evolution-core','sourcePokemon':int(parent)}

def add(bucket,rec):
 key=(rec.get('location'),rec.get('method'),rec.get('levelMin'),rec.get('levelMax'),tuple(rec.get('versions') or []),tuple(rec.get('conditions') or []),rec.get('provenance'))
 for x in bucket:
  k=(x.get('location'),x.get('method'),x.get('levelMin'),x.get('levelMax'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []),x.get('provenance'))
  if k==key:return False
 bucket.append(rec);return True

def main():
 pack=json.loads(PACK.read_text(encoding='utf-8'));core=json.loads(CORE.read_text(encoding='utf-8')).get('pokemon',{})
 scopes={name:dex_ids(pack,key) for name,key in SCOPES.items()}
 for n,want in EXPECTED.items():
  if len(scopes[n])!=want:raise SystemExit(f'{n} dex size {len(scopes[n])} != {want}')
 union=set().union(*scopes.values());pokemon={}
 ident,segs=parse_binlinker32(fetch(URL))
 wild_routes=0
 for seg in segs:
  if len(seg)<4:continue
  loc=seg[0];cross=seg[2];actual=cross or loc
  slots=seg[4:]
  for off in range(0,len(slots)-7,8):
   species=struct.unpack_from('<H',slots,off)[0];form=slots[off+2];gender=slots[off+3];lo=slots[off+4];hi=slots[off+5];tm=slots[off+6];weather=slots[off+7]
   if species not in union:continue
   cond=[]
   if form:cond.append(f'form:{form}')
   if tm:cond.append(f'time-mask:{tm}')
   if weather:cond.append(f'weather-mask:{weather}')
   rec={'location':f'SV · área #{actual}','method':'overworld-encounter','levelMin':int(lo),'levelMax':int(hi),'rate':None,'versions':['scarlet','violet'],'conditions':cond,'provenance':'pkhex-legality-wild','sourceLocationId':int(actual)}
   bucket=pokemon.setdefault(str(species),{'encounters':[]})['encounters']
   if add(bucket,rec):wild_routes+=1
 # evolution routes for every tracked species
 for pid in sorted(union):
  r=evo_route(pid,core)
  if r:add(pokemon.setdefault(str(pid),{'encounters':[]})['encounters'],r)
 # starters are verified fixed gifts in Encounters9.cs
 for pid in (906,909,912):
  if pid in union:add(pokemon.setdefault(str(pid),{'encounters':[]})['encounters'],{'location':'Cabo Poco · escolha inicial','method':'gift','levelMin':5,'levelMax':5,'rate':None,'versions':['scarlet','violet'],'conditions':['choose-one-starter'],'provenance':'pkhex-legality-static','note':'Escolha um dos três iniciais; os demais podem ser obtidos por troca.'})
 # verified Paldea Treasures of Ruin static encounters
 for pid in (1001,1002,1003,1004):
  if pid in union:add(pokemon.setdefault(str(pid),{'encounters':[]})['encounters'],{'location':'Paldea · santuário lendário','method':'legendary-capture','levelMin':60,'levelMax':60,'rate':None,'versions':['scarlet','violet'],'conditions':['treasures-of-ruin','one-per-save'],'provenance':'pkhex-legality-static'})
 # verified Kitakami story/static encounters represented in Encounters9.cs
 for pid in (1014,1015,1016,1017):
  if pid in union:add(pokemon.setdefault(str(pid),{'encounters':[]})['encounters'],{'location':'Kitakami · encontro de história','method':'story-capture','levelMin':70,'levelMax':70,'rate':None,'versions':['scarlet','violet'],'conditions':['teal-mask-story','one-per-save'],'provenance':'pkhex-legality-static'})
 for k,v in pokemon.items():
  pid=int(k);v['dexScopes']=[name for name,s in scopes.items() if pid in s]
 coverage={name:sum(1 for p in ids if (pokemon.get(str(p)) or {}).get('encounters')) for name,ids in scopes.items()}
 covered=sum(1 for p in union if (pokemon.get(str(p)) or {}).get('encounters'))
 missing=sorted(p for p in union if not (pokemon.get(str(p)) or {}).get('encounters'))
 data={'version':'8.0-f10.0','gameId':'sv','source':'pkhex-gen9-wild+offline-evolution-core+verified-static-seed','versions':['scarlet','violet'],'dexes':{n:{'size':len(scopes[n]),'covered':coverage[n]} for n in scopes},'uniqueTrackedSpecies':len(union),'coveredSpecies':covered,'missingSpecies':missing,'wildRoutes':wild_routes,'pkhexLegalityImport':True,'threeDexScopes':True,'pokemon':pokemon}
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F10.0 Scarlet/Violet acquisition provider */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SvEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexes:DATA.dexes,uniqueTrackedSpecies:DATA.uniqueTrackedSpecies,coveredSpecies:DATA.coveredSpecies,missingSpecies:DATA.missingSpecies,pkhexLegalityImport:true,threeDexScopes:true,offline:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8')
 print(f"SV F10.0: paldea={coverage['paldea']}/400, kitakami={coverage['kitakami']}/200, blueberry={coverage['blueberry']}/243; union={covered}/{len(union)}; wild_routes={wild_routes}; missing={len(missing)}")
 if missing:print('SV F10.0 missing:',missing)
if __name__=='__main__':main()

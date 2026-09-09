#!/usr/bin/env python3
"""F9.1 — enrich Legends: Arceus with PKHeX legality encounter data.

Decodes PKHeX's encounter_la.pkl BinLinker resource using EncounterArea8a's public
layout, then adds story/static/mythical routes represented by Encounters8a.cs.
Dex membership remains the 242-entry Hisui Pokédex; routes never change its denominator.
"""
from __future__ import annotations
import json,re,struct,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/pla-encounters-v8.js'
URL='https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Resources/legality/wild/Gen8/encounter_la.pkl'
TYPE={0:'wild-encounter',1:'space-time-distortion',2:'landmark',3:'mass-outbreak',4:'massive-mass-outbreak'}

def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/9.1 (+PKHeX-legality-import)'})
 with urllib.request.urlopen(req,timeout=30) as r:return r.read()

def request_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/9.1'})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)

def species_id(url):
 m=re.search(r'/pokemon-species/(\d+)/?$',str(url));return int(m.group(1)) if m else 0

def hisui_ids():
 d=request_json('https://pokeapi.co/api/v2/pokedex/hisui');return {species_id((e.get('pokemon_species') or {}).get('url','')) for e in d.get('pokemon_entries',[]) if species_id((e.get('pokemon_species') or {}).get('url',''))}

def parse_binlinker32(raw):
 if len(raw)<12:raise ValueError('short BinLinker')
 ident=raw[:2];count=struct.unpack_from('<H',raw,2)[0];offs=list(struct.unpack_from('<'+'I'*(count+1),raw,4))
 if count<=0 or offs[0]<4+4*(count+1):raise ValueError(('bad offsets',ident,count,offs[:2]))
 return ident,[raw[offs[i]:offs[i+1]] for i in range(count)]

def parse_area(seg):
 if len(seg)<4:return []
 n=seg[0];locs=list(seg[1:1+n]);align=n+1;align+=align&1
 if align+2>len(seg):return []
 typ=seg[align];count=seg[align+1];base=align+2;out=[]
 for i in range(count):
  off=base+i*8
  if off+8>len(seg):break
  species=struct.unpack_from('<H',seg,off)[0];form=seg[off+2];alpha=seg[off+3];lo=seg[off+4];hi=seg[off+5]
  if not species:continue
  cond=[]
  if form:cond.append(f'form:{form}')
  if alpha==2:cond.append('alpha:guaranteed')
  elif alpha==1:cond.append('alpha:possible')
  out.append((species,{'location':'Hisui · '+('/'.join('#'+str(x) for x in locs) if locs else 'área'), 'method':TYPE.get(typ,'wild-encounter'),'levelMin':int(lo),'levelMax':int(hi),'rate':None,'versions':['arceus'],'conditions':cond,'provenance':'pkhex-legality-wild','sourceLocations':locs,'sourceSlotType':int(typ)}))
 return out

def route(location,method,level,conditions=(),note=''):
 d={'location':location,'method':method,'levelMin':level,'levelMax':level,'rate':None,'versions':['arceus'],'conditions':list(conditions),'provenance':'pkhex-legality-static'}
 if note:d['note']=note
 return d

SPECIAL={
 483:[route('Temple of Sinnoh','story-legendary',65,('story','one-per-save'),'Dialga é encontrado durante a história principal.')],
 484:[route('Temple of Sinnoh','story-legendary',65,('story','one-per-save'),'Palkia é encontrado durante a história principal.')],
 493:[route('Temple of Sinnoh','legendary-capture',75,('complete-hisui-pokedex','one-per-save'),'Arceus é o encontro final após cumprir os requisitos da Pokédex de Hisui.')],
 480:[route('Lake Acuity','legendary-capture',70,('postgame','one-per-save'))],481:[route('Lake Verity','legendary-capture',70,('postgame','one-per-save'))],482:[route('Lake Valor','legendary-capture',70,('postgame','one-per-save'))],
 485:[route('Firespit Island','legendary-capture',70,('postgame','one-per-save'))],488:[route('Moonview Arena','legendary-capture',70,('postgame','one-per-save'))],486:[route('Snowpoint Temple','legendary-capture',70,('postgame','one-per-save'))],487:[route('Turnback Cave','legendary-capture',70,('postgame','one-per-save'))],
 641:[route('Alabaster Icelands','legendary-capture',70,('incarnate-forces-request','weather:blizzard','one-per-save'))],642:[route('Cobalt Coastlands','legendary-capture',70,('incarnate-forces-request','weather:thunderstorm','one-per-save'))],645:[route('Obsidian Fieldlands','legendary-capture',70,('incarnate-forces-request','one-per-save'))],905:[route('Crimson Mirelands','legendary-capture',70,('incarnate-forces-request','one-per-save'))],
 489:[route('Seaside Hollow','special-capture',33,('seas-legend-request',),'Phione aparece durante The Sea’s Legend.')],490:[route('Seaside Hollow','mythical-capture',50,('seas-legend-request','one-per-save'),'Manaphy aparece durante The Sea’s Legend.')],
 491:[route('Clamberclaw Cliffs','mythical-capture',70,('save-data:brilliant-diamond-or-shining-pearl','one-per-save'),'Darkrai requer dados salvos de Brilliant Diamond ou Shining Pearl para liberar o pedido.')],
 492:[route('Floaro Gardens','mythical-capture',70,('save-data:sword-or-shield','one-per-save'),'Shaymin requer dados salvos de Sword ou Shield para liberar o pedido.')],
 442:[route('Crimson Mirelands · Shrouded Ruins','static-encounter',60,('wisps:107','one-per-save'),'Spiritomb fica disponível após reunir os 107 wisps.')],
}

def load_data(text):
 m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
 if not m:raise ValueError('DATA payload not found')
 return json.loads(m.group(1))

def dedup_add(bucket,rec):
 key=(rec.get('location'),rec.get('method'),rec.get('levelMin'),rec.get('levelMax'),tuple(rec.get('conditions') or []),rec.get('provenance'))
 for x in bucket:
  if (x.get('location'),x.get('method'),x.get('levelMin'),x.get('levelMax'),tuple(x.get('conditions') or []),x.get('provenance'))==key:return False
 bucket.append(rec);return True

def main():
 data=load_data(OUT.read_text(encoding='utf-8'));pokemon=data.setdefault('pokemon',{});ids=hisui_ids()
 if len(ids)!=242:raise ValueError(f'Hisui dex size {len(ids)} != 242')
 ident,segs=parse_binlinker32(fetch(URL))
 if ident!=b'la':raise ValueError(f'unexpected ident {ident!r}')
 wild=0;touched=set()
 for seg in segs:
  for sid,rec in parse_area(seg):
   if sid not in ids:continue
   b=pokemon.setdefault(str(sid),{'encounters':[]})['encounters']
   if dedup_add(b,rec):wild+=1;touched.add(sid)
 special=0
 for sid,recs in SPECIAL.items():
  if sid not in ids:continue
  b=pokemon.setdefault(str(sid),{'encounters':[]})['encounters']
  for rec in recs:
   if dedup_add(b,dict(rec)):special+=1;touched.add(sid)
 covered=sorted(s for s in ids if (pokemon.get(str(s)) or {}).get('encounters'));missing=sorted(ids-set(covered))
 data.update({'version':'8.0-f9.1','source':str(data.get('source',''))+'+pkhex-legality-wild+pkhex-legality-static','dexSpecies':242,'coveredSpecies':len(covered),'missingSpecies':missing,'partialCoverage':bool(missing),'pkhexWildRoutesAdded':wild,'pkhexSpecialRoutesAdded':special,'pkhexSpeciesTouched':len(touched),'pkhexLegalityImport':True,'spaceTimeDistortionRoutes':True,'massOutbreakRoutes':True,'verifiedPlaSpecialRoutes':True})
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F9.1 Legends Arceus + PKHeX legality acquisition database */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8PlaEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexSpecies:DATA.dexSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,partialCoverage:DATA.partialCoverage,hisuiDex:true,pkhexLegalityImport:true,spaceTimeDistortionRoutes:true,massOutbreakRoutes:true,verifiedPlaSpecialRoutes:true,completeHisuiDex:DATA.missingSpecies.length===0,offline:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8');print(f'PLA F9.1 PKHeX: {len(covered)}/242; missing={len(missing)}; wild_routes={wild}; special_routes={special}; touched={len(touched)}');print('PLA F9.1 missing:',missing)
if __name__=='__main__':main()

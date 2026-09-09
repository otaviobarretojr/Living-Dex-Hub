#!/usr/bin/env python3
"""F8.1 — enrich BDSP acquisition provider using PKHeX legality resources.

PKHeX ships complete Brilliant Diamond/Shining Pearl wild encounter tables as
BinLinker32 resources. This importer decodes the four BD/SP overworld + Grand
Underground tables, merges them with our F8.0 provider, and adds verified static,
gift, fossil, NPC-trade, roaming and legendary routes represented in Encounters8b.
"""
from __future__ import annotations
import json,re,struct,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/bdsp-encounters-v8.js'
BASE='https://raw.githubusercontent.com/kwsch/PKHeX/master/PKHeX.Core/Resources/legality/wild/Gen8/'
FILES={
 'diamond': [('encounter_bd.pkl',False),('encounter_bd_underground.pkl',True)],
 'pearl': [('encounter_sp.pkl',False),('encounter_sp_underground.pkl',True)],
}
METHOD={1:'grass',2:'surf',3:'old-rod',4:'good-rod',5:'super-rod',6:'rock-smash',8:'honey-tree'}

def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/8.1 (+PKHeX-legality-import)'})
 with urllib.request.urlopen(req,timeout=30) as r:return r.read()

def parse_binlinker32(raw:bytes):
 if len(raw)<12:raise ValueError('short BinLinker')
 ident=raw[:2]
 count=struct.unpack_from('<H',raw,2)[0]
 offs=list(struct.unpack_from('<'+'I'*(count+1),raw,4))
 if count<=0 or offs[0]<4+4*(count+1):raise ValueError(('bad offsets',ident,count,offs[:2]))
 out=[]
 for i in range(count):
  a,b=offs[i],offs[i+1]
  if not (0<=a<=b<=len(raw)):raise ValueError('offset range')
  out.append(raw[a:b])
 return ident,out

def parse_area(seg:bytes,version:str,underground:bool):
 if len(seg)<4:return []
 loc=struct.unpack_from('<H',seg,0)[0];typ=seg[2]
 method='grand-underground' if underground else METHOD.get(typ,'wild-encounter')
 routes=[]
 for off in range(4,len(seg)-3,4):
  packed=struct.unpack_from('<H',seg,off)[0];form=(packed>>11)&0x1F;species=packed&0x3FF;lo=seg[off+2];hi=seg[off+3]
  if not species:continue
  cond=[]
  if form:cond.append(f'form:{form}')
  if underground:cond.append('grand-underground')
  routes.append((species,{
   'location':('Grand Underground' if underground else 'Sinnoh')+f' · área #{loc}',
   'method':method,'levelMin':int(lo),'levelMax':int(hi),'rate':None,
   'versions':[version],'conditions':cond,'provenance':'pkhex-legality-wild',
   'sourceLocationId':loc,'sourceSlotType':int(typ)
  }))
 return routes

def route(location,method,level,versions=('diamond','pearl'),conditions=(),note='',prov='pkhex-legality-static'):
 d={'location':location,'method':method,'levelMin':level,'levelMax':level,'rate':None,'versions':list(versions),'conditions':list(conditions),'provenance':prov}
 if note:d['note']=note
 return d

# Species/routes explicitly represented in PKHeX Encounters8b.cs.
SPECIAL={
 63:[route('Oreburgh City · troca NPC','npc-trade',9,note='Abra obtido por troca com NPC.')],
 129:[route('Snowpoint City · troca NPC','npc-trade',45,note='Magikarp obtido por troca com NPC.')],
 441:[route('Eterna City · troca NPC','npc-trade',15,note='Chatot obtido por troca com NPC.')],
 440:[route('Hearthome City · Ovo presente','gift-egg',1,conditions=('gift-egg',),note='Receba um Ovo de Happiny do viajante.')],
 447:[route('Iron Island · Riley','gift-egg',1,conditions=('gift-egg',),note='Receba um Ovo de Riolu de Riley.')],
 408:[route('Oreburgh Mining Museum','fossil-revival',1,conditions=('fossil:skull-fossil',),note='Reviva Cranidos a partir de Skull Fossil.')],
 410:[route('Oreburgh Mining Museum','fossil-revival',1,conditions=('fossil:armor-fossil',),note='Reviva Shieldon a partir de Armor Fossil.')],
 425:[route('Valley Windworks','static-encounter',22,conditions=('weekly-friday',),note='Encontro estático de Drifloon.')],
 442:[route('Hallowed Tower','static-encounter',25,conditions=('spiritomb-quest',),note='Encontro estático de Spiritomb após cumprir o requisito da Hallowed Tower.')],
 480:[route('Lake Acuity · Acuity Cavern','legendary-capture',50,conditions=('one-per-save',),note='Uxie, encontro lendário estático.')],
 481:[route('Sinnoh · roaming','roaming-legendary',50,conditions=('roaming','one-per-save'),note='Mesprit passa a vagar por Sinnoh após o evento no lago.')],
 482:[route('Lake Valor · Valor Cavern','legendary-capture',50,conditions=('one-per-save',),note='Azelf, encontro lendário estático.')],
 483:[route('Spear Pillar','legendary-capture',47,versions=('diamond',),conditions=('story','one-per-save'),note='Dialga é o lendário principal de Brilliant Diamond.')],
 484:[route('Spear Pillar','legendary-capture',47,versions=('pearl',),conditions=('story','one-per-save'),note='Palkia é o lendário principal de Shining Pearl.')],
 490:[route('Mystery Gift · bônus de lançamento','legacy-event',1,conditions=('expired-event:2022-02-21','trade-or-transfer-now'),note='O Ovo de Manaphy foi distribuído via Mystery Gift até 21/02/2022. Hoje, para um save novo, obtenha Manaphy por troca/transferência de uma cópia já existente.',prov='official-expired-event')],
}

def load_data(text):
 m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
 if not m:raise ValueError('DATA payload not found')
 return json.loads(m.group(1))

def dedup_add(bucket:list,rec:dict):
 key=(rec.get('location'),rec.get('method'),rec.get('levelMin'),rec.get('levelMax'),tuple(rec.get('versions') or []),tuple(rec.get('conditions') or []),rec.get('provenance'))
 for x in bucket:
  k=(x.get('location'),x.get('method'),x.get('levelMin'),x.get('levelMax'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []),x.get('provenance'))
  if k==key:return False
 bucket.append(rec);return True

def main():
 text=OUT.read_text(encoding='utf-8');data=load_data(text);pokemon=data.setdefault('pokemon',{})
 sinnoh=set(str(x) for x in data.get('sinnohSpecies',[]) or [])
 if not sinnoh:
  # F8.0 payload tracks missing + covered but not membership; reconstruct from embedded dex pack.
  pack=json.loads((ROOT/'data/embedded-dex-pack.json').read_text(encoding='utf-8'))
  entries=(pack.get('dexes') or {}).get('bdsp:sinnoh') or []
  sinnoh={str(int((e.get('species') if isinstance(e,dict) else e))) for e in entries}
 added_species=set();wild_routes=0;failures=[]
 for version,items in FILES.items():
  for filename,underground in items:
   try:
    ident,segs=parse_binlinker32(fetch(BASE+filename))
    if ident!=b'bs':raise ValueError(f'unexpected ident {ident!r}')
    for seg in segs:
     for sid,rec in parse_area(seg,version,underground):
      k=str(sid)
      if k not in sinnoh:continue
      bucket=pokemon.setdefault(k,{'encounters':[]})['encounters']
      if dedup_add(bucket,rec):wild_routes+=1;added_species.add(k)
   except Exception as e:failures.append(f'{filename}: {e}')
 special_routes=0
 for sid,recs in SPECIAL.items():
  k=str(sid)
  if k not in sinnoh:continue
  bucket=pokemon.setdefault(k,{'encounters':[]})['encounters']
  for rec in recs:
   if dedup_add(bucket,dict(rec)):special_routes+=1;added_species.add(k)
 covered=sorted(int(k) for k,v in pokemon.items() if k in sinnoh and (v.get('encounters') or []))
 missing=sorted(int(k) for k in sinnoh if not (pokemon.get(k) or {}).get('encounters'))
 data.update({
  'version':'8.0-f8.1','source':str(data.get('source',''))+'+pkhex-legality-wild+pkhex-legality-static+official-manaphy-event',
  'dexSpecies':151,'coveredSpecies':len(covered),'missingSpecies':missing,'partialCoverage':bool(missing),
  'pkhexWildRoutesAdded':wild_routes,'pkhexSpecialRoutesAdded':special_routes,
  'pkhexSpeciesAddedCount':len(added_species),'pkhexImportFailures':failures,
  'pkhexLegalityImport':True,'grandUndergroundRoutes':True,'verifiedBdspSpecialRoutes':True,
 })
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F8.1 BDSP + PKHeX legality acquisition database */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8BdspEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexSpecies:DATA.dexSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,offline:true,versionSpecific:true,indirectAcquisition:true,pkhexLegalityImport:true,grandUndergroundRoutes:true,verifiedBdspSpecialRoutes:true,completeSinnohDex:DATA.missingSpecies.length===0})};\n})();\n"
 OUT.write_text(js,encoding='utf-8')
 print(f"BDSP F8.1 PKHeX: {len(covered)}/151; missing={len(missing)}; wild_routes={wild_routes}; special_routes={special_routes}; species_touched={len(added_species)}; failures={len(failures)}")
 if missing:print('BDSP F8.1 missing:',missing)
 return 0
if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""F11.0 — build Pokémon Legends: Z-A acquisition provider from PKHeX legality data.

Sources:
- encounter_za.pkl: Lumiose standard encounters
- encounter_hyperspace_za.pkl: Mega Dimension / Hyperspace encounters
- Encounters9a.cs: gifts and static/story/special encounters
- local offline evolution core: evolution-only routes when the prerequisite is obtainable

Dex membership comes only from embedded-dex-pack.json and is never inferred from acquisition data.
"""
from __future__ import annotations
import json,re,struct,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'data/embedded-dex-pack.json'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
OUT=ROOT/'app/src/main/assets/za-encounters-v8.js'
BASE='https://raw.githubusercontent.com/kwsch/PKHeX/master/'
URL_LUMIOSE=BASE+'PKHeX.Core/Resources/legality/wild/Gen9/encounter_za.pkl'
URL_HYPER=BASE+'PKHeX.Core/Resources/legality/wild/Gen9/encounter_hyperspace_za.pkl'
URL_STATIC=BASE+'PKHeX.Core/Legality/Encounters/Data/Gen9/Encounters9a.cs'


def fetch(url,binary=True):
 req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub/11.0 (+PKHeX-legality-import)'})
 with urllib.request.urlopen(req,timeout=40) as r:
  b=r.read()
 return b if binary else b.decode('utf-8')

def parse_binlinker16(raw):
 if len(raw)<8:raise ValueError('short BinLinker16')
 ident=raw[:2];count=struct.unpack_from('<H',raw,2)[0]
 offs=list(struct.unpack_from('<'+'H'*(count+1),raw,4))
 if count<=0 or len(offs)!=count+1:raise ValueError(('bad count',count))
 if offs[0] < 4+2*(count+1):raise ValueError(('bad first offset',offs[0]))
 return ident,[raw[offs[i]:offs[i+1]] for i in range(count)]

def parse_area(seg,scope,method):
 if len(seg)<4:return []
 loc=struct.unpack_from('<H',seg,0)[0];body=seg[4:];out=[]
 for off in range(0,len(body)-7,8):
  species=struct.unpack_from('<H',body,off)[0];form=body[off+2];gender=body[off+3];lo=body[off+4];hi=body[off+5];alpha=body[off+6];shiny=body[off+7]
  if not species:continue
  cond=[]
  if form:cond.append(f'form:{form}')
  if gender not in (0,1,2,255):cond.append(f'gender:{gender}')
  if alpha:cond.append('alpha')
  if shiny:cond.append(f'shiny-rule:{shiny}')
  out.append((species,{'location':('Hyperspace Lumiose' if scope=='hyperspace' else 'Lumiose City')+f' · #{loc}','method':method,'levelMin':int(lo),'levelMax':int(hi),'rate':None,'versions':['za'],'conditions':cond,'provenance':'pkhex-legality-wild','dexScope':scope,'sourceLocation':loc,'sourceForm':int(form)}))
 return out

def scope_ids():
 p=json.loads(PACK.read_text(encoding='utf-8'))['dexes']
 lum=[int(x[0]) for x in p['za:lumiose']];hyp=[int(x[0]) for x in p['za:hyperspace']]
 if len(lum)!=232 or len(hyp)!=132:raise ValueError((len(lum),len(hyp)))
 return set(lum),set(hyp)

def dex_scopes(sid,lum,hyp):
 a=[]
 if sid in lum:a.append('lumiose')
 if sid in hyp:a.append('hyperspace')
 return a

def route(location,method,level,conditions=(),provenance='pkhex-legality-static',note=''):
 d={'location':location,'method':method,'levelMin':int(level),'levelMax':int(level),'rate':None,'versions':['za'],'conditions':list(conditions),'provenance':provenance}
 if note:d['note']=note
 return d

def parse_static_source(text):
 # Parse the compact constructor pattern used by EncounterGift9a / EncounterStatic9a.
 # Species, form and level are positional: new(species,form,level,size) {...} // Name
 out=[];section='special'
 for line in text.splitlines():
  z=line.strip()
  if 'internal static readonly EncounterGift9a[] Gifts' in z:section='gift';continue
  if 'internal static readonly EncounterStatic9a[] Static' in z:section='static';continue
  m=re.search(r'new\((\d+),(\d+),(\d+),(\d+)\)\s*\{([^}]*)\}',z)
  if not m:continue
  sid,form,lvl,size=map(int,m.group(1,2,3,4));body=m.group(5)
  lm=re.search(r'Location\s*=\s*(\d+)',body);loc=int(lm.group(1)) if lm else 0
  cond=[]
  if form:cond.append(f'form:{form}')
  if 'IsAlpha = true' in body:cond.append('alpha')
  if 'Shiny = Never' in body:cond.append('shiny-locked')
  elif 'Shiny = Always' in body:cond.append('shiny-guaranteed')
  method='gift' if section=='gift' else 'static-encounter'
  note=''
  cm=re.search(r'//\s*(.+)$',z)
  if cm:note=cm.group(1).strip()
  out.append((sid,route(('Lumiose/Hyperspace special encounter' if not loc else f'Z-A location #{loc}'),method,lvl,cond,note=note)))
 return out

def dedup_add(bucket,rec):
 key=(rec.get('location'),rec.get('method'),rec.get('levelMin'),rec.get('levelMax'),tuple(rec.get('conditions') or []),rec.get('provenance'))
 for x in bucket:
  k=(x.get('location'),x.get('method'),x.get('levelMin'),x.get('levelMax'),tuple(x.get('conditions') or []),x.get('provenance'))
  if k==key:return False
 bucket.append(rec);return True

def evolution_route(sid,node):
 parent=int(node.get('evolvesFrom') or 0)
 if not parent:return None
 details=node.get('evolutionDetails') or []
 cond=[f'from:{parent}']
 if details:
  d=details[0] or {}
  for k,v in d.items():
   if v in (None,False,'',0):continue
   if k=='trigger':cond.append(str(v))
   else:cond.append(f'{k.replace("_","-")}:{str(v).lower() if isinstance(v,bool) else v}')
 return route('Evolução em Pokémon Legends: Z-A','evolve',0,cond,'offline-evolution-core')

def main():
 lum,hyp=scope_ids();union=lum|hyp
 pokemon={str(s):{'dexScopes':dex_scopes(s,lum,hyp),'encounters':[]} for s in sorted(union)}
 wild=0
 for url,scope,method in ((URL_LUMIOSE,'lumiose','wild-encounter'),(URL_HYPER,'hyperspace','hyperspace-encounter')):
  ident,segs=parse_binlinker16(fetch(url))
  if ident!=b'za':raise ValueError((url,ident))
  for seg in segs:
   for sid,rec in parse_area(seg,scope,method):
    if sid not in union:continue
    if dedup_add(pokemon[str(sid)]['encounters'],rec):wild+=1
 special=0
 for sid,rec in parse_static_source(fetch(URL_STATIC,False)):
  if sid not in union:continue
  if dedup_add(pokemon[str(sid)]['encounters'],rec):special+=1
 # Evolution closure: repeatedly add an evolution route if the direct prerequisite already has a route.
 core=json.loads(CORE.read_text(encoding='utf-8')).get('pokemon',{})
 evo=0;changed=True
 while changed:
  changed=False
  for sid in sorted(union):
   b=pokemon[str(sid)]['encounters']
   if b:continue
   node=core.get(str(sid)) or {};parent=int(node.get('evolvesFrom') or 0)
   if parent and parent in union and pokemon.get(str(parent),{}).get('encounters'):
    rec=evolution_route(sid,node)
    if rec and dedup_add(b,rec):evo+=1;changed=True
 covered=sorted(s for s in union if pokemon[str(s)]['encounters']);missing=sorted(union-set(covered))
 lum_cov=sum(bool(pokemon[str(s)]['encounters']) for s in lum);hyp_cov=sum(bool(pokemon[str(s)]['encounters']) for s in hyp)
 data={'version':'8.0-f11.0','gameId':'za','label':'Pokémon Legends: Z-A','source':'PKHeX Gen9a legality encounter_za + encounter_hyperspace_za + Encounters9a + offline evolution core','dexes':{'lumiose':{'size':232,'covered':lum_cov},'hyperspace':{'size':132,'covered':hyp_cov}},'uniqueTrackedSpecies':len(union),'coveredSpecies':len(covered),'missingSpecies':missing,'partialCoverage':bool(missing),'pkhexWildRoutesAdded':wild,'pkhexSpecialRoutesAdded':special,'evolutionRoutesAdded':evo,'pkhexLegalityImport':True,'lumioseDex':True,'hyperspaceDex':True,'megaDimensionDlc':True,'threeSixtyFourAvailableSpecies':len(union)==364,'pokemon':pokemon}
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F11.0 Legends Z-A acquisition provider */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8ZaEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,lumiose:DATA.dexes.lumiose,hyperspace:DATA.dexes.hyperspace,tracked:DATA.coveredSpecies,total:DATA.uniqueTrackedSpecies,missingSpecies:DATA.missingSpecies,pkhexLegalityImport:true,megaDimensionDlc:true,offline:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8')
 print(f"ZA F11.0: lumiose={lum_cov}/232; hyperspace={hyp_cov}/132; union={len(covered)}/{len(union)}; wild_routes={wild}; special={special}; evolutions={evo}; missing={len(missing)}")
 print('ZA F11.0 missing:',missing)
if __name__=='__main__':main()

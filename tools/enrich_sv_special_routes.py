#!/usr/bin/env python3
"""F10.1 — verified Scarlet/Violet special acquisition routes.

Closes tracked dex species not represented by the generic wild table. Limited
raid-event species are explicitly classified as legacy/event acquisition so the
app never presents them as permanently catchable in a fresh save.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/sv-encounters-v8.js'

def route(location,method,versions=('scarlet','violet'),conditions=(),note='',prov='verified-sv-special'):
 d={'location':location,'method':method,'levelMin':0,'levelMax':0,'rate':None,'versions':list(versions),'conditions':list(conditions),'provenance':prov}
 if note:d['note']=note
 return d

SPECIAL={
 442:[route('Paldea · encontro estático','static-encounter',conditions=('fixed-spawn',),note='Spiritomb possui encontros estáticos em Paldea.')],
 999:[route('Paldea · torres e ruínas','static-encounter',conditions=('chest-form',),note='Gimmighoul Forma Baú aparece em pontos estáticos de Paldea.')],
 1007:[route('Area Zero · pós-jogo','legendary-capture',versions=('scarlet',),conditions=('postgame','one-per-save'),note='Uma segunda Koraidon capturável fica disponível em Scarlet após a história principal.')],
 1008:[route('Area Zero · pós-jogo','legendary-capture',versions=('violet',),conditions=('postgame','one-per-save'),note='Uma segunda Miraidon capturável fica disponível em Violet após a história principal.')],
 1009:[route('Tera Raid Battle · evento limitado','legacy-event-raid',conditions=('limited-event','trade-or-transfer-now'),note='Walking Wake foi distribuído por eventos de Tera Raid. Fora de uma janela ativa, obtenha por troca ou transferência.',prov='official-limited-event')],
 1010:[route('Tera Raid Battle · evento limitado','legacy-event-raid',conditions=('limited-event','trade-or-transfer-now'),note='Iron Leaves foi distribuído por eventos de Tera Raid. Fora de uma janela ativa, obtenha por troca ou transferência.',prov='official-limited-event')],
 1020:[route('The Indigo Disk · missão de Perrin','special-capture',versions=('scarlet',),conditions=('indigo-disk','perrin-quest','version-exclusive','one-per-save'),note='Gouging Fire é obtido em Scarlet pela linha de missão de Perrin.')],
 1021:[route('The Indigo Disk · missão de Perrin','special-capture',versions=('scarlet',),conditions=('indigo-disk','perrin-quest','version-exclusive','one-per-save'),note='Raging Bolt é obtido em Scarlet pela linha de missão de Perrin.')],
 1022:[route('The Indigo Disk · missão de Perrin','special-capture',versions=('violet',),conditions=('indigo-disk','perrin-quest','version-exclusive','one-per-save'),note='Iron Boulder é obtido em Violet pela linha de missão de Perrin.')],
 1023:[route('The Indigo Disk · missão de Perrin','special-capture',versions=('violet',),conditions=('indigo-disk','perrin-quest','version-exclusive','one-per-save'),note='Iron Crown é obtido em Violet pela linha de missão de Perrin.')],
 1024:[route('The Indigo Disk · história','story-capture',conditions=('indigo-disk','story','one-per-save'),note='Terapagos é capturado durante a história de The Indigo Disk.')],
 1025:[route('Mochi Mayhem · epílogo','story-capture',conditions=('epilogue','mythical-pecha-berry','one-per-save'),note='Pecharunt é capturado no epílogo Mochi Mayhem após iniciar o evento correspondente.')],
}

def load(text):
 m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
 if not m:raise ValueError('SV DATA missing')
 return json.loads(m.group(1))

def add(bucket,rec):
 key=(rec['location'],rec['method'],tuple(rec['versions']),tuple(rec['conditions']),rec['provenance'])
 for x in bucket:
  if (x.get('location'),x.get('method'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []),x.get('provenance'))==key:return False
 bucket.append(rec);return True

def main():
 text=OUT.read_text(encoding='utf-8');d=load(text);pokemon=d.setdefault('pokemon',{});added=0
 for sid,recs in SPECIAL.items():
  k=str(sid);bucket=pokemon.setdefault(k,{'encounters':[]})['encounters']
  for r in recs:
   if add(bucket,dict(r)):added+=1
 # retain dexScopes by deriving from existing metadata is impossible after a missing seed;
 # reconstruct from embedded dex pack for any newly added species.
 pack=json.loads((ROOT/'data/embedded-dex-pack.json').read_text(encoding='utf-8'))
 mapping={'paldea':'sv:paldea','kitakami':'sv:kitakami','blueberry':'sv:blueberry'}
 sets={n:{int(x[0] if isinstance(x,list) else x.get('species')) for x in (pack.get('dexes') or {}).get(key,[])} for n,key in mapping.items()}
 for sid in SPECIAL:
  if str(sid) in pokemon:pokemon[str(sid)]['dexScopes']=[n for n,s in sets.items() if sid in s]
 union=set().union(*sets.values())
 coverage={n:sum(1 for p in ids if (pokemon.get(str(p)) or {}).get('encounters')) for n,ids in sets.items()}
 missing=sorted(p for p in union if not (pokemon.get(str(p)) or {}).get('encounters'))
 d.update({'version':'8.0-f10.1','source':str(d.get('source',''))+'+verified-sv-specials','coveredSpecies':len(union)-len(missing),'missingSpecies':missing,'dexes':{n:{'size':len(sets[n]),'covered':coverage[n]} for n in sets},'verifiedSpecialRoutes':added,'eventAvailabilityAware':True,'versionExclusiveDlcParadox':True})
 payload=json.dumps(d,ensure_ascii=False,separators=(',',':'))
 js="/* Living Dex Hub — F10.1 Scarlet/Violet complete acquisition provider */\n(()=>{'use strict';\nconst DATA="+payload+";\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SvEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,dexes:DATA.dexes,uniqueTrackedSpecies:DATA.uniqueTrackedSpecies,coveredSpecies:DATA.coveredSpecies,missingSpecies:DATA.missingSpecies,pkhexLegalityImport:true,threeDexScopes:true,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,eventAvailabilityAware:true,versionExclusiveDlcParadox:true,offline:true})};\n})();\n"
 OUT.write_text(js,encoding='utf-8')
 print(f"SV F10.1 specials: paldea={coverage['paldea']}/400, kitakami={coverage['kitakami']}/200, blueberry={coverage['blueberry']}/243; union={len(union)-len(missing)}/{len(union)}; missing={len(missing)}; added={added}")
 if missing:print('SV F10.1 missing:',missing)
if __name__=='__main__':main()

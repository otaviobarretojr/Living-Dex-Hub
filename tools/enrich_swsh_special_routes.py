#!/usr/bin/env python3
"""F7.5 — enrich Sword/Shield DLC acquisition data with verified special routes.

F7.4 already covers ordinary encounters, evolution routes and dex scopes. This stage
fills mechanics that are not represented as standard encounter rows: Isle of Armor
gifts, Crown Tundra story choices, static legendaries and Dynamax Adventures bosses.
"""
from __future__ import annotations

import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/swsh-encounters-v8.js'


def read_data():
    text=OUT.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise RuntimeError('Sword/Shield DATA payload not found')
    return json.loads(m.group(1))


def route(location,method,level=0,versions=('sword','shield'),conditions=(),note=''):
    return {
        'location':location,'method':method,'levelMin':level,'levelMax':level,
        'rate':None,'versions':list(versions),'conditions':list(conditions),
        'provenance':'verified-dlc-game-mechanic','note':note,
    }

# Mechanics documented by the games but not represented by ordinary encounter data.
SPECIAL={
    # Isle of Armor gifts / story.
    1:[route('Master Dojo','gift',5,conditions=('isle-of-armor','choose-one-dojo-starter'),note='Após o primeiro desafio do Dojo, escolha Bulbasaur ou Squirtle; apenas um é recebido neste save.')],
    7:[route('Master Dojo','gift',5,conditions=('isle-of-armor','choose-one-dojo-starter'),note='Após o primeiro desafio do Dojo, escolha Bulbasaur ou Squirtle; apenas um é recebido neste save.')],
    137:[route('Master Dojo','gift',25,conditions=('isle-of-armor','complete-final-dojo-trial'),note='Receba Porygon de Hyde após concluir o desafio final do Master Dojo.')],
    891:[route('Master Dojo','gift',10,conditions=('isle-of-armor','complete-mustard-trials'),note='Mustard entrega Kubfu após você concluir os desafios principais do Master Dojo.')],
    892:[route('Tower of Darkness / Tower of Waters','evolution',0,conditions=('isle-of-armor','from:891','choose-one-tower'),note='Evolua Kubfu ao concluir uma das duas torres. A torre escolhida define a forma de Urshifu.')],
    893:[route('Evento / Pokémon HOME','transfer',0,conditions=('isle-of-armor','external-event'),note='Zarude não possui captura normal em Sword/Shield; requer exemplar obtido por distribuição/evento e transferência compatível.')],

    # Crown Tundra story and static encounters.
    898:[route('Crown Shrine','legendary-capture',80,conditions=('crown-tundra','calyrex-story','champion-required','one-per-save'),note='Conclua a história de Calyrex e capture a forma fundida no Crown Shrine; depois ela pode ser separada com Reins of Unity.')],
    896:[route('Crown Shrine','legendary-capture',75,conditions=('crown-tundra','calyrex-story','choose-icy-carrot','one-steed-per-save'),note='Escolha a Iceroot Carrot durante a história de Calyrex para obter Glastrier.')],
    897:[route('Crown Shrine','legendary-capture',75,conditions=('crown-tundra','calyrex-story','choose-shaderoot-carrot','one-steed-per-save'),note='Escolha a Shaderoot Carrot durante a história de Calyrex para obter Spectrier.')],
    894:[route('Split-Decision Ruins','legendary-capture',70,conditions=('crown-tundra','requires-regirock-regice-registeel','choose-one-new-regi','one-per-save'),note='Depois dos três Regis clássicos, escolha o padrão de Regieleki ou Regidrago; apenas um dos dois pode ser capturado neste save.')],
    895:[route('Split-Decision Ruins','legendary-capture',70,conditions=('crown-tundra','requires-regirock-regice-registeel','choose-one-new-regi','one-per-save'),note='Depois dos três Regis clássicos, escolha o padrão de Regieleki ou Regidrago; apenas um dos dois pode ser capturado neste save.')],
    486:[route("Giant's Bed · Raid Den",'max-raid',100,conditions=('crown-tundra','requires-all-five-regis'),note='Leve Regirock, Regice, Registeel, Regieleki e Regidrago no time e interaja com o Raid Den especial em Giant’s Bed.')],
    144:[route('The Crown Tundra','legendary-capture',70,conditions=('crown-tundra','galarian-form','legendary-tree-story'),note='Galarian Articuno percorre a Crown Tundra e usa miragens; interaja com o correto para iniciar a batalha.')],
    145:[route('Wild Area','legendary-capture',70,conditions=('crown-tundra','galarian-form','legendary-tree-story'),note='Galarian Zapdos corre pelo Wild Area após a cena da Legendary Tree; alcance-o para iniciar a batalha.')],
    146:[route('Isle of Armor','legendary-capture',70,conditions=('crown-tundra','galarian-form','legendary-tree-story'),note='Galarian Moltres circula a Isle of Armor após a cena da Legendary Tree; antecipe a rota para iniciar a batalha.')],
    638:[route('Frigid Sea','legendary-capture',70,conditions=('crown-tundra','collect-footprints'),note='Colete evidências/pegadas de Cobalion com Sonia e depois encontre-o no Frigid Sea.')],
    639:[route('Lakeside Cave','legendary-capture',70,conditions=('crown-tundra','collect-footprints'),note='Colete evidências/pegadas de Terrakion com Sonia e depois encontre-o em Lakeside Cave.')],
    640:[route("Giant's Bed",'legendary-capture',70,conditions=('crown-tundra','collect-footprints'),note='Colete evidências/pegadas de Virizion com Sonia e depois encontre-o em Giant’s Bed.')],
    647:[route('Ballimere Lake','legendary-capture',65,conditions=('crown-tundra','requires-cobalion-terrakion-virizion','make-curry'),note='Com Cobalion, Terrakion e Virizion no grupo, faça curry na pequena ilha de Ballimere Lake para fazer Keldeo aparecer.')],
    789:[route('Freezington','gift',5,conditions=('crown-tundra','calyrex-story-progress'),note='Após proteger Freezington durante a história de Calyrex, receba Cosmog da moradora que cuida de “Fwoofy”.')],
    803:[route('Max Lair','gift',20,conditions=('crown-tundra','ultra-beast-story','catch-five-ultra-beasts'),note='Após iniciar a história das Ultra Beasts e capturar cinco delas em Dynamax Adventures, Poipole aparece como presente no Max Lair.')],
}

# Final bosses available through Dynamax Adventures. "Native" version exclusives keep
# their real Sword/Shield restriction so the existing version-aware ranking stays useful.
DA_BOTH={150,243,244,245,377,378,379,384,480,481,482,485,487,488,645,646,718,785,786,787,788,793,794,795,796,797,798,799,800,805,806}
DA_SWORD={250,381,383,483,641,643,716,791}
DA_SHIELD={249,380,382,484,642,644,717,792}


def add_once(records,rec):
    sig=(rec['location'],rec['method'],tuple(rec['versions']),tuple(rec['conditions']))
    for x in records:
        if (x.get('location'),x.get('method'),tuple(x.get('versions') or []),tuple(x.get('conditions') or []))==sig:return False
    records.append(rec);return True


def main():
    data=read_data();pokemon=data.setdefault('pokemon',{})
    union=set()
    for d in (data.get('dexes') or {}).values():
        # Membership is reconstructed from per-Pokémon dexScopes below; union here only
        # controls special records to avoid adding unrelated species to this provider.
        pass
    union={int(pid) for pid,p in pokemon.items() if p.get('dexScopes')}
    # F7.4 can leave species with no payload at all. Special species are allowed only if
    # their National ID is within one of the validated Sword/Shield dex scopes. Rebuild
    # membership from the embedded dex pack if needed.
    pack_path=ROOT/'data/embedded-dex-pack.json'
    scope_map={'galar':'swsh:galar','isle-of-armor':'swsh:isle-of-armor','crown-tundra':'swsh:crown-tundra'}
    scopes={}
    if pack_path.exists():
        pack=json.loads(pack_path.read_text(encoding='utf-8'))
        for scope,key in scope_map.items():scopes[scope]={int(r[0]) for r in (pack.get('dexes') or {}).get(key,[]) if isinstance(r,list) and r}
        union=set().union(*scopes.values())
    else:
        scopes={s:set() for s in scope_map}

    added=0;special_added=0;da_added=0
    for pid,recs in SPECIAL.items():
        if pid not in union:continue
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        if scopes:p['dexScopes']=[s for s in scope_map if pid in scopes[s]]
        for rec in recs:
            if add_once(p.setdefault('encounters',[]),rec):added+=1;special_added+=1

    for pid in sorted(DA_BOTH|DA_SWORD|DA_SHIELD):
        if pid not in union:continue
        versions=('sword',) if pid in DA_SWORD else ('shield',) if pid in DA_SHIELD else ('sword','shield')
        rec=route('Max Lair · Dynamax Adventures','dynamax-adventure',70,versions=versions,conditions=('crown-tundra','dynamax-adventures','final-boss','one-capture-per-species'),note='Chefe final de Dynamax Adventures. Após capturar uma espécie lendária e levá-la, essa mesma espécie não pode ser capturada novamente nesse save.')
        p=pokemon.setdefault(str(pid),{'encounters':[]})
        if scopes:p['dexScopes']=[s for s in scope_map if pid in scopes[s]]
        if add_once(p.setdefault('encounters',[]),rec):added+=1;da_added+=1

    dexes={}
    for scope,ids in scopes.items():
        covered=sorted(pid for pid in ids if (pokemon.get(str(pid),{}).get('encounters') or []))
        dexes[scope]={'dexSpecies':len(ids),'coveredSpecies':len(covered),'missingSpecies':sorted(ids-set(covered))}
    covered_union=sorted(pid for pid in union if (pokemon.get(str(pid),{}).get('encounters') or []))

    data.update({
        'version':'8.0-f7.5',
        'source':str(data.get('source',''))+'+verified-dlc-special-routes+dynamax-adventures',
        'dexes':dexes,
        'uniqueSwordShieldSpecies':len(union),
        'coveredSpecies':len(covered_union),
        'missingSpecies':sorted(union-set(covered_union)),
        'verifiedDlcSpecialRoutes':special_added,
        'dynamaxAdventureRoutes':da_added,
    })
    js="""/* Living Dex Hub — F7.5 verified Sword/Shield DLC special acquisition routes */\n(()=>{'use strict';\nconst DATA=%s;\nfunction get(id){return DATA.pokemon[String(Number(id)||0)]||null}\nfunction byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}\nwindow.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,source:DATA.source,dexSpecies:DATA.dexSpecies,dexes:DATA.dexes,uniqueSwordShieldSpecies:DATA.uniqueSwordShieldSpecies,pokemonCount:Object.keys(DATA.pokemon).length,missingSpecies:DATA.missingSpecies,exclusiveDirectSpecies:DATA.exclusiveDirectSpecies,specialEvolutionRoutes:DATA.specialEvolutionRoutes,verifiedSpecialRoutes:DATA.verifiedSpecialRoutes,verifiedDlcSpecialRoutes:DATA.verifiedDlcSpecialRoutes,dynamaxAdventureRoutes:DATA.dynamaxAdventureRoutes,offline:true,versionSpecific:true,provenance:true,indirectAcquisition:true,exclusiveTradeRoutes:true,richEvolutionConditions:true,verifiedSpecialAcquisition:true,threeDexScopes:true,dlcDexScopes:true,verifiedDlcSpecialAcquisition:true,dynamaxAdventures:true})};\n})();\n""" % json.dumps(data,ensure_ascii=False,separators=(',',':'))
    OUT.write_text(js,encoding='utf-8')
    print('Sword/Shield F7.5 special routes: '+', '.join(f"{s}={d['coveredSpecies']}/{d['dexSpecies']}" for s,d in dexes.items())+f"; union={data['coveredSpecies']}/{data['uniqueSwordShieldSpecies']}; special={special_added}; dynamax={da_added}; added_routes={added}")
    return 0

if __name__=='__main__':raise SystemExit(main())

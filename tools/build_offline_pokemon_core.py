#!/usr/bin/env python3
from pathlib import Path
import csv, io, json, time, urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
BASE='https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/'
FILES=['pokemon.csv','pokemon_species.csv','pokemon_species_names.csv','pokemon_species_flavor_text.csv','pokemon_stats.csv','stats.csv','pokemon_types.csv','types.csv','pokemon_abilities.csv','abilities.csv','languages.csv','generations.csv','pokemon_habitats.csv','growth_rates.csv','pokemon_egg_groups.csv','egg_groups.csv','pokemon_evolution.csv','evolution_triggers.csv','items.csv','locations.csv','moves.csv','versions.csv']

def fetch(name):
    url=BASE+name
    err=None
    for n in range(4):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'LivingDexHub-offline-builder/1.0'})
            with urllib.request.urlopen(req,timeout=45) as r:
                return r.read().decode('utf-8-sig')
        except Exception as e:
            err=e; time.sleep(1.5*(n+1))
    raise RuntimeError(f'Falha ao baixar {name}: {err}')

def rows(text): return list(csv.DictReader(io.StringIO(text)))
def i(v):
    try:return int(v)
    except:return None
def b(v): return str(v).strip() in ('1','true','True','TRUE')
def idmap(rs,key='id',value='identifier'):
    return {i(r.get(key)):r.get(value,'') for r in rs if i(r.get(key)) is not None}

def main():
    data={name:rows(fetch(name)) for name in FILES}
    langs=idmap(data['languages.csv']); versions=idmap(data['versions.csv']); gens=idmap(data['generations.csv'])
    habitats=idmap(data['pokemon_habitats.csv']); growth=idmap(data['growth_rates.csv']); stats=idmap(data['stats.csv'])
    types=idmap(data['types.csv']); abilities=idmap(data['abilities.csv']); eggs=idmap(data['egg_groups.csv'])
    triggers=idmap(data['evolution_triggers.csv']); items=idmap(data['items.csv']); locations=idmap(data['locations.csv']); moves=idmap(data['moves.csv'])

    pokemon_rows={}
    pokemon_species_to_pid={}
    for r in data['pokemon.csv']:
        sid=i(r.get('species_id')); pid=i(r.get('id'))
        if not sid or not pid or sid>1025: continue
        if b(r.get('is_default')) or sid not in pokemon_species_to_pid:
            pokemon_species_to_pid[sid]=pid; pokemon_rows[pid]=r

    species={i(r.get('id')):r for r in data['pokemon_species.csv'] if i(r.get('id')) and i(r.get('id'))<=1025}
    result={str(sid):{'id':sid} for sid in range(1,1026)}

    # Portuguese genus/category.
    genus={}
    for r in data['pokemon_species_names.csv']:
        sid=i(r.get('pokemon_species_id')); lid=i(r.get('local_language_id')); lang=(langs.get(lid) or '').lower()
        if sid and sid<=1025 and lang in ('pt-br','pt') and r.get('genus'):
            # Prefer pt-BR when both are present.
            if sid not in genus or lang=='pt-br': genus[sid]=r.get('genus','')

    # Official Portuguese flavor text keyed by species and version identifier.
    flavors={}
    for r in data['pokemon_species_flavor_text.csv']:
        sid=i(r.get('species_id') or r.get('pokemon_species_id')); lid=i(r.get('language_id')); vid=i(r.get('version_id'))
        lang=(langs.get(lid) or '').lower(); ver=versions.get(vid,'')
        if not sid or sid>1025 or lang not in ('pt-br','pt') or not ver: continue
        txt=' '.join((r.get('flavor_text') or '').replace('\f',' ').replace('\n',' ').split())
        if not txt: continue
        flavors.setdefault(sid,{})[ver]={'text':txt,'lang':lang}

    # Per default Pokemon stats/types/ability.
    stat_by_pid={}; type_by_pid={}; ability_by_pid={}
    for r in data['pokemon_stats.csv']:
        pid=i(r.get('pokemon_id')); sid=i(r.get('stat_id')); val=i(r.get('base_stat'))
        if pid in pokemon_rows and sid and val is not None: stat_by_pid.setdefault(pid,[]).append((sid,val))
    for r in data['pokemon_types.csv']:
        pid=i(r.get('pokemon_id')); tid=i(r.get('type_id')); slot=i(r.get('slot')) or 99
        if pid in pokemon_rows and tid: type_by_pid.setdefault(pid,[]).append((slot,tid))
    for r in data['pokemon_abilities.csv']:
        pid=i(r.get('pokemon_id')); aid=i(r.get('ability_id')); slot=i(r.get('slot')) or 99
        if pid in pokemon_rows and aid and not b(r.get('is_hidden')): ability_by_pid.setdefault(pid,[]).append((slot,aid))

    egg_by_species={}
    for r in data['pokemon_egg_groups.csv']:
        sid=i(r.get('species_id')); eid=i(r.get('egg_group_id'))
        if sid and sid<=1025 and eid: egg_by_species.setdefault(sid,[]).append(eid)

    evo_detail={}
    for r in data['pokemon_evolution.csv']:
        child=i(r.get('evolved_species_id'))
        if not child or child>1025: continue
        d={'trigger':triggers.get(i(r.get('evolution_trigger_id')),''),'min_level':i(r.get('minimum_level')),
           'item':items.get(i(r.get('trigger_item_id')),''),'held_item':items.get(i(r.get('held_item_id')),''),
           'known_move':moves.get(i(r.get('known_move_id')),''),'known_move_type':types.get(i(r.get('known_move_type_id')),''),
           'location':locations.get(i(r.get('location_id')),''),'min_happiness':i(r.get('minimum_happiness')),
           'min_beauty':i(r.get('minimum_beauty')),'min_affection':i(r.get('minimum_affection')),
           'time_of_day':r.get('time_of_day') or '', 'gender':i(r.get('gender_id')),
           'relative_physical_stats':i(r.get('relative_physical_stats')),
           'needs_overworld_rain':b(r.get('needs_overworld_rain')),'turn_upside_down':b(r.get('turn_upside_down'))}
        evo_detail.setdefault(child,[]).append(d)

    for sid in range(1,1026):
        s=species.get(sid,{}) ; pid=pokemon_species_to_pid.get(sid); p=pokemon_rows.get(pid,{})
        ts=[types.get(tid,'') for _,tid in sorted(type_by_pid.get(pid,[])) if types.get(tid,'')]
        abs_=[abilities.get(aid,'') for _,aid in sorted(ability_by_pid.get(pid,[])) if abilities.get(aid,'')]
        sts=[{'name':stats.get(stid,''),'value':val} for stid,val in sorted(stat_by_pid.get(pid,[])) if stats.get(stid,'')]
        parent=i(s.get('evolves_from_species_id'))
        result[str(sid)].update({
          'name':s.get('identifier') or p.get('identifier') or f'pokemon-{sid}',
          'height':(i(p.get('height'))/10 if i(p.get('height')) is not None else None),
          'weight':(i(p.get('weight'))/10 if i(p.get('weight')) is not None else None),
          'baseExperience':i(p.get('base_experience')),
          'generation':gens.get(i(s.get('generation_id')),''),'habitat':habitats.get(i(s.get('habitat_id')),''),
          'growth':growth.get(i(s.get('growth_rate_id')),''),'captureRate':i(s.get('capture_rate')),
          'baseHappiness':i(s.get('base_happiness')),'genderRate':i(s.get('gender_rate')),
          'isBaby':b(s.get('is_baby')),'isLegendary':b(s.get('is_legendary')),'isMythical':b(s.get('is_mythical')),
          'types':ts,'ability':abs_[0] if abs_ else '', 'genus':genus.get(sid,''),
          'eggGroups':[eggs.get(e,'') for e in egg_by_species.get(sid,[]) if eggs.get(e,'')],
          'stats':sts,'evolvesFrom':parent if parent and parent<=1025 else None,'evolutionDetails':evo_detail.get(sid,[]),
          'flavorPt':flavors.get(sid,{})
        })
    children={sid:[] for sid in range(1,1026)}
    for sid in range(1,1026):
        parent=result[str(sid)].get('evolvesFrom')
        if parent in children: children[parent].append(sid)
    for sid,ch in children.items(): result[str(sid)]['children']=ch

    payload={'version':'8.0-f4.6','source':'PokeAPI CSV snapshot at build time','count':1025,'pokemon':result}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'),sort_keys=True),encoding='utf-8')
    check=json.loads(OUT.read_text(encoding='utf-8'))
    assert check['count']==1025 and len(check['pokemon'])==1025 and all(str(x) in check['pokemon'] for x in range(1,1026))
    print(f'Offline Pokemon core: 1025/1025 • {OUT.stat().st_size} bytes')
if __name__=='__main__': main()

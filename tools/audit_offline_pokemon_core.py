#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P=R/'app/src/main/assets/pokemon-offline-core-v8.json'
A=R/'app/src/main/assets/assets/pokemon'
VALID_TYPES={'normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy'}
VALID_STATS={'hp','attack','defense','special-attack','special-defense','speed'}

def fail(msg): raise SystemExit('OFFLINE CORE AUDIT FAIL: '+msg)

def main():
    d=json.loads(P.read_text(encoding='utf-8')); mons=d.get('pokemon',{})
    if d.get('count')!=1025 or len(mons)!=1025: fail('count != 1025')
    missing=[];bad_types=[];bad_stats=[];bad_metrics=[];bad_parent=[];bad_children=[];art=[]
    portuguese_flavor=0;with_ability=0;with_genus=0
    for i in range(1,1026):
        p=mons.get(str(i))
        if not p: missing.append(i);continue
        if p.get('id')!=i or not str(p.get('name') or '').strip(): fail(f'identity #{i}')
        ts=p.get('types') or []
        if not ts or len(ts)>2 or any(t not in VALID_TYPES for t in ts): bad_types.append(i)
        stats=p.get('stats') or []
        names={x.get('name') for x in stats}
        if len(stats)!=6 or names!=VALID_STATS or any(not isinstance(x.get('value'),int) or x.get('value')<=0 for x in stats): bad_stats.append(i)
        h=p.get('height');w=p.get('weight')
        if h is None or w is None or h<=0 or w<=0: bad_metrics.append(i)
        parent=p.get('evolvesFrom')
        if parent is not None and str(parent) not in mons: bad_parent.append(i)
        for child in p.get('children') or []:
            if str(child) not in mons or mons[str(child)].get('evolvesFrom')!=i: bad_children.append((i,child))
        if not (A/f'{i}.png').exists(): art.append(i)
        if p.get('flavorPt'): portuguese_flavor+=1
        if p.get('ability'): with_ability+=1
        if p.get('genus'): with_genus+=1
    if missing: fail('missing ids '+str(missing[:10]))
    if bad_types: fail('invalid types '+str(bad_types[:10]))
    if bad_stats: fail('invalid stats '+str(bad_stats[:10]))
    if bad_metrics: fail('invalid height/weight '+str(bad_metrics[:10]))
    if bad_parent or bad_children: fail('broken evolution references')
    if art: fail('missing canonical art '+str(art[:10]))
    # Detect cycles in evolvesFrom graph.
    for i in range(1,1026):
        seen=set();cur=i
        while mons[str(cur)].get('evolvesFrom') is not None:
            cur=mons[str(cur)]['evolvesFrom']
            if cur in seen: fail(f'evolution cycle at #{i}')
            seen.add(cur)
    # Regression sentinels for tricky evolutionary structures and current reference samples.
    assert len(mons['133'].get('children') or [])>=3, 'Eevee branching regression'
    assert mons['292'].get('evolvesFrom')==290, 'Shedinja relation regression'
    assert mons['912'].get('types')==['water'], 'Quaxly type regression'
    assert mons['906'].get('types')==['grass'], 'Sprigatito type regression'
    print(f'OFFLINE CORE AUDIT: PASS • 1025 identities/types/stats/metrics/art • evolution graph valid • PT flavor {portuguese_flavor}/1025 • abilities {with_ability}/1025 • genus PT {with_genus}/1025')
if __name__=='__main__': main()

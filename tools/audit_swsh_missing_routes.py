#!/usr/bin/env python3
"""Classify tracked Sword/Shield dex species that still have no acquisition route.
Runs after the F7.6 enrichment stage and prints a compact machine-readable report.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'app/src/main/assets/swsh-encounters-v8.js'
CORE=ROOT/'app/src/main/assets/pokemon-offline-core-v8.json'
PACK=ROOT/'data/embedded-dex-pack.json'

def data_from_js():
    text=ASSET.read_text(encoding='utf-8')
    m=re.search(r'const DATA=(\{.*\});\nfunction get',text,re.S)
    if not m:raise SystemExit('SWSH gap audit: DATA not found')
    return json.loads(m.group(1))

def main():
    data=data_from_js();pokemon=data.get('pokemon') or {}
    core=(json.loads(CORE.read_text(encoding='utf-8')).get('pokemon') or {})
    pack=json.loads(PACK.read_text(encoding='utf-8'))
    keys={'galar':'swsh:galar','isle-of-armor':'swsh:isle-of-armor','crown-tundra':'swsh:crown-tundra'}
    scopes={scope:{int(r[0]) for r in (pack.get('dexes') or {}).get(key,[]) if isinstance(r,list) and r} for scope,key in keys.items()}
    union=set().union(*scopes.values())
    missing=sorted(pid for pid in union if not (pokemon.get(str(pid),{}).get('encounters') or []))
    rows=[];classes={}
    for pid in missing:
        c=core.get(str(pid),{})
        parent=int(c.get('evolvesFrom') or 0)
        children=[int(x) for x in (c.get('children') or []) if str(x).isdigit() or isinstance(x,int)]
        parent_has=bool(parent and (pokemon.get(str(parent),{}).get('encounters') or []))
        if parent:
            kind='evolution-parent-covered' if parent_has else 'evolution-parent-missing'
        elif children:
            kind='base-with-evolution-family'
        else:
            kind='standalone-or-special'
        classes[kind]=classes.get(kind,0)+1
        rows.append({'id':pid,'name':c.get('name') or c.get('species') or f'#{pid}','scopes':[s for s,ids in scopes.items() if pid in ids],'parent':parent or None,'parentHasRoute':parent_has,'children':children,'class':kind})
    print('SWSH GAP AUDIT: '+json.dumps({'missingCount':len(missing),'classes':classes,'rows':rows},ensure_ascii=False,separators=(',',':')))
    return 0
if __name__=='__main__':raise SystemExit(main())

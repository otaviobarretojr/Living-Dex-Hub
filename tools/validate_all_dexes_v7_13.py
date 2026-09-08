from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'data'/'embedded-dex-pack.json'
IMG=ROOT/'app'/'src'/'main'/'assets'/'assets'/'pokemon'
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'

expected={
 'letsgo:kanto':153,
 'swsh:galar':400,
 'swsh:isle-of-armor':211,
 'swsh:crown-tundra':210,
 'bdsp:sinnoh':151,
 'bdsp:national-bdsp':493,
 'arceus:hisui':242,
 'sv:paldea':400,
 'sv:kitakami':200,
 'sv:blueberry':243,
 'za:lumiose':232,
 'za:hyperspace':132,
}
primary={
 'letsgo':'letsgo:kanto',
 'swsh':'swsh:galar',
 'bdsp':'bdsp:sinnoh',
 'arceus':'arceus:hisui',
 'sv':'sv:paldea',
 'za':'za:lumiose',
}

pack=json.loads(PACK.read_text(encoding='utf-8'))
dexes=pack.get('dexes',{})
errors=[]
report={}
for key,count in expected.items():
 rows=dexes.get(key)
 if not rows:
  errors.append(f'{key}: ausente/vazia');continue
 species=[int(r[0]) for r in rows]
 entries=[int(r[1]) for r in rows]
 info={
  'count':len(rows),'expected':count,'first':rows[0],'last':rows[-1],
  'unique_species':len(set(species))==len(species),
  'unique_entries':len(set(entries))==len(entries),
  'contiguous_entries':entries==list(range(1,count+1)),
  'ids_in_supported_asset_range':all(1<=i<=1025 for i in species),
  'images_present':all((IMG/f'{i}.png').exists() for i in species),
 }
 report[key]=info
 if len(rows)!=count:errors.append(f'{key}: {len(rows)} != {count}')
 if not info['unique_species']:errors.append(f'{key}: espécies duplicadas')
 if not info['unique_entries']:errors.append(f'{key}: números de entrada duplicados')
 if not info['contiguous_entries']:errors.append(f'{key}: entradas não são 1..{count}')
 if not info['ids_in_supported_asset_range']:errors.append(f'{key}: espécie fora de 1..1025')
 if not info['images_present']:errors.append(f'{key}: imagem local ausente')

pngs=list(IMG.glob('*.png'))
if len(pngs)!=1025:errors.append(f'assets: {len(pngs)} PNGs != 1025')
for game,key in primary.items():
 if len(dexes.get(key,[]))!=expected[key]:errors.append(f'Box principal {game} inválida via {key}')

html=HTML.read_text(encoding='utf-8')
required=[
 'living-dex-full-audit" content="7.13.0"',
 'LD713_SPECIAL_EVOLUTION_HINTS',
 'window.ld713Audit=function',
 'Gimmighoul Coins',
 'Linking Cord',
 'Galarian Yamask',
]
for token in required:
 if token not in html:errors.append(f'HTML sem marcador/dica: {token}')

print(json.dumps({'primary':primary,'dexes':report,'png_count':len(pngs),'errors':errors},ensure_ascii=False,indent=2))
if errors:raise SystemExit('Full Dex audit failed: '+'; '.join(errors))
print('Full Dex audit 7.13.0 passed: 12/12 dexes, 6/6 primary Boxes, 1025/1025 images.')

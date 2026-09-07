from pathlib import Path
import json, urllib.request, hashlib
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'data/ui_media_v4_5.json').read_text(encoding='utf-8'))
out=root/'app/src/main/assets/assets/ui45';out.mkdir(parents=True,exist_ok=True)
ua={'User-Agent':'Mozilla/5.0 LivingDexHub/4.5'}
rows=[]
for a in manifest['assets']:
    dest=out/a['file']
    req=urllib.request.Request(a['url'],headers=ua)
    with urllib.request.urlopen(req,timeout=35) as r: data=r.read()
    if len(data)<15000: raise SystemExit(f"Asset too small: {a['id']} {len(data)}")
    dest.write_bytes(data)
    rows.append({'id':a['id'],'file':a['file'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'source_page':a['source_page']})
(out/'manifest.json').write_text(json.dumps({'version':'4.5','assets':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print('UI 4.5 media synced:',len(rows),'assets')

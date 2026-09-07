from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
h=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
g=(root/'app/build.gradle').read_text(encoding='utf-8')
m=json.loads((root/'data/ui_media_v4_5.json').read_text(encoding='utf-8'))
vm=re.search(r"versionName\s+'([0-9]+)\.([0-9]+)\.([0-9]+)'",g)
vc=re.search(r'versionCode\s+(\d+)',g)
version_ok=bool(vm and vc and tuple(map(int,vm.groups())) >= (4,5,0) and int(vc.group(1)) >= 57)
checks={
'marker':'living-dex-reference-faithful" content="4.5"' in h,
'library-art':'function r45Library' in h and 'assets/ui45/' in h,
'map-art':"paldea-map.jpg" in h,
'map-tabs':'Rota por nível' in h and '18 objetivos' in h,
'map-controls':'.ref43-controls button' in h,
'map-pins':'.geo-node:after' in h,
'library-grid':'grid-template-columns:repeat(2' in h,
'current-game':'Jogando agora' in h,
'media-db':len(m.get('assets',[]))==7,
'version':version_ok,
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
miss=[k for k,v in checks.items() if not v]
if miss:raise SystemExit('v4.5 validation failed: '+', '.join(miss))
print('Reference faithful 4.5 validated:',len(checks),'/',len(checks))

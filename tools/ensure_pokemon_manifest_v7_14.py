from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'app'/'src'/'main'/'assets'/'assets'/'pokemon'
PNG=b'\x89PNG\r\n\x1a\n'
files={}
missing=[]
for i in range(1,1026):
    p=OUT/f'{i}.png'
    if not p.exists() or p.stat().st_size<=8 or p.read_bytes()[:8]!=PNG:
        missing.append(i)
    else:
        files[str(i)]=p.stat().st_size
manifest={
    'version':2,
    'count':len(files),
    'missing':missing,
    'totalBytes':sum(files.values()),
    'files':files,
}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Canonical Pokemon manifest: {manifest['count']}/1025")
if missing:
    raise SystemExit(f'Pokemon assets incomplete: missing={missing}')

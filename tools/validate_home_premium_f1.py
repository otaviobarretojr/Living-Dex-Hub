from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];A=R/'app/src/main/assets'
def rd(n): return (A/n).read_text(encoding='utf-8')
H=rd('index.html');J=rd('pokemon-detail-v8.js');VQ=rd('pokemon-visual-quality-v8.js');X=rd('game-context-v8.js');E=rd('pokemon-evolution-v8.js');D=rd('pokemon-data-v8.js');AB=rd('pokemon-about-v8.js');AC=rd('pokemon-about-v8.css');THEME=rd('pokemon-reference-theme-v8.css');OFF=rd('pokemon-offline-core-v8.js');COL=rd('collection-reliability-v8.js');HV=rd('home-v8.js');UX=rd('product-ux-v8.js')
ANDROID=(R/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8');GRADLE=(R/'app/build.gradle').read_text(encoding='utf-8')
legacy=['pokemon-alive-beta-v8.js','pokemon-alive-beta-v8.css','pokemon-3d-v8.js','pokemon-3d-v8.css','pokemon-frame-animation-v8.js','pokemon-frame-animation-v8.css'];pngs=list((A/'assets/pokemon').glob('*.png'));types=['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy'];offline=json.loads((A/'pokemon-offline-core-v8.json').read_text(encoding='utf-8'));off_p=offline.get('pokemon',{});loadbox=X.split('async function loadBoxRuntime',1)[1].split('function boxIsOpen',1)[0];embedded=A/'pokemon-offline-core-data-v8.js'
checks={
'canonical baseline':'living-dex-canonical-baseline\" content=\"7.14.0\"' in H,
'home F4':"version:'8.0-f4.1'" in HV,
'strict context F2.6':"version:'8.0-f2.6'" in X and 'primaryStateNeverUsesConsultation:true' in X,
'consultation never writes active id':'writePrimaryState(id)' not in loadbox,
'collection event':"const EVENT='ld:box-entry-changed'" in COL,
'Box filters preserved':"boxFilters:['all','owned','missing']" in UX and 'ld842Search' not in UX,
'offline runtime F5.7':"version:'8.0-f5.7'" in OFF and 'embeddedData:' in OFF and 'fileSchemeSafe:true' in OFF,
'embedded data generated':embedded.exists() and embedded.stat().st_size>100000 and 'window.__LD8_OFFLINE_DATA__=' in embedded.read_text(encoding='utf-8',errors='ignore')[:200],
'embedded data injected before runtime':H.count('pokemon-offline-core-data-v8.js')==1 and H.count('pokemon-offline-core-v8.js')==1 and H.index('pokemon-offline-core-data-v8.js')<H.index('pokemon-offline-core-v8.js'),
'offline JSON 1025':offline.get('count')==1025 and len(off_p)==1025 and all(str(i) in off_p for i in range(1,1026)),
'offline technical coverage':sum(bool(p.get('types')) and len(p.get('stats') or [])==6 for p in off_p.values())>=1000,
'evolution offline':"version:'8.0-f3.5.1'" in E,
'data offline':"version:'8.0-f3.6.1'" in D,
'about F5.6':"version:'8.0-f5.6'" in AB and 'officialEntryNeverFaked:true' in AB and 'factualSummaryLabeled:true' in AB,
'no invented lore':'noInventedLore:true' in AB and 'noInventedLore:true' in OFF,
'detail local fallback preserved':"version:'8.0-f5.7'" in J and 'localHeroArtForced:true' in J and 'fileSchemeSafeArt:true' in J,
'visual quality F5.8':"version:'8.0-f5.8'" in VQ and 'officialArtworkPrimary:true' in VQ and 'localArtworkFallback:true' in VQ and 'typeLabelsPortuguese:true' in VQ,
'visual module injected last':H.count('pokemon-visual-quality-v8.js')==1 and H.index('pokemon-visual-quality-v8.js')>H.index('pokemon-about-v8.js'),
'high quality official artwork':"official-artwork/" in VQ and 'imageRendering' in VQ,
'local fallback path':"assets/pokemon/" in VQ and 'document.baseURI' in VQ,
'adaptive 18 types':all(f'data-primary-type=\"{t}\"' in THEME for t in types),
'fullscreen mobile':'100dvh' in AC,
'startup-safe Android':'OnBackInvokedDispatcher' not in ANDROID and 'WindowInsetsController' not in ANDROID and 'onBackPressed()' in ANDROID,
'Android WebView safety':'MIXED_CONTENT_NEVER_ALLOW' in ANDROID and 'setSafeBrowsingEnabled(true)' in ANDROID,
'release version':"versionName '7.22.8'" in GRADLE and 'versionCode 152' in GRADLE,
'legacy removed':all(not (A/x).exists() for x in legacy),
'1025 art':len(pngs)==1025 and (A/'assets/pokemon/915.png').exists()
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK   ' if v else 'FAIL ')+k)
if failed:raise SystemExit('V7.22.8 validation failed: '+', '.join(failed))
print(f'V7.22.8: {len(checks)}/{len(checks)} checks OK • official artwork primary • local offline fallback • PT-BR type labels')

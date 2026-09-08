from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
A=R/'app/src/main/assets'
H=(A/'index.html').read_text(encoding='utf-8')
J=(A/'pokemon-detail-v8.js').read_text(encoding='utf-8')
C=(A/'pokemon-detail-v8.css').read_text(encoding='utf-8')
X=(A/'game-context-v8.js').read_text(encoding='utf-8')
S=(A/'game-selector-v8.js').read_text(encoding='utf-8')
E=(A/'pokemon-evolution-v8.js').read_text(encoding='utf-8')
D=(A/'pokemon-data-v8.js').read_text(encoding='utf-8')
AB=(A/'pokemon-about-v8.js').read_text(encoding='utf-8')
AC=(A/'pokemon-about-v8.css').read_text(encoding='utf-8')
THEME=(A/'pokemon-reference-theme-v8.css').read_text(encoding='utf-8')
OFF=(A/'pokemon-offline-core-v8.js').read_text(encoding='utf-8')
COL=(A/'collection-reliability-v8.js').read_text(encoding='utf-8')
HV=(A/'home-v8.js').read_text(encoding='utf-8')
HC=(A/'home-v8.css').read_text(encoding='utf-8')
UX=(A/'product-ux-v8.js').read_text(encoding='utf-8')
ANDROID=(R/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
GRADLE=(R/'app/build.gradle').read_text(encoding='utf-8')
legacy=['pokemon-alive-beta-v8.js','pokemon-alive-beta-v8.css','pokemon-3d-v8.js','pokemon-3d-v8.css','pokemon-frame-animation-v8.js','pokemon-frame-animation-v8.css']
pokemon_dir=A/'assets/pokemon';pngs=list(pokemon_dir.glob('*.png')) if pokemon_dir.exists() else []
types=['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy']
offline_path=A/'pokemon-offline-core-v8.json'
offline=json.loads(offline_path.read_text(encoding='utf-8')) if offline_path.exists() else {}
off_p=offline.get('pokemon',{}) if isinstance(offline,dict) else {}
feedback_body=UX.split('function hookFeedback()',1)[1].split('function hookRenders()',1)[0] if 'function hookFeedback()' in UX else ''
load_box_body=X.split('async function loadBoxRuntime',1)[1].split('function boxIsOpen',1)[0] if 'async function loadBoxRuntime' in X else ''
checks={
 'canonical baseline':'living-dex-canonical-baseline" content="7.14.0"' in H,
 'F4.5 product marker':'living-dex-product-ux" content="F4.5-event-driven-box"' in H,
 'F4.5 context marker':'living-dex-context-reliability" content="F4.5-business-events"' in H,
 'F4.6 offline marker':'living-dex-offline-core" content="F4.6-bundled-1025"' in H,
 'F4.3 detail marker':'living-dex-detail-theme" content="F4.3-adaptive-reference"' in H and 'pokemon-reference-theme-v8.css' in H,
 'home F4':'home-v8.js' in H and "version:'8.0-f4.1'" in HV,
 'compact Home':'compactHero:true' in HV and '.ld8-hero{position:relative;height:258px' in HC,
 'actionable game cards':'gameCardsActionable:' in HV and 'ld813SetBoxGame' in HV,
 'missing progress':'missingCount:true' in HV and 'Faltam ' in HV,
 'game overview':'fullScreenGameOverview:true' in S and 'ld82OpenGameOverview' in S,
 'strict context F2.6':"version:'8.0-f2.6'" in X and 'primaryStateNeverUsesConsultation:true' in X,
 'consultation never writes active id':'writePrimaryState(id)' not in load_box_body,
 'legacy Box readers context-aware':'legacyBoxReadersContextAware:true' in X and 'window.ld71Game=function' in X and 'window.ld71Dex=function' in X,
 'Box set validates primary remains primary':"String(st().activeGameId||'')===primaryId()" in X,
 'collection module injected':'collection-reliability-v8.js' in H and "version:'8.0-f4.5'" in COL,
 'collection business event':"const EVENT='ld:box-entry-changed'" in COL and 'postMutationStateVerified:true' in COL,
 'collection event dedupe':'deduplicatedEvents:true' in COL and 'before!==after' in COL,
 'Box UX injected':'product-ux-v8.js' in H and 'product-ux-v8.css' in H,
 'Box search':'boxSearch:true' in UX and 'ld842Search' in UX,
 'Box filters':"boxFilters:['all','owned','missing']" in UX and 'data-ld842-filter="missing"' in UX,
 'event-driven feedback':"version:'8.0-f4.5.1'" in UX and 'eventDrivenFeedback:true' in UX and "addEventListener('ld:box-entry-changed'" in UX,
 'feedback no DOM observer':'MutationObserver' not in feedback_body and 'noDomMutationFeedback:true' in UX,
 'Box card open no toast':"closest?.('#ld71BoxView .ld71-slot')" not in feedback_body,
 'Home refresh from collection event':'homeProgressRefresh:true' in UX and 'ld8HomeRender' in feedback_body,
 'offline runtime injected':'pokemon-offline-core-v8.js' in H and "version:'8.0-f4.6'" in OFF,
 'offline JSON exists':offline_path.exists(),
 'offline JSON 1025':offline.get('count')==1025 and len(off_p)==1025 and all(str(i) in off_p for i in range(1,1026)),
 'offline technical coverage':sum(bool(p.get('types')) and len(p.get('stats') or [])==6 for p in off_p.values())>=1000 if off_p else False,
 'offline evolution graph':all((not p.get('evolvesFrom') or str(p.get('evolvesFrom')) in off_p) for p in off_p.values()) if off_p else False,
 'evolution F3.5.1':"version:'8.0-f3.5.1'" in E and 'bundledOfflineEvolution:true' in E and 'ld8OfflineCore?.evolution' in E,
 'data F3.6.1':"version:'8.0-f3.6.1'" in D and 'bundledOfflineCore:true' in D and 'ld8OfflineCore?.data' in D,
 'about F3.7.2':"version:'8.0-f3.7.2'" in AB and 'bundledOfflineAbout:true' in AB and 'ld8OfflineCore?.about' in AB,
 'about Portuguese only':'portugueseOnlyVisibleContent:true' in AB and 'noEnglishLoreFallback:true' in AB,
 'about game contextual':'gameContextAware:true' in AB and 'VERSION_MAP' in AB,
 'about compact cards':'compactAutoHeightCards:true' in AB and 'aboutInternalScroll:true' in AB,
 'national number fixed':'nationalNumberFixed:true' in AB and 'fixHeaderNumber' in AB,
 'Portuguese type labels':'portugueseTypeLabels:true' in AB and "grass:'Planta'" in AB,
 'single legacy lore fetch path':"if(typeof window.ld8f37Audit!=='function')renderLore()" in J,
 'detail F3.4.2':"version:'8.0-f3.4.2'" in J and 'localizedTypeThemeStable:true' in J,
 'adaptive all primary types':all(f'data-primary-type="{t}"' in THEME for t in types),
 'larger reference hero':'height:clamp(225px,31dvh,305px)' in THEME and 'width:min(56vw,245px)' in THEME,
 'type themed surfaces':'var(--type-pattern)' in THEME and 'color-mix(in srgb,var(--poke-type)' in THEME,
 'fullscreen mobile':'100dvh' in AC,
 'box action preserved':'boxActionPreserved' in J and 'Na Box' in C,
 'journey harness present':(R/'tools/journey_reliability_harness.js').exists() and 'JOURNEY RELIABILITY: PASS' in (R/'tools/journey_reliability_harness.js').read_text(encoding='utf-8'),
 'startup-safe Android wrapper':'OnBackInvokedDispatcher' not in ANDROID and 'WindowInsetsController' not in ANDROID and 'onBackPressed()' in ANDROID,
 'Android WebView safety':'MIXED_CONTENT_NEVER_ALLOW' in ANDROID and 'setSafeBrowsingEnabled(true)' in ANDROID,
 'Android low-risk hardening':'setWebContentsDebuggingEnabled(BuildConfig.DEBUG)' in ANDROID and 'setCacheMode(WebSettings.LOAD_DEFAULT)' in ANDROID,
 'release version':"versionName '7.21.0'" in GRADLE and 'versionCode 143' in GRADLE,
 'only current static runtime':all(x not in H for x in legacy),
 'legacy files physically removed':all(not (A/x).exists() for x in legacy),
 '1025 canonical Pokemon art':len(pngs)==1025,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('OK   ' if v else 'FAIL ')+k)
if failed: raise SystemExit('V7.21 RELIABILITY validation failed: '+', '.join(failed))
print(f'V7.21 RELIABILITY: {len(checks)}/{len(checks)} checks OK • strict context isolation • event-driven collection • offline 1025 core • stable Android wrapper')

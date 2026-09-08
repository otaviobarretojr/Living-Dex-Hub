from pathlib import Path
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
HV=(A/'home-v8.js').read_text(encoding='utf-8')
HC=(A/'home-v8.css').read_text(encoding='utf-8')
UX=(A/'product-ux-v8.js').read_text(encoding='utf-8')
UXC=(A/'product-ux-v8.css').read_text(encoding='utf-8')
ANDROID=(R/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
GRADLE=(R/'app/build.gradle').read_text(encoding='utf-8')
legacy=['pokemon-alive-beta-v8.js','pokemon-alive-beta-v8.css','pokemon-3d-v8.js','pokemon-3d-v8.css','pokemon-frame-animation-v8.js','pokemon-frame-animation-v8.css']
pokemon_dir=A/'assets/pokemon';pngs=list(pokemon_dir.glob('*.png')) if pokemon_dir.exists() else []
checks={
 'canonical baseline':'living-dex-canonical-baseline" content="7.14.0"' in H,
 'F4 product marker':'living-dex-product-ux" content="F4.2-home-box-polish"' in H,
 'home F4':'home-v8.js' in H and "version:'8.0-f4.1'" in HV,
 'compact Home':'compactHero:true' in HV and '.ld8-hero{position:relative;height:258px' in HC,
 'actionable game cards':'gameCardsActionable:' in HV and 'button.ld8-game[data-ld8-game]' in HV and 'consultGame' in HV and 'ld813SetBoxGame' in HV,
 'consult preserves primary':'consultPreservesPrimary:true' in HV and "version:'8.0-f2.5.1'" in X,
 'missing progress':'missingCount:true' in HV and 'Faltam ' in HV,
 'safe Home actions':'musicSafeFallback:true' in HV and 'ld82OpenGameOverview' in HV,
 'game overview':'fullScreenGameOverview:true' in S and 'ld82OpenGameOverview' in S,
 'Box UX injected':'product-ux-v8.js' in H and 'product-ux-v8.css' in H,
 'Box search':'boxSearch:true' in UX and 'ld842Search' in UX,
 'Box filters':"boxFilters:['all','owned','missing']" in UX and 'data-ld842-filter="missing"' in UX,
 'Box nonblocking feedback':'boxToastFeedback:true' in UX and 'ld842-toast' in UXC,
 'Home refresh from Box':'homeProgressRefresh:true' in UX and 'ld8HomeRender' in UX,
 'independent game context':'F2.5-independent' in H and "version:'8.0-f2.5.1'" in X,
 'detail F3.4.1':"version:'8.0-f3.4.1'" in J and 'legacyLoreFetchSuppressedWhenF371:true' in J,
 'single About fetch path':"if(typeof window.ld8f37Audit!=='function')renderLore()" in J,
 'evolution F3.5':"version:'8.0-f3.5'" in E and 'officialEvolutionChain:true' in E,
 'data F3.6':"version:'8.0-f3.6'" in D and 'technicalOnly:true' in D,
 'about F3.7.1':"version:'8.0-f3.7.1'" in AB,
 'about compact cards':'compactAutoHeightCards:true' in AB and 'aboutInternalScroll:true' in AB,
 'national number fixed':'nationalNumberFixed:true' in AB and 'fixHeaderNumber' in AB,
 'Portuguese type labels':'portugueseTypeLabels:true' in AB and "grass:'Planta'" in AB,
 'Portuguese about':'portugueseOnlyVisibleContent:true' in AB and 'ptOfficialEntryPreferred:true' in AB,
 'game contextual about':'gameContextAware:true' in AB and 'VERSION_MAP' in AB,
 'obtain preserved':'obtainPreserved' in AB and 'ld75Obtain' in AB,
 'about cache':'localAboutCache:true' in AB and 'localStorage' in AB,
 'data offline fallback':'localDataCache:true' in D and 'legacyOfflineFallback:true' in D,
 'fullscreen mobile':'100dvh' in AC,
 'box action preserved':'boxActionPreserved' in J and 'Na Box' in C,
 'primary vs consultation preserved':'primaryBoxContextUntouched:true' in J and 'primaryBoxContextUntouched:true' in AB,
 'modern Android bars':'WindowInsetsController' in ANDROID and 'setSystemBarsAppearance' in ANDROID,
 'modern Android back':'OnBackInvokedDispatcher' in ANDROID and 'handleBackAction' in ANDROID,
 'Android WebView safety':'MIXED_CONTENT_NEVER_ALLOW' in ANDROID and 'setSafeBrowsingEnabled(true)' in ANDROID,
 'release version':"versionName '7.20.0'" in GRADLE and 'versionCode 139' in GRADLE,
 'only current static runtime':all(x not in H for x in legacy),
 'legacy files physically removed':all(not (A/x).exists() for x in legacy),
 '1025 canonical Pokemon art':len(pngs)==1025,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('OK   ' if v else 'FAIL ')+k)
if failed: raise SystemExit('PRODUCT UX validation failed: '+', '.join(failed))
print(f'PRODUCT UX BASELINE: {len(checks)}/{len(checks)} checks OK • v7.20.0 • Home F4.1 • Box F4.2 • Detail F3.4.1 • 1025 images')

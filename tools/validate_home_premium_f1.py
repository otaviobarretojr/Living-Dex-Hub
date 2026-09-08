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
THEME=(A/'pokemon-reference-theme-v8.css').read_text(encoding='utf-8')
HV=(A/'home-v8.js').read_text(encoding='utf-8')
HC=(A/'home-v8.css').read_text(encoding='utf-8')
UX=(A/'product-ux-v8.js').read_text(encoding='utf-8')
UXC=(A/'product-ux-v8.css').read_text(encoding='utf-8')
ANDROID=(R/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
GRADLE=(R/'app/build.gradle').read_text(encoding='utf-8')
legacy=['pokemon-alive-beta-v8.js','pokemon-alive-beta-v8.css','pokemon-3d-v8.js','pokemon-3d-v8.css','pokemon-frame-animation-v8.js','pokemon-frame-animation-v8.css']
pokemon_dir=A/'assets/pokemon';pngs=list(pokemon_dir.glob('*.png')) if pokemon_dir.exists() else []
types=['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy']
checks={
 'canonical baseline':'living-dex-canonical-baseline" content="7.14.0"' in H,
 'F4 product marker':'living-dex-product-ux" content="F4.2-home-box-polish"' in H,
 'F4.3 detail marker':'living-dex-detail-theme" content="F4.3-adaptive-reference"' in H and 'pokemon-reference-theme-v8.css' in H,
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
 'Box feedback state-safe':"version:'8.0-f4.2.1'" in UX and 'feedbackOnlyAfterStateChange:true' in UX and 'noSlotOpenFalseToast:true' in UX and 'before===after' in UX,
 'Box card open has no toast':"closest?.('#ld71BoxView .ld71-slot')" not in UX,
 'Home refresh from Box':'homeProgressRefresh:true' in UX and 'ld8HomeRender' in UX,
 'independent game context':'F2.5-independent' in H and "version:'8.0-f2.5.1'" in X,
 'detail F3.4.2':"version:'8.0-f3.4.2'" in J and 'localizedTypeThemeStable:true' in J,
 'single About fetch path':"if(typeof window.ld8f37Audit!=='function')renderLore()" in J,
 'Portuguese type theme aliases':"'água':'water'" in J and "'aço':'steel'" in J and "'dragão':'dragon'" in J,
 'adaptive all primary types':all(f'data-primary-type="{t}"' in THEME for t in types),
 'larger reference hero':'height:clamp(225px,31dvh,305px)' in THEME and 'width:min(56vw,245px)' in THEME,
 'type themed surfaces':'var(--type-pattern)' in THEME and 'color-mix(in srgb,var(--poke-type)' in THEME,
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
 'startup-safe Android wrapper':'OnBackInvokedDispatcher' not in ANDROID and 'WindowInsetsController' not in ANDROID and 'onBackPressed()' in ANDROID,
 'Android WebView safety':'MIXED_CONTENT_NEVER_ALLOW' in ANDROID and 'setSafeBrowsingEnabled(true)' in ANDROID,
 'release version':"versionName '7.20.2'" in GRADLE and 'versionCode 141' in GRADLE,
 'only current static runtime':all(x not in H for x in legacy),
 'legacy files physically removed':all(not (A/x).exists() for x in legacy),
 '1025 canonical Pokemon art':len(pngs)==1025,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('OK   ' if v else 'FAIL ')+k)
if failed: raise SystemExit('REFERENCE DETAIL validation failed: '+', '.join(failed))
print(f'REFERENCE DETAIL: {len(checks)}/{len(checks)} checks OK • v7.20.2 • F4.3 adaptive theme • Box feedback hotfix • 1025 images')

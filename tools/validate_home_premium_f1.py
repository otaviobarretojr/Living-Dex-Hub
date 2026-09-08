from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=R/'app/src/main/assets'
H=(A/'index.html').read_text(encoding='utf-8')
J=(A/'pokemon-detail-v8.js').read_text(encoding='utf-8')
C=(A/'pokemon-detail-v8.css').read_text(encoding='utf-8')
X=(A/'game-context-v8.js').read_text(encoding='utf-8')
E=(A/'pokemon-evolution-v8.js').read_text(encoding='utf-8')
D=(A/'pokemon-data-v8.js').read_text(encoding='utf-8')
AB=(A/'pokemon-about-v8.js').read_text(encoding='utf-8')
AC=(A/'pokemon-about-v8.css').read_text(encoding='utf-8')
HV=(A/'home-v8.js').read_text(encoding='utf-8')
legacy=['pokemon-alive-beta-v8.js','pokemon-alive-beta-v8.css','pokemon-3d-v8.js','pokemon-3d-v8.css','pokemon-frame-animation-v8.js','pokemon-frame-animation-v8.css']
pokemon_dir=A/'assets/pokemon'
pngs=list(pokemon_dir.glob('*.png')) if pokemon_dir.exists() else []
checks={
 'canonical baseline':'living-dex-canonical-baseline" content="7.14.0"' in H,
 'home mounted':'home-v8.js' in H and "version:'8.0-f2.1'" in HV,
 'independent game context':'F2.5-independent' in H and "version:'8.0-f2.5.1'" in X,
 'detail F3.4':"version:'8.0-f3.4'" in J,
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
 'fullscreen mobile':'100dvh' in AC,
 'box action preserved':'boxActionPreserved' in J and 'Na Box' in C,
 'primary vs consultation preserved':'primaryBoxContextUntouched:true' in J and 'primaryBoxContextUntouched:true' in AB,
 'only current static runtime':all(x not in H for x in legacy),
 'legacy files physically removed':all(not (A/x).exists() for x in legacy),
 '1025 canonical Pokemon art':len(pngs)==1025,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('OK   ' if v else 'FAIL ')+k)
if failed: raise SystemExit('STABLE BASELINE validation failed: '+', '.join(failed))
print(f'STABLE BASELINE: {len(checks)}/{len(checks)} checks OK • static Pokemon artwork • F3.7.1 Sobre • 1025 images')

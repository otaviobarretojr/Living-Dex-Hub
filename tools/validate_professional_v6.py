from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
checks={
 'professional meta':'living-dex-professional-ui" content="6.0"' in s,
 'journey hub':'living-dex-journey-hub" content="5.2"' in s,
 'home reference':'living-dex-home-reference" content="5.1"' in s,
 'single journey fix':'living-dex-home-single-journey" content="5.1.1"' in s,
 'map import':'living-dex-map-import" content="5.0"' in s,
 'professional tokens':'--ui-accent:#ff5757' in s and '--ui-r4:30px' in s,
 'bottom nav polish':'.mnav{left:16px!important' in s,
 'dex responsive':'grid-template-columns:repeat(3,minmax(0,1fr))' in s,
 'home cleanup':'function pro60CleanHome()' in s,
 'a11y audit':'function pro60A11y()' in s,
 'journey tabs':all(x in s for x in ['Jornada</button>','Time recomendado</button>','Mapa</button>']),
}
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('Professional UI validation failed: '+', '.join(failed))
print('Professional UI 6.0 static audit: OK')

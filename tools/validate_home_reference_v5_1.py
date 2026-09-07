from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-home-reference" content="5.1"' in s,
 'hero':'home51-hero' in s,
 'cover':'home51-cover' in s,
 'all-game-art':'function home51Art' in s and 'letsgo.jpg' in s and 'swsh.jpg' in s and 'bdsp.jpg' in s and 'arceus.jpg' in s and 'sv.jpg' in s and 'za.jpg' in s,
 'active-render':'function renderActiveGameHome' in s,
 'progress':'home51-progressline' in s,
 'journey':'home51-journey' in s and 'Próximo objetivo' in s,
 'cta':'Continuar jornada' in s,
 'map-link':'Ver mapa' in s,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
missing=[k for k,v in checks.items() if not v]
if missing: raise SystemExit('Home Reference 5.1 validation failed: '+', '.join(missing))
print(f'Home Reference 5.1 validated: {len(checks)}/{len(checks)}')

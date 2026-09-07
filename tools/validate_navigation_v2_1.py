from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Navigation 2.1 marker':'living-dex-navigation" content="2.1' in s,
 'Missing hidden':'[data-view="missing"]' in s and 'nav21HideMissingEverywhere' in s,
 'Home journey':'home-journey-card' in s and 'function nav21OpenJourney' in s,
 'Library shortcut removed':'library-shortcut' in s and 'ver biblioteca' in s.lower(),
 'Direct game Dex':'function nav21OpenGameDex' in s and 'nav21FindModalAction' in s,
 'Active continue direct':'function continueActiveGame(){const id=state.activeGameId;if(id)nav21OpenGameDex(id)' in s,
 'Game cards rewired':'function nav21RewireGameCards' in s,
 'Exclusive game focus':'game-dex-focus' in s and 'game-focus-bar' in s,
 'Back to games':'function nav21ExitGameDex' in s,
 'Journey 1.9 preserved':'living-dex-smart-prep" content="1.9' in s,
 'Map 2.0 preserved':'living-dex-paldea-map" content="2.0' in s,
 'Quick toggle preserved':'contextual quick add/remove by game + selected version' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário'])
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed:raise SystemExit('Navigation 2.1 validation failed: '+', '.join(failed))
print(f'NAVIGATION 2.1 VALIDADA: {len(checks)}/{len(checks)}')
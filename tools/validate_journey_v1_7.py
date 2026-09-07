from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html').read_text()
checks={
'Journey marker':'living-dex-journey" content="1.7' in s,
'Circular progress':'game-progress-ring' in s and 'faltando' in s,
'Missing nav hidden':'.mnav-item[data-view="missing"]{display:none!important}' in s,
'Four nav layout':'repeat(4,1fr)' in s,
'Journey hub':'function openJourney' in s,
'Route 18':'Team Star Fighting — Eri' in s and 'Cortondo — Katy' in s,
'Route persistence':'toggleJourneyStep' in s and 'persist();renderJourney' in s,
'Starter teams':'SV_TEAMS' in s and 'sprigatito' in s and 'fuecoco' in s and 'quaxly' in s,
'Early mid late':"['early','Início']" in s and "['mid','Mid game']" in s and "['late','Late game']" in s,
'Map':'route-map' in s and 'toggleJourneyMapFull' in s,
'Fullscreen back':'map-fullscreen' in s and 'androidHandleBack=function' in s,
'Quick toggle preserved':'contextual quick add/remove by game + selected version' in s,
'Premium preserved':'living-dex-premium" content="1.6' in s,
'Core preserved':'living-dex-build" content="core-1.0' in s,
'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário','missionTimer','userXP'])
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
f=[k for k,v in checks.items() if not v]
if f:raise SystemExit('Journey 1.7 validation failed: '+', '.join(f))
print(f'JOURNEY 1.7 VALIDADA: {len(checks)}/{len(checks)}')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Journey 1.8 marker':'living-dex-journey-plus" content="1.8' in s,
 'Journey 1.7 preserved':'living-dex-journey" content="1.7' in s,
 'Next objective':'function svNextIndex' in s and 'Próximo objetivo' in s,
 'Boss counters':'const SV_COUNTERS=' in s,
 'Build database':'const SV_BUILDS=' in s,
 'Starter final builds':all(x in s for x in ['Meowscarada','Skeledirge','Quaquaval']),
 'Story core builds':all(x in s for x in ['Corviknight','Kilowattrel','Gyarados','Clodsire','Arboliva']),
 'Version fire slot':'Armarouge / Ceruledge' in s,
 'Build detail':'function openJourneyBuild' in s and 'Golpes recomendados' in s,
 'Owned team signal':'function teamOwnedV18' in s and 'owned-dot' in s,
 'Paldea coordinates':'const SV_ROUTE_POS=' in s and 'geo-node' in s,
 'Map next highlight':"n===num?'next':''" in s,
 'Fullscreen preserved':'toggleJourneyMapFull' in s,
 'Research links':'game8.co/games/Pokemon-Scarlet-Violet/archives/393731' in s and 'archives/394479' in s,
 'Quick toggle preserved':'contextual quick add/remove by game + selected version' in s,
 'Premium preserved':'living-dex-premium" content="1.6' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário','missionTimer','userXP'])
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed:raise SystemExit('Journey 1.8 validation failed: '+', '.join(failed))
print(f'JOURNEY 1.8 VALIDADA: {len(checks)}/{len(checks)}')

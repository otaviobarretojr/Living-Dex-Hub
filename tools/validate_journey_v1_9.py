from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Journey 1.9 marker':'living-dex-smart-prep" content="1.9' in s,
 'Smart prep renderer':'function svSmartPrep()' in s,
 'Collection-aware':'function svGameOwnedSmart' in s and "ui151GameOwned(x,'sv',version)" in s,
 'Version-aware slot':'function svResolveTeamId' in s and "violet" in s and 'return 937' in s,
 'Ceruledge build':"SV_BUILDS[937]" in s and 'Bitter Blade' in s and 'Swords Dance' in s,
 'Automatic phase':'function svPhaseForNext' in s,
 'Next objective analysis':'function svSmartPrepData' in s and 'svNextIndex()' in s,
 'Readiness':'PRONTIDÃO' in s,
 'Best choice':'Ver build da melhor escolha' in s,
 'How to obtain':'Como obter ${bestName}' in s,
 'Map link':"renderJourney('map')" in s,
 'Home next objective':'function injectSmartHome' in s and 'Próximo objetivo' in s,
 'Journey 1.8 preserved':'living-dex-journey-plus" content="1.8' in s,
 'Journey 1.7 preserved':'living-dex-journey" content="1.7' in s,
 'Quick toggle preserved':'contextual quick add/remove by game + selected version' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário'])
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('Journey 1.9 validation failed: '+', '.join(failed))
print(f'JOURNEY 1.9 VALIDADA: {len(checks)}/{len(checks)}')

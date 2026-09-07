from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Premium marker':'living-dex-premium" content="1.6' in s,
 'Focused home':'#home>.scope-note' in s and '#home>.hero' in s and '#home>.progress-zone' in s,
 'Current game state':'state.activeGameId=state.activeGameId||\'\'' in s,
 'Current game setter':'function setActiveGame' in s and 'state.activeGameId=id' in s,
 'Persist current game':'state.activeGameId=id;persist()' in s,
 'Home renderer':'function renderActiveGameHome' in s,
 'Continue game':'function continueActiveGame' in s and 'openGame(id)' in s,
 'Game library selector':'Definir como jogo atual' in s and 'game-active-btn' in s,
 'Active visual':'Jogando agora' in s and 'playing-card' in s,
 'Premium animation':'premiumViewIn' in s,
 'Premium navigation':'mobile-nav' in s and 'backdrop-filter:blur(22px)' in s,
 'Quick toggle preserved':'contextual quick add/remove by game + selected version' in s,
 'UI 1.5 preserved':'living-dex-ui" content="1.5' in s,
 'Core preserved':'living-dex-build" content="core-1.0' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário','missionTimer','userXP'])
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('Premium UI 1.6 validation failed: '+', '.join(failed))
print(f'PREMIUM UI 1.6 VALIDADA: {len(checks)}/{len(checks)}')

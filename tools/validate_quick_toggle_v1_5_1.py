from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Patch marker':'Living Dex Hub v1.5.1 — contextual quick add/remove by game + selected version.' in s,
 'Version state':'state.versionCaught=state.versionCaught||{}' in s,
 'Version key':'function ui151VersionKey' in s,
 'Selected version':'selectedVersion(currentGame.id)' in s,
 'Game add':'function ui151AddGame' in s and 'state.games[`${gameId}:${id}`]=true' in s,
 'Global sync':'state.global[id]=true' in s,
 'Specimen origin':'addSpecimenInstance(id,{originGame:gameId,version:version||\'\'})' in s,
 'Current location':'matching.currentLocation.gameId=gameId' in s,
 'Game remove':'function ui151RemoveGame' in s and 'delete state.specimenInstances[uid]' in s,
 'Removal confirm':'Este registro será removido somente desta versão.' in s and 'confirm(`Remover ${name} de ${where}?' in s,
 'Global remove confirm':'confirm(`Remover ${name} do Living Dex Global?`)' in s,
 'Same shortcut':'function ui15QuickCapture' in s and "owned?'✓':'+'" in s,
 'UI 1.5 preserved':'living-dex-ui" content="1.5' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário'])
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('Quick toggle v1.5.1 validation failed: '+', '.join(failed))
print(f'QUICK TOGGLE v1.5.1 VALIDADO: {len(checks)}/{len(checks)}')

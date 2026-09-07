from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'UI 1.5 marker':'living-dex-ui" content="1.5' in s,
 'Core frozen':'living-dex-build" content="core-1.0' in s,
 '1025 offline':'OFFLINE_POKEMON_ASSET_COUNT=1025' in s,
 'Home progress copy':'Seu progresso' in s and 'sem repetir as ferramentas' in s,
 'Home shortcuts removed':"if(viewId==='home')ui12HomeShortcuts(v);" not in s,
 'Quick capture':'function ui15QuickCapture' in s and 'quick-catch' in s,
 'Card detail preserved':'card.click()' in s,
 'Backup create':'Criar backup' in s,
 'Backup restore':'Restaurar backup' in s,
 'Android back':'function androidHandleBack()' in s,
 'No gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário','missionTimer','userXP']),
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
if not all(checks.values()):raise SystemExit('UI 1.5 regression failed')
print(f'UI 1.5 VALIDADA: {len(checks)}/{len(checks)}')

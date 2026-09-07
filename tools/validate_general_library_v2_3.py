from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'marker':'living-dex-general-library" content="2.3"' in s,
 'home_single_cta':'Continuar jornada' in s and '#home .home-next-objective,#home .home-journey-card' in s,
 'general_tab':'Geral' in s and 'nav23BottomAudit' in s,
 'library_switch':'Biblioteca' in s and 'Dex Nacional' in s and 'nav23-general-switch' in s,
 'library_open':'function nav23OpenLibrary()' in s,
 'national_open':'function nav23OpenNationalDex()' in s,
 'compact_cards':'nav23-compact-library' in s and 'nav23-open-dex' in s,
 'swap_game':'Trocar jogo' in s and "swap.setAttribute('onclick','nav23OpenLibrary()')" in s,
 'game_dex_preserved':'nav221OpenGameDex' in s and 'game-dex-focus' in s,
 'svg_nav_icons':'function nav23Icon(name)' in s and '<svg viewBox=' in s,
 'touch_targets':'min-height:52px' in s and 'touch-action:manipulation' in s,
 'safe_area':'env(safe-area-inset-bottom)' in s,
 'core_preserved':'living-dex-build" content="core-1.0"' in s,
 'quick_toggle':'contextual quick add/remove by game + selected version' in s,
 'no_gamification':all(x not in s for x in ['Sistema de missões','Cronômetro de missão','XP de usuário','missionTimer','userXP'])
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
failed=[k for k,v in checks.items() if not v]
print(f"GENERAL LIBRARY 2.3 VALIDADA: {len(checks)-len(failed)}/{len(checks)}")
if failed: raise SystemExit('Falhas: '+', '.join(failed))

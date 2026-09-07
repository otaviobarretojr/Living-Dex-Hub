from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-home-journey" content="2.3.2"' in s,
 'home_reset':'function home232ResetHome()' in s,
 'home_mode':'home232-home-mode' in s,
 'library_cleanup':"classList.remove('nav23-library-mode','game-dex-focus')" in s,
 'journey_summary':'home232-journey' in s,
 'journey_progress':'Seu andamento em Paldea' in s,
 'journey_team':'Time recomendado' in s,
 'journey_map':'Próximo ponto da rota recomendado' in s,
 'single_cta':'>Continuar jornada</button>' in s,
 'home_qa':'data.homeQa' in s or 'dataset.homeQa' in s,
 'general_preserved':'living-dex-general-library" content="2.3"' in s,
 'routing_preserved':'living-dex-general-routing" content="2.3.1"' in s,
 'journey_preserved':'living-dex-smart-prep" content="1.9"' in s,
 'no_gamification':'missão diária' not in s.lower() and 'cronômetro' not in s.lower(),
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed:raise SystemExit('HOME JOURNEY 2.3.2 FAIL: '+', '.join(failed))
print(f'HOME JOURNEY 2.3.2 VALIDADA: {len(checks)}/{len(checks)}')

from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')
checks={
 'ui12_marker':'name="living-dex-ui" content="1.2"' in html,
 'core_marker':'name="living-dex-build" content="core-1.0"' in html,
 'context_headers':'UI12_SCREENS' in html and 'function ui12Intro' in html,
 'home_shortcuts':'function ui12HomeShortcuts' in html and html.count('class="quick-tile"')>=4,
 'dex_switch':'function ui12DexSwitch' in html and 'Somente faltando' in html,
 'all_9_views':all(f" {v}:['" in html for v in ['home','games','global','missing','families','planner','forms','storage','settings']),
 'mobile_nav_preserved':len(re.findall(r'class="mnav-item(?: active)?"',html))==5,
 'desktop_tabs_preserved':len(re.findall(r'class="tab(?: active)?" data-v="',html))==9,
 'touch_targets':'min-height:44px' in html,
 'sheet_mobile':'sheet-head' in html and 'safe-area-inset-bottom' in html,
 'core_functions':all(x in html for x in ['function backup()','function createSnapshot','function addSpecimenInstance','function renderFormDex','function deriveAcquisition']),
 'no_gamification':all(x not in html for x in ['Sistema de missões','Cronômetro de missão','XP de usuário']),
}
failed=[k for k,v in checks.items() if not v]
print({'passed':len(checks)-len(failed),'total':len(checks),'failed':failed})
if failed: raise SystemExit('UI 1.2 validation failed: '+', '.join(failed))

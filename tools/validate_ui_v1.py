from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')
checks={
 'ui_marker':any(f'name="living-dex-ui" content="{v}"' in html for v in ['1.1','1.2','1.3','1.4']),
 'core_preserved':'name="living-dex-build" content="core-1.0"' in html and ('BUILD_QA_VALIDATED=false' in html or 'BUILD_QA_VALIDATED=true' in html),
 'desktop_tabs_9':len(re.findall(r'class="tab(?: active)?" data-v="',html))==9,
 'mobile_nav_5':len(re.findall(r'class="mnav-item(?: active)?"',html))==5,
 'mobile_more_5':all(x in html for x in ["go('families')","go('planner')","go('forms')","go('storage')","go('settings')"]),
 'mobile_nav_sync':'function syncMobileNav(v)' in html and 'syncMobileNav(v);' in html,
 'mobile_more_close':'function closeMobileMore()' in html and 'id="mobileMoreBackdrop"' in html,
 'responsive_grid':'@media(max-width:700px)' in html and '.dexgrid{grid-template-columns:repeat(3' in html,
 'small_phone_grid':'@media(max-width:390px)' in html and 'repeat(2,minmax(0,1fr))' in html,
 'toolbar_sticky':'.toolbar{position:sticky' in html,
 'bottom_nav_safe_area':'env(safe-area-inset-bottom)' in html,
 'core_views_preserved':all(f'id="{v}"' in html for v in ['home','games','global','missing','families','planner','forms','storage','settings']),
 'core_functions_preserved':all(x in html for x in ['function backup()','function createSnapshot','function addSpecimenInstance','function renderFormDex','function deriveAcquisition'])}
failed=[k for k,v in checks.items() if not v]
print({'passed':len(checks)-len(failed),'total':len(checks),'failed':failed})
if failed: raise SystemExit('UI 1.1 regression validation failed: '+', '.join(failed))

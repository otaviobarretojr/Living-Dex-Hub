from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'app'/'src'/'main'/'assets'/'index.html').read_text(encoding='utf-8')
checks={
 'ui_marker':any(f'name="living-dex-ui" content="{v}"' in html for v in ['1.3','1.4','1.5']),
 'core_preserved':'name="living-dex-build" content="core-1.0"' in html,
 'profile_focus':'Living Dex Hub UI 1.3 — Pokemon profile focus pass' in html,
 'sheet_mobile_height':'max-height:96dvh' in html,
 'sheet_safe_area':'env(safe-area-inset-bottom)' in html,
 'sheet_overscroll':'overscroll-behavior:contain' in html,
 'touch_inputs':'.sheet input,.sheet select,.sheet textarea,.sheet button{font-size:16px}' in html,
 'image_fit':'.sheet img{object-fit:contain' in html,
 'ui12_preserved':'UI12_SCREENS' in html and 'quick-strip' in html and 'dex-switch' in html,
 'mobile_nav_preserved':'class="mobile-nav"' in html and 'function syncMobileNav(v)' in html,
 'core_functions':all(x in html for x in ['function backup()','function addSpecimenInstance','function deriveAcquisition'])}
failed=[k for k,v in checks.items() if not v]
print({'passed':len(checks)-len(failed),'total':len(checks),'failed':failed})
if failed: raise SystemExit('UI 1.3 regression validation failed: '+', '.join(failed))

from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'app/src/main/assets/index.html').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/home-v8.css').read_text(encoding='utf-8')
js=(ROOT/'app/src/main/assets/home-v8.js').read_text(encoding='utf-8')
ds=(ROOT/'app/src/main/assets/design-system-v8.css').read_text(encoding='utf-8')
shell=(ROOT/'app/src/main/assets/shell-v8.css').read_text(encoding='utf-8')

checks={
 'phase marker':'living-dex-design-phase" content="F1-home-premium"' in html,
 'shell marker':'living-dex-shell" content="F1.1-fullscreen-dock"' in html,
 'design system linked':'href="design-system-v8.css"' in html,
 'home css linked':'href="home-v8.css"' in html,
 'shell css linked':'href="shell-v8.css"' in html,
 'home js linked':'src="home-v8.js"' in html,
 'six games':all(k in js for k in ["sv:","za:","swsh:","bdsp:","letsgo:","arceus:"]),
 'six cards contract':"gameCards:root?.querySelectorAll('.ld8-game').length" in js,
 'real progress hook':"home77Progress" in js,
 'box continue hook':"ld71Open" in js,
 'game loader hook':"ld73LoadGame" in js,
 'game selector hook':"ld72OpenGames" in js,
 'home sync hook':"renderActiveGameHome" in js and "ld75CommitBox" in js,
 'hero component':'.ld8-hero{' in css,
 '3x2 games grid':'grid-template-columns:repeat(3,minmax(0,1fr))' in css,
 'legacy home hidden':'#home> :not(#ld8Home){display:none!important}' in css,
 'fullscreen wrap':'.wrap{width:100%!important;max-width:none!important' in shell,
 'legacy chrome hidden':'.wrap>.top,.wrap>.nav,.wrap>.mobile-nav' in shell,
 'fixed bottom dock':'position:fixed!important;' in shell and 'bottom:0!important;' in shell,
 'edge-to-edge dock':'left:0!important;right:0!important;' in shell and 'border-radius:0!important' in shell,
 'two-column dock':'grid-template-columns:repeat(2,minmax(0,1fr))' in shell,
 'mobile safe area':'env(safe-area-inset-bottom)' in shell,
 'design action token':'--ld-action:#FF3946' in ds,
 'canonical preserved':'living-dex-canonical-baseline" content="7.14.0"' in html,
 'box integrity preserved':'living-dex-integrity-ux" content="7.11.0"' in html,
 'detail fix preserved':'living-dex-detail-overlay-fix" content="7.12.5"' in html,
 'music preserved':'living-dex-personal-music" content="7.12.0"' in html,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK  ' if v else 'FAIL')+k)
if failed:raise SystemExit('F1.1 validation failed: '+', '.join(failed))
print(f'PHASE F1.1 FULLSCREEN + DOCK: {len(checks)}/{len(checks)} checks OK')

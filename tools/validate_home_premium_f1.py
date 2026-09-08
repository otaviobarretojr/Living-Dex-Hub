from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'app/src/main/assets/index.html').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/home-v8.css').read_text(encoding='utf-8')
js=(ROOT/'app/src/main/assets/home-v8.js').read_text(encoding='utf-8')
ctx=(ROOT/'app/src/main/assets/game-context-v8.js').read_text(encoding='utf-8')
ds=(ROOT/'app/src/main/assets/design-system-v8.css').read_text(encoding='utf-8')
shell=(ROOT/'app/src/main/assets/shell-v8.css').read_text(encoding='utf-8')
selcss=(ROOT/'app/src/main/assets/game-selector-v8.css').read_text(encoding='utf-8')
seljs=(ROOT/'app/src/main/assets/game-selector-v8.js').read_text(encoding='utf-8')
checks={
 'phase marker':'living-dex-design-phase" content="F1-home-premium"' in html,
 'shell marker':'living-dex-shell" content="F1.1-fullscreen-dock"' in html,
 'context marker':'living-dex-game-context" content="F1.3-primary-vs-consultation"' in html,
 'selector marker':'living-dex-game-selector" content="F2-explicit-primary"' in html,
 'design system linked':'href="design-system-v8.css"' in html,
 'home css linked':'href="home-v8.css"' in html,
 'shell css linked':'href="shell-v8.css"' in html,
 'selector css linked':'href="game-selector-v8.css"' in html,
 'context js linked':'src="game-context-v8.js"' in html,
 'selector js linked':'src="game-selector-v8.js"' in html,
 'home js linked':'src="home-v8.js"' in html,
 'load order':html.find('src="game-context-v8.js"') < html.find('src="game-selector-v8.js"') < html.find('src="home-v8.js"'),
 'six games':all(k in js for k in ["sv:","za:","swsh:","bdsp:","letsgo:","arceus:"]),
 'six cards contract':"gameCards:root?.querySelectorAll('.ld8-game').length" in js,
 'real progress hook':"home77Progress" in js,
 'primary home hook':'ld813PrimaryGameId' in js,
 'continue primary hook':'ld813ContinuePrimary' in js,
 'explicit primary selector':'ld813OpenPrimarySelector' in js,
 'browse selector':'ld813OpenConsultSelector' in js,
 'card consultation':'ld813ConsultGame' in js,
 'primary persistent key':"PRIMARY_KEY='ld8.primaryGame'" in ctx,
 'box context persistent key':"BOX_KEY='ld8.boxContextGame'" in ctx,
 'explicit primary setter':'window.ld813SetPrimaryGame=selectPrimary' in ctx,
 'box context getter':'window.ld813BoxContextId=boxId' in ctx,
 'selector mode split':"mode==='primary'" in ctx and "openSelector('box')" in ctx,
 'state restored to primary':'restorePrimary()' in ctx,
 'detail context runtime preserved':'currentGame?.id' in ctx and 'detailContextUsesRuntime' in ctx,
 'f2 selector overrides only primary':'window.ld813OpenPrimarySelector=open' in seljs,
 'f2 uses explicit primary setter':'ld813SetPrimaryGame' in seljs,
 'f2 preserves consultation':'ld813OpenConsultSelector' in seljs,
 'f2 six choices':all(k+":" in seljs for k in ['sv','za','swsh','bdsp','letsgo','arceus']),
 'f2 modal':'position:fixed' in selcss and '.ld82-grid' in selcss,
 'hero component':'.ld8-hero{' in css,
 '3x2 games grid':'grid-template-columns:repeat(3,minmax(0,1fr))' in css,
 'legacy home hidden':'#home> :not(#ld8Home){display:none!important}' in css,
 'fullscreen wrap':'.wrap{width:100%!important;max-width:none!important' in shell,
 'legacy chrome hidden':'.wrap>.top,.wrap>.nav,.wrap>.mobile-nav' in shell,
 'legacy injected appbars quarantined':'#v3Appbar,#r4Appbar,.v3-appbar,.v4-appbar' in shell,
 'legacy audio quick actions quarantined':'#ldhAudioQuick,#ldh712MusicQuick,.audio-quick' in shell,
 'fixed bottom dock':'position:fixed!important;' in shell and 'bottom:0!important;' in shell,
 'two-column dock':'grid-template-columns:repeat(2,minmax(0,1fr))' in shell,
 'canonical preserved':'living-dex-canonical-baseline" content="7.14.0"' in html,
 'box integrity preserved':'living-dex-integrity-ux" content="7.11.0"' in html,
 'detail fix preserved':'living-dex-detail-overlay-fix" content="7.12.5"' in html,
 'music preserved':'living-dex-personal-music" content="7.12.0"' in html,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK  ' if v else 'FAIL')+k)
if failed:raise SystemExit('F2 validation failed: '+', '.join(failed))
print(f'PHASE F2 EXPLICIT PRIMARY SELECTOR: {len(checks)}/{len(checks)} checks OK')

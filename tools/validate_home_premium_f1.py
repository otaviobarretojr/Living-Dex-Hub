from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'app/src/main/assets/index.html').read_text()
home=(ROOT/'app/src/main/assets/home-v8.js').read_text()
ctx=(ROOT/'app/src/main/assets/game-context-v8.js').read_text()
sel=(ROOT/'app/src/main/assets/game-selector-v8.js').read_text()
css=(ROOT/'app/src/main/assets/game-selector-v8.css').read_text()
shell=(ROOT/'app/src/main/assets/shell-v8.css').read_text()
checks={
'canonical':'living-dex-canonical-baseline" content="7.14.0"' in html,
'f2 marker':'living-dex-game-selector" content="F2-explicit-primary"' in html,
'load order':html.find('src="game-context-v8.js"') < html.find('src="game-selector-v8.js"') < html.find('src="home-v8.js"'),
'primary persistent':"PRIMARY_KEY='ld8.primaryGame'" in ctx,
'box persistent':"BOX_KEY='ld8.boxContextGame'" in ctx,
'primary event':"ld:primary-game-changed" in ctx,
'consult independent':'ld813ConsultGame=consultBox' in ctx,
'box hook':'window.ld71Open=async function()' in ctx,
'direct loader':'ld813LoadContextDirect=loadContextDirect' in ctx and 'directContextLoader:true' in ctx,
'no legacy openGame':'openGame(' not in ctx and 'ld73LoadGame' not in ctx,
'direct box opener':'ld813DirectOpenBox=directOpenBox' in ctx and 'directBoxOpen:true' in ctx,
'direct box closer':'ld813DirectCloseBox=directCloseBox' in ctx and 'directBoxClose:true' in ctx,
'legacy close overridden':'window.ld71Close=directCloseBox' in ctx,
'box forced visible':"box.style.display='block'" in ctx and "box.style.visibility='visible'" in ctx,
'box forced hidden':"box.style.display='none'" in ctx and "box.style.visibility='hidden'" in ctx and "box.style.pointerEvents='none'" in ctx,
'body box class removed':"classList.remove('ld7121-box','game-dex-focus')" in ctx,
'back capture':"#ld71BoxView .ld71-back" in ctx and 'stopImmediatePropagation' in ctx,
'home restored':"home.style.display='block'" in ctx and "home.removeAttribute('hidden')" in ctx,
'dock restored':"nav.removeAttribute('inert')" in ctx and "nav.setAttribute('aria-hidden','false')" in ctx,
'selectors hard hidden':"el.style.display='none'" in ctx,
'detail runtime':'detailContextUsesRuntime:true' in ctx,
'context version':"version:'8.0-f2.4'" in ctx,
'selector setter':'ld813SetPrimaryGame' in sel,
'library function':'ld82OpenGameLibrary' in sel,
'fullscreen library':'.ld82-selector.library-mode' in css and 'min-height:100dvh' in css,
'home cards visual only':'visual-only' in home,
'no home card click handler':"querySelectorAll('[data-ld8-game]').forEach" not in home,
'ver todos library':'ld82OpenGameLibrary' in home,
'continue primary':'ld813ContinuePrimary' in home,
'primary selector':'ld813OpenPrimarySelector' in home,
'six games':all(k in home for k in ['sv:','za:','swsh:','bdsp:','letsgo:','arceus:']),
'legacy chrome hidden':'#v3Appbar,#r4Appbar' in shell,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK  ' if v else 'FAIL')+k)
if failed:raise SystemExit('F2.4 validation failed: '+', '.join(failed))
print(f'PHASE F2.4 DIRECT BOX RETURN: {len(checks)}/{len(checks)} checks OK')

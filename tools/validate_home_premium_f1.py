from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'app/src/main/assets/index.html').read_text();home=(ROOT/'app/src/main/assets/home-v8.js').read_text();ctx=(ROOT/'app/src/main/assets/game-context-v8.js').read_text();sel=(ROOT/'app/src/main/assets/game-selector-v8.js').read_text();css=(ROOT/'app/src/main/assets/game-selector-v8.css').read_text();shell=(ROOT/'app/src/main/assets/shell-v8.css').read_text()
checks={
'canonical':'living-dex-canonical-baseline" content="7.14.0"' in html,
'f25 marker':'living-dex-context-architecture" content="F2.5-independent"' in html,
'load order':html.find('src="game-context-v8.js"')<html.find('src="game-selector-v8.js"')<html.find('src="home-v8.js"'),
'primary persistent':"PRIMARY_KEY='ld8.primaryGame'" in ctx,
'box persistent':"BOX_KEY='ld8.boxContextGame'" in ctx,
'primary setter':'ld813SetPrimaryGame=setPrimary' in ctx,
'box setter':'ld813SetBoxGame=setBoxGame' in ctx,
'primary no runtime':'primaryDoesNotLoadRuntime:true' in ctx,
'box runtime':'boxLoadsRuntime:true' in ctx,
'box restores primary state':'writeActive(primaryId());return ok' in ctx,
'primary selector dedicated':"ld82OpenGameSelector?.('primary')" in ctx and "ld82OpenPrimarySelector=()=>open('primary')" in sel,
'box selector dedicated':"ld82OpenGameSelector?.('box')" in ctx and "ld82OpenBoxSelector=()=>open('box')" in sel,
'box selection reopens':"ld813SetBoxGame?.(id,{open:true})" in sel,
'box change event':'ld:box-game-changed' in ctx,
'primary change event':'ld:primary-game-changed' in ctx,
'box header interception':"text.includes('trocar jogo')" in ctx,
'direct box open':'ld813DirectOpenBox=openBoxView' in ctx,
'direct box close':'ld813DirectCloseBox=closeBox' in ctx and 'window.ld71Close=closeBox' in ctx,
'context version':"version:'8.0-f2.5'" in ctx,
'selector version':"version:'8.0-f2.5'" in sel,
'detail runtime':'detailContextUsesRuntime:true' in ctx,
'library':'ld82OpenGameLibrary' in sel and '.ld82-selector.library-mode' in css,
'home visual only':'visual-only' in home,
'continue primary':'ld813ContinuePrimary' in home,
'primary selector home':'ld813OpenPrimarySelector' in home,
'legacy chrome hidden':'#v3Appbar,#r4Appbar' in shell,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK  ' if v else 'FAIL')+k)
if failed:raise SystemExit('F2.5 validation failed: '+', '.join(failed))
print(f'PHASE F2.5 INDEPENDENT CONTEXTS: {len(checks)}/{len(checks)} checks OK')

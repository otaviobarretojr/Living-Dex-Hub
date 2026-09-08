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
'commit primary first':'primaryCommittedFirst:true' in ctx and 'setPrimaryRaw(id);saveKey(BOX_KEY,id)' in ctx,
'primary event':"ld:primary-game-changed" in ctx,
'consult independent':'ld813ConsultGame=consultBox' in ctx,
'box hook':'window.ld71Open=async function()' in ctx,
'detail runtime':'detailContextUsesRuntime:true' in ctx,
'selector version':"version:'8.0-f2.1'" in sel,
'selector setter':'ld813SetPrimaryGame' in sel,
'library function':'ld82OpenGameLibrary' in sel,
'fullscreen library':'.ld82-selector.library-mode' in css and 'min-height:100dvh' in css,
'home cards visual only':'class="ld8-game ${active?\'active\':\'\'} visual-only"' in home,
'no home card click handler':"querySelectorAll('[data-ld8-game]').forEach" not in home,
'ver todos library':'ld82OpenGameLibrary' in home,
'continue primary':'ld813ContinuePrimary' in home,
'primary selector':'ld813OpenPrimarySelector' in home,
'six games':all(k in home for k in ['sv:','za:','swsh:','bdsp:','letsgo:','arceus:']),
'legacy chrome hidden':'#v3Appbar,#r4Appbar' in shell,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items():print(('OK  ' if v else 'FAIL')+k)
if failed:raise SystemExit('F2.1 validation failed: '+', '.join(failed))
print(f'PHASE F2.1: {len(checks)}/{len(checks)} checks OK')

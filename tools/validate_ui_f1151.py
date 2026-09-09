#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ui=(ROOT/'app/src/main/assets/ui-stability-f1151.js').read_text(encoding='utf-8')
page=(ROOT/'app/src/main/assets/national-livingdex-v8.js').read_text(encoding='utf-8')
css=(ROOT/'app/src/main/assets/national-livingdex-v8.css').read_text(encoding='utf-8')
loader=(ROOT/'app/src/main/assets/collection-reliability-v8.js').read_text(encoding='utf-8')
assert "version:'8.0-f11.6'" in ui
for marker in ['persistentThirdDock:true','legacyDockClassPreserved:true','livingDexClickFunctional:true','standaloneNationalDexRoute:true','legacyGlobalBypassed:true','activeDockNormalized:true']:
    assert marker in ui, marker
assert "window.ld8NationalDexOpen" in ui
assert "version:'8.0-f11.8'" in page
for marker in ['standalonePage:true','nationalOrder:true','total:TOTAL','offlineCore:true','allPokemonCards:true','providerAvailability:true','ownedGamePriority:true','lightThemeOnly:true','noDarkTheme:true','fullscreenPokemonDetail:true','staticHeader:true','gridOnlyScroll:true','bottomNavHiddenInsideDex:true','androidBackBridge:true','originAwareBack:true','versionDetailReturn:true','legacyDetailReturnBridge:true']:
    assert marker in page, marker
assert 'for(let id=1;id<=TOTAL;id++)' in page
assert 'Onde está disponível' in page
assert 'src="assets/pokemon/${id}.png"' in page
assert 'data-page-back' in page and 'navigateOrigin()' in page
assert 'id="ld8ndDetail"' in page and 'openPokemonDetail' in page and 'closePokemonDetail' in page
assert 'window.androidHandleBack=function()' in page
assert 'window.closeModal=function()' in page
assert 'restoreFromLegacyDetail' in page
assert 'national-livingdex-v8.js' in loader and 'national-livingdex-v8.css' in loader
for marker in ['.ld8nd-page{position:fixed;inset:0;z-index:8800;display:flex;flex-direction:column;overflow:hidden','.ld8nd-static{flex:0 0 auto','.ld8nd-scroll{flex:1 1 auto;min-height:0;overflow-y:auto','.ld8nd-detail{position:fixed;inset:0','.ld8-national-open .mnav.ld79-nav{display:none!important}']:
    assert marker in css, marker
assert '.ld8nd-own-nav' not in css
assert '#07111b' not in css and '#0a1622' not in css and '#0c1824' not in css
assert 'background:linear-gradient(180deg,#ffffff 0%,#f4f7fa 100%)' in css
print('UI F11.8 VALIDATION: PASS • static header • grid-only scroll • no bottom nav in Dex • Android back • version detail return')

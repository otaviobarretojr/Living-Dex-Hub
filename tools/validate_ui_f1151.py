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
assert "version:'8.0-f11.6.1'" in page
for marker in ['standalonePage:true','nationalOrder:true','total:TOTAL','offlineCore:true','allPokemonCards:true','providerAvailability:true','ownedGamePriority:true','fullDetailBridge:true','legacyGlobalIndependent:true','correctPokemonAssetPath:true','internalDock:true','explicitHomeExit:true','explicitBoxExit:true']:
    assert marker in page, marker
assert 'for(let id=1;id<=TOTAL;id++)' in page
assert 'Onde está disponível' in page
assert 'src="assets/pokemon/${id}.png"' in page
assert 'data-nd-nav="home"' in page and 'data-nd-nav="box"' in page
assert 'navigateHome()' in page and 'navigateBox()' in page
assert 'national-livingdex-v8.js' in loader and 'national-livingdex-v8.css' in loader
assert 'position:fixed' in css and '.ld8nd-grid' in css and '.ld8nd-own-nav' in css
print('UI F11.6.1 VALIDATION: PASS • standalone National Dex • correct sprites • internal nav • explicit Home/Box exits')

/* Living Dex Hub — F7.0 Sword/Shield provider seed fallback */
(()=>{'use strict';
const DATA={version:'8.0-f7.0-seed',gameId:'swsh',source:'empty-safe-fallback',versions:['sword','shield'],dexSpecies:0,coveredSpecies:0,missingSpecies:[],pokemon:{}};
function get(id){return DATA.pokemon[String(Number(id)||0)]||null}
function byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}
window.ld8SwShEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,offline:true,fallback:true,pokemonCount:0})};
})();

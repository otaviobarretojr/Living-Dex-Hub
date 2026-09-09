/* Living Dex Hub — F8.0 BDSP acquisition fallback; replaced by build generator in CI */
(()=>{'use strict';
const DATA={version:'8.0-f8.0-seed',gameId:'bdsp',source:'fallback-seed',versions:['diamond','pearl'],dexSpecies:151,coveredSpecies:3,missingSpecies:[],pokemon:{
'387':{encounters:[{location:'Lake Verity · escolha inicial',method:'gift',levelMin:5,levelMax:5,rate:null,versions:['diamond','pearl'],conditions:['choose-one-starter'],provenance:'verified-game-mechanic'}]},
'390':{encounters:[{location:'Lake Verity · escolha inicial',method:'gift',levelMin:5,levelMax:5,rate:null,versions:['diamond','pearl'],conditions:['choose-one-starter'],provenance:'verified-game-mechanic'}]},
'393':{encounters:[{location:'Lake Verity · escolha inicial',method:'gift',levelMin:5,levelMax:5,rate:null,versions:['diamond','pearl'],conditions:['choose-one-starter'],provenance:'verified-game-mechanic'}]}}};
function get(id){return DATA.pokemon[String(Number(id)||0)]||null}
function byVersion(id,version){const p=get(id);if(!p)return[];return(p.encounters||[]).filter(e=>!version||(e.versions||[]).includes(version))}
window.ld8BdspEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:'bdsp',fallback:true})};
})();

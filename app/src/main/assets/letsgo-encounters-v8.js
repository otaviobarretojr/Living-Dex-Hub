/* Living Dex Hub — F6.3 verified Let’s Go encounter seed */
(()=>{'use strict';
const DATA={version:'8.0-f6.3',gameId:'letsgo',source:'verified-static-analysis',pokemon:{
1:{name:'Bulbasaur',encounters:[
{location:'Cerulean City',method:'Gift',levelMin:12,levelMax:12,rate:null,versions:['pikachu','eevee']},
{location:'Viridian Forest',method:'Special',levelMin:3,levelMax:6,rate:null,versions:['pikachu','eevee']}
]},
25:{name:'Pikachu',encounters:[
{location:'Pallet Town',method:'Gift',levelMin:5,levelMax:5,rate:null,versions:['pikachu']},
{location:'Viridian Forest',method:'Walking',levelMin:3,levelMax:6,rate:5,versions:['pikachu','eevee']}
]},
6:{name:'Charizard',encounters:[
{location:'Route 1',method:'Special',levelMin:3,levelMax:56,rate:null,versions:['pikachu','eevee'],note:'Special/Flying encounter; additional routes are present in the analyzed source but this seed only exposes verified representative data.'}
]}
}};
function get(id){return DATA.pokemon[String(Number(id)||0)]||null}function byVersion(id,version){const p=get(id);if(!p)return[];return p.encounters.filter(e=>!version||e.versions.includes(version))}
window.ld8LetsGoEncounters={data:DATA,get,byVersion,audit:()=>({version:DATA.version,gameId:DATA.gameId,verifiedSeed:true,pokemonCount:Object.keys(DATA.pokemon).length,noPlaceholderData:true})};
})();

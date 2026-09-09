/* Living Dex Hub — F9.0 generic acquisition provider registry */
(()=>{'use strict';
const providers=new Map();
function normalizeId(v){return String(v||'').trim().toLowerCase()}
function validProvider(p){return !!p&&typeof p.get==='function'}
function register(gameId,provider){const id=normalizeId(gameId);if(!id||!validProvider(provider))return false;providers.set(id,provider);try{window.dispatchEvent(new CustomEvent('ld:acquisition-provider-registered',{detail:{gameId:id}}))}catch(e){}return true}
function unregister(gameId){return providers.delete(normalizeId(gameId))}
function ensureBuiltins(){
 if(!providers.has('letsgo')&&window.ld8LetsGoEncounters){const src=window.ld8LetsGoEncounters;register('letsgo',{gameId:'letsgo',label:"Let's Go Pikachu / Eevee",versions:['pikachu','eevee'],get:id=>src.get?.(id)||null,byVersion:(id,v)=>src.byVersion?.(id,v)||[],meta:()=>src.data||{},audit:()=>src.audit?.()||{}})}
 if(!providers.has('swsh')&&window.ld8SwShEncounters){const src=window.ld8SwShEncounters;register('swsh',{gameId:'swsh',label:'Pokémon Sword / Shield',versions:['sword','shield'],get:id=>src.get?.(id)||null,byVersion:(id,v)=>src.byVersion?.(id,v)||[],meta:()=>src.data||{},audit:()=>src.audit?.()||{}})}
 if(!providers.has('bdsp')&&window.ld8BdspEncounters){const src=window.ld8BdspEncounters;register('bdsp',{gameId:'bdsp',label:'Pokémon Brilliant Diamond / Shining Pearl',versions:['diamond','pearl'],get:id=>src.get?.(id)||null,byVersion:(id,v)=>src.byVersion?.(id,v)||[],meta:()=>src.data||{},audit:()=>src.audit?.()||{}})}
 if(!providers.has('arceus')&&window.ld8PlaEncounters){const src=window.ld8PlaEncounters;register('arceus',{gameId:'arceus',label:'Pokémon Legends: Arceus',versions:['arceus'],get:id=>src.get?.(id)||null,byVersion:(id,v)=>src.byVersion?.(id,v)||[],meta:()=>src.data||{},audit:()=>src.audit?.()||{}})}
 return providers
}
function provider(gameId){ensureBuiltins();return providers.get(normalizeId(gameId))||null}
function get(gameId,pokemonId){return provider(gameId)?.get?.(pokemonId)||null}
function list(){ensureBuiltins();return [...providers.entries()].map(([gameId,p])=>({gameId,label:p.label||gameId,versions:[...(p.versions||[])],ready:true}))}
function currentGameId(){try{const x=window.ld813ConsultGameId?.()||window.ld813BoxContextId?.()||window.currentGame?.id||'';if(x)return normalizeId(x)}catch(e){}return''}
function resolveForPokemon(pokemonId,preferredGameId){ensureBuiltins();const first=normalizeId(preferredGameId||currentGameId());if(first){const p=provider(first),data=p?.get?.(pokemonId);if(data)return{gameId:first,provider:p,data}}for(const [gameId,p] of providers){const data=p.get?.(pokemonId);if(data)return{gameId,provider:p,data}}return null}
window.ld8AcquisitionProviders={register,unregister,provider,get,list,currentGameId,resolveForPokemon,ensureBuiltins,audit:()=>{ensureBuiltins();return{version:'8.0-f9.0',genericRegistry:true,providerCount:providers.size,providers:[...providers.keys()],letsGoAdapter:providers.has('letsgo'),swordShieldAdapter:providers.has('swsh'),bdspAdapter:providers.has('bdsp'),legendsArceusAdapter:providers.has('arceus'),multiGameReady:true}}};
ensureBuiltins();setTimeout(ensureBuiltins,0);setTimeout(ensureBuiltins,250);
})();

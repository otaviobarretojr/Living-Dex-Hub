/* Living Dex Hub — F3.8 BETA Pokemon Alive: Paldea starter families */
(()=>{'use strict';
const BETA_IDS=new Set([906,907,908,909,910,911,912,913,914]);
let audio=null,token=0;
const q=(s,r=document)=>r.querySelector(s);
function pokemonId(){try{return Number(currentPokemon?.id||window.currentPokemon?.id||0)}catch(e){return Number(window.currentPokemon?.id||0)}}
function supported(){return BETA_IDS.has(pokemonId())}
function hero(){return q('#modal .poke-hero')}
function image(){return q('#modal .poke-hero img')}
function stop(){if(audio){try{audio.pause();audio.currentTime=0}catch(e){}audio=null}}
function ensure(){const h=hero(),img=image();if(!h||!img)return;const ok=supported();h.classList.toggle('ld8f38-alive',ok);h.classList.toggle('ld8f38-beta',ok);img.classList.toggle('ld8f38-mon',ok);if(ok){img.setAttribute('role','button');img.setAttribute('tabindex','0');img.setAttribute('aria-label','Ouvir o som deste Pokémon');if(!q('.ld8f38-hint',h)){const x=document.createElement('span');x.className='ld8f38-hint';x.textContent='Toque no Pokémon para ouvir';h.appendChild(x)}}else{img.removeAttribute('role');img.removeAttribute('tabindex');img.removeAttribute('aria-label');q('.ld8f38-hint',h)?.remove();stop()}}
async function cry(){if(!supported())return;const id=pokemonId(),my=++token,img=image();stop();img?.classList.remove('ld8f38-react');void img?.offsetWidth;img?.classList.add('ld8f38-react');try{const data=await fetch('https://pokeapi.co/api/v2/pokemon/'+id).then(r=>r.ok?r.json():Promise.reject(new Error('pokemon')));if(my!==token||id!==pokemonId())return;const src=data?.cries?.latest||data?.cries?.legacy;if(!src)throw new Error('cry');audio=new Audio(src);audio.volume=.72;audio.preload='auto';audio.addEventListener('ended',()=>{img?.classList.remove('ld8f38-react');audio=null},{once:true});await audio.play()}catch(e){img?.classList.remove('ld8f38-react')}}
function tap(e){const img=e.target.closest?.('#modal .poke-hero img');if(!img||!supported())return;e.preventDefault();cry()}
document.addEventListener('click',tap,true);document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches?.('#modal .poke-hero img')&&supported()){e.preventDefault();cry()}},true);
function opened(){stop();setTimeout(ensure,100);setTimeout(ensure,420)}
const oldOpen=window.openPokemon;if(typeof oldOpen==='function')window.openPokemon=function(){const r=oldOpen.apply(this,arguments);opened();return r};const oldBoxOpen=window.ld74OpenPokemon;if(typeof oldBoxOpen==='function')window.ld74OpenPokemon=function(){const r=oldBoxOpen.apply(this,arguments);opened();return r};const oldClose=window.closeModal;if(typeof oldClose==='function')window.closeModal=function(){stop();return oldClose.apply(this,arguments)};window.addEventListener('ld:box-game-changed',()=>setTimeout(ensure,100));setTimeout(()=>{if(q('#modal')?.classList.contains('show'))ensure()},600);
window.ld8f38Audit=()=>({version:'8.0-f3.8-beta',betaOnly:true,paldeaStarterFamilies:true,supportedPokemon:[906,907,908,909,910,911,912,913,914],idleAnimation:true,tapReaction:true,cryOnTapOnly:true,noAutoplay:true,officialCryEndpoint:true,volumeControlled:true,keyboardAccessible:true,unsupportedPokemonUntouched:true});
})();

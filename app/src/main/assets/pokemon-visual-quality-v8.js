/* Living Dex Hub — F5.8 detail visual quality recovery */
(()=>{'use strict';
const TYPE_PT={normal:'NORMAL',fire:'FOGO',water:'ÁGUA',electric:'ELÉTRICO',grass:'PLANTA',ice:'GELO',fighting:'LUTADOR',poison:'VENENOSO',ground:'TERRESTRE',flying:'VOADOR',psychic:'PSÍQUICO',bug:'INSETO',rock:'PEDRA',ghost:'FANTASMA',dragon:'DRAGÃO',dark:'SOMBRIO',steel:'AÇO',fairy:'FADA'};
const ALIAS={normal:'normal',fire:'fire',fogo:'fire',water:'water','água':'water',agua:'water',electric:'electric','elétrico':'electric',eletrico:'electric',grass:'grass',planta:'grass',ice:'ice',gelo:'ice',fighting:'fighting',lutador:'fighting',poison:'poison',venenoso:'poison',ground:'ground',terrestre:'ground',flying:'flying',voador:'flying',psychic:'psychic','psíquico':'psychic',psiquico:'psychic',bug:'bug',inseto:'bug',rock:'rock',pedra:'rock',ghost:'ghost',fantasma:'ghost',dragon:'dragon','dragão':'dragon',dragao:'dragon',dark:'dark',sombrio:'dark',steel:'steel','aço':'steel',aco:'steel',fairy:'fairy',fada:'fairy'};
const q=(s,r=document)=>r.querySelector(s);
function pokemonId(){try{return Number(window.currentPokemon?.id||q('#modal #mNum')?.textContent?.replace(/\D/g,'')||0)}catch(e){return 0}}
function officialArt(id){return 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'+id+'.png'}
function localArt(id){return new URL('assets/pokemon/'+id+'.png',document.baseURI).href}
function restoreArt(){const id=pokemonId(),img=q('#modal .poke-hero img');if(!id||!img)return false;const marker=String(id);if(img.dataset.ld8VisualId!==marker){img.dataset.ld8VisualId=marker;delete img.dataset.ld8VisualFallback}
if(img.dataset.ld8VisualFallback==='1'){if(img.src!==localArt(id))img.src=localArt(id);return true}
const hi=officialArt(id);if(img.src!==hi){img.onerror=()=>{img.dataset.ld8VisualFallback='1';img.onerror=null;img.src=localArt(id)};img.src=hi}
img.style.imageRendering='auto';img.style.objectFit='contain';img.alt=String(q('#modal #mName')?.textContent||'Pokémon');return true}
function translateTypes(){q('#profileTypes')?.querySelectorAll('.type,.badge').forEach(el=>{const raw=String(el.dataset.type||el.textContent||'').trim().toLowerCase();const key=ALIAS[raw]||raw;if(TYPE_PT[key]){el.dataset.type=key;el.textContent=TYPE_PT[key]}})}
function fixSummaryCapitalization(){const p=q('#ld8f37About .ld8f37-entry p');const name=String(q('#modal #mName')?.textContent||'').trim();if(!p||!name)return;const text=p.textContent||'';if(text.toLowerCase().startsWith(name.toLowerCase())&&text.charAt(0)!==text.charAt(0).toUpperCase())p.textContent=text.charAt(0).toUpperCase()+text.slice(1)}
function repair(){if(!q('#modal')?.classList.contains('show'))return;restoreArt();translateTypes();fixSummaryCapitalization()}
function opened(){[40,240,720,1100].forEach(ms=>setTimeout(repair,ms))}
const oldOpen=window.openPokemon;if(typeof oldOpen==='function'&&!oldOpen.__ld8f58){const wrap=function(){const r=oldOpen.apply(this,arguments);opened();return r};wrap.__ld8f58=true;window.openPokemon=wrap}
const oldBoxOpen=window.ld74OpenPokemon;if(typeof oldBoxOpen==='function'&&!oldBoxOpen.__ld8f58){const wrap=function(){const r=oldBoxOpen.apply(this,arguments);opened();return r};wrap.__ld8f58=true;window.ld74OpenPokemon=wrap}
const modal=q('#modal');if(modal)new MutationObserver(()=>requestAnimationFrame(repair)).observe(modal,{attributes:true,attributeFilter:['class'],subtree:true,childList:true});
document.addEventListener('click',e=>{if(e.target.closest?.('[data-ld8f3-tab],#ld75BoxBtn'))setTimeout(repair,20)},true);
setTimeout(repair,800);
window.ld8f58Audit=()=>({version:'8.0-f5.8',officialArtworkPrimary:true,localArtworkFallback:true,offlineSafe:true,typeLabelsPortuguese:true,imageRenderingAuto:true,visualReferencePreserved:true});
})();

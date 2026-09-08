/* Living Dex Hub — F2.4 primary game vs consultation context, direct Box open/close */
(()=>{
'use strict';
const IDS=['sv','za','swsh','bdsp','letsgo','arceus'];
const PRIMARY_KEY='ld8.primaryGame';
const BOX_KEY='ld8.boxContextGame';
let selectorMode=null;
function st(){try{return window.state||state||{}}catch(e){return window.state||{}}}
function valid(id){return IDS.includes(String(id||''))}
function loadKey(k){try{return localStorage.getItem(k)||''}catch(e){return ''}}
function saveKey(k,v){try{localStorage.setItem(k,String(v))}catch(e){}}
function persistState(){try{window.saveState?.()}catch(e){try{window.persist?.()}catch(_){}}}
function initialPrimary(){const s=st();const saved=loadKey(PRIMARY_KEY);if(valid(saved))return saved;const cur=String(s.activeGameId||window.currentGame?.id||'sv');return valid(cur)?cur:'sv'}
let primary=initialPrimary();saveKey(PRIMARY_KEY,primary);
function primaryId(){const saved=loadKey(PRIMARY_KEY);if(valid(saved))primary=saved;return valid(primary)?primary:'sv'}
function boxId(){const saved=loadKey(BOX_KEY);return valid(saved)?saved:primaryId()}
function writeActive(id){if(!valid(id))return;const s=st();s.activeGameId=id;persistState()}
function setPrimaryRaw(id){if(!valid(id))return false;primary=id;saveKey(PRIMARY_KEY,id);writeActive(id);return true}
function restorePrimary(){writeActive(primaryId());try{window.ld8HomeRender?.()}catch(e){}}
const originalSelector=window.ld72OpenGames;
const originalGo=window.go;
window.ld813OriginalGo=originalGo;
function closeAllSelectors(){
 selectorMode=null;
 try{window.ld82ClosePrimarySelector?.()}catch(e){}
 try{window.ld72CloseGames?.()}catch(e){}
 for(const id of ['ld82GameSelector','ld72GameSheet']){
  try{const el=document.getElementById(id);el?.classList.remove('active','library-mode');if(el)el.style.display='none'}catch(e){}
 }
 try{document.documentElement.style.overflow=''}catch(e){}
 try{document.body.style.overflow=''}catch(e){}
}
async function loadContextDirect(id){
 if(!valid(id))return false;
 writeActive(id);
 try{
  const games=(typeof GAMES!=='undefined'&&Array.isArray(GAMES))?GAMES:(Array.isArray(window.GAMES)?window.GAMES:[]);
  const game=games.find(g=>g.id===id);if(!game)return false;
  currentGame=game;
  const list=(typeof dexRegistryFor==='function'?dexRegistryFor(id):[])||[];
  const dex=list[0];if(!dex)return false;
  activeSubdex=dex;
  if(typeof loadSubdex==='function')currentDex=await loadSubdex(game,dex);
  else if(typeof embeddedDexRows==='function')currentDex=embeddedDexRows(id,dex.id)||[];
  if(!Array.isArray(currentDex)||!currentDex.length)return false;
  writeActive(id);
  return currentGame?.id===id&&currentDex.length>0
 }catch(e){console.error('Living Dex Hub direct context load failed',e);return false}
}
function directOpenBox(){
 closeAllSelectors();
 try{if(!document.getElementById('ld71BoxView')&&typeof ld71Ensure==='function')ld71Ensure()}catch(e){}
 const box=document.getElementById('ld71BoxView');if(!box)return false;
 try{document.body.classList.remove('game-dex-focus')}catch(e){}
 box.style.display='block';box.style.visibility='visible';box.style.opacity='1';box.style.pointerEvents='auto';
 box.classList.add('active');box.removeAttribute('hidden');box.setAttribute('aria-hidden','false');
 try{window.ld71Render?.()}catch(e){try{ld71Render()}catch(_){}}
 try{window.ld72Focus?.()}catch(e){try{ld72Focus()}catch(_){}}
 try{document.body.classList.add('ld7121-box')}catch(e){}
 try{window.ld7121SyncNav?.()}catch(e){}
 requestAnimationFrame(()=>{box.style.display='block';box.classList.add('active');try{window.ld71Render?.()}catch(e){}});
 setTimeout(()=>{box.style.display='block';box.classList.add('active')},80);
 return true
}
function directCloseBox(){
 closeAllSelectors();
 const box=document.getElementById('ld71BoxView');
 if(box){
  box.classList.remove('active');
  box.style.display='none';box.style.visibility='hidden';box.style.opacity='0';box.style.pointerEvents='none';
  box.setAttribute('hidden','');box.setAttribute('aria-hidden','true');
 }
 try{document.body.classList.remove('ld7121-box','game-dex-focus')}catch(e){}
 try{document.documentElement.style.overflow=''}catch(e){}
 try{document.body.style.overflow=''}catch(e){}
 writeActive(primaryId());
 const home=document.getElementById('home');
 if(home){home.style.display='block';home.style.visibility='visible';home.removeAttribute('hidden');home.setAttribute('aria-hidden','false')}
 const nav=document.querySelector('.mnav.ld79-nav');
 if(nav){nav.removeAttribute('inert');nav.setAttribute('aria-hidden','false');nav.style.removeProperty('display')}
 try{window.ld8HomeRender?.()}catch(e){}
 try{window.ld7NavState?.()}catch(e){}
 try{window.ld79Render?.()}catch(e){}
 window.scrollTo?.(0,0);
 return !box||!box.classList.contains('active')
}
async function consultBox(id,{open=true}={}){
 if(!valid(id))return false;saveKey(BOX_KEY,id);closeAllSelectors();
 const ok=await loadContextDirect(id);if(!ok)return false;
 return open?directOpenBox():true
}
async function continuePrimary(){const id=primaryId();saveKey(BOX_KEY,id);return consultBox(id,{open:true})}
async function selectPrimary(id){
 if(!valid(id))return false;setPrimaryRaw(id);saveKey(BOX_KEY,id);closeAllSelectors();
 await loadContextDirect(id);setPrimaryRaw(id);
 try{if(typeof originalGo==='function')originalGo('home')}catch(e){}
 try{window.ld8HomeRender?.()}catch(e){}
 try{window.dispatchEvent(new CustomEvent('ld:primary-game-changed',{detail:{id}}))}catch(e){}
 return primaryId()===id
}
function openSelector(mode){selectorMode=mode;if(mode==='primary'&&typeof window.ld82OpenPrimarySelector==='function')return window.ld82OpenPrimarySelector();if(typeof originalSelector!=='function')return;writeActive(mode==='box'?boxId():primaryId());return originalSelector()}
window.ld813PrimaryGameId=primaryId;window.ld813BoxContextId=boxId;window.ld813SetPrimaryGame=selectPrimary;window.ld813ConsultGame=consultBox;window.ld813ContinuePrimary=continuePrimary;window.ld813DirectOpenBox=directOpenBox;window.ld813DirectCloseBox=directCloseBox;window.ld813LoadContextDirect=loadContextDirect;window.ld813OpenPrimarySelector=function(){return openSelector('primary')};window.ld813OpenConsultSelector=function(){return openSelector('box')};
async function contextualSelect(id){const mode=selectorMode||((document.getElementById('ld71BoxView')?.classList.contains('active'))?'box':'primary');closeAllSelectors();return mode==='primary'?selectPrimary(id):consultBox(id,{open:false})}
window.ld73SelectGame=contextualSelect;window.ld72SelectGame=contextualSelect;window.ld71Open=async function(){return consultBox(boxId(),{open:true})};window.ld71Close=directCloseBox;
if(typeof originalGo==='function')window.go=function(dest){if(String(dest)==='home'){directCloseBox();return}return originalGo.apply(this,arguments)};
document.addEventListener('click',e=>{
 const back=e.target.closest?.('#ld71BoxView .ld71-back');if(back){e.preventDefault();e.stopImmediatePropagation();directCloseBox();return}
 const item=e.target.closest?.('.mnav.ld79-nav .ld79-item,.ld7-navbtn[data-ld7="box"]');if(!item)return;
 const txt=(item.textContent||'').trim().toLowerCase();
 if(item.matches?.('[data-ld7="box"]')||txt.includes('box')){e.preventDefault();e.stopImmediatePropagation();window.ld71Open?.();return}
 if(txt.includes('início')||txt.includes('inicio')){e.preventDefault();e.stopImmediatePropagation();directCloseBox()}
},true);
restorePrimary();
window.ld813Audit=function(){const box=document.getElementById('ld71BoxView');return {version:'8.0-f2.4',primaryGame:primaryId(),boxContext:boxId(),runtimeGame:String(window.currentGame?.id||''),stateActive:String(st().activeGameId||''),selectorMode:selectorMode||null,directContextLoader:true,noLegacyOpenGame:true,directBoxOpen:true,directBoxClose:true,boxActive:!!box?.classList.contains('active'),boxDisplay:box?getComputedStyle(box).display:'missing',detailContextUsesRuntime:true}};
})();

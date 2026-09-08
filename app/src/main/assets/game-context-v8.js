/* Living Dex Hub — F2.2 primary game vs consultation context, direct Box opener */
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
const originalLoad=window.ld73LoadGame;
const originalSelector=window.ld72OpenGames;
const originalGo=window.go;
const originalSelect=window.ld73SelectGame||window.ld72SelectGame;
window.ld813OriginalLoadGame=originalLoad;
window.ld813OriginalGo=originalGo;
window.ld813OriginalSelectGame=originalSelect;
async function loadContext(id){
 if(!valid(id))return false;writeActive(id);
 if(typeof originalLoad==='function'){try{return (await originalLoad(id))!==false}catch(e){console.warn('Living Dex Hub context load fallback',e)}}
 if(typeof originalSelect==='function'){try{return (await originalSelect(id))!==false}catch(e){console.warn('Living Dex Hub select fallback',e)}}
 return true
}
function closeAllSelectors(){
 selectorMode=null;
 try{window.ld82ClosePrimarySelector?.()}catch(e){}
 try{window.ld72CloseGames?.()}catch(e){}
 try{document.getElementById('ld82GameSelector')?.classList.remove('active','library-mode')}catch(e){}
 try{document.getElementById('ld72GameSheet')?.classList.remove('active')}catch(e){}
 try{document.documentElement.style.overflow=''}catch(e){}
 try{document.body.style.overflow=''}catch(e){}
}
function directOpenBox(){
 try{if(!document.getElementById('ld71BoxView')&&typeof window.ld71Ensure==='function')window.ld71Ensure()}catch(e){}
 const box=document.getElementById('ld71BoxView');
 if(!box)return false;
 closeAllSelectors();
 try{document.body.classList.remove('game-dex-focus')}catch(e){}
 box.classList.add('active');
 box.removeAttribute('hidden');
 box.setAttribute('aria-hidden','false');
 try{window.ld71Render?.()}catch(e){console.warn('Living Dex Hub Box render failed',e)}
 try{window.ld7121SyncNav?.()}catch(e){}
 try{window.ld7NavState?.()}catch(e){}
 requestAnimationFrame(()=>{try{window.ld71Render?.();window.ld7121SyncNav?.()}catch(e){}});
 return box.classList.contains('active')
}
async function consultBox(id,{open=true}={}){
 if(!valid(id))return false;saveKey(BOX_KEY,id);
 closeAllSelectors();
 const ok=await loadContext(id);if(!ok)return false;
 writeActive(id);
 if(open)return directOpenBox();
 try{window.ld71Render?.()}catch(e){}return true
}
async function continuePrimary(){const id=primaryId();saveKey(BOX_KEY,id);return consultBox(id,{open:true})}
async function selectPrimary(id){
 if(!valid(id))return false;
 setPrimaryRaw(id);saveKey(BOX_KEY,id);closeAllSelectors();
 try{await loadContext(id)}catch(e){}
 setPrimaryRaw(id);
 try{if(typeof originalGo==='function')originalGo('home')}catch(e){}
 try{window.ld8HomeRender?.()}catch(e){}
 try{window.dispatchEvent(new CustomEvent('ld:primary-game-changed',{detail:{id}}))}catch(e){}
 return primaryId()===id
}
function openSelector(mode){
 selectorMode=mode;
 if(mode==='primary'&&typeof window.ld82OpenPrimarySelector==='function')return window.ld82OpenPrimarySelector();
 if(typeof originalSelector!=='function')return;
 writeActive(mode==='box'?boxId():primaryId());
 return originalSelector()
}
window.ld813PrimaryGameId=primaryId;
window.ld813BoxContextId=boxId;
window.ld813SetPrimaryGame=selectPrimary;
window.ld813ConsultGame=consultBox;
window.ld813ContinuePrimary=continuePrimary;
window.ld813DirectOpenBox=directOpenBox;
window.ld813OpenPrimarySelector=function(){return openSelector('primary')};
window.ld813OpenConsultSelector=function(){return openSelector('box')};
if(typeof originalSelector==='function')window.ld72OpenGames=function(){if(!selectorMode){const box=document.getElementById('ld71BoxView');selectorMode=box?.classList.contains('active')?'box':'primary'}return openSelector(selectorMode)};
async function contextualSelect(id){const mode=selectorMode||((document.getElementById('ld71BoxView')?.classList.contains('active'))?'box':'primary');closeAllSelectors();return mode==='primary'?selectPrimary(id):consultBox(id,{open:false})}
window.ld73SelectGame=contextualSelect;window.ld72SelectGame=contextualSelect;
window.ld71Open=async function(){return consultBox(boxId(),{open:true})};
if(typeof originalGo==='function')window.go=function(dest){if(String(dest)==='home')restorePrimary();return originalGo.apply(this,arguments)};
document.addEventListener('click',e=>{const item=e.target.closest?.('.mnav.ld79-nav .ld79-item,.ld7-navbtn[data-ld7="box"]');if(!item)return;const txt=(item.textContent||'').trim().toLowerCase();if(item.matches?.('[data-ld7="box"]')||txt.includes('box')){e.preventDefault();e.stopPropagation();window.ld71Open?.();return}if(txt.includes('início')||txt.includes('inicio'))restorePrimary()},true);
restorePrimary();
window.ld813Audit=function(){const box=document.getElementById('ld71BoxView');return {version:'8.0-f2.2',primaryGame:primaryId(),boxContext:boxId(),runtimeGame:String(window.currentGame?.id||''),stateActive:String(st().activeGameId||''),selectorMode:selectorMode||null,primaryCommittedFirst:true,directBoxOpen:true,boxActive:!!box?.classList.contains('active'),boxOpenHook:typeof window.ld71Open==='function',primarySetter:typeof window.ld813SetPrimaryGame==='function',consultHook:typeof window.ld813ConsultGame==='function',detailContextUsesRuntime:true}};
})();

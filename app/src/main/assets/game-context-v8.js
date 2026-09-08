/* Living Dex Hub — F2.0.1 primary game vs consultation context, interaction-safe */
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
function restorePrimary(){writeActive(primaryId());try{window.ld8HomeRender?.()}catch(e){}}
function setPrimaryRaw(id){if(!valid(id))return false;primary=id;saveKey(PRIMARY_KEY,id);writeActive(id);return true}

const originalLoad=window.ld73LoadGame;
const originalOpen=window.ld71Open;
const originalSelector=window.ld72OpenGames;
const originalGo=window.go;
window.ld813OriginalLoadGame=originalLoad;
window.ld813OriginalOpenBox=originalOpen;
window.ld813OriginalGo=originalGo;

async function loadContext(id){
 if(!valid(id)||typeof originalLoad!=='function')return false;
 writeActive(id);
 try{return (await originalLoad(id))!==false}catch(e){console.error('Living Dex Hub context load failed',e);return false}
}
async function consultBox(id,{open=true}={}){
 if(!valid(id))return false;
 saveKey(BOX_KEY,id);
 const ok=await loadContext(id);if(!ok)return false;
 if(open){
  try{if(typeof originalOpen==='function')await originalOpen();else window.openGame?.(id)}catch(e){console.error('Living Dex Hub Box open failed',e);return false}
 }
 try{window.ld71Render?.()}catch(e){}
 return true
}
async function continuePrimary(){const id=primaryId();saveKey(BOX_KEY,id);return consultBox(id,{open:true})}
async function selectPrimary(id){
 if(!valid(id))return false;
 const prev=primaryId();
 const ok=await loadContext(id);if(!ok){setPrimaryRaw(prev);return false}
 setPrimaryRaw(id);saveKey(BOX_KEY,id);selectorMode=null;
 try{window.ld72CloseGames?.()}catch(e){}
 try{if(typeof originalGo==='function')originalGo('home')}catch(e){}
 try{window.ld8HomeRender?.()}catch(e){}
 return true
}
function openSelector(mode){
 selectorMode=mode;
 if(mode==='primary'&&typeof window.ld82OpenPrimarySelector==='function')return window.ld82OpenPrimarySelector();
 if(typeof originalSelector!=='function')return;
 if(mode==='box')writeActive(boxId());else writeActive(primaryId());
 return originalSelector()
}
window.ld813PrimaryGameId=primaryId;
window.ld813BoxContextId=boxId;
window.ld813SetPrimaryGame=selectPrimary;
window.ld813ConsultGame=consultBox;
window.ld813ContinuePrimary=continuePrimary;
window.ld813OpenPrimarySelector=function(){return openSelector('primary')};
window.ld813OpenConsultSelector=function(){return openSelector('box')};

if(typeof originalSelector==='function')window.ld72OpenGames=function(){
 if(!selectorMode){const box=document.getElementById('ld71BoxView');selectorMode=box?.classList.contains('active')?'box':'primary'}
 return openSelector(selectorMode)
};
async function contextualSelect(id){
 const mode=selectorMode||((document.getElementById('ld71BoxView')?.classList.contains('active'))?'box':'primary');
 selectorMode=null;
 try{window.ld72CloseGames?.()}catch(e){}
 return mode==='primary'?selectPrimary(id):consultBox(id,{open:false})
}
window.ld73SelectGame=contextualSelect;window.ld72SelectGame=contextualSelect;
window.ld71Open=async function(){return consultBox(boxId(),{open:true})};

if(typeof originalGo==='function')window.go=function(dest){
 if(String(dest)==='home'){restorePrimary()}
 return originalGo.apply(this,arguments)
};

/* Safety net for legacy dock handlers that may have been bound before F2 wrappers. */
document.addEventListener('click',e=>{
 const item=e.target.closest?.('.mnav.ld79-nav .ld79-item');if(!item)return;
 const txt=(item.textContent||'').trim().toLowerCase();
 if(txt.includes('box')){e.preventDefault();e.stopPropagation();window.ld71Open?.();return}
 if(txt.includes('início')||txt.includes('inicio')){restorePrimary()}
},true);

restorePrimary();
window.ld813Audit=function(){return {version:'8.0-f2.0.1',primaryGame:primaryId(),boxContext:boxId(),runtimeGame:String(window.currentGame?.id||''),stateActive:String(st().activeGameId||''),selectorMode:selectorMode||null,boxOpenHook:typeof window.ld71Open==='function',primarySetter:typeof window.ld813SetPrimaryGame==='function',consultHook:typeof window.ld813ConsultGame==='function'}};
})();

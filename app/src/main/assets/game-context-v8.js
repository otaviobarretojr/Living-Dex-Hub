/* Living Dex Hub — F1.3 primary game vs consultation context */
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
function boxId(){const saved=loadKey(BOX_KEY);if(valid(saved))return saved;const cg=String(window.currentGame?.id||'');return valid(cg)?cg:primaryId()}
function writeActive(id){const s=st();s.activeGameId=id;persistState()}
function restorePrimary(){writeActive(primaryId());try{window.ld8HomeRender?.()}catch(e){}}
function setPrimaryRaw(id){if(!valid(id))return false;primary=id;saveKey(PRIMARY_KEY,id);writeActive(id);return true}
const originalLoad=window.ld73LoadGame;window.ld813OriginalLoadGame=originalLoad;
const originalOpen=window.ld71Open;window.ld813OriginalOpenBox=originalOpen;
const originalSelector=window.ld72OpenGames;
const originalSelect=window.ld73SelectGame||window.ld72SelectGame;
window.ld813OriginalSelectGame=originalSelect;
async function runtimeLoad(id){if(!valid(id)||typeof originalLoad!=='function')return false;return !!(await originalLoad(id))}
async function consultBox(id,{open=true}={}){
 if(!valid(id))return false;
 saveKey(BOX_KEY,id);const p=primaryId();let ok=false;
 try{ok=await runtimeLoad(id)}catch(e){ok=false}
 if(!ok){primary=p;restorePrimary();return false}
 if(open){
  try{writeActive(id);if(typeof originalOpen==='function')await originalOpen()}catch(e){}finally{primary=p;restorePrimary()}
 }else{primary=p;restorePrimary()}
 try{window.ld71Render?.()}catch(e){}
 return true
}
async function continuePrimary(){const id=primaryId();saveKey(BOX_KEY,id);return consultBox(id,{open:true})}
async function selectPrimary(id){
 if(!valid(id))return false;
 const prev=primaryId();let ok=false;try{ok=await runtimeLoad(id)}catch(e){ok=false}
 if(!ok){setPrimaryRaw(prev);return false}
 setPrimaryRaw(id);saveKey(BOX_KEY,id);selectorMode=null;
 try{window.ld72CloseGames?.()}catch(e){};try{window.go?.('home')}catch(e){};try{window.ld8HomeRender?.()}catch(e){};return true
}
window.ld813PrimaryGameId=primaryId;
window.ld813BoxContextId=boxId;
window.ld813SetPrimaryGame=selectPrimary;
window.ld813ConsultGame=consultBox;
window.ld813ContinuePrimary=continuePrimary;
window.ld813OpenPrimarySelector=function(){selectorMode='primary';if(typeof originalSelector==='function')return originalSelector()};
window.ld813OpenConsultSelector=function(){selectorMode='box';if(typeof originalSelector==='function')return originalSelector()};
if(typeof originalSelector==='function')window.ld72OpenGames=function(){
 if(!selectorMode){const box=document.getElementById('ld71BoxView');selectorMode=box?.classList.contains('active')?'box':'primary'}
 return originalSelector.apply(this,arguments)
};
async function contextualSelect(id){
 const mode=selectorMode||((document.getElementById('ld71BoxView')?.classList.contains('active'))?'box':'primary');
 if(mode==='primary')return selectPrimary(id);
 selectorMode=null;try{window.ld72CloseGames?.()}catch(e){};return consultBox(id,{open:false})
}
window.ld73SelectGame=contextualSelect;window.ld72SelectGame=contextualSelect;
window.ld71Open=async function(){return consultBox(boxId()||primaryId(),{open:true})};
restorePrimary();
window.ld813Audit=function(){return {version:'8.0-f1.3',primaryGame:primaryId(),boxContext:boxId(),runtimeGame:String(window.currentGame?.id||''),stateActive:String(st().activeGameId||''),primaryStable:String(st().activeGameId||'')===primaryId(),selectorMode:selectorMode||null,detailContextUsesRuntime:typeof window.ld711Audit==='function'}};
})();

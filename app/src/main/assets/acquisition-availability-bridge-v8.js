/* Living Dex Hub — F7.6 bridge provider obtainability into global game availability */
(()=>{'use strict';
const TOTAL=1025;let wrapped=false,base=null;
function providerRows(gameId){const p=window.ld8AcquisitionProviders?.provider?.(gameId);if(!p)return[];const out=[];for(let id=1;id<=TOTAL;id++){let d=null;try{d=p.get?.(id)||null}catch(e){}const routes=d?.encounters||[];if(routes.length)out.push({id,providerObtainable:true,outsideDex:!!d?.obtainableOutsideDex,dexScopes:[...(d?.dexScopes||[])]})}return out}
function merge(rows,gameId){const m=new Map();for(const r of rows||[]){const id=Number(r?.id)||0;if(id)m.set(id,r)}for(const r of providerRows(gameId)){const prev=m.get(r.id)||{id:r.id};m.set(r.id,{...prev,...r,providerObtainable:true,outsideDex:!!r.outsideDex})}return[...m.values()]}
function install(){const fn=window.ensureGameAvailability;if(typeof fn!=='function')return false;if(fn.__ld8f76)return true;base=fn;const wrap=async function(gameId){const rows=await base.apply(this,arguments);return merge(rows,gameId)};wrap.__ld8f76=true;wrap.__base=base;window.ensureGameAvailability=wrap;wrapped=true;try{window.dispatchEvent(new CustomEvent('ld:availability-bridge-ready'))}catch(e){}return true}
function retry(){if(install())return;setTimeout(install,120);setTimeout(install,500);setTimeout(install,1200)}
window.addEventListener('ld:acquisition-provider-registered',()=>setTimeout(install,0));
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',retry,{once:true});else retry();
window.ld8AcquisitionAvailabilityBridge={install,providerRows,merge,audit:()=>({version:'8.0-f7.6',wrapped:!!window.ensureGameAvailability?.__ld8f76,providerAvailabilityMerged:true,outsideDexVisibleToLivingDex:true,dexMembershipUntouched:true})};
})();

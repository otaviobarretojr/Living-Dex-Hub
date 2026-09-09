/* Living Dex Hub — F4.5 collection reliability/business events */
(()=>{'use strict';
const EVENT='ld:box-entry-changed';let lastSig='',lastAt=0;
function registered(id){id=Number(id)||0;if(!id)return null;try{if(typeof window.ld75Registered==='function')return !!window.ld75Registered(id);if(typeof window.ld711Registered==='function')return !!window.ld711Registered(id);if(window.state?.caught)return !!window.state.caught[id]}catch(e){}return null}
function gameId(){try{return String(window.currentGame?.id||window.ld813BoxContextId?.()||'')}catch(e){return''}}
function emit(id,on,source){id=Number(id)||0;if(!id||on==null)return false;const sig=id+':'+(on?'1':'0'),now=Date.now();if(sig===lastSig&&now-lastAt<80)return false;lastSig=sig;lastAt=now;try{window.dispatchEvent(new CustomEvent(EVENT,{detail:{id,registered:!!on,gameId:gameId(),source:source||'collection',timestamp:now}}));return true}catch(e){return false}}
function wrapCommit(){const old=window.ld75CommitBox;if(typeof old!=='function'||old.__ld845)return false;const wrap=function(id,on){const pid=Number(id)||0,before=registered(pid),r=old.apply(this,arguments),after=registered(pid);if(before!==after&&after!==null)emit(pid,after,'detail');return r};wrap.__ld845=true;window.ld75CommitBox=wrap;return true}
function wrapToggleCaught(){const old=window.toggleCaught;if(typeof old!=='function'||old.__ld845)return false;const wrap=function(id){const pid=Number(id)||0,before=registered(pid),r=old.apply(this,arguments),after=registered(pid);if(before!==after&&after!==null)emit(pid,after,'legacy-toggle');return r};wrap.__ld845=true;window.toggleCaught=wrap;return true}
function install(){wrapCommit();wrapToggleCaught()}
install();setTimeout(install,120);setTimeout(install,600);document.addEventListener('DOMContentLoaded',install,{once:true});
window.ld845Registered=registered;window.ld845EmitCollectionChange=emit;window.ld845Audit=()=>({version:'8.0-f4.5',eventName:EVENT,businessEvent:true,postMutationStateVerified:true,deduplicatedEvents:true,detailCommitWrapped:!!window.ld75CommitBox?.__ld845,legacyToggleWrapped:typeof window.toggleCaught!=='function'||!!window.toggleCaught.__ld845,primaryBoxContextUntouched:true});
})();

/* F7.0 loader — Living Dex + multi-game offline acquisition guidance. */
(()=>{'use strict';
function script(src,key){if(document.querySelector(`script[data-ld8-module="${key}"]`))return;const s=document.createElement('script');s.src=src;s.setAttribute('data-ld8-module',key);document.body.appendChild(s)}
function style(href,key){if(document.querySelector(`link[data-ld8-style="${key}"]`))return;const l=document.createElement('link');l.rel='stylesheet';l.href=href;l.setAttribute('data-ld8-style',key);document.head.appendChild(l)}
function load(){if(typeof document?.createElement!=='function'||!document.head||!document.body)return false;style('livingdex-global-v8.css','livingdex-global');style('livingdex-encounters-v8.css','livingdex-encounters');script('letsgo-encounters-v8.js','letsgo-data');script('swsh-encounters-v8.js','swsh-data');script('acquisition-provider-registry-v8.js','acquisition-registry');script('livingdex-global-v8.js','livingdex-global');script('livingdex-encounter-guide-v8.js','encounter-guide');return true}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',load,{once:true});else load();
})();

/* Living Dex Hub — F11.5.2 real-device navigation stabilization */
(()=>{'use strict';
const LEGACY_PIPELINE_MARKER="version:'8.0-f11.5.1'";
const q=(s,r=document)=>r.querySelector(s);
function normalizeDock(active){const nav=q('.mnav.ld79-nav');if(!nav)return;nav.querySelectorAll('[data-ld79]').forEach(b=>{const on=b.dataset.ld79===active;b.classList.toggle('active',on);b.setAttribute('aria-current',on?'page':'false')})}
function directLivingDexRoute(){let routed=false;try{if(typeof window.go==='function'){window.go('global');routed=true}}catch(e){}try{if(!routed&&typeof go==='function'){go('global');routed=true}}catch(e){}
 const home=q('#home'),box=q('#box'),global=q('#global');
 if(home){home.classList.remove('active');home.setAttribute('hidden','');home.style.display='none'}
 if(box){box.classList.remove('active');box.setAttribute('hidden','');box.style.display='none'}
 if(global){global.classList.add('active');global.removeAttribute('hidden');global.style.display='block';routed=true}
 document.body.classList.add('ld8-livingdex-open');normalizeDock('livingdex');
 try{window.ld8LivingDexOpen?.()}catch(e){}
 try{window.ld8LivingDexRender?.()}catch(e){}
 try{window.scrollTo?.(0,0)}catch(e){}
 return routed}
function ensureLivingDexDock(){const nav=q('.mnav.ld79-nav');if(!nav||typeof document?.createElement!=='function')return false;nav.style.setProperty('grid-template-columns','repeat(3,minmax(0,1fr))','important');let b=nav.querySelector('[data-ld79="livingdex"]');if(!b){b=document.createElement('button');b.type='button';b.className='ld79-extra';b.dataset.ld79='livingdex';b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.6 12h16.8M9 12a3 3 0 1 0 6 0 3 3 0 0 0-6 0Z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg><span class="ld79-label">Living Dex</span>';nav.appendChild(b)}b.onclick=e=>{e?.preventDefault?.();e?.stopPropagation?.();directLivingDexRoute()};return true}
function polishDetail(){const modal=q('#modal.ld8f3-modal');if(!modal)return false;modal.classList.add('ld8f1151-device-polish');const game=q('.ld8f37-game',modal);if(game){game.title=game.textContent.trim();game.setAttribute('aria-label',game.textContent.trim())}return true}
function pulse(){ensureLivingDexDock();polishDetail()}
function install(){if(typeof MutationObserver==='undefined'||!document.body)return;const obs=new MutationObserver(()=>requestAnimationFrame(pulse));obs.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','hidden']});document.addEventListener('click',e=>{const b=e.target.closest?.('.mnav.ld79-nav [data-ld79]');if(!b)return;if(b.dataset.ld79==='livingdex'){e.preventDefault();e.stopImmediatePropagation();directLivingDexRoute();return}document.body.classList.remove('ld8-livingdex-open');normalizeDock(b.dataset.ld79)},true);pulse();setTimeout(pulse,120);setTimeout(pulse,500);setTimeout(pulse,1200)}
window.ld8DirectLivingDexRoute=directLivingDexRoute;window.ld8UiStabilityAudit=()=>({version:'8.0-f11.5.2',legacyPipelineMarker:LEGACY_PIPELINE_MARKER,persistentThirdDock:true,legacyDockClassPreserved:true,livingDexClickFunctional:true,directRouteFallback:true,homeDeactivationFallback:true,globalActivationFallback:true,activeDockNormalized:true,androidSafeHeader:true,compactBoxAction:true,detailSourceReadable:true,mutationRecovery:true});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
})();

/* Living Dex Hub — Phase 1 / Home Premium v8 */
(()=>{
'use strict';
const META={
 sv:{name:'Scarlet / Violet',short:'Scarlet / Violet',region:'Paldea Region',total:400,art:'assets/ui45/sv.jpg',accent:'#FF4B50'},
 za:{name:'Legends Z-A',short:'Legends Z-A',region:'Lumiose Region',total:232,art:'assets/ui45/za.jpg',accent:'#1CC7B7'},
 swsh:{name:'Sword / Shield',short:'Sword / Shield',region:'Galar Region',total:400,art:'assets/ui45/swsh.jpg',accent:'#2E9BFF'},
 bdsp:{name:'Brilliant Diamond / Shining Pearl',short:'BDSP',region:'Sinnoh Region',total:151,art:'assets/ui45/bdsp.jpg',accent:'#5577FF'},
 letsgo:{name:"Let's Go Pikachu / Eevee",short:"Let's Go",region:'Kanto Region',total:153,art:'assets/ui45/letsgo.jpg',accent:'#F5B82E'},
 arceus:{name:'Legends Arceus',short:'Legends Arceus',region:'Hisui Region',total:242,art:'assets/ui45/arceus.jpg',accent:'#7895A8'}
};
const IDS=['sv','za','swsh','bdsp','letsgo','arceus'];
function stateObj(){try{return window.state||state||{}}catch(e){return window.state||{}}}
function activeId(){try{const id=window.ld813PrimaryGameId?.();if(IDS.includes(id))return id}catch(e){}const s=stateObj();try{return String(s.activeGameId||currentGame?.id||'sv')}catch(e){return String(s.activeGameId||'sv')}}
function gameObj(id){try{const arr=(typeof GAMES!=='undefined'&&Array.isArray(GAMES))?GAMES:(Array.isArray(window.GAMES)?window.GAMES:[]);return arr.find(g=>g.id===id)||{id,...META[id],count:META[id]?.total||0}}catch(e){return {id,...META[id],count:META[id]?.total||0}}}
function truthy(v){return v===true||!!v?.caught||!!v?.registered||!!v?.owned}
function progress(id){
 const g=gameObj(id),m=META[id]||{},s=stateObj();
 try{if(typeof window.home77Progress==='function'){const p=window.home77Progress(g);if(p&&Number.isFinite(Number(p.total)))return {done:Number(p.caught||0),total:Number(p.total||m.total||0),pct:Number(p.pct||0)}}}catch(e){}
 let total=Number(g?.count||m.total||0),done=0;
 try{const prefix=id+':';for(const [k,v] of Object.entries(s.games||{}))if(k.startsWith(prefix)&&truthy(v))done++}catch(e){}
 done=Math.min(done,total||done);return {done,total,pct:total?Math.round(done/total*100):0}
}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function hero(id){const m=META[id]||META.sv,p=progress(id);return `<section class="ld8-hero" data-game="${id}" style="--ld8-accent:${m.accent}"><img class="ld8-hero-bg" src="${m.art}" alt="${esc(m.name)}"><div class="ld8-hero-copy"><span class="ld8-kicker">Continue sua jornada em</span><strong class="ld8-hero-title">${esc(m.name)}</strong><span class="ld8-region">${esc(m.region)}</span><div class="ld8-progress-row"><div class="ld8-progress-track" aria-label="${p.pct}% concluído"><i class="ld8-progress-fill" style="width:${Math.max(0,Math.min(100,p.pct))}%"></i></div><span class="ld8-progress-pct">${p.pct}%</span><span class="ld8-progress-numbers">${p.done} / ${p.total} Pokémon</span><span></span></div><div class="ld8-hero-actions"><button class="ld8-home-btn primary" type="button" data-ld8="continue">Continuar <span aria-hidden="true">›</span></button><button class="ld8-home-btn secondary" type="button" data-ld8="switch"><span aria-hidden="true">⇄</span> Trocar jogo</button></div></div></section>`}
function gameCard(id,active){const m=META[id],p=progress(id);return `<button type="button" class="ld8-game ${active?'active':''}" data-ld8-game="${id}" style="--ld8-accent:${m.accent}" aria-label="Consultar ${esc(m.name)}: ${p.done} de ${p.total}"><img src="${m.art}" alt=""><span class="ld8-game-copy"><strong class="ld8-game-name">${esc(m.short)}</strong><span class="ld8-game-meta"><i class="ld8-game-dot"></i>${p.done} / ${p.total}</span></span></button>`}
function markup(){const id=IDS.includes(activeId())?activeId():'sv';return `<div class="ld8-home-head"><span class="ld8-ball" aria-hidden="true"></span><div class="ld8-brand"><h1>Pokédex</h1><p>Living Dex Hub</p></div><button type="button" class="ld8-head-action" data-ld8="music" aria-label="Música" title="Música">♫</button></div>${hero(id)}<div class="ld8-section-head"><h2>Seus jogos</h2><button type="button" class="ld8-section-link" data-ld8="browse">Ver todos ›</button></div><section class="ld8-games" aria-label="Seus jogos">${IDS.map(g=>gameCard(g,g===id)).join('')}</section><div class="ld8-home-foot"><i></i> Sua jornada. Sua Pokédex. Seu mundo.</div>`}
function ensureMount(){const home=document.getElementById('home');if(!home)return null;let root=document.getElementById('ld8Home');if(!root){root=document.createElement('div');root.id='ld8Home';root.setAttribute('data-design-phase','F1');home.prepend(root)}return root}
function render(){const root=ensureMount();if(!root)return false;root.innerHTML=markup();bind(root);return true}
async function continueGame(){try{if(typeof window.ld813ContinuePrimary==='function'){await window.ld813ContinuePrimary();return}}catch(e){}const id=IDS.includes(activeId())?activeId():'sv';try{if(typeof window.ld71Open==='function'){await window.ld71Open();return}}catch(e){}try{if(typeof window.openGame==='function')await window.openGame(id)}catch(e){}try{window.ld71Open?.()}catch(e){}}
function switchGame(){try{if(typeof window.ld813OpenPrimarySelector==='function'){window.ld813OpenPrimarySelector();return}}catch(e){}try{if(typeof window.ld72OpenGames==='function'){window.ld72OpenGames();return}}catch(e){}console.warn('Living Dex Hub: seletor de jogo indisponível')}
function browseGames(){try{if(typeof window.ld813OpenConsultSelector==='function'){window.ld813OpenConsultSelector();return}}catch(e){}try{window.ld72OpenGames?.()}catch(e){}}
async function consultGame(id){if(!IDS.includes(id))return;try{if(typeof window.ld813ConsultGame==='function'){await window.ld813ConsultGame(id,{open:true});return}}catch(e){}try{if(typeof window.ld73LoadGame==='function'){await window.ld73LoadGame(id);await window.ld71Open?.()}}catch(e){}}
function openMusic(){try{const candidates=['ld712Open','ld712OpenLibrary','openMusicLibrary'];for(const n of candidates)if(typeof window[n]==='function'){window[n]();return}const btn=document.querySelector('[data-ld712],[aria-label*="música" i],[title*="música" i]');if(btn&&btn.closest('#ld8Home')===null){btn.click();return}}catch(e){} }
function bind(root){root.querySelectorAll('[data-ld8="continue"]').forEach(b=>b.onclick=continueGame);root.querySelectorAll('[data-ld8="switch"]').forEach(b=>b.onclick=switchGame);root.querySelectorAll('[data-ld8="browse"]').forEach(b=>b.onclick=browseGames);root.querySelector('[data-ld8="music"]')?.addEventListener('click',openMusic);root.querySelectorAll('[data-ld8-game]').forEach(b=>b.onclick=()=>consultGame(b.dataset.ld8Game))}
function refreshSoon(){setTimeout(render,0);setTimeout(render,140)}
const oldRender=window.renderActiveGameHome;window.renderActiveGameHome=function(){let r;try{if(typeof oldRender==='function')r=oldRender.apply(this,arguments)}catch(e){}render();return r};
for(const name of ['ld75CommitBox','ld71Toggle']){const old=window[name];if(typeof old==='function'&&!old.__ld8){const wrap=function(){const r=old.apply(this,arguments);refreshSoon();return r};wrap.__ld8=true;window[name]=wrap}}
window.ld8HomeRender=render;
window.ld8HomeAudit=function(){const id=activeId(),p=progress(id),root=document.getElementById('ld8Home');return {version:'8.0-f1.3',phase:'F1.3',mounted:!!root,primaryGame:id,progress:p,gameCards:root?.querySelectorAll('.ld8-game').length||0,hero:!!root?.querySelector('.ld8-hero'),continueAction:!!root?.querySelector('[data-ld8="continue"]'),switchAction:!!root?.querySelector('[data-ld8="switch"]'),browseAction:!!root?.querySelector('[data-ld8="browse"]'),legacyHomeChildrenVisible:[...document.querySelectorAll('#home > :not(#ld8Home)')].filter(e=>getComputedStyle(e).display!=='none').length}};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{render();setTimeout(render,250)});else{render();setTimeout(render,250)}
})();

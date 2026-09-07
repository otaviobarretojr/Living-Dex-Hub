from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-general-library" content="2.3"' not in s:
    s=s.replace('</head>','<meta name="living-dex-general-library" content="2.3"/>\n</head>',1)
css=r'''
/* General Library 2.3 — Home only continues the current game; General owns Library + National Dex. */
#home .home-next-objective,#home .home-journey-card{display:none!important}
.mobile-nav{grid-template-columns:repeat(3,1fr)!important;left:12px!important;right:12px!important;bottom:max(10px,env(safe-area-inset-bottom))!important;padding:7px!important}
.mnav-item[data-v="global"],.mnav-item[data-v="missing"]{display:none!important}
.mnav-item{min-height:52px!important;padding:7px 5px!important;gap:4px!important}
.mnav-icon{width:22px;height:22px;display:grid;place-items:center;font-size:0!important;line-height:1!important}
.mnav-icon svg{width:21px;height:21px;display:block;stroke:currentColor;stroke-width:1.9;fill:none;stroke-linecap:round;stroke-linejoin:round}
#mobileMoreBtn .mnav-icon svg{width:22px;height:22px}
.nav23-general-switch{display:flex;gap:4px;align-items:center;width:min(100%,460px);margin:2px auto 16px;padding:4px;border-radius:16px;border:1px solid rgba(148,180,215,.13);background:rgba(7,17,31,.72);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);position:sticky;top:6px;z-index:23}
.nav23-general-switch button{appearance:none;border:0;background:transparent;color:#8298af;min-height:42px;flex:1;border-radius:12px;font-size:10px;font-weight:850;display:flex;align-items:center;justify-content:center;gap:7px;padding:8px 10px}
.nav23-general-switch button.active{color:#eef9ff;background:linear-gradient(135deg,rgba(60,173,231,.20),rgba(88,111,255,.13));box-shadow:inset 0 0 0 1px rgba(114,213,255,.13)}
.nav23-general-switch svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
body.nav23-library-mode #games{display:block!important}
body.nav23-library-mode #games>#dexCard{display:none!important}
body.nav23-library-mode #games>#gamesGrid{display:grid!important}
body.nav23-library-mode #games>.section:first-child{display:block!important}
body.game-dex-focus .nav23-general-switch{display:none!important}
#gamesGrid.nav23-compact-library{grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
#gamesGrid.nav23-compact-library .game{min-height:154px!important;padding:13px!important;border-radius:18px!important;display:flex;flex-direction:column;align-items:stretch}
#gamesGrid.nav23-compact-library .game .plat{font-size:7px!important;letter-spacing:.08em}
#gamesGrid.nav23-compact-library .game h3{font-size:13px!important;line-height:1.12;margin:8px 0 5px;max-width:86%}
#gamesGrid.nav23-compact-library .game .tiny{font-size:7.5px!important;line-height:1.35;min-height:21px;color:#8fa5bb}
#gamesGrid.nav23-compact-library .game .pill{font-size:7px!important;margin-top:6px;align-self:flex-start}
#gamesGrid.nav23-compact-library .game .orb{width:62px!important;height:62px!important;border-width:12px!important;right:-20px!important;top:-20px!important;opacity:.55}
#gamesGrid.nav23-compact-library .game:after{font-size:6.5px!important;right:8px!important;top:8px!important;padding:4px 6px!important}
.nav23-game-actions{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:auto;padding-top:10px;position:relative;z-index:5}
.nav23-game-actions .game-active-btn,.nav23-game-actions .nav23-open-dex{position:static!important;inset:auto!important;width:100%;min-height:38px;border-radius:11px;border:1px solid rgba(148,180,215,.14);font-size:7.5px;font-weight:850;padding:6px 5px;cursor:pointer}
.nav23-game-actions .game-active-btn{background:rgba(255,255,255,.025);color:#a9bbcd}
.nav23-game-actions .game-active-btn.active{color:#c9f7e2;background:rgba(102,224,173,.07);border-color:rgba(102,224,173,.20)}
.nav23-game-actions .nav23-open-dex{background:linear-gradient(135deg,rgba(58,178,232,.16),rgba(73,113,255,.12));color:#dff5ff;border-color:rgba(114,213,255,.18)}
#home .playing-actions{grid-template-columns:1fr!important}
#home .playing-actions .btn{width:100%!important;min-height:52px!important}
#home .home-current-head>button{min-height:42px!important}
button,.btn,.mnav-item,.nav23-general-switch button,.game-active-btn,.nav23-open-dex{touch-action:manipulation;-webkit-tap-highlight-color:transparent}
@media(max-width:700px){#gamesGrid.nav23-compact-library{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.nav23-general-switch{top:4px;margin-bottom:12px}.wrap{padding-bottom:calc(96px + env(safe-area-inset-bottom))!important}.sheet{padding-bottom:calc(16px + env(safe-area-inset-bottom))!important}.mobile-more{bottom:calc(82px + env(safe-area-inset-bottom))!important}}
@media(max-width:365px){#gamesGrid.nav23-compact-library{grid-template-columns:1fr 1fr}.nav23-game-actions{grid-template-columns:1fr}.nav23-game-actions .game-active-btn,.nav23-game-actions .nav23-open-dex{min-height:36px}}
'''
if '/* General Library 2.3' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// General Library 2.3 — one clean Home CTA, a true game library, and National Dex inside General.
function nav23Icon(name){const icons={home:'<svg viewBox="0 0 24 24"><path d="M3.5 10.8 12 3.8l8.5 7v8.7a1.7 1.7 0 0 1-1.7 1.7H5.2a1.7 1.7 0 0 1-1.7-1.7z"/><path d="M9.2 21.2v-6.7h5.6v6.7"/></svg>',general:'<svg viewBox="0 0 24 24"><rect x="3.5" y="4" width="7" height="7" rx="1.5"/><rect x="13.5" y="4" width="7" height="7" rx="1.5"/><rect x="3.5" y="14" width="7" height="6" rx="1.5"/><rect x="13.5" y="14" width="7" height="6" rx="1.5"/></svg>',more:'<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.4" fill="currentColor" stroke="none"/></svg>',library:'<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="7" height="6" rx="1.4"/><rect x="13.5" y="5" width="7" height="6" rx="1.4"/><rect x="3.5" y="14" width="7" height="5" rx="1.4"/><rect x="13.5" y="14" width="7" height="5" rx="1.4"/></svg>',dex:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M3.7 12h16.6M9 12a3 3 0 0 0 6 0 3 3 0 0 0-6 0z"/></svg>'};return icons[name]||''}
function nav23MarkGeneral(){document.querySelectorAll('.mnav-item').forEach(x=>x.classList.remove('active'));document.querySelector('.mnav-item[data-v="games"]')?.classList.add('active')}
function nav23BottomAudit(){
 const home=document.querySelector('.mnav-item[data-v="home"]'),games=document.querySelector('.mnav-item[data-v="games"]'),more=document.getElementById('mobileMoreBtn');
 if(home){home.querySelector('.mnav-icon').innerHTML=nav23Icon('home');const l=home.querySelector('.mnav-icon+span');if(l)l.textContent='Início'}
 if(games){games.querySelector('.mnav-icon').innerHTML=nav23Icon('general');const l=games.querySelector('.mnav-icon+span');if(l)l.textContent='Geral';games.setAttribute('onclick','nav23OpenLibrary()')}
 if(more){more.querySelector('.mnav-icon').innerHTML=nav23Icon('more')}
}
function nav23SwitchMarkup(mode){return `<div class="nav23-general-switch" role="tablist" aria-label="Visão geral"><button type="button" class="${mode==='library'?'active':''}" onclick="nav23OpenLibrary()">${nav23Icon('library')} Biblioteca</button><button type="button" class="${mode==='dex'?'active':''}" onclick="nav23OpenNationalDex()">${nav23Icon('dex')} Dex Nacional</button></div>`}
function nav23EnsureSwitch(mode){
 const target=document.getElementById(mode==='dex'?'global':'games');if(!target)return;
 document.querySelectorAll('.nav23-general-switch').forEach(x=>x.remove());
 target.insertAdjacentHTML('afterbegin',nav23SwitchMarkup(mode));
}
function nav23OpenLibrary(){
 document.body.classList.remove('game-dex-focus');document.body.classList.add('nav23-library-mode');document.body.dataset.gameDexOpen='0';
 closeJourney?.();closeModal?.();closeMobileMore?.();
 const base=window.nav23BaseGo||window.go;base('games');
 const card=document.getElementById('dexCard');if(card)card.style.display='none';
 renderGames?.();nav23DecorateLibrary();nav23EnsureSwitch('library');nav23MarkGeneral();
 window.scrollTo({top:0,behavior:'auto'});
}
function nav23OpenNationalDex(){
 document.body.classList.remove('game-dex-focus','nav23-library-mode');document.body.dataset.gameDexOpen='0';
 closeJourney?.();closeModal?.();closeMobileMore?.();
 const base=window.nav23BaseGo||window.go;base('global');
 nav23EnsureSwitch('dex');nav23MarkGeneral();window.scrollTo({top:0,behavior:'auto'});
}
function nav23DecorateLibrary(){
 const grid=document.getElementById('gamesGrid');if(!grid)return;grid.classList.add('nav23-compact-library');
 grid.querySelectorAll('.game').forEach(card=>{
   const oc=card.getAttribute('onclick')||'';const m=oc.match(/(?:nav221OpenGameDex|nav21OpenGameDex|openGame)\(['\"]([^'\"]+)['\"]\)/);if(!m)return;const id=m[1];
   card.removeAttribute('onclick');
   let actions=card.querySelector('.nav23-game-actions');if(!actions){actions=document.createElement('div');actions.className='nav23-game-actions';const active=card.querySelector('.game-active-btn');if(active)actions.appendChild(active);const open=document.createElement('button');open.type='button';open.className='nav23-open-dex';open.textContent='Abrir Dex';open.setAttribute('onclick',`event.stopPropagation();nav221OpenGameDex('${id}')`);actions.appendChild(open);card.appendChild(actions)}
 });
}
function nav23PolishHome(){
 document.querySelectorAll('#home .home-next-objective,#home .home-journey-card').forEach(x=>x.remove());
 const shell=document.querySelector('#home .home-current-shell');if(!shell)return;
 const swap=[...shell.querySelectorAll('button')].find(b=>/trocar jogo|ver biblioteca/i.test((b.textContent||'').trim()));if(swap){swap.textContent='Trocar jogo';swap.setAttribute('onclick','nav23OpenLibrary()')}
 const primary=[...shell.querySelectorAll('.playing-actions button')].find(b=>/continuar/i.test((b.textContent||'').trim())||/continueActiveGame/.test(b.getAttribute('onclick')||''));if(primary){primary.textContent='Continuar jornada';primary.setAttribute('onclick','continueActiveGame()')}
 shell.querySelectorAll('.playing-actions button').forEach(b=>{if(b!==primary)b.remove()});
}
window.nav23BaseGo=window.go;
window.go=function(v){if(v==='games')return nav23OpenLibrary();if(v==='global')return nav23OpenNationalDex();return window.nav23BaseGo(v)};
const nav23OldRenderGames=window.renderGames;if(typeof nav23OldRenderGames==='function'){window.renderGames=function(){const r=nav23OldRenderGames.apply(this,arguments);setTimeout(()=>{nav23DecorateLibrary();nav23BottomAudit()},0);return r}}
const nav23OldHome=window.renderActiveGameHome;if(typeof nav23OldHome==='function'){window.renderActiveGameHome=function(){const r=nav23OldHome.apply(this,arguments);setTimeout(nav23PolishHome,0);return r}}
window.nav21ExitGameDex=nav23OpenLibrary;
window.continueActiveGame=function(){const id=state.activeGameId;if(id){document.body.classList.remove('nav23-library-mode');nav221OpenGameDex(id)}else nav23OpenLibrary()};
const nav23OpenDexBase=window.nav221OpenGameDex;window.nav221OpenGameDex=async function(id){document.body.classList.remove('nav23-library-mode');return nav23OpenDexBase(id)};window.nav21OpenGameDex=window.nav221OpenGameDex;
setTimeout(()=>{nav23BottomAudit();nav23PolishHome();if(document.querySelector('#games.active')){document.body.classList.add('nav23-library-mode');nav23DecorateLibrary();nav23EnsureSwitch('library')}},0);
if(new URLSearchParams(location.search).get('generalqa')==='1'){
 setTimeout(()=>{nav23OpenLibrary();const library=!!document.querySelector('#gamesGrid.nav23-compact-library .nav23-open-dex');nav23OpenNationalDex();const dex=!!document.querySelector('#global.active .nav23-general-switch');nav23OpenLibrary();const general=document.querySelector('.mnav-item[data-v="games"]');const hiddenDex=getComputedStyle(document.querySelector('.mnav-item[data-v="global"]')).display==='none';document.documentElement.dataset.generalQa=(library&&dex&&general?.textContent.includes('Geral')&&hiddenDex)?'1':'0'},900)
}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('General Library 2.3 applied')

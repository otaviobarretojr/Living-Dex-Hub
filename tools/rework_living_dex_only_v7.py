from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-only" content="7.0"' not in s:
    s=s.replace('</head>','<meta name="living-dex-only" content="7.0"/>\n</head>',1)
css=r'''
/* Living Dex Only 7.0 — one purpose: choose a game and complete its Living Dex. */
#global,#families,#planner,#forms,#storage,#settings,.jh52,.ref42-page,#ref41Hub,.home51-journey,.home232-journey,.home-journey-summary,.home-journey-card,.journey,.journey-section,[data-view="missing"]{display:none!important}
#home .home-current-shell{padding-bottom:110px!important}
#home .playing-card{cursor:pointer!important}
.home51-cta{display:flex!important;align-items:center;justify-content:center;gap:10px}
.home51-cta:before{content:'◉';font-size:15px}
/* Strip non-Living-Dex utility surfaces from game view. */
body.livingdex-only #games .journey,body.livingdex-only #games .journey-card,body.livingdex-only #games .map-card,body.livingdex-only #games .team-card{display:none!important}
/* Dedicated two-destination navigation. */
.mnav{grid-template-columns:repeat(3,1fr)!important}
.mnav .ld7-hidden{display:none!important}
.ld7-navbtn{border:0!important;background:transparent!important;color:#9aa4b4!important;min-height:64px!important;border-radius:18px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:5px!important;font-size:11px!important;font-weight:850!important}.ld7-navbtn svg{width:22px;height:22px}.ld7-navbtn.active{background:#fff0f0!important;color:#ff5757!important}
/* Living Dex card and grid remain the visual focus. */
body.game-dex-focus #games{padding-bottom:100px!important}.game-focus-bar{max-width:820px!important;background:rgba(255,255,255,.96)!important;color:#16213b!important;border:1px solid #e8edf4!important;box-shadow:0 8px 26px rgba(33,48,78,.07)!important}.game-focus-bar .game-focus-copy small{color:#8b96a9!important}.game-focus-bar .btn{background:#fff!important;color:#16213b!important;border:1px solid #e8edf4!important}
@media(max-width:520px){#home .home-current-shell{padding-bottom:100px!important}.home51-title{margin-bottom:18px!important}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Living Dex Only 7.0
function ld7Current(){return GAMES.find(g=>g.id===state.activeGameId)||null}
function ld7OpenCurrent(){const g=ld7Current();if(g){nav221OpenGameDex(g.id)}else{go('games');setTimeout(ld7Audit,0)}}
function ld7Home(){go('home');setTimeout(()=>{try{renderActiveGameHome()}catch(e){}ld7Audit()},0)}
function ld7Library(){document.body.classList.remove('game-dex-focus');go('games');setTimeout(ld7Audit,0)}
function ld7Nav(){const nav=document.querySelector('.mnav');if(!nav)return;nav.innerHTML=`<button class="ld7-navbtn" data-ld7="home" onclick="ld7Home()" aria-label="Início"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg><span>Início</span></button><button class="ld7-navbtn" data-ld7="games" onclick="ld7Library()" aria-label="Biblioteca"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/></svg><span>Biblioteca</span></button><button class="ld7-navbtn" data-ld7="dex" onclick="ld7OpenCurrent()" aria-label="Living Dex"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><circle cx="12" cy="12" r="3"/></svg><span>Living Dex</span></button>`;ld7NavState()}
function ld7NavState(){const page=document.querySelector('.view.active')?.id;document.querySelectorAll('.ld7-navbtn').forEach(b=>b.classList.remove('active'));let key=document.body.classList.contains('game-dex-focus')?'dex':page==='games'?'games':'home';document.querySelector(`.ld7-navbtn[data-ld7="${key}"]`)?.classList.add('active')}
function ld7HomePrune(){const h=document.getElementById('home');if(!h)return;h.querySelectorAll('.home51-journey,.home232-journey,.home-journey-summary,.home-journey-card,.journey,.journey-section').forEach(x=>x.remove());const c=h.querySelector('.home51-cta');if(c){c.textContent='Abrir Living Dex';c.onclick=ld7OpenCurrent}const card=h.querySelector('.playing-card');if(card){card.onclick=e=>{if(e.target.closest('button'))return;ld7OpenCurrent()}}}
function ld7RemoveNonDex(){['global','families','planner','forms','storage','settings'].forEach(id=>document.getElementById(id)?.remove());document.querySelectorAll('.jh52,.ref42-page,#ref41Hub,.journey,.journey-section,.map-card,.team-card').forEach(x=>x.remove());document.querySelectorAll('button,a,.menu-item,.more-item').forEach(el=>{const t=(el.textContent||'').trim();if(/jornada|time recomendado|mapa|planejador|formas|armazenamento|configurações/i.test(t)&&!el.closest('#dexCard'))el.remove()})}
function ld7RewireLibrary(){document.querySelectorAll('.game,.library46-card,.ref45-game-card').forEach(card=>{const oc=card.getAttribute('onclick')||'';const m=oc.match(/(?:nav221OpenGameDex|nav21OpenGameDex|openGame)\(['\"]([^'\"]+)['\"]\)/);if(m)card.setAttribute('onclick',`nav221OpenGameDex('${m[1]}')`)})}
function ld7Audit(){document.body.classList.add('livingdex-only');ld7RemoveNonDex();ld7HomePrune();ld7RewireLibrary();ld7Nav();ld7NavState();document.documentElement.dataset.livingDexOnly='7.0'}
// Journey entry points are deliberately retired in this product direction.
window.ref42Open=function(){ld7OpenCurrent()};window.jh52Open=function(){ld7OpenCurrent()};window.continueActiveGame=ld7OpenCurrent;
const ld7Go=window.go;if(typeof ld7Go==='function')window.go=function(dest){const allowed=['home','games'];const r=ld7Go.call(this,allowed.includes(dest)?dest:'home');setTimeout(ld7Audit,0);return r};
const ld7Render=window.renderActiveGameHome;if(typeof ld7Render==='function')window.renderActiveGameHome=function(){const r=ld7Render.apply(this,arguments);setTimeout(ld7Audit,0);return r};
const ld7Games=window.renderGames;if(typeof ld7Games==='function')window.renderGames=function(){const r=ld7Games.apply(this,arguments);setTimeout(ld7Audit,0);return r};
setTimeout(ld7Audit,100);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Living Dex Only 7.0 applied')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-navigation" content="2.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-navigation" content="2.1"/>\n</head>',1)
css=r'''
/* Navigation Audit 2.1 */
/* Faltando fica funcional no código, mas deixa de existir como destino visual separado. */
[data-view="missing"],button[onclick*="go('missing')"],button[onclick*='go("missing")']{display:none!important}
.mobile-nav{grid-template-columns:repeat(4,1fr)!important}
.home-journey-card{margin-top:12px;padding:15px 16px;border-radius:20px;border:1px solid rgba(102,224,173,.16);background:linear-gradient(145deg,rgba(102,224,173,.07),rgba(79,181,255,.04));display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center}
.home-journey-card .eyebrow{font-size:8px;letter-spacing:.14em;text-transform:uppercase;color:#66e0ad;font-weight:900}.home-journey-card h3{margin:5px 0 4px;font-size:16px}.home-journey-card p{margin:0;color:#90a6bc;font-size:9px;line-height:1.5}.home-journey-card .btn{min-height:42px}
/* Biblioteca não precisa aparecer como atalho dentro do card do jogo atual. */
.playing-actions .library-shortcut,.home-current-head .library-shortcut{display:none!important}
/* Quando estamos dentro de uma Dex de jogo, a interface deve parecer uma tela exclusiva daquele título. */
body.game-dex-focus .view:not(#global):not(.active){display:none!important}
body.game-dex-focus #games{display:none!important}
body.game-dex-focus .game-focus-bar{display:flex}
.game-focus-bar{display:none;align-items:center;justify-content:space-between;gap:10px;margin:0 auto 12px;max-width:980px;padding:10px 12px;border-radius:16px;border:1px solid rgba(148,180,215,.13);background:rgba(8,20,35,.72);backdrop-filter:blur(14px)}
.game-focus-bar .game-focus-copy small{display:block;color:#7f96ac;font-size:7px;text-transform:uppercase;letter-spacing:.12em}.game-focus-bar .game-focus-copy b{display:block;margin-top:3px;font-size:11px}.game-focus-bar .btn{min-height:36px;font-size:8px}
@media(max-width:520px){.home-journey-card{grid-template-columns:1fr}.home-journey-card .btn{width:100%}}
'''
if '/* Navigation Audit 2.1 */' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Navigation Audit 2.1 — remove redundant destinations and open game Dex directly.
function nav21FindModalAction(){
 const modal=document.getElementById('modal');if(!modal||!modal.classList.contains('show'))return null;
 const nodes=[...modal.querySelectorAll('button,a,[role="button"]')];
 return nodes.find(x=>/pok[eé]dex|\bdex\b|abrir pok[eé]dex|ver pok[eé]dex/i.test((x.textContent||'').trim()));
}
function nav21EnsureFocusBar(game){
 let bar=document.getElementById('gameFocusBar');
 if(!bar){bar=document.createElement('div');bar.id='gameFocusBar';bar.className='game-focus-bar';document.body.prepend(bar)}
 const version=typeof selectedVersion==='function'?(selectedVersion(game.id)||''):'';
 bar.innerHTML=`<div class="game-focus-copy"><small>Dex do jogo atual</small><b>${version||game.name} · somente este jogo</b></div><button class="btn" onclick="nav21ExitGameDex()">Voltar aos jogos</button>`;
}
function nav21ExitGameDex(){document.body.classList.remove('game-dex-focus');go('games')}
function nav21OpenGameDex(id){
 const game=GAMES.find(g=>g.id===id);if(!game)return;
 openGame(id);
 let tries=0;
 const finish=()=>{
   const action=nav21FindModalAction();
   if(action){action.click();setTimeout(()=>{document.body.classList.add('game-dex-focus');nav21EnsureFocusBar(game)},30);return}
   if(++tries<8)setTimeout(finish,55);else{document.body.classList.add('game-dex-focus');nav21EnsureFocusBar(game)}
 };
 setTimeout(finish,20);
}
function continueActiveGame(){const id=state.activeGameId;if(id)nav21OpenGameDex(id);else go('games')}
function nav21OpenJourney(){const id=state.activeGameId;if(!id){go('games');premiumToast?.('Escolha um jogo atual primeiro');return}if(typeof openJourney==='function'&&journeySupported?.(id)){openJourney(id,'route');return}premiumToast?.('Jornada detalhada deste jogo ainda não está disponível')}
function nav21DecorateHome(){
 const shell=document.querySelector('#home .home-current-shell');if(!shell)return;
 shell.querySelectorAll('button').forEach(b=>{const t=(b.textContent||'').trim();if(/ver biblioteca/i.test(t)){b.classList.add('library-shortcut');b.style.display='none'}});
 const pc=shell.querySelector('.playing-card');if(!pc||pc.querySelector('.home-journey-card'))return;
 const g=GAMES.find(x=>x.id===state.activeGameId);if(!g)return;
 const supported=typeof journeySupported==='function'&&journeySupported(g.id);
 pc.insertAdjacentHTML('beforeend',`<div class="home-journey-card"><div><div class="eyebrow">Jornada</div><h3>${supported?'Continuar sua jornada':'Companheiro de jornada'}</h3><p>${supported?'Rota, próximo objetivo, time recomendado e mapa do jogo atual.':'Este jogo ainda não possui Jornada detalhada.'}</p></div><button class="btn ${supported?'primary':''}" onclick="nav21OpenJourney()" ${supported?'':'disabled'}>Abrir Jornada</button></div>`)
}
function nav21HideMissingEverywhere(){
 document.querySelectorAll('button,a,.tab,.mnav-item').forEach(el=>{if(/^faltando$/i.test((el.textContent||'').trim()))el.style.display='none'});
}
function nav21RewireGameCards(){
 document.querySelectorAll('.game').forEach(card=>{
   const m=(card.getAttribute('onclick')||'').match(/openGame\(['\"]([^'\"]+)['\"]\)/);
   if(m)card.setAttribute('onclick',`nav21OpenGameDex('${m[1]}')`)
 });
}
function nav21AuditPass(){nav21HideMissingEverywhere();nav21DecorateHome();nav21RewireGameCards()}
const nav21RenderGames=window.renderGames;if(typeof nav21RenderGames==='function'){window.renderGames=function(){const r=nav21RenderGames.apply(this,arguments);setTimeout(nav21AuditPass,0);return r}}
const nav21RenderHome=window.renderActiveGameHome;if(typeof nav21RenderHome==='function'){window.renderActiveGameHome=function(){const r=nav21RenderHome.apply(this,arguments);setTimeout(nav21AuditPass,0);return r}}
setTimeout(nav21AuditPass,0);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Navigation Audit 2.1 applied')
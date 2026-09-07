from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-game-dex-fix" content="2.2.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-game-dex-fix" content="2.2.1"/>\n</head>',1)
css=r'''
/* Game Dex Fix 2.2.1 — the game Dex lives inside #games; hide only the library around it. */
body.game-dex-focus #games{display:block!important}
body.game-dex-focus #games>.section:first-child{display:none!important}
body.game-dex-focus #games>#gamesGrid{display:none!important}
body.game-dex-focus #games>#dexCard{display:block!important;margin-top:0!important}
body.game-dex-focus #games.active{display:block!important}
body.game-dex-focus .game-focus-bar{display:flex!important}
'''
if '/* Game Dex Fix 2.2.1' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Game Dex Fix 2.2.1 — use the real embedded #dexCard instead of looking for a nonexistent modal button.
function nav221DexReady(id){
 const card=document.getElementById('dexCard');
 const grid=document.getElementById('dexGrid');
 return !!(currentGame&&currentGame.id===id&&card&&card.style.display!=='none'&&grid&&currentDex&&currentDex.length);
}
function nav221FocusRealDex(game){
 document.body.classList.add('game-dex-focus');
 nav21EnsureFocusBar?.(game);
 document.body.dataset.gameDexOpen='1';
 document.body.dataset.gameDexView='games:dexCard';
 const card=document.getElementById('dexCard');
 if(card)card.scrollIntoView({behavior:'auto',block:'start'});
}
async function nav221OpenGameDex(id){
 const game=GAMES.find(g=>g.id===id);if(!game)return;
 document.body.classList.remove('game-dex-focus');
 document.body.dataset.gameDexOpen='0';
 closeJourney?.();closeMobileMore?.();closeModal?.();
 try{
   await openGame(id);
   let tries=0;
   const wait=()=>{
     if(nav221DexReady(id)){nav221FocusRealDex(game);return}
     if(++tries<18){setTimeout(wait,70);return}
     document.body.classList.remove('game-dex-focus');
     document.body.dataset.gameDexOpen='0';
     premiumToast?.('Não foi possível carregar a Dex deste jogo');
   };
   wait();
 }catch(e){
   document.body.classList.remove('game-dex-focus');
   document.body.dataset.gameDexOpen='0';
   premiumToast?.('Não foi possível carregar a Dex deste jogo');
 }
}
window.nav21OpenGameDex=nav221OpenGameDex;
window.continueActiveGame=function(){const id=state.activeGameId;if(id)nav221OpenGameDex(id);else go('games')};
function nav221RewireCards(){
 document.querySelectorAll('.game').forEach(card=>{
   const oc=card.getAttribute('onclick')||'';
   const m=oc.match(/(?:nav21OpenGameDex|nav221OpenGameDex|openGame)\(['\"]([^'\"]+)['\"]\)/);
   if(m)card.setAttribute('onclick',`nav221OpenGameDex('${m[1]}')`);
 });
}
const nav221RG=window.renderGames;if(typeof nav221RG==='function'){window.renderGames=function(){const r=nav221RG.apply(this,arguments);setTimeout(nav221RewireCards,0);return r}}
setTimeout(nav221RewireCards,0);
if(new URLSearchParams(location.search).get('navfixqa')==='1'){
 setTimeout(()=>nav221OpenGameDex('sv'),350);
 setTimeout(()=>{
   const card=document.getElementById('dexCard'),grid=document.getElementById('dexGrid');
   const ok=document.body.dataset.gameDexOpen==='1'&&document.body.classList.contains('game-dex-focus')&&currentGame?.id==='sv'&&card&&getComputedStyle(card).display!=='none'&&grid&&grid.querySelectorAll('.pk').length>0;
   document.documentElement.setAttribute('data-navfix-pass',ok?'1':'0');
   document.documentElement.dataset.navfixPokemon=String(grid?.querySelectorAll('.pk').length||0);
 },2500);
}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Game Dex Fix 2.2.1 applied — real #dexCard focus')

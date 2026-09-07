from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-game-dex-fix" content="2.2.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-game-dex-fix" content="2.2.1"/>\n</head>',1)
js=r'''
// Game Dex Fix 2.2.1 — never enter focused mode before the game's Dex is actually active.
function nav221ModalButtons(){
 const modal=document.getElementById('modal');if(!modal)return [];
 return [...modal.querySelectorAll('button,a,[role="button"]')].map(el=>(el.textContent||'').replace(/\s+/g,' ').trim()).filter(Boolean);
}
function nav221DexAction(){
 const modal=document.getElementById('modal');
 if(!modal||!modal.classList.contains('show'))return null;
 const nodes=[...modal.querySelectorAll('button,a,[role="button"]')];
 return nodes.find(el=>{
   const t=(el.textContent||'').replace(/\s+/g,' ').trim();
   if(!t||/jornada|time|mapa/i.test(t))return false;
   return /abrir\s+(?:a\s+)?(?:pok[eé]dex|dex)|ver\s+(?:a\s+)?(?:pok[eé]dex|dex)|(?:pok[eé]dex|dex)\s+do\s+jogo|continuar\s+registros?/i.test(t);
 });
}
function nav221ActiveDexView(){
 const active=[...document.querySelectorAll('.view.active')].find(v=>!['home','games','missing'].includes(v.id));
 if(active&&getComputedStyle(active).display!=='none')return active;
 return null;
}
function nav221FinishFocus(game,attempt=0){
 const v=nav221ActiveDexView();
 if(v){
   document.body.classList.add('game-dex-focus');
   nav21EnsureFocusBar?.(game);
   document.body.dataset.gameDexOpen='1';
   document.body.dataset.gameDexView=v.id||'active';
   return true;
 }
 if(attempt<12){setTimeout(()=>nav221FinishFocus(game,attempt+1),70);return false}
 document.body.classList.remove('game-dex-focus');
 document.body.dataset.gameDexOpen='0';
 premiumToast?.('Não foi possível abrir a Dex deste jogo');
 return false;
}
function nav221OpenGameDex(id){
 const game=GAMES.find(g=>g.id===id);if(!game)return;
 document.body.classList.remove('game-dex-focus');
 document.body.dataset.gameDexOpen='0';
 closeJourney?.();
 closeMobileMore?.();
 openGame(id);
 let tries=0;
 const press=()=>{
   document.documentElement.dataset.navfixButtons=nav221ModalButtons().join(' | ').slice(0,400);
   const action=nav221DexAction();
   if(action){
     document.documentElement.dataset.navfixAction=(action.textContent||'').replace(/\s+/g,' ').trim();
     action.click();
     setTimeout(()=>nav221FinishFocus(game,0),35);
     return;
   }
   if(++tries<18){setTimeout(press,60);return}
   document.body.classList.remove('game-dex-focus');
   document.body.dataset.gameDexOpen='0';
   premiumToast?.('Abra a Pokédex pelo painel do jogo');
 };
 setTimeout(press,30);
}
window.nav21OpenGameDex=nav221OpenGameDex;
window.continueActiveGame=function(){const id=state.activeGameId;if(id)nav221OpenGameDex(id);else go('games')};
function nav221RewireCards(){
 document.querySelectorAll('.game').forEach(card=>{
   const oc=card.getAttribute('onclick')||'';
   let m=oc.match(/(?:nav21OpenGameDex|nav221OpenGameDex|openGame)\(['\"]([^'\"]+)['\"]\)/);
   if(m)card.setAttribute('onclick',`nav221OpenGameDex('${m[1]}')`);
 });
}
const nav221RG=window.renderGames;if(typeof nav221RG==='function'){window.renderGames=function(){const r=nav221RG.apply(this,arguments);setTimeout(nav221RewireCards,0);return r}}
setTimeout(nav221RewireCards,0);
if(new URLSearchParams(location.search).get('navfixqa')==='1'){
 setTimeout(()=>nav221OpenGameDex('sv'),350);
 setTimeout(()=>{
   const ok=document.body.dataset.gameDexOpen==='1'&&!!nav221ActiveDexView();
   document.documentElement.setAttribute('data-navfix-pass',ok?'1':'0');
 },2300);
}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Game Dex Fix 2.2.1 applied')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-current-game-star" content="4.5.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-current-game-star" content="4.5.1"/>\n</head>',1)
css=r'''
/* Current Game Star 4.5.1 — transparent favorite star, yellow when selected. */
#gamesGrid .game .nav23-game-actions{grid-template-columns:1fr!important;position:static!important}
#gamesGrid .game .game-active-btn.r451-star{position:absolute!important;top:12px!important;left:12px!important;right:auto!important;bottom:auto!important;width:40px!important;height:40px!important;min-width:40px!important;min-height:40px!important;padding:0!important;margin:0!important;border:0!important;border-radius:0!important;background:transparent!important;color:#9aa5b7!important;box-shadow:none!important;display:grid!important;place-items:center!important;font-size:0!important;line-height:1!important;z-index:8!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;-webkit-tap-highlight-color:transparent!important}
#gamesGrid .game .game-active-btn.r451-star::before{content:'☆';font-size:31px!important;line-height:1!important;font-family:Arial,sans-serif;font-weight:400!important;filter:none!important;text-shadow:0 1px 2px rgba(17,27,54,.12)}
#gamesGrid .game .game-active-btn.r451-star.active,#gamesGrid .game .game-active-btn.r451-star.current{background:transparent!important;color:#f6bf16!important;box-shadow:none!important}
#gamesGrid .game .game-active-btn.r451-star.active::before,#gamesGrid .game .game-active-btn.r451-star.current::before{content:'★';font-size:28px!important;text-shadow:0 1px 3px rgba(156,112,0,.18)}
#gamesGrid .game .r45-current{display:none!important}
#gamesGrid .game .orb{display:none!important;width:0!important;height:0!important;min-width:0!important;min-height:0!important;padding:0!important;margin:0!important;border:0!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important}
#gamesGrid .game .nav23-open-dex,#gamesGrid .game .r45-open{width:100%!important;min-height:48px!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
function r451Stars(){
 document.querySelectorAll('#gamesGrid .game').forEach(card=>{
   const id=typeof r45GameId==='function'?r45GameId(card):'';
   const b=card.querySelector('.game-active-btn');if(!b)return;
   const current=!!id&&id===state.activeGameId;
   b.classList.add('r451-star');b.classList.toggle('current',current);b.classList.toggle('active',current);
   b.textContent='';b.setAttribute('aria-label',current?'Jogo selecionado':'Selecionar jogo');b.setAttribute('title',current?'Jogo selecionado':'Selecionar jogo');
 });
 document.querySelectorAll('#gamesGrid .game .orb,#gamesGrid .game .r45-current').forEach(el=>el.setAttribute('aria-hidden','true'));
 document.documentElement.dataset.r451Stars='1';
}
const r451RenderGames=window.renderGames;if(typeof r451RenderGames==='function')window.renderGames=function(){const r=r451RenderGames.apply(this,arguments);setTimeout(r451Stars,40);return r};
const r451SetActive=window.setActiveGame;if(typeof r451SetActive==='function')window.setActiveGame=function(){const r=r451SetActive.apply(this,arguments);setTimeout(()=>{if(typeof r45Library==='function')r45Library();r451Stars()},50);return r};
setTimeout(r451Stars,220);
if(new URLSearchParams(location.search).has('r451qa'))setTimeout(()=>{try{if(typeof r45EnsureLibrary==='function')r45EnsureLibrary();}catch(e){}setTimeout(()=>{r451Stars();const cards=[...document.querySelectorAll('#gamesGrid .game')];const stars=[...document.querySelectorAll('#gamesGrid .game .game-active-btn.r451-star')];const ok=cards.length>=6&&stars.length===cards.length&&stars.every(b=>b.getAttribute('aria-label')&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)')&&[...document.querySelectorAll('#gamesGrid .game .orb')].every(o=>getComputedStyle(o).display==='none');document.documentElement.dataset.r451Qa=ok?'1':'0'},650)},450);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Current Game Star 4.5.1 applied — transparent star, yellow selected, black orb removed')

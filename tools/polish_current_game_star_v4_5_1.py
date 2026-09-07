from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-current-game-star" content="4.5.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-current-game-star" content="4.5.1"/>\n</head>',1)
css=r'''
/* Current Game Star 4.5.1 — compact visual control, 48px accessible touch target. */
#gamesGrid .game .nav23-game-actions{grid-template-columns:1fr!important;position:static!important}
#gamesGrid .game .game-active-btn.r451-star{position:absolute!important;top:10px!important;left:10px!important;right:auto!important;bottom:auto!important;width:48px!important;height:48px!important;min-width:48px!important;min-height:48px!important;padding:0!important;margin:0!important;border:0!important;border-radius:50%!important;background:rgba(255,255,255,.94)!important;color:#a5afbf!important;box-shadow:0 4px 14px rgba(24,38,68,.13)!important;display:grid!important;place-items:center!important;font-size:0!important;line-height:1!important;z-index:8!important;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
#gamesGrid .game .game-active-btn.r451-star::before{content:'☆';font-size:25px!important;line-height:1!important;font-family:Arial,sans-serif;font-weight:400!important;transform:translateY(-1px)}
#gamesGrid .game .game-active-btn.r451-star.active,#gamesGrid .game .game-active-btn.r451-star.current{background:rgba(255,255,255,.97)!important;color:var(--rf45-red,#ff5158)!important}
#gamesGrid .game .game-active-btn.r451-star.active::before,#gamesGrid .game .game-active-btn.r451-star.current::before{content:'★';font-size:22px!important}
#gamesGrid .game .r45-current{right:10px!important;left:auto!important;pointer-events:none}
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
   b.textContent='';b.setAttribute('aria-label',current?'Jogo atual':'Definir como jogo atual');b.setAttribute('title',current?'Jogo atual':'Definir como jogo atual');
 });
 document.documentElement.dataset.r451Stars='1';
}
const r451RenderGames=window.renderGames;if(typeof r451RenderGames==='function')window.renderGames=function(){const r=r451RenderGames.apply(this,arguments);setTimeout(r451Stars,40);return r};
const r451SetActive=window.setActiveGame;if(typeof r451SetActive==='function')window.setActiveGame=function(){const r=r451SetActive.apply(this,arguments);setTimeout(()=>{if(typeof r45Library==='function')r45Library();r451Stars()},50);return r};
setTimeout(r451Stars,220);
if(new URLSearchParams(location.search).has('r451qa'))setTimeout(()=>{try{if(typeof r45EnsureLibrary==='function')r45EnsureLibrary();}catch(e){}setTimeout(()=>{r451Stars();const cards=[...document.querySelectorAll('#gamesGrid .game')];const stars=[...document.querySelectorAll('#gamesGrid .game .game-active-btn.r451-star')];const ok=cards.length>=6&&stars.length===cards.length&&stars.every(b=>b.getAttribute('aria-label')&&parseFloat(getComputedStyle(b).width)>=48&&parseFloat(getComputedStyle(b).height)>=48);document.documentElement.dataset.r451Qa=ok?'1':'0'},650)},450);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Current Game Star 4.5.1 applied')

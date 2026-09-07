from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-library-reference" content="4.6"' not in s:
    s=s.replace('</head>','<meta name="living-dex-library-reference" content="4.6"/>\n</head>',1)
css=r'''
/* Library Reference 4.6 — faithful to approved mobile reference. */
:root{--v46-red:#ff5259;--v46-ink:#111a35;--v46-muted:#8d97aa;--v46-line:#e9edf4;--v46-yellow:#f7c843}
#games{max-width:980px!important;margin:0 auto!important;padding:18px 18px calc(126px + env(safe-area-inset-bottom))!important;overflow:visible!important}
#games .nav23-general-switch{position:sticky!important;top:0!important;z-index:18!important;margin:0 0 24px!important;background:rgba(255,255,255,.97)!important;border:0!important;border-radius:0 0 26px 26px!important;box-shadow:0 10px 30px rgba(24,37,70,.06)!important;padding:8px!important}
#games .nav23-general-switch button{min-height:50px!important;font-size:15px!important;font-weight:850!important;color:#9aa4b5!important;border-radius:18px!important}
#games .nav23-general-switch button.active{background:#fff0f1!important;color:var(--v46-red)!important;box-shadow:none!important}
#games .section:first-of-type h2,#games h1{font-size:31px!important;line-height:1.08!important;letter-spacing:-.045em!important;color:var(--v46-ink)!important;margin:16px 0 8px!important}
#games .section:first-of-type p,#games>p{font-size:15px!important;line-height:1.4!important;color:var(--v46-muted)!important;margin-bottom:20px!important}
.v46-filters{display:flex;gap:10px;overflow-x:auto;padding:1px 0 16px;scrollbar-width:none}.v46-filters::-webkit-scrollbar{display:none}.v46-chip{appearance:none;white-space:nowrap;border:0;border-radius:999px;background:#f1f3f7;color:#7d879a;min-height:42px;padding:0 18px;font-size:13px;font-weight:850}.v46-chip.active{background:var(--v46-red);color:#fff}
#games #gamesGrid,#gamesGrid.nav23-compact-library{display:grid!important;grid-template-columns:1fr!important;gap:16px!important}
#gamesGrid .game{position:relative!important;display:grid!important;grid-template-columns:minmax(148px,34%) 1fr!important;grid-template-rows:auto!important;column-gap:0!important;align-items:stretch!important;width:100%!important;min-height:212px!important;padding:0!important;margin:0!important;border:1px solid rgba(229,234,243,.9)!important;border-radius:27px!important;background:#fff!important;overflow:hidden!important;box-shadow:0 12px 30px rgba(29,42,76,.075)!important}
#gamesGrid .game .r45-game-art{grid-column:1!important;grid-row:1 / span 10!important;height:100%!important;min-height:212px!important;margin:0!important;border-radius:0!important;background:#edf1f7!important;overflow:hidden!important}
#gamesGrid .game .r45-game-art img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important}
#gamesGrid .game .r45-game-platform,#gamesGrid .game h3,#gamesGrid .game .r45-dexname,#gamesGrid .game .v46-stats,#gamesGrid .game .v46-progress,#gamesGrid .game .nav23-game-actions{grid-column:2!important;margin-left:18px!important;margin-right:18px!important}
#gamesGrid .game .r45-game-platform{align-self:end!important;margin-top:15px!important;margin-bottom:6px!important;width:max-content!important;padding:5px 10px!important;border-radius:11px!important;background:var(--v46-red)!important;color:#fff!important;font-size:9px!important;line-height:1!important;letter-spacing:.06em!important;font-weight:900!important}
#gamesGrid .game h3{font-size:20px!important;line-height:1.08!important;letter-spacing:-.03em!important;color:var(--v46-ink)!important;margin-top:0!important;margin-bottom:4px!important;max-width:calc(100% - 36px)!important}
#gamesGrid .game .r45-dexname{font-size:12px!important;color:var(--v46-muted)!important;margin-top:0!important;margin-bottom:12px!important}
#gamesGrid .game .tiny,#gamesGrid .game .pill,#gamesGrid .game .r45-progressline,#gamesGrid .game .r45-current,#gamesGrid .game .orb{display:none!important}
.v46-stats{display:flex;gap:18px;align-items:flex-end;margin-bottom:8px!important}.v46-stat{min-width:86px;padding-right:18px;border-right:1px solid var(--v46-line)}.v46-stat:last-child{border-right:0}.v46-stat strong{display:block;font-size:20px;line-height:1;color:var(--v46-ink);font-weight:850}.v46-stat span{display:block;margin-top:4px;font-size:11px;color:var(--v46-muted);font-weight:700}.v46-progress{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;margin-bottom:12px!important}.v46-track{height:9px;border-radius:999px;background:#e9edf3;overflow:hidden}.v46-track i{display:block;height:100%;border-radius:999px;background:#55c997}.v46-pct{font-size:12px;font-weight:850;color:#778197}
#gamesGrid .game .nav23-game-actions{display:flex!important;justify-content:flex-end!important;align-items:center!important;gap:8px!important;padding:0 0 15px!important;margin-top:auto!important;position:static!important}
#gamesGrid .game .nav23-open-dex,#gamesGrid .game .r45-open{width:min(185px,100%)!important;min-height:54px!important;border:0!important;border-radius:17px!important;background:var(--v46-red)!important;color:#fff!important;font-size:15px!important;font-weight:900!important;margin:0!important}
#gamesGrid .game .game-active-btn.r451-star{position:absolute!important;top:13px!important;left:13px!important;right:auto!important;bottom:auto!important;width:42px!important;height:42px!important;min-width:42px!important;min-height:42px!important;margin:0!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;color:rgba(255,255,255,.96)!important;display:grid!important;place-items:center!important;z-index:9!important;text-shadow:0 2px 7px rgba(0,0,0,.4)!important}
#gamesGrid .game .game-active-btn.r451-star::before{content:'☆'!important;font-size:39px!important;line-height:1!important;font-family:Arial,sans-serif!important;font-weight:400!important;transform:none!important}
#gamesGrid .game .game-active-btn.r451-star.active,#gamesGrid .game .game-active-btn.r451-star.current{color:var(--v46-yellow)!important;background:transparent!important}
#gamesGrid .game .game-active-btn.r451-star.active::before,#gamesGrid .game .game-active-btn.r451-star.current::before{content:'★'!important;font-size:35px!important}
.mobile-nav{position:fixed!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;bottom:max(10px,env(safe-area-inset-bottom))!important;width:min(calc(100% - 32px),430px)!important;z-index:100!important;border-radius:28px!important;background:rgba(255,255,255,.96)!important;box-shadow:0 14px 40px rgba(24,38,68,.16)!important;backdrop-filter:blur(16px)!important;-webkit-backdrop-filter:blur(16px)!important}
body{overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
@media(max-width:680px){#games{padding:10px 14px calc(122px + env(safe-area-inset-bottom))!important}#gamesGrid .game{grid-template-columns:42% 58%!important;min-height:205px!important;border-radius:24px!important}#gamesGrid .game .r45-game-art{min-height:205px!important}#gamesGrid .game .r45-game-platform,#gamesGrid .game h3,#gamesGrid .game .r45-dexname,#gamesGrid .game .v46-stats,#gamesGrid .game .v46-progress,#gamesGrid .game .nav23-game-actions{margin-left:14px!important;margin-right:14px!important}#gamesGrid .game h3{font-size:17px!important}.v46-stats{gap:10px}.v46-stat{min-width:64px;padding-right:10px}.v46-stat strong{font-size:17px}.v46-stat span{font-size:10px}#gamesGrid .game .nav23-open-dex,#gamesGrid .game .r45-open{min-height:50px!important;font-size:14px!important}}
@media(max-width:430px){#gamesGrid .game{grid-template-columns:40% 60%!important;min-height:198px!important}#gamesGrid .game .r45-game-art{min-height:198px!important}#gamesGrid .game h3{font-size:16px!important}.v46-filters{gap:8px}.v46-chip{min-height:40px;padding:0 15px;font-size:12px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
const V46_TOTAL={letsgo:153,swsh:400,bdsp:151,arceus:242,sv:400,za:230};
function v46Percent(card){const m=(card.textContent||'').match(/(\d{1,3})%/);return m?Math.max(0,Math.min(100,Number(m[1]))):0}
function v46Library(){
 const grid=document.getElementById('gamesGrid');if(!grid)return;
 if(!document.querySelector('.v46-filters')){const box=document.createElement('div');box.className='v46-filters';box.innerHTML='<button class="v46-chip active">Todos</button><button class="v46-chip">Em andamento</button><button class="v46-chip">Completos</button><button class="v46-chip">Favoritos</button>';grid.parentNode.insertBefore(box,grid);box.querySelectorAll('button').forEach(b=>b.onclick=()=>{box.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active')})}
 grid.querySelectorAll('.game').forEach(card=>{
   const id=typeof r45GameId==='function'?r45GameId(card):'';if(!id)return;
   card.querySelector('.r45-current')?.remove();
   const total=V46_TOTAL[id]||0,pct=v46Percent(card),caught=Math.round(total*pct/100),missing=Math.max(0,total-caught);
   if(!card.querySelector('.v46-stats')){const d=document.createElement('div');d.className='v46-stats';d.innerHTML=`<div class="v46-stat"><strong>${total}</strong><span>entradas</span></div><div class="v46-stat"><strong>${missing}</strong><span>faltando</span></div>`;const dex=card.querySelector('.r45-dexname')||card.querySelector('h3');dex?.insertAdjacentElement('afterend',d)}
   if(!card.querySelector('.v46-progress')){const d=document.createElement('div');d.className='v46-progress';d.innerHTML=`<div class="v46-track"><i style="width:${pct}%"></i></div><span class="v46-pct">${pct}%</span>`;(card.querySelector('.v46-stats')||card.querySelector('h3'))?.insertAdjacentElement('afterend',d)}
   const star=card.querySelector('.game-active-btn');if(star){star.classList.add('r451-star');star.style.background='transparent';star.style.boxShadow='none'}
 });
 document.documentElement.dataset.v46Library='1';
}
const v46Render=window.renderGames;if(typeof v46Render==='function')window.renderGames=function(){const r=v46Render.apply(this,arguments);setTimeout(v46Library,80);return r};
const v46Set=window.setActiveGame;if(typeof v46Set==='function')window.setActiveGame=function(){const r=v46Set.apply(this,arguments);setTimeout(v46Library,100);return r};
setTimeout(v46Library,300);
if(new URLSearchParams(location.search).has('v46qa'))setTimeout(()=>{try{if(typeof r45EnsureLibrary==='function')r45EnsureLibrary()}catch(e){}setTimeout(()=>{v46Library();const cards=[...document.querySelectorAll('#gamesGrid .game')],stars=[...document.querySelectorAll('#gamesGrid .game .game-active-btn.r451-star')];const nav=document.querySelector('.mobile-nav');const ok=cards.length>=6&&stars.length===cards.length&&stars.every(b=>getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)'||getComputedStyle(b).backgroundColor==='transparent')&&nav&&getComputedStyle(nav).position==='fixed'&&document.querySelectorAll('.v46-stats').length===cards.length;document.documentElement.dataset.v46Qa=ok?'1':'0'},900)},500);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Library Reference 4.6 applied')

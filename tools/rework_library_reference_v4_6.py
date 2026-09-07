from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-library-reference" content="4.7"' not in s:
    s=s.replace('</head>','<meta name="living-dex-library-reference" content="4.7"/>\n</head>',1)
css=r'''
/* Library Reference 4.7 — final faithful mobile layout. */
:root{--v47-red:#ff5259;--v47-ink:#111a35;--v47-muted:#8c96aa;--v47-line:#e8edf4;--v47-yellow:#f7c843}
#games{max-width:980px!important;margin:0 auto!important;padding:16px 18px calc(124px + env(safe-area-inset-bottom))!important;overflow:visible!important}
#games .v47-hide{display:none!important}
#games .nav23-general-switch{position:sticky!important;top:0!important;z-index:20!important;margin:0 0 22px!important;background:rgba(255,255,255,.97)!important;border:0!important;border-radius:0 0 26px 26px!important;box-shadow:0 10px 30px rgba(24,37,70,.06)!important;padding:8px!important}
#games .nav23-general-switch button{min-height:48px!important;font-size:14px!important;font-weight:850!important;color:#9aa4b5!important;border-radius:18px!important}
#games .nav23-general-switch button.active{background:#fff0f1!important;color:var(--v47-red)!important;box-shadow:none!important}
.v46-filters{display:flex;gap:9px;overflow-x:auto;padding:0 0 14px;scrollbar-width:none}.v46-filters::-webkit-scrollbar{display:none}.v46-chip{white-space:nowrap;border:0;border-radius:999px;background:#f1f3f7;color:#7d879a;min-height:39px;padding:0 16px;font-size:12px;font-weight:850}.v46-chip.active{background:var(--v47-red);color:#fff}
#games #gamesGrid,#gamesGrid.nav23-compact-library{display:grid!important;grid-template-columns:1fr!important;gap:14px!important}
#gamesGrid .game{position:relative!important;display:grid!important;grid-template-columns:minmax(138px,36%) 1fr!important;align-items:stretch!important;width:100%!important;min-height:184px!important;padding:0!important;margin:0!important;border:1px solid rgba(229,234,243,.9)!important;border-radius:24px!important;background:#fff!important;overflow:hidden!important;box-shadow:0 10px 26px rgba(29,42,76,.07)!important}
#gamesGrid .game .r45-game-art{grid-column:1!important;grid-row:1 / span 12!important;height:100%!important;min-height:184px!important;margin:0!important;border-radius:0!important;background:#f4f6fa!important;overflow:hidden!important;display:flex!important;align-items:center!important;justify-content:center!important}
#gamesGrid .game .r45-game-art img{width:100%!important;height:100%!important;object-fit:contain!important;object-position:center!important;display:block!important;background:#f4f6fa!important}
#gamesGrid .game .r45-game-platform,#gamesGrid .game h3,#gamesGrid .game .r45-dexname,#gamesGrid .game .v46-stats,#gamesGrid .game .v46-progress,#gamesGrid .game .nav23-game-actions{grid-column:2!important;margin-left:14px!important;margin-right:14px!important}
#gamesGrid .game .r45-game-platform{margin-top:13px!important;margin-bottom:5px!important;width:max-content!important;padding:5px 9px!important;border-radius:10px!important;background:var(--v47-red)!important;color:#fff!important;font-size:8px!important;line-height:1!important;letter-spacing:.05em!important;font-weight:900!important}
#gamesGrid .game h3{font-size:16px!important;line-height:1.08!important;letter-spacing:-.025em!important;color:var(--v47-ink)!important;margin-top:0!important;margin-bottom:3px!important;max-width:100%!important}
#gamesGrid .game .r45-dexname{font-size:11px!important;color:var(--v47-muted)!important;margin-top:0!important;margin-bottom:8px!important}
#gamesGrid .game .tiny,#gamesGrid .game .pill,#gamesGrid .game .r45-progressline,#gamesGrid .game .r45-current,#gamesGrid .game .orb{display:none!important}
.v46-stats{display:flex;gap:12px;align-items:flex-end;margin-bottom:7px!important}.v46-stat{min-width:68px;padding-right:12px;border-right:1px solid var(--v47-line)}.v46-stat:last-child{border-right:0}.v46-stat strong{display:block;font-size:17px;line-height:1;color:var(--v47-ink);font-weight:850}.v46-stat span{display:block;margin-top:3px;font-size:10px;color:var(--v47-muted);font-weight:700}.v46-progress{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center;margin-bottom:9px!important}.v46-track{height:7px;border-radius:999px;background:#e9edf3;overflow:hidden}.v46-track i{display:block;height:100%;border-radius:999px;background:#55c997}.v46-pct{font-size:11px;font-weight:850;color:#778197}
#gamesGrid .game .nav23-game-actions{display:flex!important;justify-content:flex-end!important;align-items:center!important;padding:0 0 13px!important;margin-top:auto!important;position:static!important}
#gamesGrid .game .nav23-open-dex,#gamesGrid .game .r45-open{width:min(170px,100%)!important;min-height:46px!important;border:0!important;border-radius:15px!important;background:var(--v47-red)!important;color:#fff!important;font-size:13px!important;font-weight:900!important;margin:0!important}
#gamesGrid .game .game-active-btn.r451-star{position:absolute!important;top:10px!important;left:10px!important;right:auto!important;bottom:auto!important;width:30px!important;height:30px!important;min-width:30px!important;min-height:30px!important;margin:0!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;color:rgba(255,255,255,.98)!important;display:grid!important;place-items:center!important;z-index:9!important;text-shadow:0 2px 6px rgba(0,0,0,.42)!important}
#gamesGrid .game .game-active-btn.r451-star::before{content:'☆'!important;font-size:27px!important;line-height:1!important;font-family:Arial,sans-serif!important;font-weight:400!important}
#gamesGrid .game .game-active-btn.r451-star.active,#gamesGrid .game .game-active-btn.r451-star.current{color:var(--v47-yellow)!important;background:transparent!important}
#gamesGrid .game .game-active-btn.r451-star.active::before,#gamesGrid .game .game-active-btn.r451-star.current::before{content:'★'!important;font-size:24px!important}
.mobile-nav{position:fixed!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;bottom:max(10px,env(safe-area-inset-bottom))!important;width:min(calc(100% - 28px),430px)!important;z-index:100!important;border-radius:26px!important;background:rgba(255,255,255,.97)!important;box-shadow:0 14px 40px rgba(24,38,68,.16)!important;backdrop-filter:blur(16px)!important;-webkit-backdrop-filter:blur(16px)!important}
body{overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
@media(max-width:680px){#games{padding:10px 14px calc(120px + env(safe-area-inset-bottom))!important}#gamesGrid .game{grid-template-columns:39% 61%!important;min-height:180px!important;border-radius:22px!important}#gamesGrid .game .r45-game-art{min-height:180px!important}#gamesGrid .game h3{font-size:15px!important}.v46-stat strong{font-size:16px!important}}
@media(max-width:430px){#gamesGrid .game{grid-template-columns:38% 62%!important;min-height:176px!important}#gamesGrid .game .r45-game-art{min-height:176px!important}#gamesGrid .game .r45-game-platform,#gamesGrid .game h3,#gamesGrid .game .r45-dexname,#gamesGrid .game .v46-stats,#gamesGrid .game .v46-progress,#gamesGrid .game .nav23-game-actions{margin-left:11px!important;margin-right:11px!important}#gamesGrid .game .nav23-open-dex,#gamesGrid .game .r45-open{min-height:44px!important;font-size:12px!important}}
'''
s=s.replace('</head>','<style id="v47-final-library">'+css+'</style>\n</head>',1)
js=r'''
const V47_TOTAL={letsgo:153,swsh:400,bdsp:151,arceus:242,sv:400,za:230};
function v47Pct(card){const e=card.querySelector('.v46-pct');if(e){const n=parseInt(e.textContent)||0;return Math.max(0,Math.min(100,n))}const m=(card.textContent||'').match(/(\d{1,3})%/);return m?Math.max(0,Math.min(100,Number(m[1]))):0}
function v47CleanLegacy(card){
 card.querySelectorAll('.orb,.r45-current').forEach(x=>x.remove());
 [...card.querySelectorAll('*')].forEach(el=>{if(el.classList.contains('r45-game-platform')||el.closest('.v46-stats,.v46-progress'))return;const t=(el.textContent||'').trim().replace(/\s+/g,' ');if(/^\d+%\s*DEX$/i.test(t)||/^\d+%\s*faltando$/i.test(t)||/^NINTENDO SWITCH(?:\s*\/\s*SWITCH 2)?$/i.test(t)){el.remove()}});
}
function v47HideDuplicateHeader(){document.querySelectorAll('#games h1,#games h2').forEach(h=>{if((h.textContent||'').trim().toLowerCase()==='jogos'){const sec=h.closest('.section')||h.parentElement;sec&&sec.classList.add('v47-hide')}})}
function v47Library(){
 const grid=document.getElementById('gamesGrid');if(!grid)return;v47HideDuplicateHeader();
 if(!document.querySelector('.v46-filters')){const box=document.createElement('div');box.className='v46-filters';box.innerHTML='<button class="v46-chip active">Todos (6)</button><button class="v46-chip">Em andamento</button><button class="v46-chip">Completos</button><button class="v46-chip">Favoritos</button>';grid.parentNode.insertBefore(box,grid);box.querySelectorAll('button').forEach(b=>b.onclick=()=>{box.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active')})}
 grid.querySelectorAll('.game').forEach(card=>{
   const id=typeof r45GameId==='function'?r45GameId(card):'';if(!id)return;v47CleanLegacy(card);
   const total=V47_TOTAL[id]||0,pct=v47Pct(card),caught=Math.round(total*pct/100),missing=Math.max(0,total-caught);
   let st=card.querySelector('.v46-stats');if(!st){st=document.createElement('div');st.className='v46-stats';(card.querySelector('.r45-dexname')||card.querySelector('h3'))?.insertAdjacentElement('afterend',st)}st.innerHTML=`<div class="v46-stat"><strong>${total}</strong><span>entradas</span></div><div class="v46-stat"><strong>${missing}</strong><span>faltando</span></div>`;
   let pr=card.querySelector('.v46-progress');if(!pr){pr=document.createElement('div');pr.className='v46-progress';st.insertAdjacentElement('afterend',pr)}pr.innerHTML=`<div class="v46-track"><i style="width:${pct}%"></i></div><span class="v46-pct">${pct}%</span>`;
   const star=card.querySelector('.game-active-btn');if(star){star.classList.add('r451-star');star.style.background='transparent';star.style.boxShadow='none'}
 });document.documentElement.dataset.v47Library='1';
}
const v47Render=window.renderGames;if(typeof v47Render==='function')window.renderGames=function(){const r=v47Render.apply(this,arguments);setTimeout(v47Library,100);return r};
const v47Set=window.setActiveGame;if(typeof v47Set==='function')window.setActiveGame=function(){const r=v47Set.apply(this,arguments);setTimeout(v47Library,120);return r};
setTimeout(v47Library,320);
if(new URLSearchParams(location.search).has('v47qa'))setTimeout(()=>{try{if(typeof r45EnsureLibrary==='function')r45EnsureLibrary()}catch(e){}setTimeout(()=>{v47Library();const cards=[...document.querySelectorAll('#gamesGrid .game')],stars=[...document.querySelectorAll('#gamesGrid .game .game-active-btn.r451-star')],nav=document.querySelector('.mobile-nav'),legacy=[...document.querySelectorAll('#gamesGrid .game .orb')],imgs=[...document.querySelectorAll('#gamesGrid .game .r45-game-art img')];const duplicateJogos=[...document.querySelectorAll('#games h1,#games h2')].some(h=>(h.textContent||'').trim().toLowerCase()==='jogos'&&getComputedStyle(h.closest('.section')||h.parentElement).display!=='none');const ok=cards.length===6&&stars.length===6&&legacy.length===0&&imgs.length===6&&imgs.every(i=>getComputedStyle(i).objectFit==='contain')&&nav&&getComputedStyle(nav).position==='fixed'&&!duplicateJogos&&document.querySelectorAll('.v46-stats').length===6&&document.querySelectorAll('.v46-progress').length===6;document.documentElement.dataset.v47Qa=ok?'1':'0'},1000)},500);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Library Reference 4.7 applied — legacy black orb removed, duplicates cleaned, images uncropped')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-visible" content="7.1.1"' not in s:s=s.replace('</head>','<meta name="living-dex-box-visible" content="7.1.1"/>\n</head>',1)
css=r'''
/* Box 7.1.1 — expose Box in the real bottom navigation used by the app. */
.mobile-nav{grid-template-columns:repeat(4,1fr)!important}
.mobile-nav .ld711-navbtn{border:0;background:transparent;color:#9aa4b4;min-height:64px;border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;font-size:10px;font-weight:850}
.mobile-nav .ld711-navbtn.active{background:#fff0f0;color:#ff5757}
.mobile-nav .ld711-navbtn svg{width:21px;height:21px}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box visibility + loading fix 7.1.1
function ld711RealNav(){return document.querySelector('.mobile-nav')||document.querySelector('.mnav')}
function ld711RenderNav(){
 const nav=ld711RealNav();if(!nav)return;
 nav.innerHTML=`<button class="ld711-navbtn" data-ld711="home" onclick="ld7Home()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11 12 4l9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg><span>Início</span></button><button class="ld711-navbtn" data-ld711="games" onclick="ld7Library()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/></svg><span>Biblioteca</span></button><button class="ld711-navbtn" data-ld711="dex" onclick="ld7OpenCurrent()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><circle cx="12" cy="12" r="3"/></svg><span>Living Dex</span></button><button class="ld711-navbtn" data-ld711="box" onclick="ld71Open()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="15" rx="3"/><path d="M3 10h18M9 10v10M15 10v10"/></svg><span>Box</span></button>`;
 ld711NavState()
}
function ld711NavState(){
 const box=document.getElementById('ld71BoxView')?.classList.contains('active');
 const page=document.querySelector('.view.active')?.id;
 let key=box?'box':document.body.classList.contains('game-dex-focus')?'dex':page==='games'?'games':'home';
 document.querySelectorAll('.ld711-navbtn').forEach(b=>b.classList.toggle('active',b.dataset.ld711===key))
}
// Load the selected game's Dex first; Box must never open empty.
window.ld71Open=async function(){
 ld71Ensure();const g=ld71Game();
 try{
   if(!(Array.isArray(currentDex)&&currentDex.length&&currentGame?.id===g.id)) await openGame(g.id);
 }catch(e){}
 document.body.classList.remove('game-dex-focus');
 const e=document.getElementById('ld71BoxView');e.classList.add('active');
 ld71Render();ld711RenderNav();ld711NavState()
}
const ld711OldAudit=window.ld7Audit;if(typeof ld711OldAudit==='function')window.ld7Audit=function(){const r=ld711OldAudit.apply(this,arguments);setTimeout(ld711RenderNav,0);return r};
const ld711OldHome=window.renderActiveGameHome;if(typeof ld711OldHome==='function')window.renderActiveGameHome=function(){const r=ld711OldHome.apply(this,arguments);setTimeout(ld711RenderNav,0);return r};
const ld711OldGames=window.renderGames;if(typeof ld711OldGames==='function')window.renderGames=function(){const r=ld711OldGames.apply(this,arguments);setTimeout(ld711RenderNav,0);return r};
setTimeout(ld711RenderNav,0);setTimeout(ld711RenderNav,250);setTimeout(ld711RenderNav,800);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box visibility 7.1.1 applied')
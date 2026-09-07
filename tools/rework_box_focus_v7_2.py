from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-focus" content="7.2"' not in s:s=s.replace('</head>','<meta name="living-dex-box-focus" content="7.2"/>\n</head>',1)
css=r'''
/* Box 7.2 — focused Box-only screen. */
#ld71BoxView{padding-bottom:calc(28px + env(safe-area-inset-bottom))!important}
#ld71BoxView .ld71-nav{display:none!important}
#ld71BoxView .ld71-tabs{grid-template-columns:1fr!important}
#ld71BoxView .ld71-tab{display:none!important}
#ld71BoxView .ld72-games{display:flex!important;align-items:center;justify-content:center;gap:9px;border:0;background:#3478e5;color:#fff;border-radius:15px;min-height:52px;font-weight:900;font-size:15px;width:100%}
#ld71BoxView .ld72-games svg{width:20px;height:20px}
#ld72GameSheet{display:none;position:fixed;inset:0;z-index:1100;background:rgba(18,28,48,.36);padding:calc(20px + env(safe-area-inset-top)) 14px calc(20px + env(safe-area-inset-bottom));align-items:flex-end}
#ld72GameSheet.active{display:flex}
.ld72-sheet{background:#fff;border-radius:28px 28px 22px 22px;width:min(100%,620px);margin:auto auto 0;padding:18px;max-height:78vh;overflow:auto;box-shadow:0 20px 60px rgba(20,35,65,.22)}
.ld72-sheethead{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}.ld72-sheethead h2{margin:0;font-size:22px}.ld72-close{width:42px;height:42px;border:0;border-radius:14px;background:#f1f4f8;font-size:22px}.ld72-gameslist{display:grid;gap:9px}.ld72-gameitem{border:1px solid #e5eaf2;background:#f8fafc;border-radius:18px;padding:10px;display:grid;grid-template-columns:50px 1fr auto;align-items:center;gap:12px;text-align:left;color:#172440}.ld72-gameitem.active{border-color:#3478e5;background:#edf4ff}.ld72-gameitem img{width:50px;height:66px;object-fit:cover;border-radius:10px}.ld72-gameitem b{display:block;font-size:14px}.ld72-gameitem small{display:block;color:#7d879a;margin-top:3px}.ld72-check{font-size:20px;color:#3478e5;font-weight:900}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Focused Box + game selector 7.2
function ld72Cover(g){const map={sv:'sv.jpg',za:'za.jpg',swsh:'swsh.jpg',bdsp:'bdsp.jpg',letsgo:'letsgo.jpg',arceus:'arceus.jpg'};return `assets/ui45/${map[g?.id]||'sv.jpg'}`}
function ld72EnsureSheet(){if(document.getElementById('ld72GameSheet'))return;document.body.insertAdjacentHTML('beforeend','<div id="ld72GameSheet" onclick="if(event.target===this)ld72CloseGames()"><section class="ld72-sheet"><div class="ld72-sheethead"><h2>Selecionar jogo</h2><button class="ld72-close" onclick="ld72CloseGames()">×</button></div><div id="ld72GamesList" class="ld72-gameslist"></div></section></div>')}
function ld72OpenGames(){ld72EnsureSheet();const root=document.getElementById('ld72GamesList');const active=state.activeGameId;root.innerHTML=GAMES.map(g=>`<button class="ld72-gameitem ${g.id===active?'active':''}" onclick="ld72SelectGame('${g.id}')"><img src="${ld72Cover(g)}"><span><b>${g.name}</b><small>Abrir boxes deste jogo</small></span><span class="ld72-check">${g.id===active?'✓':'›'}</span></button>`).join('');document.getElementById('ld72GameSheet').classList.add('active')}
function ld72CloseGames(){document.getElementById('ld72GameSheet')?.classList.remove('active')}
async function ld72SelectGame(id){try{state.activeGameId=id;saveState?.();await openGame(id)}catch(e){}ld71BoxIndex=0;ld72CloseGames();ld71Render();ld72Focus()}
function ld72Focus(){const root=document.getElementById('ld71BoxView');if(!root)return;root.querySelector('.ld71-nav')?.remove();const tabs=root.querySelector('.ld71-tabs');if(tabs){tabs.innerHTML=`<button class="ld72-games" onclick="ld72OpenGames()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/></svg><span>Jogos</span></button>`}root.querySelector('.ld71-switch')?.remove()}
const ld72OldRender=window.ld71Render;window.ld71Render=function(){const r=ld72OldRender.apply(this,arguments);ld72Focus();return r}
const ld72OldOpen=window.ld71Open;window.ld71Open=async function(){const r=await ld72OldOpen.apply(this,arguments);ld72Focus();document.querySelector('.mobile-nav')?.style.setProperty('display','none','important');return r}
const ld72OldClose=window.ld71Close;window.ld71Close=function(){document.querySelector('.mobile-nav')?.style.removeProperty('display');return ld72OldClose.apply(this,arguments)}
ld72EnsureSheet();setTimeout(()=>{if(document.getElementById('ld71BoxView')?.classList.contains('active'))ld72Focus()},300)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Focused Box 7.2 applied')
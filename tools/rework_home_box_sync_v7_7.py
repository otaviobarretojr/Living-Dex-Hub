from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-box-sync" content="7.7.0"' in s:
    print('Home Box Sync 7.7.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-home-box-sync" content="7.7.0"/>\n</head>',1)
css=r'''
/* 7.7.0 — Inicio rework based on approved reference; one clean game-cover card. */
#home .home-current-shell{max-width:780px!important;margin:0 auto!important;padding:10px 0 36px!important}
#home .playing-card{background:transparent!important;border:0!important;box-shadow:none!important;overflow:visible!important}
.home77-card{position:relative;min-height:540px;border-radius:34px;overflow:hidden;background:#101828;box-shadow:0 24px 58px rgba(23,33,60,.18);border:1px solid rgba(255,255,255,.72);cursor:pointer}
.home77-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;display:block;transform:scale(1.01)}
.home77-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,20,36,.02) 0%,rgba(12,20,36,.06) 46%,rgba(12,20,36,.86) 100%)}
.home77-top{position:absolute;top:24px;left:24px;right:24px;z-index:2;display:flex;align-items:center;justify-content:space-between;gap:12px}
.home77-badge,.home77-platform{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;font-weight:900;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.home77-badge{gap:9px;padding:12px 18px;background:#ff5757;color:#fff;font-size:13px;box-shadow:0 10px 24px rgba(255,87,87,.24)}
.home77-badge i{width:8px;height:8px;border-radius:50%;background:#fff}
.home77-platform{padding:11px 16px;background:rgba(30,70,120,.55);border:1px solid rgba(255,255,255,.35);color:#fff;font-size:12px}
.home77-bottom{position:absolute;z-index:2;left:26px;right:26px;bottom:26px;color:#fff}
.home77-progress{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:end}
.home77-count{font-size:20px;font-weight:950;letter-spacing:-.02em;text-shadow:0 2px 12px rgba(0,0,0,.22)}
.home77-pct{font-size:46px;line-height:.9;font-weight:950;letter-spacing:-.05em;text-shadow:0 2px 12px rgba(0,0,0,.22)}
.home77-bar{grid-column:1/-1;height:10px;border-radius:999px;background:rgba(255,255,255,.48);overflow:hidden;margin-top:4px}
.home77-bar i{display:block;height:100%;border-radius:inherit;background:#ff5757;transition:width .25s ease}
.home77-hint{margin-top:12px;font-size:11px;font-weight:800;color:rgba(255,255,255,.78);letter-spacing:.02em}
#home .home51-journey,#home .home232-journey,#home .home-journey-summary{display:none!important}
@media(max-width:680px){#home .home-current-shell{padding:6px 2px 26px!important}.home77-card{min-height:500px;border-radius:30px}.home77-top{top:20px;left:18px;right:18px}.home77-bottom{left:20px;right:20px;bottom:22px}.home77-badge{padding:10px 15px;font-size:12px}.home77-platform{padding:9px 13px;font-size:11px}.home77-count{font-size:18px}.home77-pct{font-size:42px}}
@media(max-width:390px){.home77-card{min-height:470px}.home77-count{font-size:16px}.home77-pct{font-size:38px}.home77-platform{font-size:10px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Home Box Sync 7.7.0
function home77Art(g){
 const key=String(g?.id||'').toLowerCase(),name=String(g?.name||'').toLowerCase();
 if(key.includes('lets')||name.includes("let's go"))return 'assets/ui45/letsgo.jpg';
 if(key.includes('swsh')||key.includes('sword')||key.includes('shield')||name.includes('sword')||name.includes('shield'))return 'assets/ui45/swsh.jpg';
 if(key.includes('bdsp')||key.includes('bd')||key.includes('sp')||name.includes('diamond')||name.includes('pearl'))return 'assets/ui45/bdsp.jpg';
 if(key.includes('arceus')||name.includes('arceus'))return 'assets/ui45/arceus.jpg';
 if(key.includes('za')||name.includes('z-a'))return 'assets/ui45/za.jpg';
 return 'assets/ui45/sv.jpg'
}
function home77Truthy(v){return v===true||v?.caught||v?.registered||v?.owned}
function home77Progress(g){
 let fallback={caught:0,total:Number(g?.count||0),pct:0};
 try{const p=activeGameProgress(g);if(p)fallback={caught:Number(p.caught||0),total:Number(p.total||g?.count||0),pct:Number(p.pct||0)}}catch(e){}
 let total=fallback.total||Number(g?.count||0),done=0;
 try{
  const dex=(Array.isArray(currentDex)&&currentGame?.id===g.id)?currentDex:[];
  if(dex.length){
   total=dex.length;
   const ids=new Set();
   if(typeof ld71RegSet==='function')for(const id of ld71RegSet())ids.add(Number(id));
   done=dex.filter(x=>ids.has(Number(x.id||x))).length
  }
 }catch(e){}
 try{
  const prefix=String(g.id)+':';
  const specific=Object.entries(state?.games||{}).filter(([k,v])=>k.startsWith(prefix)&&home77Truthy(v)).length;
  if(specific>0)done=specific
 }catch(e){}
 if(!done)done=fallback.caught;
 done=Math.min(done,total||done);
 const pct=total?Math.round(done/total*100):0;
 return {caught:done,total,pct}
}
function renderActiveGameHome(){
 const home=document.getElementById('home');if(!home)return;
 let shell=home.querySelector('.home-current-shell');if(!shell){shell=document.createElement('div');shell.className='home-current-shell';home.prepend(shell)}
 const g=GAMES.find(x=>x.id===state.activeGameId);
 if(!g){shell.innerHTML='<div class="empty-current"><div class="icon">◉</div><h2>Nenhum jogo atual</h2><p>Escolha um jogo na Biblioteca.</p><button class="btn primary" onclick="go(\'games\')">Escolher jogo</button></div>';return}
 const p=home77Progress(g),art=home77Art(g);
 shell.innerHTML=`<div class="playing-card"><button class="home77-card" type="button" onclick="typeof ld71Open==='function'?ld71Open():continueActiveGame()" aria-label="Abrir Box de ${g.name}" style="width:100%;padding:0;border:0;text-align:left"><img class="home77-bg" src="${art}" alt="${g.name}" draggable="false"><span class="home77-shade"></span><span class="home77-top"><span class="home77-badge"><i></i>Jogo atual</span><span class="home77-platform">${g.platform||'Nintendo Switch'}</span></span><span class="home77-bottom"><span class="home77-progress"><span class="home77-count">${p.caught} / ${p.total} Pokémon</span><span class="home77-pct">${p.pct}%</span><span class="home77-bar"><i style="width:${p.pct}%"></i></span></span><span class="home77-hint">Toque para abrir a Box</span></span></button></div>`
}
window.renderActiveGameHome=renderActiveGameHome;
const home77OldCommit=window.ld75CommitBox;
if(typeof home77OldCommit==='function')window.ld75CommitBox=function(){const r=home77OldCommit.apply(this,arguments);setTimeout(()=>{try{renderActiveGameHome()}catch(e){}},0);return r};
const home77OldToggle=window.ld71Toggle;
if(typeof home77OldToggle==='function')window.ld71Toggle=function(){const r=home77OldToggle.apply(this,arguments);setTimeout(()=>{try{renderActiveGameHome()}catch(e){}},120);return r};
setTimeout(()=>{try{renderActiveGameHome()}catch(e){}},180)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Home Box Sync 7.7.0 applied')

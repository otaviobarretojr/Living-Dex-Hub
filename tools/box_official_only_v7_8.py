from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-official-only" content="7.8.0"' in s:
    print('Box official-only 7.8.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-box-official-only" content="7.8.0"/>\n</head>',1)
css=r'''
/* 7.8.0 — Box is the only official Pokemon library. */
#games,#dex,#gameDex,#nationalDex,#library,#livingDex{display:none!important}
.mnav{grid-template-columns:repeat(2,1fr)!important}
.ld73-pill{display:none!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box official-only 7.8.0
function ld78Truthy(v){return v===true||v?.caught||v?.registered||v?.owned}
function ld78GameEntries(gameId){
 const prefix=String(gameId)+':';
 return Object.entries(state?.games||{}).filter(([k,v])=>k.startsWith(prefix)&&ld78Truthy(v))
}
function ld78MigrateLegacyCurrentGame(){
 try{
  const g=currentGame, dex=Array.isArray(currentDex)?currentDex:[];
  if(!g?.id||!dex.length)return false;
  state.games=state.games||{};
  if(ld78GameEntries(g.id).length)return false;
  const legacy=new Set();
  const add=o=>{if(!o)return;Object.entries(o).forEach(([k,v])=>{if(ld78Truthy(v))legacy.add(Number(k))})};
  add(state.caught);add(state.registered);add(state.owned);add(state.dex);
  let moved=0;
  for(const row of dex){const id=Number(row.id||row);if(legacy.has(id)){state.games[g.id+':'+id]=true;moved++}}
  if(moved){try{persist?.()}catch(e){try{saveState?.()}catch(_){}}}
  return moved>0
 }catch(e){return false}
}
window.ld71RegSet=function(){
 const ids=new Set();const id=currentGame?.id||state?.activeGameId;if(!id)return ids;
 for(const [k,v] of ld78GameEntries(id)){const n=Number(k.split(':').pop());if(Number.isFinite(n))ids.add(n)}
 return ids
};
function ld78OfficialProgress(g){
 const total=(Array.isArray(currentDex)&&currentGame?.id===g?.id&&currentDex.length)?currentDex.length:Number(g?.count||0);
 const done=ld78GameEntries(g?.id).length;
 return {caught:Math.min(done,total||done),total,pct:total?Math.round(Math.min(done,total)/total*100):0}
}
window.home77Progress=ld78OfficialProgress;
function ld78Nav(){
 const nav=document.querySelector('.mnav');if(!nav)return;
 nav.innerHTML=`<button class="ld7-navbtn" data-ld7="home" onclick="ld7Home()"><span>Início</span></button><button class="ld7-navbtn" data-ld7="box" onclick="ld71Open()"><span>Box</span></button>`;
 nav.style.gridTemplateColumns='repeat(2,1fr)';ld78NavState()
}
function ld78NavState(){
 document.querySelectorAll('.ld7-navbtn').forEach(b=>b.classList.remove('active'));
 const box=document.getElementById('ld71BoxView')?.classList.contains('active');
 document.querySelector(`.ld7-navbtn[data-ld7="${box?'box':'home'}"]`)?.classList.add('active')
}
window.ld7Nav=ld78Nav;window.ld7NavState=ld78NavState;
window.ld7Library=function(){return ld71Open()};
window.ld7OpenCurrent=function(){return ld71Open()};
const ld78OldGo=window.go;
if(typeof ld78OldGo==='function')window.go=function(page){if(page==='games'||page==='dex'||page==='library'||page==='livingDex')return ld71Open();return ld78OldGo.apply(this,arguments)};
const ld78OldLoad=window.ld73LoadGame;
if(typeof ld78OldLoad==='function')window.ld73LoadGame=async function(id){const r=await ld78OldLoad.apply(this,arguments);ld78MigrateLegacyCurrentGame();try{ld71Render()}catch(e){};try{renderActiveGameHome()}catch(e){};return r};
const ld78OldOpen=window.ld71Open;
if(typeof ld78OldOpen==='function')window.ld71Open=async function(){const r=await ld78OldOpen.apply(this,arguments);ld78MigrateLegacyCurrentGame();try{ld71Render()}catch(e){};try{renderActiveGameHome()}catch(e){};ld78NavState();return r};
const ld78OldCommit=window.ld75CommitBox;
if(typeof ld78OldCommit==='function')window.ld75CommitBox=function(){const r=ld78OldCommit.apply(this,arguments);try{renderActiveGameHome()}catch(e){};return r};
const ld78OldRender=window.ld71Render;
if(typeof ld78OldRender==='function')window.ld71Render=function(){const r=ld78OldRender.apply(this,arguments);const p=document.querySelector('#ld71BoxView .ld71-game p');if(p){const t=ld71Dex().length||0,b=Math.max(1,Math.ceil(t/30));p.innerHTML=`Box oficial <span class="ld73-gamebadge">${t} Pokémon · ${b} Boxes</span>`}return r};
const ld78OldGames=window.ld72OpenGames;
if(typeof ld78OldGames==='function')window.ld72OpenGames=function(){const r=ld78OldGames.apply(this,arguments);document.querySelectorAll('#ld72GamesList .ld73-pill').forEach(x=>x.remove());document.querySelectorAll('#ld72GamesList small').forEach(x=>x.textContent='30 Pokémon por Box');return r};
setTimeout(()=>{try{ld78MigrateLegacyCurrentGame();renderActiveGameHome();ld78Nav()}catch(e){}},220)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box official-only 7.8.0 applied')

from pathlib import Path
import runpy
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-game-selector-commit" content="7.3.2"' not in s:s=s.replace('</head>','<meta name="living-dex-game-selector-commit" content="7.3.2"/>\n</head>',1)
css=r'''
/* 7.3.2 — selected game is the single source of truth before the selector closes. */
.ld72-gameitem.ld732-selected{border-color:#3478e5!important;background:#eaf2ff!important;box-shadow:inset 0 0 0 1px #3478e5}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Selector commit + Box refresh 7.3.2
function ld732WaitGame(id,timeout=1800){
 return new Promise(resolve=>{
   const started=Date.now();
   const tick=()=>{
     const ready=currentGame?.id===id&&Array.isArray(currentDex)&&currentDex.length>0;
     if(ready){resolve(true);return}
     if(Date.now()-started>=timeout){resolve(false);return}
     setTimeout(tick,60)
   };tick()
 })
}
function ld732SelectVisual(id){
 document.querySelectorAll('#ld72GamesList .ld72-gameitem').forEach(btn=>{
   const target=String(btn.getAttribute('onclick')||'').includes(`'${id}'`);
   btn.classList.toggle('active',target);
   btn.classList.toggle('ld732-selected',target);
   btn.classList.toggle('ld731-pending',target);
   btn.classList.toggle('ld731-disabled',!target);
   const check=btn.querySelector('.ld72-check');if(check)check.textContent=target?'✓':'›'
 })
}
function ld732CommitState(id){
 state.activeGameId=id;
 try{saveState?.()}catch(e){}
 ld71BoxIndex=0
}
window.ld73SelectGame=async function(id){
 ld732SelectVisual(id);
 ld732CommitState(id);
 let ok=false;
 try{
   await openGame(id);
   ok=await ld732WaitGame(id)
 }catch(e){ok=false}
 if(!ok){
   try{await openGame(id);ok=await ld732WaitGame(id,1200)}catch(e){}
 }
 if(!ok){ld731RestoreSelector?.();ld72OpenGames?.();return}
 ld732CommitState(id);
 ld73BoxByGame[id]=0;
 ld71Render();
 ld72Focus();
 requestAnimationFrame(()=>{ld71Render();ld72Focus()});
 setTimeout(()=>{ld71Render();ld72Focus();ld72CloseGames();ld731RestoreSelector?.()},120)
}
window.ld72SelectGame=window.ld73SelectGame;
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Game selector commit 7.3.2 applied')
runpy.run_path(str(Path(__file__).with_name('migrate_box_library_v7_4.py')), run_name='__main__')
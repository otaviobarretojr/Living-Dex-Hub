from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')

js=r'''
// Living Dex Hub v1.5.1 — contextual quick add/remove by game + selected version.
state.versionCaught=state.versionCaught||{};
function ui151VersionKey(gameId,version,id){return `${gameId}:${version||''}:${id}`}
function ui151QuickContext(card){
 const id=ui15SpeciesId(card),inGame=!!card?.closest?.('#dexGrid');
 if(inGame&&currentGame){
  const version=typeof selectedVersion==='function'?selectedVersion(currentGame.id):((state.versions||{})[currentGame.id]||'');
  return {scope:'game',id,gameId:currentGame.id,gameName:currentGame.name,version};
 }
 return {scope:'global',id};
}
function ui151GameOwned(id,gameId,version){
 const k=ui151VersionKey(gameId,version,id);
 if(Object.prototype.hasOwnProperty.call(state.versionCaught||{},k))return state.versionCaught[k]===true;
 return !!state.games?.[`${gameId}:${id}`];
}
function ui151SpeciesLabel(card,id){
 const h=card?.querySelector?.('h4');return (h?.textContent||`Pokémon #${id}`).trim();
}
function ui151AddGame(ctx){
 const {id,gameId,version}=ctx,k=ui151VersionKey(gameId,version,id);
 state.versionCaught[k]=true;
 state.games[`${gameId}:${id}`]=true;
 state.global[id]=true;
 let matching=instancesForSpecies(id).find(x=>x.originGame===gameId&&(x.version||'')===(version||''));
 if(!matching){
  const uid=addSpecimenInstance(id,{originGame:gameId,version:version||''});
  matching=state.specimenInstances?.[uid];
 }
 if(matching){
  matching.originGame=gameId;matching.version=version||'';
  matching.currentLocation=matching.currentLocation||{};
  matching.currentLocation.type='game';matching.currentLocation.gameId=gameId;
 }
 persist();
}
function ui151RemoveGame(ctx,card){
 const {id,gameId,version,gameName}=ctx,name=ui151SpeciesLabel(card,id);
 const where=version||gameName||gameId;
 if(!confirm(`Remover ${name} de ${where}?\n\nEste registro será removido somente desta versão.`))return false;
 const k=ui151VersionKey(gameId,version,id);state.versionCaught[k]=false;
 for(const [uid,x] of Object.entries(state.specimenInstances||{})){
  if(Number(x.speciesId)!==Number(id))continue;
  const sameGame=x.originGame===gameId||x.currentLocation?.gameId===gameId;
  const sameVersion=(x.version||'')===(version||'');
  if(sameGame&&sameVersion)delete state.specimenInstances[uid];
 }
 const prefix=`${gameId}:`,suffix=`:${id}`;
 const anotherVersion=Object.entries(state.versionCaught||{}).some(([key,val])=>key.startsWith(prefix)&&key.endsWith(suffix)&&val===true);
 if(!anotherVersion)delete state.games[`${gameId}:${id}`];
 const anyGame=Object.keys(state.games||{}).some(key=>key.endsWith(`:${id}`)&&state.games[key]);
 const anyInstance=instancesForSpecies(id).length>0;
 if(!anyGame&&!anyInstance)delete state.global[id];
 persist();return true;
}
function ui151RemoveGlobal(id,card){
 const name=ui151SpeciesLabel(card,id);
 if(!confirm(`Remover ${name} do Living Dex Global?`))return false;
 delete state.global[id];persist();return true;
}
function ui151RefreshViews(){
 if(currentGame&&document.getElementById('dexGrid'))renderDex();
 if(document.getElementById('global')?.classList.contains('active'))renderGlobal();
 if(document.getElementById('missing')?.classList.contains('active'))renderMissing();
 if(typeof updateStats==='function')updateStats();
 setTimeout(ui15DecorateDex,0);
}
function ui15QuickCapture(ev,card){
 ev.preventDefault();ev.stopPropagation();
 const ctx=ui151QuickContext(card);if(!ctx.id)return;
 if(ctx.scope==='game'){
  const owned=ui151GameOwned(ctx.id,ctx.gameId,ctx.version);
  if(owned){if(!ui151RemoveGame(ctx,card))return}else ui151AddGame(ctx);
 }else{
  const owned=!!state.global[ctx.id];
  if(owned){if(!ui151RemoveGlobal(ctx.id,card))return}else{state.global[ctx.id]=true;persist()}
 }
 ui151RefreshViews();
}
function ui15DecorateDex(){
 document.querySelectorAll('.pk').forEach(card=>{
  const ctx=ui151QuickContext(card);if(!ctx.id)return;
  let b=card.querySelector('.quick-catch');
  if(!b){b=document.createElement('button');b.type='button';b.className='quick-catch';card.appendChild(b)}
  const owned=ctx.scope==='game'?ui151GameOwned(ctx.id,ctx.gameId,ctx.version):!!state.global[ctx.id];
  const where=ctx.scope==='game'?(ctx.version||ctx.gameName||'neste jogo'):'Living Dex Global';
  b.setAttribute('aria-label',owned?`Remover de ${where}`:`Adicionar em ${where}`);
  b.title=owned?`Registrado em ${where} — toque para remover`:`Adicionar em ${where}`;
  b.textContent=owned?'✓':'+';
  if(b.classList.contains('is-owned')!==owned)b.classList.toggle('is-owned',owned);
  b.onclick=e=>ui15QuickCapture(e,card);
 });
}
'''
marker='// Living Dex Hub v1.5.1 — contextual quick add/remove by game + selected version.'
if marker not in html:
    html=html.replace('function androidHandleBack(){',js+'\nfunction androidHandleBack(){',1)

css='''\n/* v1.5.1 contextual quick toggle */\n.quick-catch.is-owned{background:#1d5c46;color:#eafff7;border-color:#48d7a2}\n'''
if 'v1.5.1 contextual quick toggle' not in html:
    html=html.replace('</style>',css+'\n</style>',1)

required=[marker,'function ui151AddGame','function ui151RemoveGame','state.versionCaught=state.versionCaught||{}','Este registro será removido somente desta versão.','function ui15QuickCapture']
missing=[x for x in required if x not in html]
if missing: raise SystemExit('Patch v1.5.1 incompleto: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'Quick toggle v1.5.1 aplicado: {HTML} • {HTML.stat().st_size} bytes')

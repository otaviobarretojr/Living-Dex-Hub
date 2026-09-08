from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-integrity-ux" content="7.11.0"' in s:
    print('Integrity + UX 7.11.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-integrity-ux" content="7.11.0"/>\n</head>',1)
css=r'''
/* 7.11.0 — authoritative per-game Box state + focused UX polish. */
#modal .ld75-boxbtn{width:auto!important;min-width:96px!important;padding:0 12px!important;gap:6px!important;font-size:12px!important;line-height:1!important;white-space:nowrap}
#modal .ld75-boxbtn.on{min-width:82px!important}
.ld711-search-hint{margin:7px 4px 0;color:#98a2b3;font-size:10px;font-weight:700;text-align:right}
.ld711-integrity-note{display:none}
@media(max-width:430px){#modal .ld75-boxbtn{min-width:82px!important;padding:0 9px!important;font-size:10px!important}#modal .ld75-boxbtn.on{min-width:70px!important}.ld711-search-hint{display:none}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 7.11.0 — one authoritative Box state for every game.
function ld711GameId(){return String(currentGame?.id||state?.activeGameId||'')}
function ld711Truthy(v){return v===true||v?.caught||v?.registered||v?.owned}
function ld711DexSet(){
 const g=ld711GameId();
 if(!g||!Array.isArray(currentDex)||currentGame?.id!==g||!currentDex.length)return null;
 return new Set(currentDex.map(x=>Number(x?.id||x)).filter(Number.isFinite))
}
function ld711Registered(id){
 const g=ld711GameId(),n=Number(id);if(!g||!Number.isFinite(n))return false;
 const dex=ld711DexSet();if(dex&&!dex.has(n))return false;
 return ld711Truthy(state?.games?.[g+':'+n])
}
function ld711RegSet(){
 const out=new Set(),g=ld711GameId();if(!g)return out;
 const dex=ld711DexSet();
 for(const [k,v] of Object.entries(state?.games||{})){
  if(!k.startsWith(g+':')||!ld711Truthy(v))continue;
  const n=Number(k.slice(g.length+1));if(Number.isFinite(n)&&(!dex||dex.has(n)))out.add(n)
 }
 return out
}
function ld711SanitizeCurrentGame(){
 try{
  const g=ld711GameId(),dex=ld711DexSet();if(!g||!dex)return {removed:0};
  state.games=state.games||{};let removed=0;
  for(const k of Object.keys(state.games)){
   if(!k.startsWith(g+':'))continue;
   const n=Number(k.slice(g.length+1));
   if(!Number.isFinite(n)||!dex.has(n)){delete state.games[k];removed++}
  }
  state.boxIntegrityV711=state.boxIntegrityV711||{};state.boxIntegrityV711[g]={checked:true,removed};
  if(removed){try{persist?.()}catch(e){try{saveState?.()}catch(_){}}}
  return {removed}
 }catch(e){return {removed:0,error:String(e)}}
}
window.ld75Registered=ld711Registered;
window.ld71RegSet=ld711RegSet;
window.ld75CommitBox=function(id,on){
 const n=Number(id),g=ld711GameId(),dex=ld711DexSet();
 if(!g||!Number.isFinite(n))return false;
 if(dex&&!dex.has(n)){console.warn('Living Dex Hub: blocked out-of-game Box write',g,n);return false}
 state.games=state.games||{};const key=g+':'+n;
 if(on)state.games[key]=true;else delete state.games[key];
 try{persist?.()}catch(e){try{saveState?.()}catch(_){}}
 try{ld71Render?.()}catch(e){};try{ld75RefreshBoxButton?.()}catch(e){};try{renderActiveGameHome?.()}catch(e){}
 return true
};
window.home77Progress=function(g){
 const gameId=String(g?.id||state?.activeGameId||'');let total=Number(g?.count||0),done=0;
 const exact=Array.isArray(currentDex)&&currentGame?.id===gameId&&currentDex.length;
 if(exact){
  total=currentDex.length;const ids=new Set(currentDex.map(x=>Number(x?.id||x)).filter(Number.isFinite));
  for(const id of ids)if(ld711Truthy(state?.games?.[gameId+':'+id]))done++
 }else{
  const prefix=gameId+':';for(const [k,v] of Object.entries(state?.games||{}))if(k.startsWith(prefix)&&ld711Truthy(v))done++
  done=Math.min(done,total||done)
 }
 return {caught:done,total,pct:total?Math.round(done/total*100):0}
};
function ld711RefreshBoxButton(){
 const b=document.getElementById('ld75BoxBtn');if(!b||!currentPokemon)return;
 const on=ld711Registered(currentPokemon.id);b.classList.toggle('on',on);b.innerHTML=on?'✓&nbsp; Na Box':'+&nbsp; Adicionar';b.title=on?'Remover da Box':'Adicionar à Box';b.setAttribute('aria-label',b.title)
}
window.ld75RefreshBoxButton=ld711RefreshBoxButton;
window.ld75ToggleBox=function(){
 if(!currentPokemon)return;const id=Number(currentPokemon.id),on=ld711Registered(id);
 if(on&&!confirm('Remover este Pokémon da Box deste jogo?'))return;
 ld75CommitBox(id,!on)
};
function ld711EnhanceSearch(){
 const tools=document.querySelector('#ld71BoxView .ld710-tools'),input=tools?.querySelector('.ld710-search');if(!tools||!input)return;
 if(!tools.querySelector('.ld711-search-hint'))tools.insertAdjacentHTML('beforeend','<div class="ld711-search-hint">Enter abre o primeiro resultado · Esc limpa a busca</div>');
 if(input.dataset.ld711==='1')return;input.dataset.ld711='1';
 input.addEventListener('keydown',e=>{
  if(e.key==='Escape'){e.preventDefault();ld710Clear?.();return}
  if(e.key==='Enter'){
   const first=ld710Rows?.(input.value)?.[0];if(first){e.preventDefault();ld710Pick?.(first.id,first.index)}
  }
 })
}
const ld711OldRender=window.ld71Render;
if(typeof ld711OldRender==='function')window.ld71Render=function(){ld711SanitizeCurrentGame();const r=ld711OldRender.apply(this,arguments);ld711EnhanceSearch();try{ld711RefreshBoxButton()}catch(e){};return r};
const ld711OldLoad=window.ld73LoadGame;
if(typeof ld711OldLoad==='function')window.ld73LoadGame=async function(){const r=await ld711OldLoad.apply(this,arguments);ld711SanitizeCurrentGame();try{ld71Render?.()}catch(e){};try{renderActiveGameHome?.()}catch(e){};return r};
const ld711OldOpen=window.ld74OpenPokemon;
if(typeof ld711OldOpen==='function')window.ld74OpenPokemon=function(){const r=ld711OldOpen.apply(this,arguments);setTimeout(ld711RefreshBoxButton,0);return r};
window.ld711Audit=function(){
 const g=ld711GameId(),dex=ld711DexSet(),prefix=g+':';let raw=0,orphans=0;
 for(const [k,v] of Object.entries(state?.games||{}))if(k.startsWith(prefix)&&ld711Truthy(v)){raw++;const n=Number(k.slice(prefix.length));if(dex&&!dex.has(n))orphans++}
 const exact=ld711RegSet().size,total=dex?.size||Number((GAMES.find(x=>x.id===g)||{}).count||0);
 return {version:'7.11.0',game:g,total,registered:exact,rawEntries:raw,orphans,detailButton:!!document.getElementById('ld75BoxBtn'),search:!!document.querySelector('#ld71BoxView .ld710-search'),homeProgress:window.home77Progress?.(GAMES.find(x=>x.id===g))||null}
};
setTimeout(()=>{try{ld711SanitizeCurrentGame();if(document.getElementById('ld71BoxView')?.classList.contains('active'))ld71Render?.();renderActiveGameHome?.()}catch(e){}},300)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Integrity + UX 7.11.0 applied')

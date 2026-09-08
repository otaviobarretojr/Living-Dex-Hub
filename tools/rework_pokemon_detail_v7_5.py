from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-pokemon-detail" content="7.5.0"' in s:
    print('Pokemon detail 7.5.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-pokemon-detail" content="7.5.0"/>\n</head>',1)
css=r'''
/* 7.5.0 — minimal, Box-first Pokemon detail across every game. */
#modal .sheet{max-width:560px;background:#f5f7fb;padding:0 0 24px;border-radius:28px 28px 0 0;overflow-x:hidden}
#modal .sheethead{position:sticky;top:0;z-index:8;padding:18px 18px 14px;background:rgba(255,255,255,.96);backdrop-filter:blur(18px);border-bottom:1px solid #e8edf5;align-items:center}
#modal .sheethead>div:first-child{min-width:0;flex:1}
#modal #mNum{font-size:12px;font-weight:900;letter-spacing:.08em;color:#3478e5}
#modal #mName{font-size:27px!important;line-height:1.05;color:#101828;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#modal #mSource{font-size:12px;color:#7b8799;font-weight:750}
#modal .close{width:38px;height:38px;border-radius:13px;background:#eef2f7;color:#344054;border:0;font-size:22px}
#modal .poke-profile{margin:16px 16px 0;padding:18px;background:#fff;border:1px solid #e4e9f1;border-radius:24px;display:block!important;box-shadow:0 8px 28px rgba(16,24,40,.06)}
#modal .poke-hero{height:230px;border:0!important;border-radius:20px;background:linear-gradient(180deg,#f8faff,#eef3fa);display:grid;place-items:center}
#modal .poke-hero img{width:min(62%,220px);height:min(86%,210px);object-fit:contain;filter:drop-shadow(0 14px 18px rgba(32,50,80,.12))}
#modal #profileTypes{justify-content:center;margin:13px 0 0}
#modal #profileTypes .type{font-size:11px;padding:6px 11px;border-radius:999px}
#modal .profile-data,#modal #variantGrid,#modal #familyLivingPlan,#modal #family,#modal #pokemonBadges,#modal .detailgrid,#modal #exclusiveAlert,#modal #storageQuickBox,#modal #methodSummary,#modal #acquisitionGuide,#modal #availabilityGrid,#modal #encounterBox,#modal .specimen{display:none!important}
#modal .note:has(#variantGrid),#modal .note:has(#methodSummary),#modal .note:has(#acquisitionGuide),#modal .note:has(#availabilityGrid){display:none!important}
.ld75-boxbtn{width:42px;height:42px;border:1px solid #dce4ef;border-radius:14px;background:#fff;color:#667085;display:grid;place-items:center;font-size:21px;font-weight:900;box-shadow:0 3px 12px rgba(16,24,40,.06);margin-left:8px}
.ld75-boxbtn.on{background:#3478e5;border-color:#3478e5;color:#fff}
.ld75-boxbtn:active{transform:scale(.94)}
.ld75-obtain{margin:14px 16px 0;padding:18px;background:#fff;border:1px solid #e4e9f1;border-radius:22px;box-shadow:0 8px 28px rgba(16,24,40,.05)}
.ld75-obtain-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}.ld75-obtain-icon{width:34px;height:34px;border-radius:11px;background:#eef4ff;color:#3478e5;display:grid;place-items:center;font-size:17px}.ld75-obtain h3{font-size:15px;margin:0;color:#101828}.ld75-obtain-game{font-size:11px;color:#98a2b3;font-weight:750;margin-top:2px}.ld75-obtain-main{font-size:14px;font-weight:850;color:#1d2939;line-height:1.35}.ld75-obtain-detail{font-size:12px;color:#667085;line-height:1.45;margin-top:6px}.ld75-obtain-route{margin-top:10px;padding:11px 12px;border-radius:14px;background:#f7f9fc;font-size:12px;color:#475467;line-height:1.45}.ld75-obtain-loading{font-size:12px;color:#98a2b3}
@media(max-width:420px){#modal .sheethead{padding:15px 14px 12px}#modal #mName{font-size:24px!important}#modal .poke-profile,#modal .ld75-obtain{margin-left:12px;margin-right:12px}#modal .poke-hero{height:210px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Minimal Pokemon detail 7.5.0
function ld75Registered(id){return !!state?.caught?.[Number(id)]}
function ld75EnsureUI(){
 const head=document.querySelector('#modal .sheethead');if(head&&!document.getElementById('ld75BoxBtn')){
  const close=head.querySelector('.close');const b=document.createElement('button');b.id='ld75BoxBtn';b.className='ld75-boxbtn';b.type='button';b.title='Adicionar à Box';b.setAttribute('aria-label','Adicionar à Box');b.innerHTML='▣';b.onclick=ld75ToggleBox;head.insertBefore(b,close)
 }
 const profile=document.querySelector('#modal .poke-profile');if(profile&&!document.getElementById('ld75Obtain'))profile.insertAdjacentHTML('afterend','<section class="ld75-obtain" id="ld75Obtain"><div class="ld75-obtain-head"><span class="ld75-obtain-icon">⌖</span><div><h3>Onde obter</h3><div class="ld75-obtain-game" id="ld75ObtainGame"></div></div></div><div id="ld75ObtainBody" class="ld75-obtain-loading">Carregando…</div></section>')
}
function ld75RefreshBoxButton(){
 const b=document.getElementById('ld75BoxBtn');if(!b||!currentPokemon)return;const on=ld75Registered(currentPokemon.id);b.classList.toggle('on',on);b.innerHTML=on?'✓':'＋';b.title=on?'Remover da Box':'Adicionar à Box';b.setAttribute('aria-label',b.title)
}
function ld75CommitBox(id,on){
 state.caught=state.caught||{};state.games=state.games||{};
 if(on){state.caught[id]=true;if(currentGame)state.games[currentGame.id+':'+id]=true}else{delete state.caught[id];if(currentGame)delete state.games[currentGame.id+':'+id]}
 try{persist()}catch(e){try{saveState?.()}catch(_){} }
 try{renderDex?.()}catch(e){};try{ld71Render?.()}catch(e){};ld75RefreshBoxButton()
}
function ld75ToggleBox(){
 if(!currentPokemon)return;const id=Number(currentPokemon.id),on=ld75Registered(id);
 if(on&&!confirm('Remover este Pokémon da Box?'))return;
 ld75CommitBox(id,!on)
}
function ld75SafeText(v){return String(v||'').replace(/<[^>]*>/g,'').trim()}
async function ld75RenderObtain(id){
 ld75EnsureUI();const game=document.getElementById('ld75ObtainGame'),body=document.getElementById('ld75ObtainBody');if(!body)return;
 game.textContent=currentGame?.name||'Living Dex';body.className='ld75-obtain-loading';body.textContent='Verificando a melhor fonte neste jogo…';
 if(!currentGame){body.textContent='Abra o Pokémon a partir de um jogo para ver onde obtê-lo.';return}
 try{
  const a=await deriveAcquisition(currentGame.id,Number(id));
  const details=(a?.details||[]).map(ld75SafeText).filter(Boolean);
  const route=(a?.routes||[])[0];
  let routeText='';if(route){const bits=[route.location,route.method,route.minLevel?`Nv. ${route.minLevel}${route.maxLevel&&route.maxLevel!==route.minLevel?'–'+route.maxLevel:''}`:''].map(ld75SafeText).filter(Boolean);routeText=bits.join(' • ')}
  body.className='';body.innerHTML=`<div class="ld75-obtain-main">${ld75SafeText(a?.method)||'Sem obtenção direta confirmada'}</div>${details.length?`<div class="ld75-obtain-detail">${details.slice(0,2).join(' • ')}</div>`:''}${routeText?`<div class="ld75-obtain-route">${routeText}</div>`:''}`
 }catch(e){body.className='ld75-obtain-loading';body.textContent='Fonte de obtenção indisponível no momento.'}
}
const ld75OldOpen=window.openPokemon;
window.openPokemon=async function(id,name,entry){
 const r=ld75OldOpen.apply(this,arguments);ld75EnsureUI();ld75RefreshBoxButton();ld75RenderObtain(id);return r
};
const ld75OldOpenBox=window.ld74OpenPokemon;
if(typeof ld75OldOpenBox==='function')window.ld74OpenPokemon=function(id){const r=ld75OldOpenBox.apply(this,arguments);setTimeout(()=>{ld75EnsureUI();ld75RefreshBoxButton();ld75RenderObtain(id)},0);return r};
setTimeout(ld75EnsureUI,120)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Pokemon detail 7.5.0 applied')

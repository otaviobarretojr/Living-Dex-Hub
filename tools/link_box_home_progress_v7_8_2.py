from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-home-link" content="7.8.2"' in s:
    print('Box/Home link 7.8.2 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-box-home-link" content="7.8.2"/>\n</head>',1)
js=r'''
// 7.8.2 — Box is authoritative and Home mirrors it immediately.
function ld782GameId(){return currentGame?.id||state?.activeGameId||''}
function ld782Registered(id){const g=ld782GameId();return !!(g&&state?.games?.[g+':'+Number(id)])}
window.ld75Registered=ld782Registered;
window.ld75CommitBox=function(id,on){
 id=Number(id);const g=ld782GameId();if(!g||!Number.isFinite(id))return;
 state.games=state.games||{};const key=g+':'+id;
 if(on)state.games[key]=true;else delete state.games[key];
 try{persist?.()}catch(e){try{saveState?.()}catch(_){}}
 try{ld71Render?.()}catch(e){};try{ld75RefreshBoxButton?.()}catch(e){};
 try{renderActiveGameHome?.()}catch(e){}
 setTimeout(()=>{try{renderActiveGameHome?.()}catch(e){}},0)
};
window.ld75ToggleBox=function(){
 if(!currentPokemon)return;const id=Number(currentPokemon.id),on=ld782Registered(id);
 if(on&&!confirm('Remover este Pokémon da Box?'))return;
 ld75CommitBox(id,!on)
};
window.home77Progress=function(g){
 const gameId=g?.id||state?.activeGameId||'';
 let total=Number(g?.count||0);
 try{if(Array.isArray(currentDex)&&currentGame?.id===gameId&&currentDex.length)total=currentDex.length}catch(e){}
 let done=0;
 try{const prefix=gameId+':';done=Object.entries(state?.games||{}).filter(([k,v])=>k.startsWith(prefix)&&(v===true||v?.caught||v?.registered||v?.owned)).length}catch(e){}
 done=Math.min(done,total||done);return {caught:done,total,pct:total?Math.round(done/total*100):0}
};
const ld782OldLoad=window.ld73LoadGame;
if(typeof ld782OldLoad==='function')window.ld73LoadGame=async function(){const r=await ld782OldLoad.apply(this,arguments);try{renderActiveGameHome?.()}catch(e){};return r};
setTimeout(()=>{try{renderActiveGameHome?.()}catch(e){}},180)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box/Home link 7.8.2 applied')
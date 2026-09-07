from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-all-games" content="7.3"' not in s:
    s=s.replace('</head>','<meta name="living-dex-box-all-games" content="7.3"/>\n</head>',1)
css=r'''
/* Box 7.3 — same Box experience for every supported game. */
.ld73-gamebadge{display:inline-flex;align-items:center;gap:6px;margin-top:5px;padding:5px 8px;border-radius:999px;background:#eef3fb;color:#49617f;font-size:10px;font-weight:850}
.ld72-gameitem .ld73-meta{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:5px}.ld73-pill{font-size:9px;font-weight:850;padding:4px 7px;border-radius:999px;background:#eef3fb;color:#5d6d86}.ld72-gameitem.active .ld73-pill{background:#dceaff;color:#2668c8}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box all-games parity 7.3
const LD73_SUPPORTED=['sv','za','swsh','bdsp','letsgo','arceus'];
const LD73_FALLBACK_GAMES=[
 {id:'sv',name:'Scarlet / Violet'},
 {id:'za',name:'Legends Z-A'},
 {id:'swsh',name:'Sword / Shield'},
 {id:'bdsp',name:'Brilliant Diamond / Shining Pearl'},
 {id:'letsgo',name:"Let\'s Go Pikachu / Eevee"},
 {id:'arceus',name:'Legends Arceus'}
];
const ld73BoxByGame={};
function ld73SupportedGames(){
 let source=[];
 try{if(typeof GAMES!=='undefined'&&Array.isArray(GAMES))source=GAMES}catch(e){}
 if(!source.length&&Array.isArray(window.GAMES))source=window.GAMES;
 const byId=new Map(source.map(g=>[g.id,g]));
 return LD73_SUPPORTED.map(id=>byId.get(id)||LD73_FALLBACK_GAMES.find(g=>g.id===id)).filter(Boolean)
}
function ld73RememberBox(){const id=state?.activeGameId;if(id)ld73BoxByGame[id]=ld71BoxIndex||0}
function ld73RestoreBox(id){ld71BoxIndex=Math.max(0,Number(ld73BoxByGame[id]||0))}
function ld73CurrentMeta(){const dex=ld71Dex(),total=dex.length||0;return {total,boxes:Math.max(1,Math.ceil(total/30))}}
async function ld73LoadGame(id){
 if(!LD73_SUPPORTED.includes(id))return false;
 ld73RememberBox();
 try{state.activeGameId=id;saveState?.();await openGame(id)}catch(e){return false}
 ld73RestoreBox(id);
 const max=Math.max(0,ld71BoxCount()-1);if(ld71BoxIndex>max)ld71BoxIndex=max;
 return true
}
window.ld72OpenGames=function(){
 ld72EnsureSheet();const root=document.getElementById('ld72GamesList');if(!root)return;
 const active=state?.activeGameId;
 const games=ld73SupportedGames();
 root.innerHTML=games.map(g=>`<button class="ld72-gameitem ${g.id===active?'active':''}" onclick="ld73SelectGame('${g.id}')"><img src="${ld72Cover(g)}"><span><b>${g.name}</b><small>Boxes organizadas de 30 em 30</small><span class="ld73-meta"><span class="ld73-pill">Living Dex</span><span class="ld73-pill">Box por jogo</span></span></span><span class="ld72-check">${g.id===active?'✓':'›'}</span></button>`).join('');
 document.getElementById('ld72GameSheet')?.classList.add('active')
}
async function ld73SelectGame(id){
 const ok=await ld73LoadGame(id);if(!ok)return;
 ld72CloseGames();ld71Render();ld72Focus()
}
window.ld72SelectGame=ld73SelectGame;
const ld73OldOpen=window.ld71Open;window.ld71Open=async function(){
 const id=state?.activeGameId||ld73SupportedGames()[0]?.id;
 if(id && !(Array.isArray(currentDex)&&currentDex.length&&currentGame?.id===id))await ld73LoadGame(id);
 const r=await ld73OldOpen.apply(this,arguments);ld73RestoreBox(state?.activeGameId);ld71Render();return r
}
const ld73OldSetBox=window.ld71SetBox;window.ld71SetBox=function(i){const r=ld73OldSetBox.call(this,i);ld73RememberBox();return r}
const ld73OldRender=window.ld71Render;window.ld71Render=function(){
 const r=ld73OldRender.apply(this,arguments);const game=ld71Game(),meta=ld73CurrentMeta();
 const p=document.querySelector('#ld71BoxView .ld71-game p');if(p)p.innerHTML=`Living Dex <span class="ld73-gamebadge">${meta.total} Pokémon · ${meta.boxes} Boxes</span>`;
 return r
}
function ld73AuditGames(){const ids=ld73SupportedGames().map(g=>g.id);return LD73_SUPPORTED.every(id=>ids.includes(id))&&ids.length===LD73_SUPPORTED.length}
window.ld73AuditGames=ld73AuditGames;
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box all-games 7.3 applied')
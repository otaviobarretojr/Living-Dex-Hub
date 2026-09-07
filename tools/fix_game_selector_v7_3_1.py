from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-game-selector-fix" content="7.3.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-box-game-selector-fix" content="7.3.1"/>\n</head>',1)
js=r'''
// Box game selector runtime fix 7.3.1
const LD731_FALLBACK_GAMES=[
 {id:'sv',name:'Scarlet / Violet'},
 {id:'za',name:'Legends Z-A'},
 {id:'swsh',name:'Sword / Shield'},
 {id:'bdsp',name:'Brilliant Diamond / Shining Pearl'},
 {id:'letsgo',name:"Let's Go Pikachu / Eevee"},
 {id:'arceus',name:'Legends Arceus'}
];
window.ld73SupportedGames=function(){
 let source=[];
 try{if(typeof GAMES!=='undefined'&&Array.isArray(GAMES))source=GAMES}catch(e){}
 if(!source.length&&Array.isArray(window.GAMES))source=window.GAMES;
 const byId=new Map(source.map(g=>[g.id,g]));
 return LD73_SUPPORTED.map(id=>byId.get(id)||LD731_FALLBACK_GAMES.find(g=>g.id===id)).filter(Boolean)
};
window.ld72OpenGames=function(){
 ld72EnsureSheet();const root=document.getElementById('ld72GamesList');if(!root)return;
 const active=state?.activeGameId;
 const games=ld73SupportedGames();
 root.innerHTML=games.map(g=>`<button class="ld72-gameitem ${g.id===active?'active':''}" onclick="ld73SelectGame('${g.id}')"><img src="${ld72Cover(g)}"><span><b>${g.name}</b><small>Boxes organizadas de 30 em 30</small><span class="ld73-meta"><span class="ld73-pill">Living Dex</span><span class="ld73-pill">Box por jogo</span></span></span><span class="ld72-check">${g.id===active?'✓':'›'}</span></button>`).join('');
 if(!root.children.length)root.innerHTML='<div style="padding:18px;text-align:center;color:#6d7890;font-weight:800">Nenhum jogo disponível.</div>';
 document.getElementById('ld72GameSheet')?.classList.add('active')
};
function ld731AuditSelector(){const ids=ld73SupportedGames().map(g=>g.id);return LD73_SUPPORTED.length===6&&LD73_SUPPORTED.every(id=>ids.includes(id))&&ids.length===6}
window.ld731AuditSelector=ld731AuditSelector;
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box game selector 7.3.1 fixed')
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-game-selector-feedback" content="7.3.1"' not in s:s=s.replace('</head>','<meta name="living-dex-game-selector-feedback" content="7.3.1"/>\n</head>',1)
css=r'''
/* 7.3.1 — immediate visual feedback when switching games. */
.ld72-gameitem.ld731-pending{border-color:#3478e5;background:#eaf2ff;box-shadow:inset 0 0 0 1px #3478e5}
.ld72-gameitem.ld731-pending .ld72-check{color:#3478e5}
.ld72-gameitem.ld731-disabled{opacity:.52;pointer-events:none}
.ld731-status{display:block;margin-top:5px;color:#3478e5;font-size:10px;font-weight:900}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Game selector visual feedback 7.3.1
function ld731MarkSelection(id){
 const items=[...document.querySelectorAll('#ld72GamesList .ld72-gameitem')];
 items.forEach(btn=>{
   const target=String(btn.getAttribute('onclick')||'').includes(`'${id}'`);
   btn.classList.toggle('ld731-pending',target);
   btn.classList.toggle('ld731-disabled',!target);
   const check=btn.querySelector('.ld72-check');if(check)check.textContent=target?'✓':'›';
   const old=btn.querySelector('.ld731-status');if(old)old.remove();
   if(target){const info=btn.querySelector('span:nth-child(2)');if(info)info.insertAdjacentHTML('beforeend','<span class="ld731-status">Carregando boxes…</span>')}
 })
}
function ld731RestoreSelector(){document.querySelectorAll('#ld72GamesList .ld72-gameitem').forEach(btn=>{btn.classList.remove('ld731-pending','ld731-disabled');btn.querySelector('.ld731-status')?.remove()})}
window.ld73SelectGame=async function(id){
 ld731MarkSelection(id);
 const ok=await ld73LoadGame(id);
 if(!ok){ld731RestoreSelector();return}
 ld71BoxIndex=0;
 ld71Render();ld72Focus();
 // Keep the selected state visible briefly so the tap has an obvious response.
 setTimeout(()=>{ld72CloseGames();ld731RestoreSelector()},180)
}
window.ld72SelectGame=window.ld73SelectGame;
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Game selector feedback 7.3.1 applied')
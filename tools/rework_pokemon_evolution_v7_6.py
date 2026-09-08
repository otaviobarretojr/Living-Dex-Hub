from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-pokemon-evolution" content="7.6.0"' in s:
    print('Pokemon evolution detail 7.6.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-pokemon-evolution" content="7.6.0"/>\n</head>',1)
css=r'''
/* 7.6.0 — detail focused on evolution; no acquisition blocks. */
#modal .ld75-obtain,#modal #acquisitionBox,#modal #exclusiveAlert,#modal #methodSummary,#modal #acquisitionGuide,#modal #availabilityGrid,#modal #encounterBox,#modal #storageQuickBox{display:none!important}
#modal .note:has(#methodSummary),#modal .note:has(#acquisitionGuide),#modal .note:has(#availabilityGrid),#modal .note:has(#encounterBox){display:none!important}
#modal #profileTypes{display:flex!important;justify-content:center;gap:7px;margin:13px 0 0!important;min-height:0}
#modal #profileTypes .type,#modal #profileTypes .badge{background:#eef4ff!important;color:#3478e5!important;border:1px solid #dbe8ff!important;box-shadow:none!important;font-size:11px!important;font-weight:850!important;padding:6px 11px!important;border-radius:999px!important;min-width:0!important;width:auto!important;height:auto!important}
#modal .poke-profile{margin-bottom:0}
.ld76-evo{margin:14px 16px 0;padding:18px;background:#fff;border:1px solid #e4e9f1;border-radius:22px;box-shadow:0 8px 28px rgba(16,24,40,.05)}
.ld76-evo-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}.ld76-evo-icon{width:34px;height:34px;border-radius:11px;background:#eef4ff;color:#3478e5;display:grid;place-items:center;font-size:17px;font-weight:900}.ld76-evo h3{font-size:16px;margin:0;color:#101828}.ld76-evo-sub{font-size:11px;color:#98a2b3;font-weight:700;margin-top:2px}
.ld76-path{display:flex;align-items:stretch;gap:7px;overflow-x:auto;padding:2px 1px 8px;scrollbar-width:none}.ld76-path::-webkit-scrollbar{display:none}.ld76-path+.ld76-path{margin-top:12px;padding-top:12px;border-top:1px solid #edf1f6}
.ld76-mon{min-width:92px;max-width:92px;padding:10px 7px;border:1px solid #e4e9f1;border-radius:16px;background:#f8faff;text-align:center}.ld76-mon.current{border-color:#3478e5;background:#eef4ff}.ld76-mon img{width:58px;height:58px;object-fit:contain}.ld76-mon b{display:block;margin-top:4px;font-size:11px;color:#1d2939;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.ld76-mon span{display:block;margin-top:2px;font-size:9px;color:#98a2b3}
.ld76-step{min-width:112px;max-width:138px;align-self:center;padding:8px 7px;text-align:center;color:#475467;font-size:10px;line-height:1.35;font-weight:750}.ld76-arrow{display:block;color:#3478e5;font-size:18px;line-height:1;margin-bottom:4px}.ld76-loading,.ld76-empty{font-size:12px;color:#98a2b3;line-height:1.5}
@media(max-width:420px){.ld76-evo{margin-left:12px;margin-right:12px;padding:15px}.ld76-mon{min-width:82px;max-width:82px}.ld76-mon img{width:52px;height:52px}.ld76-step{min-width:96px;max-width:120px;font-size:9.5px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Evolution-first Pokemon detail 7.6.0
function ld76EnsureEvolutionUI(){
 const profile=document.querySelector('#modal .poke-profile');if(profile&&!document.getElementById('ld76Evolution')){
  profile.insertAdjacentHTML('afterend','<section class="ld76-evo" id="ld76Evolution"><div class="ld76-evo-head"><span class="ld76-evo-icon">↗</span><div><h3>Linha evolutiva</h3><div class="ld76-evo-sub">Nível ou método de evolução</div></div></div><div id="ld76EvolutionBody" class="ld76-loading">Carregando linha evolutiva…</div></section>')
 }
}
function ld76EvolutionMethod(details){
 if(!details||!details.length)return 'Evolução especial';
 const options=details.map(d=>{
  try{const a=typeof evoDetailText==='function'?evoDetailText(d):[];if(a&&a.length)return a.join(' • ')}catch(e){}
  const out=[];if(d.min_level)out.push('Nível '+d.min_level);if(d.item)out.push('Usar '+title(d.item.name));if(d.trigger?.name==='trade')out.push('Troca');if(d.min_happiness)out.push('Amizade ≥ '+d.min_happiness);if(d.time_of_day)out.push(d.time_of_day==='day'?'Durante o dia':d.time_of_day==='night'?'Durante a noite':title(d.time_of_day));return out.join(' • ')||'Evolução especial'
 }).filter(Boolean);
 return options.join(' / ')
}
function ld76Paths(node,path=[],out=[]){
 const id=typeof speciesId==='function'?speciesId(node.species.url):Number(String(node.species.url).split('/').filter(Boolean).pop());
 const next=[...path,{id,name:node.species.name,details:node.evolution_details||[]}];
 if(!node.evolves_to||!node.evolves_to.length)out.push(next);else node.evolves_to.forEach(c=>ld76Paths(c,next,out));return out
}
function ld76MonCard(x,current){
 const img=typeof pokemonImageHTML==='function'?pokemonImageHTML(x.id):`<img src="assets/pokemon/${x.id}.png" alt="">`;
 return `<div class="ld76-mon ${Number(x.id)===Number(current)?'current':''}">${img}<b>${typeof title==='function'?title(x.name):x.name}</b><span>#${String(x.id).padStart(4,'0')}</span></div>`
}
async function ld76RenderEvolution(id){
 ld76EnsureEvolutionUI();const body=document.getElementById('ld76EvolutionBody');if(!body)return;body.className='ld76-loading';body.textContent='Carregando linha evolutiva…';
 try{
  const sp=await fetch(`${API}/pokemon-species/${Number(id)}/`,{cache:'force-cache'}).then(r=>{if(!r.ok)throw 0;return r.json()});
  if(!sp.evolution_chain?.url)throw 0;const ch=await fetch(sp.evolution_chain.url,{cache:'force-cache'}).then(r=>{if(!r.ok)throw 0;return r.json()});
  const paths=ld76Paths(ch.chain);if(!paths.length)throw 0;
  body.className='';body.innerHTML=paths.map(path=>`<div class="ld76-path">${path.map((x,i)=>`${i?`<div class="ld76-step"><span class="ld76-arrow">→</span>${ld76EvolutionMethod(x.details)}</div>`:''}${ld76MonCard(x,id)}`).join('')}</div>`).join('')
 }catch(e){body.className='ld76-empty';body.textContent='Linha evolutiva indisponível no momento.'}
}
const ld76OldOpen=window.openPokemon;
window.openPokemon=function(id,name,entry){const r=ld76OldOpen.apply(this,arguments);ld76EnsureEvolutionUI();ld76RenderEvolution(id);return r};
const ld76OldBoxOpen=window.ld74OpenPokemon;
if(typeof ld76OldBoxOpen==='function')window.ld74OpenPokemon=function(id){const r=ld76OldBoxOpen.apply(this,arguments);setTimeout(()=>{ld76EnsureEvolutionUI();ld76RenderEvolution(id)},0);return r};
setTimeout(ld76EnsureEvolutionUI,150)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Pokemon evolution detail 7.6.0 applied')

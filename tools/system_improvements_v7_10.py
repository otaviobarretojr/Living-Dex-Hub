from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-system-foundation" content="7.10.0"' in s:
    print('System foundation 7.10.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-system-foundation" content="7.10.0"/>\n</head>',1)
css=r'''
/* 7.10.0 — first system improvement pass: safer state + useful Box search. */
.ld710-tools{max-width:980px;margin:0 auto 14px;position:relative}
.ld710-searchwrap{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #e1e7f0;border-radius:18px;padding:0 13px;min-height:52px;box-shadow:0 5px 18px rgba(33,48,78,.05)}
.ld710-searchwrap svg{width:19px;height:19px;color:#718096;flex:0 0 19px}
.ld710-search{border:0;outline:0;background:transparent;width:100%;font:700 14px/1.2 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#172440;padding:14px 0}
.ld710-search::placeholder{color:#98a2b3;font-weight:650}
.ld710-clear{display:none;border:0;background:#eef2f7;color:#667085;border-radius:10px;width:31px;height:31px;font-size:18px;line-height:1}
.ld710-tools.has-query .ld710-clear{display:block}
.ld710-results{display:none;position:absolute;left:0;right:0;top:58px;z-index:1080;background:#fff;border:1px solid #e2e8f0;border-radius:18px;padding:7px;box-shadow:0 18px 45px rgba(15,23,42,.16);max-height:330px;overflow:auto}
.ld710-tools.has-query .ld710-results{display:block}
.ld710-result{width:100%;border:0;background:transparent;border-radius:13px;padding:8px 10px;display:grid;grid-template-columns:44px 1fr auto;gap:10px;align-items:center;text-align:left;color:#172440}
.ld710-result:active,.ld710-result:hover{background:#f3f6fb}
.ld710-result img{width:42px;height:42px;object-fit:contain}
.ld710-result b{display:block;font-size:13px}.ld710-result small{display:block;color:#7d879a;font-size:10px;margin-top:2px}
.ld710-status{font-size:9px;font-weight:900;padding:5px 7px;border-radius:999px;background:#f0f2f5;color:#8a94a6}.ld710-status.on{background:#e8f7ee;color:#21854d}
.ld710-empty{padding:18px;text-align:center;color:#7d879a;font-size:12px;font-weight:700}
#ld71BoxView .ld71-tabs{margin-bottom:10px!important}
@media(max-width:520px){.ld710-result{grid-template-columns:40px 1fr auto}.ld710-result img{width:38px;height:38px}.ld710-status{font-size:8px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 7.10.0 — stabilize Box ownership and add fast lookup inside the current game's Dex.
function ld710Save(){try{persist?.()}catch(e){try{saveState?.()}catch(_){}}}
function ld710Truthy(v){return v===true||v?.caught||v?.registered||v?.owned}
function ld710MigrateOnce(){
 try{
  const g=currentGame, dex=Array.isArray(currentDex)?currentDex:[];if(!g?.id||!dex.length)return false;
  state.games=state.games||{};state.boxMigrationV710=state.boxMigrationV710||{};
  if(state.boxMigrationV710[g.id])return false;
  const prefix=g.id+':';const hasSpecific=Object.keys(state.games).some(k=>k.startsWith(prefix));
  let moved=0;
  if(!hasSpecific){
   const legacy=new Set();const add=o=>{if(!o)return;Object.entries(o).forEach(([k,v])=>{if(ld710Truthy(v))legacy.add(Number(k))})};
   add(state.caught);add(state.registered);add(state.owned);add(state.dex);
   for(const row of dex){const id=Number(row.id||row);if(legacy.has(id)){state.games[prefix+id]=true;moved++}}
  }
  state.boxMigrationV710[g.id]=true;ld710Save();
  return moved>0
 }catch(e){return false}
}
try{ld78MigrateLegacyCurrentGame=ld710MigrateOnce}catch(e){}window.ld78MigrateLegacyCurrentGame=ld710MigrateOnce;
let ld710Query='';
function ld710Norm(v){return String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim()}
function ld710Rows(q){
 const query=ld710Norm(q),dex=ld71Dex();if(!query)return [];
 const numeric=query.replace(/^#/,'');
 return dex.map((row,index)=>{const id=Number(row?.id||row),name=String(row?.name||ld71Name(id)),entry=Number(row?.entry||row?.entry_number||index+1);return {row,index,id,name,entry}})
  .filter(x=>ld710Norm(x.name).includes(query)||String(x.id)===numeric||String(x.entry)===numeric||String(x.index+1)===numeric)
  .slice(0,10)
}
function ld710ResultHtml(){
 const rows=ld710Rows(ld710Query),regs=ld71RegSet();
 if(!rows.length)return '<div class="ld710-empty">Nenhum Pokémon encontrado neste jogo.</div>';
 return rows.map(x=>`<button type="button" class="ld710-result" onclick="ld710Pick(${x.id},${x.index})"><img src="assets/pokemon/${x.id}.png" alt=""><span><b>${x.name}</b><small>#${String(x.entry).padStart(3,'0')} · Box ${Math.floor(x.index/30)+1}</small></span><span class="ld710-status ${regs.has(x.id)?'on':''}">${regs.has(x.id)?'Na Box':'Faltando'}</span></button>`).join('')
}
function ld710Input(v){ld710Query=v||'';const tools=document.querySelector('.ld710-tools');if(!tools)return;tools.classList.toggle('has-query',!!ld710Query.trim());const out=tools.querySelector('.ld710-results');if(out)out.innerHTML=ld710ResultHtml()}
function ld710Clear(){ld710Query='';const input=document.querySelector('.ld710-search');if(input)input.value='';ld710Input('');input?.focus?.()}
function ld710Pick(id,index){ld710Query='';ld71BoxIndex=Math.max(0,Math.floor(Number(index)/30));ld71Render();setTimeout(()=>{try{ld74OpenPokemon(Number(id))}catch(e){}},40)}
function ld710Polish(){
 const root=document.getElementById('ld71BoxView');if(!root)return;
 const gameBtn=root.querySelector('.ld72-games span');if(gameBtn)gameBtn.textContent='Trocar jogo';
 root.querySelectorAll('.ld74-register').forEach(reg=>{const slot=reg.closest('.ld71-slot'),on=slot?.classList.contains('registered');reg.title=on?'Remover da Box':'Adicionar à Box';reg.setAttribute('aria-label',reg.title)});
 root.querySelectorAll('.ld71-stat span').forEach(el=>{if((el.textContent||'').trim()==='Não registrado')el.textContent='Faltando'});
 const p=root.querySelector('.ld71-game p');if(p&&!/Box oficial/.test(p.textContent||'')){const t=ld71Dex().length||0,b=Math.max(1,Math.ceil(t/30));p.innerHTML=`Box oficial <span class="ld73-gamebadge">${t} Pokémon · ${b} Boxes</span>`}
}
function ld710EnsureTools(){
 const root=document.getElementById('ld71BoxView');if(!root)return;
 let tools=root.querySelector('.ld710-tools');
 if(!tools){
  tools=document.createElement('section');tools.className='ld710-tools';
  tools.innerHTML=`<div class="ld710-searchwrap"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="6.5" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><input class="ld710-search" type="search" autocomplete="off" spellcheck="false" placeholder="Buscar Pokémon por nome ou número" aria-label="Buscar Pokémon" oninput="ld710Input(this.value)"><button type="button" class="ld710-clear" aria-label="Limpar busca" onclick="ld710Clear()">×</button></div><div class="ld710-results"></div>`;
  const anchor=root.querySelector('.ld71-tabs');if(anchor)anchor.insertAdjacentElement('afterend',tools);else root.querySelector('.ld71-main')?.insertAdjacentElement('beforebegin',tools)
 }
 const input=tools.querySelector('.ld710-search');if(input&&input.value!==ld710Query)input.value=ld710Query;
 tools.classList.toggle('has-query',!!ld710Query.trim());const out=tools.querySelector('.ld710-results');if(out&&ld710Query.trim())out.innerHTML=ld710ResultHtml();
 ld710Polish()
}
window.ld710Audit=function(){
 const root=document.getElementById('ld71BoxView');
 return {game:currentGame?.id||state?.activeGameId||'',dex:Array.isArray(currentDex)?currentDex.length:0,registered:ld71RegSet?.().size||0,search:!!root?.querySelector('.ld710-search'),migrationMarked:!!state?.boxMigrationV710?.[currentGame?.id||state?.activeGameId]}
};
const ld710OldRender=window.ld71Render;if(typeof ld710OldRender==='function')window.ld71Render=function(){const r=ld710OldRender.apply(this,arguments);ld710EnsureTools();return r};
const ld710OldGames=window.ld72OpenGames;if(typeof ld710OldGames==='function')window.ld72OpenGames=function(){const r=ld710OldGames.apply(this,arguments);document.querySelectorAll('#ld72GamesList small').forEach(x=>x.textContent='Abrir Box deste jogo');return r};
const ld710OldLoad=window.ld73LoadGame;if(typeof ld710OldLoad==='function')window.ld73LoadGame=async function(){const r=await ld710OldLoad.apply(this,arguments);ld710Query='';ld710MigrateOnce();try{ld71Render()}catch(e){};return r};
setTimeout(()=>{try{ld710MigrateOnce();if(document.getElementById('ld71BoxView')?.classList.contains('active'))ld71Render()}catch(e){}},260)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('System foundation 7.10.0 applied')

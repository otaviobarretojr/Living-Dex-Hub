from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')
html=html.replace('<meta name="living-dex-ui" content="1.4"/>','<meta name="living-dex-ui" content="1.5"/>',1)
html=html.replace('Core 1.0 • UI 1.4 • Offline','Core 1.0 • UI 1.5 • Offline',1)
html=html.replace(" if(viewId==='home')ui12HomeShortcuts(v);","",1)
html=html.replace("home:['Visão geral','Seu progresso, próximos passos e visão rápida da coleção.']","home:['Seu progresso','Visão geral da sua coleção, sem repetir as ferramentas das outras abas.']",1)
css=r'''
/* Living Dex Hub UI 1.5 — progress-first Home + quick capture + clear backup */
#home .quick-strip{display:none!important}#home .scope-note{display:none!important}
.pk{position:relative}.quick-catch{position:absolute;right:7px;top:7px;z-index:4;width:34px;height:34px;min-height:34px!important;border-radius:11px;border:1px solid #38516f;background:#0b1728e8;color:#b9c9dc;display:grid;place-items:center;font-size:16px;font-weight:900;box-shadow:0 5px 16px #0007;cursor:pointer;backdrop-filter:blur(8px)}.pk.caught .quick-catch{background:#1d5c46;color:#eafff7;border-color:#48d7a2}.quick-catch:active{transform:scale(.92)}
.backup-guide{margin:10px 0 14px;padding:14px;border:1px solid #29425f;border-radius:16px;background:#0b1728}.backup-guide h3{margin:0 0 5px;font-size:14px}.backup-guide p{margin:0;color:#91a5bf;font-size:10px;line-height:1.55}.backup-guide .row{margin-top:11px;display:flex;gap:8px;flex-wrap:wrap}.backup-guide .btn{min-height:44px}.backup-status{margin-top:8px;font-size:9px;color:#7f94ae}
@media(max-width:700px){#home .screen-intro{margin-bottom:8px}.quick-catch{right:6px;top:6px;width:32px;height:32px}.backup-guide{padding:12px}.backup-guide .row{display:grid;grid-template-columns:1fr}.backup-guide .btn{width:100%}}
'''
if 'Living Dex Hub UI 1.5' not in html: html=html.replace('</style>',css+'\n</style>',1)
js=r'''
// Living Dex Hub UI 1.5 — usability layer. Existing collection functions remain the source of truth.
function ui15SpeciesId(card){
 if(!card)return 0;
 const img=card.querySelector('img[data-poke-id]'); if(img)return Number(img.dataset.pokeId||0);
 const txt=(card.textContent||'').match(/#\s*(\d{1,4})/); return txt?Number(txt[1]):0;
}
function ui15QuickCapture(ev,card){
 ev.preventDefault();ev.stopPropagation();
 const id=ui15SpeciesId(card); if(!id)return;
 if(card.classList.contains('caught')){ if(typeof openPokemon==='function')openPokemon(id); else card.click(); return; }
 card.click();
 setTimeout(()=>{
  const modal=document.getElementById('modal'); if(!modal)return;
  const candidates=[...modal.querySelectorAll('button')];
  const b=candidates.find(x=>/registrar|captur|adicionar/i.test((x.textContent||'').trim()));
  if(b)b.click();
 },80);
}
function ui15DecorateDex(){
 document.querySelectorAll('.pk').forEach(card=>{
  if(card.querySelector('.quick-catch'))return;
  const b=document.createElement('button');b.type='button';b.className='quick-catch';b.setAttribute('aria-label','Registro rápido');b.title=card.classList.contains('caught')?'Já registrado — abrir ficha':'Registrar rapidamente';b.textContent=card.classList.contains('caught')?'✓':'+';b.onclick=e=>ui15QuickCapture(e,card);card.appendChild(b);
 });
}
function ui15BackupGuide(){
 const v=document.getElementById('settings');if(!v||v.querySelector('.backup-guide'))return;
 const box=document.createElement('div');box.className='backup-guide';
 box.innerHTML='<h3>Seus dados</h3><p>Crie um arquivo de segurança da sua coleção e guarde-o fora do aplicativo. Para recuperar os dados, use Restaurar backup e escolha o arquivo salvo.</p><div class="row"><button class="btn primary" type="button" data-backup-action="create">Criar backup</button><button class="btn" type="button" data-backup-action="restore">Restaurar backup</button></div><div class="backup-status">O backup protege sua coleção caso o app seja reinstalado ou os dados do aparelho sejam apagados.</div>';
 const intro=v.querySelector('.screen-intro');(intro||v).insertAdjacentElement(intro?'afterend':'afterbegin',box);
 box.querySelector('[data-backup-action=create]').onclick=()=>ui15ForwardBackup(/backup|exportar|baixar|download/i);
 box.querySelector('[data-backup-action=restore]').onclick=()=>ui15ForwardBackup(/restaurar|importar|restore/i);
}
function ui15ForwardBackup(rx){
 const settings=document.getElementById('settings');const buttons=[...settings.querySelectorAll('button,input[type=button],label')].filter(x=>!x.closest('.backup-guide'));
 const target=buttons.find(x=>rx.test((x.textContent||x.value||'').trim()));
 if(target){target.click();return} alert('A ação de backup original não foi localizada. Abra as opções de dados logo abaixo para concluir.');
}
function ui15Ensure(){ui15DecorateDex();ui15BackupGuide()}
// Deterministic one-shot setup. Later renders are decorated by the v1.5.1 render hooks.
setTimeout(ui15Ensure,0);
'''
if 'Living Dex Hub UI 1.5 — usability layer' not in html: html=html.replace('function androidHandleBack(){',js+'\nfunction androidHandleBack(){',1)
required=['living-dex-ui" content="1.5','Living Dex Hub UI 1.5','function ui15QuickCapture','quick-catch','Criar backup','Restaurar backup','Core 1.0 • UI 1.5 • Offline','setTimeout(ui15Ensure,0)']
missing=[x for x in required if x not in html]
if missing: raise SystemExit('UI 1.5 incompleta: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'UI 1.5 aplicada: {HTML} • {HTML.stat().st_size} bytes')

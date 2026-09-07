from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-library" content="7.4.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-box-library" content="7.4.1"/>\n</head>',1)
css=r'''
/* 7.4.1 — Box becomes the official Pokémon library. */
.ld71-slot{cursor:pointer}
.ld74-register{position:absolute;top:7px;right:7px;width:24px;height:24px;border:1px solid #d9e1ec;border-radius:8px;background:#fff;color:#7c8799;display:grid;place-items:center;font-size:13px;font-weight:950;z-index:2;box-shadow:0 2px 7px rgba(30,48,80,.06)}
.ld71-slot.registered .ld74-register{background:#3478e5;border-color:#3478e5;color:#fff}
.ld74-register:active{transform:scale(.94)}
body.ld74-box-detail #modal,body.ld74-box-detail .modal,body.ld74-box-detail [role="dialog"]{z-index:1400!important}
body.ld74-box-detail #modal .sheet{max-height:94vh}
@media(max-width:390px){.ld74-register{width:21px;height:21px;top:5px;right:5px;border-radius:7px;font-size:11px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box official library 7.4.1 — route taps through the already-working Dex detail engine.
function ld74EntryFor(id){const row=ld71Dex().find(x=>Number(x.id||x)===Number(id));return Number(row?.entry||row?.entry_number||row?.id||id)}
function ld74NameFor(id){const row=ld71Dex().find(x=>Number(x.id||x)===Number(id));return row?.name||ld71Name(id)}
function ld74DexCard(id){
 const all=[...document.querySelectorAll('#dexGrid [data-id],#dexGrid .pk,#dexCard [data-id]')];
 return all.find(x=>Number(x.dataset?.id||x.getAttribute?.('data-id'))===Number(id))||null
}
function ld74OpenPokemon(id){
 id=Number(id);document.body.classList.add('ld74-box-detail');
 const card=ld74DexCard(id);
 if(card){card.click();return}
 const entry=ld74EntryFor(id),name=ld74NameFor(id);
 if(typeof openPokemon==='function'){openPokemon(id,String(name),entry);return}
 if(typeof showPokemon==='function'){showPokemon(id);return}
 if(typeof openPokemonDetail==='function'){openPokemonDetail(id);return}
 console.warn('Box detail engine unavailable for',id)
}
function ld74ToggleRegister(ev,id){ev?.stopPropagation?.();ev?.preventDefault?.();ld71Toggle(Number(id));setTimeout(()=>{try{ld71Render()}catch(e){}},100)}
const ld74OldClose=window.closeModal;if(typeof ld74OldClose==='function')window.closeModal=function(){document.body.classList.remove('ld74-box-detail');return ld74OldClose.apply(this,arguments)};
const ld74OldRender=window.ld71Render;
window.ld71Render=function(){
 const r=ld74OldRender.apply(this,arguments);const root=document.getElementById('ld71BoxView');if(!root)return r;
 const dex=ld71Dex(),start=ld71BoxIndex*30;
 root.querySelectorAll('.ld71-slot').forEach((slot,i)=>{
   const row=dex[start+i];if(!row)return;const id=Number(row.id||row),registered=slot.classList.contains('registered');
   slot.setAttribute('onclick',`ld74OpenPokemon(${id})`);slot.setAttribute('aria-label',`Abrir informações de ${ld74NameFor(id)}`);
   let reg=slot.querySelector('.ld74-register');if(!reg){reg=document.createElement('span');reg.className='ld74-register';slot.appendChild(reg)}
   reg.textContent=registered?'✓':'+';reg.title=registered?'Remover da Living Dex':'Registrar na Living Dex';reg.setAttribute('role','button');reg.setAttribute('aria-label',reg.title);reg.setAttribute('onclick',`ld74ToggleRegister(event,${id})`)
 });return r
};
setTimeout(()=>{try{if(document.getElementById('ld71BoxView')?.classList.contains('active'))ld71Render()}catch(e){}},200)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box official library 7.4.1 applied')
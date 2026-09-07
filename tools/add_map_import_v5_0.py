from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')

if 'living-dex-map-import\" content=\"5.0\"' not in s:
    s=s.replace('</head>','<meta name="living-dex-map-import" content="5.0"/>\n</head>',1)

css=r'''
/* Map Import 5.0 — persistent custom background via IndexedDB. */
.ref50-import{position:absolute;inset:0;z-index:80;display:none;align-items:flex-end;justify-content:center;padding:12px;background:rgba(10,20,36,.48);backdrop-filter:blur(8px)}
.ref50-import.open{display:flex}.ref50-sheet{width:min(560px,100%);max-height:min(82vh,720px);overflow:auto;background:#fff;border-radius:24px;padding:18px;box-shadow:0 22px 60px rgba(0,0,0,.28);color:#17213c}.ref50-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}.ref50-head b{font-size:18px}.ref50-x{width:36px;height:36px;border:0;border-radius:12px;background:#f0f2f5;font-size:20px;color:#667085}.ref50-drop{display:block;border:2px dashed #c8d2df;border-radius:18px;padding:22px 16px;text-align:center;background:#f8fafc}.ref50-drop strong{display:block;font-size:15px}.ref50-drop small{display:block;color:#7b8798;margin:5px 0 12px;line-height:1.35}.ref50-drop span{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 16px;border-radius:13px;background:#2f80ed;color:#fff;font-weight:850}.ref50-file{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px}.ref50-preview{margin-top:14px;border-radius:18px;overflow:hidden;background:#172a46;aspect-ratio:1;display:none}.ref50-preview.show{display:block}.ref50-preview img{width:100%;height:100%;object-fit:contain;display:block}.ref50-note{margin-top:12px;padding:12px 13px;border-radius:15px;background:#f4f7fb;color:#657184;font-size:11px;line-height:1.45}.ref50-actions{display:flex;gap:8px;margin-top:14px}.ref50-actions button{flex:1;min-height:44px;border:0;border-radius:14px;font-weight:850}.ref50-cancel{background:#eef1f5;color:#596579}.ref50-save{background:#ff5555;color:#fff}.ref50-reset{width:100%;min-height:42px;margin-top:8px;border:0;border-radius:13px;background:#fff0f0;color:#dd4b4b;font-weight:850}.ref50-toast{position:absolute;left:50%;bottom:calc(18px + env(safe-area-inset-bottom));transform:translate(-50%,16px);z-index:100;opacity:0;pointer-events:none;padding:9px 13px;border-radius:999px;background:rgba(15,29,49,.92);color:#fff;font-size:11px;font-weight:800;transition:.2s ease}.ref50-toast.show{opacity:1;transform:translate(-50%,0)}
@media(min-width:700px){.ref50-import{align-items:center}.ref50-sheet{padding:22px}}
'''
if '/* Map Import 5.0' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

js=r'''
// Map Import 5.0
const REF50_DB='livingdex-media-v1',REF50_STORE='media',REF50_KEY='paldea-map';
let ref50Pending=null,ref50ObjectUrl=null;
function ref50Db(){return new Promise((ok,no)=>{const r=indexedDB.open(REF50_DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(REF50_STORE))db.createObjectStore(REF50_STORE)};r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)})}
async function ref50Get(){try{const db=await ref50Db();return await new Promise((ok,no)=>{const t=db.transaction(REF50_STORE,'readonly'),r=t.objectStore(REF50_STORE).get(REF50_KEY);r.onsuccess=()=>ok(r.result||null);r.onerror=()=>no(r.error)})}catch(e){return null}}
async function ref50Put(blob){const db=await ref50Db();return new Promise((ok,no)=>{const t=db.transaction(REF50_STORE,'readwrite');t.objectStore(REF50_STORE).put(blob,REF50_KEY);t.oncomplete=ok;t.onerror=()=>no(t.error)})}
async function ref50Delete(){try{const db=await ref50Db();await new Promise((ok,no)=>{const t=db.transaction(REF50_STORE,'readwrite');t.objectStore(REF50_STORE).delete(REF50_KEY);t.oncomplete=ok;t.onerror=()=>no(t.error)})}catch(e){}}
function ref50Toast(msg){const t=document.getElementById('ref50Toast');if(!t)return;t.textContent=msg;t.classList.add('show');clearTimeout(ref50Toast._t);ref50Toast._t=setTimeout(()=>t.classList.remove('show'),1800)}
function ref50Open(){document.getElementById('ref50Import')?.classList.add('open')}
function ref50Close(){document.getElementById('ref50Import')?.classList.remove('open');ref50Pending=null;const f=document.getElementById('ref50File');if(f)f.value='';const p=document.getElementById('ref50Preview');if(p)p.classList.remove('show')}
function ref50Choose(){document.getElementById('ref50File')?.click()}
function ref50Selected(input){const file=input.files&&input.files[0];if(!file)return;if(!file.type.startsWith('image/')){ref50Toast('Selecione uma imagem válida');input.value='';return}if(file.size>18*1024*1024){ref50Toast('Imagem muito grande · máximo 18 MB');input.value='';return}ref50Pending=file;const url=URL.createObjectURL(file),img=document.getElementById('ref50PreviewImg'),box=document.getElementById('ref50Preview');if(img)img.src=url;if(box)box.classList.add('show');setTimeout(()=>URL.revokeObjectURL(url),30000)}
async function ref50Save(){if(!ref50Pending){ref50Toast('Escolha uma imagem primeiro');return}try{await ref50Put(ref50Pending);await ref50ApplyStored();ref50Close();ref50Toast('Mapa importado com sucesso')}catch(e){ref50Toast('Não foi possível salvar a imagem')}}
async function ref50ResetMap(){if(!confirm('Restaurar o mapa padrão de Paldea?'))return;await ref50Delete();if(ref50ObjectUrl){URL.revokeObjectURL(ref50ObjectUrl);ref50ObjectUrl=null}const img=document.querySelector('.ref49-mapimg');if(img){img.src='assets/maps/paldea-correct-order.jpg';img.onload=()=>ref50FitCanvas(img)}ref50Close();ref50Toast('Mapa padrão restaurado')}
function ref50FitCanvas(img){const c=document.getElementById('ref49Canvas');if(!c||!img||!img.naturalWidth||!img.naturalHeight)return;c.style.aspectRatio=`${img.naturalWidth}/${img.naturalHeight}`}
async function ref50ApplyStored(){const img=document.querySelector('.ref49-mapimg');if(!img)return;const blob=await ref50Get();if(!blob){img.onload=()=>ref50FitCanvas(img);return}if(ref50ObjectUrl)URL.revokeObjectURL(ref50ObjectUrl);ref50ObjectUrl=URL.createObjectURL(blob);img.onload=()=>ref50FitCanvas(img);img.src=ref50ObjectUrl;img.alt='Mapa personalizado de Paldea'}
function ref50Sheet(){return `<div id="ref50Import" class="ref50-import" onclick="if(event.target===this)ref50Close()"><div class="ref50-sheet"><div class="ref50-head"><b>Importar mapa</b><button class="ref50-x" onclick="ref50Close()" aria-label="Fechar">×</button></div><label class="ref50-drop" onclick="ref50Choose()"><strong>Selecione a imagem do mapa</strong><small>PNG, JPG ou WEBP · alta resolução recomendada · até 18 MB</small><span>Escolher imagem</span></label><input id="ref50File" class="ref50-file" type="file" accept="image/png,image/jpeg,image/webp,image/*" onchange="ref50Selected(this)"><div id="ref50Preview" class="ref50-preview"><img id="ref50PreviewImg" alt="Prévia do mapa"></div><div class="ref50-note">A imagem fica salva somente neste aparelho. Seus 19 pontos, níveis e progresso continuam funcionando por cima do mapa importado.</div><div class="ref50-actions"><button class="ref50-cancel" onclick="ref50Close()">Cancelar</button><button class="ref50-save" onclick="ref50Save()">Usar este mapa</button></div><button class="ref50-reset" onclick="ref50ResetMap()">Restaurar mapa padrão</button></div></div><div id="ref50Toast" class="ref50-toast"></div>`}
const ref50OldHtml=window.ref49MapHtml;
if(typeof ref50OldHtml==='function')window.ref49MapHtml=function(){let h=ref50OldHtml();h=h.replace('<div class="ref49-tools">','<div class="ref49-tools"><button onclick="ref50Open()" aria-label="Importar mapa">⇧</button>');return h+ref50Sheet()};
const ref50OldBind=window.ref49Bind||ref49Bind;
window.ref49Bind=function(){if(typeof ref50OldBind==='function')ref50OldBind();setTimeout(ref50ApplyStored,20)};
try{ref49Bind=window.ref49Bind}catch(e){}
const ref50OldRender=window.ref42RenderMap;
window.ref42RenderMap=function(){if(typeof ref50OldRender==='function')ref50OldRender();setTimeout(ref50ApplyStored,60)};
if(new URLSearchParams(location.search).get('v50qa')==='1')setTimeout(()=>{try{ref42Open('map');setTimeout(()=>{const f=document.getElementById('ref50File'),b=[...document.querySelectorAll('.ref49-tools button')].some(x=>x.getAttribute('aria-label')==='Importar mapa');if(f&&b&&f.accept.includes('image/'))document.documentElement.setAttribute('data-v50-qa','1')},350)}catch(e){}},250);
'''
if '// Map Import 5.0' not in s:
    s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)

p.write_text(s,encoding='utf-8')
print('Map Import 5.0 applied')

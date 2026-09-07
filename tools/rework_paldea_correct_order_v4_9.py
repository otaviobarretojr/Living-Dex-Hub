from pathlib import Path
import base64

ROOT=Path(__file__).resolve().parents[1]
assets=ROOT/'app/src/main/assets'
source=assets/'assets/maps/paldea-correct-order.jpg.b64'
image=assets/'assets/maps/paldea-correct-order.jpg'
if source.exists():
    image.write_bytes(base64.b64decode(source.read_text(encoding='utf-8').strip()))

p=assets/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-paldea-correct-order" content="4.9"' not in s:
    s=s.replace('</head>','<meta name="living-dex-paldea-correct-order" content="4.9"/>\n</head>',1)

css=r'''
/* Paldea Correct Order 4.9 — faithful image map + invisible interactive hotspots. */
.ref49-mapviewport{position:absolute;inset:0;overflow:hidden;background:#20395d;touch-action:none;user-select:none;-webkit-user-select:none}.ref49-mapviewport.fullscreen{position:fixed;inset:0;z-index:99999}.ref49-mapcanvas{position:absolute;left:50%;top:50%;width:min(100%,1080px);aspect-ratio:684/544;transform-origin:50% 50%;will-change:transform}.ref49-mapcanvas.dragging{transition:none}.ref49-mapimg{position:absolute;inset:0;width:100%;height:100%;display:block;object-fit:contain;pointer-events:none}.ref49-hotspot{position:absolute;width:clamp(40px,6.5vw,62px);aspect-ratio:1;border:0;border-radius:50%;background:transparent;transform:translate(-50%,-50%);z-index:8;cursor:pointer;-webkit-tap-highlight-color:transparent}.ref49-hotspot:focus-visible{outline:3px solid rgba(255,255,255,.95);outline-offset:2px}.ref49-hotspot.done::after{content:'✓';position:absolute;right:-2px;top:-3px;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;background:#26b56d;color:white;font-size:12px;font-weight:950;box-shadow:0 3px 10px rgba(0,0,0,.28);border:2px solid white}.ref49-toolbar{position:absolute;left:12px;right:12px;top:calc(10px + env(safe-area-inset-top));z-index:20;display:flex;align-items:center;justify-content:space-between;gap:8px;pointer-events:none}.ref49-progress{padding:8px 11px;border-radius:999px;background:rgba(15,29,49,.78);backdrop-filter:blur(10px);color:#fff;font-size:11px;font-weight:850;box-shadow:0 5px 18px rgba(0,0,0,.16)}.ref49-tools{display:flex;gap:6px;pointer-events:auto}.ref49-tools button{width:40px;height:40px;border:0;border-radius:13px;background:rgba(255,255,255,.94);color:#1d2b44;font-size:18px;font-weight:900;box-shadow:0 5px 16px rgba(0,0,0,.16)}.ref49-detail{position:absolute;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:30;padding:14px 15px;border-radius:20px;background:rgba(255,255,255,.97);color:#17213c;box-shadow:0 12px 34px rgba(0,0,0,.24);backdrop-filter:blur(16px);transform:translateY(calc(100% + 32px));opacity:0;transition:.2s ease}.ref49-detail.open{transform:none;opacity:1}.ref49-detailtop{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center}.ref49-badge{width:40px;height:40px;border-radius:13px;background:#fff0f0;color:#ff5555;display:grid;place-items:center;font-size:13px;font-weight:950}.ref49-detail b{display:block;font-size:14px}.ref49-detail small{display:block;margin-top:3px;color:#7b8798;font-size:10px;line-height:1.35}.ref49-close{width:32px;height:32px;border:0;border-radius:10px;background:#f1f3f6;color:#6f7a8c;font-size:18px}.ref49-actions{display:flex;gap:7px;margin-top:11px}.ref49-actions button{flex:1;min-height:40px;border:0;border-radius:13px;font-weight:850}.ref49-primary{background:#ff5555;color:#fff}.ref49-secondary{background:#f2f4f7;color:#556176}.ref49-hint{position:absolute;left:50%;bottom:calc(16px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:12;padding:7px 10px;border-radius:999px;background:rgba(15,29,49,.68);color:#fff;font-size:9px;white-space:nowrap;pointer-events:none;transition:.25s ease}.ref49-hint.hide{opacity:0;transform:translate(-50%,8px)}
@media(max-width:680px){.ref49-mapcanvas{width:112%;}.ref49-detail{left:8px;right:8px;bottom:calc(8px + env(safe-area-inset-bottom))}.ref49-toolbar{left:8px;right:8px}.ref49-tools button{width:38px;height:38px}.ref49-actions{flex-direction:column}}
'''
if '/* Paldea Correct Order 4.9' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

js=r'''
// Paldea Correct Order 4.9
const REF49_LEVELS=[15,16,17,19,21,24,27,28,30,33,36,42,44,45,48,51,55,56,62];
const REF49_POS=[[33.5,79.1],[67.8,74.0],[75.3,79.1],[18.6,63.2],[31.5,59.9],[82.6,58.4],[73.8,69.9],[76.6,50.4],[36.0,51.0],[64.3,42.9],[43.2,40.8],[59.0,31.1],[19.4,51.9],[25.4,91.2],[59.4,34.1],[56.0,23.3],[37.1,26.1],[82.7,34.3],[50.7,66.2]];
let ref49Zoom=1,ref49X=0,ref49Y=0,ref49Pointers=new Map(),ref49LastDist=0,ref49LastTap=0;
function ref49DoneArray(){try{return typeof ref43DoneArray==='function'?ref43DoneArray():[]}catch(e){return []}}
function ref49FinalDone(){return !!state?.journey?.sv?.correctOrderFinal}
function ref49IsDone(n){return n===19?ref49FinalDone():ref49DoneArray().includes(n)}
function ref49DoneCount(){return ref49DoneArray().length+(ref49FinalDone()?1:0)}
function ref49SetDone(n,value){state.journey=state.journey||{};state.journey.sv=state.journey.sv||{};if(n===19){state.journey.sv.correctOrderFinal=!!value;try{save()}catch(e){};return}if(typeof ref43SetDone==='function')ref43SetDone(n,value)}
function ref49Apply(){const c=document.getElementById('ref49Canvas');if(c)c.style.transform=`translate(-50%,-50%) translate(${ref49X}px,${ref49Y}px) scale(${ref49Zoom})`}
function ref49Reset(){ref49Zoom=1;ref49X=0;ref49Y=0;ref49Apply()}
function ref49ZoomBy(delta){ref49Zoom=Math.max(1,Math.min(4,ref49Zoom+delta));if(ref49Zoom===1){ref49X=0;ref49Y=0}ref49Apply();ref49HideHint()}
function ref49HideHint(){document.getElementById('ref49Hint')?.classList.add('hide')}
function ref49Name(n){if(n<=18&&window.SV_ROUTE&&SV_ROUTE[n-1])return SV_ROUTE[n-1][0];return 'Desafio final de Paldea'}
function ref49Kind(n){if(n<=18&&window.SV_ROUTE&&SV_ROUTE[n-1]){const k=SV_ROUTE[n-1][1];return k==='gym'?'Ginásio':k==='titan'?'Titã':'Team Star'}return 'Etapa final'}
function ref49Point(n){const d=document.getElementById('ref49Detail');if(!d)return;const done=ref49IsDone(n),level=REF49_LEVELS[n-1],name=ref49Name(n),kind=ref49Kind(n);d.innerHTML=`<div class="ref49-detailtop"><span class="ref49-badge">#${n}</span><div><b>${name}</b><small>${kind} · nível recomendado ${level} · ordem ${n} de 19</small></div><button class="ref49-close" onclick="ref49ClosePoint()" aria-label="Fechar">×</button></div><div class="ref49-actions"><button class="ref49-primary" onclick="ref49TogglePoint(${n})">${done?'Desmarcar concluído':'Marcar concluído'}</button>${n<=18?'<button class="ref49-secondary" onclick="ref42Open(\'team\')">Ver time</button>':''}</div>`;d.classList.add('open');ref49HideHint()}
function ref49ClosePoint(){document.getElementById('ref49Detail')?.classList.remove('open')}
function ref49TogglePoint(n){ref49SetDone(n,!ref49IsDone(n));ref49RenderMap();setTimeout(()=>ref49Point(n),40);if(typeof ref41Home==='function')setTimeout(ref41Home,0)}
function ref49Fullscreen(){const v=document.getElementById('ref49Viewport');if(!v)return;v.classList.toggle('fullscreen');document.body.style.overflow=v.classList.contains('fullscreen')?'hidden':'';setTimeout(ref49Reset,60)}
function ref49MapHtml(){return `<div id="ref49Viewport" class="ref49-mapviewport"><div id="ref49Canvas" class="ref49-mapcanvas"><img class="ref49-mapimg" src="assets/maps/paldea-correct-order.jpg" alt="Mapa de Paldea com ordem recomendada dos 19 objetivos" draggable="false">${REF49_POS.map((p,i)=>`<button class="ref49-hotspot ${ref49IsDone(i+1)?'done':''}" style="left:${p[0]}%;top:${p[1]}%" onclick="ref49Point(${i+1})" aria-label="Objetivo ${i+1}, nível ${REF49_LEVELS[i]}"></button>`).join('')}</div><div class="ref49-toolbar"><div id="ref49Progress" class="ref49-progress">${ref49DoneCount()}/19 concluídos</div><div class="ref49-tools"><button onclick="ref49ZoomBy(.45)" aria-label="Aumentar zoom">+</button><button onclick="ref49ZoomBy(-.45)" aria-label="Diminuir zoom">−</button><button onclick="ref49Reset()" aria-label="Restaurar mapa">⌂</button><button onclick="ref49Fullscreen()" aria-label="Tela cheia">⛶</button></div></div><div id="ref49Hint" class="ref49-hint">Toque nos pontos · pinça para ampliar</div><div id="ref49Detail" class="ref49-detail"></div></div>`}
function ref49RenderMap(){const page=document.getElementById('ref42MapPage');if(!page)return;ref49Zoom=1;ref49X=0;ref49Y=0;page.innerHTML=`${ref42Header('Mapa de Paldea','Ordem recomendada · 19 etapas','map')}<div class="ref42-content">${ref49MapHtml()}</div>`;setTimeout(ref49Bind,0)}
window.ref42RenderMap=ref49RenderMap;
function ref49Bind(){const v=document.getElementById('ref49Viewport'),c=document.getElementById('ref49Canvas');if(!v||!c)return;ref49Apply();v.onpointerdown=e=>{if(e.target.closest('.ref49-hotspot,.ref49-tools,.ref49-detail'))return;v.setPointerCapture?.(e.pointerId);ref49Pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});c.classList.add('dragging');ref49HideHint()};v.onpointermove=e=>{if(!ref49Pointers.has(e.pointerId))return;const prev=ref49Pointers.get(e.pointerId);ref49Pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(ref49Pointers.size===1&&ref49Zoom>1){ref49X+=e.clientX-prev.x;ref49Y+=e.clientY-prev.y;ref49Apply()}else if(ref49Pointers.size===2){const a=[...ref49Pointers.values()],dist=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);if(ref49LastDist){ref49Zoom=Math.max(1,Math.min(4,ref49Zoom+(dist-ref49LastDist)/150));ref49Apply()}ref49LastDist=dist}};const end=e=>{const start=ref49Pointers.get(e.pointerId);ref49Pointers.delete(e.pointerId);if(ref49Pointers.size<2)ref49LastDist=0;if(!ref49Pointers.size)c.classList.remove('dragging');if(start&&Math.hypot(e.clientX-start.x,e.clientY-start.y)<12){const now=Date.now();if(now-ref49LastTap<330){ref49Zoom=ref49Zoom>1?1:2;ref49X=0;ref49Y=0;ref49Apply();ref49LastTap=0}else ref49LastTap=now}};v.onpointerup=end;v.onpointercancel=end;v.onwheel=e=>{e.preventDefault();ref49ZoomBy(e.deltaY<0?.25:-.25)}}
// QA hook used by CI browser validation.
if(new URLSearchParams(location.search).get('v49qa')==='1'){setTimeout(()=>{try{ref42Open('map');setTimeout(()=>{const v=document.getElementById('ref49Viewport'),img=document.querySelector('.ref49-mapimg'),spots=document.querySelectorAll('.ref49-hotspot');if(v&&img&&spots.length===19&&img.getAttribute('src')==='assets/maps/paldea-correct-order.jpg')document.documentElement.setAttribute('data-v49-qa','1')},250)}catch(e){}},250)}
'''
if '// Paldea Correct Order 4.9' not in s:
    s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)

p.write_text(s,encoding='utf-8')
print('Paldea Correct Order 4.9 applied')

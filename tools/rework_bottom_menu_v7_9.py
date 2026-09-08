from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-menu-rework" content="7.9.0"' in s:
    print('Menu rework 7.9.0 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-menu-rework" content="7.9.0"/>\n</head>',1)
css=r'''
/* 7.9.0 — canonical, uniform Inicio + Box navigation. */
:root{--ld79-nav-h:68px}
body{padding-bottom:calc(var(--ld79-nav-h) + env(safe-area-inset-bottom,0px) + 14px)!important}
.mnav.ld79-nav{
 position:fixed!important;left:12px!important;right:12px!important;bottom:calc(10px + env(safe-area-inset-bottom,0px))!important;
 width:auto!important;height:var(--ld79-nav-h)!important;z-index:9999!important;
 display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:6px!important;
 padding:6px!important;margin:0!important;box-sizing:border-box!important;
 border:1px solid rgba(15,23,42,.10)!important;border-radius:22px!important;
 background:rgba(255,255,255,.96)!important;box-shadow:0 10px 30px rgba(15,23,42,.14)!important;
 backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)
}
.mnav.ld79-nav .ld79-item{
 min-width:0!important;border:0!important;border-radius:17px!important;background:transparent!important;
 display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;
 padding:0 12px!important;color:#64748b!important;font:700 13px/1 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;
 box-shadow:none!important;outline:none!important;transition:background .16s ease,color .16s ease,transform .12s ease!important
}
.mnav.ld79-nav .ld79-item:active{transform:scale(.98)!important}
.mnav.ld79-nav .ld79-item.active{background:#eef4ff!important;color:#1428a0!important}
.mnav.ld79-nav .ld79-icon{width:21px;height:21px;display:block;flex:0 0 21px}
.mnav.ld79-nav .ld79-label{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ld71-nav{display:none!important}
@media(min-width:700px){.mnav.ld79-nav{left:50%!important;right:auto!important;width:420px!important;transform:translateX(-50%)!important}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 7.9.0 — one menu component, one visual language, two destinations.
const LD79_HOME_ICON='<svg class="ld79-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3.5 10.5 12 3l8.5 7.5v9a1.5 1.5 0 0 1-1.5 1.5h-5v-6h-4v6H5a1.5 1.5 0 0 1-1.5-1.5v-9Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
const LD79_BOX_ICON='<svg class="ld79-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7.5 12 3l8 4.5v9L12 21l-8-4.5v-9Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="m4.5 7.8 7.5 4.3 7.5-4.3M12 12.1V21" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
function ld79Current(){
 const box=document.getElementById('boxView')||document.getElementById('box');
 if(box&&getComputedStyle(box).display!=='none'&&!box.hidden)return 'box';
 return 'home'
}
function ld79SetActive(page){
 const nav=document.querySelector('.mnav.ld79-nav');if(!nav)return;
 nav.querySelectorAll('.ld79-item').forEach(b=>{const on=b.dataset.ld79===page;b.classList.toggle('active',on);b.setAttribute('aria-current',on?'page':'false')})
}
function ld79Render(){
 let nav=document.querySelector('.mnav');
 if(!nav){nav=document.createElement('nav');nav.className='mnav';document.body.appendChild(nav)}
 document.querySelectorAll('.mnav').forEach((n,i)=>{if(i&&n!==nav)n.remove()});
 nav.className='mnav ld79-nav';nav.setAttribute('aria-label','Navegação principal');
 const valid=nav.querySelectorAll(':scope > .ld79-item').length===2;
 if(!valid)nav.innerHTML=`<button type="button" class="ld79-item" data-ld79="home" aria-label="Início">${LD79_HOME_ICON}<span class="ld79-label">Início</span></button><button type="button" class="ld79-item" data-ld79="box" aria-label="Box">${LD79_BOX_ICON}<span class="ld79-label">Box</span></button>`;
 const home=nav.querySelector('[data-ld79="home"]'),box=nav.querySelector('[data-ld79="box"]');
 home.onclick=()=>{try{ld7Home()}finally{setTimeout(()=>ld79SetActive('home'),0)}};
 box.onclick=()=>{try{ld71Open()}finally{setTimeout(()=>ld79SetActive('box'),0)}};
 document.querySelectorAll('.ld71-nav').forEach(n=>n.remove());
 ld79SetActive(ld79Current())
}
window.ld7Nav=ld79Render;
const ld79OldHome=window.ld7Home;if(typeof ld79OldHome==='function')window.ld7Home=function(){const r=ld79OldHome.apply(this,arguments);setTimeout(()=>{ld79Render();ld79SetActive('home')},0);return r};
const ld79OldBox=window.ld71Open;if(typeof ld79OldBox==='function')window.ld71Open=function(){const r=ld79OldBox.apply(this,arguments);setTimeout(()=>{ld79Render();ld79SetActive('box')},0);return r};
let ld79Queued=false;const ld79Observer=new MutationObserver(()=>{if(ld79Queued)return;ld79Queued=true;requestAnimationFrame(()=>{ld79Queued=false;ld79Render()})});
ld79Observer.observe(document.documentElement,{childList:true,subtree:true});
setTimeout(ld79Render,0);setTimeout(ld79Render,300);setTimeout(ld79Render,1000);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Menu rework 7.9.0 applied')

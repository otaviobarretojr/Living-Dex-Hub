from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-two-tabs-only" content="7.8.3"' in s:
    print('Two-tabs-only 7.8.3 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-two-tabs-only" content="7.8.3"/>\n</head>',1)
css=r'''
/* 7.8.3 — user-facing navigation is ONLY Inicio + Box. */
#library,#livingDex,#dex,#gameDex,#nationalDex,#games{display:none!important}
.ld71-nav,[data-ld7="library"],[data-ld7="livingDex"],[data-ld7="dex"],
[data-page="library"],[data-page="livingDex"],[data-page="dex"],
[onclick*="ld7Library"],[onclick*="livingDex"],[onclick*="go('library')"],[onclick*="go('livingDex')"]{display:none!important}
.mnav{grid-template-columns:repeat(2,1fr)!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 7.8.3 — purge legacy Biblioteca/Living Dex tabs and keep one canonical nav.
function ld783LegacyTab(el){
 const txt=(el?.textContent||'').trim().toLowerCase().replace(/\s+/g,' ');
 const data=((el?.getAttribute?.('data-ld7')||'')+' '+(el?.getAttribute?.('data-page')||'')+' '+(el?.getAttribute?.('onclick')||'')).toLowerCase();
 return txt==='biblioteca'||txt==='living dex'||txt==='livingdex'||/\b(library|livingdex)\b/.test(data)
}
function ld783NormalizeNav(){
 try{ld781Observer?.disconnect?.()}catch(e){}
 const navs=[...document.querySelectorAll('.mnav')];
 if(navs.length){
  const primary=navs[0];
  navs.slice(1).forEach(n=>n.remove());
  const buttons=[...primary.querySelectorAll(':scope > button')];
  const valid=buttons.length===2&&buttons[0]?.dataset?.ld7==='home'&&buttons[1]?.dataset?.ld7==='box';
  if(!valid)primary.innerHTML='<button class="ld7-navbtn" data-ld7="home" onclick="ld7Home()"><span>Início</span></button><button class="ld7-navbtn" data-ld7="box" onclick="ld71Open()"><span>Box</span></button>';
  primary.style.gridTemplateColumns='repeat(2,1fr)';
 }
 document.querySelectorAll('.ld71-nav').forEach(n=>n.remove());
 document.querySelectorAll('nav button,nav a,.mnav button,.mnav a,[role="tab"]').forEach(el=>{if(ld783LegacyTab(el))el.remove()});
 try{ld78NavState?.()}catch(e){}
}
window.ld7Nav=ld783NormalizeNav;
window.ld7Library=function(){return ld71Open()};
window.ld7OpenCurrent=function(){return ld71Open()};
const ld783PrevGo=window.go;
if(typeof ld783PrevGo==='function')window.go=function(page){
 const p=String(page||'').toLowerCase();
 if(['library','livingdex','dex','gamedex','nationaldex','games'].includes(p))return ld71Open();
 return ld783PrevGo.apply(this,arguments)
};
let ld783Queued=false;
const ld783Observer=new MutationObserver(()=>{
 if(ld783Queued)return;ld783Queued=true;
 requestAnimationFrame(()=>{ld783Queued=false;ld783NormalizeNav()})
});
ld783Observer.observe(document.documentElement,{childList:true,subtree:true});
setTimeout(ld783NormalizeNav,0);setTimeout(ld783NormalizeNav,250);setTimeout(ld783NormalizeNav,900);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Two-tabs-only 7.8.3 applied')

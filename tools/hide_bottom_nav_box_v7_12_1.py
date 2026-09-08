from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-only-bottom-nav" content="7.12.1"' in s:
    print('Home-only bottom nav 7.12.1 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-home-only-bottom-nav" content="7.12.1"/>\n</head>',1)
css=r'''
/* 7.12.1 — bottom navigation belongs to Home only. */
body.ld7121-box .mnav.ld79-nav{display:none!important}
body.ld7121-box{padding-bottom:14px!important}
#ld71BoxView{padding-bottom:calc(22px + env(safe-area-inset-bottom))!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 7.12.1 — hide the Inicio/Box bottom bar while Box is open.
function ld7121BoxOpen(){
 const box=document.getElementById('ld71BoxView');
 return !!(box&&box.classList.contains('active')&&getComputedStyle(box).display!=='none')
}
function ld7121SyncNav(){
 const onBox=ld7121BoxOpen();
 document.body.classList.toggle('ld7121-box',onBox);
 const nav=document.querySelector('.mnav.ld79-nav');
 if(nav){
  nav.setAttribute('aria-hidden',onBox?'true':'false');
  if(onBox)nav.setAttribute('inert','');else nav.removeAttribute('inert')
 }
 return !onBox
}
const ld7121OldOpen=window.ld71Open;
if(typeof ld7121OldOpen==='function')window.ld71Open=function(){const r=ld7121OldOpen.apply(this,arguments);ld7121SyncNav();setTimeout(ld7121SyncNav,0);return r};
const ld7121OldClose=window.ld71Close;
if(typeof ld7121OldClose==='function')window.ld71Close=function(){const r=ld7121OldClose.apply(this,arguments);setTimeout(ld7121SyncNav,0);return r};
const ld7121OldHome=window.ld7Home;
if(typeof ld7121OldHome==='function')window.ld7Home=function(){const r=ld7121OldHome.apply(this,arguments);setTimeout(ld7121SyncNav,0);return r};
const ld7121OldRender=window.ld79Render;
if(typeof ld7121OldRender==='function')window.ld79Render=function(){const r=ld7121OldRender.apply(this,arguments);ld7121SyncNav();return r};
let ld7121Queued=false;
const ld7121Observer=new MutationObserver(()=>{if(ld7121Queued)return;ld7121Queued=true;requestAnimationFrame(()=>{ld7121Queued=false;ld7121SyncNav()})});
ld7121Observer.observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style','hidden']});
window.ld7121Audit=function(){const nav=document.querySelector('.mnav.ld79-nav'),box=ld7121BoxOpen();return {version:'7.12.1',boxOpen:box,navPresent:!!nav,navHidden:box?(!nav||getComputedStyle(nav).display==='none'):false,homeNavExpected:!box}};
setTimeout(ld7121SyncNav,0);setTimeout(ld7121SyncNav,250);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Home-only bottom nav 7.12.1 applied')

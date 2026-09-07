from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-menu-fonts" content="4.1"' not in s:s=s.replace('</head>','<meta name="living-dex-menu-fonts" content="4.1"/>\n</head>',1)
css=r'''
/* Menu + typography 4.1 — one coherent reference system. */
:root{--r41-font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--r41-ink:#17213c;--r41-muted:#8f99aa;--r41-line:#edf0f5;--r41-surface:#fff;--r41-accent:#ff5555}
html,body,button,input,select,textarea{font-family:var(--r41-font)!important}body{font-weight:450;letter-spacing:-.008em;color:var(--r41-ink)}h1,h2,h3,.title,.r4-title{font-weight:800!important;letter-spacing:-.04em!important}.eyebrow,.kicker,.label{font-weight:800!important;letter-spacing:.085em!important}button,.btn{font-weight:750!important;letter-spacing:-.012em!important}
/* Bottom menu: stable three destinations, no legacy visual language. */
.mobile-nav,.r4-bottom-nav{height:72px!important;max-width:430px!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;bottom:max(10px,env(safe-area-inset-bottom))!important;padding:6px 9px!important;display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:4px!important;background:rgba(255,255,255,.96)!important;border:1px solid var(--r41-line)!important;border-radius:23px!important;box-shadow:0 9px 30px rgba(35,48,79,.12)!important;backdrop-filter:blur(14px)}.mobile-nav button,.r4-bottom-nav button{min-height:58px!important;border:0!important;border-radius:17px!important;background:transparent!important;color:#9aa3b4!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:3px!important;font-size:9px!important}.mobile-nav button.active,.r4-bottom-nav button.active{background:#fff0f0!important;color:var(--r41-accent)!important}.mobile-nav svg,.r4-bottom-nav svg{width:21px!important;height:21px!important}
/* More/Menu sheet */
.more-sheet,.sheet.more,.r4-menu-sheet{background:#f7f8fb!important;color:var(--r41-ink)!important}.more-sheet .sheet-card,.more-sheet .menu-item,.r4-menu-item{background:#fff!important;border:1px solid var(--r41-line)!important;border-radius:17px!important;box-shadow:0 4px 14px rgba(35,48,79,.055)!important}.more-sheet .menu-item,.r4-menu-item{min-height:54px!important;padding:10px 13px!important;font-size:13px!important}.more-sheet .menu-item small,.r4-menu-item small{display:none!important}
/* Appbar hierarchy */
#r4Appbar,.r4-appbar{font-family:var(--r41-font)!important}.r4-brand strong{font-size:15px!important;font-weight:850!important;letter-spacing:-.035em!important}.r4-screen{font-size:10px!important;font-weight:750!important;color:#8f99aa!important}
@media(max-width:430px){body{font-size:14px}.wrap{padding-left:15px!important;padding-right:15px!important;padding-bottom:98px!important}.ref41-title h2{font-size:22px}.ref41-card b{font-size:16px}.ref41-hubhead h1{font-size:25px}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Menu 4.1: normalize labels and preserve exactly Home / Geral / Menu as primary destinations.
function r41MenuNormalize(){const nav=document.querySelector('.mobile-nav')||document.querySelector('.r4-bottom-nav');if(nav){const visible=[...nav.querySelectorAll('button')].filter(b=>getComputedStyle(b).display!=='none');visible.forEach(b=>{const t=(b.textContent||'').trim().toLowerCase();if(t.includes('início')||t.includes('inicio'))b.dataset.r41='home';else if(t.includes('geral')||t.includes('jogos'))b.dataset.r41='general';else if(t.includes('mais')||t.includes('menu')){b.dataset.r41='menu';const tx=[...b.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());if(tx)tx.textContent='Menu'}})}document.querySelectorAll('.more-sheet h2,.sheet.more h2').forEach(h=>h.textContent='Menu')}
const r41Go=window.go;if(typeof r41Go==='function'){window.go=function(){const r=r41Go.apply(this,arguments);setTimeout(r41MenuNormalize,0);return r}}
setTimeout(r41MenuNormalize,50);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Menu and typography 4.1 applied')
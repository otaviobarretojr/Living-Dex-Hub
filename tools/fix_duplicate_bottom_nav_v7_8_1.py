from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-nav-dedup" content="7.8.1"' in s:
    print('Nav dedup 7.8.1 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-nav-dedup" content="7.8.1"/>\n</head>',1)
css=r'''
/* 7.8.1 — exactly one bottom navigation bar. */
.ld71-nav{display:none!important}
body>.mnav:not(:first-of-type){display:none!important}
.mnav{grid-template-columns:repeat(2,1fr)!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Bottom navigation dedup 7.8.1
function ld781NormalizeBottomNav(){
 const navs=[...document.querySelectorAll('.mnav')];
 if(!navs.length)return;
 const primary=navs[0];
 navs.slice(1).forEach(n=>n.remove());
 primary.innerHTML=`<button class="ld7-navbtn" data-ld7="home" onclick="ld7Home()"><span>Início</span></button><button class="ld7-navbtn" data-ld7="box" onclick="ld71Open()"><span>Box</span></button>`;
 primary.style.gridTemplateColumns='repeat(2,1fr)';
 document.querySelectorAll('.ld71-nav').forEach(n=>n.remove());
 try{ld78NavState?.()}catch(e){}
}
const ld781OldLd7Nav=window.ld7Nav;
window.ld7Nav=function(){
 try{if(typeof ld781OldLd7Nav==='function')ld781OldLd7Nav.apply(this,arguments)}catch(e){}
 ld781NormalizeBottomNav()
};
const ld781Observer=new MutationObserver(()=>ld781NormalizeBottomNav());
ld781Observer.observe(document.documentElement,{childList:true,subtree:true});
setTimeout(ld781NormalizeBottomNav,0);setTimeout(ld781NormalizeBottomNav,250);setTimeout(ld781NormalizeBottomNav,900)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Nav dedup 7.8.1 applied')

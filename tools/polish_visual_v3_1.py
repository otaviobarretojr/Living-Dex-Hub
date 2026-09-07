from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-visual-polish" content="3.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-visual-polish" content="3.1"/>\n</head>',1)
css=r'''
/* Visual polish 3.1 — tighter hierarchy, quieter UI, consistent first-party feel */
:root{--v31-space:12px;--v31-tap:48px}
/* remove remaining helper copy from navigation surfaces */
.mobile-more>button span,.mobile-more-head+small,.nav23-general-switch+small{display:none!important}
.mobile-more-head{padding:4px 5px 10px!important}.mobile-more-head b{font-size:15px!important;letter-spacing:-.02em!important}.mobile-more>button:not(.mobile-more-head button){min-height:52px!important;display:flex!important;align-items:center!important;padding:12px 14px!important;border-top:0!important;margin-top:6px!important}.mobile-more>button b{font-size:12px!important;font-weight:800!important}
/* normalized page rhythm */
.section{margin-top:18px!important}.section h2{margin-bottom:10px!important}.card+.card{margin-top:10px}.row{gap:9px!important}
/* Dex — more information with less visual bulk */
.dexgrid{gap:9px!important}.pk{min-height:142px!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:flex-start!important;padding:10px 8px 9px!important;position:relative!important}.pk img{width:76px!important;height:76px!important;margin:1px auto 3px!important}.pk h4{font-size:11px!important;line-height:1.15!important;margin:2px 0!important;text-align:center!important;max-width:100%!important}.pk .num{font-size:8px!important;letter-spacing:.04em!important}.pk .small,.pk small{font-size:8px!important;line-height:1.25!important}.quick-catch{position:absolute!important;right:7px!important;top:7px!important;width:31px!important;height:31px!important;min-width:31px!important;min-height:31px!important;padding:0!important;border-radius:10px!important;display:grid!important;place-items:center!important;font-size:0!important}.quick-catch:after{content:'+';font-size:18px;font-weight:700;line-height:1}.quick-catch.is-owned:after{content:'✓';font-size:15px}.toolbar,.filters{gap:8px!important;margin-bottom:10px!important}.toolbar .btn,.filters .btn{min-height:42px!important}.search{font-size:14px!important}
/* Game library — clearer card actions and less chrome */
#gamesGrid.nav23-compact-library .game{min-height:168px!important}.nav23-game-actions{grid-template-columns:1fr!important}.nav23-game-actions .game-active-btn,.nav23-game-actions .nav23-open-dex{min-height:42px!important;font-size:9px!important}.game .pill{padding:5px 7px!important}.game.playing:after{font-size:7px!important;padding:5px 7px!important}
/* Home — one visual focal point */
.home-current-head{align-items:center!important}.home-current-head>button{min-width:112px!important}.playing-top{align-items:center!important}.playing-name{margin-top:20px!important}.playing-progress{margin-top:18px!important}.playing-actions{margin-top:18px!important}.home-journey-summary{border-radius:20px!important;box-shadow:0 5px 18px rgba(3,10,24,.12)!important}.home-journey-summary h2,.home-journey-summary h3{margin-top:0!important}
/* Journey — organize as game companion, not dashboard */
.journey-card,.journey-panel{box-shadow:0 5px 18px rgba(3,10,24,.12)!important}.journey-card h2,.journey-card h3,.journey-panel h2,.journey-panel h3{margin-top:0!important}.journey-card .btn,.journey-panel .btn{min-height:44px!important}.journey-map-wrap,.journey-map{border:1px solid #e5eaf0!important}.journey-route-item,.journey-step,.route{border-radius:15px!important;box-shadow:none!important}.journey-team-card,.journey-build-card{border-radius:16px!important;box-shadow:none!important}
/* Pokémon profile — make the Pokémon the hero */
.sheet{padding-top:0!important}.sheet-head{position:sticky!important;top:0!important;z-index:4!important;background:#fff!important;padding:13px 4px 11px!important;margin:0 0 8px!important}.sheet-head h2,.sheet-head h3{font-size:18px!important}.sheet-close,.sheet-head button{min-width:44px!important;min-height:44px!important;border-radius:13px!important}.sheet .detailgrid{gap:10px!important}.sheet .detailgrid>.card:first-child{background:linear-gradient(180deg,#f7f9fc,#eef2f7)!important;min-height:230px!important;display:flex!important;align-items:center!important;justify-content:center!important}.sheet .detailgrid>.card:first-child img{width:min(68vw,240px)!important;height:min(68vw,240px)!important;max-height:240px!important;filter:drop-shadow(0 16px 22px rgba(16,24,40,.16))!important}.sheet .card{border-radius:17px!important;padding:14px!important}.sheet textarea{min-height:86px!important}.sheet select,.sheet input,.sheet textarea{width:100%!important}
/* Inputs/settings — simple grouped controls */
#settings .card,#storage .card,#planner .card,#forms .card,#families .card{box-shadow:0 5px 18px rgba(3,10,24,.12)!important}.settings label,#settings label{font-size:10px!important;font-weight:750!important;color:#667085!important}.settings input,.settings select,.settings textarea,#settings input,#settings select,#settings textarea{margin-top:5px!important}
/* App bar/nav */
.v3-appbar{height:42px!important;margin-bottom:10px!important}.v3-brand b{font-weight:850!important}.v3-screen{padding:6px 9px!important;border-radius:999px!important;background:rgba(255,255,255,.055)!important;color:#c2ccda!important}.mobile-nav{height:70px!important;align-items:center!important}.mnav-item{min-height:56px!important}.mnav-item.active{box-shadow:inset 0 0 0 1px #e4e9f0!important}.mnav-icon{height:22px!important}.mnav-icon svg{width:21px!important;height:21px!important}
/* accessibility/touch */
button:not(.quick-catch),.btn,.mnav-item,.mobile-more button,input,select{touch-action:manipulation}.btn,.mnav-item,.mobile-more button{cursor:pointer}
@media(max-width:700px){.dexgrid{grid-template-columns:repeat(3,minmax(0,1fr))!important}.pk{min-height:137px!important}.pk img{width:70px!important;height:70px!important}.sheet{max-height:96dvh!important;padding:0 12px calc(92px + env(safe-area-inset-bottom))!important}.sheet .detailgrid>.card:first-child{min-height:210px!important}.home-current-head>button{min-width:auto!important;min-height:42px!important}.mobile-more{left:12px!important;right:12px!important}}
@media(max-width:390px){.dexgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.pk{min-height:144px!important}.pk img{width:78px!important;height:78px!important}}
'''
if '/* Visual polish 3.1' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Visual polish 3.1 — trims residual instructional chrome and keeps screen labels in sync.
function v31Polish(){
 document.querySelectorAll('.mobile-more>button span').forEach(x=>x.remove());
 const mh=document.querySelector('.mobile-more-head b');if(mh)mh.textContent='Menu';
 // Remove duplicate explanatory microcopy, never gameplay/collection guidance.
 document.querySelectorAll('[data-ui-explainer],.library-intro,.general-intro,.dex-intro').forEach(x=>x.remove());
 if(typeof v3Appbar==='function')v3Appbar();
}
const v31Go=window.go;window.go=function(){const r=v31Go.apply(this,arguments);setTimeout(v31Polish,0);return r};
const v31OpenGameDex=window.nav221OpenGameDex;if(typeof v31OpenGameDex==='function')window.nav221OpenGameDex=async function(){const r=await v31OpenGameDex.apply(this,arguments);setTimeout(v31Polish,0);return r};
setTimeout(v31Polish,0);
if(new URLSearchParams(location.search).has('v31qa'))setTimeout(()=>{
 const appbar=!!document.getElementById('v3Appbar');
 const menu=document.querySelector('.mobile-more-head b')?.textContent.trim()==='Menu';
 const helper=!document.querySelector('.mobile-more>button span');
 const dex=!!document.querySelector('.dexgrid');
 document.documentElement.dataset.v31Qa=(appbar&&menu&&helper&&dex)?'1':'0';
},850);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Visual polish 3.1 applied')

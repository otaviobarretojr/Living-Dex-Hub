from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-visual-v3" content="3.0"' not in s:
    s=s.replace('</head>','<meta name="living-dex-visual-v3" content="3.0"/>\n</head>',1)
css=r'''
/* Living Dex Hub Visual 3.0 — original first-party console-grade design system. */
:root{
 --v3-bg:#0b1220;--v3-bg2:#101a2a;--v3-surface:#162235;--v3-surface2:#1b2940;
 --v3-card:#f7f9fc;--v3-card2:#ffffff;--v3-text:#101828;--v3-on-dark:#f8fbff;
 --v3-muted:#667085;--v3-muted-dark:#a7b4c6;--v3-line:#e5eaf0;--v3-line-dark:rgba(255,255,255,.09);
 --v3-accent:#e84b4b;--v3-blue:#4388f5;--v3-green:#35b779;--v3-yellow:#f3c64e;
 --v3-r-sm:12px;--v3-r:18px;--v3-r-lg:26px;--v3-shadow:0 8px 28px rgba(3,10,24,.16);
}
*{box-sizing:border-box}html{background:var(--v3-bg)!important}body{background:linear-gradient(180deg,var(--v3-bg) 0,var(--v3-bg2) 100%)!important;color:var(--v3-on-dark)!important;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;letter-spacing:0!important}
.wrap{max-width:1120px!important;margin:0 auto!important;padding-left:18px!important;padding-right:18px!important}.view{padding-top:6px!important}
/* remove legacy/prototype chrome */
.scope-note,.statusbar,.backup-guide,.sync-note,.data-pack-note{display:none!important}.ui24-explainer-hidden{display:none!important}
/* compact first-party app masthead */
.v3-appbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:8px auto 18px;max-width:1120px;padding:0 2px}.v3-brand{display:flex;align-items:center;gap:10px}.v3-mark{width:34px;height:34px;border-radius:11px;background:var(--v3-accent);display:grid;place-items:center;box-shadow:0 5px 14px rgba(232,75,75,.24)}.v3-mark svg{width:20px;height:20px;stroke:#fff;fill:none;stroke-width:2}.v3-brand b{font-size:15px;letter-spacing:-.02em}.v3-screen{font-size:11px;color:var(--v3-muted-dark);font-weight:700}
/* one card language */
.card,.game,.metric,.ring-card,.globalbox>.card,.playing-card,.empty-current,.home-journey-summary,.journey-card,.journey-panel,.sheet>div,.modal>div{background:var(--v3-card)!important;color:var(--v3-text)!important;border:1px solid var(--v3-line)!important;border-radius:var(--v3-r-lg)!important;box-shadow:var(--v3-shadow)!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
.card h1,.card h2,.card h3,.game h3,.playing-card h2,.home-journey-summary h2,.journey-card h2,.journey-card h3{color:var(--v3-text)!important;letter-spacing:-.025em!important}.tiny,.muted,.card p,.game .tiny,.playing-name p,.home-current-head p{color:var(--v3-muted)!important}
/* headers — title then content, no essays */
.section-head,.home-current-head{margin:4px 0 14px!important}.section-head h1,.section-head h2,.home-current-head h1{font-size:clamp(23px,5vw,34px)!important;line-height:1.06!important;letter-spacing:-.035em!important;margin:0!important;color:var(--v3-on-dark)!important}.section-head p,.home-current-head p,#home .playing-name p{display:none!important}.eyebrow{font-size:9px!important;letter-spacing:.12em!important;text-transform:uppercase!important;font-weight:800!important;color:#8fb5ff!important}
/* buttons */
button,.btn{font-family:inherit!important}.btn,.game-active-btn,.nav23-open-dex{min-height:46px!important;border-radius:14px!important;border:1px solid #d8dee8!important;background:#fff!important;color:#243044!important;font-size:11px!important;font-weight:800!important;box-shadow:none!important}.btn.primary,.btn.green,.nav23-open-dex{background:var(--v3-accent)!important;color:#fff!important;border-color:var(--v3-accent)!important}.btn:active,.game-active-btn:active,.nav23-open-dex:active{transform:scale(.98)!important}.game-active-btn.active{background:#eaf8f1!important;color:#157a4d!important;border-color:#ccebdc!important}
/* Home */
.home-current-shell{max-width:880px!important}.playing-card{padding:24px!important;overflow:hidden!important;position:relative!important}.playing-card:before{content:""!important;position:absolute!important;width:190px!important;height:190px!important;border-radius:50%!important;right:-65px!important;top:-72px!important;border:32px solid #eef2f7!important;opacity:.95!important}.playing-badge{background:#eaf8f1!important;color:#157a4d!important;border:0!important;border-radius:999px!important;padding:7px 10px!important}.playing-platform{background:#f0f3f7!important;color:#596579!important;border:0!important}.playing-name .version{color:var(--v3-accent)!important}.playing-name h2{font-size:clamp(30px,8vw,48px)!important}.premium-progress{height:9px!important;background:#e9edf3!important;border:0!important}.premium-progress i{background:linear-gradient(90deg,var(--v3-blue),#6b6df7)!important}.playing-percent{color:var(--v3-text)!important}.playing-actions{grid-template-columns:1fr!important}.playing-actions .btn{width:100%!important}
.home-journey-summary{margin-top:14px!important;padding:20px!important}.home-journey-summary .btn{margin-top:12px!important}
/* General library */
.nav23-general-switch{background:#111b2b!important;border:1px solid var(--v3-line-dark)!important;border-radius:15px!important;padding:4px!important;box-shadow:0 8px 22px rgba(0,0,0,.16)!important;backdrop-filter:none!important}.nav23-general-switch button{color:#aab6c7!important;border-radius:11px!important;font-size:11px!important}.nav23-general-switch button.active{background:#fff!important;color:#172235!important;box-shadow:none!important}
#gamesGrid.nav23-compact-library{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:12px!important}.game{min-height:172px!important;padding:16px!important}.game .plat{color:#7a8799!important}.game h3{font-size:15px!important}.game .pill{background:#eef2f7!important;color:#596579!important;border:0!important}.game .orb{opacity:.08!important;border-color:#667085!important}.game.playing:after{background:#eaf8f1!important;color:#157a4d!important;border:0!important}.nav23-game-actions{gap:7px!important}.nav23-game-actions .game-active-btn,.nav23-game-actions .nav23-open-dex{min-height:40px!important;font-size:8px!important}
/* Dex */
#dexCard,.globalbox{background:transparent!important;border:0!important;box-shadow:none!important}.toolbar,.filters{background:rgba(16,26,42,.96)!important;border:1px solid var(--v3-line-dark)!important;border-radius:18px!important;padding:10px!important;box-shadow:none!important}.search,input,select,textarea{background:#fff!important;color:#172235!important;border:1px solid #d9e0ea!important;border-radius:12px!important;min-height:42px!important}.pk{background:#fff!important;color:var(--v3-text)!important;border:1px solid var(--v3-line)!important;border-radius:18px!important;box-shadow:0 5px 18px rgba(3,10,24,.12)!important;padding:10px!important}.pk:hover{border-color:#cfd7e2!important}.pk img{filter:none!important}.pk .num,.pk .small,.pk small{color:#778397!important}.quick-catch{background:#fff!important;color:#344054!important;border:1px solid #dfe5ed!important;box-shadow:0 3px 10px rgba(0,0,0,.09)!important}.quick-catch.is-owned{background:#eaf8f1!important;color:#157a4d!important;border-color:#caeadb!important}
/* Journey */
.journey-shell,.journey-view{color:var(--v3-on-dark)!important}.journey-card,.journey-panel{padding:18px!important}.journey-card p,.journey-card small,.journey-panel p,.journey-panel small{color:var(--v3-muted)!important}.journey-map-wrap,.journey-map{border-radius:20px!important;overflow:hidden!important}.journey-progress,.journey-route-progress{background:#e9edf3!important}.journey-progress>i,.journey-route-progress>i{background:var(--v3-blue)!important}
/* profile / sheets */
.sheet,.modal{background:rgba(3,8,18,.58)!important;backdrop-filter:blur(10px)!important;-webkit-backdrop-filter:blur(10px)!important}.sheet>div,.modal>div{background:#fff!important;color:var(--v3-text)!important}.sheet h2,.sheet h3,.modal h2,.modal h3{color:var(--v3-text)!important}.sheet p,.sheet small,.modal p,.modal small{color:var(--v3-muted)!important}.sheet .btn,.modal .btn{background:#f7f9fc!important}.sheet .btn.primary,.modal .btn.primary{background:var(--v3-accent)!important;color:#fff!important}
/* More / settings */
.mobile-more{background:#fff!important;color:var(--v3-text)!important;border:1px solid var(--v3-line)!important;border-radius:24px 24px 0 0!important;box-shadow:0 -14px 44px rgba(0,0,0,.22)!important;backdrop-filter:none!important}.mobile-more button{background:#f7f9fc!important;color:#243044!important;border:1px solid #edf0f4!important;border-radius:14px!important}.mobile-more button:active{background:#eef2f7!important}
#settings .card,#storage .card,#planner .card,#forms .card,#families .card{padding:18px!important}.audio-settings,#ldhAudioSettings,#ldhAudioQuick{display:none!important}
/* bottom navigation */
.mobile-nav{left:14px!important;right:14px!important;bottom:max(10px,env(safe-area-inset-bottom))!important;background:#fff!important;border:1px solid #e6ebf1!important;border-radius:22px!important;padding:6px!important;box-shadow:0 12px 35px rgba(0,0,0,.22)!important;backdrop-filter:none!important}.mnav-item{color:#7b8798!important;border-radius:16px!important;min-height:54px!important}.mnav-item.active{background:#f0f3f7!important;color:#172235!important}.mnav-icon svg{stroke-width:2!important}.mnav-item span:last-child{font-size:9px!important;font-weight:800!important}
/* desktop legacy tabs become subtle rather than another dominant navigation */
.tabs{background:transparent!important;border:0!important;box-shadow:none!important;gap:4px!important}.tabs button{background:transparent!important;border:0!important;color:#91a0b4!important;border-radius:10px!important}.tabs button.active{background:rgba(255,255,255,.08)!important;color:#fff!important}
/* motion */
.view.active{animation:v3in .18s ease-out!important}@keyframes v3in{from{opacity:.55;transform:translateY(5px)}to{opacity:1;transform:none}}
@media(max-width:700px){.wrap{padding-left:12px!important;padding-right:12px!important;padding-bottom:calc(94px + env(safe-area-inset-bottom))!important}.v3-appbar{margin-top:5px;margin-bottom:12px}.v3-mark{width:31px;height:31px;border-radius:10px}.v3-brand b{font-size:13px}.v3-screen{font-size:9px}.playing-card{padding:18px!important;border-radius:22px!important}.home-journey-summary{padding:16px!important;border-radius:20px!important}#gamesGrid.nav23-compact-library{gap:9px!important}.game{min-height:160px!important;padding:13px!important;border-radius:18px!important}.pk{border-radius:16px!important}.mobile-more{padding-bottom:calc(16px + env(safe-area-inset-bottom))!important}}
@media(min-width:900px){#gamesGrid.nav23-compact-library{grid-template-columns:repeat(3,minmax(0,1fr))!important}.mobile-nav{max-width:420px!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important}}
'''
if '/* Living Dex Hub Visual 3.0' not in s:s.replace('</style>',css+'\n</style>',1)
else: pass
if '/* Living Dex Hub Visual 3.0' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Visual 3.0 — original UI chrome; no Nintendo-owned UI assets are used.
function v3Icon(){return '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M4 12h16"/><circle cx="12" cy="12" r="2.6"/></svg>'}
function v3CurrentScreen(){
 const active=document.querySelector('.view.active');
 const id=active?.id||'home';
 const names={home:'Início',games:'Geral',global:'Dex Nacional',families:'Famílias',planner:'Planejamento',forms:'Form Dex',storage:'Storage',settings:'Configurações'};
 if(document.body.classList.contains('game-dex-focus'))return 'Dex do jogo';
 return names[id]||'Living Dex';
}
function v3Appbar(){
 let bar=document.getElementById('v3Appbar');
 if(!bar){bar=document.createElement('div');bar.id='v3Appbar';bar.className='v3-appbar';bar.innerHTML=`<div class="v3-brand"><span class="v3-mark">${v3Icon()}</span><b>Living Dex</b></div><span class="v3-screen"></span>`;const wrap=document.querySelector('.wrap');if(wrap)wrap.prepend(bar);else document.body.prepend(bar)}
 const label=bar.querySelector('.v3-screen');if(label)label.textContent=v3CurrentScreen();
}
function v3AuditCleanup(){
 document.querySelectorAll('.scope-note,.statusbar,.sync-note,.data-pack-note').forEach(x=>x.remove());
 document.querySelectorAll('#home .home-current-head p,#home .playing-name p').forEach(x=>x.remove());
 // keep useful data, warnings, Journey guidance and Pokémon acquisition instructions.
 v3Appbar();
}
const v3BaseGo=window.go;
window.go=function(){const r=v3BaseGo.apply(this,arguments);setTimeout(v3AuditCleanup,0);return r};
const v3BaseHome=window.renderActiveGameHome;
if(typeof v3BaseHome==='function')window.renderActiveGameHome=function(){const r=v3BaseHome.apply(this,arguments);setTimeout(v3AuditCleanup,0);return r};
setTimeout(v3AuditCleanup,0);
if(new URLSearchParams(location.search).has('v3qa'))setTimeout(()=>{
 const ok=!!document.getElementById('v3Appbar')&&!!document.querySelector('.mobile-nav')&&!document.querySelector('.scope-note')&&!document.querySelector('.statusbar')&&!!document.querySelector('meta[name="living-dex-visual-v3"]');
 document.documentElement.dataset.v3Qa=ok?'1':'0';
},700);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Visual rework 3.0 applied')

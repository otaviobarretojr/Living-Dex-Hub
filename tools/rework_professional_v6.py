from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-professional-ui" content="6.0"' not in s:s=s.replace('</head>','<meta name="living-dex-professional-ui" content="6.0"/>\n</head>',1)
css=r'''
/* Professional UI 6.0 — unified spacing, typography, surfaces, motion and touch targets. */
:root{
 --ui-bg:#f6f8fc;--ui-surface:#fff;--ui-surface2:#f9fafc;--ui-ink:#16213b;--ui-muted:#8b96a9;--ui-line:#e8edf4;
 --ui-accent:#ff5757;--ui-accent-soft:#fff0f0;--ui-success:#20b985;--ui-blue:#4f91f3;
 --ui-r1:14px;--ui-r2:18px;--ui-r3:24px;--ui-r4:30px;--ui-shadow:0 8px 26px rgba(33,48,78,.07);
 --ui-s1:4px;--ui-s2:8px;--ui-s3:12px;--ui-s4:16px;--ui-s5:20px;--ui-s6:24px;--ui-s7:32px;
}
html,body{background:var(--ui-bg)!important;color:var(--ui-ink)!important;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
body{letter-spacing:-.008em}button,input,select,textarea{font:inherit}button,[role="button"],a[onclick]{-webkit-tap-highlight-color:transparent;touch-action:manipulation}button:active,[role="button"]:active{transform:scale(.985)}
/* Consistent page canvas */
.view,#home,#games,#global,#families,#planner,#forms,#storage,#settings{max-width:820px;margin:0 auto!important;padding-left:16px!important;padding-right:16px!important}
#home{padding-top:10px!important}.section-title,h1,h2,h3{color:var(--ui-ink)}
/* Professional bottom navigation */
.mnav{left:16px!important;right:16px!important;bottom:calc(10px + env(safe-area-inset-bottom))!important;width:auto!important;max-width:790px!important;margin:auto!important;padding:8px!important;border-radius:24px!important;background:rgba(255,255,255,.95)!important;border:1px solid rgba(230,235,243,.9)!important;box-shadow:0 16px 38px rgba(31,46,75,.13)!important;backdrop-filter:blur(18px)}
.mnav-item{min-height:64px!important;border-radius:18px!important;color:#9aa4b4!important;font-size:11px!important;font-weight:850!important;gap:5px!important}.mnav-item svg{width:22px!important;height:22px!important}.mnav-item.active{background:var(--ui-accent-soft)!important;color:var(--ui-accent)!important}
/* Home: preserve approved structure and eliminate residual competing cards */
#home .home-current-shell{max-width:780px!important}.home51-hero{border-radius:30px!important}.home51-cta{min-height:62px!important;border-radius:20px!important}.home51-journey{margin-top:26px!important}.home51-jhead{margin-bottom:14px!important}.home51-next{box-shadow:var(--ui-shadow)!important;border-color:var(--ui-line)!important;overflow:hidden}.home51-nexttitle,.home51-nextsub{display:block!important}.home51-nexttitle{padding-right:28px}
#home>.journey,#home>.journey-section,#home>.ref41-home,#home .home-journey-summary,#home .home232-journey{display:none!important}
/* Journey hub */
.jh52{background:var(--ui-bg)!important}.jh52-head{min-height:72px!important;padding-left:16px!important;padding-right:16px!important}.jh52-back{min-width:44px!important;min-height:44px!important}.jh52-body{max-width:820px;width:100%;margin:0 auto!important;padding:16px 16px calc(32px + env(safe-area-inset-bottom))!important}.jh52-summary{border-radius:28px!important;padding:22px!important}.jh52-tabs{gap:8px!important;padding-top:10px!important}.jh52-tab{min-height:46px!important;border-radius:15px!important}.jh52-card,.jh52-step,.jh52-mon{border-color:var(--ui-line)!important;box-shadow:0 4px 16px rgba(33,48,78,.045)!important}.jh52-step{min-height:66px!important}.jh52-check{min-width:38px!important;min-height:38px!important}.jh52-mon{min-height:150px!important}.jh52-mon img{width:100px!important;height:100px!important}.jh52-mapwrap{border:1px solid var(--ui-line);box-shadow:var(--ui-shadow)}
/* Library */
.nav23-general-switch{position:sticky;top:calc(8px + env(safe-area-inset-top));z-index:20;margin:8px 0 14px!important;padding:5px!important;border-radius:18px!important;background:rgba(255,255,255,.95)!important;backdrop-filter:blur(16px);box-shadow:0 6px 18px rgba(33,48,78,.06)!important}.nav23-general-switch button{min-height:44px!important;border-radius:14px!important;font-weight:850!important}
#games .game-card{border-radius:24px!important;border:1px solid var(--ui-line)!important;box-shadow:var(--ui-shadow)!important;padding:0!important;overflow:hidden!important}.library46-card,.ref45-game-card{border-radius:24px!important;overflow:hidden!important}.library46-cover,.ref45-game-cover{aspect-ratio:16/9!important;object-fit:cover!important;width:100%!important}.library46-actions button,.ref45-game-card button{min-height:46px!important;border-radius:14px!important}
/* Dex and cards */
#dexCard{padding:16px!important;border-radius:26px!important;border-color:var(--ui-line)!important;box-shadow:var(--ui-shadow)!important}.dex-grid,.pokemon-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:10px!important}.pokemon-card,.dex-card{min-width:0!important;border-radius:20px!important;border:1px solid var(--ui-line)!important;box-shadow:0 3px 13px rgba(33,48,78,.045)!important;padding:10px!important}.pokemon-card img,.dex-card img{width:100%!important;aspect-ratio:1/1!important;object-fit:contain!important}.pokemon-card b,.dex-card b{font-size:12px!important}.pokemon-card small,.dex-card small{font-size:9px!important;color:var(--ui-muted)!important}
/* Menu, settings and generic cards */
#moreSheet,.more-sheet{background:var(--ui-bg)!important}.more-item,.menu-item,#settings .card,#storage .card,#planner .card,#forms .card,#families .card{border-radius:20px!important;border:1px solid var(--ui-line)!important;background:#fff!important;box-shadow:0 4px 16px rgba(33,48,78,.045)!important}.more-item,.menu-item{min-height:60px!important;padding:12px 14px!important}.more-item svg,.menu-item svg{width:22px!important;height:22px!important}
/* Dialogs/forms */
.sheet,.modal-content,.dialog{border-radius:28px 28px 0 0!important;background:#fff!important;border-color:var(--ui-line)!important}.sheet-header,.modal-header{min-height:64px!important;padding:14px 16px!important}.profile-section,.profile-card,.detail-card{border-radius:20px!important;border:1px solid var(--ui-line)!important;padding:16px!important}.sheet-close,.close,.icon-btn,.back-btn{min-width:44px!important;min-height:44px!important;border-radius:14px!important}
input,select,textarea{min-height:48px!important;border-radius:14px!important;padding:10px 12px!important}textarea{min-height:96px!important}
/* Buttons */
.btn,button.primary,button.secondary{font-weight:850}.btn.primary,button.primary{background:var(--ui-accent)!important;border:0!important;color:#fff!important;box-shadow:0 6px 16px rgba(255,87,87,.18)!important}.btn.secondary,button.secondary{background:#fff!important;color:var(--ui-ink)!important;border:1px solid var(--ui-line)!important;box-shadow:none!important}
/* Accessibility / polish */
:focus-visible{outline:3px solid rgba(79,145,243,.35)!important;outline-offset:2px}.scope-note,.statusbar,.backup-guide,.sync-note,.data-pack-note,.library-intro,.general-intro,.dex-intro,[data-ui-explainer]{display:none!important}
@media(max-width:520px){.view,#home,#games,#global,#families,#planner,#forms,#storage,#settings{padding-left:12px!important;padding-right:12px!important}.mnav{left:10px!important;right:10px!important}.dex-grid,.pokemon-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}.home51-title{font-size:36px!important}.home51-hero{padding:20px!important}.home51-cover{width:104px!important;height:140px!important}.home51-next{padding-left:78px!important}.home51-nexticon{left:17px!important}.jh52-team{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(max-width:360px){.dex-grid,.pokemon-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.home51-platform{max-width:145px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Professional UI 6.0 runtime audit/cleanup.
function pro60CleanHome(){const h=document.getElementById('home');if(!h)return;h.querySelectorAll('.home232-journey,.home-journey-summary').forEach(x=>x.remove());const sections=[...h.querySelectorAll('section')].filter(x=>x.classList.contains('home51-journey'));sections.slice(1).forEach(x=>x.remove());}
function pro60A11y(){document.querySelectorAll('button,[role="button"],a[onclick]').forEach(el=>{if(!el.getAttribute('aria-label')&&!String(el.textContent||'').trim()){const t=el.getAttribute('title')||'Ação';el.setAttribute('aria-label',t)}})}
function pro60Audit(){pro60CleanHome();pro60A11y();document.documentElement.dataset.professionalUi='6.0';document.documentElement.dataset.touchAudit=[...document.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect();return r.width>0&&r.height>0&&r.height<38}).length?'warn':'ok'}
const pro60Go=window.go;if(typeof pro60Go==='function')window.go=function(){const r=pro60Go.apply(this,arguments);setTimeout(pro60Audit,0);return r};
const pro60Render=window.renderActiveGameHome;if(typeof pro60Render==='function')window.renderActiveGameHome=function(){const r=pro60Render.apply(this,arguments);setTimeout(pro60Audit,0);return r};
const pro60Open=window.jh52Open;if(typeof pro60Open==='function')window.jh52Open=function(){const r=pro60Open.apply(this,arguments);setTimeout(pro60Audit,0);return r};
setTimeout(pro60Audit,120);
if(new URLSearchParams(location.search).has('pro60qa'))setTimeout(()=>{pro60Audit();const h=document.getElementById('home');const one=h?[...h.querySelectorAll('.home51-journey')].length<=1:true;const hub=!!document.getElementById('jh52');document.documentElement.dataset.pro60Qa=(one&&hub&&document.documentElement.dataset.professionalUi==='6.0')?'1':'0'},900);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Professional UI 6.0 applied')

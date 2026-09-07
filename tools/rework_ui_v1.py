from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html'
html = HTML.read_text(encoding='utf-8')

html = html.replace('<meta name="living-dex-build" content="core-1.0"/>', '<meta name="living-dex-build" content="core-1.0"/>\n<meta name="living-dex-ui" content="1.1"/>', 1)
html = html.replace('Living Dex Hub • Build 28.0 • Android Package', 'Living Dex Hub • Core 1.0 • UI 1.1 • Offline', 1)
html = html.replace('<div class="top">', '<div class="top appbar">', 1)
html = html.replace('<div class="note" style="margin-bottom:12px">\n<b>Escopo do Living Dex Hub</b>', '<div class="note scope-note" style="margin-bottom:12px">\n<b>Escopo do Living Dex Hub</b>', 1)

mobile_nav = '''
<nav class="mobile-nav" aria-label="Navegação principal">
 <button class="mnav-item active" data-v="home" onclick="go('home')"><span class="mnav-icon">⌂</span><span>Início</span></button>
 <button class="mnav-item" data-v="games" onclick="go('games')"><span class="mnav-icon">▦</span><span>Jogos</span></button>
 <button class="mnav-item" data-v="global" onclick="go('global')"><span class="mnav-icon">◉</span><span>Dex</span></button>
 <button class="mnav-item" data-v="missing" onclick="go('missing')"><span class="mnav-icon">◎</span><span>Faltando</span></button>
 <button class="mnav-item" id="mobileMoreBtn" onclick="toggleMobileMore(event)"><span class="mnav-icon">•••</span><span>Mais</span></button>
</nav>
<div class="mobile-more" id="mobileMore" aria-hidden="true">
 <div class="mobile-more-head"><b>Mais ferramentas</b><button type="button" onclick="closeMobileMore()">×</button></div>
 <button onclick="go('families')"><b>Famílias evolutivas</b><span>Veja linhas completas e pendências</span></button>
 <button onclick="go('planner')"><b>Planejamento</b><span>Organize próximas capturas e evoluções</span></button>
 <button onclick="go('forms')"><b>Form Dex</b><span>Acompanhe formas colecionáveis</span></button>
 <button onclick="go('storage')"><b>Storage &amp; HOME</b><span>Localização dos seus exemplares</span></button>
 <button onclick="go('settings')"><b>Configurações</b><span>Backup, dados e sincronização</span></button>
</div>
<div class="mobile-more-backdrop" id="mobileMoreBackdrop" onclick="closeMobileMore()"></div>
'''
if 'class="mobile-nav"' not in html:
    html = html.replace('</div>\n<div class="statusbar">', '</div>\n' + mobile_nav + '<div class="statusbar">', 1)

ui_css = r'''
/* Living Dex Hub UI 1.1 — visual rework. Core logic untouched. */
:root{--bg:#07101b;--panel:#0e1827;--panel2:#142238;--line:#223652;--text:#f7f9fc;--muted:#8fa1bc;--red:#ff5a67;--yellow:#ffd45a;--green:#48d7a2;--blue:#6aafff;--surface:#0b1524;--surface2:#101d31;--shadow:0 18px 55px #0005}
html{scroll-behavior:smooth}body{min-height:100vh;background:radial-gradient(circle at 12% -8%,#24508655 0,transparent 30%),radial-gradient(circle at 92% 8%,#54274433 0,transparent 26%),linear-gradient(180deg,#08111e 0,#060b13 60%,#050910 100%)}
.wrap{max-width:1320px;padding:20px 22px 46px}.appbar{position:relative;padding:5px 0 4px}.brand h1{font-size:21px;letter-spacing:-.02em}.brand .tiny{margin-top:2px}.logo{width:44px;height:44px;box-shadow:0 10px 30px #0008,0 0 0 1px #ffffff0a}
.actions .btn{min-height:38px}.btn{transition:.18s ease;border-color:#29405f;background:linear-gradient(180deg,#14213a,#101a2d);box-shadow:inset 0 1px #ffffff08}.btn:hover{transform:translateY(-1px);border-color:#49698f}.btn.primary{background:linear-gradient(135deg,#ff5364,#e94356);box-shadow:0 8px 22px #ff536421}.btn.green{background:linear-gradient(135deg,#12352b,#163e31)}
.nav{gap:8px;padding:14px 0 11px}.tab{padding:9px 13px;background:#0d1829;border-color:#223754;transition:.18s ease}.tab:hover{border-color:#486485;color:#eef4ff}.tab.active{background:#f5f8fd;color:#0b1320;border-color:#f5f8fd;box-shadow:0 8px 22px #0003}
.statusbar{margin-top:2px;background:#081322cc;border-color:#1d304a;backdrop-filter:blur(12px);padding:8px 11px}.statusgroup{gap:13px}.card{background:linear-gradient(180deg,#101c2f 0,#0c1626 100%);border-color:#213652;box-shadow:var(--shadow);border-radius:22px}.hero>.card:first-child{background:radial-gradient(circle at 86% 8%,#4b7ecb18,transparent 33%),linear-gradient(160deg,#13243c,#0c1627)}
.scope-note{border-style:dashed;background:#091422aa;color:#aebed3}.scope-note b{color:#dce8f6}.kicker{color:#8fa9ca}.big{letter-spacing:-.035em}.section{margin-top:26px}.section h2{font-size:19px;letter-spacing:-.02em}.metric,.gp,.family-card,.quest,.route,.queue-item,.callout,.pk,.game{box-shadow:inset 0 1px #ffffff06;transition:transform .18s ease,border-color .18s ease,background .18s ease}.pk:hover,.game:hover,.family-card:hover{transform:translateY(-2px);border-color:#47698f}.pk.caught{box-shadow:inset 0 1px #ffffff08,0 8px 24px #153e3020}.pk img{filter:drop-shadow(0 9px 14px #0006)}
.search,.settings input,.settings textarea,.specimen select,.specimen input{background:#07111f;border-color:#243b5a;outline:none}.search:focus,.settings input:focus,.settings textarea:focus,.specimen select:focus,.specimen input:focus{border-color:#5d91c8;box-shadow:0 0 0 3px #5d91c819}.sheet{background:linear-gradient(180deg,#111d31,#0b1423);box-shadow:0 -24px 70px #0008}.pager{gap:10px}.pagerinfo{color:#aebed4;font-size:10px}.mobile-nav,.mobile-more,.mobile-more-backdrop{display:none}
@media(max-width:700px){body{background:radial-gradient(circle at 30% -5%,#1a3c6855,transparent 28%),linear-gradient(180deg,#08111d,#060b13)}.wrap{padding:12px 12px 94px}.appbar{padding:2px 0 8px}.brand{gap:9px}.brand h1{font-size:18px}.brand .tiny{font-size:9px;max-width:210px}.logo{width:38px;height:38px;border-width:2px}.actions{margin-left:auto}.actions .optional{display:none}.actions .primary{font-size:0;width:38px;height:38px;padding:0;border-radius:13px}.actions .primary:after{content:'→';font-size:19px;font-weight:800}.nav{display:none!important}.statusbar{margin:0 0 12px;padding:8px 10px;border-radius:12px}.statusbar>span:last-child{display:none}.statusgroup{width:100%;justify-content:space-between;gap:6px}.statusitem{font-size:8px}.scope-note{font-size:10px;padding:10px 11px;border-radius:14px}.hero,.progress-zone,.globalbox,.family-dashboard,.detailgrid,.planner{grid-template-columns:1fr}.hero{gap:10px}.card{padding:14px;border-radius:18px;box-shadow:0 12px 35px #0004}.big{font-size:29px}.stats{grid-template-columns:repeat(2,1fr)}.ring-card{grid-template-columns:108px 1fr;gap:12px;min-height:150px}.ring{width:104px;height:104px}.ring:before{inset:9px}.ring-inner b{font-size:22px}.ring-copy h3{font-size:18px}.metric-grid{grid-template-columns:repeat(2,1fr)}.metric{min-height:82px;padding:11px}.metric .v{font-size:19px}.game-progress-list{grid-template-columns:repeat(2,1fr)}.games{grid-template-columns:1fr 1fr}.game{min-height:132px;padding:13px}.game h3{font-size:14px}.orb{width:94px;height:94px;border-width:18px}.dexgrid{grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}.pk{min-height:127px;padding:8px;border-radius:14px}.pk img{width:65px;height:65px}.pk h4{font-size:10px}.toolbar{position:sticky;top:0;z-index:12;background:#07101be8;margin:0 -4px 11px;padding:8px 4px;backdrop-filter:blur(10px)}.search{min-width:100%;width:100%;flex-basis:100%}.family-list{grid-template-columns:1fr}.route-grid{grid-template-columns:1fr}.sheet{max-height:94vh;padding:14px;border-radius:24px 24px 0 0}.pager{position:sticky;bottom:76px;z-index:11;background:#091523e8;padding:8px;border:1px solid var(--line);border-radius:14px;backdrop-filter:blur(10px)}.section{margin:20px 0 9px}.section h2{font-size:17px}.mobile-nav{display:grid;grid-template-columns:repeat(5,1fr);position:fixed;left:10px;right:10px;bottom:max(10px,env(safe-area-inset-bottom));z-index:50;background:#0a1422eb;border:1px solid #263b58;border-radius:20px;padding:7px;box-shadow:0 18px 55px #000b;backdrop-filter:blur(18px)}.mnav-item{appearance:none;border:0;background:transparent;color:#8496af;border-radius:14px;padding:7px 3px 6px;display:grid;place-items:center;gap:3px;font-size:8px;font-weight:700;cursor:pointer}.mnav-item.active{background:#f3f7fc;color:#0a1320}.mnav-icon{font-size:18px;line-height:1;font-weight:800}.mnav-item:last-child .mnav-icon{letter-spacing:1px;font-size:14px}.mobile-more-backdrop{position:fixed;inset:0;z-index:51;background:#02060dbd;backdrop-filter:blur(3px)}.mobile-more-backdrop.show{display:block}.mobile-more{position:fixed;left:10px;right:10px;bottom:84px;z-index:52;background:linear-gradient(180deg,#111e32,#091321);border:1px solid #2a405e;border-radius:22px;padding:10px;box-shadow:0 22px 70px #000c}.mobile-more.show{display:block}.mobile-more-head{display:flex;justify-content:space-between;align-items:center;padding:5px 7px 9px}.mobile-more-head b{font-size:13px}.mobile-more-head button{border:0;background:#ffffff0a;color:white;width:30px;height:30px;border-radius:10px;font-size:20px}.mobile-more>button:not(.mobile-more-head button){width:100%;text-align:left;border:0;border-top:1px solid #ffffff0a;background:transparent;color:white;padding:11px 8px;display:grid;gap:3px}.mobile-more>button b{font-size:11px}.mobile-more>button span{font-size:9px;color:#8fa1ba}}
@media(max-width:390px){.dexgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.games{grid-template-columns:1fr}.game-progress-list{grid-template-columns:1fr}.metric-grid{grid-template-columns:1fr 1fr}.brand .tiny{max-width:165px}}
'''
if 'Living Dex Hub UI 1.1' not in html:
    html = html.replace('</style>', ui_css + '\n</style>', 1)

ui_js = r'''
// Living Dex Hub UI 1.1 — navigation only; collection logic remains frozen.
function closeMobileMore(){const m=document.getElementById('mobileMore'),b=document.getElementById('mobileMoreBackdrop');if(m){m.classList.remove('show');m.setAttribute('aria-hidden','true')}if(b)b.classList.remove('show')}
function toggleMobileMore(ev){if(ev)ev.stopPropagation();const m=document.getElementById('mobileMore'),b=document.getElementById('mobileMoreBackdrop');if(!m)return;const open=!m.classList.contains('show');closeMobileMore();if(open){m.classList.add('show');m.setAttribute('aria-hidden','false');if(b)b.classList.add('show')}}
function syncMobileNav(v){const main=['home','games','global','missing'];document.querySelectorAll('.mnav-item').forEach(x=>x.classList.toggle('active',x.dataset.v===v));const more=document.getElementById('mobileMoreBtn');if(more&&!main.includes(v))more.classList.add('active');closeMobileMore()}
'''
if 'Living Dex Hub UI 1.1 — navigation only' not in html:
    html = html.replace('function go(v){', ui_js + '\nfunction go(v){syncMobileNav(v);', 1)

required = ['living-dex-ui" content="1.1', 'class="mobile-nav"', 'function syncMobileNav(v)', 'Living Dex Hub UI 1.1', 'Core 1.0 • UI 1.1 • Offline']
missing=[x for x in required if x not in html]
if missing:
    raise SystemExit('UI 1.1 incompleta: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'UI 1.1 aplicada: {HTML} • {HTML.stat().st_size} bytes')

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html'
html = HTML.read_text(encoding='utf-8')

html = html.replace('<meta name="living-dex-ui" content="1.1"/>', '<meta name="living-dex-ui" content="1.2"/>', 1)
html = html.replace('Core 1.0 • UI 1.1 • Offline', 'Core 1.0 • UI 1.2 • Offline', 1)

css = r'''
/* Living Dex Hub UI 1.2 — screen-by-screen usability pass */
.screen-intro{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:8px 0 16px;padding:3px 2px}.screen-intro-copy{display:grid;gap:4px}.screen-eyebrow{font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#7595ba}.screen-intro h2{margin:0;font-size:25px;letter-spacing:-.035em}.screen-intro p{margin:0;max-width:720px;color:#91a5bf;font-size:11px;line-height:1.55}.screen-actions{display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end}.screen-action{border:1px solid #2a4262;background:#0d192a;color:#dce8f6;border-radius:12px;padding:9px 11px;font-size:9px;font-weight:750;cursor:pointer;min-height:38px}.screen-action:hover{border-color:#5579a1;background:#14243a}
.quick-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin:0 0 16px}.quick-tile{appearance:none;border:1px solid #223a59;background:linear-gradient(145deg,#102039,#0b1626);color:#eef5ff;border-radius:16px;padding:12px;text-align:left;display:grid;gap:4px;cursor:pointer;min-height:68px}.quick-tile b{font-size:11px}.quick-tile span{font-size:9px;color:#879bb5;line-height:1.35}.quick-tile:hover{border-color:#4d719a;transform:translateY(-1px)}
.dex-switch{display:flex;gap:7px;margin:0 0 11px}.dex-switch button{appearance:none;border:1px solid #263d5b;background:#0b1728;color:#91a5bf;border-radius:12px;padding:8px 11px;font-size:9px;font-weight:800;cursor:pointer}.dex-switch button.on{background:#f4f7fb;color:#09121f;border-color:#f4f7fb}
.view[data-ui12-ready="1"]>.note:first-of-type{margin-top:0}.pk{content-visibility:auto;contain-intrinsic-size:127px}.pk,.game,.family-card,.metric,.btn,.screen-action,.quick-tile,.mnav-item{touch-action:manipulation}.sheet-head{position:sticky;top:-1px;z-index:6;background:linear-gradient(180deg,#111d31 78%,#111d3100);padding-top:2px;padding-bottom:7px}.sheet .detailgrid{align-items:start}.sheet img{max-width:100%}.sheet button,.sheet select,.sheet input,.sheet textarea{min-height:40px}
@media(max-width:700px){.screen-intro{align-items:flex-start;margin:3px 0 12px}.screen-intro h2{font-size:21px}.screen-intro p{font-size:10px;max-width:95%}.screen-actions{display:none}.quick-strip{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-bottom:12px}.quick-tile{padding:10px;min-height:62px;border-radius:14px}.quick-tile b{font-size:10px}.quick-tile span{font-size:8px}.dex-switch{position:sticky;top:57px;z-index:11;background:#07101be8;margin:0 -2px 8px;padding:6px 2px;backdrop-filter:blur(10px)}.dex-switch button{flex:1;min-height:40px}.sheet{padding-bottom:max(20px,env(safe-area-inset-bottom))}.sheet-head{top:-14px;padding-top:13px}.btn,.tab,.screen-action,.quick-tile,.mnav-item,.mobile-more>button{min-height:44px}.pk{content-visibility:auto;contain-intrinsic-size:128px}}
'''
if 'Living Dex Hub UI 1.2' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
// Living Dex Hub UI 1.2 — contextual headers and shortcuts; Core logic untouched.
const UI12_SCREENS={
 home:['Visão geral','Seu progresso, próximos passos e visão rápida da coleção.'],
 games:['Jogos','Escolha um jogo e acompanhe as Pokédexes que fazem parte da sua coleção.'],
 global:['National Dex','Acompanhe as 1.025 espécies e registre sua Living Dex principal.'],
 missing:['Faltando','Veja somente o que ainda falta e encontre rapidamente o próximo alvo.'],
 families:['Famílias evolutivas','Confira linhas evolutivas completas e identifique lacunas na família.'],
 planner:['Planejamento','Organize capturas e evoluções que você decidiu fazer depois.'],
 forms:['Form Dex','Acompanhe formas colecionáveis separadamente da National Dex principal.'],
 storage:['Storage & HOME','Registre onde cada exemplar está guardado e de qual jogo ele veio.'],
 settings:['Configurações','Backup, snapshots, integridade dos dados e opções de sincronização.']
};
function ui12Intro(viewId){
 const v=document.getElementById(viewId); if(!v||v.dataset.ui12Ready==='1')return;
 const info=UI12_SCREENS[viewId]; if(!info)return;
 const intro=document.createElement('div'); intro.className='screen-intro';
 intro.innerHTML=`<div class="screen-intro-copy"><span class="screen-eyebrow">Living Dex Hub</span><h2>${info[0]}</h2><p>${info[1]}</p></div><div class="screen-actions"><button class="screen-action" onclick="go('global')">National Dex</button><button class="screen-action" onclick="go('missing')">Faltando</button><button class="screen-action" onclick="go('storage')">Storage</button></div>`;
 v.insertBefore(intro,v.firstChild); v.dataset.ui12Ready='1';
 if(viewId==='home')ui12HomeShortcuts(v);
 if(viewId==='global'||viewId==='missing')ui12DexSwitch(v,viewId);
}
function ui12HomeShortcuts(v){
 const row=document.createElement('div'); row.className='quick-strip';
 row.innerHTML=`<button class="quick-tile" onclick="go('global')"><b>Abrir National Dex</b><span>Continue marcando sua coleção.</span></button><button class="quick-tile" onclick="go('missing')"><b>Ver o que falta</b><span>Vá direto para espécies pendentes.</span></button><button class="quick-tile" onclick="go('games')"><b>Pokédexes por jogo</b><span>Veja progresso por versão e DLC.</span></button><button class="quick-tile" onclick="go('storage')"><b>Localizar exemplares</b><span>Confira box, HOME e origem.</span></button>`;
 const intro=v.querySelector('.screen-intro'); intro.insertAdjacentElement('afterend',row);
}
function ui12DexSwitch(v,active){
 const row=document.createElement('div'); row.className='dex-switch';
 row.innerHTML=`<button class="${active==='global'?'on':''}" onclick="go('global')">Todos</button><button class="${active==='missing'?'on':''}" onclick="go('missing')">Somente faltando</button>`;
 const intro=v.querySelector('.screen-intro'); intro.insertAdjacentElement('afterend',row);
}
function ui12Ensure(){Object.keys(UI12_SCREENS).forEach(ui12Intro)}
setTimeout(ui12Ensure,0);
'''
if 'Living Dex Hub UI 1.2 — contextual headers' not in html:
    html = html.replace('function closeMobileMore(){', js + '\nfunction closeMobileMore(){', 1)

# Whenever the app changes views, ensure the contextual UI is present and current.
html = html.replace('function go(v){syncMobileNav(v);', 'function go(v){ui12Ensure();syncMobileNav(v);', 1)

required=['living-dex-ui" content="1.2','Living Dex Hub UI 1.2','UI12_SCREENS','quick-strip','dex-switch','function ui12Ensure()','Core 1.0 • UI 1.2 • Offline']
missing=[x for x in required if x not in html]
if missing: raise SystemExit('UI 1.2 incompleta: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'UI 1.2 aplicada: {HTML} • {HTML.stat().st_size} bytes')

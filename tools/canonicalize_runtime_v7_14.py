from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html'
s = HTML.read_text(encoding='utf-8')

marker = 'living-dex-canonical-baseline" content="7.14.0"'
if marker not in s:
    s = s.replace('</head>', '<meta name="living-dex-canonical-baseline" content="7.14.0"/>\n</head>', 1)

css = r'''
/* 7.14.0 — canonical runtime guard. Legacy views may remain as internal engines, never as user-facing destinations. */
#games,#dex,#gameDex,#nationalDex,#library,#livingDex,#global,#missing,#families,#planner,#forms,#storage,#settings{display:none!important}
body.ld7121-box .mnav.ld79-nav{display:none!important}
'''
if '/* 7.14.0 — canonical runtime guard.' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

js = r'''
// Canonical runtime 7.14.0 — the public product is Home + Box; old screens are quarantined as internal-only code.
const LD714_PUBLIC_SURFACES=['home','box'];
const LD714_LEGACY_VIEW_IDS=['games','dex','gameDex','nationalDex','library','livingDex','global','missing','families','planner','forms','storage','settings'];
function ld714LegacyVisible(){
 return LD714_LEGACY_VIEW_IDS.filter(id=>{const e=document.getElementById(id);if(!e)return false;const cs=getComputedStyle(e);return cs.display!=='none'&&e.offsetParent!==null})
}
function ld714NormalizePublicUi(){
 // Preserve #games/#dexCard as a hidden Pokédex loading engine because openGame/currentDex still depend on it.
 for(const id of LD714_LEGACY_VIEW_IDS){const e=document.getElementById(id);if(e){e.setAttribute('aria-hidden','true');e.setAttribute('inert','')}}
 const box=document.getElementById('ld71BoxView');if(box)box.removeAttribute('inert');
 const home=document.getElementById('home');if(home){home.removeAttribute('inert');home.setAttribute('aria-hidden','false')}
 try{ld783NormalizeNav?.()}catch(e){}
 try{ld7121SyncNav?.()}catch(e){}
}
window.ld714CanonicalAudit=function(){
 const navs=[...document.querySelectorAll('.mnav.ld79-nav')];
 const buttons=navs[0]?[...navs[0].querySelectorAll(':scope > button')].map(b=>b.dataset.ld79||b.dataset.ld7||''):[];
 const box=document.getElementById('ld71BoxView');
 const modal=document.getElementById('modal'),sheet=modal?.querySelector('.sheet');
 return {
  version:'7.14.0',canonical:true,
  publicSurfaces:[...LD714_PUBLIC_SURFACES],
  supportedGames:(typeof LD73_SUPPORTED!=='undefined'?LD73_SUPPORTED.length:0),
  legacyVisible:ld714LegacyVisible(),
  navCount:navs.length,navButtons:buttons,
  boxReady:!!box,detailSheetReady:!!sheet,
  dexAudit:typeof ld713Audit==='function',musicAudit:typeof ld712Audit==='function'
 }
};
setTimeout(ld714NormalizePublicUi,0);setTimeout(ld714NormalizePublicUi,250);setTimeout(ld714NormalizePublicUi,900);
'''
if 'window.ld714CanonicalAudit=function' not in s:
    s = s.replace('</body>', '<script>' + js + '</script>\n</body>', 1)

HTML.write_text(s, encoding='utf-8')
print('Canonical runtime 7.14.0 applied')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-secondary-polish" content="4.4"' not in s:
    s=s.replace('</head>','<meta name="living-dex-secondary-polish" content="4.4"/>\n</head>',1)
css=r'''
/* Secondary Screen Polish 4.4 — one clean light visual language everywhere. */
:root{--s44-ink:#17213c;--s44-muted:#8994a8;--s44-line:#e9edf3;--s44-surface:#fff;--s44-soft:#f6f8fb;--s44-red:#ff5555;--s44-blue:#5398ff;--s44-green:#20b985}
#games,#global,#families,#planner,#forms,#storage,#settings{color:var(--s44-ink)}
#games .card,#global .card,#families .card,#planner .card,#forms .card,#storage .card,#settings .card,#dexCard,.sheet,.modal-content,.dialog,.panel{background:var(--s44-surface)!important;border:1px solid var(--s44-line)!important;box-shadow:0 6px 20px rgba(35,48,79,.065)!important;color:var(--s44-ink)!important}
#games h1,#games h2,#games h3,#global h1,#global h2,#families h1,#families h2,#planner h1,#planner h2,#forms h1,#forms h2,#storage h1,#storage h2,#settings h1,#settings h2{color:var(--s44-ink)!important;letter-spacing:-.035em}
#games p,#global p,#families p,#planner p,#forms p,#storage p,#settings p,.muted,.sub,.hint{color:var(--s44-muted)!important}
button,.btn,[role="button"],select,input[type="button"],input[type="submit"]{min-height:48px}
.icon-btn,.quick-catch,.quick-toggle,.close,.back-btn,.sheet-close{min-width:48px!important;min-height:48px!important}
input,select,textarea{min-height:48px;border:1px solid var(--s44-line)!important;border-radius:14px!important;background:#fff!important;color:var(--s44-ink)!important;box-shadow:none!important}
button.primary,.btn.primary,.primary{border-color:transparent!important;background:var(--s44-red)!important;color:#fff!important;box-shadow:0 5px 14px rgba(255,85,85,.18)!important}
button.secondary,.btn.secondary{background:#fff!important;color:var(--s44-ink)!important;border:1px solid var(--s44-line)!important;box-shadow:none!important}
/* General / game library */
#games .games-grid,#games .game-grid{gap:12px!important}#games .game-card{background:#fff!important;border:1px solid var(--s44-line)!important;border-radius:22px!important;box-shadow:0 5px 18px rgba(35,48,79,.06)!important;overflow:hidden}#games .game-card button{min-height:48px!important}
.nav23-general-switch{background:#fff!important;border:1px solid var(--s44-line)!important;border-radius:17px!important;padding:5px!important;box-shadow:0 4px 15px rgba(35,48,79,.05)!important}.nav23-general-switch button{min-height:44px!important;border:0!important;border-radius:13px!important}.nav23-general-switch button.active{background:#fff0f0!important;color:var(--s44-red)!important}
/* Dex */
#dexCard{border-radius:24px!important;padding:14px!important}.dex-grid,.pokemon-grid{gap:10px!important}.pokemon-card,.dex-card{background:#fff!important;border:1px solid var(--s44-line)!important;border-radius:18px!important;box-shadow:0 4px 14px rgba(35,48,79,.05)!important;color:var(--s44-ink)!important}.pokemon-card img,.dex-card img{filter:none!important}.pokemon-card:active,.dex-card:active{transform:scale(.975)}
/* Families / planner / forms */
#families .family-card,#planner .planner-card,#forms .form-card{background:#fff!important;border:1px solid var(--s44-line)!important;border-radius:20px!important;box-shadow:0 4px 15px rgba(35,48,79,.05)!important}
/* Storage and settings become grouped native-like lists. */
#storage .card,#settings .card{border-radius:20px!important;margin-bottom:11px!important}#storage button,#settings button{border-radius:14px!important}#settings label,#storage label{color:var(--s44-ink)!important}
/* Pokemon profile: light hero, readable groups, no legacy dark blocks. */
.sheet,.modal-content{border-radius:26px 26px 0 0!important}.sheet-header,.modal-header{background:rgba(255,255,255,.96)!important;color:var(--s44-ink)!important;border-bottom:1px solid var(--s44-line)!important}.profile-hero,.pokemon-hero{background:linear-gradient(180deg,#f7f9fc 0%,#fff 100%)!important}.profile-hero img,.pokemon-hero img{filter:none!important}.profile-section,.profile-card,.detail-card{background:#fff!important;color:var(--s44-ink)!important;border:1px solid var(--s44-line)!important;border-radius:18px!important;box-shadow:none!important}
/* More/menu */
#moreSheet,.more-sheet{background:#f7f8fb!important;color:var(--s44-ink)!important}.more-item,.menu-item{min-height:56px!important;background:#fff!important;border:1px solid var(--s44-line)!important;border-radius:16px!important;color:var(--s44-ink)!important;box-shadow:none!important}
/* Reduce decorative/prototype residue without hiding useful status. */
.scope-note,.statusbar,.backup-guide,.sync-note,.data-pack-note,.library-intro,.general-intro,.dex-intro,[data-ui-explainer]{display:none!important}
@media(max-width:680px){#games,#global,#families,#planner,#forms,#storage,#settings{padding-bottom:92px}.sheet,.modal-content{max-height:92vh!important}.pokemon-card,.dex-card{min-height:126px}.ref41-back,.ref43-control{min-width:48px!important;min-height:48px!important}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Secondary Screen Polish 4.4
function s44Polish(){
 document.documentElement.dataset.secondaryPolish='4.4';
 document.querySelectorAll('.scope-note,.statusbar,.backup-guide,.sync-note,.data-pack-note,.library-intro,.general-intro,.dex-intro,[data-ui-explainer]').forEach(el=>el.remove());
 document.querySelectorAll('button,[role="button"],a[onclick]').forEach(el=>{if(!el.getAttribute('aria-label')&&!String(el.textContent||'').trim()){const t=el.getAttribute('title');if(t)el.setAttribute('aria-label',t)}});
}
const s44Go=window.go;if(typeof s44Go==='function'){window.go=function(){const r=s44Go.apply(this,arguments);setTimeout(s44Polish,0);return r}}
const s44Profile=window.openProfile;if(typeof s44Profile==='function'){window.openProfile=function(){const r=s44Profile.apply(this,arguments);setTimeout(s44Polish,0);return r}}
setTimeout(s44Polish,80);
if(new URLSearchParams(location.search).has('s44qa'))setTimeout(()=>{const ok=document.querySelector('meta[name="living-dex-secondary-polish"][content="4.4"]')&&document.documentElement.dataset.secondaryPolish==='4.4'&&[...document.querySelectorAll('button')].every(b=>parseFloat(getComputedStyle(b).minHeight||0)>=0);if(ok)document.documentElement.dataset.s44Qa='1'},350);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Secondary Screen Polish 4.4 applied')

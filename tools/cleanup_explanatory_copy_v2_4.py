from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-clean-copy" content="2.4"' not in s:
    s=s.replace('</head>','<meta name="living-dex-clean-copy" content="2.4"/>\n</head>',1)
css=r'''
/* 2.4 — cleaner native-style information hierarchy */
.ui24-explainer-hidden{display:none!important}
#home .section-head p,#games .section-head p,#global .section-head p,#families .section-head p,#planner .section-head p,#forms .section-head p,#storage .section-head p,#settings .section-head p{display:none!important}
#games .library-intro,#games .general-intro,#global .dex-intro,.nav21-focusbar small,.nav23-general-head p{display:none!important}
'''
if '/* 2.4 — cleaner native-style information hierarchy */' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// 2.4 — remove interface self-explanations while preserving actionable guidance and game data.
function ui24CleanExplanatoryCopy(root=document){
 const scopes=['#home','#games','#global','#families','#planner','#forms','#storage','#settings'];
 scopes.forEach(sel=>{
  const box=root.querySelector?.(sel); if(!box)return;
  box.querySelectorAll('.section-head p,.library-intro,.general-intro,.dex-intro,.nav23-general-head p').forEach(el=>el.classList.add('ui24-explainer-hidden'));
 });
 // Hide only generic UI-help prose; do not touch Journey, Pokémon profiles, status, warnings or acquisition guidance.
 root.querySelectorAll('[data-ui-explainer]').forEach(el=>el.classList.add('ui24-explainer-hidden'));
}
const ui24BaseGo=window.go;
window.go=function(v){const r=ui24BaseGo.apply(this,arguments);setTimeout(()=>ui24CleanExplanatoryCopy(),0);return r};
const ui24BaseHome=window.renderActiveGameHome;
if(typeof ui24BaseHome==='function')window.renderActiveGameHome=function(){const r=ui24BaseHome.apply(this,arguments);setTimeout(()=>ui24CleanExplanatoryCopy(),0);return r};
setTimeout(()=>ui24CleanExplanatoryCopy(),0);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Clean explanatory copy 2.4 applied')

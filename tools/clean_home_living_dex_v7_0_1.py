from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-clean" content="7.0.1"' not in s:s=s.replace('</head>','<meta name="living-dex-home-clean" content="7.0.1"/>\n</head>',1)
css=r'''
/* 7.0.1 — Home contains only the selected game and its Living Dex entry point. */
#home [class*="journey"],#home [id*="journey"],#home [class*="Journey"],#home [id*="Journey"]{display:none!important}
#home .home51-journey,#home .home232-journey,#home .home-journey-summary,#home .home-journey-card{display:none!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
function ld701CleanHome(){
 const h=document.getElementById('home');if(!h)return;
 // Remove legacy Journey surfaces by structure and copy, including nodes injected after initial render.
 h.querySelectorAll('[class*="journey"],[id*="journey"],[class*="Journey"],[id*="Journey"]').forEach(x=>x.remove());
 [...h.querySelectorAll('section,article,div,button,a')].forEach(el=>{
   const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').trim();
   const txt=(el.textContent||'').trim();
   if((/^Jornada$/i.test(own)||/^(Abrir|Continuar|Ver) Jornada$/i.test(txt))&&!el.closest('.playing-card'))el.remove();
 });
 const c=h.querySelector('.home51-cta');if(c){c.textContent='Abrir Living Dex';c.onclick=ld7OpenCurrent}
 const card=h.querySelector('.playing-card');if(card)card.onclick=e=>{if(e.target.closest('button'))return;ld7OpenCurrent()};
}
const ld701Render=window.renderActiveGameHome;if(typeof ld701Render==='function')window.renderActiveGameHome=function(){const r=ld701Render.apply(this,arguments);setTimeout(ld701CleanHome,0);return r};
const ld701Audit=window.ld7Audit;if(typeof ld701Audit==='function')window.ld7Audit=function(){const r=ld701Audit.apply(this,arguments);ld701CleanHome();return r};
setTimeout(ld701CleanHome,0);setTimeout(ld701CleanHome,250);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Living Dex Home clean 7.0.1 applied')
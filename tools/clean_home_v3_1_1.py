from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-clean" content="3.1.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-home-clean" content="3.1.1"/>\n</head>',1)
css=r'''
/* Home clean 3.1.1 — content first, no interface narration */
#home .hero,#home>.hero,#home .home-current-head,#home .home-current-head+*,#home .home-intro,#home .home-heading,#home .home-kicker,#home .home-lead{display:none!important}
#home .home-current-shell{margin-top:4px!important}
#home .playing-card{margin-top:0!important}
'''
if '/* Home clean 3.1.1' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
function home311Clean(){
 const home=document.getElementById('home');if(!home)return;
 const phrases=['Seu progresso','Visão geral da sua coleção','JOGANDO AGORA','Continue de onde parou','Sem atalhos duplicados','Trocar jogo'];
 [...home.querySelectorAll('h1,h2,h3,h4,p,small,button,.eyebrow,.kicker')].forEach(el=>{
   const t=(el.textContent||'').trim();
   if(phrases.some(x=>t.toLowerCase().includes(x.toLowerCase()))){
     const parent=el.closest('.home-current-head,.hero,.home-intro,.home-heading')||el;
     parent.classList.add('ui24-explainer-hidden');
   }
 });
}
const home311Go=window.go;window.go=function(){const r=home311Go.apply(this,arguments);setTimeout(home311Clean,0);return r};
const home311Render=window.renderActiveGameHome;if(typeof home311Render==='function')window.renderActiveGameHome=function(){const r=home311Render.apply(this,arguments);setTimeout(home311Clean,0);return r};
setTimeout(home311Clean,0);
if(new URLSearchParams(location.search).has('home311qa'))setTimeout(()=>{
 home311Clean();const h=document.getElementById('home');const txt=(h?.innerText||'');
 const banned=['Seu progresso','Visão geral da sua coleção','JOGANDO AGORA','Continue de onde parou','Sem atalhos duplicados','Trocar jogo'];
 const visible=banned.some(x=>txt.includes(x));
 const current=!!h?.querySelector('.home-current-shell');
 const journey=!!h?.querySelector('.home232-journey,.home-journey-summary');
 document.documentElement.dataset.home311Qa=(!visible&&current&&journey)?'1':'0';
},1100);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Home clean 3.1.1 applied')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-single-journey" content="5.1.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-home-single-journey" content="5.1.1"/>\n</head>',1)
css=r'''
/* Home 5.1.1 — the approved home51 journey is the single journey block. */
#home .home232-journey,#home .home-journey-summary{display:none!important}
'''
if '/* Home 5.1.1' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Home 5.1.1 — neutralize the legacy renderer that was re-inserting a second Journey.
function home511RemoveLegacyJourney(){const home=document.getElementById('home');if(!home)return;home.querySelectorAll('.home232-journey,.home-journey-summary').forEach(x=>x.remove())}
window.home232RenderJourney=function(){home511RemoveLegacyJourney()};
const home511Render=window.renderActiveGameHome;if(typeof home511Render==='function'){window.renderActiveGameHome=function(){const r=home511Render.apply(this,arguments);home511RemoveLegacyJourney();return r}}
setTimeout(home511RemoveLegacyJourney,0);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Home duplicate Journey removed: 5.1.1')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
js=r'''
// Paldea 4.3 runtime QA.
if(new URLSearchParams(location.search).has('ref43qa')){setTimeout(()=>{try{state.activeGameId='sv';state.journey=state.journey||{};state.journey.sv=state.journey.sv||{starter:'sprigatito',done:[]};if(!Array.isArray(state.journey.sv.done))state.journey.sv.done=[];ref42Open('map');setTimeout(()=>{const page=document.getElementById('ref42MapPage'),nodes=page?.querySelectorAll('.geo-node')||[],controls=page?.querySelectorAll('.ref43-controls button')||[];const before=ref43Zoom;ref43ZoomBy(.35);ref43Point(1);const detail=document.getElementById('ref43Detail');const ok=page&&!page.hidden&&!!page.querySelector('.ref43-mapviewport')&&nodes.length===18&&controls.length===3&&ref43Zoom>before&&detail?.classList.contains('open')&&detail.textContent.includes('Lv.15');document.documentElement.dataset.ref43Qa=ok?'1':'0'},300)}catch(e){document.documentElement.dataset.ref43Qa='0'}},500)}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Paldea 4.3 runtime QA patched')
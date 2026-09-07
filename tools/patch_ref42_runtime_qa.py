from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
js=r'''
// Dedicated Journey 4.2 browser QA — verifies each card opens an exclusive full page.
if(new URLSearchParams(location.search).get('ref42qa')==='1'){
 setTimeout(()=>{
  try{
   state.activeGameId='sv'; if(typeof renderActiveGameHome==='function')renderActiveGameHome();
   ref42Open('route'); const route=!document.getElementById('ref42RoutePage').hidden&&document.getElementById('ref42TeamPage').hidden&&document.getElementById('ref42MapPage').hidden;
   const routeRows=document.querySelectorAll('#ref42RoutePage .ref42-step').length===18;
   ref42Open('team'); const team=!document.getElementById('ref42TeamPage').hidden&&document.getElementById('ref42RoutePage').hidden&&document.getElementById('ref42MapPage').hidden&&!!document.querySelector('#ref42TeamPage .ref42-teamgrid');
   ref42Open('map'); const map=!document.getElementById('ref42MapPage').hidden&&document.getElementById('ref42RoutePage').hidden&&document.getElementById('ref42TeamPage').hidden&&!!document.querySelector('#ref42MapPage .paldea-map');
   const fixed=getComputedStyle(document.getElementById('ref42MapPage')).position==='fixed';
   document.documentElement.dataset.ref42Qa=(route&&routeRows&&team&&map&&fixed)?'1':'0';
  }catch(e){document.documentElement.dataset.ref42Qa='0'}
 },1200)
}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Dedicated Journey 4.2 runtime QA added')
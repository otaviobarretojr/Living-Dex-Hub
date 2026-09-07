from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
js=r'''
// Reference 4.0 QA context only — deterministic Scarlet/Violet Home for browser validation.
if(new URLSearchParams(location.search).has('r4qa')){
 setTimeout(()=>{
   if(typeof state==='object'){
     state.activeGameId='sv';
     try{if(typeof persist==='function')persist()}catch(_e){}
     try{if(typeof renderActiveGameHome==='function')renderActiveGameHome()}catch(_e){}
     try{if(typeof home232RenderJourney==='function')home232RenderJourney()}catch(_e){}
     try{if(typeof r4Apply==='function')r4Apply()}catch(_e){}
   }
   document.documentElement.dataset.r4QaSetup='1';
 },120);
}
'''
if 'data-r4-qa-setup' not in s and 'r4QaSetup' not in s:
    s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Reference UI 4.0 runtime QA context fixed')

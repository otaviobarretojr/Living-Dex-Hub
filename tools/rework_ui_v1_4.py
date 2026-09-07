from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')
html=html.replace('<meta name="living-dex-ui" content="1.3"/>','<meta name="living-dex-ui" content="1.4"/>',1)
html=html.replace('Core 1.0 • UI 1.3 • Offline','Core 1.0 • UI 1.4 • Offline',1)
js=r'''
// Living Dex Hub UI 1.4 — Android back bridge.
function androidHandleBack(){
 const modal=document.getElementById('modal');
 if(modal&&modal.classList.contains('show')){closeModal();return true}
 const more=document.getElementById('mobileMore');
 if(more&&more.classList.contains('show')){closeMobileMore();return true}
 return false
}
'''
if 'Living Dex Hub UI 1.4 — Android back bridge.' not in html:
    html=html.replace('function closeMobileMore(){',js+'\nfunction closeMobileMore(){',1)
required=['living-dex-ui" content="1.4','function androidHandleBack()','closeModal();return true','closeMobileMore();return true','Core 1.0 • UI 1.4 • Offline']
missing=[x for x in required if x not in html]
if missing: raise SystemExit('UI 1.4 incompleta: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'UI 1.4 aplicada: {HTML} • {HTML.stat().st_size} bytes')

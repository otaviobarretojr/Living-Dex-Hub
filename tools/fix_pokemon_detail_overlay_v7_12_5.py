from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
marker='living-dex-detail-overlay-fix" content="7.12.5"'
if marker in s:
 print('Pokemon detail overlay fix 7.12.5 already applied'); raise SystemExit
s=s.replace('</head>','<meta name="living-dex-detail-overlay-fix" content="7.12.5"/>\n</head>',1)
css=r'''
/* 7.12.5 — keep Pokemon detail sheet visible; hide only the two obsolete controls. */
#modal .sheet.ld7124-hidden,#modal .sheet .poke-profile.ld7124-hidden,#modal .sheet .ld76-evo.ld7124-hidden{display:block!important}
#modal textarea{display:none!important}
#modal .ld7125-observation,#modal .ld7125-journey{display:none!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Pokemon detail overlay fix 7.12.5
function ld7125FixDetail(){
 const modal=document.getElementById('modal');if(!modal)return;
 const sheet=modal.querySelector('.sheet');
 if(sheet)sheet.classList.remove('ld7124-hidden');
 // Undo any over-broad 7.12.4 hiding first, then hide only exact obsolete elements.
 modal.querySelectorAll('.ld7124-hidden').forEach(el=>el.classList.remove('ld7124-hidden'));
 modal.querySelectorAll('textarea').forEach(t=>{
   t.classList.add('ld7125-observation');
   const p=t.parentElement;
   if(p && p.children.length<=2 && !p.classList.contains('sheet')) p.classList.add('ld7125-observation');
 });
 modal.querySelectorAll('button,a,[role="button"]').forEach(el=>{
   const txt=(el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
   if(txt.includes('abrir jornada') || (txt.includes('jornada')&&txt.includes('time')&&txt.includes('mapa'))) el.classList.add('ld7125-journey');
 });
}
const ld7125OldOpen=window.openPokemon;
if(typeof ld7125OldOpen==='function')window.openPokemon=function(){
 const r=ld7125OldOpen.apply(this,arguments);setTimeout(ld7125FixDetail,0);setTimeout(ld7125FixDetail,120);return r;
};
const ld7125OldBoxOpen=window.ld74OpenPokemon;
if(typeof ld7125OldBoxOpen==='function')window.ld74OpenPokemon=function(){
 const r=ld7125OldBoxOpen.apply(this,arguments);setTimeout(ld7125FixDetail,0);setTimeout(ld7125FixDetail,120);return r;
};
window.ld7125Audit=function(){
 const modal=document.getElementById('modal'),sheet=modal?.querySelector('.sheet');
 const sheetVisible=!!sheet&&getComputedStyle(sheet).display!=='none'&&sheet.getBoundingClientRect().height>0;
 const visibleTextareas=[...(modal?.querySelectorAll('textarea')||[])].filter(x=>getComputedStyle(x).display!=='none').length;
 const visibleJourney=[...(modal?.querySelectorAll('button,a,[role="button"]')||[])].filter(el=>{const t=(el.textContent||'').toLowerCase();return (t.includes('abrir jornada')||(t.includes('jornada')&&t.includes('time')&&t.includes('mapa'))) && getComputedStyle(el).display!=='none'}).length;
 return {version:'7.12.5',sheetVisible,visibleObservationFields:visibleTextareas,visibleJourneyCtas:visibleJourney};
};
setTimeout(ld7125FixDetail,220);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Pokemon detail overlay fix 7.12.5 applied')

from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
marker='living-dex-detail-cleanup" content="7.12.4"'
if marker in s:
 print('Pokemon detail cleanup 7.12.4 already applied'); raise SystemExit
s=s.replace('</head>','<meta name="living-dex-detail-cleanup" content="7.12.4"/>\n</head>',1)
css=r'''
/* 7.12.4 — remove legacy observations and journey CTA from every Pokemon detail. */
#modal textarea{display:none!important}
#modal .ld7124-hidden{display:none!important}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Pokemon detail cleanup 7.12.4
function ld7124CleanDetail(){
 const modal=document.getElementById('modal');if(!modal)return;
 // Remove/hide the legacy observations textarea and its surrounding card when possible.
 modal.querySelectorAll('textarea').forEach(t=>{
  const wrap=t.closest('.note,.card,.panel,.section,.detail-card,.box')||t.parentElement;
  if(wrap&&wrap!==modal)wrap.classList.add('ld7124-hidden');else t.classList.add('ld7124-hidden');
 });
 // Remove any legacy CTA that opens Jornada / Time / Mapa from Pokemon details.
 modal.querySelectorAll('button,a,[role="button"]').forEach(el=>{
  const txt=(el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
  if(txt.includes('abrir jornada') || (txt.includes('jornada')&&txt.includes('time')&&txt.includes('mapa'))){
   const wrap=el.closest('.note,.card,.panel,.section,.detail-card,.box');
   (wrap||el).classList.add('ld7124-hidden');
  }
 });
}
const ld7124OldOpen=window.openPokemon;
if(typeof ld7124OldOpen==='function')window.openPokemon=function(){
 const r=ld7124OldOpen.apply(this,arguments);setTimeout(ld7124CleanDetail,0);return r;
};
const ld7124OldBoxOpen=window.ld74OpenPokemon;
if(typeof ld7124OldBoxOpen==='function')window.ld74OpenPokemon=function(){
 const r=ld7124OldBoxOpen.apply(this,arguments);setTimeout(ld7124CleanDetail,0);return r;
};
window.ld7124Audit=function(){
 const modal=document.getElementById('modal');
 const visibleTextareas=[...(modal?.querySelectorAll('textarea')||[])].filter(x=>getComputedStyle(x).display!=='none');
 const legacyCtas=[...(modal?.querySelectorAll('button,a,[role="button"]')||[])].filter(el=>{const t=(el.textContent||'').toLowerCase();return t.includes('abrir jornada')||(t.includes('jornada')&&t.includes('time')&&t.includes('mapa'))}).filter(x=>getComputedStyle(x).display!=='none');
 return {version:'7.12.4',visibleObservationFields:visibleTextareas.length,visibleJourneyCtas:legacyCtas.length};
};
setTimeout(ld7124CleanDetail,180);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Pokemon detail cleanup 7.12.4 applied')

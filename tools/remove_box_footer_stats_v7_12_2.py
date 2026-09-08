from pathlib import Path

p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
marker='living-dex-box-footer-cleanup" content="7.12.2"'
if marker in s:
    print('Box footer cleanup 7.12.2 already applied'); raise SystemExit

s=s.replace('</head>','<meta name="living-dex-box-footer-cleanup" content="7.12.2"/>\n</head>',1)
css=r'''
/* 7.12.2 — remove redundant per-Box footer summary from every game. */
#ld71BoxView .ld71-footerstats{display:none!important}
#ld71BoxView .ld71-panel{padding-bottom:16px}
'''
s=s.replace('</style>',css+'\n</style>',1)

js=r'''
// Box footer cleanup 7.12.2
function ld7122RemoveFooterStats(){
 document.querySelectorAll('#ld71BoxView .ld71-footerstats').forEach(el=>el.remove());
}
const ld7122OldRender=window.ld71Render;
if(typeof ld7122OldRender==='function')window.ld71Render=function(){
 const r=ld7122OldRender.apply(this,arguments);
 ld7122RemoveFooterStats();
 return r;
};
window.ld7122Audit=function(){
 return {
  version:'7.12.2',
  boxOpen:!!document.getElementById('ld71BoxView')?.classList.contains('active'),
  footerStats:document.querySelectorAll('#ld71BoxView .ld71-footerstats').length,
  footerHidden:getComputedStyle(document.querySelector('#ld71BoxView .ld71-footerstats')||document.createElement('div')).display==='none'
 };
};
setTimeout(ld7122RemoveFooterStats,250);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box footer cleanup 7.12.2 applied')

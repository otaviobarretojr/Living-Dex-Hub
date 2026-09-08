from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
marker='living-dex-box-viewport" content="7.12.3"'
if marker in s:
 print('Box viewport 7.12.3 already applied'); raise SystemExit
s=s.replace('</head>','<meta name="living-dex-box-viewport" content="7.12.3"/>\n</head>',1)
css=r'''
/* 7.12.3 — compact phone Box: keep all 30 slots visible in one viewport when height permits. */
@media (max-width:720px){
 #ld71BoxView{padding:calc(8px + env(safe-area-inset-top)) 14px calc(10px + env(safe-area-inset-bottom))!important}
 #ld71BoxView .ld71-head{margin-bottom:8px!important;gap:10px!important}
 #ld71BoxView .ld71-back{width:40px!important;height:40px!important;border-radius:13px!important}
 #ld71BoxView .ld71-cover{width:50px!important;height:67px!important;border-radius:11px!important}
 #ld71BoxView .ld71-game{gap:10px!important}
 #ld71BoxView .ld71-game h1{font-size:19px!important}
 #ld71BoxView .ld71-game p{margin-top:2px!important;font-size:11px!important}
 #ld71BoxView .ld71-progress{margin-top:4px!important;gap:8px!important;font-size:14px!important}
 #ld71BoxView .ld71-tabs{margin-bottom:8px!important;padding:4px!important;border-radius:17px!important}
 #ld71BoxView .ld72-games{min-height:42px!important;border-radius:13px!important;font-size:13px!important}
 #ld71BoxView .ld710-searchwrap{margin-bottom:8px!important;min-height:46px!important}
 #ld71BoxView .ld710-search{min-height:46px!important}
 #ld71BoxView .ld71-main{gap:8px!important}
 #ld71BoxView .ld71-boxlist{gap:6px!important;padding-bottom:2px!important}
 #ld71BoxView .ld71-boxitem{min-width:116px!important;padding:8px 10px!important;border-radius:15px!important;grid-template-columns:30px 1fr auto!important;gap:7px!important}
 #ld71BoxView .ld71-boxicon{width:30px!important;height:30px!important;border-radius:9px!important}
 #ld71BoxView .ld71-panel{padding:10px!important;border-radius:20px!important}
 #ld71BoxView .ld71-panelhead{margin-bottom:7px!important;gap:7px!important}
 #ld71BoxView .ld71-panelhead h2{font-size:19px!important}
 #ld71BoxView .ld71-arrow{width:34px!important;height:34px!important;border-radius:10px!important;font-size:19px!important}
 #ld71BoxView .ld71-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important;gap:5px!important}
 #ld71BoxView .ld71-slot{min-height:0!important;height:clamp(72px,9.4vh,88px)!important;padding:4px!important;border-radius:12px!important}
 #ld71BoxView .ld71-slot img{width:clamp(37px,5.3vh,48px)!important;height:clamp(37px,5.3vh,48px)!important}
 #ld71BoxView .ld71-num{top:4px!important;left:6px!important;font-size:8px!important}
 #ld71BoxView .ld71-name{font-size:8px!important;margin-top:0!important}
}
@media (max-width:720px) and (max-height:800px){
 #ld71BoxView .ld71-cover{width:44px!important;height:59px!important}
 #ld71BoxView .ld71-head{margin-bottom:6px!important}
 #ld71BoxView .ld71-tabs{margin-bottom:6px!important}
 #ld71BoxView .ld710-searchwrap{margin-bottom:6px!important}
 #ld71BoxView .ld71-slot{height:68px!important}
 #ld71BoxView .ld71-slot img{width:34px!important;height:34px!important}
}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box viewport audit 7.12.3
window.ld7123Audit=function(){
 const root=document.getElementById('ld71BoxView'),grid=root?.querySelector('.ld71-grid'),slots=[...(grid?.querySelectorAll('.ld71-slot')||[])];
 const last=slots[29], rr=root?.getBoundingClientRect(), lr=last?.getBoundingClientRect();
 return {version:'7.12.3',columns:grid?getComputedStyle(grid).gridTemplateColumns.split(' ').length:0,slots:slots.length,lastSlotVisible:!!(lr&&rr&&lr.bottom<=window.innerHeight+1),viewportHeight:window.innerHeight,lastBottom:lr?Math.round(lr.bottom):null};
};
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box viewport 7.12.3 applied')

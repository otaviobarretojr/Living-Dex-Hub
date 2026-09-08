from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-clean-card" content="7.5.1"' in s:
    print('Box clean card 7.5.1 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-box-clean-card" content="7.5.1"/>\n</head>',1)
css=r'''
/* 7.5.1 — clean Box cards: registration happens only inside Pokemon detail. */
.ld74-register{display:none!important}
.ld71-slot{padding-right:8px!important}
/* Six Pokemon per row: 30 slots = 6 columns x 5 rows. */
.ld71-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important;gap:6px!important}
.ld71-slot{min-height:92px!important;padding:6px 4px!important;border-radius:12px!important}
.ld71-slot img{width:44px!important;height:44px!important}
.ld71-num{top:5px!important;left:6px!important;font-size:7px!important}
.ld71-name{font-size:7px!important;line-height:1.05!important;margin-top:1px!important}
@media(min-width:721px){.ld71-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important}.ld71-slot{min-height:108px!important}.ld71-slot img{width:58px!important;height:58px!important}.ld71-name{font-size:9px!important}.ld71-num{font-size:8px!important}}
@media(max-width:390px){.ld71-grid{gap:4px!important}.ld71-slot{min-height:82px!important;padding:5px 3px!important}.ld71-slot img{width:39px!important;height:39px!important}.ld71-name{font-size:6.5px!important}}
'''
s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Box clean cards 7.5.1
function ld751CleanBoxCards(){
 const root=document.getElementById('ld71BoxView');if(!root)return;
 root.querySelectorAll('.ld74-register').forEach(el=>el.remove());
 root.querySelectorAll('.ld71-slot').forEach(slot=>{
   slot.title='Abrir informações do Pokémon';
   slot.setAttribute('aria-label',slot.getAttribute('aria-label')||'Abrir informações do Pokémon')
 })
}
const ld751OldRender=window.ld71Render;
window.ld71Render=function(){const r=ld751OldRender.apply(this,arguments);ld751CleanBoxCards();return r};
setTimeout(ld751CleanBoxCards,180)
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Box clean card 7.5.1 applied with 6-column layout')

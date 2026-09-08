from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-box-six-columns" content="7.5.2"' in s:
    print('Box six columns 7.5.2 already applied');raise SystemExit
s=s.replace('</head>','<meta name="living-dex-box-six-columns" content="7.5.2"/>\n</head>',1)
css=r'''
/* 7.5.2 — 30 Pokémon shown as 6 columns x 5 rows on phone. */
.ld71-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important;gap:6px!important}
.ld71-slot{min-height:92px!important;padding:6px 4px!important;border-radius:12px!important}
.ld71-slot img{width:44px!important;height:44px!important}
.ld71-num{top:5px!important;left:6px!important;font-size:7px!important}
.ld71-name{font-size:7px!important;line-height:1.05!important;margin-top:1px!important}
@media(min-width:721px){.ld71-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important}.ld71-slot{min-height:108px!important}.ld71-slot img{width:58px!important;height:58px!important}.ld71-name{font-size:9px!important}.ld71-num{font-size:8px!important}}
@media(max-width:390px){.ld71-grid{gap:4px!important}.ld71-slot{min-height:82px!important;padding:5px 3px!important}.ld71-slot img{width:39px!important;height:39px!important}.ld71-name{font-size:6.5px!important}}
'''
s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s,encoding='utf-8')
print('Box six columns 7.5.2 applied')

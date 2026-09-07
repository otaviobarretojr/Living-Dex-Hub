from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
html=HTML.read_text(encoding='utf-8')
html=html.replace('<meta name="living-dex-ui" content="1.2"/>','<meta name="living-dex-ui" content="1.3"/>',1)
html=html.replace('Core 1.0 • UI 1.2 • Offline','Core 1.0 • UI 1.3 • Offline',1)
css=r'''
/* Living Dex Hub UI 1.3 — Pokemon profile focus pass */
.sheet{overscroll-behavior:contain}.sheet-head{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid #ffffff0b}.sheet-head h2,.sheet-head h3{letter-spacing:-.025em}.sheet .detailgrid{gap:16px}.sheet .card{box-shadow:none}.sheet img{object-fit:contain;filter:drop-shadow(0 14px 24px #0007)}
.sheet .pill,.sheet .tag{white-space:nowrap}.sheet textarea{resize:vertical;min-height:88px}.sheet .btn{font-weight:750}.sheet-close{min-width:44px;min-height:44px}
@media(max-width:700px){.sheet{max-height:96dvh;padding:12px 12px max(92px,calc(20px + env(safe-area-inset-bottom)));border-radius:26px 26px 0 0}.sheet-head{margin:0 -2px 10px;padding:10px 2px 11px}.sheet .detailgrid{gap:10px}.sheet .card{padding:12px;border-radius:16px}.sheet img{max-height:210px}.sheet input,.sheet select,.sheet textarea,.sheet button{font-size:16px}.sheet textarea{min-height:96px}.sheet .btn{width:100%}.sheet .row{gap:8px}.sheet .row>.btn{flex:1}.sheet h2{font-size:21px}.sheet h3{font-size:15px}}
@media(max-width:390px){.sheet img{max-height:180px}.sheet{padding-left:10px;padding-right:10px}}
'''
if 'Living Dex Hub UI 1.3' not in html: html=html.replace('</style>',css+'\n</style>',1)
required=['living-dex-ui" content="1.3','Living Dex Hub UI 1.3','Core 1.0 • UI 1.3 • Offline','96dvh','overscroll-behavior:contain']
missing=[x for x in required if x not in html]
if missing: raise SystemExit('UI 1.3 incompleta: '+str(missing))
HTML.write_text(html,encoding='utf-8')
print(f'UI 1.3 aplicada: {HTML} • {HTML.stat().st_size} bytes')

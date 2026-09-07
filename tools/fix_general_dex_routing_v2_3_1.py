from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
old="window.nav23BaseGo=window.go;\nwindow.go=function(v){if(v==='games')return nav23OpenLibrary();if(v==='global')return nav23OpenNationalDex();return window.nav23BaseGo(v)};"
new="window.nav23BaseGo=window.go;\n// General 2.3.1: do not override the app's internal go(). Only explicit General/Library controls route to nav23OpenLibrary/nav23OpenNationalDex."
if old not in s:
    raise SystemExit('General routing block not found')
s=s.replace(old,new,1)
if 'living-dex-general-routing" content="2.3.1"' not in s:
    s=s.replace('</head>','<meta name="living-dex-general-routing" content="2.3.1"/>\n</head>',1)
p.write_text(s,encoding='utf-8')
print('General routing 2.3.1 applied — internal game Dex navigation preserved')

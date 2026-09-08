from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app/src/main/assets/index.html'
s=HTML.read_text(encoding='utf-8')

marker='living-dex-design-phase" content="F1-home-premium"'
if marker not in s:
    s=s.replace('</head>','<meta name="living-dex-design-phase" content="F1-home-premium"/>\n</head>',1)

css_tags='''<link rel="stylesheet" href="design-system-v8.css" data-ld8="design-system"/>\n<link rel="stylesheet" href="home-v8.css" data-ld8="home-f1"/>\n'''
if 'data-ld8="design-system"' not in s:
    s=s.replace('</head>',css_tags+'</head>',1)

js_tag='<script src="home-v8.js" data-ld8="home-f1"></script>\n'
if 'src="home-v8.js"' not in s:
    s=s.replace('</body>',js_tag+'</body>',1)

HTML.write_text(s,encoding='utf-8')
print('Phase F1 premium Home assets injected')

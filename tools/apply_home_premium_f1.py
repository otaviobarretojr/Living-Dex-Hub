from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app/src/main/assets/index.html'
s=HTML.read_text(encoding='utf-8')

marker='living-dex-design-phase" content="F1-home-premium"'
if marker not in s:
    s=s.replace('</head>','<meta name="living-dex-design-phase" content="F1-home-premium"/>\n</head>',1)
if 'living-dex-shell" content="F1.1-fullscreen-dock"' not in s:
    s=s.replace('</head>','<meta name="living-dex-shell" content="F1.1-fullscreen-dock"/>\n</head>',1)
if 'living-dex-game-context" content="F1.3-primary-vs-consultation"' not in s:
    s=s.replace('</head>','<meta name="living-dex-game-context" content="F1.3-primary-vs-consultation"/>\n</head>',1)

css_tags='''<link rel="stylesheet" href="design-system-v8.css" data-ld8="design-system"/>\n<link rel="stylesheet" href="home-v8.css" data-ld8="home-f1"/>\n<link rel="stylesheet" href="shell-v8.css" data-ld8="shell-f11"/>\n'''
if 'data-ld8="design-system"' not in s:
    s=s.replace('</head>',css_tags+'</head>',1)
elif 'data-ld8="shell-f11"' not in s:
    s=s.replace('</head>','<link rel="stylesheet" href="shell-v8.css" data-ld8="shell-f11"/>\n</head>',1)

context_tag='<script src="game-context-v8.js" data-ld8="game-context-f13"></script>\n'
home_tag='<script src="home-v8.js" data-ld8="home-f1"></script>\n'
if 'src="game-context-v8.js"' not in s:
    s=s.replace('</body>',context_tag+'</body>',1)
if 'src="home-v8.js"' not in s:
    s=s.replace('</body>',home_tag+'</body>',1)

HTML.write_text(s,encoding='utf-8')
print('Phase F1.3 premium Home + explicit primary/consultation game context injected')

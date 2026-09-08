from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app/src/main/assets/index.html';s=HTML.read_text(encoding='utf-8')
markers=[('living-dex-design-phase" content="F1-home-premium"','<meta name="living-dex-design-phase" content="F1-home-premium"/>'),('living-dex-shell" content="F1.1-fullscreen-dock"','<meta name="living-dex-shell" content="F1.1-fullscreen-dock"/>'),('living-dex-game-context" content="F1.3-primary-vs-consultation"','<meta name="living-dex-game-context" content="F1.3-primary-vs-consultation"/>'),('living-dex-game-selector" content="F2-explicit-primary"','<meta name="living-dex-game-selector" content="F2-explicit-primary"/>'),('living-dex-context-architecture" content="F2.5-independent"','<meta name="living-dex-context-architecture" content="F2.5-independent"/>'),('living-dex-pokemon-detail" content="F3-detail-2.0"','<meta name="living-dex-pokemon-detail" content="F3-detail-2.0"/>')]
for marker,tag in markers:
 if marker not in s:s=s.replace('</head>',tag+'\n</head>',1)
styles=[('data-ld8="design-system"','<link rel="stylesheet" href="design-system-v8.css" data-ld8="design-system"/>'),('data-ld8="home-f1"','<link rel="stylesheet" href="home-v8.css" data-ld8="home-f1"/>'),('data-ld8="shell-f11"','<link rel="stylesheet" href="shell-v8.css" data-ld8="shell-f11"/>'),('data-ld8="selector-f2"','<link rel="stylesheet" href="game-selector-v8.css" data-ld8="selector-f2"/>'),('data-ld8="detail-f3"','<link rel="stylesheet" href="pokemon-detail-v8.css" data-ld8="detail-f3"/>')]
for marker,tag in styles:
 if marker not in s:s=s.replace('</head>',tag+'\n</head>',1)
scripts=[('src="game-context-v8.js"','<script src="game-context-v8.js" data-ld8="game-context-f25"></script>'),('src="game-selector-v8.js"','<script src="game-selector-v8.js" data-ld8="selector-f25"></script>'),('src="home-v8.js"','<script src="home-v8.js" data-ld8="home-f1"></script>'),('src="pokemon-detail-v8.js"','<script src="pokemon-detail-v8.js" data-ld8="detail-f3"></script>')]
for marker,tag in scripts:
 if marker not in s:s=s.replace('</body>',tag+'\n</body>',1)
HTML.write_text(s,encoding='utf-8');print('Phase F3 Pokemon Detail 2.0 injected with stable F2.5 contexts preserved')

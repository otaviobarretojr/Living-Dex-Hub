from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-paldea-map" content="2.0"' not in s:
    s=s.replace('</head>','<meta name="living-dex-paldea-map" content="2.0"/>\n</head>',1)
css=r'''
/* Paldea Map 2.0 — offline geographic map artwork */
.paldea-map{position:relative;min-height:620px;aspect-ratio:4/3;border-radius:26px;overflow:hidden;border:1px solid rgba(148,180,215,.16);background:#4b93aa;box-shadow:0 20px 60px rgba(0,0,0,.28)}
.paldea-map-art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;user-select:none;-webkit-user-drag:none}
.paldea-map-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,12,22,.10),transparent 20%,transparent 78%,rgba(4,12,22,.22));pointer-events:none}
.route-polyline{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none;overflow:visible}.route-polyline polyline{fill:none;stroke:rgba(235,250,255,.62);stroke-width:3;stroke-dasharray:7 7;vector-effect:non-scaling-stroke;filter:drop-shadow(0 2px 2px rgba(0,0,0,.55))}
.geo-node{z-index:5}.geo-node::after{content:"";position:absolute;inset:-5px;border-radius:50%;border:1px solid rgba(255,255,255,.24)}.geo-node.next{animation:mapPulse 1.8s ease-in-out infinite}@keyframes mapPulse{0%,100%{box-shadow:0 0 0 7px rgba(102,224,173,.10),0 10px 30px rgba(0,0,0,.38)}50%{box-shadow:0 0 0 13px rgba(102,224,173,.03),0 10px 30px rgba(0,0,0,.38)}}
.map-caption{position:absolute;left:14px;top:14px;z-index:6;padding:8px 10px;border-radius:12px;background:rgba(5,14,24,.78);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(10px);font-size:8px;color:#d9edf7;font-weight:850;letter-spacing:.08em;text-transform:uppercase}
.map-full{z-index:8!important}.journey-shell.map-fullscreen .paldea-map{height:100vh!important;min-height:100vh!important;aspect-ratio:auto!important;border-radius:0!important}.journey-shell.map-fullscreen .paldea-map-art{object-fit:contain;background:#4b93aa}.journey-shell.map-fullscreen .map-caption{top:calc(14px + env(safe-area-inset-top))}.journey-shell.map-fullscreen .map-full{top:calc(14px + env(safe-area-inset-top))}
.map-legend{z-index:7!important}.map-next-label{z-index:7!important;backdrop-filter:blur(10px)}
@media(max-width:600px){.paldea-map{min-height:560px;aspect-ratio:3/4}.paldea-map-art{object-fit:cover}.journey-shell.map-fullscreen .paldea-map-art{object-fit:contain}}
'''
if '/* Paldea Map 2.0' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Paldea Map 2.0 — real offline map artwork and route overlay.
function paldeaRoutePolyline(){return (SV_ROUTE_POS||[]).map(p=>`${p[0]},${p[1]}`).join(' ')}
journeyMap=function(){const next=svNextIndex(),done=new Set(state.journey.sv.done||[]);return `<div class="paldea-map"><img class="paldea-map-art" src="assets/maps/paldea-route.svg" alt="Mapa estilizado de Paldea" draggable="false"><div class="paldea-map-shade"></div><div class="map-caption">Paldea · rota por nível</div><svg class="route-polyline" viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="${paldeaRoutePolyline()}"></polyline></svg><button class="btn map-full" onclick="toggleJourneyMapFull()">⛶ Tela cheia</button>${SV_ROUTE.map((r,i)=>{const p=SV_ROUTE_POS[i],n=i+1,cls=`${r[1]} ${done.has(n)?'done':''} ${next===n?'next':''}`;return `<button class="geo-node ${cls}" style="left:${p[0]}%;top:${p[1]}%" title="${n}. ${r[0]} · Lv.${r[2]}" onclick="premiumToast('${n}. ${r[0]} · Lv.${r[2]}')">${n}</button>`}).join('')}<div class="map-legend"><span>● Ginásio</span><span>● Titã</span><span>● Team Star</span></div>${next?`<div class="map-next-label"><b>Próximo: ${next}. ${SV_ROUTE[next-1][0]}</b>Lv.${SV_ROUTE[next-1][2]} · ${SV_ROUTE[next-1][3]}</div>`:''}</div><p style="font-size:9px;color:#8197ad;line-height:1.5;margin-top:10px">Mapa visual próprio e offline do Living Dex Hub, criado para orientação da rota recomendada. Os 18 marcadores continuam interativos e a tela cheia funciona sem internet.</p>`}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Paldea Map 2.0 applied')
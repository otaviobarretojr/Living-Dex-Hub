from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'app'/'src'/'main'/'assets'/'index.html').read_text(encoding='utf-8')
svg=root/'app'/'src'/'main'/'assets'/'assets'/'maps'/'paldea-route.svg'
svg_text=svg.read_text(encoding='utf-8') if svg.exists() else ''
checks={
 'Map 2.0 marker':'living-dex-paldea-map" content="2.0' in s,
 'Offline SVG exists':svg.exists() and svg.stat().st_size>1000,
 'Offline SVG referenced':'assets/maps/paldea-route.svg' in s,
 'Map image renderer':'paldea-map-art' in s,
 '18 route overlay':'SV_ROUTE.map((r,i)' in s and 'SV_ROUTE_POS[i]' in s,
 'Route polyline':'function paldeaRoutePolyline' in s and 'route-polyline' in s,
 'Next destination':'map-next-label' in s and 'svNextIndex()' in s,
 'Fullscreen':'toggleJourneyMapFull()' in s and 'map-fullscreen' in s,
 'Journey 1.9 preserved':'living-dex-smart-prep" content="1.9' in s,
 'No external map dependency':'href="http' not in svg_text and "href='http" not in svg_text and 'url(http' not in svg_text
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed:raise SystemExit('Map 2.0 validation failed: '+', '.join(failed))
print(f'MAP 2.0 VALIDADO: {len(checks)}/{len(checks)}')
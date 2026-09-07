from pathlib import Path
root=Path(__file__).resolve().parents[1]
h=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
svg=(root/'app/src/main/assets/assets/maps/paldea-route.svg').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-paldea-map" content="4.3"' in h,
 '18 positions':'const REF43_POS=' in h and 'SV_ROUTE_POS.splice' in h,
 'zoom controls':'ref43ZoomBy' in h and 'ref43Reset' in h,
 'pan pointers':'onpointerdown' in h and 'onpointermove' in h,
 'detail card':'ref43Point' in h and 'ref43-detail' in h,
 'progress toggle':'ref43SetDone' in h and 'ref43TogglePoint' in h,
 'array repair':'!Array.isArray(state.journey.sv.done)' in h,
 'light builds':'Remove the old dark build modal visually' in h,
 'map geography':all(x in svg for x in ['LAGO CASSEROYA','DESERTO ASADO','CRATERA DE','Mesagoza','Levincia','Glaseado']),
 'offline svg':'http://' not in svg.replace('http://www.w3.org/2000/svg','') and 'https://' not in svg,
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
assert all(checks.values())
print('Paldea map 4.3 validation passed')
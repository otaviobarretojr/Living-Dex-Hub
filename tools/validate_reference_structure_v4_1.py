from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-reference-structure" content="4.1"' in s,
 'three doors':all(x in s for x in ['Próximo objetivo','Time recomendado','Rota de Paldea']),
 'route checklist':'function ref41Route()' in s and 'ref41Toggle' in s,
 'team builds':'function ref41Team()' in s and 'openJourneyBuild' in s,
 'map action':'function ref41Map()' in s and 'journeyMap()' in s,
 'map asset':"assets/maps/paldea-route.svg" in s,
 '18 route source':'SV_ROUTE.map' in s,
 'no old journey home':'#home .home232-journey,#home .home-journey-summary{display:none!important}' in s,
}
for k,v in checks.items(): print(('OK ' if v else 'FAIL ')+k)
assert all(checks.values())
print('Reference Structure 4.1 validation passed')
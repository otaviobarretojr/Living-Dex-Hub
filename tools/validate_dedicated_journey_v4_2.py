from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-dedicated-journey" content="4.2"' in s,
 'route page':'id="ref42RoutePage"' in s,
 'team page':'id="ref42TeamPage"' in s,
 'map page':'id="ref42MapPage"' in s,
 'fullscreen layout':'position:fixed;inset:0;z-index:900' in s,
 'route checklist':'function ref42RenderRoute()' in s and 'ref42Toggle' in s,
 'team builds':'function ref42RenderTeam()' in s and 'openJourneyBuild' in s,
 'map dedicated':'function ref42RenderMap()' in s and 'ref42-mapstage' in s,
 'home routing':'window.ref41Open=function' in s and 'ref42Open(kind)' in s,
 'android back':'window.androidHandleBack=function' in s,
 '18 objectives':'SV_ROUTE.map' in s,
 'map renderer':'journeyMap()' in s,
}
for k,v in checks.items():print(('PASS ' if v else 'FAIL ')+k)
assert all(checks.values())
print('Dedicated Journey 4.2 validation passed')
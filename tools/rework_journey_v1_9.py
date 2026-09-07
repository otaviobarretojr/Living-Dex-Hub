from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-smart-prep" content="1.9"' not in s:
    s=s.replace('</head>','<meta name="living-dex-smart-prep" content="1.9"/>\n</head>',1)
css=r'''
/* Journey 1.9 — smart matchup preparation */
.smart-prep{margin:12px 0 14px;padding:16px;border-radius:22px;border:1px solid rgba(102,224,173,.16);background:radial-gradient(360px 180px at 100% 0,rgba(102,224,173,.09),transparent 65%),rgba(255,255,255,.025)}
.smart-prep-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px}.smart-prep-head .kicker{font-size:8px;letter-spacing:.14em;text-transform:uppercase;color:#66e0ad;font-weight:900}.smart-prep-head h3{margin:4px 0 3px;font-size:17px}.smart-prep-head p{margin:0;color:#8fa5bc;font-size:9px;line-height:1.5}.smart-score{min-width:58px;text-align:center;padding:8px 10px;border-radius:16px;border:1px solid rgba(102,224,173,.14);background:rgba(102,224,173,.06)}.smart-score b{display:block;font-size:19px}.smart-score small{font-size:7px;color:#8fb7a5}.prep-team{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.prep-member{position:relative;display:grid;grid-template-columns:54px 1fr;align-items:center;gap:8px;padding:10px;border-radius:16px;border:1px solid rgba(148,180,215,.11);background:rgba(255,255,255,.022);cursor:pointer}.prep-member.best{border-color:rgba(102,224,173,.30);background:rgba(102,224,173,.055)}.prep-member.risk{border-color:rgba(255,174,112,.20)}.prep-member img{width:54px;height:54px;object-fit:contain}.prep-member b{font-size:10px;display:block}.prep-member small{display:block;font-size:7px;color:#8399ae;margin-top:2px;line-height:1.35}.prep-rank{position:absolute;right:7px;top:7px;font-size:7px;padding:4px 6px;border-radius:999px;background:rgba(255,255,255,.05);color:#a8bbcd}.prep-rank.best{background:rgba(102,224,173,.12);color:#c8f8e1}.prep-rank.good{background:rgba(79,181,255,.10);color:#c9edff}.prep-rank.risk{background:rgba(255,174,112,.10);color:#ffd7b8}.prep-status{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}.prep-status span{font-size:6.5px;padding:4px 5px;border-radius:999px;border:1px solid rgba(148,180,215,.10);color:#92a8bd}.prep-status .owned{color:#bff5da;border-color:rgba(102,224,173,.18);background:rgba(102,224,173,.06)}.prep-status .missing{color:#ffc7b1;border-color:rgba(255,146,109,.16);background:rgba(255,146,109,.05)}.battle-plan{margin-top:10px;padding:11px 12px;border-radius:15px;background:rgba(79,181,255,.05);border:1px solid rgba(79,181,255,.10);font-size:8.5px;line-height:1.55;color:#a8bdd0}.battle-plan b{color:#eaf8ff}.smart-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.smart-actions .btn{min-height:38px;font-size:9px}.home-next-objective{margin-top:12px;padding:13px 14px;border-radius:17px;border:1px solid rgba(102,224,173,.13);background:rgba(102,224,173,.035);display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center}.home-next-objective .kicker{font-size:7px;letter-spacing:.13em;text-transform:uppercase;color:#66e0ad;font-weight:900}.home-next-objective b{display:block;font-size:11px;margin-top:3px}.home-next-objective small{color:#8fa5bc;font-size:7px}.home-next-objective .btn{min-height:36px;font-size:8px}
@media(max-width:680px){.prep-team{grid-template-columns:1fr 1fr}.prep-member{grid-template-columns:46px 1fr}.prep-member img{width:46px;height:46px}.smart-prep-head{align-items:center}}
@media(max-width:430px){.prep-team{grid-template-columns:1fr}.smart-score{min-width:52px}.home-next-objective{grid-template-columns:1fr}}
'''
if '/* Journey 1.9 — smart matchup preparation */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Journey 1.9 — collection-aware smart preparation for the next Scarlet/Violet objective.
const SV_TEAM_TYPES={908:['Grass','Dark'],911:['Fire','Ghost'],914:['Water','Fighting'],936:['Fire','Psychic'],937:['Fire','Ghost'],823:['Flying','Steel'],941:['Electric','Flying'],130:['Water','Flying'],980:['Poison','Ground'],930:['Grass','Normal']};
const SV_BOSS_TIPS={
 Bug:'Fire, Flying e Rock funcionam muito bem. Evite depender de golpes Grass.',
 Rock:'Water, Grass, Fighting, Ground e Steel são as melhores coberturas.',
 Grass:'Fire e Flying resolvem boa parte do confronto com segurança.',
 Flying:'Electric, Ice e Rock são as coberturas prioritárias.',
 Dark:'Fighting, Bug e Fairy são as respostas mais diretas.',
 Electric:'Ground é a resposta principal; lembre que alguns líderes usam cobertura e Tera para contornar a fraqueza.',
 Fire:'Water, Ground e Rock são as opções mais seguras.',
 Steel:'Fire, Fighting e Ground oferecem ótima pressão.',
 Water:'Electric e Grass são os melhores atalhos ofensivos.',
 Poison:'Ground e Psychic são as coberturas prioritárias.',
 Normal:'Fighting é a resposta direta.',
 Ghost:'Ghost e Dark são os melhores tipos ofensivos.',
 Ground:'Water, Grass e Ice funcionam bem, respeitando cobertura do oponente.',
 Psychic:'Bug, Ghost e Dark são as respostas principais.',
 Ice:'Fire, Fighting, Rock e Steel são excelentes.',
 Fairy:'Poison e Steel são os counters mais limpos.',
 Dragon:'Ice, Dragon e Fairy são as melhores respostas.',
 Fighting:'Flying, Psychic e Fairy são as melhores coberturas.'
};
function svCurrentVersionName(){return (typeof selectedVersion==='function'?selectedVersion('sv'):'')||'Scarlet / Violet'}
function svResolveTeamId(id){let t=SV_BUILD_FAMILY[id]||id;if(t===936){const v=svCurrentVersionName().toLowerCase();if(v.includes('violet'))return 937}return t}
function svGameOwnedSmart(id){const base=SV_BUILD_FAMILY[id]||id,targets=[id,base,svResolveTeamId(id)];const version=typeof selectedVersion==='function'?selectedVersion('sv'):'';return targets.some(x=>{try{return ui151GameOwned(x,'sv',version)}catch(e){return !!state.games?.[`sv:${x}`]||!!state.global?.[x]}})}
function svPhaseForNext(){const n=svNextIndex()||18;return n<=6?'early':n<=12?'mid':'late'}
function svRecommendedTeamIds(){const j=state.journey.sv,phase=svPhaseForNext();return (SV_TEAMS[j.starter]?.[phase]||[]).map(svResolveTeamId)}
function svMemberName(id){const b=SV_BUILDS[id]||SV_BUILDS[SV_BUILD_FAMILY[id]];if(id===937)return 'Ceruledge';if(id===936)return 'Armarouge';return b?.name||`#${id}`}
function svMemberTypes(id){if(id===937)return ['Fire','Ghost'];return SV_TEAM_TYPES[id]||SV_TEAM_TYPES[SV_BUILD_FAMILY[id]]||[]}
function svPrepScore(id,bossType){const counters=SV_COUNTERS[bossType]||[],types=svMemberTypes(id),owned=svGameOwnedSmart(id);let score=0;types.forEach(t=>{if(counters.includes(t))score+=4});if(owned)score+=2;const build=SV_BUILDS[id]||SV_BUILDS[SV_BUILD_FAMILY[id]];if(build)score+=1;return {id,score,owned,types,good:types.some(t=>counters.includes(t))}}
function svSmartPrepData(){const n=svNextIndex();if(!n)return null;const r=SV_ROUTE[n-1],items=svRecommendedTeamIds().map(id=>svPrepScore(id,r[3])).sort((a,b)=>b.score-a.score);return {n,r,items,best:items[0],second:items[1]}}
function svSmartPrep(){const d=svSmartPrepData();if(!d)return `<div class="smart-prep"><div class="smart-prep-head"><div><div class="kicker">Preparação inteligente</div><h3>Rota principal concluída</h3><p>Os 18 objetivos principais já foram marcados como completos.</p></div><div class="smart-score"><b>✓</b><small>PRONTO</small></div></div></div>`;const [title,kind,level,type]=d.r,counters=SV_COUNTERS[type]||[],ownedCount=d.items.filter(x=>x.owned).length;const readiness=Math.round((ownedCount/d.items.length)*60 + (d.best?.good?40:15));const bestName=d.best?svMemberName(d.best.id):'seu melhor counter';const secondName=d.second?svMemberName(d.second.id):'uma alternativa';return `<div class="smart-prep"><div class="smart-prep-head"><div><div class="kicker">Preparação inteligente · ${d.n}/18</div><h3>${title}</h3><p>${kind==='gym'?'Ginásio':kind==='titan'?'Titã':'Team Star'} · Lv.${level} · foco ${type}. O app cruza a fase atual, seu starter, a versão e os Pokémon já registrados neste jogo.</p></div><div class="smart-score"><b>${readiness}%</b><small>PRONTIDÃO</small></div></div><div class="prep-team">${d.items.map((x,i)=>{const label=i===0?'Melhor':x.good?'Boa':'Neutro',cls=i===0?'best':x.good?'good':'';return `<div class="prep-member ${i===0?'best':''}" onclick="openJourneyBuild(${x.id})">${pokemonImageHTML(x.id,'')}<div><b>${svMemberName(x.id)}</b><small>${x.types.join(' / ')||'Cobertura variada'}</small><div class="prep-status"><span class="${x.owned?'owned':'missing'}">${x.owned?'✓ No seu jogo':'○ Não registrado'}</span>${x.good?'<span>vantagem de tipo</span>':'<span>cobertura neutra</span>'}</div></div><span class="prep-rank ${cls}">${label}</span></div>`}).join('')}</div><div class="battle-plan"><b>Plano rápido:</b> entre próximo de <b>Lv.${level}</b>. Prioridade: <b>${bestName}</b>${d.second?` · alternativa: <b>${secondName}</b>`:''}. ${SV_BOSS_TIPS[type]||`Priorize ${counters.join(', ')}.`}</div><div class="smart-actions"><button class="btn primary" onclick="openJourneyBuild(${d.best?.id||0})">Ver build da melhor escolha</button>${d.best&&!d.best.owned?`<button class="btn" onclick="closeJourney();setTimeout(()=>openPokemon?.(${d.best.id}),30)">Como obter ${bestName}</button>`:''}<button class="btn" onclick="renderJourney('map')">Ver próximo no mapa</button></div></div>`}
const journeyRouteV18Smart=journeyRoute;journeyRoute=function(){return svNextCard()+svSmartPrep()+journeyRouteV18Smart().replace(svNextCard(),'')}
function injectSmartHome(){if(state.activeGameId!=='sv')return;const card=document.querySelector('#home .playing-card');if(!card||card.querySelector('.home-next-objective'))return;const d=svSmartPrepData();if(!d)return;const name=d.r[0],level=d.r[2];card.insertAdjacentHTML('beforeend',`<div class="home-next-objective"><div><div class="kicker">Próximo objetivo</div><b>${name}</b><small>Nível recomendado ${level} · preparação pronta na Jornada</small></div><button class="btn" onclick="openJourney('sv','route')">Preparar</button></div>`)}
const renderActiveGameHomeV19=renderActiveGameHome;renderActiveGameHome=function(){const r=renderActiveGameHomeV19.apply(this,arguments);setTimeout(injectSmartHome,0);return r}
const setJourneyStarterV19=setJourneyStarter;setJourneyStarter=function(x){setJourneyStarterV19(x);setTimeout(()=>{if(document.getElementById('journeyShell')?.dataset.tab==='route')renderJourney('route')},0)}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Journey 1.9 smart preparation applied')

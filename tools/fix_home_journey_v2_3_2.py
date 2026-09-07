from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-home-journey" content="2.3.2"' not in s:
    s=s.replace('</head>','<meta name="living-dex-home-journey" content="2.3.2"/>\n</head>',1)
css=r'''
/* Home + Journey 2.3.2 — Home is always isolated from General and Journey is a separate summary. */
#home .home232-journey{display:block!important;max-width:860px;margin:14px auto 26px;padding:18px;border-radius:24px;border:1px solid rgba(148,180,215,.14);background:radial-gradient(380px 180px at 100% 0,rgba(102,224,173,.08),transparent 65%),linear-gradient(180deg,rgba(15,31,50,.91),rgba(9,22,38,.95));box-shadow:0 18px 50px rgba(0,0,0,.24)}
.home232-journey-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:13px}.home232-journey-head .eyebrow{font-size:8px;letter-spacing:.15em;text-transform:uppercase;color:#66e0ad;font-weight:900}.home232-journey-head h2{margin:4px 0 4px;font-size:20px;letter-spacing:-.025em}.home232-journey-head p{margin:0;color:#8fa5bc;font-size:9px;line-height:1.5}.home232-journey-progress{font-size:10px;font-weight:850;color:#c9f7e2;padding:7px 9px;border-radius:999px;border:1px solid rgba(102,224,173,.17);background:rgba(102,224,173,.06);white-space:nowrap}
.home232-journey-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.home232-jitem{min-height:92px;padding:12px;border-radius:16px;border:1px solid rgba(148,180,215,.10);background:rgba(255,255,255,.022)}.home232-jitem .label{font-size:7px;text-transform:uppercase;letter-spacing:.11em;color:#7890a8;font-weight:850}.home232-jitem b{display:block;margin-top:6px;font-size:11px;line-height:1.3;color:#eef8ff}.home232-jitem small{display:block;margin-top:4px;color:#849aaf;font-size:7.5px;line-height:1.45}.home232-team{display:flex;gap:4px;margin-top:7px;flex-wrap:wrap}.home232-team span{font-size:6.5px;border:1px solid rgba(114,213,255,.13);background:rgba(114,213,255,.04);padding:4px 5px;border-radius:999px;color:#bcd9e8}.home232-journey .home232-continue{width:100%;margin-top:10px;min-height:48px;font-size:10px}
body.home232-home-mode .nav23-general-switch{display:none!important}body.home232-home-mode #home{display:block!important}body.home232-home-mode #games,body.home232-home-mode #global{display:none!important}
@media(max-width:680px){.home232-journey-grid{grid-template-columns:1fr}.home232-jitem{min-height:auto}.home232-journey{margin-top:11px;padding:15px;border-radius:21px}}
'''
if '/* Home + Journey 2.3.2' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Home + Journey 2.3.2 — restore a deterministic Home after visiting General.
function home232JourneyData(){
 if(state.activeGameId!=='sv')return null;
 const done=state.journey?.sv?.done||{};
 const count=Object.values(done).filter(Boolean).length;
 const next=typeof svSmartPrepData==='function'?svSmartPrepData():null;
 const team=typeof svRecommendedTeamIds==='function'?svRecommendedTeamIds():[];
 return {count,next,team};
}
function home232TeamNames(ids){return (ids||[]).slice(0,3).map(id=>typeof svMemberName==='function'?svMemberName(id):`#${id}`)}
function home232RenderJourney(){
 const home=document.getElementById('home');if(!home)return;
 home.querySelectorAll('.home232-journey').forEach(x=>x.remove());
 if(state.activeGameId!=='sv')return;
 const d=home232JourneyData();if(!d)return;
 const nextName=d.next?.r?.[0]||'Rota principal concluída';
 const nextLevel=d.next?.r?.[2];
 const names=home232TeamNames(d.team);
 const destination=d.next?.r?.[0]||'Paldea concluída';
 const shell=home.querySelector('.home-current-shell');if(!shell)return;
 shell.insertAdjacentHTML('afterend',`<section class="home232-journey" aria-label="Resumo da Jornada"><div class="home232-journey-head"><div><div class="eyebrow">Jornada</div><h2>Seu andamento em Paldea</h2><p>Mapa, time recomendado e próximo objetivo reunidos em um único lugar.</p></div><span class="home232-journey-progress">${d.count}/18</span></div><div class="home232-journey-grid"><div class="home232-jitem"><div class="label">Andamento</div><b>${nextName}</b><small>${nextLevel?`Próximo objetivo recomendado · Lv.${nextLevel}`:'Os 18 objetivos principais foram concluídos.'}</small></div><div class="home232-jitem"><div class="label">Time recomendado</div><b>${names[0]||'Equipe atual'}</b><div class="home232-team">${names.map(x=>`<span>${x}</span>`).join('')}</div><small>Baseado no starter, fase da história, versão e registros.</small></div><div class="home232-jitem"><div class="label">Mapa</div><b>${destination}</b><small>Próximo ponto da rota recomendado no mapa estilizado de Paldea.</small></div></div><button class="btn primary home232-continue" onclick="openJourney('sv','route')">Continuar jornada</button></section>`);
}
function home232ResetHome(){
 document.body.classList.remove('nav23-library-mode','game-dex-focus');
 document.body.classList.add('home232-home-mode');
 document.querySelectorAll('.nav23-general-switch').forEach(x=>x.remove());
 document.querySelectorAll('.mnav-item').forEach(x=>x.classList.remove('active'));
 document.querySelector('.mnav-item[data-v="home"]')?.classList.add('active');
 if(typeof renderActiveGameHome==='function')renderActiveGameHome();
 setTimeout(()=>{if(typeof nav23PolishHome==='function')nav23PolishHome();home232RenderJourney();},0);
 window.scrollTo({top:0,behavior:'auto'});
}
function home232LeaveHome(){document.body.classList.remove('home232-home-mode')}
const home232BaseGo=window.go;
window.go=function(v){
 if(v==='home'){const r=home232BaseGo(v);setTimeout(home232ResetHome,0);return r}
 home232LeaveHome();return home232BaseGo(v);
};
const home232BaseLibrary=window.nav23OpenLibrary;if(typeof home232BaseLibrary==='function'){window.nav23OpenLibrary=function(){home232LeaveHome();return home232BaseLibrary.apply(this,arguments)}}
const home232BaseNational=window.nav23OpenNationalDex;if(typeof home232BaseNational==='function'){window.nav23OpenNationalDex=function(){home232LeaveHome();return home232BaseNational.apply(this,arguments)}}
const home232BaseOpenDex=window.nav221OpenGameDex;if(typeof home232BaseOpenDex==='function'){window.nav221OpenGameDex=async function(){home232LeaveHome();return home232BaseOpenDex.apply(this,arguments)};window.nav21OpenGameDex=window.nav221OpenGameDex}
const home232BaseRenderHome=window.renderActiveGameHome;if(typeof home232BaseRenderHome==='function'){window.renderActiveGameHome=function(){const r=home232BaseRenderHome.apply(this,arguments);setTimeout(home232RenderJourney,0);return r}}
setTimeout(()=>{if(document.getElementById('home')?.classList.contains('active'))home232ResetHome()},10);
if(new URLSearchParams(location.search).get('homeqa')==='1'){
 setTimeout(()=>{nav23OpenLibrary();go('home');setTimeout(()=>{const home=document.getElementById('home');const library=!document.body.classList.contains('nav23-library-mode');const current=!!home?.querySelector('.home-current-shell');const journey=state.activeGameId==='sv'?!!home?.querySelector('.home232-journey'):true;const noSwitch=!home?.querySelector('.nav23-general-switch');document.documentElement.dataset.homeQa=(home?.classList.contains('active')&&library&&current&&journey&&noSwitch)?'1':'0'},450)},650)
}
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Home + Journey 2.3.2 applied')

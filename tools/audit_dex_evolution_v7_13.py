from pathlib import Path
import re

p=Path(__file__).resolve().parents[1]/'app/src/main/assets/index.html'
s=p.read_text(encoding='utf-8')
marker='living-dex-full-audit" content="7.13.0"'
if marker in s:
    print('Full Dex/evolution audit 7.13.0 already applied'); raise SystemExit

# Correct stale Isle of Armor display metadata without touching the actual embedded Dex,
# which is validated independently as 211 entries.
def fix_isle_segment(m):
    seg=m.group(0)
    seg=re.sub(r'(?<!\d)210(?!\d)', '211', seg)
    return seg
s=re.sub(r'(?is)(?:isle[- ]of[- ]armor|ilha da armadura).{0,180}', fix_isle_segment, s)

s=s.replace('</head>','<meta name="living-dex-full-audit" content="7.13.0"/>\n</head>',1)
css=r'''
/* 7.13.0 — compact special evolution guidance inside the existing evolution card. */
#modal .ld713-tip{margin:0 0 12px;padding:10px 12px;border:1px solid #dbe8ff;border-radius:14px;background:#f6f9ff;color:#344054;font-size:10px;line-height:1.45;font-weight:700}
#modal .ld713-tip b{display:block;color:#2367d1;font-size:10px;margin-bottom:3px}
'''
s=s.replace('</style>',css+'\n</style>',1)

js=r'''
// Full Dex/evolution audit 7.13.0
// Curated rules cover special evolutions whose practical requirements are often
// clearer than a generic evolution-chain response.
const LD713_SPECIAL_EVOLUTION_HINTS={
  sv:{
    999:'Colete 999 Gimmighoul Coins e suba Gimmighoul de nível para evoluir para Gholdengo.',
    983:'Para obter Kingambit, Bisharp deve derrotar 3 Bisharp que carregam Leader’s Crest enquanto ele também segura Leader’s Crest; depois, suba de nível.',
    979:'Use Rage Fist 20 vezes com Primeape e depois suba de nível para evoluir para Annihilape.',
    922:'Caminhe cerca de 1.000 passos com Pawmo usando Let’s Go e depois suba de nível para obter Pawmot.',
    946:'Caminhe cerca de 1.000 passos com Bramblin usando Let’s Go e depois suba de nível para obter Brambleghast.',
    953:'Caminhe cerca de 1.000 passos com Rellor usando Let’s Go e depois suba de nível para obter Rabsca.',
    963:'Finizen evolui para Palafin ao subir para o nível 38 ou mais enquanto você está em uma sessão do Union Circle.',
    935:'Charcadet evolui com Auspicious Armor para Armarouge ou Malicious Armor para Ceruledge, conforme a versão.',
    203:'Ensine Twin Beam a Girafarig e depois suba de nível para obter Farigiraf.',
    206:'Ensine Hyper Drill a Dunsparce e depois suba de nível para obter Dudunsparce.'
  },
  arceus:{
    123:'Use Black Augurite em Scyther para evoluir para Kleavor.',
    217:'Use Peat Block em Ursaring durante uma lua cheia para evoluir para Ursaluna.',
    234:'Use Psyshield Bash em Agile Style 20 vezes com Stantler para evoluir para Wyrdeer.',
    550:'White-Striped Basculin deve acumular 294 ou mais de dano de recoil sem desmaiar para evoluir para Basculegion.',
    211:'Use Barb Barrage em Strong Style 20 vezes com Hisuian Qwilfish para evoluir para Overqwil.',
    215:'Use Razor Claw em Hisuian Sneasel durante o dia para evoluir para Sneasler.',
    64:'Kadabra pode evoluir para Alakazam usando Linking Cord em Legends Arceus.',
    67:'Machoke pode evoluir para Machamp usando Linking Cord em Legends Arceus.',
    75:'Graveler pode evoluir para Golem usando Linking Cord em Legends Arceus.',
    93:'Haunter pode evoluir para Gengar usando Linking Cord em Legends Arceus.'
  },
  swsh:{
    83:'Galarian Farfetch’d evolui para Sirfetch’d após acertar 3 golpes críticos na mesma batalha.',
    562:'Galarian Yamask deve perder pelo menos 49 HP sem desmaiar; depois passe sob o grande arco de pedra em Dusty Bowl para evoluir para Runerigus.',
    868:'Dê um Sweet a Milcery e faça o personagem girar para evoluir para Alcremie; o resultado varia conforme Sweet, horário e duração do giro.',
    79:'Galarian Slowpoke evolui para Slowbro com Galarica Cuff ou para Slowking com Galarica Wreath.'
  },
  letsgo:{
    808:'Meltan não evolui dentro de Let’s Go. A evolução para Melmetal é feita no Pokémon GO usando 400 Meltan Candies antes da transferência.'
  }
};
function ld713HintFor(id){
 const g=String(currentGame?.id||state?.activeGameId||'');
 return LD713_SPECIAL_EVOLUTION_HINTS[g]?.[Number(id)]||'';
}
function ld713ApplyEvolutionTip(id){
 const evo=document.getElementById('ld76Evolution');if(!evo)return;
 evo.querySelector('.ld713-tip')?.remove();
 const tip=ld713HintFor(id);if(!tip)return;
 const body=document.getElementById('ld76EvolutionBody');
 if(body)body.insertAdjacentHTML('beforebegin','<div class="ld713-tip"><b>Dica de evolução</b>'+tip+'</div>');
}
const ld713OldRenderEvolution=window.ld76RenderEvolution;
if(typeof ld713OldRenderEvolution==='function')window.ld76RenderEvolution=async function(id){
 const r=await ld713OldRenderEvolution.apply(this,arguments);ld713ApplyEvolutionTip(id);return r;
};
const ld713OldBoxOpen=window.ld74OpenPokemon;
if(typeof ld713OldBoxOpen==='function')window.ld74OpenPokemon=function(id){
 const r=ld713OldBoxOpen.apply(this,arguments);setTimeout(()=>ld713ApplyEvolutionTip(id),80);setTimeout(()=>ld713ApplyEvolutionTip(id),700);return r;
};
const ld713OldOpen=window.openPokemon;
if(typeof ld713OldOpen==='function')window.openPokemon=function(id){
 const r=ld713OldOpen.apply(this,arguments);setTimeout(()=>ld713ApplyEvolutionTip(id),80);setTimeout(()=>ld713ApplyEvolutionTip(id),700);return r;
};
window.ld713Audit=function(){
 const expected={letsgo:153,swsh:400,bdsp:151,arceus:242,sv:400,za:232};
 const g=String(currentGame?.id||state?.activeGameId||''),dex=Array.isArray(currentDex)?currentDex:[];
 const ids=dex.map(x=>Number(x?.id||x)).filter(Number.isFinite),entries=dex.map((x,i)=>Number(x?.entry||x?.entry_number||i+1));
 return {version:'7.13.0',game:g,total:dex.length,expectedPrimary:expected[g]||null,uniquePokemon:new Set(ids).size===ids.length,uniqueEntries:new Set(entries).size===entries.length,allHaveLocalImageIds:ids.every(id=>id>=1&&id<=1025),specialHint:!!ld713HintFor(currentPokemon?.id)};
};
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Full Dex/evolution audit 7.13.0 applied')

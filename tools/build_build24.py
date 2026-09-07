from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Living_Dex_Hub_Build_23_0.html"
OUT = ROOT / "Living_Dex_Hub_Build_24_0.html"

if not SRC.exists():
    raise SystemExit("Build 23 não encontrado. Execute tools/restore_build23.py primeiro.")

s = SRC.read_text(encoding="utf-8")
s = s.replace("Living Dex Hub — Build 23.0", "Living Dex Hub — Build 24.0")
s = s.replace("Living Dex Hub • Build 23.0 • Embedded Data Pack", "Living Dex Hub • Build 24.0 • Image Integrity")

s = s.replace(
    "cards.push(`<div class=\"variant ${have?'have':''}\" onclick=\"toggleForm('${fk}',${pid},'${v.pokemon.name}')\"><img loading=\"lazy\" src=\"${ART}${pid}.png\"><b>${pretty(v.pokemon.name)}</b><small>${v.is_default?'Forma padrão':'Variante'}</small><div class=\"vcheck\">${have?'✓ Tenho esta forma':'Marcar forma'}</div></div>`);",
    "cards.push(`<div class=\"variant ${have?'have':''}\" onclick=\"toggleForm('${fk}',${pid},'${v.pokemon.name}')\">${pokemonImageHTML(pid)}<b>${pretty(v.pokemon.name)}</b><small>${v.is_default?'Forma padrão':'Variante'}</small><div class=\"vcheck\">${have?'✓ Tenho esta forma':'Marcar forma'}</div></div>`);"
)
s = s.replace(
    " document.getElementById('profileImg').src=ART+pid+'.png';",
    " const variantImg=document.getElementById('profileImg');if(variantImg){variantImg.dataset.fallbackStage='0';variantImg.onerror=()=>pokemonImageFallback(variantImg,pid);variantImg.src=`assets/pokemon/${pid}.png`;}`"
)
s = s.replace(
    "<div class=\"family-member ${state.global[m.id]?'have':''}\" title=\"${title(m.name)}\"><img loading=\"lazy\" src=\"${ART}${m.id}.png\"></div>",
    "<div class=\"family-member ${state.global[m.id]?'have':''}\" title=\"${title(m.name)}\">${pokemonImageHTML(m.id)}</div>"
)
s = s.replace(
    "box.innerHTML=`<img src=\"${ART}${t.id}.png\"><div>",
    "box.innerHTML=`${pokemonImageHTML(t.id)}<div>"
)

s = s.replace(
    "{id:'images',label:'Imagem com fallback para todo Pokémon',check:()=>typeof pokemonImageFallback==='function'&&typeof pokemonImageHTML==='function'},",
    "{id:'images',label:'Imagem com fallback para todo Pokémon',check:()=>typeof pokemonImageFallback==='function'&&typeof pokemonImageHTML==='function'&&!document.documentElement.innerHTML.includes('src=\\\"${ART}')},"
)
s = s.replace(
    "['Imagem com fallback',typeof pokemonImageFallback==='function'&&typeof pokemonImageHTML==='function'],",
    "['Imagem com fallback',typeof pokemonImageFallback==='function'&&typeof pokemonImageHTML==='function'&&!document.documentElement.innerHTML.includes('src=\\\"${ART}')],"
)

if 'src="${ART}' in s:
    raise SystemExit("Falha: ainda existe imagem Pokémon sem o pipeline de fallback.")

OUT.write_text(s, encoding="utf-8")
print(f"Build 24 criado em: {OUT}")

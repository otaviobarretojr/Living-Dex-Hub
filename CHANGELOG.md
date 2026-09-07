# Changelog

## Build 24.0 — Image Integrity

- Corrige as telas que ainda carregavam imagens diretamente sem fallback.
- Variantes passam a usar `pokemonImageHTML()`.
- Famílias evolutivas passam a usar `pokemonImageHTML()`.
- Próximo alvo passa a usar `pokemonImageHTML()`.
- A troca de variante na ficha reinicia corretamente o pipeline local → artwork oficial → HOME → sprite → placeholder.
- Auditorias internas de imagem ficam mais rígidas e falham se uma imagem Pokémon voltar a ser inserida diretamente pela variável `ART`.
- Sintaxe JavaScript validada com `node --check`.

### Bloqueadores ainda abertos para Core 1.0

- Empacotar imagens Pokémon localmente para uso offline real no APK.
- Executar a auditoria de obtenção dos 6 jogos e fechar as rotas parciais relevantes.
- Fazer teste funcional real em navegador/mobile com persistência e reabertura.

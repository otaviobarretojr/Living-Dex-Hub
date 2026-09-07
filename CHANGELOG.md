# Changelog

## Build 25.0 — Offline Data Pack

- Automatiza a geração do Data Pack das Pokédexes no GitHub Actions.
- Injeta o pacote gerado diretamente no HTML usado pelo aplicativo Android.
- Validação bloqueante exige as 12 Pokédexes antes da compilação.
- Pipeline confirmado com 12/12 Pokédexes embutidas.
- APK debug compilado, verificado, hash SHA-256 gerado e artefato publicado com sucesso.

### Próximos bloqueadores para Core 1.0

- Empacotar imagens Pokémon localmente para uso offline real no APK.
- Auditar e fechar rotas de obtenção parciais/especiais.
- Executar teste funcional real de persistência, reabertura e navegação em Android.

## Build 24.0 — Image Integrity

- Corrige as telas que ainda carregavam imagens diretamente sem fallback.
- Variantes passam a usar `pokemonImageHTML()`.
- Famílias evolutivas passam a usar `pokemonImageHTML()`.
- Próximo alvo passa a usar `pokemonImageHTML()`.
- A troca de variante na ficha reinicia corretamente o pipeline local → artwork oficial → HOME → sprite → placeholder.
- Auditorias internas de imagem ficam mais rígidas e falham se uma imagem Pokémon voltar a ser inserida diretamente pela variável `ART`.
- Sintaxe JavaScript validada com `node --check`.

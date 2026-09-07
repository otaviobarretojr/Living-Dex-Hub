# Changelog

## UI 1.1 — Validated

- Mantém o **Core 1.0** congelado e altera somente apresentação/navegação.
- Atualiza o pacote Android para **v1.1.0** (`versionCode 30`).
- Rework visual completo de fundo, superfícies, cards, botões, status e hierarquia.
- No mobile, substitui a navegação superior extensa por barra inferior com **Início, Jogos, Dex, Faltando e Mais**.
- O menu **Mais** reúne Famílias evolutivas, Planejamento, Form Dex, Storage/HOME e Configurações.
- Desktop mantém as 9 áreas originais.
- Busca e filtros ficam sticky durante a rolagem em telas menores.
- Grids da Pokédex se adaptam para 3 ou 2 colunas conforme a largura do aparelho.
- Paginação respeita a barra inferior e `safe-area-inset-bottom`.
- Adiciona suíte específica da interface com **13/13 verificações**.
- Core continua aprovado em **17/17 verificações**.
- JavaScript continua aprovado em `node --check`.
- Smoke test em Chrome real passou com a UI 1.1.
- Persistência após fechar e reabrir o navegador continuou aprovada.
- APK foi compilado, inspecionado e confirmado com UI 1.1 + 1.025 sprites locais.

### Estado de distribuição

O APK v1.1.0 é um **debug APK validado para instalação e QA**. Release público continua dependendo de assinatura/keystore de produção.

## Core 1.0 — Validated

- Fecha o Data Pack offline em **12/12 Pokédexes**.
- Empacota e valida fisicamente **1.025/1.025 sprites Pokémon** dentro do APK.
- Mantém imagem local como primeira fonte e fallbacks remotos para melhoria de qualidade.
- Remove o estado genérico `Método ainda não fechado` da engine de obtenção.
- Diferencia obtenção verificada, derivada, orientação geral e ausência de obtenção direta confirmada, sem inventar localização.
- Adiciona uma passada de usabilidade mobile para navegação, grids, fichas e paginação.
- Adiciona suíte bloqueante com **17/17 verificações estruturais**.
- Valida sintaxe JavaScript com `node --check`.
- Executa smoke test do aplicativo em Chrome headless real.
- Reabre o navegador com o mesmo perfil e confirma persistência de `localStorage`.
- Sela `BUILD_QA_VALIDATED=true` somente após os testes funcionais passarem.
- Compila o APK Android e inspeciona o conteúdo interno para confirmar 1.025 sprites e Core 1.0 validado.
- Gera e valida SHA-256 do APK.

## Build 25.0 — Offline Data Pack

- Automatiza a geração do Data Pack das Pokédexes no GitHub Actions.
- Injeta o pacote gerado diretamente no HTML usado pelo aplicativo Android.
- Validação bloqueante exige as 12 Pokédexes antes da compilação.
- Pipeline confirmado com 12/12 Pokédexes embutidas.
- APK debug compilado, verificado, hash SHA-256 gerado e artefato publicado com sucesso.

## Build 24.0 — Image Integrity

- Corrige as telas que ainda carregavam imagens diretamente sem fallback.
- Variantes passam a usar `pokemonImageHTML()`.
- Famílias evolutivas passam a usar `pokemonImageHTML()`.
- Próximo alvo passa a usar `pokemonImageHTML()`.
- A troca de variante na ficha reinicia corretamente o pipeline local → artwork oficial → HOME → sprite → placeholder.
- Auditorias internas de imagem ficam mais rígidas e falham se uma imagem Pokémon voltar a ser inserida diretamente pela variável `ART`.
- Sintaxe JavaScript validada com `node --check`.

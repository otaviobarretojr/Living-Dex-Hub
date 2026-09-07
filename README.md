# Living Dex Hub

Repositório oficial do projeto Living Dex Hub.

## Estado atual

- Baseline preservado: **Build 23.0 — Embedded Data Pack**
- Build intermediário: **Build 24.0 — Image Integrity**
- Build intermediário: **Build 25.0 — Offline Data Pack**
- Core funcional congelado: **Core 1.0 Validated**
- Interface atual: **UI 1.1 Validated**
- Android: **v1.1.0** (`versionCode 30`)
- National Dex: **1.025 espécies**
- Pokédexes embutidas: **12/12**
- Imagens locais no APK: **1.025/1.025**
- Escopo: Let's Go, Sword/Shield, Brilliant Diamond/Shining Pearl, Legends: Arceus, Scarlet/Violet e Legends Z-A
- Recursos centrais: Living Dex, famílias evolutivas, formas, Storage/HOME por espécime, jogos possuídos, disponibilidade, exclusivos, engine de obtenção, backup e snapshots.

## UI 1.1

A UI 1.1 reorganiza a experiência sem alterar as regras congeladas do Core 1.0:

- rework visual completo de superfícies, cards, botões, status, grids e hierarquia;
- navegação mobile fixa com **Início, Jogos, Dex, Faltando e Mais**;
- menu **Mais** com Famílias, Planejamento, Form Dex, Storage/HOME e Configurações;
- desktop preserva as 9 áreas originais;
- barra de busca/filtros passa a ficar acessível durante a rolagem no mobile;
- grids se adaptam a 3 colunas em celulares e 2 colunas em telas menores;
- paginação respeita a navegação inferior e safe area do Android;
- ações menos importantes do cabeçalho são reduzidas no mobile para diminuir poluição visual.

A suíte da UI possui **13/13 verificações estruturais** e também passa pelo smoke test funcional em Chrome e pelo teste de persistência após reabertura.

## Validação Core 1.0

O pipeline do GitHub Actions bloqueia o APK caso alguma etapa obrigatória falhe. O Core 1.0 passou por:

- geração e validação das 12 Pokédexes offline;
- empacotamento e validação física dos 1.025 sprites PNG;
- 17 verificações estruturais do Core;
- validação de sintaxe JavaScript com Node;
- smoke test em Chrome real;
- fechamento e reabertura do navegador com o mesmo perfil para validar persistência em `localStorage`;
- compilação Android;
- inspeção do APK para confirmar os 1.025 sprites, Data Pack, UI 1.1 e marcador de QA validado;
- geração de SHA-256.

A engine de obtenção não usa mais o estado genérico “Método ainda não fechado”. Ela diferencia rotas verificadas, rotas derivadas, orientação geral e ausência de obtenção direta confirmada, evitando inventar encontros ou locais sem evidência na base.

## Android

O artefato atual é um **APK debug v1.1.0 validado**. Ele serve para instalação e uso/teste do Core 1.0 + UI 1.1, mas ainda não é um release assinado para distribuição pública. A etapa de release exige assinatura/keystore própria.

## Builds anteriores

### Build 23.0

O Build 23.0 original é preservado em `archive/build-23/` como snapshot comprimido e pode ser reconstruído com:

```bash
python tools/restore_build23.py
```

### Build 24.0

Fechou a integridade de imagens em todos os renderizadores principais e padronizou o pipeline local → artwork → HOME → sprite → placeholder.

### Build 25.0

Automatizou e confirmou o Data Pack offline com 12/12 Pokédexes antes da compilação Android.

## Regra do projeto

O foco é Pokédex/Living Dex, salvamento e acompanhamento da coleção. Não adicionar sistemas de missão, cronômetro ou gamificação fora da mecânica real dos jogos Pokémon.

Todo Pokémon exibido deve possuir imagem/ícone. Os 1.025 Pokémon da National Dex possuem sprite local empacotado no APK, com fontes remotas apenas como melhoria/fallback de maior resolução.

## Próxima fase

Com **Core 1.0 + UI 1.1** validados, as próximas mudanças devem priorizar refinamento de telas específicas, qualidade visual das fichas, testes manuais em aparelho Android e preparação de assinatura release, sem reabrir funcionalidades congeladas sem necessidade.

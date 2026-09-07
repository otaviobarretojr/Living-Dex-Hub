# Living Dex Hub

Repositório oficial do projeto Living Dex Hub.

## Estado atual

- Core funcional: **Core 1.0 Validated**
- Interface atual: **UI 1.4 Validated**
- Android: **v1.4.0** (`versionCode 33`)
- National Dex: **1.025 espécies**
- Pokédexes embutidas: **12/12**
- Imagens locais no APK: **1.025/1.025**
- Escopo: Let's Go, Sword/Shield, Brilliant Diamond/Shining Pearl, Legends: Arceus, Scarlet/Violet e Legends Z-A
- Recursos centrais: Living Dex, famílias evolutivas, formas, Storage/HOME por espécime, jogos possuídos, disponibilidade, exclusivos, engine de obtenção, backup e snapshots.

## Android v1.4.0

A UI/Android 1.4 fecha a preparação técnica para distribuição sem alterar o Core 1.0:

- botão Voltar do Android fecha primeiro ficha/modal e menu Mais antes de sair do app;
- estado da WebView é salvo/restaurado durante recriação da Activity;
- ciclo de vida da WebView possui pause/resume/destroy explícitos;
- Safe Browsing ativo e mixed content bloqueado;
- links externos HTTPS são encaminhados ao navegador do sistema;
- DOM Storage continua habilitado para persistência local;
- tráfego HTTP em texto claro permanece bloqueado;
- o pipeline compila e inspeciona tanto o APK debug quanto o APK release unsigned.

## Validação

O pipeline bloqueia a publicação do artefato caso qualquer gate falhe. A versão 1.4 passou por:

- geração e validação das 12 Pokédexes offline;
- empacotamento e validação física dos 1.025 sprites PNG;
- validação Core 1.0;
- regressões das UI 1.1, 1.2 e 1.3;
- Android release readiness;
- sintaxe JavaScript;
- smoke test em Chrome real;
- persistência após fechamento/reabertura;
- compilação de debug e release unsigned;
- inspeção dos dois APKs para confirmar Core/UI e 1.025 sprites;
- SHA-256 dos dois pacotes.

## Distribuição

O **APK debug v1.4.0** está validado e é instalável para uso/teste. O **APK release unsigned** também foi compilado e validado estruturalmente, provando que a configuração de release está pronta.

Para um release público definitivo falta apenas assinar o pacote com um keystore de produção e preservar esse keystore para todas as futuras atualizações do aplicativo.

## Regra do projeto

O foco é Pokédex/Living Dex, salvamento e acompanhamento da coleção. Não adicionar sistemas de missão, cronômetro ou gamificação fora da mecânica real dos jogos Pokémon.

Todo Pokémon exibido deve possuir imagem/ícone. Os 1.025 Pokémon da National Dex possuem sprite local empacotado no APK, com fontes remotas apenas como melhoria/fallback de maior resolução.

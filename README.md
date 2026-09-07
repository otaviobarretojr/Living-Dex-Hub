# Living Dex Hub

Repositório oficial do projeto Living Dex Hub.

## Estado atual

- Core funcional: **Core 1.0 Validated**
- Interface atual: **UI 1.4 Validated**
- Android: **v1.4.0** (`versionCode 33`)
- Release atual: **Production Signed — v2/v3 Validated**
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
- pipeline compila debug, release de validação e release de produção assinado.

## Validação

A versão 1.4 passou por:

- 12/12 Pokédexes offline;
- 1.025/1.025 sprites PNG locais;
- Core 1.0: 17/17 verificações;
- regressões UI 1.1: 13/13, UI 1.2: 12/12 e UI 1.3: 11/11;
- Android release readiness: 11/11;
- sintaxe JavaScript;
- smoke test em Chrome real;
- persistência após fechamento/reabertura;
- compilação Android debug/release;
- inspeção física do APK;
- assinatura de produção verificada pelo `apksigner`.

## Release oficial v1.4.0

O APK de produção é assinado com o certificado definitivo do projeto e foi verificado com:

- APK Signature Scheme v2: **true**;
- APK Signature Scheme v3: **true**;
- signatários: **1**;
- algoritmo: **RSA 4096**;
- certificado SHA-256: `6af5c07977a8c8cb419c598c4cf184b47c7fa61a1173d3d170ff6e32a5cb0f5e`;
- APK SHA-256: `80718fd9394079d9d5af0f07a14f606993ee716cc5d227b9b90c8c6dfcb1d44e`.

O `minSdk` é 26, portanto a assinatura v2/v3 cobre os dispositivos suportados pelo aplicativo. A mesma chave de produção deve ser preservada para futuras atualizações.

## Regra do projeto

O foco é Pokédex/Living Dex, salvamento e acompanhamento da coleção. Não adicionar sistemas de missão, cronômetro ou gamificação fora da mecânica real dos jogos Pokémon.

Todo Pokémon exibido deve possuir imagem/ícone. Os 1.025 Pokémon da National Dex possuem sprite local empacotado no APK, com fontes remotas apenas como melhoria/fallback de maior resolução.

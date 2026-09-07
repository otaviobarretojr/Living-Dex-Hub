# Living Dex Hub — assinatura Android de produção

A configuração Gradle está pronta para usar uma chave de produção sem armazenar o keystore ou senhas no repositório.

## Variáveis esperadas pelo Gradle

- `RELEASE_STORE_FILE`: caminho local para o arquivo `.jks`.
- `RELEASE_STORE_PASSWORD`: senha do keystore.
- `RELEASE_KEY_ALIAS`: alias da chave. Para a chave criada para o projeto: `livingdex`.
- `RELEASE_KEY_PASSWORD`: senha da chave.

Quando as quatro variáveis estão presentes, `assembleRelease` usa a signing config de produção com assinatura v1, v2 e v3 habilitadas. Sem elas, o projeto continua conseguindo gerar o release unsigned usado pelos gates de CI.

## GitHub Actions

Nunca faça commit do `.jks`, senha ou conteúdo Base64 da chave. Para automatizar a assinatura, configure secrets privados no repositório e faça o workflow materializar o keystore somente no runner temporário.

Secrets recomendados:

- `LIVINGDEX_KEYSTORE_BASE64`
- `LIVINGDEX_KEYSTORE_PASSWORD`
- `LIVINGDEX_KEY_PASSWORD`

O alias permanece `livingdex`.

## Regra crítica

Preserve a chave de produção e as senhas em pelo menos duas cópias privadas e seguras. Futuras atualizações que precisem manter a identidade do aplicativo devem continuar usando a mesma chave de assinatura.

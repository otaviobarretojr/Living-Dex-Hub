# Living Dex Hub

Repositório oficial do projeto Living Dex Hub.

## Estado atual

- Baseline preservado: **Build 23.0 — Embedded Data Pack**
- Build de desenvolvimento atual: **Build 24.0 — Image Integrity**
- National Dex: 1.025 espécies
- Escopo atual: Let's Go, Sword/Shield, Brilliant Diamond/Shining Pearl, Legends: Arceus, Scarlet/Violet e Legends Z-A
- Recursos centrais: Living Dex, famílias evolutivas, formas, Storage/HOME, jogos possuídos, disponibilidade, exclusivos e engine de obtenção.

## Builds

### Build 23.0

O Build 23.0 original é preservado em `archive/build-23/` como snapshot comprimido e pode ser reconstruído com:

```bash
python tools/restore_build23.py
```

### Build 24.0

O Build 24 fecha a primeira etapa da auditoria final: **integridade das imagens Pokémon em todas as telas**.

Depois de restaurar o Build 23, gere o Build 24 com:

```bash
python tools/build_build24.py
```

O gerador impede a criação do Build 24 se ainda encontrar imagens Pokémon usando diretamente `src="${ART}..."`, sem o pipeline de fallback.

## Regra do projeto

O foco é Pokédex/Living Dex, salvamento e acompanhamento da coleção. Não adicionar sistemas de missão, cronômetro ou gamificação fora da mecânica real dos jogos Pokémon.

Todo Pokémon exibido deve possuir imagem/ícone com fallback. Para o APK final, os assets essenciais deverão ser empacotados localmente para funcionamento offline real.

## Próximos bloqueadores do Core 1.0

1. Empacotar imagens Pokémon locais/offline.
2. Executar e fechar a auditoria de obtenção dos 6 jogos.
3. Resolver rotas relevantes que ainda retornam confiança parcial ou método não fechado.
4. Validar persistência, backup/restauração e migração em teste real mobile.
5. Só então congelar o Core 1.0 e iniciar o rework visual/estrutura Android/APK.

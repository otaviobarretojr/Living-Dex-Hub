# Living Dex Hub — Design Master Roadmap

Status base: v7.14.0 consolidada e funcional.
Objetivo: transformar o Living Dex Hub em uma experiência visual premium, com linguagem inspirada nos produtos oficiais Pokémon/Nintendo, preservando a lógica já validada e usando o conceito visual aprovado como referência principal.

## Status executivo

- [x] F0 — Fundação / Design System — CONCLUÍDA em 08/09/2026
- [ ] F1 — Início premium — EM VALIDAÇÃO VISUAL (F1.3 funcional concluída)
- [ ] F2 — Seletor de jogo
- [ ] F3 — Detalhes do Pokémon 2.0
- [ ] F4 — Box premium
- [ ] F5 — Pesquisa global
- [ ] F6 — Habitat e Dados por jogo
- [ ] F7 — Identidade visual por jogo
- [ ] F8 — Splash / Loading / acabamento
- [ ] F9 — Navegação final
- [ ] F10 — Auditoria visual 1:1
- [ ] F11 — Auditoria funcional completa
- [ ] F12 — Release final

## Regras permanentes

1. A v7.14.0 é a base funcional. Nenhum rework visual pode quebrar Pokédex, Box, progresso, persistência, detalhes, evolução ou música.
2. O conceito visual aprovado é o Design Master. A implementação deve buscar fidelidade próxima de 1:1 em hierarquia, composição, espaçamento, cards, fundos, tipografia, ícones e estados.
3. Implementar e validar uma etapa por vez. Não avançar uma tela grande antes da anterior estar funcional e visualmente aprovada.
4. Evitar telas pretas/secas e grandes áreas vazias. Usar artwork, identidade do jogo atual, profundidade discreta, gradientes, texturas e composição visual sem poluição.
5. Existem dois contextos distintos: **jogo principal** e **jogo em consulta**. Só uma ação explícita de Trocar jogo altera o jogo principal.
6. Consultar uma Box de outro jogo não altera a jornada principal. O detalhe do Pokémon sempre herda o contexto da Box/origem em que foi aberto.
7. Box continua sendo a fonte autoritativa do registro do Pokémon e deve sincronizar com Início.
8. Biblioteca e Living Dex antigas não retornam como abas.
9. Recursos legados em quarentena não devem reaparecer na UI sem decisão explícita.
10. Assets existentes devem ser reaproveitados quando adequados. Novos assets só entram de forma controlada e coerente com o Design Master.
11. Cada fase termina com auditoria funcional, responsiva e visual antes do APK de produção.

## Fase 0 — Fundação / Design System — CONCLUÍDA

Entregas versionadas:
- `docs/design/DESIGN_SYSTEM_V8.md` — contrato visual oficial, tokens, componentes, responsividade, acessibilidade, movimento e checklist 1:1.
- `app/src/main/assets/design-system-v8.css` — tokens e primitives CSS compartilhados para as próximas telas.

Decisões fechadas:
- base visual dark navy/charcoal, não preto puro;
- vermelho coral como ação primária controlada;
- verde para progresso/registrado;
- superfícies claras reservadas para Box/listas quando coerentes com o Design Master;
- identidade contextual por jogo sem fragmentar o Design System;
- escala única de spacing 4/8/12/16/20/24/32/40;
- raios 10/14/18/24;
- touch target >=44 px;
- motion 100–240 ms e reduced-motion;
- mobile-first com referência principal 361–430 px;
- Início + Box permanecem como navegação atual; Pesquisa só entra após ser implementada;
- regra `Pokémon + jogo/versão da origem = contexto do detalhe` preservada.

Critério atingido: fundação visual definida sem reestruturar nem arriscar a lógica funcional da v7.14.0. A aplicação visual integral começa na F1.

## Fase 1 — Início premium

- Reestruturar o topo e identidade da Pokédex.
- Hero grande do jogo principal com artwork, região, progresso e CTA Continuar.
- Ação Trocar jogo integrada ao hero e tratada como alteração explícita da jornada principal.
- Grade/cartões dos seis jogos com identidade visual própria e progresso real.
- Cards de jogos podem ser usados para **consulta**, sem trocar silenciosamente o jogo principal.
- Reduzir áreas pretas vazias e melhorar hierarquia, profundidade e composição.
- Manter sincronização Início ↔ Box.

### F1.3 — Arquitetura de contexto — CONCLUÍDA

- `primaryGame`: jogo/jornada principal escolhida explicitamente.
- `boxContextGame`: jogo atualmente consultado na Box.
- `detailContextGame`: herdado do runtime/Box de onde o Pokémon foi aberto.
- `Continuar` abre a Box do jogo principal.
- Selecionar outro jogo dentro da Box muda apenas a consulta.
- Tocar em um card de outro jogo na Home abre consulta da Box sem alterar a jornada principal.
- `Trocar jogo` é a única ação da Home que altera o jogo principal.
- voltar para a Home preserva a jornada principal mesmo após consultar outro jogo.

Critério: tela inicial visualmente próxima do Design Master, dados reais e sem mudanças acidentais de contexto.

## Fase 2 — Seletor de jogo

- Tela dedicada Trocar jogo.
- Cards premium para Scarlet/Violet, Legends Z-A, Sword/Shield, BDSP, Let's Go e Legends Arceus.
- Mostrar região e progresso real.
- O seletor principal altera explicitamente `primaryGame`.
- A Box pode usar o mesmo componente visual em modo consulta, alterando apenas `boxContextGame`.
- Preparar distinção de versão quando necessária: Scarlet/Violet, Sword/Shield, BD/SP e Let's Go Pikachu/Eevee.

## Fase 3 — Detalhes do Pokémon 2.0

Transformar o detalhe em perfil completo e modular.

### Cabeçalho
- artwork grande do Pokémon;
- número, nome, jogo/contexto;
- tipos;
- estado Adicionar / Na Box;
- fundo visual relacionado ao Pokémon/jogo sem comprometer legibilidade.

### Aba Sobre
- nome/número;
- tipo(s);
- altura;
- peso;
- descrição Pokédex apropriada ao contexto quando disponível;
- informações essenciais, sem excesso.

### Aba Evolução
- linha evolutiva completa;
- nível, item, troca, amizade e métodos especiais;
- preservar dicas especiais já consolidadas;
- apresentar método de maneira curta e prática;
- prever fallback local/seguro quando fonte externa não estiver disponível.

### Aba Habitat
Regra central: Pokémon + jogo/versão da origem = contexto do habitat.

- mostrar apenas localização pertinente ao jogo/versão selecionado na consulta;
- área/rota;
- método de encontro quando relevante;
- condição/horário/clima quando relevante;
- exclusividade de versão;
- dica curta útil;
- se não houver captura selvagem, explicar corretamente evolução, troca, transferência, evento ou indisponibilidade, sem inventar habitat.

### Aba Dados
- tipos;
- habilidades;
- stats base;
- informações técnicas realmente úteis;
- apresentação compacta e legível.

Critério: apenas uma aba de conteúdo aberta por vez; mais informação total com menos poluição visual.

## Fase 4 — Box premium

- Preservar 30 slots por Box e lógica já validada.
- Reproduzir cabeçalho/contexto do jogo do Design Master.
- Navegação clara entre Box 1, Box 2, etc.
- Seletor da Box funciona como consulta e não altera o jogo principal.
- Estados registrado/faltante visualmente distintos.
- Melhorar slots, número, miniatura e feedback de toque.
- Manter abertura do detalhe pelo Pokémon e herança do contexto consultado.
- Manter performance e encaixe mobile.

## Fase 5 — Pesquisa global

Nova função deliberada, não apenas decoração do conceito.

- pesquisa por nome e número;
- filtros Todos / Registrados / Faltando;
- considerar Favoritos somente se a função for aprovada/implementada;
- resultados no contexto da consulta/jogo escolhido para pesquisa;
- abrir diretamente Detalhes do Pokémon preservando o contexto de origem;
- decidir após validação se Pesquisa entra na navegação inferior como terceiro item.

## Fase 6 — Habitat e dados por jogo: cobertura completa

- auditar os Pokémon das seis experiências suportadas;
- estruturar fonte de dados de habitat por jogo/versão;
- validar exclusividades e métodos especiais;
- garantir que o mesmo Pokémon apresente habitat diferente quando o jogo exigir;
- criar validação automática contra entradas vazias/incompatíveis;
- tratar DLCs e Pokédex secundárias de forma explícita sem misturá-las silenciosamente à Box principal.

## Fase 7 — Identidade visual por jogo

- fundos, hero, acentos e artworks coerentes para cada jogo;
- Scarlet/Violet;
- Legends Z-A;
- Sword/Shield;
- Brilliant Diamond/Shining Pearl;
- Let's Go Pikachu/Eevee;
- Legends Arceus.

A identidade muda com o jogo, mas componentes e ergonomia permanecem consistentes.

## Fase 8 — Splash / Loading / acabamento premium

- splash/loading inspirado no conceito aprovado;
- transições discretas;
- estados de carregamento;
- feedback de interação;
- microanimações sem prejudicar desempenho;
- revisar ícone/app branding interno e telas vazias.

## Fase 9 — Navegação final

- revisar Início e Box;
- avaliar Pesquisa como terceiro item após a função estar pronta;
- padronizar estados ativo/inativo;
- garantir que telas secundárias não criem navegação duplicada;
- comportamento correto de voltar/fechar no Android.

## Fase 10 — Auditoria visual 1:1

Para cada tela principal:
- capturar implementação real;
- comparar com Design Master;
- corrigir proporção, espaçamento, tipografia, tamanho dos cards, ícones, imagens, alinhamentos e densidade;
- testar telas menores/maiores;
- eliminar resquícios visuais da interface antiga.

Nenhuma diferença relevante deve ser aceita apenas porque está funcional.

## Fase 11 — Auditoria funcional completa

Revalidar:
- 12 Pokédex embutidas;
- 6 Boxes principais;
- 1.025 assets Pokémon;
- sequência e correspondência das Dex;
- jogo principal vs jogo consultado;
- Início ↔ Box;
- adicionar/remover;
- persistência após reiniciar;
- troca explícita de jogo principal;
- consulta de outro jogo sem alteração da jornada;
- contexto de versão;
- Sobre/Evolução/Habitat/Dados;
- busca e filtros;
- música local;
- navegação/back;
- funcionamento offline onde aplicável;
- regressões e código legado/quarentena.

## Fase 12 — Release final

- limpeza técnica final;
- validações CI obrigatórias;
- build release;
- assinatura de produção;
- verificação do APK;
- SHA-256;
- entrega do APK final.

## Ordem de execução aprovada

F0 Design System → F1 Início → F2 Trocar jogo → F3 Detalhes 2.0 → F4 Box → F5 Pesquisa → F6 cobertura Habitat/Dados → F7 identidade por jogo → F8 Splash/acabamento → F9 navegação → F10 auditoria 1:1 → F11 auditoria funcional → F12 release.

## Decisões que não devem ser esquecidas

- Uso pessoal; objetivo visual é sensação de produto Pokémon/Nintendo premium.
- Não basta ficar inspirado: buscar alta fidelidade ao conceito aprovado.
- O app deve parecer rico e profissional, não uma tela preta com cards soltos.
- Mostrar mais informação por organização e abas, não colocando tudo simultaneamente na tela.
- **Trocar contexto de consulta não é trocar jogo principal.**
- `Continuar` sempre segue o jogo principal.
- Box pode consultar qualquer jogo suportado sem alterar a jornada principal.
- O detalhe sempre herda o jogo/versão da Box/origem em que o Pokémon foi aberto.
- Habitat nunca deve misturar jogos.
- Se o Pokémon foi aberto pela Box de Let's Go, Habitat é de Let's Go; se aberto por Sword/Shield, Habitat é de Sword/Shield, e assim por diante.
- Diferenças de versão devem ser respeitadas quando afetarem encontros/informações.
- A arte conceitual pode sugerir funções novas, mas elas só entram deliberadamente. Pesquisa foi aprovada como candidata real; Favoritos ainda depende de decisão.
- O comportamento funcional aprovado da v7.14.0 é a rede de segurança de todas as fases.

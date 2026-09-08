# Living Dex Hub — Design System v8

Status: Fase 0 — Fundação visual
Referência visual: conceito Design Master aprovado pelo usuário em 08/09/2026.
Base funcional protegida: v7.14.0.

## 1. Princípio

O Design Master é referência de composição, densidade, hierarquia e sensação visual. A interface deve parecer uma Pokédex premium, rica e contextual, sem copiar cegamente funções apenas sugeridas pelo conceito.

A camada visual nunca pode alterar silenciosamente a lógica de Box, progresso, Pokédex, persistência, evolução ou música.

## 2. Tokens — cor

### Base
- `--ld-bg-0: #071019` — fundo principal profundo.
- `--ld-bg-1: #0B1621` — superfície de navegação/cabeçalho.
- `--ld-bg-2: #101E2B` — cards escuros.
- `--ld-surface: #142331` — superfície elevada.
- `--ld-surface-soft: rgba(20,35,49,.82)` — superfície sobre artwork.
- `--ld-line: rgba(255,255,255,.09)` — divisores.
- `--ld-text: #F7FAFC` — texto principal.
- `--ld-text-2: #A9B6C2` — texto secundário.
- `--ld-text-3: #71808E` — metadados.

### Ação
- `--ld-action: #FF3946` — ação primária / seleção.
- `--ld-action-pressed: #E52F3B`.
- `--ld-success: #20C997` — registrado / progresso positivo.
- `--ld-missing: #AAB4BE` — silhueta/faltante.
- `--ld-white-surface: #F8FAFC` — Box/listas claras do conceito.
- `--ld-dark-on-light: #17212B`.

### Contexto por jogo
Cores contextuais são acentos e glows; não substituem os tokens estruturais.
- Scarlet/Violet: vermelho coral + violeta.
- Legends Z-A: teal/ciano.
- Sword/Shield: azul elétrico + magenta discreto.
- BDSP: azul safira + rosa suave.
- Let's Go: amarelo quente + âmbar.
- Legends Arceus: azul acinzentado + creme.

## 3. Tipografia

Usar stack Android/Web segura e geométrica, sem depender de fonte proprietária:
`Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif`.

Escala mobile:
- Display: 30/34, peso 800.
- H1: 24/29, peso 800.
- H2: 20/25, peso 750.
- H3: 17/22, peso 700.
- Body: 14/20, peso 450–500.
- Small: 12/17, peso 500–600.
- Micro: 10/14, peso 650; tracking +.02em.
- Número Pokédex/eyebrow: 12/16, peso 800, tracking +.04em.

Nomes e números devem ter hierarquia forte; textos auxiliares nunca competem com o Pokémon/jogo.

## 4. Espaçamento

Escala única: 4, 8, 12, 16, 20, 24, 32, 40 px.
- Margem horizontal principal mobile: 16 px.
- Gap padrão de cards: 12 px.
- Padding card compacto: 12 px.
- Padding card principal/hero: 16–20 px.
- Espaço mínimo antes da bottom nav: 12 px + safe-area.

## 5. Raios e elevação

- `--ld-radius-sm: 10px`
- `--ld-radius-md: 14px`
- `--ld-radius-lg: 18px`
- `--ld-radius-xl: 24px`
- pill: 999px.

Sombras devem ser discretas e usadas para separar planos, não como decoração pesada.
- Card: `0 8px 24px rgba(0,0,0,.22)`.
- Hero: `0 16px 40px rgba(0,0,0,.32)`.
- Sheet/modal: `0 -16px 48px rgba(0,0,0,.42)`.

## 6. Componentes canônicos

### App Header
44–56 px úteis + safe-area. Título forte, subtítulo/contexto opcional, no máximo duas ações à direita. Nunca criar barra superior excessivamente alta.

### Hero Game Card
Artwork ocupa a composição; gradiente escuro protege texto. Deve conter jogo, região, progresso real e CTA. Artwork não pode virar mero thumbnail pequeno.

### Game Card
Imagem de fundo + overlay; nome, região e progresso. Estado selecionado recebe borda/glow contextual sutil. Grid mobile 2 colunas quando usado na tela Trocar jogo; Home pode usar composição 3×2 se largura permitir sem comprimir texto.

### Primary Button
Altura 44–48 px, radius 12–14, fundo action, texto branco 700. Pressed reduz brilho/escala de forma mínima.

### Secondary Button
Mesma altura, superfície escura/elevada, borda sutil.

### Type Chip
Pill compacta, ícone opcional, label uppercase ou title case consistente. Cor sem sacrificar contraste.

### Progress
Track 4–6 px, preenchimento contextual/success, valor numérico sempre legível fora do track quando necessário.

### Tabs
Uma linha, alvo de toque >=44 px. Ativa com texto forte + indicador action de 3 px. Apenas uma área de conteúdo visível.

### Box Slot
Grid 6×5 preservado quando a altura permitir. Número pequeno no topo, sprite central, registrado com superfície levemente contextual; faltante em silhueta/cinza. Alvo de toque nunca menor que 44 px quando possível.

### Pokémon Row
Sprite 40–48 px, número/nome, chips, ação opcional à direita. Divisor leve; lista clara pode usar `--ld-white-surface`.

### Sheet / Detail Surface
Topo visual pode usar artwork/fundo contextual; conteúdo abaixo deve ter contraste estável. Bordas superiores 20–24 px quando sheet; tela dedicada segue App Header.

### Empty / Loading / Error
Mensagem curta + ilustração/ícone discreto + ação quando útil. Nunca exibir grande vazio preto sem orientação.

## 7. Fundos e artwork

Cada tela deve possuir três planos:
1. fundo estrutural escuro;
2. identidade contextual do jogo/Pokémon por glow, gradiente ou artwork;
3. superfície de conteúdo legível.

Artwork nunca deve comprometer texto. Usar overlays/gradientes, `object-fit: cover/contain` conforme função e ponto focal. Não esticar imagem.

## 8. Movimento

- toque/press: 100–140 ms;
- tabs/cards: 160–200 ms;
- mudança de tela/sheet: 200–240 ms;
- easing preferido: `cubic-bezier(.2,.8,.2,1)`.

Respeitar `prefers-reduced-motion`. Não usar animações contínuas decorativas.

## 9. Responsividade

Mobile-first.
- Compacto: <=360 px.
- Base: 361–430 px — referência principal Android.
- Large phone: 431–600 px.
- Tablet/web: >600 px; limitar largura de leitura e evitar esticar cards indefinidamente.

Safe areas obrigatórias em topo e bottom nav. Nenhum CTA importante pode ficar atrás da barra do sistema.

## 10. Acessibilidade e ergonomia

- contraste mínimo AA para texto funcional;
- toque ideal >=44×44 px;
- estado não pode depender apenas de cor;
- texto pode crescer sem cortar ações essenciais;
- foco visível no ambiente web;
- imagens decorativas não devem gerar ruído semântico.

## 11. Navegação

Na Fase 0 permanece a arquitetura aprovada da base: Início + Box. Pesquisa só entra como terceiro destino depois de implementada e validada na fase correspondente. Biblioteca/Living Dex antigas não retornam.

## 12. Regra contextual do detalhe

`Pokémon + jogo atual + versão = contexto do detalhe`.

Sobre, Evolução, Habitat e Dados compartilham o mesmo cabeçalho do Pokémon, mas apenas uma aba apresenta conteúdo por vez. Habitat nunca mistura jogos/versões.

## 13. Checklist visual obrigatório por fase

- [ ] composição corresponde ao Design Master;
- [ ] densidade e hierarquia equivalentes;
- [ ] não há grandes vazios sem intenção;
- [ ] artwork tem ponto focal e overlay corretos;
- [ ] tipografia segue escala;
- [ ] spacing segue tokens;
- [ ] raios/sombras consistentes;
- [ ] estados active/pressed/disabled/empty definidos;
- [ ] contraste e touch targets verificados;
- [ ] 360 px, 390–430 px e >430 px testados;
- [ ] lógica funcional anterior continua intacta.

## 14. Critério de saída da Fase 0

A Fase 0 termina quando este Design System e o contrato técnico de implementação estiverem definidos e versionados, sem reestruturar ainda as telas de produção. A primeira aplicação visual completa desses tokens acontece na Fase 1 — Início Premium.

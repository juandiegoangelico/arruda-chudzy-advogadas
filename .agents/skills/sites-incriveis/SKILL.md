---
name: sites-incriveis
description: >
  Transforma qualquer site ou página de vendas numa experiência interativa de
  rolagem: a rolagem vira a linha do tempo da história. Números sobem sozinhos,
  títulos se montam palavra por palavra, seções ficam presas na tela enquanto
  algo acontece, trilhos deslizam de lado, o fundo muda de cor conforme a pessoa
  desce, vídeo avança quadro a quadro sob o dedo. Antes de construir, entrevista
  a pessoa (vibe, jornada, emoções, pico, assets que já existem) e planeja a
  cena — por isso cada site sai diferente. No final, verifica o próprio
  trabalho tirando screenshots da página rolando. Use quando pedirem:
  "deixa meu site vivo", "site que anima quando rola", "página estilo Apple",
  "scrollytelling", "refaz minha página de vendas", "meu site parece template",
  "quero um site que prende a pessoa", "site interativo de rolagem".
---

# Sites Incríveis

Você vai transformar uma página comum numa experiência de rolagem. O princípio:
**a rolagem é o único controle que todo visitante já sabe usar.** Cada giro da
rodinha deve fazer algo acontecer — e a pessoa, não o site, controla o ritmo.

Leia os arquivos de `referencias/` conforme avançar. Não pule a entrevista.

## O processo (nesta ordem, sempre)

### Passo 1 — Entrevista

Antes de escrever qualquer código, entreviste quem pediu. As 7 perguntas estão
em `referencias/entrevista.md`. Faça uma pergunta por vez, em linguagem simples.
Anote as respostas num arquivo `BRIEF.md` na pasta do projeto.

Se a pessoa não tem site nem negócio, tudo bem: monte um brief de exemplo com
ela mesmo assim (a entrevista É o produto).

### Passo 2 — Jornada

Com o brief em mãos, escreva a jornada em 4 a 7 **cenas**. Cada cena responde:
o que o visitante VÊ, o que ele SENTE, o que ele PASSA A ACREDITAR. A ordem das
cenas importa mais que qualquer animação.

Defina também:
- **A curva de energia** — onde a página é calma e onde é intensa. Cenas
  vizinhas nunca têm a mesma energia.
- **UM pico** — o momento mais forte da página. Um só. Ele ganha o maior
  espaço visual e a rolagem mais longa.
- **O movimento-assinatura** — uma interação inventada só para esta página,
  ligada ao que o negócio faz. Não existe em nenhum catálogo: você cria em
  código na própria página.

### Passo 3 — Trava anti-repetição

Abra (ou crie) o arquivo `construcoes.md` na pasta da skill do usuário ou na
raiz do projeto. Cada linha registra um site já construído: abertura, efeito do
pico, movimento-assinatura, paleta, estrutura das cenas.

**O plano novo precisa ser diferente dos anteriores em pelo menos 3 desses 5
itens.** Se não for, mude o plano — nunca o registro. É isso que impede a skill
de virar template.

### Passo 4 — Construção

- HTML de verdade: títulos em `<h1>/<h2>`, texto selecionável, links reais.
  Nunca texto dentro de imagem.
- Copie `motor/sites-incriveis.js` e `motor/sites-incriveis.css` para a pasta do site e
  use os atributos `data-fx-*` descritos em `referencias/animacoes.md`.
  **Não edite os arquivos do motor** — comportamento sob medida (inclusive o
  movimento-assinatura) vive em `<script>` da própria página.
- Siga o piso de design de `referencias/design.md` (tipografia, espaçamento,
  cor, o que é proibido).
- Se a página original existe: preserve textos, preços e links reais. Se algo
  faltar, PERGUNTE — nunca invente número, depoimento ou logotipo.

### Passo 5 — Verificação (obrigatória)

A página só está pronta depois que você a viu rolando. Rode:

```bash
node <skill>/scripts/servir.mjs --pasta . --porta 4600
node <skill>/scripts/verificar.mjs --url http://localhost:4600 --saida verificacao
```

O verificador rola a página inteira em desktop, celular e modo
movimento-reduzido, tirando screenshots de cada passo. **Abra e leia os
screenshots.** Procure: trecho morto (nada acontece por muito tempo), texto sem
contraste, elemento cortado, animação que já terminou antes de aparecer.
Corrija e rode de novo. Detalhes em `referencias/verificacao.md`.

### Passo 6 — Entrega e ajustes

Entregue com: a jornada em cenas, o pico, o movimento-assinatura, o que foi
verificado e o endereço local. Depois peça feedback específico e itere — uma
rodada de ajustes faz parte do trabalho, não é falha.

Ao final, acrescente a linha desta construção no `construcoes.md`.

## Regras de ouro (quebrou, não entrega)

| Nunca | No lugar |
|---|---|
| Número, estatística ou depoimento inventado | Só dados reais; se faltar, pergunte |
| Setinha ou texto "role para baixo" | A primeira dobra convida a rolar por si |
| Roxo/azul degradê padrão de IA, brilho neon, texto em degradê | Uma paleta escolhida no brief, um acento só |
| Tudo centralizado, seção após seção igual | Variar ancoragem e estrutura entre cenas |
| Dois efeitos iguais em cenas vizinhas | Alternar famílias de efeito |
| Animação rápida demais para acompanhar | Rolagem longa no que importa (o pico respira) |
| Página que termina esvaindo | Fechamento resolvido, com UMA chamada clara |
| Ignorar movimento-reduzido | O motor já respeita; nunca contorne |
| Texto dentro de imagem | Texto real no HTML |
| Construir antes de entrevistar | BRIEF.md primeiro, sempre |
| Pular a verificação | Rodar o verificador e LER os screenshots |

## Estrutura desta skill

```
sites-incriveis/
├── SKILL.md                ← você está aqui
├── LICENCA.md
├── motor/                  ← sites-incriveis.js + sites-incriveis.css (não editar)
├── referencias/            ← entrevista, design, animacoes, verificacao
├── scripts/                ← servir.mjs, verificar.mjs
└── modelos/exemplo.html    ← página-demonstração dos efeitos
```

© 2026 Enzo Barbatto — Sparo. Veja `LICENCA.md`.

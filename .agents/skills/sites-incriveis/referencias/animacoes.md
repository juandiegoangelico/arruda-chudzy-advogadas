# Catálogo de efeitos do motor

Tudo funciona por atributos `data-fx-*` no HTML. O motor
(`motor/sites-incriveis.js` + `motor/sites-incriveis.css`) lê os atributos e anima.
**Nunca edite o motor** — efeito sob medida (movimento-assinatura) vai em
`<script>` na própria página.

Antes de usar: incluir no `<head>` / fim do `<body>`:

```html
<link rel="stylesheet" href="sites-incriveis.css">
<script src="sites-incriveis.js" defer></script>
```

## Família 1 — Revelações (elemento entra na tela)

```html
<h2 data-fx="subir">Aparece subindo</h2>
<p  data-fx="surgir" data-fx-atraso="150">Só aparece (com atraso em ms)</p>
<img data-fx="esquerda" src="...">   <!-- entra da esquerda -->
<img data-fx="direita"  src="...">   <!-- entra da direita -->
<div data-fx="crescer">Entra crescendo de 92% pra 100%</div>
```

- `data-fx-atraso="200"` — espera antes de animar (bom pra sequência).
- `data-fx-duracao="1200"` — duração da transição.

## Família 2 — Texto que se monta

```html
<h1 data-fx="palavras">Cada palavra sobe na sua vez</h1>
<p  data-fx="digitar">Este texto é datilografado com cursor.</p>
```

Use `palavras` no máximo 2 vezes por página (título de abertura e pico).
`digitar` é forte — uma vez só.

## Família 3 — Números que sobem

```html
<span data-fx="contar" data-fx-fim="4415">0</span>
<span data-fx="contar" data-fx-fim="70" data-fx-prefixo="R$ " data-fx-sufixo=" mil">0</span>
<span data-fx="contar" data-fx-fim="4.9" data-fx-decimais="1">0</span>
```

Formata em pt-BR automaticamente. Só números REAIS.

## Família 4 — Cena fixa (o visitante rola, a cena acontece)

A estrutura: a seção define quantas "telas" de rolagem a cena dura; o palco
fica preso enquanto isso.

```html
<section data-fx-fixa data-fx-altura="4">
  <div class="fx-palco">
    <!-- o que fica preso na tela -->
  </div>
</section>
```

Enquanto preso, a seção recebe a variável CSS `--progresso` (0 → 1). Filhos
podem reagir de três jeitos:

**a) Interpolação direta** (o canivete suíço — serve pra quase tudo):

```html
<img data-fx-y="120,-80"          src="...">  <!-- sobe 200px durante a cena -->
<div data-fx-x="0,-400" data-fx-faixa="0.3,0.9">…</div>
<h2  data-fx-escala="0.7,1" data-fx-opacidade="0,1">…</h2>
<img data-fx-giro="-8,8" src="...">
```

`data-fx-faixa="0.3,0.9"` limita o efeito a um trecho do progresso — é assim
que você coreografa vários elementos na mesma cena, um após o outro.

**b) Etapas** (uma coisa por vez, estilo apresentação):

```html
<section data-fx-fixa data-fx-altura="4" data-fx-etapas="3">
  <div class="fx-palco">
    <div class="fx-etapa">Primeiro ponto</div>
    <div class="fx-etapa">Segundo ponto</div>
    <div class="fx-etapa">Terceiro ponto</div>
  </div>
</section>
```

A seção ganha `data-etapa="1..3"` conforme a rolagem; o CSS padrão mostra uma
etapa por vez (sobreponha no CSS da página pra layouts especiais).

**c) Trilho horizontal** (galeria que desliza de lado):

```html
<section data-fx-fixa data-fx-altura="3">
  <div class="fx-palco">
    <div data-fx="trilho">
      <article>…</article><article>…</article><article>…</article>
    </div>
  </div>
</section>
```

**d) Vídeo controlado pela rolagem**:

```html
<section data-fx-fixa data-fx-altura="5">
  <div class="fx-palco">
    <video data-fx="rolar-video" src="cena.mp4" muted playsinline preload="auto"></video>
  </div>
</section>
```

O vídeo avança/retrocede com a rodinha. Pra ficar liso, o arquivo precisa de
keyframes densos — reencode com:
`ffmpeg -i entrada.mp4 -an -g 8 -vf scale=1600:-2 -crf 23 saida.mp4`
(`-g 8` = keyframe a cada 8 quadros; `-an` remove o áudio). Máximo 2 cenas de
vídeo por página.

## Família 5 — Profundidade

```html
<img data-fx-paralaxe="0.25" src="...">  <!-- flutua contra a rolagem -->
<div data-fx-mouse="14">…</div>          <!-- acompanha o ponteiro de leve -->
```

Paralaxe: 0.1 sutil, 0.4 forte. Fora de cenas fixas apenas (dentro, use
`data-fx-y`). `data-fx-mouse` ignora telas de toque sozinho.

## Família 6 — Fundo que viaja

```html
<section data-fx-fundo="#14100C" data-fx-tinta="#F4EDE2">…</section>
<section data-fx-fundo="#F4EDE2" data-fx-tinta="#14100C">…</section>
```

Quando a seção domina a tela, o fundo e a cor de texto da página fazem a
transição. Ótimo pra marcar mudança de ato na história.

## Regras de combinação

- Cenas vizinhas nunca repetem a mesma família.
- Máximo de 2 cenas fixas de vídeo; o pico é UMA cena fixa longa (altura 4–5).
- Revelações são o tecido comum entre cenas fixas — não abuse: se tudo revela,
  nada revela.
- Movimento-assinatura: código próprio na página. Pode ler `--progresso` de
  qualquer cena fixa via JS (`getComputedStyle(secao).getPropertyValue("--progresso")`)
  para sincronizar com a rolagem.

# Piso de design — o mínimo que toda página Sites Incríveis respeita

Animação não salva design ruim. Antes de animar, a página parada já tem que
parecer cara. Este é o piso; o teto vem do brief.

## Tipografia

- **Duas fontes, papéis claros**: uma de display (títulos, com personalidade)
  e uma de texto (leitura). Escolha a dupla a partir da vibe do brief — nunca
  a mesma dupla de um build anterior (confira o `construcoes.md`).
- Escala definida antes de escrever CSS (ex.: 15 / 18 / 24 / 36 / 56 / 88) e
  respeitada em toda a página. Título de abertura pode ser enorme; texto de
  leitura nunca abaixo de 15px.
- Linha de texto corrido: 60–70 caracteres. Mais que isso cansa.
- Rótulos em caixa alta: tamanho pequeno + espaçamento de letra (~0.08em).
- Números que se comparam entre si: `font-variant-numeric: tabular-nums`.

## Cor

- **Uma paleta com papel definido**: fundo, superfície, tinta (texto), tinta
  suave, UM acento. O acento aparece poucas vezes — botão principal, pico,
  detalhe. Se está em todo lugar, não é acento.
- Neutro escolhido, não herdado: cinza com um leve puxão pra cor do acento
  parece decisão; cinza puro parece esqueleto.
- Contraste de leitura sempre: texto sobre foto ou vídeo ganha uma sombra de
  proteção localizada — nunca uma manta escura sobre a tela inteira.
- Proibido: degradê roxo/azul "cara de IA", texto em degradê, brilho neon,
  sombras coloridas gritantes.

## Espaço e estrutura

- Espaçamento em escala (8 / 16 / 24 / 40 / 64 / 104…), não a olho.
- Variar a ancoragem entre cenas: uma cena ancora à esquerda, outra centraliza,
  outra ocupa a tela inteira. Página onde toda seção é "título centralizado +
  três cartões" é template — exatamente o que esta skill existe pra evitar.
- Numeração de seção, contador "01/06", migalha decorativa: só se a ordem
  significa algo de verdade. Na dúvida, corte.
- O rodapé fecha: chamada única e clara, contatos, fim. Página que termina
  murchando desperdiça a atenção que o resto construiu.

## Movimento

- O movimento serve à história, não à vitrine. Cada efeito responde: "o que o
  visitante entende a mais por causa disso?" Sem resposta, corte o efeito.
- Devagar no que importa: o pico ganha rolagem longa (cena fixa com altura 3–5
  telas). Efeito que passa rápido demais é efeito que não existiu.
- Duas cenas vizinhas nunca usam a mesma família de efeito.
- Anime `transform` e `opacity` — nunca `width`, `height`, `top`, `left`
  (trava a rolagem em máquina fraca).
- Movimento-reduzido é sagrado: o motor já desliga tudo sozinho; confira no
  passo de verificação que a página inteira continua legível parada.

## Conteúdo

- Texto real, selecionável, no HTML — nunca dentro de imagem.
- Números, preços, depoimentos e logotipos: só os reais do brief.
- Links apontando pros destinos verdadeiros (checkout, WhatsApp, agenda).
- Ortografia impecável. Voz do dono, não voz de folheto.

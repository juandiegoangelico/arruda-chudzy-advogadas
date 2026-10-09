# Verificação — a página só existe depois que você a viu rolando

O harness não sente rolagem. Screenshots sentem. Por isso este passo é
obrigatório e vem ANTES de mostrar o resultado pra pessoa.

## Como rodar

```bash
# 1. na pasta do site (uma vez):
npm i playwright-core

# 2. servir
node <skill>/scripts/servir.mjs --pasta . --porta 4600

# 3. em outro terminal, verificar
node <skill>/scripts/verificar.mjs --url http://localhost:4600 --saida verificacao
```

O verificador usa o Chrome já instalado na máquina. Ele rola a página em
passos de 75% da tela e fotografa cada passo, em três condições:

- `verificacao/desktop/` — 1440×900
- `verificacao/celular/` — 390×844
- `verificacao/reduzido/` — página inteira com movimento-reduzido ligado

E escreve `verificacao/RELATORIO.md` com erros de console/página.

## O que você DEVE fazer com os screenshots

**Abrir e ler um por um, na ordem.** Você tem visão — use. Procure:

1. **Trecho morto** — dois passos seguidos quase idênticos significam rolagem
   sem recompensa. Ou a cena está longa demais, ou falta algo acontecer ali.
2. **Contraste** — todo texto legível sobre o fundo daquele exato momento
   (fundos que viajam mudam o jogo no meio da cena).
3. **Cortes** — títulos, botões ou imagens cortados na borda. Confira o
   celular com o dobro de atenção: é onde tudo quebra primeiro.
4. **Ritmo** — o pico aparece com espaço de sobra? Efeitos importantes
   aparecem já terminados (= animação disparou cedo demais)?
5. **Estado inicial** — o passo 1 convida a rolar sem precisar de setinha?
6. **Reduzido** — a versão sem movimento mostra TODO o conteúdo, legível,
   na ordem certa? (É a página que leitores de tela e muita gente sensível a
   movimento vai usar.)

## Depois de corrigir

Rode o verificador de novo. Repita até uma passada limpa. Só então mostre o
resultado, junto com um resumo honesto: o que foi verificado, o que ficou de
fora (ex.: toque real em celular físico, autoplay em iOS) e o que recomenda
testar à mão.

# SKILL: cardapio-digital  (Fase 3 · dono: @Sites)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Cliente fechado pede cardápio.

## Entradas
`modelos/DESIGN.md`, cardápio do cliente

## Passos
1. Bloquear se DESIGN.md estiver ausente.
2. Gerar HTML para celular, seguindo o DESIGN.md.
3. Salvar em `handoff/cardapio-<slug>.html`.

## Saída
HTML em `handoff/`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/cardapio-digital-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

# SKILL: critica-proposta  (Fase 2 · dono: @Critical)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Toda proposta antes de ir ao cliente.

## Entradas
`handoff/proposta-<slug>.md`

## Passos
1. Rodar `python scripts/verificar_texto.py` no arquivo. Se falhar: REPROVADO.
2. Apontar os 3 furos principais.
3. Checar promessa velada e valor mínimo.
4. Emitir APROVADO, REVISAR ou REPROVADO com a razão.

## Saída
Veredito anexado à proposta.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/critica-proposta-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

# SKILL: follow-up-3-dias  (Fase 1 · dono: Maestro)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Rotina 08h.

## Entradas
`funil/leads.csv`

## Passos
1. Achar leads com `data_followup` de hoje ou antes e status diferente de `fechado`/`perdido`.
2. Ordenar por receita, risco, prazo.
3. Incluir no resumo das 08h.
4. NÃO enviar nada ao cliente.

## Saída
Alerta no resumo.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/follow-up-3-dias-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

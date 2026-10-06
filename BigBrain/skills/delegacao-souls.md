# SKILL: delegacao-souls  (Fase 1 · dono: Maestro)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Pedido que não é do Maestro.

## Entradas
Pedido do Augusto

## Passos
1. Consultar `_map.md`: qual soul/skill cobre o pedido.
2. Invocar a soul com o contexto necessário (só do cliente em questão).
3. Salvar o resultado em `handoff/`.
4. Avisar o Augusto e registrar no ledger.

## Saída
Resultado da soul em `handoff/`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/delegacao-souls-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

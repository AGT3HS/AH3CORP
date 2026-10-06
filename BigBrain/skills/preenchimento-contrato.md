# SKILL: preenchimento-contrato  (Fase 2 · dono: @Propostas)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Lead `fechado`.

## Entradas
`modelos/contrato_base.md`, dados do cliente

## Passos
1. Bloquear se o status não for `fechado`.
2. Copiar o modelo e preencher todos os [COLCHETES]; se faltar dado, parar e pedir.
3. Marcar o pacote na cláusula 1.1.
4. Salvar em `handoff/contrato-<slug>-<data>.md`.
5. Registrar no ledger.

## Saída
Contrato em `handoff/` para o Augusto revisar.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/preenchimento-contrato-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

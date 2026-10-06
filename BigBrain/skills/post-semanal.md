# SKILL: post-semanal  (Fase 3 · dono: @GestãoLocal)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Semanal, por cliente com contrato assinado.

## Entradas
`clientes/<slug>/`, `conteudo/calendario.md`

## Passos
1. Confirmar contrato assinado.
2. Escrever rascunho: gancho, corpo, chamada final honesta.
3. Rodar `verificar_texto.py`.
4. Salvar em `handoff/post-<slug>-<data>.md`.

## Saída
Rascunho em `handoff/`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/post-semanal-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

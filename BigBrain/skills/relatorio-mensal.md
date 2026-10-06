# SKILL: relatorio-mensal  (Fase 3 · dono: @GestãoLocal)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Primeiro dia útil do mês, por cliente.

## Entradas
`clientes/<slug>/`, métricas do mês

## Passos
1. Reunir métricas disponíveis (não inventar as que faltam).
2. Gerar PDF com `gerar_relatorio.py`.
3. Salvar em `clientes/<slug>/relatorios/<AAAA-MM>.pdf`.

## Saída
PDF do mês.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/relatorio-mensal-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

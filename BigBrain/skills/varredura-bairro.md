# SKILL: varredura-bairro  (Fase 1 · dono: Radar)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Augusto diz "varre o bairro X".

## Entradas
Bairro, cidade (padrão Florianópolis), chave em `.env`

## Passos
1. Buscar restaurantes e bares do bairro na Places API.
2. Filtrar nota 3.5 a 4.5 e pelo menos 10 avaliações.
3. Ordenar: nota mais baixa com mais avaliações primeiro.
4. Salvar em `handoff/varredura-<bairro>-<data>.md` com os 5 melhores para auditar.
5. Registrar no ledger.

## Saída
Lista em `handoff/`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/varredura-bairro-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

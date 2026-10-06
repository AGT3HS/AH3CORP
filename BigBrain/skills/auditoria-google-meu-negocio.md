# SKILL: auditoria-google-meu-negocio  (Fase 1 · dono: Radar)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Augusto diz "audita o [restaurante]" ou lead novo em varredura.

## Entradas
Nome, bairro, chave em `.env`

## Passos
1. Consultar Google Places API: nome, endereço, nota, nº de avaliações, horário, fotos, categorias, telefone. Campo ausente = "não disponível".
2. Montar JSON e rodar `python scripts/gerar_relatorio.py entrada.json saida/auditoria-<slug>.pdf`.
3. Mover o PDF para `handoff/`.
4. Rascunhar abordagem de WhatsApp (até 4 linhas, direta, sem prometer resultado) em `handoff/abordagem-<slug>.md`.
5. Rodar `python scripts/verificar_texto.py` na abordagem.
6. Adicionar linha em `leads.csv` com status `auditado`.
7. Registrar no ledger.

## Saída
`handoff/auditoria-<slug>.pdf`, `handoff/abordagem-<slug>.md`, linha no `leads.csv`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/auditoria-google-meu-negocio-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.

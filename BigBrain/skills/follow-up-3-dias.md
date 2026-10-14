---
name: follow-up-3-dias
description: Identificação de leads pendentes de contato e sugestão de cadência de reengajamento em 3 toques.
owner: "@Maestro"
phase: 1
triggers:
  - "Rotina matinal das 08:00"
  - "Verificação de leads estagnados no pipeline"
inputs:
  - funil: "BigBrain/funil/leads.csv"
outputs:
  - alertas: "Lista de follow-ups sugeridos com copy de reengajamento"
governance_rules:
  - "NUNCA enviar mensagens diretamente ao lead; o envio é 100% manual pelo Augusto."
  - "Respeitar intervalo mínimo de 3 dias úteis entre toques para evitar spam."
---

# SKILL: follow-up-3-dias (Fase 1 · Dono: @Maestro)

## Quando Usar
Diariamente na rotina das 08:00 para identificar estabelecimentos abordados que não responderam.

## Entradas
- Pipeline: [`BigBrain/funil/leads.csv`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/funil/leads.csv) (campo `data_followup` e `status="abordado"`).

## Procedimento de Execução
1. **Identificação dos Leads:**
   - Filtrar leads com status `abordado` cuja data de último contato seja $\ge 3$ dias.
2. **Classificação do Toque de Cadência:**
   - **Toque 1 (3 dias após primeiro contato):** Reativação suave com foco em curiosidade.
   - **Toque 2 (7 dias após primeiro contato):** Prova de valor (exemplo de placa NFC de outro estabelecimento ou métrica de busca local).
   - **Toque 3 (14 dias após primeiro contato):** "Break-up elegante" (liberação educada do contato).
3. **Apresentação ao Augusto:**
   - Gerar links diretos do WhatsApp no formato `wa.me/55...` com texto pré-preenchido.

## Golden Sample (Exemplos Padrão-Ouro de Mensagens)

### Toque 1 (Dia 3 — Reativação Suave):
> *"Oi, [Nome]! Tudo bem? Passando só para confirmar se conseguiu ver a auditoria de presença local que te enviei na terça-feira. Se fizer sentido, te mostro como outros hotéis/restaurantes aqui de Floripa estão usando para subir no Google Maps."*

### Toque 2 (Dia 7 — Prova de Valor Local):
> *"[Nome], vi que a movimentação em [Bairro] aumentou essa semana. Preparei uma prévia visual de como ficaria a placa NFC personalizada com a identidade do [Nome do Local] para facilitar as avaliações dos clientes no balcão. Quer dar uma olhada?"*

### Toque 3 (Dia 14 — Break-up Elegante):
> *"[Nome], imagino que a rotina aí esteja corrida. Não quero insistir! Vou pausar os meus contatos por aqui, mas fico à disposição se no futuro você quiser fortalecer a presença do [Nome do Local] no Google. Grande abraço e sucesso!"*

## Ao Final
Registrar no diário de bordo com `python scripts/ledger_append.py "Follow-up" "Alertas de reengajamento gerados para X leads."`.

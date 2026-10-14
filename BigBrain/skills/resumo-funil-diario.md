---
name: resumo-funil-diario
description: Geração do briefing executivo diário de status do funil de prospecção e decisões pendentes.
owner: "@Maestro"
phase: 1
triggers:
  - "Rotina matinal das 08:00 (Fase 1 e 2)"
  - "Rotina de encerramento das 18:00 (Fase 2)"
  - "Augusto pede resumo do funil ou status dos leads"
inputs:
  - funil: "BigBrain/funil/leads.csv"
  - historico: "BigBrain/ledger/ (últimos 7 dias)"
outputs:
  - briefing: "Mensagem formatada para o WhatsApp do Augusto"
  - painel: "painel_controle.html atualizado"
governance_rules:
  - "Nunca alterar status de leads sem comando expresso do Augusto."
  - "Destacar no máximo 3 prioridades operacionais do dia para evitar sobrecarga."
---

# SKILL: resumo-funil-diario (Fase 1 · Dono: @Maestro)

## Quando Usar
Executado pontualmente às 08:00 (e 18:00 na Fase 2) ou quando o Augusto solicitar "qual a situação do funil hoje?".

## Entradas
- Pipeline: [`BigBrain/funil/leads.csv`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/funil/leads.csv)
- Histórico operacional: [`BigBrain/ledger/`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/ledger)

## Procedimento de Execução
1. **Leitura e Contagem do Funil:**
   - Contabilizar leads por status: `novo`, `auditado`, `abordado`, `respondeu`, `proposta_enviada`, `fechado`, `perdido`.
   - Identificar leads com `data_followup` igual ou anterior à data atual.

2. **Cálculo de Indicadores Chave:**
   - Total de leads ativos no pipeline.
   - Leads com proposta na mesa aguardando resposta.
   - Follow-ups atrasados (> 3 dias sem interação após abordagem).

3. **Geração do Briefing Formatado:**
   Estruturar o texto em blocos visuais objetivos e diretos.

## Golden Sample (Exemplo Padrão-Ouro de Saída)
```text
☀️ *AH3 — Briefing Operacional das 08:00*

📊 *Status do Funil:*
• Novos no radar: 35
• Auditados (prontos para abordagem): 50
• Abordados (aguardando retorno): 0
• Propostas enviadas: 0
• Clientes fechados: 0

🔥 *3 Prioridades de Hoje:*
1. Disparar primeiras 5 abordagens via WhatsApp no bairro Centro (leads já auditados).
2. Verificar painel_controle.html para testar links diretos de WhatsApp.
3. Revisar templates de propostas de Hotelaria vs Gastronomia.

💡 *Ação Rápida:* Abra `painel_controle.html` para iniciar os contatos de hoje.
```

## Ao Final
Registrar a execução no diário operacional:
```bash
python scripts/ledger_append.py "Funil" "Briefing diário gerado para o Augusto."
```

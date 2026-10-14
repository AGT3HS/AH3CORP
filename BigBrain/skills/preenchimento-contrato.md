---
name: preenchimento-contrato
description: Geração automatizada do contrato de prestação de serviços com cláusulas de escopo, SLA e anexos técnicos por pacote.
owner: "@Comercial"
phase: 2
triggers:
  - "Lead confirmado com status 'fechado' pelo Augusto"
  - "Ativação formal de novo cliente na carteira AH3"
inputs:
  - cliente: "Dados cadastrais (Razão Social, CNPJ, Endereço, Representante)"
  - pacote: "Essencial, Crescimento ou Domínio Local"
  - valor: "Valor mensal acordado (respeitando o piso de R$ 1.850/mês)"
outputs:
  - contrato: "BigBrain/clientes/<slug>/contrato_<slug>.md e PDF homologado"
governance_rules:
  - "TRAVA INVIOLÁVEL: Bloqueio imediato se o lead não estiver confirmado como 'fechado' pelo Augusto."
  - "Preenchimento de 100% dos dados cadastrais sem campos pendentes entre colchetes."
---

# SKILL: preenchimento-contrato (Fase 2 · Dono: @Comercial)

## Quando Usar
Apenas quando o Augusto fechar o negócio com o cliente e autorizar a formalização do contrato.

## Entradas
- Modelo base: [`BigBrain/modelos/contrato_base.md`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/modelos/contrato_base.md)
- Dados do cliente coletados no onboarding.

## Procedimento de Execução
1. **Verificação de Trava de Status:**
   - Conferir se o status no [`BigBrain/funil/leads.csv`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/funil/leads.csv) é estritamente `fechado`. Se for qualquer outro status, a execução é cancelada imediatamente.

2. **Ativação e Estruturação de Pastas:**
   ```bash
   python scripts/ativar_cliente.py --nome "Nome do Cliente" --pacote "Crescimento" --valor 3200
   ```

3. **Preenchimento dos Anexos Técnicos:**
   - **Cláusula 1.1:** Especificação detalhada dos entregáveis do pacote contratado.
   - **Cláusula de SLA:** Prazos de resposta para suporte e calendário de aprovação prévia de publicações.
   - **Cláusula de LGPD:** Compromisso irrevogável de isolamento de dados e sigilo absoluto.

4. **Entrega para Revisão do Augusto:**
   - Salvar a minuta final em `BigBrain/clientes/<slug>/contrato_<slug>.md` e gerar PDF para assinatura digital.

## Ao Final
Registrar a formalização do contrato no ledger:
```bash
python scripts/ledger_append.py "Contratos" "Contrato preenchido e formalizado para cliente <nome>."
```

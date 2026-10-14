---
name: auditoria-google-meu-negocio
description: Diagnóstico de presença local no Google Maps, cálculo do GAP de autoridade e geração de proposta de abordagem para WhatsApp.
owner: "@Comercial"
phase: 1
triggers:
  - "Augusto pede auditoria de um estabelecimento específico"
  - "Processamento de novo lead no pipeline comercial"
inputs:
  - nome: "Nome do restaurante ou hotel"
  - bairro: "Bairro do estabelecimento"
outputs:
  - proposta: "BigBrain/handoff/proposta_<slug>.pdf"
  - abordagem: "Texto de WhatsApp formatado no painel_controle.html"
governance_rules:
  - "Nunca prometer primeiro lugar no Google ou faturamento garantido."
  - "Rodar obrigatoriamente verificar_texto.py antes de liberar a mensagem."
---

# SKILL: auditoria-google-meu-negocio (Fase 1 · Dono: @Comercial)

## Quando Usar
Sempre que um novo lead for qualificado para abordagem ou quando o Augusto solicitar a auditoria de um restaurante ou hotel.

## Entradas
- Nome do estabelecimento.
- Cidade e Bairro (padrão Florianópolis).

## Procedimento de Execução
1. **Executar o Pipeline Integrado:**
   ```bash
   python scripts/pipeline_lead_to_proposal.py --nome "Nome do Estabelecimento" --nicho "gastronomia"
   ```
2. **Coleta de Métricas Chave:**
   - Volume total de avaliações e nota média.
   - Volume de avaliações recebidas nos últimos 90 dias.
   - Taxa de resposta do proprietário a reviews de clientes.
   - Presença de fotos profissionais do cardápio ou acomodações.

3. **Cálculo do GAP de Autoridade Regional:**
   $$\text{GAP} = \frac{\text{Média Mensal de Avaliações do Líder do Bairro}}{\text{Média Mensal do Estabelecimento}}$$
   *Exemplo: "O líder da sua microrregião recebe até 3.8× mais avaliações por mês."*

4. **Geração do Roteiro de Abordagem para WhatsApp:**
   - 3 a 4 linhas no máximo, direto ao ponto, tom consultivo e amigável.

## Golden Sample (Exemplo Padrão-Ouro de Abordagem)
> *"Oi, [Nome do Proprietário]! Tudo bem? Passando rápido aqui porque vi o perfil do [Nome do Restaurante] no Google Maps em [Bairro].*
> 
> *Vocês têm pratos excelentes, mas notei que o líder da sua região recebe até 3.8× mais avaliações por mês e tem muito mais visibilidade nas buscas de turistas.*
> 
> *Preparei uma auditoria rápida de 2 minutos mostrando onde vocês estão perdendo clientes locais e uma amostra da placa inteligente NFC com a marca de vocês. Quer que eu te envie por aqui?"*

## Ao Final
Validar o texto e registrar no ledger:
```bash
python scripts/verificar_texto.py "BigBrain/handoff/abordagem_<slug>.md"
python scripts/ledger_append.py "Auditoria" "Diagnóstico de presença local concluído para <nome>."
```

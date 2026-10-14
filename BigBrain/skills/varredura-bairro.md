---
name: varredura-bairro
description: Mapeamento e prospecção regional de estabelecimentos gastronômicos e hoteleiros com cálculo do Score de Oportunidade AH3.
owner: "@Comercial"
phase: 1
triggers:
  - "Augusto diz 'varre o bairro X' ou 'busque novos leads'"
  - "Início de campanha de prospecção regional em Florianópolis"
inputs:
  - bairro: "Nome do bairro ou microrregião (ex: Centro, Jurerê, Lagoa da Conceição, Canasvieiras)"
  - nicho: "restaurante, bar, hotel, pousada (padrão: hospitalidade/gastronomia)"
outputs:
  - leads: "Novos leads inseridos em BigBrain/funil/leads.csv com status 'auditado'"
  - painel: "Atualização automática no painel_controle.html"
governance_rules:
  - "Sanitizar números de telefone para o padrão internacional (5548...)."
  - "Salvar novos leads apenas com status 'novo' ou 'auditado' no leads.csv."
---

# SKILL: varredura-bairro (Fase 1 · Dono: @Comercial)

## Quando Usar
Quando o Augusto desejar mapear novos restaurantes, bares ou hotéis em um bairro específico de Florianópolis.

## Entradas
- Nome do bairro / região (ex: `Jurerê`, `Centro`, `Canasvieiras`, `Lagoa da Conceição`).
- Nicho alvo (`gastronomia` ou `hotelaria`).

## Procedimento de Execução
1. **Execução do Script Parametrizado:**
   ```bash
   python scripts/gerar_lote_bairro.py --bairro "Centro" --nicho "restaurante" --limite 10
   ```
2. **Cálculo do Score de Oportunidade AH3:**
   Os estabelecimentos são ranqueados pela fórmula:
   $$\text{Score} = \frac{\text{Volume de Avaliações} \times (5.0 - \text{Nota Média})}{\text{Distância do Líder Local}}$$
   *Quanto mais avaliações e mais espaço para subir a nota, maior a oportunidade de conversão.*

3. **Validação e Inserção no Pipeline:**
   - Adicionar os leads qualificados em [`BigBrain/funil/leads.csv`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/funil/leads.csv).
   - Gerar links diretos de WhatsApp (`https://wa.me/5548...`).

## Golden Sample (Exemplo Padrão-Ouro de Lead Qualificado)
```csv
id,nome,slug,bairro,categoria,rating,reviews_count,telefone,link_gmb,status,data_adicao,data_followup,observacoes
86,Restaurante Mar de Dentro,restaurante-mar-de-dentro,Centro,Frutos do Mar,4.2,420,5548991234567,https://maps.google.com/?cid=...,auditado,2026-10-08,2026-10-11,GAP de 2.8x vs lider local. 40 avaliacoes sem resposta.
```

## Ao Final
Registrar a varredura no ledger:
```bash
python scripts/ledger_append.py "Prospecção" "Varredura de bairro concluída: X novos leads qualificados em <bairro>."
```

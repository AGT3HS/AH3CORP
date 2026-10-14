---
name: planejamento-trafego
description: Planejamento de campanhas de tráfego pago hiperlocal em raio de 1 km a 5 km (Meta Ads e Google Ads) para atração de clientes locais e turistas.
owner: "@Marketing"
phase: 3
triggers:
  - "Cliente fechado solicita plano de mídia ou tráfego pago"
  - "Augusto pede rascunho de planejamento de anúncios locais"
inputs:
  - cliente: "BigBrain/clientes/<slug>/"
  - verba_mensal: "Orçamento de mídia do cliente (ex: R$ 500, R$ 1.000, R$ 2.000)"
outputs:
  - plano_midia: "BigBrain/handoff/trafego_<slug>.md (e planilha auxiliar)"
governance_rules:
  - "TRAVA INVIOLÁVEL: O agente NUNCA cria campanhas nem toca em verba real; apenas entrega o planejamento rascunhado para o Augusto."
  - "Nunca prometer ROI numérico ou faturamento garantido nas projeções de tráfego."
---

# SKILL: planejamento-trafego (Fase 3 · Dono: @Marketing)

## Quando Usar
Quando um cliente do pacote Domínio Local (ou com verba extra de mídia) desejar amplificar o alcance do estabelecimento via anúncios pagos no Instagram, Facebook ou Google Maps.

## Estratégia de Tráfego Hiperlocal AH3 (Raio de 1 a 5 km)

### 1. Segmentação Geográfica e Comportamental
- **Raio Imediato (1 a 3 km):** Pessoas que moram ou trabalham perto do local (foco em Almoço Executivo e Happy Hour).
- **Turistas e Viajantes:** Pessoas em Florianópolis que moram a mais de 100 km de distância (foco em gastronomia típica e hospedagem).

### 2. Matriz de Distribuição de Verba Sugerida (Exemplo: R$ 1.000 / mês)

| Objetivo da Campanha | Verba (%) | Formato do Anúncio | Destino / Conversão |
|---|---|---|---|
| **Atração & Descoberta Local** | 50% (R$ 500) | Carrossel de Pratos / Vídeo Reels com Gancho | Link para o Perfil do Instagram ou Cardápio Digital |
| **Geração de Reservas & Pedidos** | 35% (R$ 350) | Post de Oferta / Prato Especial da Semana | WhatsApp Direto com mensagem pronta de reserva |
| **Remarketing de Reconhecimento** | 15% (R$ 150) | Post com Prova Social e Avaliações 5 Estrelas | Google Maps do Estabelecimento |

### 3. Rascunhos de Copies com Travas de Segurança
- Exemplo Gastronomia: *"Buscando onde almoçar com tranquilidade no Centro? Conheça nossos pratos executivos preparados na hora com ingredientes frescos. Toque abaixo para ver o cardápio e reservar sua mesa."*

## Ao Final
Validar textos com `verificar_texto.py` e registrar no ledger:
```bash
python scripts/ledger_append.py "Tráfego" "Plano de mídia hiperlocal rascunhado para <slug>."
```

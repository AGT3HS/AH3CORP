# Regra de Seleção de Concorrentes (Benchmarking de Proximidade)

**Origem:** Decisão de produto/operação com Augusto  
**Skill de Referência:** `auditoria-google-meu-negocio` / `scripts/gerar_relatorio.py`  
**Status:** Atualizado com base no feedback prático de campo

---

## 1. Princípio Fundamental: Concorrência Hiperlocal por Proximidade

Na gastronomia de praia e microrregiões (ex: Ponta das Canas / Lagoinha do Norte), o consumidor decide onde comer com base na conveniência geográfica imediata. Restaurantes a 3-5 km em outros bairros (como Canasvieiras) não disputam a mesa do cliente que já está na praia.

**A proximidade geográfica (menor distância) é o critério soberano #1.**

---

## 2. As 4 Etapas de Seleção

1. **Status Operacional Ativo (Mandatório):**
   - Exclusão sumária de estabelecimentos com status `CLOSED_PERMANENTLY` ou `CLOSED_TEMPORARILY`.
   - Exclusão de locais não gastronômicos (praias físicas, pousadas sem restaurante aberto ao público, parques, etc.).

2. **Mesma Categoria Geral (Gastronomia / Restaurantes):**
   - Todos os restaurantes, bares, petiscarias e bistrôs que disputam o consumo de alimentação no polo local.

3. **Ordenação por Menor Distância (Proximidade Absoluta):**
   - Seleção dos 5 concorrentes geograficamente mais próximos do restaurante auditado (raio imediato: 0 a 1.5 km, expandindo progressivamente apenas se faltarem concorrentes).
   - O nicho ultraespecífico fica em 2º plano em relação à proximidade física.

4. **Desempate por Relevância Local:**
   - Havendo múltiplos estabelecimentos na mesma faixa de distância, o desempate prioriza o volume de avaliações e nota média no Google.

---

## 3. Exibição e Contraste do Alvo
- O restaurante do cliente auditado entra destacado como `• ALVO` (em linha de alerta visual), evidenciando o gap de nota, avaliações, distância e presença de canal direto de conversão (WhatsApp/Cardápio).

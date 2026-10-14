---
name: relatorio-mensal
description: Geração do relatório executivo mensal de presença local, reputação no Google Maps e benchmark competitivo.
owner: "@Marketing"
phase: 3
triggers:
  - "Primeiro dia útil de cada mês para cada cliente ativo"
  - "Augusto solicita fechamento mensal de métricas"
inputs:
  - metricas: "Visualizações de perfil, rotas traçadas, chamadas telefônicas, novos reviews e nota média"
  - cliente: "BigBrain/clientes/<slug>/"
outputs:
  - relatorio_pdf: "BigBrain/clientes/<slug>/relatorios/relatorio_<slug>_<AAAA-MM>.pdf"
governance_rules:
  - "Nunca inventar métricas inexistentes; reportar apenas dados reais apurados."
  - "Apresentar a evolução percentual e o plano de ação do mês seguinte."
---

# SKILL: relatorio-mensal (Fase 3 · Dono: @Marketing)

## Quando Usar
No primeiro dia útil de cada mês para consolidar a entrega de valor para o cliente e embasar a renovação/continuidade contratual.

## Estrutura do Relatório Executivo de 3 Páginas

### Página 1 — Indicadores Chave de Presença Local (KPIs)
- **Visualizações no Google Maps:** Volume de pessoas que encontraram o estabelecimento.
- **Ações dos Usuários:** Quantidade de cliques para pedir rota no GPS, chamadas telefônicas e acessos ao cardápio/site.
- **Novas Avaliações:** Volume de avaliações coletadas no mês via Placas NFC e taxa de resposta (100%).
- **Nota Média do Estabelecimento:** Evolução da nota no Google (ex: 4.3 ➔ 4.6).

### Página 2 — Benchmark e Market Share Regional
- Comparativo direto de volume de reviews e posição no ranking de buscas locais do bairro contra os 3 principais concorrentes diretos.

### Página 3 — Plano de Ação e Metas para o Mês Seguinte
- 3 iniciativas prioritárias da AH3 para o novo mês (ex: novos testes de prato do dia, reforço de placas NFC no salão, campanha hiperlocal para o feriado).

## Procedimento de Execução
```bash
# Relatório de presença e evolução gerado via motor unificado:
python scripts/gerar_auditoria_oficial_real.py --slug "<slug>" --output "BigBrain/clientes/<slug>/relatorios"
```

## Ao Final
Registrar a entrega no ledger:
```bash
python scripts/ledger_append.py "Relatórios" "Relatório mensal de performance gerado para <slug>."
```

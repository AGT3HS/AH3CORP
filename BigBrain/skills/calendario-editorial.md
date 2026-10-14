---
name: calendario-editorial
description: Planejamento semanal e mensal de conteúdos e campanhas locais sincronizados com a sazonalidade e clima de Florianópolis.
owner: "@Marketing"
phase: 3
triggers:
  - "Início de cada semana ou virada de mês para clientes ativos"
  - "Augusto pede planejamento de pautas para restaurante ou hotel"
inputs:
  - cliente: "BigBrain/clientes/<slug>/"
  - historico: "Posts anteriores e eventos locais de Florianópolis"
outputs:
  - calendario: "BigBrain/clientes/<slug>/conteudo/calendario_<AAAA-MM>.md"
governance_rules:
  - "Balancear formatos: 2x Carrosséis/Imagens estáticas, 2x Reels, 1x Foto/Feed e Stories diários."
  - "Adaptar a pauta para dias úteis (almoço/corporativo) vs finais de semana (lazer/família/turismo)."
---

# SKILL: calendario-editorial (Fase 3 · Dono: @Marketing)

## Quando Usar
Toda segunda-feira de manhã para abastecer o cliente com o cronograma de conteúdos da semana.

## Matriz Semanal Canônica de 5 Publicações

| Dia | Formato | Pilar de Conteúdo | Gancho / Objetivo |
|---|---|---|---|
| **Segunda** | Carrossel Imagem | Bastidores & Qualidade | *"Como nossos frutos do mar chegam frescos todos os dias da Ilha"* |
| **Terça** | Reels Vídeo | Prato Protagonista | Vídeo macro de preparo com fumaça e corte do prato principal. |
| **Quinta** | Post Imagem Estática | Prova Social (Google Reviews) | Depoimento 5 estrelas de cliente com foto do ambiente. |
| **Sexta** | Carrossel / Imagem | Convite para Fim de Semana | Destaque para drinks, música ao vivo ou cardápio especial de happy hour. |
| **Domingo** | Reels / Stories | Experiência & Família | Salão cheio, clima acolhedor e chamada para almoço de domingo. |

## Sazonalidade de Florianópolis
- **Verão / Alta Temporada (Dez - Março):** Foco em turistas, reservas antecipadas, drinks refrescantes e localização próxima às praias.
- **Inverno / Baixa Temporada (Maio - Agosto):** Foco no público residente da Grande Florianópolis, pratos quentes, vinhos, lareira e eventos corporativos.

## Ao Final
Registrar a montagem do calendário no ledger:
```bash
python scripts/ledger_append.py "Calendário" "Calendário editorial da semana gerado para <slug>."
```

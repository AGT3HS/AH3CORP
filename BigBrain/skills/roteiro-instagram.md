---
name: roteiro-instagram
description: Elaboração de roteiros estruturados em 3 colunas para vídeos curtos (Reels / Stories / TikTok) com ganchos visuais de retenção.
owner: "@Marketing"
phase: 3
triggers:
  - "Augusto pede roteiro de vídeo ou Reels para cliente"
  - "Cronograma do calendário editorial semanal prevendo publicação em vídeo"
inputs:
  - cliente: "BigBrain/clientes/<slug>/"
  - tema: "Assunto do vídeo (prato, suíte, drink, bastidores)"
outputs:
  - roteiro: "BigBrain/handoff/roteiro_<slug>_<data>.md"
governance_rules:
  - "Roteiro deve ter no máximo 30 a 45 segundos de duração total."
  - "Gancho magnético nos 3 primeiros segundos para evitar que o usuário pule o vídeo."
---

# SKILL: roteiro-instagram (Fase 3 · Dono: @Marketing)

## Quando Usar
Quando for necessário gravar ou produzir um vídeo curto (Reels/Stories) para restaurantes, bares ou hotéis.

## Estrutura do Roteiro em 3 Colunas

| Tempo | 🎧 Áudio / Locução | 🎬 Ação Visual na Tela | 💬 Texto / Gancho Visual |
|---|---|---|---|
| **00-03s (Gancho)** | Áudio em alta + frase de impacto (ex: *"Você comeria isso?"*) | Plano detalhe macro com fumaça subindo da chapa ou queijo derretendo. | **Texto Grande:** "O segredo que ninguém te conta sobre o Centro de Floripa..." |
| **03-15s (Corpo 1)** | Explicação rápida do chef ou narrativa acolhedora. | Cortes rápidos: corte da carne, montagem da taça, garçom servindo à mesa. | "Ingredientes 100% frescos selecionados hoje de manhã." |
| **15-25s (Corpo 2)** | Destaque do ambiente e da experiência do local. | Plano aberto do salão aconchegante ou vista da praia. | "Ambiente climatizado e perfeito para o almoço ou jantar." |
| **25-30s (CTA Final)** | *"Vem experimentar hoje mesmo!"* | Placa NFC no balcão sendo aproximada pelo celular ou logo da casa. | **"Link na bio para reservar sua mesa pelo WhatsApp ➔"** |

## Dicas de Direção para o Estabelecimento
1. **Luz Natural:** Gravar próximo a janelas ou com luz quente difusa.
2. **Sem Estabilizadores Complexos:** Vídeos gravados direto no celular na vertical (9:16) geram mais autenticidade e conexão com clientes locais.

## Ao Final
Validar o texto e registrar no ledger:
```bash
python scripts/verificar_texto.py "BigBrain/handoff/roteiro_<slug>_<data>.md"
python scripts/ledger_append.py "Vídeos" "Roteiro de Reels em 3 colunas produzido para <slug>."
```

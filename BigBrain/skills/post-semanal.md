---
name: post-semanal
description: Criação de publicações semanais completas para Instagram com copy magnético e geração automatizada de artes gráficas em imagem (estático ou carrossel).
owner: "@Marketing"
phase: 3
triggers:
  - "Rotina semanal de produção de conteúdo por cliente ativo"
  - "Augusto pede criação de post ou carrossel para o Instagram"
inputs:
  - cliente: "BigBrain/clientes/<slug>/"
  - pauta: "Tema definido no calendário editorial ou solicitação pontual"
  - formato: "imagem_estatica (1080x1350 ou 1080x1080) ou carrossel (3 a 5 slides)"
outputs:
  - copy: "BigBrain/handoff/post_<slug>_<data>.md"
  - imagens: "saida/posts_instagram/<slug>/slide_*.png (300 DPI)"
governance_rules:
  - "Validação obrigatória com scripts/verificar_texto.py antes de liberar para o handoff."
  - "Nunca postar diretamente no perfil do cliente; todo material é entregue ao Augusto para aprovação."
---

# SKILL: post-semanal (Fase 3 · Dono: @Marketing)

## Quando Usar
Semanalmente para cada cliente com contrato ativo ou sob demanda de publicações especiais.

## Os 4 Pilares de Conteúdo Local AH3
1. **Pilar 1 — Bastidores & Origem:** O processo de preparo do chef, fornecedores locais da Ilha de Santa Catarina, cuidados com a hospitalidade.
2. **Pilar 2 — Prova Social & Avaliações:** Depoimentos reais de clientes 5 estrelas no Google Maps transformados em posts visuais elegantes.
3. **Pilar 3 — Protagonismo Sensorial:** Foto macro com descrição envolvente do prato mais pedido ou da melhor suíte com vista para o mar.
4. **Pilar 4 — Ação Semanal / Convite:** Sugestão para o almoço executivo, happy hour de sexta ou reserva de fim de semana.

## Procedimento de Execução

1. **Rascunho do Texto & Legenda:**
   - Gancho forte na primeira linha (visível antes do *"ver mais"*).
   - Corpo do texto com quebras de linha limpas e tom acolhedor da casa.
   - Chamada final honesta (ex: *"Qual dessas opções é a sua favorita? Link na bio para conferir o cardápio completo."*).
   - 3 a 5 hashtags hiperlocais (ex: `#Florianopolis #GastronomiaFloripa #Jurere`).

2. **Geração Automatizada da Imagem / Carrossel:**
   Executar o gerador gráfico de alta resolução:
   ```bash
   # Exemplo 1: Post de Avaliação 5 Estrelas do Google
   python scripts/gerar_post_instagram.py --tipo avaliacao --nome "Nome do Restaurante" --texto "Melhor polvo grelhado que já comi em Floripa!" --autor "Mariana S." --nota 5

   # Exemplo 2: Carrossel Completo de 4 Slides
   python scripts/gerar_post_instagram.py --tipo carrossel --nome "Nome do Hotel" --tema "3 Motivos para se hospedar em Jurerê nesta primavera" --slides 4
   ```

3. **Validação de Texto & Travas:**
   ```bash
   python scripts/verificar_texto.py "BigBrain/handoff/post_<slug>_<data>.md"
   ```

## Saída
- Arquivo de legenda e orientações em `BigBrain/handoff/post_<slug>_<data>.md`.
- Imagens em alta resolução PNG (300 DPI) prontas para publicação no feed em `saida/posts_instagram/<slug>/`.

## Ao Final
Registrar no diário de bordo operacional:
```bash
python scripts/ledger_append.py "Conteúdo" "Post semanal e artes visuais geradas para <slug>."
```

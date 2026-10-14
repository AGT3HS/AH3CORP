---
name: landing-page
description: Criação de landing page moderna, ultra-rápida e de alta conversão para reservas de hotéis ou pedidos de restaurantes.
owner: "@Designer"
phase: 3
triggers:
  - "Cliente fechado solicita site ou landing page de alta conversão"
  - "Augusto pede desenvolvimento de interface web para cliente"
inputs:
  - cliente: "BigBrain/clientes/<slug>/"
  - identidade: "Paleta de cores, fotos e logo do estabelecimento"
outputs:
  - landing_html: "BigBrain/handoff/landing_<slug>.html"
governance_rules:
  - "Usar HTML semântico moderno e CSS Vanilla puro (sem frameworks pesados)."
  - "Design responsivo obrigatório (mobile-first), Core Web Vitals < 1.2s e selo de avaliações do Google integrado."
---

# SKILL: landing-page (Fase 3 · Dono: @Designer)

## Quando Usar
Quando um cliente ativo demandar uma página web institucional para atrair reservas diretas (hotelaria) ou apresentar cardápio/ambiente com pedidos via WhatsApp (gastronomia).

## Blueprint de Alta Conversão da AH3

1. **Hero Section de Alto Impacto:**
   - Imagem de fundo imersiva do ambiente ou prato principal.
   - Título forte com proposta de valor clara em tipografia **Outfit**.
   - Botão de Ação Primário: *"Reservar Mesa / Suíte pelo WhatsApp"*.

2. **Diferenciais & Experiência:**
   - 3 a 4 destaques rápidos (ex: *"Beira-mar em Jurerê"*, *"Frutos do mar frescos do dia"*, *"Estacionamento próprio"*).

3. **Carrossel Visual / Galeria:**
   - Fotos em alta resolução de pratos, drinks ou acomodações com efeito hover suave.

4. **Widget de Prova Social (Google Reviews):**
   - Destaque da nota média (ex: ⭐ 4.8 no Google Maps) com 3 depoimentos reais de clientes verificados.

5. **Localização & Acesso Rápido:**
   - Mapa interativo com rota direta no Google Maps, endereço completo e horário de funcionamento.

6. **SEO Local On-Page:**
   - Metatags OpenGraph e marcação Schema.org (`LocalBusiness`, `Restaurant` ou `Hotel`).

## Ao Final
Registrar no diário de bordo operacional:
```bash
python scripts/ledger_append.py "Sites" "Landing page de alta conversão desenvolvida para <slug>."
```

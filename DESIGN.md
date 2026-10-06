---
version: alpha
name: Jurere-Beach-Village-NFC-10x10
description: Design system oficial dos Cartões Inteligentes 10x10 NFC para o resort Jurerê Beach Village.
colors:
  primary: "#0D3B66"
  secondary: "#112233"
  accent: "#EE964B"
  accent-dark: "#E09F3E"
  neutral-light: "#F8FAFC"
  neutral-card: "#FFFFFF"
  border-card: "#E2E8F0"
  text-heading: "#0D3B66"
  text-muted: "#64748B"
  text-kicker: "#94A3B8"
typography:
  kicker:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: 800
    letterSpacing: "3px"
  card-title:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: 700
  card-desc:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: 500
  footer:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: 600
rounded:
  outer: 60px
  card-item: 20px
  icon-badge: 40px
  pill: 18px
spacing:
  margin: 80px
  gap-grid: 24px
components:
  card-container:
    backgroundColor: "{colors.neutral-card}"
    rounded: "{rounded.card-item}"
    border: "1.5px solid {colors.border-card}"
    padding: 16px
  nfc-cluster:
    accentColor: "{colors.accent}"
    pillBackground: "{colors.accent}"
    pillTextColor: "{colors.primary}"
    textColor: "#FFFFFF"
---

## Overview

Design System oficial dos Cartões Inteligentes 10x10 NFC para o resort Jurerê Beach Village.
Projetado para unir harmonia cromática litorânea, contraste visual absoluto e navegação tátil imediata para o hóspede.

## Colors

- **Primary (#0D3B66):** Azul Marinho Jurerê. Utilizado no cabeçalho curvo orgânico, títulos e elementos de destaque da marca.
- **Secondary (#112233):** Azul Petróleo Profundo. Cor de ancoragem e contraste.
- **Accent (#EE964B):** Âmbar Solar. Cor de ação do cluster NFC (ondas e pílula) e ícones de ativação.
- **Neutral Light (#F8FAFC):** Fundo base inferior suave.
- **Neutral Card (#FFFFFF):** Fundo dos 4 cards de serviço individuais com bordas refinadas.

## Typography

- **Plus Jakarta Sans:** Família tipográfica única em 3 pesos estruturados:
  - Extra Bold (800): Kicker `UM TOQUE LIBERA` e badge `NFC`.
  - Bold (700): Títulos dos 4 serviços.
  - Medium (500/600): Textos de apoio, instruções e rodapé.

## Layout

- **Canvas:** 1000x1000 px com margem de segurança de 80 px.
- **Divisão:** Curva senoidal superior (`Q500,485`) separando a área de marca do grid de serviços.
- **Grid de Serviços:** Grade 2x2 composta por 4 cartões com cantos arredondados (20px), contorno fino em `#E2E8F0` e sombra de elevação.

## Elevation & Depth

- **Cards de Serviço:** Sombra suave `0 4px 12px rgba(13, 59, 102, 0.06)` com borda sutil de `1.5px`.
- **Canvas Geral:** Sombra projetada Gaussian `0 20px 40px rgba(0, 20, 40, 0.20)` sobre o fundo de apresentação.

## Shapes

- Cantos externos do display: Raio de 60px (6mm no corte físico).
- Cantos dos cards internos: Raio de 20px.
- Pílula NFC: Raio de 18px.

## Components

- `nfc-cluster`: Conjunto compacto no topo direito: ondas de radiofrequência, pílula `[ NFC ]` e chamada `Aproxime o celular` em branco.
- `service-card`: Contêiner individual retangular com ícone circular colorido, título em negrito e subtítulo legível.

## Do's and Don'ts

- **Do:** Manter os 4 cards de serviços delimitados com caixas estruturadas, bordas nítidas e respiro interno.
- **Do:** Preservar a cor branca para o texto `Aproxime o celular` sobre o fundo azul escuro para garantir legibilidade máxima.
- **Don't:** Jamais deixar os itens inferiores soltos sem contorno ou estrutura de card.
- **Don't:** Jamais achatar ou deformar o logotipo oficial do hotel.

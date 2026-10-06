---
version: alpha
name: AH3 Audit Design Tokens Ecosystem (10 Variations)
description: Formal DESIGN.md token specifications for 10 distinct executive audit report design themes.
colors:
  primary: "#1F2430"
  secondary: "#6B7280"
  tertiary: "#F26A21"
  neutral: "#FAFAF5"
  surface: "#FFFFFF"
  border: "#E5E1DA"
  success: "#1E9E5A"
  warning: "#E8A317"
  critical: "#D6403A"
typography:
  h1:
    fontFamily: Inter, "Segoe UI", sans-serif
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  h2:
    fontFamily: Inter, "Segoe UI", sans-serif
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.2
  h3:
    fontFamily: Inter, "Segoe UI", sans-serif
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.3
  body-md:
    fontFamily: Inter, "Segoe UI", sans-serif
    fontSize: 9.5px
    lineHeight: 1.4
  caption:
    fontFamily: Inter, "Segoe UI", sans-serif
    fontSize: 8px
    lineHeight: 1.2
rounded:
  sm: 4px
  md: 8px
  lg: 14px
spacing:
  xs: 4px
  sm: 8px
  md: 14px
  lg: 24px
components:
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 14px
  hero-box:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 18px
  badge-target:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 4px
---

## Overview

Este documento estabelece o catálogo oficial de **10 Variações de Design Systems (DESIGN.md)** para os relatórios de auditoria executiva da AH3. Cada variação foi calibrada para nichos gastronômicos específicos do mercado de Florianópolis, mantendo a densidade de dados e conformidade com as regras operacionais.

---

## Colors

### Catálogo das 10 Variações de Design Tokens

#### 1. V2 Warm Light & Hero Dark (Design Ativo / Canto do Mar)
- **Nicho:** Frutos do Mar, Peixes e Gastronomia Litorânea.
- **Fundo Base:** `#FAFAF5` (Alabastro suave)
- **Superfície dos Cards:** `#FFFFFF` puro
- **Hero & CTA:** `#1F2430` (Navy Obsidian)
- **Acento Principal:** `#F26A21` (Laranja Quente)
- **Status (Sucesso / Alerta / Crítico):** `#1E9E5A` / `#E8A317` / `#D6403A`

#### 2. Dark Obsidian & Neon Orange (Dark Orange)
- **Nicho:** Choperias Artesanais, Hamburguerias Premium e Gastrobares Noturnos.
- **Fundo Base:** `#0E0E0E` (Preto Profundo)
- **Superfície dos Cards:** `#181818` / `#1F1F1F`
- **Acento Principal:** `#F26522` (Laranja Neon)
- **Acento Secundário:** `#22C55E` (Esmeralda)
- **Bordas:** `#2C2C2C`

#### 3. Slate Executive Minimalist (McKinsey Corporate)
- **Nicho:** Restaurantes Executivos, Grandes Redes e Cantinas Clássicas.
- **Fundo Base:** `#F8FAFC` (Slate 50)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero & Textos:** `#0F172A` (Slate 900)
- **Acento Principal:** `#2563EB` (Azul Royal)
- **Bordas:** `#E2E8F0`

#### 4. Tuscan Terracotta & Sage Green
- **Nicho:** Pizzarias Artesanais, Forno a Lenha e Trattorias Italianas.
- **Fundo Base:** `#FBF8F3` (Panna Cotta)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero & Títulos:** `#2C221E` (Espresso)
- **Acento Principal:** `#C85A32` (Terracota Toscano)
- **Acento Secundário:** `#4A6B5B` (Verde Sálvia)
- **Bordas:** `#E8DEC8`

#### 5. Nordic Roast & Amber Wood
- **Nicho:** Parrillas Uruguaias, Churrascarias e Steak Houses.
- **Fundo Base:** `#F5F3EF` (Areia Nórdica)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero:** `#1E1B18` (Carvão Tostado)
- **Acento Principal:** `#D97706` (Âmbar Queimado)
- **Acento Secundário:** `#78350F` (Madeira Nobre)
- **Bordas:** `#E4DFD7`

#### 6. Atlantic Deep Navy & Seafoam
- **Nicho:** Restaurantes Pé na Areia, Quiosques e Petiscarias de Praia.
- **Fundo Base:** `#F0F4F8` (Brisa Marinha)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero & Títulos:** `#0C1E36` (Azul Abissal)
- **Acento Principal:** `#0284C7` (Azul Ciano)
- **Acento Secundário:** `#0D9488` (Teal Espuma)
- **Bordas:** `#CBD5E1`

#### 7. Cyber Midnight & Electric Lime
- **Nicho:** Dark Kitchens, Smash Burgers e Operações Focadas em Delivery Jovem.
- **Fundo Base:** `#121316` (Midnight Dark)
- **Superfície dos Cards:** `#1C1E24`
- **Acento Principal:** `#84CC16` (Verde Limão Elétrico)
- **Acento Secundário:** `#06B6D4` (Ciano)
- **Bordas:** `#2E323D`

#### 8. Bordeaux Editorial & Rose Gold
- **Nicho:** Bistrôs Franceses, Wine Bars e Fine Dining Contemporâneo.
- **Fundo Base:** `#FAF8F7` (Seda Champagne)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero:** `#2A0E18` (Bordeaux Escuro)
- **Acento Principal:** `#8B1E3F` (Vinho Borgonha)
- **Acento Secundário:** `#D4AF37` (Ouro Envelhecido)
- **Bordas:** `#EDE4E6`

#### 9. Kyoto Zen & Wasabi Leaf
- **Nicho:** Sushibars, Izakayas e Culinária Asiática / Fusion.
- **Fundo Base:** `#F7F8F5` (Papel Arroz)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero & Títulos:** `#1A1D20` (Nanquim)
- **Acento Principal:** `#4D7C0F` (Matcha / Wasabi)
- **Acento Secundário:** `#E11D48` (Atum Fresco)
- **Bordas:** `#E2E6DF`

#### 10. Sunset Island Coral & Goldenrod
- **Nicho:** Beach Clubs de Jurerê, Bares de Sunset e Cafés Gourmet.
- **Fundo Base:** `#FCF9F5` (Concha Clara)
- **Superfície dos Cards:** `#FFFFFF`
- **Hero:** `#211815` (Sépia Tropical)
- **Acento Principal:** `#F95738` (Coral Sunset)
- **Acento Secundário:** `#EE964B` (Dourado de Verão)
- **Bordas:** `#EBE3DA`

---

## Typography

- **Títulos e Destaques:** Inter / Segoe UI (Geométrico, neutro e de alta legibilidade).
- **Dados Técnicos:** JetBrains Mono para coordenadas de GPS, telefones e volumes numéricos.

## Layout

- Formato estrito: **A4 Retrato (210mm × 297mm)**.
- Extensão obrigatória: **3 páginas balanceadas**, sem espaços vazios e sem transbordo de cartões.

## Elevation & Depth

- Cards com borda sólida de 1px e cantos arredondados de 8px a 14px.
- Sem sombras difusas pesadas, garantindo fidelidade de impressão e exportação vetorial.

## Shapes

- Pílulas compactas (`4px` de raio) para tags de status e badges do ranking.

## Components

- `card`: Módulo de informação com respiro interno e borda padronizada.
- `hero-box`: Bloco de topo escuro para contraste imediato na abertura da auditoria.
- `badge-target`: Distintivo exclusivo `ALVO AUDITADO` posicionado na linha do cliente.

## Do's and Don'ts

### Do's
- Ordene sempre os concorrentes por volume decrescente de avaliações.
- Mantenha a presença do Alvo Auditado na sua posição matemática real.
- Assegure conformidade rigorosa com as 8 travas invioláveis da AH3.

### Don'ts
- Não quebre tabelas ou listas entre páginas.
- Não prometa resultados em métricas ou faturamento.
- Não utilize paletas de baixo contraste que violem o padrão WCAG AA.

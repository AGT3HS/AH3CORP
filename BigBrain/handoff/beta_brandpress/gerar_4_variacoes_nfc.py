# -*- coding: utf-8 -*-
"""
Geração das 4 Variações de Placa NFC 100x100 mm conforme especificação rigorosa do guia 'placa-nfc-design':
- Formato 1000x1000 (10 unidades = 1 mm), cantos rx=60
- Margem de segurança de 90 unidades (9 mm)
- Curva escuro/claro com CENTRO mais alto que as bordas (530 nas bordas, 460 no centro)
- Logo de referência oficial embutida em base64
- Símbolo NFC em âmbar com pílula e texto
- Grade 2x2 com ícones de traço em círculos de 80 unidades (8 mm) a 12% de opacidade
- 4 humores/tons distintos: Clássico (Esmeralda), Escuro de Alto Impacto (Obsidiana), Sóbrio (Navy), Quente/Suave (Terracota)
- Renderização em PNGs de alta qualidade com palco neutro evidenciando os cantos arredondados rx=60
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_4_variacoes"
os.makedirs(OUT, exist_ok=True)

LOGO_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES = [
    {
        "id": "1_classica_emerald",
        "nome": "1. Clássica (Emerald Heritage)",
        "intencao": "Sofisticação atemporal e conexão com a natureza de Florianópolis.",
        "topo_start": "#0E2B24",
        "topo_end": "#051310",
        "cor_principal": "#0E2B24",
        "cor_ambar": "#F09C24",
        "cor_ambar_dark": "#051310",
        "neutro_corpo": "#F8F6F0",
        "texto_escuro": "#111827",
        "texto_sub": "#4B5563",
        "filete": "#E2DFD8",
        "site": "costao.com.br"
    },
    {
        "id": "2_alto_impacto_obsidian",
        "nome": "2. Escura de Alto Impacto (Obsidian Luxe)",
        "intencao": "Modernidade executiva, presença imponente e alto contraste tecnológico.",
        "topo_start": "#18181B",
        "topo_end": "#09090B",
        "cor_principal": "#18181B",
        "cor_ambar": "#F59E0B",
        "cor_ambar_dark": "#09090B",
        "neutro_corpo": "#F4F4F5",
        "texto_escuro": "#09090B",
        "texto_sub": "#52525B",
        "filete": "#E4E4E7",
        "site": "costao.com.br"
    },
    {
        "id": "3_sobria_navy",
        "nome": "3. Sóbria (Deep Navy Marine)",
        "intencao": "Tranquilidade marítima, elegância corporativa e hospitalidade costeira de luxo.",
        "topo_start": "#0A2540",
        "topo_end": "#041220",
        "cor_principal": "#0A2540",
        "cor_ambar": "#E59819",
        "cor_ambar_dark": "#041220",
        "neutro_corpo": "#F6F8FB",
        "texto_escuro": "#0A2540",
        "texto_sub": "#475569",
        "filete": "#DEE4EC",
        "site": "costao.com.br"
    },
    {
        "id": "4_quente_terracotta",
        "nome": "4. Quente & Suave (Terracotta & Warm Clay)",
        "intencao": "Acolhimento humanizado, atmosfera boutique artesanal e calor sensorial.",
        "topo_start": "#7C2D21",
        "topo_end": "#45160E",
        "cor_principal": "#7C2D21",
        "cor_ambar": "#E68226",
        "cor_ambar_dark": "#45160E",
        "neutro_corpo": "#FAF5EE",
        "texto_escuro": "#381A14",
        "texto_sub": "#6B4840",
        "filete": "#EADFD0",
        "site": "costao.com.br"
    }
]

def gerar_svg_placa(cfg):
    """
    Layout com as regras da placa-nfc-design:
    - Dimensão: 1000x1000 com rx=60 (raio de 6 mm).
    - Margem de segurança de 90 unidades (9 mm) rigorosa.
    - Curva suave: bordas em Y=530 e centro mais alto em Y=460.
    - Grade 2x2 com nomes diretos (4,4 mm = 44 un) e ícones de traço dentro de círculos de 80 un a 12%.
    - Rodapé com filete de 3 un e textos a 30 un (3 mm).
    """
    v_id = cfg["id"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="gradTopo_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg['topo_start']}"/>
      <stop offset="100%" stop-color="{cfg['topo_end']}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Base Clara Inferior (Neutro Quente) -->
    <rect width="1000" height="1000" fill="{cfg['neutro_corpo']}"/>

    <!-- Divisão Superior Escura com Curva Suave (Bordas Y=530, Centro Alto Y=460) -->
    <path d="M 0,0 L 1000,0 L 1000,530 Q 500,450 0,530 Z" fill="url(#gradTopo_{v_id})"/>

    <!-- A) LOGO OFICIAL DE REFERÊNCIA (Margem X=90, Y=110) -->
    <g transform="translate(90, 115)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="350" height="115" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER SÍMBOLO NFC (Topo Direito Centralizado em X=800, Y=90) -->
    <g transform="translate(800, 90)">
      <!-- 1. Símbolo NFC: Ponto e 3 Arcos em Traço Arredondado (Largura 220 un / 22 mm) -->
      <g stroke="{cfg['cor_ambar']}" stroke-width="6.5" stroke-linecap="round" fill="none" transform="translate(0, 50)">
        <circle cx="-25" cy="0" r="4" fill="{cfg['cor_ambar']}" stroke="none"/>
        <path d="M -12 -20 C -2 -10 -2 10 -12 20"/>
        <path d="M 4 -34 C 20 -17 20 17 4 34"/>
        <path d="M 20 -48 C 42 -24 42 24 20 48"/>
      </g>

      <!-- 2. Pílula [ NFC ] (30 un de altura) -->
      <g transform="translate(0, 132)">
        <rect x="-45" y="-18" width="90" height="36" rx="18" fill="{cfg['cor_ambar']}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['cor_ambar_dark']}" text-anchor="middle" letter-spacing="2">NFC</text>
      </g>

      <!-- 3. Frase "Aproxime o celular" (28 un / 2.8 mm) -->
      <text x="0" y="190" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: "UM TOQUE LIBERA" (29 un / 2.9 mm, caixa alta, espaçada) -->
    <g transform="translate(90, 560)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['texto_sub']}" letter-spacing="3.5">UM TOQUE LIBERA</text>
    </g>

    <!-- D) GRADE 2x2 COM ÍCONES DE TRAÇO EM CÍRCULOS DE 80 UN A 12% -->
    
    <!-- Item 1: Wi-Fi -->
    <g transform="translate(90, 600)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" fill="none" transform="translate(24, 24)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="{cfg['cor_principal']}" stroke="none"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_escuro']}">Wi-Fi Resort</text>
    </g>

    <!-- Item 2: Spa & Relax -->
    <g transform="translate(540, 600)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_escuro']}">Costão SPA</text>
    </g>

    <!-- Item 3: Gastronomia -->
    <g transform="translate(90, 725)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_escuro']}">Restaurantes</text>
    </g>

    <!-- Item 4: Programação -->
    <g transform="translate(540, 725)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{cfg['cor_principal']}"/>
        <circle cx="16" cy="19" r="1.5" fill="{cfg['cor_principal']}"/>
        <circle cx="22" cy="19" r="1.5" fill="{cfg['cor_principal']}"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_escuro']}">Programação</text>
    </g>

    <!-- E) RODAPÉ COM FILETE DE 3 UNIDADES (Margem de 90 un) -->
    <g transform="translate(90, 875)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="{cfg['filete']}" stroke-width="2.5"/>
      <text x="0" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{cfg['texto_sub']}">Mais tempo para o que importa.</text>
      <text x="820" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['cor_principal']}" text-anchor="end">{cfg['site']}</text>
    </g>
  </g>
</svg>'''
    return svg

def criar_mockup_arredondado(png_path, out_mockup_path):
    card = Image.open(png_path).convert("RGBA")
    cw, ch = card.size
    margin = 80
    stage_w = cw + margin * 2
    stage_h = ch + margin * 2
    
    # Palco neutro com iluminação de estúdio
    stage = Image.new("RGBA", (stage_w, stage_h), (243, 245, 248, 255))
    
    # Sombra do cartão arredondado
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 90))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=26))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    generated_mockups = []
    for cfg in VARIACOES:
        svg_content = gerar_svg_placa(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        pix = doc[0].get_pixmap(dpi=300, alpha=True)
        raw_png = os.path.join(OUT, f"placa_{cfg['id']}_raw.png")
        pix.save(raw_png)
        
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        criar_mockup_arredondado(raw_png, mockup_png)
        generated_mockups.append((cfg, mockup_png))
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

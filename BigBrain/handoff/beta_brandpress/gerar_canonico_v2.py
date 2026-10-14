# -*- coding: utf-8 -*-
"""
Implementação Canônica da Especificação 'placa-nfc-design' (v2 - Protocolo Completo Anti-Colisão)
Para o Costão do Santinho Resort.

Parâmetros Obrigatórios:
- Prancheta 1000x1000 com cantos arredondados rx="60" ry="60"
- Margens e Zonas Anti-Colisão:
  - ZONA A (Logo): X: 90 a 670 | Y: 90 a 460 -> image x="90" y="110" width="540" height="260" preserveAspectRatio="xMidYMid meet"
  - ZONA B (NFC): X: 700 a 910 | Y: 90 a 460 -> Centro X=800
    - Ponto: circle cx="720" cy="180" r="14"
    - Arcos (stroke-width="14"):
      - M 760 125 Q 830 180 760 235
      - M 800 95 Q 880 180 800 265
      - M 840 65 Q 930 180 840 295
    - Pílula: x="710" y="300" width="180" height="46" rx="23"
    - Texto NFC: x="800" y="333" font-size="30" font-weight="800" letter-spacing="3"
    - Frase Apoio: x="800" y="378" font-size="28" text-anchor="middle" "Aproxime o celular"
  - DIVISÃO CURVA: d="M0,0 H1000 V540 Q500,490 0,540 Z" (bicolor)
  - ZONA C (Chamada): Y: 600 a 640 -> "UM TOQUE LIBERA" x="90" y="620" font-size="29" font-weight="800" letter-spacing="4"
  - ZONA D (Grade 2x2):
    - Círculos de raio 40 (diâmetro 80) a 12% opacidade
    - Item 1 (Wi-Fi): círculo (90, 670), texto x="190" y="722" font-size="44"
    - Item 2 (Serviços / Cardápio): círculo (540, 670), texto x="640" y="722" font-size="44"
    - Item 3 (Descontos / SPA): círculo (90, 810), texto x="190" y="862" font-size="44"
    - Item 4 (Horários / Recepção): círculo (540, 810), texto x="640" y="862" font-size="44"
  - ZONA E (Rodapé):
    - Divisor: line x1="90" y1="890" x2="910" y2="890" stroke-width="3" opacity="0.25"
    - Slogan: x="90" y="930" font-size="30" "Mais tempo para o que importa."
    - Site: x="910" y="930" font-size="30" text-anchor="end" "costao.com.br"

3 Variações Estratégicas:
1. Opção 1 — Clássica Bicolor (Verde Floresta Costão #1E6B48 com base Creme #F5F0E6)
2. Opção 2 — Dark Elegance (Verde Floresta Noturna #0A231C total com Dourado Nobre #D4A853)
3. Opção 3 — Vibrant Brand (Azul Royal Santinho #1E6091 com base Gelo #F1F5F9)
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_canonico_v2"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES = [
    {
        "id": "1_classica_bicolor_verde",
        "nome": "Opção 1 — Clássica Bicolor (Verde Floresta Costão)",
        "tipo": "bicolor",
        "cor_topo_start": "#1E6B48",
        "cor_topo_end": "#154D34",
        "fundo_base": "#F5F0E6",
        "cor_nfc": "#E8A825",
        "cor_nfc_texto": "#154D34",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#5B6B62",
        "cor_texto_grade": "#154D34",
        "cor_rodape_texto": "#5B6B62",
        "cor_rodape_site": "#154D34",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "SPA & Lazer",
        "item4": "Horários"
    },
    {
        "id": "2_dark_elegance_luxo",
        "nome": "Opção 2 — Dark Elegance (Verde Floresta Profundo & Ouro)",
        "tipo": "dark",
        "cor_fundo_start": "#0E1F18",
        "cor_fundo_end": "#07120E",
        "fundo_base": "#0E1F18",
        "cor_nfc": "#D4A853",
        "cor_nfc_texto": "#07120E",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#D4A853",
        "cor_texto_grade": "#FAF8F2",
        "cor_rodape_texto": "#A3B3AA",
        "cor_rodape_site": "#D4A853",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "SPA & Lazer",
        "item4": "Horários"
    },
    {
        "id": "3_vibrant_brand_azul_royal",
        "nome": "Opção 3 — Vibrant Brand (Azul Royal Santinho · Mar Aberto)",
        "tipo": "bicolor",
        "cor_topo_start": "#1E6091",
        "cor_topo_end": "#144366",
        "fundo_base": "#F1F5F9",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#144366",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#5A738E",
        "cor_texto_grade": "#144366",
        "cor_rodape_texto": "#5A738E",
        "cor_rodape_site": "#1E6091",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "Serviços",
        "item4": "Horários"
    }
]

def gerar_svg_canonico(cfg):
    v_id = cfg["id"]
    is_dark = (cfg["tipo"] == "dark")
    
    if is_dark:
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="url(#gradFundo_{v_id})"/>
        <!-- Moldura sutil interna tom sobre tom -->
        <rect x="50" y="50" width="900" height="900" rx="40" fill="none" stroke="{cfg['cor_nfc']}" stroke-width="1.5" stroke-opacity="0.25"/>
        <rect x="70" y="580" width="860" height="300" rx="20" fill="rgba(255,255,255,0.02)" stroke="{cfg['cor_nfc']}" stroke-width="1" stroke-opacity="0.15"/>
        '''
        icone_stroke = cfg['cor_nfc']
        icone_fill_color = cfg['cor_nfc']
        icone_opacity = "0.15"
    else:
        # Traçado Canônico: d="M0,0 H1000 V540 Q500,490 0,540 Z"
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>
        <path d="M0,0 H1000 V540 Q500,490 0,540 Z" fill="url(#gradFundo_{v_id})"/>
        '''
        icone_stroke = cfg['cor_texto_grade']
        icone_fill_color = cfg['cor_texto_grade']
        icone_opacity = "0.12"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="card-shape">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="gradFundo_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg.get('cor_topo_start') or cfg.get('cor_fundo_start')}"/>
      <stop offset="100%" stop-color="{cfg.get('cor_topo_end') or cfg.get('cor_fundo_end')}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#card-shape)">
    {fundo_layer}

    <!-- ZONA A: LOGO / MARCA (X: 90 a 670 | Y: 90 a 460) -->
    <image x="90" y="110" width="540" height="260" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{logo_b64}"/>

    <!-- ZONA B: SENSOR NFC (X: 700 a 910 | Y: 90 a 460, Centro X=800) -->
    <!-- 1. Ponto Central e 3 Arcos Concêntricos Geométricos Canônicos -->
    <g fill="none" stroke="{cfg['cor_nfc']}" stroke-width="14" stroke-linecap="round">
      <circle cx="720" cy="180" r="14" fill="{cfg['cor_nfc']}" stroke="none"/>
      <path d="M 760 125 Q 830 180 760 235"/>
      <path d="M 800 95 Q 880 180 800 265"/>
      <path d="M 840 65 Q 930 180 840 295"/>
    </g>

    <!-- 2. Etiqueta Pílula NFC -->
    <rect x="710" y="300" width="180" height="46" rx="23" fill="{cfg['cor_nfc']}"/>
    <text x="800" y="333" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="30" font-weight="800" fill="{cfg['cor_nfc_texto']}" text-anchor="middle" letter-spacing="3">NFC</text>

    <!-- 3. Frase de Apoio -->
    <text x="800" y="378" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="28" font-weight="500" fill="{cfg['texto_aproxime']}" text-anchor="middle">Aproxime o celular</text>

    <!-- ZONA C: CHAMADA 'UM TOQUE LIBERA' (X: 90 a 910 | Y: 600 a 640) -->
    <text x="90" y="620" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="29" font-weight="800" fill="{cfg['cor_chamada']}" letter-spacing="4">UM TOQUE LIBERA</text>

    <!-- ZONA D: GRADE DE BENEFÍCIOS 2×2 -->
    <!-- Item 1 (Wi-Fi): Círculo em (90, 670), Texto em (190, 722) -->
    <g>
      <circle cx="130" cy="710" r="40" fill="{icone_fill_color}" fill-opacity="{icone_opacity}"/>
      <!-- Ícone Wi-Fi (Centro em 130, 710) -->
      <g stroke="{icone_stroke}" stroke-width="3" stroke-linecap="round" fill="none" transform="translate(114, 694)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="{icone_stroke}" stroke="none"/>
      </g>
      <text x="190" y="722" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item1']}</text>
    </g>

    <!-- Item 2 (Cardápio / Serviços): Círculo em (540, 670), Texto em (640, 722) -->
    <g>
      <circle cx="580" cy="710" r="40" fill="{icone_fill_color}" fill-opacity="{icone_opacity}"/>
      <!-- Ícone Cardápio (Centro em 580, 710) -->
      <g stroke="{icone_stroke}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(564, 694)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="640" y="722" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item2']}</text>
    </g>

    <!-- Item 3 (SPA & Lazer): Círculo em (90, 810), Texto em (190, 862) -->
    <g>
      <circle cx="130" cy="850" r="40" fill="{icone_fill_color}" fill-opacity="{icone_opacity}"/>
      <!-- Ícone SPA Flor de Lótus (Centro em 130, 850) -->
      <g stroke="{icone_stroke}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(114, 834)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="190" y="862" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item3']}</text>
    </g>

    <!-- Item 4 (Horários / Recepção): Círculo em (540, 810), Texto em (640, 862) -->
    <g>
      <circle cx="580" cy="850" r="40" fill="{icone_fill_color}" fill-opacity="{icone_opacity}"/>
      <!-- Ícone Calendário / Horários (Centro em 580, 850) -->
      <g stroke="{icone_stroke}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(564, 834)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{icone_stroke}"/>
        <circle cx="16" cy="19" r="1.5" fill="{icone_stroke}"/>
        <circle cx="22" cy="19" r="1.5" fill="{icone_stroke}"/>
      </g>
      <text x="640" y="862" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item4']}</text>
    </g>

    <!-- ZONA E: RODAPÉ INSTITUCIONAL (Divisor Y=890 | Slogan & Site Y=930) -->
    <line x1="90" y1="890" x2="910" y2="890" stroke="{cfg['cor_texto_grade']}" stroke-width="3" opacity="0.25"/>
    <text x="90" y="930" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="30" font-weight="500" fill="{cfg['cor_rodape_texto']}">Mais tempo para o que importa.</text>
    <text x="910" y="930" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="30" font-weight="700" fill="{cfg['cor_rodape_site']}" text-anchor="end">costao.com.br</text>
  </g>
</svg>'''
    return svg

def criar_mockup(png_path, out_mockup_path):
    card = Image.open(png_path).convert("RGBA")
    cw, ch = card.size
    margin = 80
    stage_w = cw + margin * 2
    stage_h = ch + margin * 2
    
    stage = Image.new("RGBA", (stage_w, stage_h), (242, 245, 248, 255))
    
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 100))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES:
        svg_content = gerar_svg_canonico(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        pix = doc[0].get_pixmap(dpi=300, alpha=True)
        raw_png = os.path.join(OUT, f"placa_{cfg['id']}_raw.png")
        pix.save(raw_png)
        
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        criar_mockup(raw_png, mockup_png)
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

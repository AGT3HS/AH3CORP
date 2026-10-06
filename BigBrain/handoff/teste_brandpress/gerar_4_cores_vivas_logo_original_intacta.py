# -*- coding: utf-8 -*-
"""
Geração das 4 Variações de Placa NFC 100x100 mm com a LOGO ORIGINAL 100% INTACTA
- A logo do cliente (imagem original enviada) NUNCA é alterada, pintada ou modificada em NENHUMA variação.
- Cada variação usa uma cor de topo VIVA e DISTINTA, que acolhe perfeitamente a logo original:
  1. Verde Floresta Nobre (#1E6B48 a #134B32)
  2. Azul Royal Náutico Vivo (#1E6091 a #134368)
  3. Azul Petróleo Costão (#214E68 a #15364A)
  4. Verde Musgo & Oliva Iluminado (#2D5A3E a #1C3D28)
- Cantos arredondados rx="60" e ry="60" (6 mm).
- Margem de segurança de 90 unidades (9 mm).
- Curva: 53 mm (Y=530) nas bordas e 48 mm (Y=480) no centro.
- Tamanhos exatos da Seção 3: NFC 30 un, Aproxime 28 un, Um toque libera 29 un, Itens 44 un, Rodapé 30 un.
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_4_cores_vivas_logo_original_intacta"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_original_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES_VIVAS = [
    {
        "id": "1_verde_floresta_vivo",
        "nome": "Variação 1 — Verde Floresta Costão · Mata Atlântica Viva (#1E6B48)",
        "cor_topo_start": "#1E6B48",
        "cor_topo_end": "#134B32",
        "fundo_base": "#F5F0E6",
        "cor_nfc": "#E8A825",
        "cor_nfc_texto": "#134B32",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#576B60",
        "cor_texto_grade": "#134B32",
        "cor_rodape_texto": "#576B60",
        "cor_rodape_site": "#134B32",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "SPA",
        "item4": "Horários"
    },
    {
        "id": "2_azul_royal_santinho",
        "nome": "Variação 2 — Azul Royal Santinho · Mar Iluminado (#1E6091)",
        "cor_topo_start": "#1E6091",
        "cor_topo_end": "#134368",
        "fundo_base": "#F1F5F9",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#134368",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#54728E",
        "cor_texto_grade": "#134368",
        "cor_rodape_texto": "#54728E",
        "cor_rodape_site": "#1E6091",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "Serviços",
        "item4": "Horários"
    },
    {
        "id": "3_azul_petroleo_costao",
        "nome": "Variação 3 — Azul Petróleo Costão · Requinte Marítimo (#214E68)",
        "cor_topo_start": "#214E68",
        "cor_topo_end": "#15364A",
        "fundo_base": "#F3F7FA",
        "cor_nfc": "#E8A825",
        "cor_nfc_texto": "#15364A",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#567082",
        "cor_texto_grade": "#15364A",
        "cor_rodape_texto": "#567082",
        "cor_rodape_site": "#214E68",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "SPA",
        "item4": "Horários"
    },
    {
        "id": "4_verde_musgo_oliva",
        "nome": "Variação 4 — Verde Musgo & Oliva Iluminado · Natureza Preservada (#2D5A3E)",
        "cor_topo_start": "#2D5A3E",
        "cor_topo_end": "#1C3D28",
        "fundo_base": "#F5F8F5",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#1C3D28",
        "texto_aproxime": "#FAF8F2",
        "cor_chamada": "#5A7363",
        "cor_texto_grade": "#1C3D28",
        "cor_rodape_texto": "#5A7363",
        "cor_rodape_site": "#2D5A3E",
        "item1": "Wi-Fi",
        "item2": "Cardápio",
        "item3": "Serviços",
        "item4": "Horários"
    }
]

def gerar_svg_original(cfg):
    v_id = cfg["id"]
    
    # Curva suave: 53 mm (Y=530) nas bordas e 48 mm (Y=480) no centro
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="gradFundo_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg['cor_topo_start']}"/>
      <stop offset="100%" stop-color="{cfg['cor_topo_end']}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Base Clara Inferior -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>

    <!-- Divisão Superior Bicolor com Cor Viva e Curva Suave -->
    <path d="M 0,0 L 1000,0 L 1000,530 Q 500,430 0,530 Z" fill="url(#gradFundo_{v_id})"/>

    <!-- 1. ZONA A: LOGO ORIGINAL INTACTA (NENHUMA ALTERAÇÃO DE COR, Limite X <= 670) -->
    <image x="90" y="110" width="540" height="260" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{logo_original_b64}"/>

    <!-- 2. ZONA B: SENSOR NFC DE 220 UN (22 mm) + PÍLULA + FRASE (Centro X=800) -->
    <!-- Símbolo NFC: Ponto e 3 Arcos Concêntricos -->
    <g fill="none" stroke="{cfg['cor_nfc']}" stroke-width="14" stroke-linecap="round">
      <circle cx="720" cy="180" r="14" fill="{cfg['cor_nfc']}" stroke="none"/>
      <path d="M 760 125 Q 830 180 760 235"/>
      <path d="M 800 95 Q 880 180 800 265"/>
      <path d="M 840 65 Q 930 180 840 295"/>
    </g>

    <!-- Etiqueta Pílula NFC (Texto 3.0 mm = 30 un, espaçada) -->
    <rect x="710" y="300" width="180" height="46" rx="23" fill="{cfg['cor_nfc']}"/>
    <text x="800" y="333" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="30" font-weight="800" fill="{cfg['cor_nfc_texto']}" text-anchor="middle" letter-spacing="3">NFC</text>

    <!-- Frase 'Aproxime o celular' (2.8 mm = 28 un) -->
    <text x="800" y="378" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="28" font-weight="500" fill="{cfg['texto_aproxime']}" text-anchor="middle">Aproxime o celular</text>

    <!-- 3. ZONA C: CHAMADA 'UM TOQUE LIBERA' (2.9 mm = 29 un, caixa alta, espaçada) -->
    <text x="90" y="615" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="29" font-weight="800" fill="{cfg['cor_chamada']}" letter-spacing="4">UM TOQUE LIBERA</text>

    <!-- 4. ZONA D: GRADE 2x2 COM RÓTULOS DE UMA PALAVRA (4.4 mm = 44 un) & CÍRCULOS DE 80 UN (8 mm) -->
    
    <!-- Item 1 (Wi-Fi): Círculo (130, 710), Texto (190, 724) -->
    <g>
      <circle cx="130" cy="710" r="40" fill="{cfg['cor_texto_grade']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_texto_grade']}" stroke-width="3" stroke-linecap="round" fill="none" transform="translate(114, 694)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="{cfg['cor_texto_grade']}" stroke="none"/>
      </g>
      <text x="190" y="724" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item1']}</text>
    </g>

    <!-- Item 2 (Cardápio): Círculo (580, 710), Texto (640, 724) -->
    <g>
      <circle cx="580" cy="710" r="40" fill="{cfg['cor_texto_grade']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_texto_grade']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(564, 694)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="640" y="724" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item2']}</text>
    </g>

    <!-- Item 3 (SPA / Serviços): Círculo (130, 840), Texto (190, 854) -->
    <g>
      <circle cx="130" cy="840" r="40" fill="{cfg['cor_texto_grade']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_texto_grade']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(114, 824)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="190" y="854" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item3']}</text>
    </g>

    <!-- Item 4 (Horários): Círculo (580, 840), Texto (640, 854) -->
    <g>
      <circle cx="580" cy="840" r="40" fill="{cfg['cor_texto_grade']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_texto_grade']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(564, 824)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{cfg['cor_texto_grade']}"/>
        <circle cx="16" cy="19" r="1.5" fill="{cfg['cor_texto_grade']}"/>
        <circle cx="22" cy="19" r="1.5" fill="{cfg['cor_texto_grade']}"/>
      </g>
      <text x="640" y="854" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="{cfg['cor_texto_grade']}">{cfg['item4']}</text>
    </g>

    <!-- 5. ZONA E: RODAPÉ INSTITUCIONAL (Filete 3 un a 30%, Textos 3.0 mm = 30 un) -->
    <line x1="90" y1="890" x2="910" y2="890" stroke="{cfg['cor_texto_grade']}" stroke-width="3" opacity="0.30"/>
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
    for cfg in VARIACOES_VIVAS:
        svg_content = gerar_svg_original(cfg)
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

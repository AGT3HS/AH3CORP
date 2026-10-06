# -*- coding: utf-8 -*-
"""
Geração Canônica de 3 Variações de Placa NFC 100x100 mm do Costão do Santinho
REGRAS ESTRITAS E INEGOCIÁVEIS:
1. Usar ESTRITAMENTE as cores da paleta oficial do hotel:
   - #1B3B2B (Verde Floresta)
   - #2C3E50 (Azul Petróleo)
   - #8C7B63 (Fendi / Areia)
   - #D4AF37 (Dourado Imperial)
2. Símbolo e Pílula NFC com a cor exata do guia original: #D4AF37 (Dourado Imperial) em TODAS as peças.
3. A cor do topo onde fica a logo muda estritamente entre as cores da paleta oficial do hotel:
   - Variação 1: #1B3B2B (Verde Floresta)
   - Variação 2: #2C3E50 (Azul Petróleo)
   - Variação 3: #8C7B63 (Fendi / Areia)
4. Modelo e anatomia 100% IDÊNTICOS em todas as peças.
5. Logo original do Costão 100% INTACTA.
6. Cantos arredondados físicos REAIS (rx="60" / 6 mm) com recorte perfeito e sombra projetada.
"""
import os
import base64
from PIL import Image, ImageDraw, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/teste_paleta_oficial_estrita"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

# Cor do NFC do GUIA ORIGINAL: Dourado Imperial (#D4AF37)
NFC_DOURADO_GUIA = "#D4AF37"
NFC_TEXTO_ESCURO = "#080B09"

VARIACOES_OFICIAIS = [
    {
        "id": "1_verde_floresta_1B3B2B",
        "nome": "Variação 1 — Verde Floresta (#1B3B2B)",
        "cor_topo": "#1B3B2B",
        "cor_detalhe": "#1B3B2B",
        "cor_base": "#F8F9FA",
        "site_cor": "#1B3B2B"
    },
    {
        "id": "2_azul_petroleo_2C3E50",
        "nome": "Variação 2 — Azul Petróleo (#2C3E50)",
        "cor_topo": "#2C3E50",
        "cor_detalhe": "#2C3E50",
        "cor_base": "#F8F9FA",
        "site_cor": "#2C3E50"
    },
    {
        "id": "3_fendi_areia_8C7B63",
        "nome": "Variação 3 — Fendi / Areia (#8C7B63)",
        "cor_topo": "#8C7B63",
        "cor_detalhe": "#8C7B63",
        "cor_base": "#F8F9FA",
        "site_cor": "#8C7B63"
    }
]

def gerar_svg_estrito(cfg):
    v_id = cfg["id"]
    cor_topo = cfg["cor_topo"]
    
    # SVG 1000x1000 rigorosamente idêntico em todas as peças
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Fundo Base Claro Acolhedor -->
    <rect width="1000" height="1000" fill="{cfg['cor_base']}"/>

    <!-- Topo Sólido com a Cor Oficial Estrita da Paleta do Hotel -->
    <path d="M0,0 L1000,0 L1000,430 Q500,485 0,430 Z" fill="{cor_topo}"/>

    <!-- A) LOGO OFICIAL INTACTA (X=80, Y=135) -->
    <g transform="translate(80, 135)">
      <image href="data:image/png;base64,{logo_b64}" width="420" height="150" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC DO GUIA ORIGINAL (#D4AF37) EM TODAS AS PEÇAS -->
    <g transform="translate(830, 95)">
      <!-- 1. Ondas NFC (Traço Fino do Guia Original: stroke-width=6) -->
      <g stroke="{NFC_DOURADO_GUIA}" stroke-width="6" stroke-linecap="round" fill="none" transform="translate(0, 40)">
        <circle cx="-25" cy="0" r="3.5" fill="{NFC_DOURADO_GUIA}" stroke="none"/>
        <path d="M-12,-18 C-3,-9 -3,9 -12,18"/>
        <path d="M3,-30 C18,-15 18,15 3,30"/>
        <path d="M18,-42 C38,-21 38,21 18,42"/>
      </g>

      <!-- 2. Pílula [ NFC ] (Guia Original: 88x36 em #D4AF37) -->
      <g transform="translate(0, 115)">
        <rect x="-44" y="-18" width="88" height="36" rx="18" fill="{NFC_DOURADO_GUIA}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{NFC_TEXTO_ESCURO}" text-anchor="middle" letter-spacing="1.5">NFC</text>
      </g>

      <!-- 3. Frase Aproxime o celular -->
      <text x="0" y="170" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: UM TOQUE LIBERA -->
    <g transform="translate(80, 520)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#6B7280" letter-spacing="3">UM TOQUE LIBERA</text>
    </g>

    <!-- D) ITENS EM GRADE 2x2 COM EQUILÍBRIO VISUAL -->
    
    <!-- Item 1: Spa & Terapias -->
    <g transform="translate(80, 565)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_detalhe']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_detalhe']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M16 26 C16 12 6 8 2 18 C2 24 10 26 16 26 Z"/>
        <path d="M16 26 C16 12 26 8 30 18 C30 24 22 26 16 26 Z"/>
        <path d="M16 26 C11 16 13 6 16 3 C19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Costão SPA &amp; Relax</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Massagens, hidro e rituais</text>
    </g>

    <!-- Item 2: Shows & Programação -->
    <g transform="translate(520, 565)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_detalhe']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_detalhe']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{cfg['cor_detalhe']}"/>
        <circle cx="16" cy="19" r="1.5" fill="{cfg['cor_detalhe']}"/>
        <circle cx="22" cy="19" r="1.5" fill="{cfg['cor_detalhe']}"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Shows &amp; Programação</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Agenda diária e atrações</text>
    </g>

    <!-- Item 3: Gastronomia All-Inclusive -->
    <g transform="translate(80, 715)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_detalhe']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_detalhe']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M5 3 L5 12 C5 15 8 17 11 17 L11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M17 3 L17 12 C17 15 14 17 11 17"/>
        <path d="M23 3 C27 8 27 15 24 18 L24 29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Restaurantes &amp; Bares</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Cardápios, reservas e horários</text>
    </g>

    <!-- Item 4: Mapa & Experiência Resort -->
    <g transform="translate(520, 715)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_detalhe']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_detalhe']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <polygon points="3 7 11 3 21 7 29 3 29 25 21 29 11 25 3 29"/>
        <line x1="11" y1="3" x2="11" y2="25"/>
        <line x1="21" y1="7" x2="21" y2="29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Mapa &amp; Guia Resort</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Wi-Fi, trilhas e arqueologia</text>
    </g>

    <!-- E) RODAPÉ ANATÔMICO COM FILETE -->
    <g transform="translate(80, 890)">
      <line x1="0" y1="0" x2="840" y2="0" stroke="#E5E7EB" stroke-width="1.5"/>
      <text x="0" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="#6B7280">Experiência All-Inclusive na Praia do Santinho.</text>
      <text x="840" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['site_cor']}" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''
    return svg

def renderizar_mockup_com_cantos_reais(svg_path, out_mockup_path):
    doc = fitz.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300, alpha=True)
    card_img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    
    # Corte exato com raio de 6mm (rx=60 em 1000 = 6% da largura)
    w, h = card_img.size
    radius = int(w * 0.060)
    mask = Image.new("L", (w, h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
    
    card_cut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card_cut.paste(card_img, (0, 0), mask)
    
    margin = int(w * 0.08)
    stage_w = w + margin * 2
    stage_h = h + margin * 2
    
    stage = Image.new("RGBA", (stage_w, stage_h), (226, 232, 240, 255))
    
    shadow = Image.new("RGBA", (w, h), (15, 23, 42, 110))
    shadow.putalpha(mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=int(w * 0.035)))
    
    stage.paste(shadow_blurred, (margin + int(w * 0.005), margin + int(h * 0.016)), shadow_blurred)
    stage.paste(card_cut, (margin, margin), card_cut)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES_OFICIAIS:
        svg_content = gerar_svg_estrito(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        renderizar_mockup_com_cantos_reais(svg_path, mockup_png)
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

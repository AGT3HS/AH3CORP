# -*- coding: utf-8 -*-
"""
Geração de 4 Placas NFC 100x100 mm com:
1. CANTOS ARREDONDADOS FÍSICOS REAIS E EVIDENTES (Corte perfeito do cartão com máscara alpha e fundo neutro de contraste).
2. CORES DO TOPO 100% DISTINTAS E IMPACTANTES (Verde Esmeralda #1E7E53, Azul Cobalto Vivo #1565C0, Dourado Ocre Solar #C88D18, Terracota Nobre #B84A2A).
3. HARMONIA TOTAL: O topo muda de cor drasticamente em cada peça, enquanto a logo original em branco/ouro se destaca perfeitamente.
4. PROPORÇÕES CANÔNICAS: NFC fino (stroke-width=6), pílula delicada, grade 2x2 elegante e legível.
"""
import os
import base64
from PIL import Image, ImageDraw, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/teste_cores_claras_bordas_reais"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES_CORES = [
    {
        "id": "1_verde_esmeralda_vivo",
        "nome": "1. Verde Esmeralda Vibrante (Natureza Viva)",
        "cor_topo_start": "#1E7E53",
        "cor_topo_end": "#145C3B",
        "cor_nfc": "#F1C40F",
        "cor_nfc_texto": "#0D3823",
        "cor_base": "#F6FAF7",
        "cor_detalhe": "#1E7E53",
        "site_cor": "#1E7E53"
    },
    {
        "id": "2_azul_cobalto_maritimo",
        "nome": "2. Azul Cobalto Vivo (Mar Aberto do Santinho)",
        "cor_topo_start": "#1976D2",
        "cor_topo_end": "#115293",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#0B3159",
        "cor_base": "#F4F8FC",
        "cor_detalhe": "#1976D2",
        "site_cor": "#1976D2"
    },
    {
        "id": "3_dourado_ocre_solar",
        "nome": "3. Dourado Solar & Âmbar (Pôr do Sol & Luxo)",
        "cor_topo_start": "#D49B24",
        "cor_topo_end": "#A67412",
        "cor_nfc": "#145C3B",
        "cor_nfc_texto": "#FFFFFF",
        "cor_base": "#FCFAF4",
        "cor_detalhe": "#A67412",
        "site_cor": "#A67412"
    },
    {
        "id": "4_terracota_rupestre_nobre",
        "nome": "4. Terracota Nobre (Arqueologia & Dunas)",
        "cor_topo_start": "#C05232",
        "cor_topo_end": "#8F381F",
        "cor_nfc": "#F1C40F",
        "cor_nfc_texto": "#521C0D",
        "cor_base": "#FAF5F2",
        "cor_detalhe": "#C05232",
        "site_cor": "#C05232"
    }
]

def gerar_svg(cfg):
    v_id = cfg["id"]
    
    # SVG puro em 1000x1000 com cantos rx="60" e ry="60" (6 mm real)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="topoGrad_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg['cor_topo_start']}"/>
      <stop offset="100%" stop-color="{cfg['cor_topo_end']}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Fundo Base Claro Acolhedor -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['cor_base']}"/>

    <!-- Topo Colorido Vibrante com Curva Suave Canônica -->
    <path d="M0,0 L1000,0 L1000,430 Q500,485 0,430 Z" fill="url(#topoGrad_{v_id})"/>

    <!-- A) LOGO ORIGINAL OFICIAL DO COSTÃO (Posição nobre, respiro perfeito: X=80, Y=135) -->
    <g transform="translate(80, 135)">
      <image href="data:image/png;base64,{logo_b64}" width="420" height="150" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC SUTIL E PROPORCIONAL (Centralizado em X=830, Y=95) -->
    <g transform="translate(830, 95)">
      <!-- 1. Ondas NFC (Traço fino de 6px) -->
      <g stroke="{cfg['cor_nfc']}" stroke-width="6" stroke-linecap="round" fill="none" transform="translate(0, 40)">
        <circle cx="-25" cy="0" r="3.5" fill="{cfg['cor_nfc']}" stroke="none"/>
        <path d="M-12,-18 C-3,-9 -3,9 -12,18"/>
        <path d="M3,-30 C18,-15 18,15 3,30"/>
        <path d="M18,-42 C38,-21 38,21 18,42"/>
      </g>

      <!-- 2. Pílula [ NFC ] (Delicada: 88x36) -->
      <g transform="translate(0, 115)">
        <rect x="-44" y="-18" width="88" height="36" rx="18" fill="{cfg['cor_nfc']}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['cor_nfc_texto']}" text-anchor="middle" letter-spacing="1.5">NFC</text>
      </g>

      <!-- 3. Texto Aproxime o celular -->
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

    <!-- E) RODAPÉ ANATÔMICO COM FILETE SUAVE -->
    <g transform="translate(80, 890)">
      <line x1="0" y1="0" x2="840" y2="0" stroke="#E5E7EB" stroke-width="1.5"/>
      <text x="0" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="#6B7280">Experiência All-Inclusive na Praia do Santinho.</text>
      <text x="840" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['site_cor']}" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''
    return svg

def renderizar_mockup_com_cantos_reais(svg_path, out_mockup_path):
    # Renderiza SVG transparente em altíssima definição
    doc = fitz.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300, alpha=True)
    card_img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    
    # Criação da Máscara Exata de Cantos Arredondados (Raio de 6% = 6mm em 100mm)
    w, h = card_img.size
    radius = int(w * 0.060)  # 60 unidades em 1000 = raio de 6mm
    mask = Image.new("L", (w, h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
    
    # Aplica o corte exato com anti-aliasing nos cantos
    card_cut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card_cut.paste(card_img, (0, 0), mask)
    
    # Montagem do Mockup sobre palco escuro/neutro com contraste e sombra profunda
    margin = int(w * 0.08)
    stage_w = w + margin * 2
    stage_h = h + margin * 2
    
    # Palco em tom grafite suave para evidenciar os 4 cantos arredondados brancos/claros
    stage = Image.new("RGBA", (stage_w, stage_h), (228, 233, 240, 255))
    
    # Sombra física realista do cartão arredondado
    shadow = Image.new("RGBA", (w, h), (10, 20, 35, 120))
    shadow.putalpha(mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=int(w * 0.035)))
    
    # Aplica sombra deslocada
    stage.paste(shadow_blurred, (margin + int(w * 0.005), margin + int(h * 0.018)), shadow_blurred)
    # Aplica cartão recortado
    stage.paste(card_cut, (margin, margin), card_cut)
    
    # Salva imagem final
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES_CORES:
        svg_content = gerar_svg(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        renderizar_mockup_com_cantos_reais(svg_path, mockup_png)
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

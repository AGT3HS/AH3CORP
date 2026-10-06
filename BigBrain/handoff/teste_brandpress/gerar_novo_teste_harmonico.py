# -*- coding: utf-8 -*-
"""
Geração do Novo Teste de Placa NFC 100x100 mm do Costão do Santinho
Baseado no modelo canônico original de design equilibrado (01_costao_do_santinho_card_10x10.svg):
1. Logo oficial original 100% INTACTA, posicionada com elegância e respiro (X=80, Y=135).
2. Cluster NFC perfeitamente proporcional: traço fino (stroke-width=6), pílula delicada (88x36), sem poluir a peça.
3. Topo colorido rico, vivo e nobre com curva suave orgânica (Y=430 nas bordas, Y=485 no centro).
4. Grade 2x2 com ícones de traço leve (3.5 px), títulos expressivos e subtítulos descritivos legíveis.
5. Base clara em #F8F9FA com respiro generoso, rodapé discreto com filete fino e cantos arredondados rx="60" (6 mm).
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/novo_teste_harmonico"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES_HARMONICAS = [
    {
        "id": "1_verde_esmeralda_costao",
        "nome": "1. Verde Esmeralda Nobre (Identidade Costão Viva)",
        "topo_grad_1": "#1B6B48",
        "topo_grad_2": "#104D33",
        "cor_nfc": "#F09C24",
        "cor_nfc_texto": "#0A2419",
        "cor_icone_fill": "#1B6B48",
        "cor_icone_stroke": "#1B6B48",
        "titulo_cor": "#111827",
        "subtitulo_cor": "#4B5563",
        "site_cor": "#1B6B48",
        "fundo_base": "#F8F9FA"
    },
    {
        "id": "2_azul_royal_santinho",
        "nome": "2. Azul Royal Náutico (Mar da Praia do Santinho)",
        "topo_grad_1": "#1E6091",
        "topo_grad_2": "#134266",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#0E2B42",
        "cor_icone_fill": "#1E6091",
        "cor_icone_stroke": "#1E6091",
        "titulo_cor": "#111827",
        "subtitulo_cor": "#4B5563",
        "site_cor": "#1E6091",
        "fundo_base": "#F8F9FA"
    },
    {
        "id": "3_azul_petroleo_luxo",
        "nome": "3. Azul Petróleo & Ouro (Sofisticação Noturna)",
        "topo_grad_1": "#214E68",
        "topo_grad_2": "#153548",
        "cor_nfc": "#E0A33A",
        "cor_nfc_texto": "#0E2330",
        "cor_icone_fill": "#214E68",
        "cor_icone_stroke": "#214E68",
        "titulo_cor": "#111827",
        "subtitulo_cor": "#4B5563",
        "site_cor": "#214E68",
        "fundo_base": "#F8F9FA"
    }
]

def gerar_svg(cfg):
    v_id = cfg["id"]
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="topoGrad_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg['topo_grad_1']}"/>
      <stop offset="100%" stop-color="{cfg['topo_grad_2']}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Base Clara Inferior Texturizada e Leve -->
    <rect width="1000" height="1000" fill="{cfg['fundo_base']}"/>

    <!-- Divisão Superior Colorida e Orgânica (Curva Suave Canônica) -->
    <path d="M0,0 L1000,0 L1000,430 Q500,485 0,430 Z" fill="url(#topoGrad_{v_id})"/>

    <!-- A) LOGO OFICIAL ORIGINAL (Posicionamento nobre, respiro perfeito: X=80, Y=135) -->
    <g transform="translate(80, 135)">
      <image href="data:image/png;base64,{logo_b64}" width="420" height="150" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC SUTIL E PROPORCIONAL (Centralizado no topo direito em X=830, Y=95) -->
    <g transform="translate(830, 95)">
      <!-- 1. Ondas NFC (Traço fino de 6px, escala harmoniosa) -->
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

    <!-- C) CHAMADA: UM TOQUE LIBERA (Elegante e sutil) -->
    <g transform="translate(80, 520)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#6B7280" letter-spacing="3">UM TOQUE LIBERA</text>
    </g>

    <!-- D) ITENS EM GRADE 2x2 COM EQUILÍBRIO VISUAL E HIERARQUIA TIPOGRÁFICA -->
    
    <!-- Item 1: Spa & Terapias -->
    <g transform="translate(80, 565)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_icone_fill']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_icone_stroke']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M16 26 C16 12 6 8 2 18 C2 24 10 26 16 26 Z"/>
        <path d="M16 26 C16 12 26 8 30 18 C30 24 22 26 16 26 Z"/>
        <path d="M16 26 C11 16 13 6 16 3 C19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{cfg['titulo_cor']}">Costão SPA &amp; Relax</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{cfg['subtitulo_cor']}">Massagens, hidro e rituais</text>
    </g>

    <!-- Item 2: Shows & Programação -->
    <g transform="translate(520, 565)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_icone_fill']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_icone_stroke']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{cfg['cor_icone_stroke']}"/>
        <circle cx="16" cy="19" r="1.5" fill="{cfg['cor_icone_stroke']}"/>
        <circle cx="22" cy="19" r="1.5" fill="{cfg['cor_icone_stroke']}"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{cfg['titulo_cor']}">Shows &amp; Programação</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{cfg['subtitulo_cor']}">Agenda diária e atrações</text>
    </g>

    <!-- Item 3: Gastronomia All-Inclusive -->
    <g transform="translate(80, 715)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_icone_fill']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_icone_stroke']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M5 3 L5 12 C5 15 8 17 11 17 L11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M17 3 L17 12 C17 15 14 17 11 17"/>
        <path d="M23 3 C27 8 27 15 24 18 L24 29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{cfg['titulo_cor']}">Restaurantes &amp; Bares</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{cfg['subtitulo_cor']}">Cardápios, reservas e horários</text>
    </g>

    <!-- Item 4: Mapa & Experiência Resort -->
    <g transform="translate(520, 715)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_icone_fill']}" fill-opacity="0.10"/>
      <g stroke="{cfg['cor_icone_stroke']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <polygon points="3 7 11 3 21 7 29 3 29 25 21 29 11 25 3 29"/>
        <line x1="11" y1="3" x2="11" y2="25"/>
        <line x1="21" y1="7" x2="21" y2="29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{cfg['titulo_cor']}">Mapa &amp; Guia Resort</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{cfg['subtitulo_cor']}">Wi-Fi, trilhas e arqueologia</text>
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

def criar_mockup(png_path, out_mockup_path):
    card = Image.open(png_path).convert("RGBA")
    cw, ch = card.size
    margin = 80
    stage_w = cw + margin * 2
    stage_h = ch + margin * 2
    
    stage = Image.new("RGBA", (stage_w, stage_h), (242, 245, 248, 255))
    
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 90))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES_HARMONICAS:
        svg_content = gerar_svg(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        pix = doc[0].get_pixmap(dpi=300, alpha=True)
        raw_png = os.path.join(OUT, f"placa_{cfg['id']}_raw.png")
        pix.save(raw_png)
        
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        criar_mockup(raw_png, mockup_png)
        print(f"Gerado com sucesso: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

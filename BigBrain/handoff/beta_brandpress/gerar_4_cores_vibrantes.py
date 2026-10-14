# -*- coding: utf-8 -*-
"""
Geração de 4 Variações TOTALMENTE DISTINTAS e com Cores VIVAS da Paleta do Hotel:
1. VERDE FLORESTA COSTÃO (Verde Esmeralda Nobre e Vibrante #165B33)
2. AZUL OCEANO SANTINHO (Azul Marinho Costeiro Intenso #154360)
3. OURO & AREIA DOURADA (Dourado Quente e Fendi #C59B27 / #EAD8A4)
4. ÔNIX & OURO METÁLICO (Dark Luxe com Detalhes e Logo em Ouro Puro #D4AF37)

Cada variação possui:
- Cor de topo saturada, viva e imediatamente reconhecível (Verde real, Azul real, Dourado real, Ônix real).
- Tratamento e adaptação da Logo para combinar e destacar perfeitamente em cada tema.
- Ícones, títulos, pílula NFC e detalhes 100% harmonizados com a cor tema.
- Cantos arredondados rx="60" (6 mm) e margem de segurança de 9 mm.
"""
import os
import base64
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_4_cores_distintas"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"

# 1. Gerar variações visuais da logo para cada tema
# Logo 1: Branca com sol dourado (Padrão para fundo verde vivo)
# Logo 2: Branca e azul marinho (Padrão para fundo azul ou claro)
# Logo 3: Verde escuro institucional (Para fundo claro/dourado)
# Logo 4: Dourado monocromático ouro puro (Para fundo ônix)

im_logo = Image.open(LOGO_ORIGINAL).convert("RGBA")

# Versão 1: Logo Branca com Dourado (já pronta)
logo1_path = os.path.join(OUT, "logo_v1_white_gold.png")
im_logo.save(logo1_path)

# Versão 3: Logo Verde Floresta Intenso (#165B33)
logo_verde = Image.new("RGBA", im_logo.size, (22, 91, 51, 255))
r, g, b, alpha = im_logo.split()
logo_verde.putalpha(alpha)
logo3_path = os.path.join(OUT, "logo_v3_verde.png")
logo_verde.save(logo3_path)

# Versão 4: Logo Ouro Puro Monocromático (#D4AF37)
logo_ouro = Image.new("RGBA", im_logo.size, (212, 175, 55, 255))
logo_ouro.putalpha(alpha)
logo4_path = os.path.join(OUT, "logo_v4_ouro.png")
logo_ouro.save(logo4_path)

# Versão 2: Logo Branca com ciano/azul suave
logo2_path = logo1_path

with open(logo1_path, "rb") as f:
    b64_logo1 = base64.b64encode(f.read()).decode("utf-8")
with open(logo3_path, "rb") as f:
    b64_logo3 = base64.b64encode(f.read()).decode("utf-8")
with open(logo4_path, "rb") as f:
    b64_logo4 = base64.b64encode(f.read()).decode("utf-8")

TEMAS = [
    {
        "id": "1_verde_floresta_vivo",
        "nome": "1. Verde Floresta Costão (Verde Vivo & Dourado)",
        "intencao": "Verde esmeralda florestal intenso (#165B33), celebrando a natureza do Santinho.",
        "topo_grad_start": "#1E6B40",
        "topo_grad_end": "#114728",
        "logo_b64": b64_logo1,
        "nfc_simbolo": "#F1C40F",
        "nfc_pilula": "#F1C40F",
        "nfc_pilula_texto": "#0E3820",
        "fundo_base": "#F6FAF7",
        "cor_marca": "#165B33",
        "texto_itens": "#0D3820",
        "texto_sub": "#457056",
        "icone_bg": "#165B33",
        "filete": "rgba(22, 91, 51, 0.20)",
        "site": "costao.com.br"
    },
    {
        "id": "2_azul_oceano_real",
        "nome": "2. Azul Oceano Santinho (Azul Marinho Intenso & Âmbar)",
        "intencao": "Azul marinho oceânico vibrante (#1B4F72), remetendo ao mar da Praia do Santinho.",
        "topo_grad_start": "#24608A",
        "topo_grad_end": "#133D5B",
        "logo_b64": b64_logo1,
        "nfc_simbolo": "#FFA726",
        "nfc_pilula": "#FFA726",
        "nfc_pilula_texto": "#0E2B40",
        "fundo_base": "#F4F8FC",
        "cor_marca": "#1B4F72",
        "texto_itens": "#0E2B40",
        "texto_sub": "#466B88",
        "icone_bg": "#1B4F72",
        "filete": "rgba(27, 79, 114, 0.20)",
        "site": "costao.com.br"
    },
    {
        "id": "3_ouro_areia_dourada",
        "nome": "3. Ouro & Areia Dourada (Dourado Nobre & Logo Verde)",
        "intencao": "Topo em Dourado Solar nobre (#C59B27) com a Logo Oficial em Verde Floresta destacado.",
        "topo_grad_start": "#D4AF37",
        "topo_grad_end": "#B2881C",
        "logo_b64": b64_logo3,
        "nfc_simbolo": "#165B33",
        "nfc_pilula": "#165B33",
        "nfc_pilula_texto": "#FFFFFF",
        "fundo_base": "#FCFAF5",
        "cor_marca": "#B2881C",
        "texto_itens": "#165B33",
        "texto_sub": "#7A6836",
        "icone_bg": "#165B33",
        "filete": "rgba(178, 136, 28, 0.25)",
        "site": "costao.com.br"
    },
    {
        "id": "4_onix_ouro_metalico",
        "nome": "4. Ônix & Ouro Metálico (Black Luxury VIP)",
        "intencao": "Fundo preto ônix integral (#141815) com a Logo e detalhes 100% em Ouro Puro Metálico.",
        "topo_grad_start": "#1C221D",
        "topo_grad_end": "#0D100E",
        "logo_b64": b64_logo4,
        "nfc_simbolo": "#D4AF37",
        "nfc_pilula": "#D4AF37",
        "nfc_pilula_texto": "#0D100E",
        "fundo_base": "#0D100E",
        "is_full_dark": True,
        "cor_marca": "#D4AF37",
        "texto_itens": "#FFFFFF",
        "texto_sub": "#D4AF37",
        "icone_bg": "#D4AF37",
        "filete": "rgba(212, 175, 55, 0.35)",
        "site": "costao.com.br"
    }
]

def gerar_svg_tema(cfg):
    v_id = cfg["id"]
    is_dark = cfg.get("is_full_dark", False)
    
    if is_dark:
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="url(#gradTopo_{v_id})"/>
        <!-- Moldura sutil interna dourada -->
        <rect x="50" y="50" width="900" height="900" rx="45" fill="none" stroke="rgba(212,175,55,0.25)" stroke-width="1.5"/>
        <rect x="70" y="520" width="860" height="320" rx="24" fill="rgba(255,255,255,0.02)" stroke="rgba(212,175,55,0.15)" stroke-width="1"/>
        '''
        icone_opacity = "0.18"
        icone_stroke = "#D4AF37"
        chamada_color = "#D4AF37"
        texto_aproxime = "#FFFFFF"
    else:
        # Curva suave: bordas Y=530, centro Y=480
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>
        <path d="M 0,0 L 1000,0 L 1000,530 Q 500,430 0,530 Z" fill="url(#gradTopo_{v_id})"/>
        '''
        icone_opacity = "0.12"
        icone_stroke = cfg["icone_bg"]
        chamada_color = cfg["texto_sub"]
        texto_aproxime = "#FFFFFF" if v_id != "3_ouro_areia_dourada" else "#165B33"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="gradTopo_{v_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cfg['topo_grad_start']}"/>
      <stop offset="100%" stop-color="{cfg['topo_grad_end']}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    {fundo_layer}

    <!-- A) LOGO OFICIAL ADAPTADA AO TEMA (Margem X=90, Y=110) -->
    <g transform="translate(90, 110)">
      <image href="data:image/png;base64,{cfg['logo_b64']}" x="0" y="0" width="370" height="125" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC: SÍMBOLO (220 un) + PÍLULA + FRASE (X=810, Y=90) -->
    <g transform="translate(810, 90)">
      <!-- 1. Símbolo NFC de 22 mm -->
      <g stroke="{cfg['nfc_simbolo']}" stroke-width="6.5" stroke-linecap="round" fill="none" transform="translate(0, 50)">
        <circle cx="-25" cy="0" r="4" fill="{cfg['nfc_simbolo']}" stroke="none"/>
        <path d="M -12 -20 C -2 -10 -2 10 -12 20"/>
        <path d="M 4 -34 C 20 -17 20 17 4 34"/>
        <path d="M 20 -48 C 42 -24 42 24 20 48"/>
      </g>

      <!-- 2. Pílula [ NFC ] -->
      <g transform="translate(0, 132)">
        <rect x="-46" y="-18" width="92" height="36" rx="18" fill="{cfg['nfc_pilula']}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['nfc_pilula_texto']}" text-anchor="middle" letter-spacing="2">NFC</text>
      </g>

      <!-- 3. Frase "Aproxime o celular" -->
      <text x="0" y="190" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="{texto_aproxime}" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: "UM TOQUE LIBERA" -->
    <g transform="translate(90, 560)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{chamada_color}" letter-spacing="3.5">UM TOQUE LIBERA</text>
    </g>

    <!-- D) GRADE 2x2: RÓTULOS DE UMA PALAVRA (Wi-Fi, SPA, Cardápio, Horários) -->
    
    <!-- Item 1: Wi-Fi -->
    <g transform="translate(90, 600)">
      <circle cx="40" cy="40" r="40" fill="{icone_stroke}" fill-opacity="{icone_opacity}"/>
      <g stroke="{icone_stroke}" stroke-width="3.5" stroke-linecap="round" fill="none" transform="translate(24, 24)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="{icone_stroke}" stroke="none"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Wi-Fi</text>
    </g>

    <!-- Item 2: SPA -->
    <g transform="translate(540, 600)">
      <circle cx="40" cy="40" r="40" fill="{icone_stroke}" fill-opacity="{icone_opacity}"/>
      <g stroke="{icone_stroke}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">SPA</text>
    </g>

    <!-- Item 3: Cardápio -->
    <g transform="translate(90, 725)">
      <circle cx="40" cy="40" r="40" fill="{icone_stroke}" fill-opacity="{icone_opacity}"/>
      <g stroke="{icone_stroke}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Cardápio</text>
    </g>

    <!-- Item 4: Horários -->
    <g transform="translate(540, 725)">
      <circle cx="40" cy="40" r="40" fill="{icone_stroke}" fill-opacity="{icone_opacity}"/>
      <g stroke="{icone_stroke}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="{icone_stroke}"/>
        <circle cx="16" cy="19" r="1.5" fill="{icone_stroke}"/>
        <circle cx="22" cy="19" r="1.5" fill="{icone_stroke}"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Horários</text>
    </g>

    <!-- E) RODAPÉ: FILETE E TEXTOS (Margem X=90) -->
    <g transform="translate(90, 875)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="{cfg['filete']}" stroke-width="2.5"/>
      <text x="0" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{cfg['texto_sub']}">Mais tempo para o que importa.</text>
      <text x="820" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['cor_marca']}" text-anchor="end">{cfg['site']}</text>
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
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 100))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in TEMAS:
        svg_content = gerar_svg_tema(cfg)
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

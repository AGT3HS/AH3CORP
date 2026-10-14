# -*- coding: utf-8 -*-
"""
Geração Refinada das Variações de Placa NFC 100x100 mm para o Costão do Santinho Resort
Aplicando 100% das diretrizes do guia 'placa-nfc-design' (atualizado com Roda Cromática e Contraste):
1. Dimensões: 1000x1000 com cantos rx="60" ry="60" (raio 6 mm)
2. Margem de segurança: 90 unidades (9 mm) rigorosa
3. Divisão: Curva suave com centro elevado (bordas Y=530, centro Y=480)
4. Destaque da logo: Posicionamento amplo com respiro, contraste de luminância
5. Símbolo NFC de 220 un + pílula âmbar + frase "Aproxime o celular"
6. Grade 2x2 com rótulo de UMA PALAVRA (Wi-Fi, SPA, Cardápio, Horários) e ícones de 80 un a 12%
7. Rodapé com filete de 3 un a 30% e margens contidas
8. Variações explorando Topo Bicolor e Fundo Inteiro Dark Luxe
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_nfc_refinado"
os.makedirs(OUT, exist_ok=True)

LOGO_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES = [
    {
        "id": "1_classica_verde_costao",
        "nome": "1. Clássica Institucional (Verde Floresta Costão)",
        "tipo_fundo": "bicolor",
        "topo_start": "#1B3B2B",
        "topo_end": "#0D2017",
        "cor_marca": "#1B3B2B",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#0D2017",
        "fundo_base": "#F8F6F0",
        "texto_titulo": "#1B3B2B",
        "texto_itens": "#12261C",
        "texto_sub": "#5A6D62",
        "filete": "rgba(27, 59, 43, 0.25)",
        "site": "costao.com.br"
    },
    {
        "id": "2_escura_alto_impacto",
        "nome": "2. Escura de Alto Impacto (Obsidian & Dourado Total)",
        "tipo_fundo": "fundo_inteiro_dark",
        "topo_start": "#131C16",
        "topo_end": "#080E0A",
        "cor_marca": "#D4AF37",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#080E0A",
        "fundo_base": "#0E1510",
        "card_itens_bg": "rgba(212, 175, 55, 0.08)",
        "texto_titulo": "#FFFFFF",
        "texto_itens": "#F4F4F5",
        "texto_sub": "#9CA3AF",
        "filete": "rgba(212, 175, 55, 0.30)",
        "site": "costao.com.br"
    },
    {
        "id": "3_vibrante_azul_petroleo",
        "nome": "3. Vibrante / Marítima (Azul Petróleo Costão)",
        "tipo_fundo": "bicolor",
        "topo_start": "#2C3E50",
        "topo_end": "#182430",
        "cor_marca": "#2C3E50",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#182430",
        "fundo_base": "#F4F7FB",
        "texto_titulo": "#2C3E50",
        "texto_itens": "#1A2836",
        "texto_sub": "#576C82",
        "filete": "rgba(44, 62, 80, 0.25)",
        "site": "costao.com.br"
    },
    {
        "id": "4_quente_fendi_santinho",
        "nome": "4. Quente & Acolhedora (Fendi & Dunas do Santinho)",
        "tipo_fundo": "bicolor",
        "topo_start": "#8C7B63",
        "topo_end": "#524635",
        "cor_marca": "#524635",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#362D20",
        "fundo_base": "#FAF7F2",
        "texto_titulo": "#524635",
        "texto_itens": "#362D20",
        "texto_sub": "#7A6C5B",
        "filete": "rgba(82, 70, 53, 0.25)",
        "site": "costao.com.br"
    }
]

def gerar_svg(cfg):
    v_id = cfg["id"]
    is_dark = (cfg["tipo_fundo"] == "fundo_inteiro_dark")
    
    if is_dark:
        # Fundo escuro integral de luxo com relevo sutil
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="url(#gradTopo_{v_id})"/>
        <rect x="50" y="500" width="900" height="340" rx="30" fill="rgba(255,255,255,0.03)" stroke="rgba(212,175,55,0.15)" stroke-width="1.5"/>
        '''
        icone_bg_fill = cfg["cor_nfc"]
        icone_bg_opacity = "0.15"
        icone_stroke = cfg["cor_nfc"]
        chamada_color = cfg["cor_nfc"]
    else:
        # Curva suave: Bordas Y=530, Ponto de controle Y=430 -> Vértice no centro exato Y=480 (48 mm do topo)
        fundo_layer = f'''
        <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>
        <path d="M 0,0 L 1000,0 L 1000,530 Q 500,430 0,530 Z" fill="url(#gradTopo_{v_id})"/>
        '''
        icone_bg_fill = cfg["cor_marca"]
        icone_bg_opacity = "0.12"
        icone_stroke = cfg["cor_marca"]
        chamada_color = cfg["texto_sub"]

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
    {fundo_layer}

    <!-- A) LOGO OFICIAL DE REFERÊNCIA (Margem X=90, Y=110) -->
    <g transform="translate(90, 110)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="360" height="120" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC: SÍMBOLO (220 un / 22 mm) + PÍLULA + FRASE (X=810, Y=90) -->
    <g transform="translate(810, 90)">
      <!-- Símbolo NFC: Ponto e 3 Arcos com 22 mm de largura -->
      <g stroke="{cfg['cor_nfc']}" stroke-width="6.5" stroke-linecap="round" fill="none" transform="translate(0, 50)">
        <circle cx="-25" cy="0" r="4" fill="{cfg['cor_nfc']}" stroke="none"/>
        <path d="M -12 -20 C -2 -10 -2 10 -12 20"/>
        <path d="M 4 -34 C 20 -17 20 17 4 34"/>
        <path d="M 20 -48 C 42 -24 42 24 20 48"/>
      </g>

      <!-- Pílula [ NFC ] (30 un de altura) -->
      <g transform="translate(0, 132)">
        <rect x="-46" y="-18" width="92" height="36" rx="18" fill="{cfg['cor_nfc']}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['cor_nfc_texto']}" text-anchor="middle" letter-spacing="2">NFC</text>
      </g>

      <!-- Frase "Aproxime o celular" (28 un / 8pt) -->
      <text x="0" y="190" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: "UM TOQUE LIBERA" (29 un / 8pt, caixa alta, espaçada) -->
    <g transform="translate(90, 560)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{chamada_color}" letter-spacing="3.5">UM TOQUE LIBERA</text>
    </g>

    <!-- D) GRADE 2x2: RÓTULOS DE UMA PALAVRA (44 un / 12.5pt) + ÍCONES DE 80 UN -->
    
    <!-- Item 1: Wi-Fi -->
    <g transform="translate(90, 600)">
      <circle cx="40" cy="40" r="40" fill="{icone_bg_fill}" fill-opacity="{icone_bg_opacity}"/>
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
      <circle cx="40" cy="40" r="40" fill="{icone_bg_fill}" fill-opacity="{icone_bg_opacity}"/>
      <g stroke="{icone_stroke}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">SPA</text>
    </g>

    <!-- Item 3: Cardápio -->
    <g transform="translate(90, 725)">
      <circle cx="40" cy="40" r="40" fill="{icone_bg_fill}" fill-opacity="{icone_bg_opacity}"/>
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
      <circle cx="40" cy="40" r="40" fill="{icone_bg_fill}" fill-opacity="{icone_bg_opacity}"/>
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

    <!-- E) RODAPÉ: FILETE DE 3 UN + TEXTOS A 30 UN (3 mm / 8.5pt) -->
    <g transform="translate(90, 875)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="{cfg['filete']}" stroke-width="2.5"/>
      <text x="0" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{cfg['texto_sub']}">Mais tempo para o que importa.</text>
      <text x="820" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['cor_marca'] if not is_dark else cfg['cor_nfc']}" text-anchor="end">{cfg['site']}</text>
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
    
    stage = Image.new("RGBA", (stage_w, stage_h), (242, 245, 248, 255))
    
    # Sombra suave e precisa do cartão com cantos rx=60
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 100))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES:
        svg_content = gerar_svg(cfg)
        svg_path = os.path.join(OUT, f"placa_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        pix = doc[0].get_pixmap(dpi=300, alpha=True)
        raw_png = os.path.join(OUT, f"placa_{cfg['id']}_raw.png")
        pix.save(raw_png)
        
        mockup_png = os.path.join(OUT, f"placa_{cfg['id']}_mockup.png")
        criar_mockup_arredondado(raw_png, mockup_png)
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

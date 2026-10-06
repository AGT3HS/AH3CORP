# -*- coding: utf-8 -*-
"""
Geração de 4 Novas Versões Vibrantes e Iluminadas para o Costão do Santinho Resort
Inspiradas no sucesso da estética 'Azul Royal Náutico Vivo (#1E6091)':
- Cores saturadas, ricas, nobres e vivas (sem escurecer para tons opacos/pretos).
- Contraste de luz perfeito com a logo oficial original intacta.
- Símbolo NFC e pílula em destaque vibrante e complementar.
- Base clara impecável, ícones nítidos e cantos arredondados rx="60" (6 mm).

4 Temas:
1. Verde Esmeralda Santinho (#1E6B48) - Mata Atlântica & Natureza Viva
2. Azul Royal Santinho (#1E6091) - Mar Iluminado da Praia do Santinho
3. Dourado Solar Imperial (#C89626) - Pôr do Sol & Exclusividade
4. Terracota & Dunas Rupestres (#A65236) - Arqueologia & Charme Natural
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_4_versoes_costao_vibrantes"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VERSOES = [
    {
        "id": "1_verde_esmeralda_santinho",
        "nome": "Variação 1 — Verde Esmeralda Santinho · Mata Atlântica Viva (#1E6B48)",
        "conceito": "Verde esmeralda nobre, rico e iluminado, homenageando a reserva natural do Costão.",
        "cor_topo": "#1E6B48",
        "cor_principal": "#1E6B48",
        "cor_nfc": "#F1C40F",
        "cor_nfc_texto": "#0F422A",
        "texto_aproxime": "#FFFFFF",
        "fundo_base": "#F4FAF6",
        "texto_itens": "#0F422A",
        "texto_sub": "#417359",
        "filete": "rgba(30, 107, 72, 0.22)",
        "site": "costao.com.br"
    },
    {
        "id": "2_azul_royal_santinho",
        "nome": "Variação 2 — Azul Royal Santinho · Mar Iluminado (#1E6091)",
        "conceito": "O mesmo azul náutico vibrante e elegante que destaca o mar aberto da Praia do Santinho.",
        "cor_topo": "#1E6091",
        "cor_principal": "#1E6091",
        "cor_nfc": "#FFA726",
        "cor_nfc_texto": "#103957",
        "texto_aproxime": "#FFFFFF",
        "fundo_base": "#F3F8FC",
        "texto_itens": "#103957",
        "texto_sub": "#467091",
        "filete": "rgba(30, 96, 145, 0.22)",
        "site": "costao.com.br"
    },
    {
        "id": "3_dourado_solar_imperial",
        "nome": "Variação 3 — Dourado Solar Imperial · Pôr do Sol no Morro (#C89626)",
        "conceito": "Dourado âmbar luminoso e caloroso, transmitindo requinte e hospitalidade de alto padrão.",
        "cor_topo": "#C89626",
        "cor_principal": "#C89626",
        "cor_nfc": "#1B5E38",
        "cor_nfc_texto": "#FFFFFF",
        "texto_aproxime": "#FFFFFF",
        "fundo_base": "#FCFAF4",
        "texto_itens": "#1B5E38",
        "texto_sub": "#78622E",
        "filete": "rgba(200, 150, 38, 0.28)",
        "site": "costao.com.br"
    },
    {
        "id": "4_terracota_dunas_rupestres",
        "nome": "Variação 4 — Terracota & Dunas · Arte Rupestre (#A65236)",
        "conceito": "Tom terracota sofisticado e acolhedor, inspirado nas inscrições rupestres e dunas do resort.",
        "cor_topo": "#A65236",
        "cor_principal": "#A65236",
        "cor_nfc": "#F1C40F",
        "cor_nfc_texto": "#5C2614",
        "texto_aproxime": "#FFFFFF",
        "fundo_base": "#FAF5F2",
        "texto_itens": "#5C2614",
        "texto_sub": "#805141",
        "filete": "rgba(166, 82, 54, 0.25)",
        "site": "costao.com.br"
    }
]

def gerar_svg_vibrante(cfg):
    v_id = cfg["id"]
    cor_topo = cfg["cor_topo"]
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Base Clara Inferior Texturizada -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>

    <!-- Divisão Superior com a Cor Viva e Iluminada -->
    <path d="M 0,0 L 1000,0 L 1000,530 Q 500,430 0,530 Z" fill="{cor_topo}"/>

    <!-- A) LOGO ORIGINAL OFICIAL DO COSTÃO (Margem X=90, Y=110) -->
    <g transform="translate(90, 110)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="370" height="125" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC: SÍMBOLO DE 220 UN (22 mm) + PÍLULA + FRASE (X=810, Y=90) -->
    <g transform="translate(810, 90)">
      <!-- 1. Símbolo NFC em Destaque Vibrante -->
      <g stroke="{cfg['cor_nfc']}" stroke-width="6.5" stroke-linecap="round" fill="none" transform="translate(0, 50)">
        <circle cx="-25" cy="0" r="4" fill="{cfg['cor_nfc']}" stroke="none"/>
        <path d="M -12 -20 C -2 -10 -2 10 -12 20"/>
        <path d="M 4 -34 C 20 -17 20 17 4 34"/>
        <path d="M 20 -48 C 42 -24 42 24 20 48"/>
      </g>

      <!-- 2. Pílula [ NFC ] -->
      <g transform="translate(0, 132)">
        <rect x="-46" y="-18" width="92" height="36" rx="18" fill="{cfg['cor_nfc']}"/>
        <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['cor_nfc_texto']}" text-anchor="middle" letter-spacing="2">NFC</text>
      </g>

      <!-- 3. Frase "Aproxime o celular" -->
      <text x="0" y="190" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="{cfg['texto_aproxime']}" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: "UM TOQUE LIBERA" -->
    <g transform="translate(90, 560)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{cfg['texto_sub']}" letter-spacing="3.5">UM TOQUE LIBERA</text>
    </g>

    <!-- D) GRADE 2x2: RÓTULOS DE UMA PALAVRA (Wi-Fi, SPA, Cardápio, Horários) -->
    
    <!-- Item 1: Wi-Fi -->
    <g transform="translate(90, 600)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" fill="none" transform="translate(24, 24)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="{cfg['cor_principal']}" stroke="none"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Wi-Fi</text>
    </g>

    <!-- Item 2: SPA -->
    <g transform="translate(540, 600)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">SPA</text>
    </g>

    <!-- Item 3: Cardápio -->
    <g transform="translate(90, 725)">
      <circle cx="40" cy="40" r="40" fill="{cfg['cor_principal']}" fill-opacity="0.12"/>
      <g stroke="{cfg['cor_principal']}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Cardápio</text>
    </g>

    <!-- Item 4: Horários -->
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
      <text x="100" y="48" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="700" fill="{cfg['texto_itens']}">Horários</text>
    </g>

    <!-- E) RODAPÉ COM FILETE (Margem X=90) -->
    <g transform="translate(90, 875)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="{cfg['filete']}" stroke-width="2.5"/>
      <text x="0" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{cfg['texto_sub']}">Mais tempo para o que importa.</text>
      <text x="820" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['cor_principal']}" text-anchor="end">{cfg['site']}</text>
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
    for cfg in VERSOES:
        svg_content = gerar_svg_vibrante(cfg)
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

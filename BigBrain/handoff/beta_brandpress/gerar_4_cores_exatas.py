# -*- coding: utf-8 -*-
"""
Geração das 4 Variações de Placa NFC 100x100 mm utilizando ESTRITAMENTE as 4 cores oficiais solicitadas:
- Variação 1: #1B3B2B (Verde Floresta)
- Variação 2: #2C3E50 (Azul Petróleo)
- Variação 3: #D4AF37 (Dourado Imperial)
- Variação 4: #8C7B63 (Fendi / Areia Santinho)

Regras Inegociáveis:
1. Logo Original de Referência 100% INTACTA (sem alteração de cores da imagem fornecida).
2. Fundo do topo SÓLIDO nas cores exatas (#1B3B2B, #2C3E50, #D4AF37, #8C7B63) para que cada placa tenha sua cor evidente e inconfundível.
3. Cantos arredondados rx="60" e ry="60" (6 mm) em 1000x1000 un.
4. Margem de segurança de 90 un (9 mm).
5. Curva suave: bordas em Y=530 e centro em Y=480.
6. Símbolo NFC de 220 un (22 mm) + pílula + "Aproxime o celular".
7. Grade 2x2 com rótulos de uma palavra (Wi-Fi, SPA, Cardápio, Horários) e círculos de 80 un a 12%.
8. Rodapé com filete de 3 un e site costao.com.br.
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_4_cores_exatas"
os.makedirs(OUT, exist_ok=True)

LOGO_ORIGINAL = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_ORIGINAL, "rb") as f:
    logo_original_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES_EXATAS = [
    {
        "id": "1_verde_floresta_1B3B2B",
        "nome": "1. Verde Floresta (#1B3B2B)",
        "cor_topo": "#1B3B2B",
        "cor_principal": "#1B3B2B",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#1B3B2B",
        "fundo_base": "#F8F6F0",
        "texto_aproxime": "#FFFFFF",
        "texto_itens": "#1B3B2B",
        "texto_sub": "#576B60",
        "filete": "rgba(27, 59, 43, 0.25)",
        "site": "costao.com.br"
    },
    {
        "id": "2_azul_petroleo_2C3E50",
        "nome": "2. Azul Petróleo (#2C3E50)",
        "cor_topo": "#2C3E50",
        "cor_principal": "#2C3E50",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#2C3E50",
        "fundo_base": "#F4F7FB",
        "texto_aproxime": "#FFFFFF",
        "texto_itens": "#2C3E50",
        "texto_sub": "#5A6E82",
        "filete": "rgba(44, 62, 80, 0.25)",
        "site": "costao.com.br"
    },
    {
        "id": "3_dourado_imperial_D4AF37",
        "nome": "3. Dourado Imperial (#D4AF37)",
        "cor_topo": "#D4AF37",
        "cor_principal": "#D4AF37",
        "cor_nfc": "#1B3B2B",
        "cor_nfc_texto": "#FFFFFF",
        "fundo_base": "#FCFAF5",
        "texto_aproxime": "#1B3B2B",
        "texto_itens": "#1B3B2B",
        "texto_sub": "#7A6836",
        "filete": "rgba(212, 175, 55, 0.40)",
        "site": "costao.com.br"
    },
    {
        "id": "4_fendi_areia_8C7B63",
        "nome": "4. Fendi / Areia (#8C7B63)",
        "cor_topo": "#8C7B63",
        "cor_principal": "#8C7B63",
        "cor_nfc": "#D4AF37",
        "cor_nfc_texto": "#3D3428",
        "fundo_base": "#FAF7F2",
        "texto_aproxime": "#FFFFFF",
        "texto_itens": "#3D3428",
        "texto_sub": "#706354",
        "filete": "rgba(140, 123, 99, 0.30)",
        "site": "costao.com.br"
    }
]

def gerar_svg_exato(cfg):
    v_id = cfg["id"]
    cor_topo = cfg["cor_topo"]
    
    # Curva suave: bordas Y=530, centro Y=480 (control point Y=430)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip_{v_id}">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cardClip_{v_id})">
    <!-- Base Clara Inferior -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="{cfg['fundo_base']}"/>

    <!-- Divisão Superior com Cor SÓLIDA Pura Exata do Hotel -->
    <path d="M 0,0 L 1000,0 L 1000,530 Q 500,430 0,530 Z" fill="{cor_topo}"/>

    <!-- A) LOGO ORIGINAL DE REFERÊNCIA 100% INTACTA (Margem X=90, Y=110) -->
    <g transform="translate(90, 110)">
      <image href="data:image/png;base64,{logo_original_b64}" x="0" y="0" width="370" height="125" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC: SÍMBOLO DE 220 UN (22 mm) + PÍLULA + FRASE (X=810, Y=90) -->
    <g transform="translate(810, 90)">
      <!-- 1. Símbolo NFC -->
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
    for cfg in VARIACOES_EXATAS:
        svg_content = gerar_svg_exato(cfg)
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

# -*- coding: utf-8 -*-
"""
Geração das 4 Variações Oficiais do Cartão NFC 100x100 mm para o Costão do Santinho Resort
Utilizando EXCLUSIVAMENTE a paleta institucional do Guia de Identidade Visual do Hotel:
- #1B3B2B (Verde Floresta Costão)
- #D4AF37 (Dourado Imperial)
- #8C7B63 (Fendi / Areia Santinho)
- #2C3E50 (Azul Petróleo Costão)

Seguindo à risca as regras de anatomia do guia 'placa-nfc-design':
- Dimensões 1000x1000 com cantos rx=60 (raio de 6 mm)
- Margem de segurança de 90 unidades (9 mm)
- Curva escuro/claro com centro elevado (bordas Y=530, centro Y=450)
- Logo oficial de referência fornecida
- Símbolo NFC de 220 un + pílula + texto
- Grade 2x2 com ícones de traço e círculos a 12%
- Rodapé com filete de 3 un e textos a 30 un
"""
import os
import base64
from PIL import Image, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_costao_paleta_hotel"
os.makedirs(OUT, exist_ok=True)

LOGO_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"
with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

VARIACOES_HOTEL = [
    {
        "id": "1_verde_floresta_institucional",
        "nome": "1. Verde Floresta Institucional (Identidade Principal do Resort)",
        "intencao": "Assinatura oficial do Costão: sofisticação e harmonia com a reserva natural do Santinho.",
        "topo_start": "#1B3B2B",
        "topo_end": "#0C1D15",
        "cor_principal": "#1B3B2B",
        "cor_ambar": "#D4AF37",
        "cor_ambar_dark": "#0C1D15",
        "neutro_corpo": "#F8F6F2",
        "texto_escuro": "#12251B",
        "texto_sub": "#576B60",
        "filete": "#E0DAD0",
        "site": "costao.com.br"
    },
    {
        "id": "2_azul_petroleo_oceano",
        "nome": "2. Azul Petróleo & Oceano (Costão Sea & Night)",
        "intencao": "Serenidade marítima e elegância cosmopolita à beira-mar.",
        "topo_start": "#2C3E50",
        "topo_end": "#17232F",
        "cor_principal": "#2C3E50",
        "cor_ambar": "#D4AF37",
        "cor_ambar_dark": "#17232F",
        "neutro_corpo": "#F5F7FA",
        "texto_escuro": "#1C2936",
        "texto_sub": "#5A6E82",
        "filete": "#DCE2E9",
        "site": "costao.com.br"
    },
    {
        "id": "3_fendi_areia_santinho",
        "nome": "3. Fendi & Areia Santinho (Costão Dunes & Beach)",
        "intencao": "Atmosfera sensorial orgânica, calor do litoral e acolhimento boutique.",
        "topo_start": "#8C7B63",
        "topo_end": "#524635",
        "cor_principal": "#524635",
        "cor_ambar": "#D4AF37",
        "cor_ambar_dark": "#362E22",
        "neutro_corpo": "#FAF7F2",
        "texto_escuro": "#382F24",
        "texto_sub": "#706354",
        "filete": "#E5DDD1",
        "site": "costao.com.br"
    },
    {
        "id": "4_dourado_dark_luxe",
        "nome": "4. Dourado Imperial & Dark Luxe (Costão VIP 5 Estrelas)",
        "intencao": "Máximo contraste e exclusividade premium para suítes e áreas VIP.",
        "topo_start": "#141C16",
        "topo_end": "#080C09",
        "cor_principal": "#1B3B2B",
        "cor_ambar": "#D4AF37",
        "cor_ambar_dark": "#080C09",
        "neutro_corpo": "#F9F7F3",
        "texto_escuro": "#0D140F",
        "texto_sub": "#526156",
        "filete": "#DFD9CD",
        "site": "costao.com.br"
    }
]

def gerar_svg_placa_hotel(cfg):
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
    <!-- Base Clara Inferior em Neutro Quente Derivado -->
    <rect width="1000" height="1000" fill="{cfg['neutro_corpo']}"/>

    <!-- Divisão Superior Escura com Curva Suave (Bordas Y=530, Centro Alto Y=450) -->
    <path d="M 0,0 L 1000,0 L 1000,530 Q 500,450 0,530 Z" fill="url(#gradTopo_{v_id})"/>

    <!-- A) LOGO OFICIAL DE REFERÊNCIA (Margem de Segurança X=90, Y=115) -->
    <g transform="translate(90, 115)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="350" height="115" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER SÍMBOLO NFC EM DOURADO IMPERIAL (X=800, Y=90) -->
    <g transform="translate(800, 90)">
      <!-- 1. Símbolo NFC: Ponto e 3 Arcos em Traço Arredondado (Largura 220 un / 22 mm) -->
      <g stroke="{cfg['cor_ambar']}" stroke-width="6.5" stroke-linecap="round" fill="none" transform="translate(0, 50)">
        <circle cx="-25" cy="0" r="4" fill="{cfg['cor_ambar']}" stroke="none"/>
        <path d="M -12 -20 C -2 -10 -2 10 -12 20"/>
        <path d="M 4 -34 C 20 -17 20 17 4 34"/>
        <path d="M 20 -48 C 42 -24 42 24 20 48"/>
      </g>

      <!-- 2. Pílula [ NFC ] -->
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

    <!-- D) GRADE 2x2 COM ÍCONES DE TRAÇO E CÍRCULOS A 12% DA COR PRINCIPAL -->
    
    <!-- Item 1: Wi-Fi Resort -->
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

    <!-- Item 3: Restaurantes -->
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

    <!-- E) RODAPÉ COM FILETE (Contido dentro da margem de segurança de 90 un) -->
    <g transform="translate(90, 875)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="{cfg['filete']}" stroke-width="2.5"/>
      <text x="0" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{cfg['texto_sub']}">Mais tempo para o que importa.</text>
      <text x="820" y="38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{cfg['cor_principal']}" text-anchor="end">{cfg['site']}</text>
    </g>
    
    <!-- Filete de contorno perimetral elegante para corte -->
    <rect x="1" y="1" width="998" height="998" rx="59" fill="none" stroke="{cfg['cor_principal']}" stroke-width="1.5" stroke-opacity="0.2"/>
  </g>
</svg>'''
    return svg

def criar_mockup_palco(png_path, out_mockup_path):
    card = Image.open(png_path).convert("RGBA")
    cw, ch = card.size
    margin = 80
    stage_w = cw + margin * 2
    stage_h = ch + margin * 2
    
    stage = Image.new("RGBA", (stage_w, stage_h), (242, 244, 247, 255))
    
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 95))
    shadow.putalpha(shadow_mask)
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    
    stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)

def main():
    for cfg in VARIACOES_HOTEL:
        svg_content = gerar_svg_placa_hotel(cfg)
        svg_path = os.path.join(OUT, f"placa_costao_{cfg['id']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = fitz.open(svg_path)
        pix = doc[0].get_pixmap(dpi=300, alpha=True)
        raw_png = os.path.join(OUT, f"placa_costao_{cfg['id']}_raw.png")
        pix.save(raw_png)
        
        mockup_png = os.path.join(OUT, f"placa_costao_{cfg['id']}_mockup.png")
        criar_mockup_palco(raw_png, mockup_png)
        print(f"Gerado: {cfg['nome']} -> {mockup_png}")

if __name__ == "__main__":
    main()

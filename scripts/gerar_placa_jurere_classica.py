import os
import base64
import pymupdf
from PIL import Image, ImageFilter

out_dir = 'saida/proposta_jurere'
os.makedirs(out_dir, exist_ok=True)

logo_path = 'guias_identidade_visual/logos/02_jurer_beach_village/02_jurer_beach_village_logo_1.png'
with open(logo_path, 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')

# Placa 01_modelo_classico_cor_mae
# Formato 1000x1000, rx=60 ry=60
# Curva Canônica: M0,0 H1000 V530 Q500,480 0,530 Z
# Cores Jurerê Beach Village:
# Cor-mãe Topo: #4DA2AD (Turquesa Oceânico Nobre) -> degradê para #2D7580
# Fundo Base: #FAF8F5 (Areia Nobre)
# Ponto Focal NFC: #E8A825 (Âmbar Solar de Ativação)
# Textos & Ícones: #12181A (Obsidian Petróleo) / #5A6577

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="card-shape">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="topGrad_jurere" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4DA2AD"/>
      <stop offset="1" stop-color="#276B75"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#card-shape)">
    <!-- Base Areia Nobre (60%) -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="#FAF8F5"/>

    <!-- Topo Cor-Mãe Jurerê Beach Village com Curva Canônica (30%) -->
    <path d="M0,0 H1000 V530 Q500,480 0,530 Z" fill="url(#topGrad_jurere)"/>

    <!-- ZONA A: LOGO E MARCA JURERÊ BEACH VILLAGE (X: 90 a 670, Y: 90 a 460) -->
    <g transform="translate(90, 110)">
      <image x="0" y="0" width="140" height="140" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{logo_b64}"/>
      <g transform="translate(160, 42)">
        <text font-family="'Cinzel', 'Georgia', serif" font-size="42" font-weight="700" fill="#FFFFFF" letter-spacing="2">JURERÊ</text>
        <text font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="800" fill="#FAF8F5" letter-spacing="6" opacity="0.95" y="32">BEACH VILLAGE</text>
        <text font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="500" fill="#FAF8F5" letter-spacing="2" opacity="0.8" y="58">FLORIANÓPOLIS • BRASIL</text>
      </g>
    </g>

    <!-- ZONA B: SENSOR NFC DE 220 UN (X: 700 a 910, Centro X=800) -->
    <!-- Símbolo NFC: Ponto e 3 Arcos Concêntricos em Âmbar/Ouro -->
    <g fill="none" stroke="#E8A825" stroke-width="14" stroke-linecap="round">
      <circle cx="720" cy="180" r="14" fill="#E8A825" stroke="none"/>
      <path d="M 760 125 Q 830 180 760 235"/>
      <path d="M 800 95 Q 880 180 800 265"/>
      <path d="M 840 65 Q 930 180 840 295"/>
    </g>

    <!-- Etiqueta Pílula NFC (Texto 3.0 mm = 30 un, espaçada) -->
    <rect x="710" y="300" width="180" height="46" rx="23" fill="#E8A825"/>
    <text x="800" y="333" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="30" font-weight="800" fill="#12181A" text-anchor="middle" letter-spacing="3">NFC</text>

    <!-- Frase 'Aproxime o celular' (2.8 mm = 28 un) -->
    <text x="800" y="378" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="28" font-weight="500" fill="#FAF8F5" text-anchor="middle">Aproxime o celular</text>

    <!-- ZONA C: CHAMADA 'UM TOQUE LIBERA' (2.9 mm = 29 un, caixa alta, espaçada) -->
    <text x="90" y="615" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="29" font-weight="800" fill="#276B75" letter-spacing="4">UM TOQUE LIBERA</text>

    <!-- ZONA D: GRADE 2x2 DE SERVIÇOS DO HOTEL (4.4 mm = 44 un) & CÍRCULOS DE 80 UN -->
    <!-- Item 1 (Restaurante ZPerry): Círculo (130, 710), Texto (190, 724) -->
    <g>
      <circle cx="130" cy="710" r="40" fill="#276B75" fill-opacity="0.12"/>
      <g stroke="#276B75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(114, 694)">
        <path d="M 5 3 L 5 12 C 5 15 8 17 11 17 L 11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M 17 3 L 17 12 C 17 15 14 17 11 17"/>
        <path d="M 23 3 C 27 8 27 15 24 18 L 24 29"/>
      </g>
      <text x="190" y="724" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="#12181A">Restaurante</text>
    </g>

    <!-- Item 2 (Serviço de Praia): Círculo (580, 710), Texto (640, 724) -->
    <g>
      <circle cx="580" cy="710" r="40" fill="#276B75" fill-opacity="0.12"/>
      <g stroke="#276B75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(564, 694)">
        <path d="M 4 24 C 8 21 12 21 16 24 C 20 27 24 27 28 24"/>
        <path d="M 4 28 C 8 25 12 25 16 28 C 20 31 24 31 28 28"/>
        <circle cx="16" cy="9" r="6"/>
      </g>
      <text x="640" y="724" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="#12181A">Praia &amp; Piscina</text>
    </g>

    <!-- Item 3 (SPA & Relax): Círculo (130, 850), Texto (190, 864) -->
    <g>
      <circle cx="130" cy="850" r="40" fill="#276B75" fill-opacity="0.12"/>
      <g stroke="#276B75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(114, 834)">
        <path d="M 16 26 C 16 12 6 8 2 18 C 2 24 10 26 16 26 Z"/>
        <path d="M 16 26 C 16 12 26 8 30 18 C 30 24 22 26 16 26 Z"/>
        <path d="M 16 26 C 11 16 13 6 16 3 C 19 6 21 16 16 26 Z"/>
      </g>
      <text x="190" y="864" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="#12181A">SPA &amp; Relax</text>
    </g>

    <!-- Item 4 (Wi-Fi & Concierge): Círculo (580, 850), Texto (640, 864) -->
    <g>
      <circle cx="580" cy="850" r="40" fill="#276B75" fill-opacity="0.12"/>
      <g stroke="#276B75" stroke-width="3" stroke-linecap="round" fill="none" transform="translate(564, 834)">
        <path d="M 2 8 C 9 1, 23 1, 30 8"/>
        <path d="M 7 14 C 12 9, 20 9, 25 14"/>
        <path d="M 12 20 C 14 17, 18 17, 20 20"/>
        <circle cx="16" cy="26" r="2" fill="#276B75" stroke="none"/>
      </g>
      <text x="640" y="864" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="44" font-weight="600" fill="#12181A">Wi-Fi &amp; Lazer</text>
    </g>

    <!-- ZONA E: RODAPÉ INSTITUCIONAL (Divisor Y=890 | Endereço & Site Y=930) -->
    <line x1="90" y1="890" x2="910" y2="890" stroke="#276B75" stroke-width="3" opacity="0.2"/>
    <text x="90" y="935" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="26" font-weight="500" fill="#5A6577">Alameda César Nascimento, 646 — Jurerê</text>
    <text x="910" y="935" font-family="'Plus Jakarta Sans', Helvetica, sans-serif" font-size="28" font-weight="700" fill="#276B75" text-anchor="end">jurerebeachvillage.com.br</text>
  </g>
</svg>'''

svg_path = os.path.join(out_dir, '01_modelo_classico_cor_mae_jurere.svg')
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

doc = pymupdf.open(svg_path)
pix = doc[0].get_pixmap(dpi=300, alpha=True)
png_path = os.path.join(out_dir, '01_modelo_classico_cor_mae_jurere.png')
pix.save(png_path)

# Criar Mockup com Sombra Suave Realista
card = Image.open(png_path).convert("RGBA")
cw, ch = card.size
margin = 80
stage_w = cw + margin * 2
stage_h = ch + margin * 2

stage = Image.new("RGBA", (stage_w, stage_h), (242, 245, 248, 255))
shadow_mask = card.split()[-1]
shadow = Image.new("RGBA", (cw, ch), (15, 23, 42, 110))
shadow.putalpha(shadow_mask)
shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=28))

stage.paste(shadow_blurred, (margin + 4, margin + 14), shadow_blurred)
stage.paste(card, (margin, margin), card)

mockup_path = os.path.join(out_dir, '01_modelo_classico_cor_mae_jurere_mockup.png')
stage.convert("RGB").save(mockup_path, "PNG", quality=95)

print('SVG, PNG e Mockup gerados com sucesso:', svg_path, png_path, mockup_path)

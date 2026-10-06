import os
import re
import math
import io
import base64
import subprocess
from PIL import Image

out_dir = r"C:\Users\Augusto\Desktop\AH3\BigBrain\handoff\placas_costao"
attachments_dir = r"C:\Users\Augusto\AppData\Local\hermes\profiles\designer\attachments"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

os.makedirs(out_dir, exist_ok=True)

# 1. Extract embedded fonts from references
font_defs = {}
svg_files = [
    "costao-novo-1-ponte-noturna.svg",
    "costao-novo-2-por-do-sol.svg",
    "costao-novo-3-bruxas-da-ilha.svg",
    "costao-novo-4-ostras-e-sabores.svg",
    "costao-novo-5-trilhas-da-ilha.svg",
    "costao-novo-6-etiqueta-de-bagagem.svg",
    "costao-novo-7-tipografia-gigante.svg",
    "costao-novo-8-guarda-sol.svg"
]

for sf in svg_files:
    path = os.path.join(attachments_dir, sf)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            c = f.read()
        fonts = re.findall(r'(@font-face\{[^}]+\})', c)
        for f_def in fonts:
            m = re.search(r"font-family:'([^']+)'", f_def) or re.search(r'font-family:"([^"]+)"', f_def)
            if m:
                font_name = m.group(1)
                if font_name not in font_defs:
                    font_defs[font_name] = f_def

# 2. Extract and recolor logo
logo_path = os.path.join(out_dir, "logo_costao.png")
if not os.path.exists(logo_path):
    # fallback extract from reference
    with open(os.path.join(attachments_dir, "costao-novo-1-ponte-noturna.svg"), "r", encoding="utf-8") as f:
        ref_c = f.read()
    m_img = re.search(r'href="(data:image/png;base64,[^"]+)"', ref_c)
    if m_img:
        b64_d = m_img.group(1).split(",", 1)[1]
        with open(logo_path, "wb") as f:
            f.write(base64.b64decode(b64_d))

img = Image.open(logo_path)

def recolor_png(img_in, target_rgb):
    img_rgba = img_in.convert("RGBA")
    r, g, b, a = img_rgba.split()
    solid = Image.new("RGBA", img_in.size, (*target_rgb, 255))
    solid.putalpha(a)
    return solid

def to_b64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

b64_gold = to_b64(recolor_png(img, (242, 193, 78)))
b64_navy = to_b64(recolor_png(img, (14, 59, 63)))
b64_sand = to_b64(recolor_png(img, (246, 237, 219)))

# 3. Mathematically perfect Contactless NFC waves generator
def generate_nfc_waves(cx, cy, radii=[10, 18, 26, 34], stroke="#F2C14E", stroke_width=3.2, direction="right"):
    paths = []
    cos45 = math.cos(math.pi / 4)
    sin45 = math.sin(math.pi / 4)
    for r in radii:
        if direction == "right":
            x_start = cx + r * cos45
            y_start = cy - r * sin45
            x_end = cx + r * cos45
            y_end = cy + r * sin45
            sweep = 1
            d = f"M {x_start:.1f},{y_start:.1f} A {r},{r} 0 0,{sweep} {x_end:.1f},{y_end:.1f}"
        paths.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"/>')
    return "\n      ".join(paths)

# 4. Generate the 4 Master SVGs
font_cormorant_jost = font_defs.get('Cormorant Garamond', '') + "\n" + font_defs.get('Jost', '')
font_bodoni_hanken = font_defs.get('Bodoni Moda', '') + "\n" + font_defs.get('Hanken Grotesk', '')
font_outfit = font_defs.get('Outfit', '')
font_space_barlow = font_defs.get('Space Mono', '') + "\n" + font_defs.get('Barlow Condensed', '')

# DESIGN 1: PONTE NOTURNA
nfc_waves_d1 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#F2C14E", stroke_width=3.2, direction="right")
svg1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_cormorant_jost}
      .font-title {{ font-family: 'Cormorant Garamond', Georgia, serif; }}
      .font-body {{ font-family: 'Jost', -apple-system, BlinkMacSystemFont, sans-serif; }}
    </style>
    <clipPath id="cc1"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#040C20"/>
      <stop offset="0.55" stop-color="#0B2147"/>
      <stop offset="1" stop-color="#183B68"/>
    </linearGradient>
    <radialGradient id="moon1" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFFDF5"/>
      <stop offset="0.6" stop-color="#FCEAB3"/>
      <stop offset="1" stop-color="#E5BE64"/>
    </radialGradient>
    <filter id="moon-glow1" x="-40%" y="-40%" width="1.8" height="1.8">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <g clip-path="url(#cc1)">
    <rect width="1000" height="1000" fill="url(#sky1)"/>

    <circle cx="120" cy="80" r="1.5" fill="#FFF1CF" opacity="0.8"/>
    <circle cx="280" cy="50" r="1.2" fill="#FFF1CF" opacity="0.6"/>
    <circle cx="340" cy="110" r="1.8" fill="#FFF1CF" opacity="0.9"/>
    <circle cx="520" cy="70" r="1.2" fill="#FFF1CF" opacity="0.7"/>
    <circle cx="680" cy="55" r="2.0" fill="#FFF1CF" opacity="0.85"/>
    <circle cx="890" cy="65" r="1.5" fill="#FFF1CF" opacity="0.9"/>
    <circle cx="160" cy="170" r="1.2" fill="#FFF1CF" opacity="0.5"/>
    <circle cx="240" cy="220" r="1.6" fill="#FFF1CF" opacity="0.7"/>
    <circle cx="480" cy="190" r="1.2" fill="#FFF1CF" opacity="0.6"/>
    <circle cx="620" cy="230" r="1.5" fill="#FFF1CF" opacity="0.8"/>
    <circle cx="710" cy="160" r="1.8" fill="#FFF1CF" opacity="0.75"/>
    <circle cx="940" cy="210" r="1.4" fill="#FFF1CF" opacity="0.85"/>

    <path d="M-10,380 L250,210 Q500,450 750,210 L1010,380" stroke="#F2C14E" stroke-width="5" fill="none" stroke-linejoin="round" opacity="0.85"/>
    <path d="M-10,395 L250,225 Q500,465 750,225 L1010,395" stroke="#F2C14E" stroke-width="2" fill="none" stroke-linejoin="round" opacity="0.5"/>

    <g stroke="#F2C14E" stroke-width="2" opacity="0.7" fill="none">
      <line x1="240" y1="200" x2="230" y2="480"/>
      <line x1="260" y1="200" x2="270" y2="480"/>
      <line x1="235" y1="260" x2="265" y2="260"/>
      <line x1="233" y1="330" x2="267" y2="330"/>
      <line x1="230" y1="400" x2="270" y2="400"/>
      <line x1="235" y1="260" x2="267" y2="330"/>
      <line x1="265" y1="260" x2="233" y2="330"/>
      <line x1="233" y1="330" x2="270" y2="400"/>
      <line x1="267" y1="330" x2="230" y2="400"/>

      <line x1="740" y1="200" x2="730" y2="480"/>
      <line x1="760" y1="200" x2="770" y2="480"/>
      <line x1="735" y1="260" x2="765" y2="260"/>
      <line x1="733" y1="330" x2="767" y2="330"/>
      <line x1="730" y1="400" x2="770" y2="400"/>
      <line x1="735" y1="260" x2="767" y2="330"/>
      <line x1="765" y1="260" x2="733" y2="330"/>
      <line x1="733" y1="330" x2="770" y2="400"/>
      <line x1="767" y1="330" x2="730" y2="400"/>

      <line x1="330" y1="270" x2="330" y2="480" stroke-width="1" opacity="0.4"/>
      <line x1="410" y1="350" x2="410" y2="480" stroke-width="1" opacity="0.4"/>
      <line x1="500" y1="410" x2="500" y2="480" stroke-width="1.5" opacity="0.6"/>
      <line x1="590" y1="350" x2="590" y2="480" stroke-width="1" opacity="0.4"/>
      <line x1="670" y1="270" x2="670" y2="480" stroke-width="1" opacity="0.4"/>
    </g>

    <line x1="0" y1="480" x2="1000" y2="480" stroke="#F2C14E" stroke-width="3" opacity="0.6"/>
    <rect x="0" y="485" width="1000" height="515" fill="#061226" opacity="0.88"/>

    <image href="{b64_gold}" x="70" y="60" width="360" height="100" preserveAspectRatio="xMinYMid meet"/>

    <g transform="translate(845, 115)">
      <circle cx="0" cy="0" r="54" fill="none" stroke="#F2C14E" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
      <circle cx="0" cy="0" r="46" fill="url(#moon1)" filter="url(#moon-glow1)"/>
      <circle cx="0" cy="0" r="43" fill="#0A1D3D"/>
      <g transform="translate(-4, 0)">
        {nfc_waves_d1}
      </g>
    </g>
    <text class="font-body" x="845" y="192" font-size="15" font-weight="800" fill="#F2C14E" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-body" x="845" y="212" font-size="12" font-weight="600" fill="#FFF1CF" text-anchor="middle" opacity="0.85">Aproxime o celular</text>

    <text class="font-title" x="70" y="215" font-size="36" font-weight="700" fill="#FFF1CF" letter-spacing="0.5">Um toque libera a sua experiência</text>
    <line x1="70" y1="230" x2="380" y2="230" stroke="#F2C14E" stroke-width="2"/>

    <g transform="translate(70, 260)">
      <text class="font-title" x="0" y="32" font-size="28" font-weight="700" fill="#FFF1CF">Costão SPA &amp; Relax</text>
      <text class="font-body" x="0" y="58" font-size="16" font-weight="400" fill="#CBDDF5" opacity="0.85">Massagens exclusivas, hidromassagem aquecida, saunas e rituais de renovação</text>
      <line x1="0" y1="78" x2="860" y2="78" stroke="#F2C14E" stroke-width="1" stroke-opacity="0.2"/>
    </g>

    <g transform="translate(70, 365)">
      <text class="font-title" x="0" y="32" font-size="28" font-weight="700" fill="#FFF1CF">Shows &amp; Programação Diária</text>
      <text class="font-body" x="0" y="58" font-size="16" font-weight="400" fill="#CBDDF5" opacity="0.85">Agenda diária ao vivo, espetáculos teatrais, bandas e recreação infantil completa</text>
      <line x1="0" y1="78" x2="860" y2="78" stroke="#F2C14E" stroke-width="1" stroke-opacity="0.2"/>
    </g>

    <g transform="translate(70, 470)">
      <text class="font-title" x="0" y="32" font-size="28" font-weight="700" fill="#FFF1CF">Restaurantes &amp; Bares All-Inclusive</text>
      <text class="font-body" x="0" y="58" font-size="16" font-weight="400" fill="#CBDDF5" opacity="0.85">Cardápios assinados em tempo real, reservas de alta gastronomia e carta de vinhos</text>
      <line x1="0" y1="78" x2="860" y2="78" stroke="#F2C14E" stroke-width="1" stroke-opacity="0.2"/>
    </g>

    <g transform="translate(70, 575)">
      <text class="font-title" x="0" y="32" font-size="28" font-weight="700" fill="#FFF1CF">Mapa Geral &amp; Guia do Resort</text>
      <text class="font-body" x="0" y="58" font-size="16" font-weight="400" fill="#CBDDF5" opacity="0.85">Navegação GPS pelas vilas, piscinas, Wi-Fi liberado, trilhas ecológicas e arqueologia</text>
      <line x1="0" y1="78" x2="860" y2="78" stroke="#F2C14E" stroke-width="1" stroke-opacity="0.2"/>
    </g>

    <g transform="translate(70, 930)">
      <line x1="0" y1="0" x2="860" y2="0" stroke="#F2C14E" stroke-width="1" stroke-opacity="0.25"/>
      <text class="font-body" x="0" y="32" font-size="14" font-weight="400" fill="#CBDDF5" opacity="0.85">Experiência All-Inclusive na Praia do Santinho • Florianópolis</text>
      <text class="font-body" x="860" y="32" font-size="15" font-weight="800" fill="#F2C14E" text-anchor="end" letter-spacing="1">costao.com.br</text>
    </g>
  </g>
</svg>'''

# DESIGN 2: OSTRA PEROLADA
nfc_waves_d2 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#B98A3E", stroke_width=3.2, direction="right")
svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_bodoni_hanken}
      .font-serif2 {{ font-family: 'Bodoni Moda', Georgia, serif; }}
      .font-sans2 {{ font-family: 'Hanken Grotesk', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc2"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="bg2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FAF5EB"/>
      <stop offset="1" stop-color="#ECE3D2"/>
    </linearGradient>
    <radialGradient id="pearl2" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.45" stop-color="#F4ECE0"/>
      <stop offset="1" stop-color="#CDBFA8"/>
    </radialGradient>
    <filter id="pearl-shadow2" x="-20%" y="-20%" width="1.4" height="1.4">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#0E3B3F" flood-opacity="0.15"/>
    </filter>
  </defs>

  <g clip-path="url(#cc2)">
    <rect width="1000" height="1000" fill="url(#bg2)"/>

    <g opacity="0.08" stroke="#0E3B3F" stroke-width="1.5">
      <line x1="500" y1="1000" x2="0" y2="350"/>
      <line x1="500" y1="1000" x2="100" y2="250"/>
      <line x1="500" y1="1000" x2="220" y2="180"/>
      <line x1="500" y1="1000" x2="350" y2="130"/>
      <line x1="500" y1="1000" x2="500" y2="110"/>
      <line x1="500" y1="1000" x2="650" y2="130"/>
      <line x1="500" y1="1000" x2="780" y2="180"/>
      <line x1="500" y1="1000" x2="900" y2="250"/>
      <line x1="500" y1="1000" x2="1000" y2="350"/>
      <path d="M150,750 Q500,450 850,750" fill="none" stroke-width="2"/>
      <path d="M250,850 Q500,650 750,850" fill="none" stroke-width="2"/>
    </g>

    <image href="{b64_navy}" x="70" y="60" width="360" height="100" preserveAspectRatio="xMinYMid meet"/>

    <g transform="translate(845, 115)" filter="url(#pearl-shadow2)">
      <circle cx="0" cy="0" r="52" fill="none" stroke="#B98A3E" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.7"/>
      <circle cx="0" cy="0" r="45" fill="url(#pearl2)"/>
      <circle cx="0" cy="0" r="41" fill="#FAF5EB" stroke="#B98A3E" stroke-width="1"/>
      <g transform="translate(-4, 0)">
        {nfc_waves_d2}
      </g>
    </g>
    <text class="font-sans2" x="845" y="190" font-size="15" font-weight="800" fill="#0E3B3F" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-sans2" x="845" y="210" font-size="12" font-weight="600" fill="#7A6852" text-anchor="middle">Aproxime o celular</text>

    <text class="font-serif2" x="70" y="215" font-size="34" font-weight="700" fill="#0E3B3F" letter-spacing="0.5">Um toque libera a sua estadia</text>
    <line x1="70" y1="230" x2="360" y2="230" stroke="#B98A3E" stroke-width="2"/>

    <g transform="translate(70, 265)">
      <circle cx="20" cy="38" r="6" fill="#B98A3E"/>
      <text class="font-serif2" x="42" y="35" font-size="26" font-weight="700" fill="#0E3B3F">Costão SPA &amp; Relax</text>
      <text class="font-sans2" x="42" y="62" font-size="15.5" font-weight="500" fill="#3D5658">
        Massagens aromáticas exclusivas, banhos de imersão e rituais botânicos.
      </text>
      <line x1="0" y1="85" x2="860" y2="85" stroke="#0E3B3F" stroke-width="1" stroke-opacity="0.12"/>
    </g>

    <g transform="translate(70, 375)">
      <circle cx="20" cy="38" r="6" fill="#B98A3E"/>
      <text class="font-serif2" x="42" y="35" font-size="26" font-weight="700" fill="#0E3B3F">Shows &amp; Programação Diária</text>
      <text class="font-sans2" x="42" y="62" font-size="15.5" font-weight="500" fill="#3D5658">
        Espetáculos ao vivo, apresentações musicais e lazer para todas as idades.
      </text>
      <line x1="0" y1="85" x2="860" y2="85" stroke="#0E3B3F" stroke-width="1" stroke-opacity="0.12"/>
    </g>

    <g transform="translate(70, 485)">
      <circle cx="20" cy="38" r="6" fill="#B98A3E"/>
      <text class="font-serif2" x="42" y="35" font-size="26" font-weight="700" fill="#0E3B3F">Restaurantes, Bares &amp; Ostras</text>
      <text class="font-sans2" x="42" y="62" font-size="15.5" font-weight="500" fill="#3D5658">
        Cardápios da gastronomia açoriana, frutos do mar frescos e reservas exclusivas.
      </text>
      <line x1="0" y1="85" x2="860" y2="85" stroke="#0E3B3F" stroke-width="1" stroke-opacity="0.12"/>
    </g>

    <g transform="translate(70, 595)">
      <circle cx="20" cy="38" r="6" fill="#B98A3E"/>
      <text class="font-serif2" x="42" y="35" font-size="26" font-weight="700" fill="#0E3B3F">Mapa Geral &amp; Guia do Resort</text>
      <text class="font-sans2" x="42" y="62" font-size="15.5" font-weight="500" fill="#3D5658">
        Localização de piscinas, vilas, trilhas até o sítio arqueológico e Wi-Fi.
      </text>
      <line x1="0" y1="85" x2="860" y2="85" stroke="#0E3B3F" stroke-width="1" stroke-opacity="0.12"/>
    </g>

    <g transform="translate(70, 930)">
      <line x1="0" y1="0" x2="860" y2="0" stroke="#0E3B3F" stroke-width="1" stroke-opacity="0.15"/>
      <text class="font-sans2" x="0" y="30" font-size="14" font-weight="600" fill="#586E70">Experiência Gastronômica &amp; Hospitalidade • Praia do Santinho</text>
      <text class="font-sans2" x="860" y="30" font-size="15" font-weight="800" fill="#B98A3E" text-anchor="end" letter-spacing="1">costao.com.br</text>
    </g>
  </g>
</svg>'''

# DESIGN 3: PÔR DO SOL
nfc_waves_d3 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#FFF4DC", stroke_width=3.2, direction="right")
svg3 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_outfit}
      .font-outfit {{ font-family: 'Outfit', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc3"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="sunset-sky3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1A0A10"/>
      <stop offset="0.4" stop-color="#4A1822"/>
      <stop offset="0.75" stop-color="#9E3824"/>
      <stop offset="1" stop-color="#F28522"/>
    </linearGradient>
    <radialGradient id="sun3" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.3" stop-color="#FFF2BD"/>
      <stop offset="0.7" stop-color="#FFC561"/>
      <stop offset="1" stop-color="#F27A18"/>
    </radialGradient>
    <filter id="sun-glow3" x="-30%" y="-30%" width="1.6" height="1.6">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <g clip-path="url(#cc3)">
    <rect width="1000" height="1000" fill="url(#sunset-sky3)"/>

    <g fill="none" stroke="#FFF4DC" stroke-linecap="round" opacity="0.25">
      <path d="M220,580 A280,280 0 0,1 780,580" stroke-width="8"/>
      <path d="M280,580 A220,220 0 0,1 720,580" stroke-width="6"/>
      <path d="M340,580 A160,160 0 0,1 660,580" stroke-width="5"/>
    </g>

    <path d="M0,640 Q250,620 500,640 T1000,630 L1000,1000 L0,1000 Z" fill="#12050A" opacity="0.95"/>

    <image href="{b64_gold}" x="70" y="60" width="360" height="100" preserveAspectRatio="xMinYMid meet"/>

    <g transform="translate(845, 115)">
      <circle cx="0" cy="0" r="54" fill="none" stroke="#FFC561" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.7"/>
      <circle cx="0" cy="0" r="46" fill="url(#sun3)" filter="url(#sun-glow3)"/>
      <circle cx="0" cy="0" r="42" fill="#240B13"/>
      <g transform="translate(-4, 0)">
        {nfc_waves_d3}
      </g>
    </g>
    <text class="font-outfit" x="845" y="192" font-size="15" font-weight="800" fill="#FFC561" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-outfit" x="845" y="212" font-size="12" font-weight="600" fill="#FFF4DC" text-anchor="middle" opacity="0.9">Aproxime o celular</text>

    <text class="font-outfit" x="70" y="215" font-size="34" font-weight="800" fill="#FFF4DC">Um toque libera a sua experiência</text>
    <line x1="70" y1="230" x2="380" y2="230" stroke="#FFC561" stroke-width="2.5"/>

    <g transform="translate(70, 260)">
      <rect width="860" height="85" rx="14" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFC561" stroke-opacity="0.25" stroke-width="1"/>
      <text class="font-outfit" x="25" y="36" font-size="22" font-weight="700" fill="#FFF4DC">Costão SPA &amp; Relax</text>
      <text class="font-outfit" x="25" y="62" font-size="14.5" font-weight="400" fill="#FFDAB0">Massagens exclusivas, hidro aquecida, saunas e terapias de renovação</text>
    </g>

    <g transform="translate(70, 360)">
      <rect width="860" height="85" rx="14" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFC561" stroke-opacity="0.25" stroke-width="1"/>
      <text class="font-outfit" x="25" y="36" font-size="22" font-weight="700" fill="#FFF4DC">Shows &amp; Programação Diária</text>
      <text class="font-outfit" x="25" y="62" font-size="14.5" font-weight="400" fill="#FFDAB0">Agenda artística ao vivo, bandas, peças de teatro e recreação infantil</text>
    </g>

    <g transform="translate(70, 460)">
      <rect width="860" height="85" rx="14" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFC561" stroke-opacity="0.25" stroke-width="1"/>
      <text class="font-outfit" x="25" y="36" font-size="22" font-weight="700" fill="#FFF4DC">Restaurantes, Bares &amp; Reservas</text>
      <text class="font-outfit" x="25" y="62" font-size="14.5" font-weight="400" fill="#FFDAB0">Cardápios all-inclusive, reservas para jantar e alta gastronomia</text>
    </g>

    <g transform="translate(70, 560)">
      <rect width="860" height="85" rx="14" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFC561" stroke-opacity="0.25" stroke-width="1"/>
      <text class="font-outfit" x="25" y="36" font-size="22" font-weight="700" fill="#FFF4DC">Mapa Geral, Wi-Fi &amp; Trilhas</text>
      <text class="font-outfit" x="25" y="62" font-size="14.5" font-weight="400" fill="#FFDAB0">Localização das vilas, piscinas, sítio arqueológico e suporte ao hóspede</text>
    </g>

    <g transform="translate(70, 930)">
      <line x1="0" y1="0" x2="860" y2="0" stroke="#FFC561" stroke-width="1" stroke-opacity="0.3"/>
      <text class="font-outfit" x="0" y="30" font-size="14" font-weight="500" fill="#FFDAB0">Experiência All-Inclusive na Praia do Santinho • Florianópolis</text>
      <text class="font-outfit" x="860" y="30" font-size="15" font-weight="800" fill="#FFC561" text-anchor="end" letter-spacing="1">costao.com.br</text>
    </g>
  </g>
</svg>'''

# DESIGN 4: ETIQUETA DE BAGAGEM FLN
nfc_waves_d4 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#F6B137", stroke_width=3.2, direction="right")
svg4 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_space_barlow}
      .font-mono4 {{ font-family: 'Space Mono', monospace; }}
      .font-condensed4 {{ font-family: 'Barlow Condensed', sans-serif; }}
    </style>
    <clipPath id="cc4"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <pattern id="dots4" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#FFFFFF" opacity="0.04"/>
    </pattern>
    <linearGradient id="tag-bg4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#092226"/>
      <stop offset="0.6" stop-color="#0E3339"/>
      <stop offset="1" stop-color="#14464E"/>
    </linearGradient>
    <linearGradient id="brass4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFE8A3"/>
      <stop offset="0.5" stop-color="#F6B137"/>
      <stop offset="1" stop-color="#B87B16"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc4)">
    <rect width="1000" height="1000" fill="url(#tag-bg4)"/>
    <rect width="1000" height="1000" fill="url(#dots4)"/>

    <rect x="35" y="35" width="930" height="930" rx="40" fill="none" stroke="#F6B137" stroke-width="1.8" stroke-dasharray="8,6" opacity="0.4"/>

    <g transform="translate(500, 48)">
      <circle cx="0" cy="0" r="18" fill="url(#brass4)"/>
      <circle cx="0" cy="0" r="10" fill="#092226"/>
    </g>

    <g transform="translate(70, 50)">
      <rect width="140" height="26" rx="4" fill="#F6B137" fill-opacity="0.15" stroke="#F6B137" stroke-width="1"/>
      <text class="font-mono4" x="70" y="17" font-size="11" font-weight="700" fill="#F6B137" text-anchor="middle" letter-spacing="2">FLN • SANTINHO</text>
    </g>

    <image href="{b64_sand}" x="70" y="90" width="340" height="92" preserveAspectRatio="xMinYMid meet"/>

    <g transform="translate(845, 115)">
      <circle cx="0" cy="0" r="52" fill="url(#brass4)"/>
      <circle cx="0" cy="0" r="46" fill="#092226"/>
      <g transform="translate(-4, 0)">
        {nfc_waves_d4}
      </g>
    </g>
    <text class="font-mono4" x="845" y="192" font-size="14" font-weight="700" fill="#F6B137" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-condensed4" x="845" y="212" font-size="13" font-weight="600" fill="#D3E7EB" text-anchor="middle">APROXIME O CELULAR</text>

    <text class="font-condensed4" x="70" y="218" font-size="36" font-weight="800" fill="#FFFFFF" letter-spacing="1">UM TOQUE LIBERA O SEU ACESSO VIP</text>
    <line x1="70" y1="232" x2="380" y2="232" stroke="#F6B137" stroke-width="2"/>

    <g transform="translate(70, 260)">
      <rect width="860" height="85" rx="10" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1"/>
      <rect x="0" y="0" width="6" height="85" rx="3" fill="#F6B137"/>
      <text class="font-mono4" x="25" y="32" font-size="14" font-weight="700" fill="#F6B137">01 [BEM-ESTAR]</text>
      <text class="font-condensed4" x="25" y="60" font-size="24" font-weight="700" fill="#FFFFFF">COSTÃO SPA &amp; RELAX</text>
      <text class="font-condensed4" x="260" y="60" font-size="16" font-weight="500" fill="#A2C4CA">— Massagens, hidromassagem e rituais de renovação</text>
    </g>

    <g transform="translate(70, 360)">
      <rect width="860" height="85" rx="10" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1"/>
      <rect x="0" y="0" width="6" height="85" rx="3" fill="#F6B137"/>
      <text class="font-mono4" x="25" y="32" font-size="14" font-weight="700" fill="#F6B137">02 [LAZER]</text>
      <text class="font-condensed4" x="25" y="60" font-size="24" font-weight="700" fill="#FFFFFF">SHOWS &amp; PROGRAMAÇÃO</text>
      <text class="font-condensed4" x="280" y="60" font-size="16" font-weight="500" fill="#A2C4CA">— Agenda diária ao vivo, teatro e recreação infantil</text>
    </g>

    <g transform="translate(70, 460)">
      <rect width="860" height="85" rx="10" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1"/>
      <rect x="0" y="0" width="6" height="85" rx="3" fill="#F6B137"/>
      <text class="font-mono4" x="25" y="32" font-size="14" font-weight="700" fill="#F6B137">03 [GASTRONOMIA]</text>
      <text class="font-condensed4" x="25" y="60" font-size="24" font-weight="700" fill="#FFFFFF">RESTAURANTES &amp; BARES</text>
      <text class="font-condensed4" x="280" y="60" font-size="16" font-weight="500" fill="#A2C4CA">— Cardápios completos all-inclusive e reservas</text>
    </g>

    <g transform="translate(70, 560)">
      <rect width="860" height="85" rx="10" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1"/>
      <rect x="0" y="0" width="6" height="85" rx="3" fill="#F6B137"/>
      <text class="font-mono4" x="25" y="32" font-size="14" font-weight="700" fill="#F6B137">04 [COMPLEXO]</text>
      <text class="font-condensed4" x="25" y="60" font-size="24" font-weight="700" fill="#FFFFFF">MAPA &amp; GUIA RESORT</text>
      <text class="font-condensed4" x="260" y="60" font-size="16" font-weight="500" fill="#A2C4CA">— Localização de vilas, piscinas, Wi-Fi e trilhas</text>
    </g>

    <g transform="translate(70, 920)">
      <line x1="0" y1="0" x2="860" y2="0" stroke="#F6B137" stroke-width="1" stroke-opacity="0.25"/>
      <text class="font-mono4" x="0" y="30" font-size="13" font-weight="400" fill="#A2C4CA">GPS: 27°28'14"S 48°22'40"W • RESORT SANTINHO</text>
      <text class="font-mono4" x="860" y="30" font-size="14" font-weight="700" fill="#F6B137" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# 5. Write and Render
master_files = [
    ("01_ponte_noturna_master.svg", svg1),
    ("02_ostras_perola_master.svg", svg2),
    ("03_por_do_sol_master.svg", svg3),
    ("04_etiqueta_bagagem_master.svg", svg4)
]

def render_svg_to_png(svg_path, png_path, width=2000, height=2000):
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        "--default-background-color=00000000",
        svg_path
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    return os.path.exists(png_path)

for fname, content in master_files:
    fpath = os.path.join(out_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    png_path = fpath.replace(".svg", ".png")
    render_svg_to_png(fpath, png_path, 2000, 2000)
    print(f"Generated {fname} & {os.path.basename(png_path)}")

print("All 4 Masterclass pieces successfully generated and rendered!")

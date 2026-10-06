import os
import re
import math
import io
import base64
from PIL import Image

out_dir = r"C:\Users\Augusto\Desktop\AH3\BigBrain\handoff\placas_costao"
attachments_dir = r"C:\Users\Augusto\AppData\Local\hermes\profiles\designer\attachments"

# 1. Extract embedded fonts
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

# 2. Extract and recolor logo to Charcoal & Gold
logo_path = os.path.join(out_dir, "logo_costao.png")
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

b64_charcoal = to_b64(recolor_png(img, (28, 32, 38)))

# 3. Lucide Official NFC Icon with exact optical centering
def get_lucide_nfc_svg(cx, cy, size=46, color="#C89B3C", stroke_width=2.2):
    scale = size / 24.0
    tx = cx - (11.2 * scale)
    ty = cy - (12.0 * scale)
    return f'''<g transform="translate({tx:.2f}, {ty:.2f}) scale({scale:.4f})" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 8.32a7.43 7.43 0 0 1 0 7.36"/>
        <path d="M9.46 6.21a11.76 11.76 0 0 1 0 11.58"/>
        <path d="M12.91 4.1a15.91 15.91 0 0 1 .01 15.8"/>
        <path d="M16.37 2a20.16 20.16 0 0 1 0 20"/>
      </g>'''

# 4. Brick Pattern
brick_w = 118
brick_h = 46
mortar = 6
rows = 24
cols = 10

brick_paths = []
for r_idx in range(rows):
    y = r_idx * (brick_h + mortar) - 20
    offset_x = - (brick_w / 2) if (r_idx % 2 == 1) else 0
    for c_idx in range(-1, cols + 2):
        x = c_idx * (brick_w + mortar) + offset_x
        brick_paths.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{brick_w}" height="{brick_h}" rx="3" fill="#FAF7F2" stroke="#EAE2D5" stroke-width="1.2"/>')
        brick_paths.append(f'<line x1="{x+3:.1f}" y1="{y+2:.1f}" x2="{x+brick_w-3:.1f}" y2="{y+2:.1f}" stroke="#FFFFFF" stroke-width="1.5" opacity="0.9"/>')
        brick_paths.append(f'<line x1="{x+3:.1f}" y1="{y+brick_h-1:.1f}" x2="{x+brick_w-3:.1f}" y2="{y+brick_h-1:.1f}" stroke="#D8CEBD" stroke-width="1.2" opacity="0.7"/>')

bricks_svg_block = "\n    ".join(brick_paths)

font_cormorant_jost = font_defs.get('Cormorant Garamond', '') + "\n" + font_defs.get('Jost', '')
lucide_nfc_block = get_lucide_nfc_svg(735, 90, size=46, color="#C89B3C", stroke_width=2.2)

svg_brick = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_cormorant_jost}
      .font-serif-brick {{ font-family: 'Cormorant Garamond', Georgia, serif; }}
      .font-sans-brick {{ font-family: 'Jost', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc_brick"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    
    <radialGradient id="wall_light" cx="0.5" cy="0.08" r="0.85">
      <stop offset="0" stop-color="#FFF8EC" stop-opacity="0.95"/>
      <stop offset="0.35" stop-color="#F7EEDC" stop-opacity="0.6"/>
      <stop offset="0.7" stop-color="#E2D4C0" stop-opacity="0.2"/>
      <stop offset="1" stop-color="#CBBBA4" stop-opacity="0.05"/>
    </radialGradient>

    <linearGradient id="ambient_vignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6B543E" stop-opacity="0.35"/>
      <stop offset="0.15" stop-color="#6B543E" stop-opacity="0.05"/>
      <stop offset="0.8" stop-color="#4A3828" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#2D1F14" stop-opacity="0.45"/>
    </linearGradient>

    <filter id="plaque_drop" x="-10%" y="-10%" width="1.2" height="1.25">
      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#3A2818" flood-opacity="0.28"/>
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#3A2818" flood-opacity="0.15"/>
    </filter>

    <linearGradient id="brass_standoff" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFF1CF"/>
      <stop offset="0.35" stop-color="#E5C170"/>
      <stop offset="0.7" stop-color="#C59B3F"/>
      <stop offset="1" stop-color="#8F6A1E"/>
    </linearGradient>

    <linearGradient id="plaque_surface" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="1" stop-color="#FAF6EE" stop-opacity="0.92"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_brick)">
    <rect width="1000" height="1000" fill="#E8DEC8"/>

    <g>
      {bricks_svg_block}
    </g>

    <rect width="1000" height="1000" fill="url(#wall_light)"/>
    <rect width="1000" height="1000" fill="url(#ambient_vignette)"/>

    <path d="M350,0 Q500,120 650,0 Z" fill="#FFFFFF" opacity="0.45" filter="blur(10px)"/>

    <g transform="translate(70, 75)" filter="url(#plaque_drop)">
      <rect width="860" height="850" rx="32" fill="url(#plaque_surface)" stroke="#D4AF37" stroke-width="1.5" stroke-opacity="0.4"/>
      <rect x="8" y="8" width="844" height="834" rx="26" fill="none" stroke="#E2D7C5" stroke-width="1"/>

      <!-- Distanciadores / Parafusos Franceses nos 4 Cantos -->
      <g transform="translate(36, 36)">
        <circle cx="0" cy="0" r="10" fill="url(#brass_standoff)"/>
        <circle cx="0" cy="0" r="8" fill="#523E1E" opacity="0.4"/>
        <circle cx="0" cy="0" r="3" fill="#FFF1CF"/>
      </g>
      <g transform="translate(824, 36)">
        <circle cx="0" cy="0" r="10" fill="url(#brass_standoff)"/>
        <circle cx="0" cy="0" r="8" fill="#523E1E" opacity="0.4"/>
        <circle cx="0" cy="0" r="3" fill="#FFF1CF"/>
      </g>
      <g transform="translate(36, 814)">
        <circle cx="0" cy="0" r="10" fill="url(#brass_standoff)"/>
        <circle cx="0" cy="0" r="8" fill="#523E1E" opacity="0.4"/>
        <circle cx="0" cy="0" r="3" fill="#FFF1CF"/>
      </g>
      <g transform="translate(824, 814)">
        <circle cx="0" cy="0" r="10" fill="url(#brass_standoff)"/>
        <circle cx="0" cy="0" r="8" fill="#523E1E" opacity="0.4"/>
        <circle cx="0" cy="0" r="3" fill="#FFF1CF"/>
      </g>

      <!-- Logo Costão do Santinho -->
      <image href="{b64_charcoal}" x="55" y="45" width="350" height="92" preserveAspectRatio="xMinYMid meet"/>

      <!-- SENSOR NFC ALINHADO COM ÍCONE OFICIAL LUCIDE -->
      <g transform="translate(735, 90)">
        <circle cx="0" cy="0" r="48" fill="none" stroke="#C89B3C" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.7"/>
        <circle cx="0" cy="0" r="42" fill="url(#brass_standoff)"/>
        <circle cx="0" cy="0" r="38" fill="#FAF6EE"/>
      </g>
      {lucide_nfc_block}

      <text class="font-sans-brick" x="735" y="156" font-size="13" font-weight="800" fill="#1C2026" text-anchor="middle" letter-spacing="3">NFC</text>
      <text class="font-sans-brick" x="735" y="174" font-size="11.5" font-weight="600" fill="#7A6852" text-anchor="middle">Aproxime o celular</text>

      <!-- Chamada -->
      <text class="font-serif-brick" x="55" y="185" font-size="34" font-weight="700" fill="#1C2026" letter-spacing="0.5">Um toque libera a sua estadia</text>
      <line x1="55" y1="202" x2="360" y2="202" stroke="#C89B3C" stroke-width="2"/>

      <!-- 4 Experiências -->
      <g transform="translate(55, 235)">
        <text class="font-serif-brick" x="0" y="32" font-size="28" font-weight="700" fill="#C89B3C">01</text>
        <text class="font-serif-brick" x="48" y="32" font-size="24" font-weight="700" fill="#1C2026">Costão SPA &amp; Relax</text>
        <text class="font-sans-brick" x="48" y="56" font-size="15" font-weight="400" fill="#585044">Massagens exclusivas, hidro aquecida, saunas e terapias de renovação</text>
        <line x1="0" y1="76" x2="750" y2="76" stroke="#E2D7C5" stroke-width="1"/>
      </g>

      <g transform="translate(55, 340)">
        <text class="font-serif-brick" x="0" y="32" font-size="28" font-weight="700" fill="#C89B3C">02</text>
        <text class="font-serif-brick" x="48" y="32" font-size="24" font-weight="700" fill="#1C2026">Shows &amp; Programação Diária</text>
        <text class="font-sans-brick" x="48" y="56" font-size="15" font-weight="400" fill="#585044">Agenda artística ao vivo, música na praça, teatro e lazer infantil</text>
        <line x1="0" y1="76" x2="750" y2="76" stroke="#E2D7C5" stroke-width="1"/>
      </g>

      <g transform="translate(55, 445)">
        <text class="font-serif-brick" x="0" y="32" font-size="28" font-weight="700" fill="#C89B3C">03</text>
        <text class="font-serif-brick" x="48" y="32" font-size="24" font-weight="700" fill="#1C2026">Restaurantes &amp; Bares All-Inclusive</text>
        <text class="font-sans-brick" x="48" y="56" font-size="15" font-weight="400" fill="#585044">Cardápios assinados em tempo real, reservas de alta gastronomia e adega</text>
        <line x1="0" y1="76" x2="750" y2="76" stroke="#E2D7C5" stroke-width="1"/>
      </g>

      <g transform="translate(55, 550)">
        <text class="font-serif-brick" x="0" y="32" font-size="28" font-weight="700" fill="#C89B3C">04</text>
        <text class="font-serif-brick" x="48" y="32" font-size="24" font-weight="700" fill="#1C2026">Mapa Geral, Wi-Fi &amp; Trilhas</text>
        <text class="font-sans-brick" x="48" y="56" font-size="15" font-weight="400" fill="#585044">Localização das vilas, piscinas aquecidas, sítio arqueológico e trilhas</text>
        <line x1="0" y1="76" x2="750" y2="76" stroke="#E2D7C5" stroke-width="1"/>
      </g>

      <!-- Rodapé -->
      <g transform="translate(55, 780)">
        <text class="font-sans-brick" x="0" y="0" font-size="13" font-weight="500" fill="#8A7A68">Praia do Santinho — Florianópolis • Santa Catarina</text>
        <text class="font-sans-brick" x="750" y="0" font-size="14" font-weight="700" fill="#1C2026" text-anchor="end">costao.com.br</text>
      </g>
    </g>
  </g>
</svg>'''

output_svg_path = os.path.join(out_dir, "costao_efeito_tijolo_iluminado.svg")
with open(output_svg_path, "w", encoding="utf-8") as f:
    f.write(svg_brick)

print(f"Updated {output_svg_path} with official Lucide NFC alignment!")

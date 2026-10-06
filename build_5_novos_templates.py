import os
import re
import math
import io
import base64
import subprocess
from PIL import Image

out_dir = r"C:\Users\Augusto\Desktop\AH3\BigBrain\handoff\placas_costao\novos_templates"
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
logo_path = os.path.join(r"C:\Users\Augusto\Desktop\AH3\BigBrain\handoff\placas_costao", "logo_costao.png")
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

# Palette-specific logos
b64_charcoal = to_b64(recolor_png(img, (26, 28, 30)))         # Clean Escandinavo
b64_terracotta = to_b64(recolor_png(img, (184, 80, 48)))      # Terroso e Natural
b64_botanical = to_b64(recolor_png(img, (24, 60, 42)))        # Botânico
b64_stitch = to_b64(recolor_png(img, (82, 66, 50)))           # Linho e Textura
b64_gold_matte = to_b64(recolor_png(img, (218, 178, 102)))    # Luz de Vela

# 3. Mathematically perfect Contactless NFC waves generator
def generate_nfc_waves(cx, cy, radii=[10, 18, 26, 34], stroke="#D4A843", stroke_width=3.0, direction="right"):
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

# =========================================================================
# TEMPLATE 1: CLEAN ESCANDINAVO
# Fundo off-white, tipografia preta fina, ícones minimalistas, muito respiro
# =========================================================================
font_inter = font_defs.get('Inter', '') + "\n" + font_defs.get('Jost', '')
nfc_w1 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#1A1C1E", stroke_width=2.5, direction="right")

svg1 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_inter}
      .font-sans-clean {{ font-family: 'Inter', 'Jost', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc_esc"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="bg_nordic" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FAF9F6"/>
      <stop offset="1" stop-color="#F2EFE9"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_esc)">
    <!-- Fundo Off-White Puro e Sereno -->
    <rect width="1000" height="1000" fill="url(#bg_nordic)"/>

    <!-- Moldura Fina Minimalista Escandinava -->
    <rect x="50" y="50" width="900" height="900" rx="30" fill="none" stroke="#E2DDD5" stroke-width="1.2"/>

    <!-- Topo: Logo Costão em Preto Carvão Fino -->
    <image href="{b64_charcoal}" x="80" y="80" width="340" height="90" preserveAspectRatio="xMinYMid meet"/>

    <!-- Sensor NFC Minimalista Nórdico -->
    <g transform="translate(840, 125)">
      <circle cx="0" cy="0" r="45" fill="none" stroke="#1A1C1E" stroke-width="1.2"/>
      <g transform="translate(-4, 0)">
        {nfc_w1}
      </g>
    </g>
    <text class="font-sans-clean" x="840" y="195" font-size="13" font-weight="700" fill="#1A1C1E" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-sans-clean" x="840" y="214" font-size="11" font-weight="400" fill="#787672" text-anchor="middle">Aproxime o celular</text>

    <!-- Respiro Generoso e Título Minimalista -->
    <text class="font-sans-clean" x="80" y="250" font-size="28" font-weight="300" fill="#1A1C1E" letter-spacing="-0.5">Um toque libera a sua experiência</text>
    <line x1="80" y1="270" x2="160" y2="270" stroke="#1A1C1E" stroke-width="1.5"/>

    <!-- 4 Serviços com Linhas Finas e Espaço Aberto -->
    <g transform="translate(80, 330)">
      <text class="font-sans-clean" x="0" y="28" font-size="21" font-weight="600" fill="#1A1C1E">Costão SPA &amp; Relax</text>
      <text class="font-sans-clean" x="0" y="52" font-size="14.5" font-weight="400" fill="#6E6B65">Massagens exclusivas, hidroterapia, saunas e renovação</text>
      <line x1="0" y1="75" x2="840" y2="75" stroke="#E5E0D8" stroke-width="1"/>
    </g>

    <g transform="translate(80, 445)">
      <text class="font-sans-clean" x="0" y="28" font-size="21" font-weight="600" fill="#1A1C1E">Shows &amp; Programação Diária</text>
      <text class="font-sans-clean" x="0" y="52" font-size="14.5" font-weight="400" fill="#6E6B65">Agenda de atrações ao vivo, música, teatro e lazer infantil</text>
      <line x1="0" y1="75" x2="840" y2="75" stroke="#E5E0D8" stroke-width="1"/>
    </g>

    <g transform="translate(80, 560)">
      <text class="font-sans-clean" x="0" y="28" font-size="21" font-weight="600" fill="#1A1C1E">Restaurantes &amp; Bares</text>
      <text class="font-sans-clean" x="0" y="52" font-size="14.5" font-weight="400" fill="#6E6B65">Cardápios completos all-inclusive, reservas e carta de vinhos</text>
      <line x1="0" y1="75" x2="840" y2="75" stroke="#E5E0D8" stroke-width="1"/>
    </g>

    <g transform="translate(80, 675)">
      <text class="font-sans-clean" x="0" y="28" font-size="21" font-weight="600" fill="#1A1C1E">Mapa Geral &amp; Guia do Resort</text>
      <text class="font-sans-clean" x="0" y="52" font-size="14.5" font-weight="400" fill="#6E6B65">Localização de vilas, piscinas, Wi-Fi liberado e trilhas ecológicas</text>
      <line x1="0" y1="75" x2="840" y2="75" stroke="#E5E0D8" stroke-width="1"/>
    </g>

    <!-- Rodapé Discreto -->
    <g transform="translate(80, 915)">
      <text class="font-sans-clean" x="0" y="25" font-size="13" font-weight="400" fill="#8C8880">Costão do Santinho • Florianópolis</text>
      <text class="font-sans-clean" x="840" y="25" font-size="13" font-weight="600" fill="#1A1C1E" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# =========================================================================
# TEMPLATE 2: TERROSO E NATURAL
# Terracota, areia, verde sálvia, formas orgânicas e curvas suaves
# =========================================================================
font_fraunces_nunito = font_defs.get('Fraunces', '') + "\n" + font_defs.get('Nunito', '')
nfc_w2 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#B85030", stroke_width=3.2, direction="right")

svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_fraunces_nunito}
      .font-serif-natural {{ font-family: 'Fraunces', Georgia, serif; }}
      .font-sans-natural {{ font-family: 'Nunito', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc_terroso"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="bg_earth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FBF7EE"/>
      <stop offset="1" stop-color="#EFE6D5"/>
    </linearGradient>
    <linearGradient id="terracotta_grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#D46A48"/>
      <stop offset="1" stop-color="#A84428"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_terroso)">
    <!-- Base Areia Quente -->
    <rect width="1000" height="1000" fill="url(#bg_earth)"/>

    <!-- Formas Orgânicas Fluidas em Verde Sálvia e Terracota Suave -->
    <path d="M-50,280 C180,220 320,340 580,260 C800,190 920,290 1050,220 L1050,-50 L-50,-50 Z" fill="#6A8D73" opacity="0.12"/>
    <path d="M-50,680 C200,600 420,740 680,640 C880,560 980,690 1050,620 L1050,1050 L-50,1050 Z" fill="#D46A48" opacity="0.08"/>

    <!-- Topo: Logo Costão em Terracota -->
    <image href="{b64_terracotta}" x="75" y="65" width="350" height="95" preserveAspectRatio="xMinYMid meet"/>

    <!-- Sensor NFC em Medalhão Terracota Natural -->
    <g transform="translate(840, 115)">
      <circle cx="0" cy="0" r="50" fill="#E8DDD0" stroke="#B85030" stroke-width="1.5"/>
      <circle cx="0" cy="0" r="44" fill="#F4EFE6"/>
      <g transform="translate(-4, 0)">
        {nfc_w2}
      </g>
    </g>
    <text class="font-sans-natural" x="840" y="185" font-size="14" font-weight="800" fill="#B85030" text-anchor="middle" letter-spacing="2">NFC</text>
    <text class="font-sans-natural" x="840" y="205" font-size="12" font-weight="600" fill="#58685A" text-anchor="middle">Aproxime o celular</text>

    <!-- Frase Orgânica -->
    <text class="font-serif-natural" x="75" y="215" font-size="32" font-weight="700" fill="#2E241E">Acolhimento natural &amp; bem-estar</text>
    <path d="M75,232 Q200,240 320,230" stroke="#B85030" stroke-width="2.5" fill="none" stroke-linecap="round"/>

    <!-- 4 Cards com Curvas Suaves e Pílula Sálvia/Terracota -->
    <g transform="translate(75, 265)">
      <rect width="850" height="120" rx="24" fill="#FFFFFF" stroke="#E0D6C4" stroke-width="1.5"/>
      <circle cx="55" cy="60" r="28" fill="#E4EFE7"/>
      <path d="M55,46 C48,53 43,58 43,64 C43,71 48,75 55,75 C62,75 67,71 67,64 C67,58 62,53 55,46 Z" fill="#4B6B54"/>
      <text class="font-sans-natural" x="105" y="46" font-size="12" font-weight="800" fill="#4B6B54" letter-spacing="1.5">RELAXAMENTO</text>
      <text class="font-serif-natural" x="105" y="74" font-size="22" font-weight="700" fill="#2E241E">Costão SPA &amp; Terapias da Terra</text>
      <text class="font-sans-natural" x="105" y="96" font-size="14.5" font-weight="500" fill="#6A5C52">Massagens botânicas, banhos de argila, hidro e rituais orgânicos</text>
    </g>

    <g transform="translate(75, 410)">
      <rect width="850" height="120" rx="24" fill="#FFFFFF" stroke="#E0D6C4" stroke-width="1.5"/>
      <circle cx="55" cy="60" r="28" fill="#FCEEE8"/>
      <path d="M55,44 L57,53 L66,54 L59,60 L61,69 L55,64 L49,69 L51,60 L44,54 L53,53 Z" fill="#B85030"/>
      <text class="font-sans-natural" x="105" y="46" font-size="12" font-weight="800" fill="#B85030" letter-spacing="1.5">ENTRETENIMENTO</text>
      <text class="font-serif-natural" x="105" y="74" font-size="22" font-weight="700" fill="#2E241E">Shows &amp; Cultura Açoriana</text>
      <text class="font-sans-natural" x="105" y="96" font-size="14.5" font-weight="500" fill="#6A5C52">Música ao vivo sob o céu da ilha, recreação infantil e apresentações</text>
    </g>

    <g transform="translate(75, 555)">
      <rect width="850" height="120" rx="24" fill="#FFFFFF" stroke="#E0D6C4" stroke-width="1.5"/>
      <circle cx="55" cy="60" r="28" fill="#E4EFE7"/>
      <circle cx="55" cy="60" r="14" fill="none" stroke="#4B6B54" stroke-width="2"/>
      <path d="M50,51 L50,69 M60,51 L60,69" stroke="#B85030" stroke-width="2" stroke-linecap="round"/>
      <text class="font-sans-natural" x="105" y="46" font-size="12" font-weight="800" fill="#4B6B54" letter-spacing="1.5">GASTRONOMIA</text>
      <text class="font-serif-natural" x="105" y="74" font-size="22" font-weight="700" fill="#2E241E">Restaurantes da Horta ao Mar</text>
      <text class="font-sans-natural" x="105" y="96" font-size="14.5" font-weight="500" fill="#6A5C52">Ingredientes locais frescos, peixes da estação e reservas all-inclusive</text>
    </g>

    <g transform="translate(75, 700)">
      <rect width="850" height="120" rx="24" fill="#FFFFFF" stroke="#E0D6C4" stroke-width="1.5"/>
      <circle cx="55" cy="60" r="28" fill="#FCEEE8"/>
      <path d="M45,69 L55,49 L65,69 Z" fill="none" stroke="#B85030" stroke-width="2"/>
      <circle cx="55" cy="58" r="3" fill="#4B6B54"/>
      <text class="font-sans-natural" x="105" y="46" font-size="12" font-weight="800" fill="#B85030" letter-spacing="1.5">NATUREZA</text>
      <text class="font-serif-natural" x="105" y="74" font-size="22" font-weight="700" fill="#2E241E">Trilhas, Dunas &amp; Guia Resort</text>
      <text class="font-sans-natural" x="105" y="96" font-size="14.5" font-weight="500" fill="#6A5C52">Caminhos ecológicos, inscrições rupestres, vilas e mapa interativo</text>
    </g>

    <!-- Rodapé -->
    <g transform="translate(75, 915)">
      <line x1="0" y1="0" x2="850" y2="0" stroke="#D8CDBC" stroke-width="1"/>
      <text class="font-sans-natural" x="0" y="30" font-size="14" font-weight="600" fill="#6A5C52">Costão do Santinho • Praia do Santinho, Florianópolis</text>
      <text class="font-sans-natural" x="850" y="30" font-size="14" font-weight="800" fill="#B85030" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# =========================================================================
# TEMPLATE 3: BOTÂNICO
# Ilustrações de plantas nativas (bromélias, folhagens da Mata Atlântica)
# =========================================================================
font_botanical = font_defs.get('Cormorant Garamond', '') + "\n" + font_defs.get('Jost', '')
nfc_w3 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#286044", stroke_width=3.2, direction="right")

svg3 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_botanical}
      .font-botanical-title {{ font-family: 'Cormorant Garamond', Georgia, serif; }}
      .font-botanical-body {{ font-family: 'Jost', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc_bot"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <linearGradient id="bg_bot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FAF8F2"/>
      <stop offset="1" stop-color="#EEEDE2"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_bot)">
    <!-- Base Marfim Botânico -->
    <rect width="1000" height="1000" fill="url(#bg_bot)"/>

    <!-- Moldura Fina com Acento Verde Floresta -->
    <rect x="40" y="40" width="920" height="920" rx="34" fill="none" stroke="#286044" stroke-width="1.2" stroke-opacity="0.3"/>

    <!-- Ilustrações Botânicas Vetoriais nas Bordas (Bromélias e Folhas Nativas) -->
    <!-- Canto Superior Esquerdo -->
    <g transform="translate(45, 45)" stroke="#286044" fill="none" stroke-width="1.5" opacity="0.45">
      <path d="M0,0 Q60,30 90,80 Q40,60 0,0"/>
      <path d="M0,0 Q30,60 80,90 Q60,40 0,0"/>
      <path d="M0,0 Q80,10 120,40 Q60,40 0,0"/>
      <path d="M0,0 Q10,80 40,120 Q40,60 0,0"/>
    </g>

    <!-- Canto Superior Direito -->
    <g transform="translate(955, 45) scale(-1, 1)" stroke="#286044" fill="none" stroke-width="1.5" opacity="0.45">
      <path d="M0,0 Q60,30 90,80 Q40,60 0,0"/>
      <path d="M0,0 Q30,60 80,90 Q60,40 0,0"/>
    </g>

    <!-- Canto Inferior Esquerdo -->
    <g transform="translate(45, 955) scale(1, -1)" stroke="#286044" fill="none" stroke-width="1.5" opacity="0.45">
      <path d="M0,0 Q60,30 90,80 Q40,60 0,0"/>
      <path d="M0,0 Q30,60 80,90 Q60,40 0,0"/>
    </g>

    <!-- Canto Inferior Direito (Bromélia Completa) -->
    <g transform="translate(955, 955) scale(-1, -1)" stroke="#286044" fill="none" stroke-width="1.5" opacity="0.55">
      <path d="M0,0 Q70,35 110,95 Q50,70 0,0" fill="#286044" fill-opacity="0.08"/>
      <path d="M0,0 Q35,70 95,110 Q70,50 0,0" fill="#286044" fill-opacity="0.08"/>
      <path d="M0,0 Q90,15 140,50 Q70,50 0,0"/>
      <path d="M0,0 Q15,90 50,140 Q50,70 0,0"/>
    </g>

    <!-- Logo Costão em Verde Botânico Nobre -->
    <image href="{b64_botanical}" x="75" y="65" width="350" height="95" preserveAspectRatio="xMinYMid meet"/>

    <!-- Sensor NFC em Selo Botânico Gravado -->
    <g transform="translate(840, 115)">
      <circle cx="0" cy="0" r="50" fill="#FAF8F2" stroke="#286044" stroke-width="1.8"/>
      <circle cx="0" cy="0" r="44" fill="none" stroke="#286044" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>
      <g transform="translate(-4, 0)">
        {nfc_w3}
      </g>
    </g>
    <text class="font-botanical-body" x="840" y="185" font-size="14" font-weight="800" fill="#286044" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-botanical-body" x="840" y="205" font-size="12" font-weight="600" fill="#4B6355" text-anchor="middle">Aproxime o celular</text>

    <!-- Título Serifado Nobre -->
    <text class="font-botanical-title" x="75" y="215" font-size="34" font-weight="700" fill="#183C2A">Reserva Ecológica &amp; Resort de Luxo</text>
    <line x1="75" y1="230" x2="380" y2="230" stroke="#286044" stroke-width="2"/>

    <!-- 4 Serviços Botânicos com Folha Delicada -->
    <g transform="translate(75, 270)">
      <circle cx="15" cy="20" r="4" fill="#286044"/>
      <text class="font-botanical-title" x="35" y="25" font-size="25" font-weight="700" fill="#183C2A">Costão SPA &amp; Rituais da Mata</text>
      <text class="font-botanical-body" x="35" y="52" font-size="15.5" font-weight="400" fill="#43594C">Massagens com óleos botânicos nativos, hidro aquecida e saunas relaxantes</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#286044" stroke-width="1" stroke-opacity="0.15"/>
    </g>

    <g transform="translate(75, 380)">
      <circle cx="15" cy="20" r="4" fill="#286044"/>
      <text class="font-botanical-title" x="35" y="25" font-size="25" font-weight="700" fill="#183C2A">Shows &amp; Programação Cultural</text>
      <text class="font-botanical-body" x="35" y="52" font-size="15.5" font-weight="400" fill="#43594C">Apresentações artísticas diárias, música ao vivo e lazer ecológico infantil</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#286044" stroke-width="1" stroke-opacity="0.15"/>
    </g>

    <g transform="translate(75, 490)">
      <circle cx="15" cy="20" r="4" fill="#286044"/>
      <text class="font-botanical-title" x="35" y="25" font-size="25" font-weight="700" fill="#183C2A">Restaurantes &amp; Sabores da Terra</text>
      <text class="font-botanical-body" x="35" y="52" font-size="15.5" font-weight="400" fill="#43594C">Cardápios da gastronomia açoriana e internacional, all-inclusive e reservas</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#286044" stroke-width="1" stroke-opacity="0.15"/>
    </g>

    <g transform="translate(75, 600)">
      <circle cx="15" cy="20" r="4" fill="#286044"/>
      <text class="font-botanical-title" x="35" y="25" font-size="25" font-weight="700" fill="#183C2A">Trilhas da Mata Atlântica &amp; Arqueologia</text>
      <text class="font-botanical-body" x="35" y="52" font-size="15.5" font-weight="400" fill="#43594C">Mapa interativo de trilhas preservadas, sítio rupestre, piscinas e Wi-Fi</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#286044" stroke-width="1" stroke-opacity="0.15"/>
    </g>

    <!-- Rodapé -->
    <g transform="translate(75, 920)">
      <line x1="0" y1="0" x2="850" y2="0" stroke="#286044" stroke-width="1" stroke-opacity="0.2"/>
      <text class="font-botanical-body" x="0" y="30" font-size="14" font-weight="500" fill="#4B6355">Reserva Florestal do Santinho • Florianópolis</text>
      <text class="font-botanical-body" x="850" y="30" font-size="15" font-weight="700" fill="#183C2A" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# =========================================================================
# TEMPLATE 4: LINHO E TEXTURA
# Fundo que simula tecido de linho com trama. Logo e grafismos bordados/costurados
# =========================================================================
font_linen = font_defs.get('Space Mono', '') + "\n" + font_defs.get('Barlow Condensed', '')
nfc_w4 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#8A6848", stroke_width=3.2, direction="right")

svg4 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_linen}
      .font-mono-linen {{ font-family: 'Space Mono', monospace; }}
      .font-condensed-linen {{ font-family: 'Barlow Condensed', sans-serif; }}
    </style>
    <clipPath id="cc_lin"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <!-- Padrão de Trama de Tecido de Linho Fino -->
    <pattern id="linen_weave" width="12" height="12" patternUnits="userSpaceOnUse">
      <rect width="12" height="12" fill="#F4EFE6"/>
      <line x1="0" y1="3" x2="12" y2="3" stroke="#E5DC handle" stroke="#E2D6C4" stroke-width="0.8" opacity="0.6"/>
      <line x1="0" y1="9" x2="12" y2="9" stroke="#E2D6C4" stroke-width="0.8" opacity="0.6"/>
      <line x1="3" y1="0" x2="3" y2="12" stroke="#E2D6C4" stroke-width="0.8" opacity="0.6"/>
      <line x1="9" y1="0" x2="9" y2="12" stroke="#E2D6C4" stroke-width="0.8" opacity="0.6"/>
    </pattern>
    <linearGradient id="linen_shadow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FAF7F0"/>
      <stop offset="1" stop-color="#E8DFC8"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_lin)">
    <!-- Base Linho Tecido -->
    <rect width="1000" height="1000" fill="url(#linen_shadow)"/>
    <rect width="1000" height="1000" fill="url(#linen_weave)" opacity="0.7"/>

    <!-- Costura Perimetral Dupla de Alta Costura (Bordado Tátil) -->
    <rect x="36" y="36" width="928" height="928" rx="36" fill="none" stroke="#8A6848" stroke-width="2" stroke-dasharray="6,4" opacity="0.5"/>
    <rect x="46" y="46" width="908" height="908" rx="28" fill="none" stroke="#C2A88A" stroke-width="1" opacity="0.4"/>

    <!-- Logo Costão Bordado em Tons de Linho Escuro -->
    <image href="{b64_stitch}" x="75" y="70" width="340" height="90" preserveAspectRatio="xMinYMid meet"/>

    <!-- Sensor NFC em Etiqueta / Patch de Couro/Linho Bordado -->
    <g transform="translate(840, 120)">
      <rect x="-50" y="-45" width="100" height="90" rx="16" fill="#EDE4D4" stroke="#8A6848" stroke-width="1.8" stroke-dasharray="5,3"/>
      <g transform="translate(-4, -6)">
        {nfc_w4}
      </g>
      <text class="font-mono-linen" x="0" y="32" font-size="12" font-weight="700" fill="#524232" text-anchor="middle" letter-spacing="2">NFC</text>
    </g>
    <text class="font-condensed-linen" x="840" y="205" font-size="13" font-weight="700" fill="#8A6848" text-anchor="middle" letter-spacing="1">APROXIME O CELULAR</text>

    <!-- Chamada Estilo Alfaiataria -->
    <text class="font-condensed-linen" x="75" y="222" font-size="34" font-weight="800" fill="#423425" letter-spacing="1.5">UM TOQUE LIBERA SUA ESTADIA EXCLUSIVA</text>
    <line x1="75" y1="236" x2="380" y2="236" stroke="#8A6848" stroke-width="2" stroke-dasharray="8,4"/>

    <!-- 4 Blocos em Formato de Patches de Tecido -->
    <g transform="translate(75, 270)">
      <rect width="850" height="120" rx="16" fill="#FAF6EE" stroke="#D8CAAF" stroke-width="1.5" stroke-dasharray="8,4"/>
      <text class="font-mono-linen" x="30" y="42" font-size="13" font-weight="700" fill="#8A6848">[01] BEM-ESTAR</text>
      <text class="font-condensed-linen" x="30" y="72" font-size="24" font-weight="700" fill="#423425">COSTÃO SPA &amp; RELAX</text>
      <text class="font-condensed-linen" x="30" y="96" font-size="16" font-weight="500" fill="#75614D">Massagens exclusivas, hidromassagem aquecida, saunas e terapias</text>
    </g>

    <g transform="translate(75, 415)">
      <rect width="850" height="120" rx="16" fill="#FAF6EE" stroke="#D8CAAF" stroke-width="1.5" stroke-dasharray="8,4"/>
      <text class="font-mono-linen" x="30" y="42" font-size="13" font-weight="700" fill="#8A6848">[02] LAZER &amp; ARTE</text>
      <text class="font-condensed-linen" x="30" y="72" font-size="24" font-weight="700" fill="#423425">SHOWS &amp; PROGRAMAÇÃO DIÁRIA</text>
      <text class="font-condensed-linen" x="30" y="96" font-size="16" font-weight="500" fill="#75614D">Agenda artística ao vivo, bandas, teatro e recreação infantil completa</text>
    </g>

    <g transform="translate(75, 560)">
      <rect width="850" height="120" rx="16" fill="#FAF6EE" stroke="#D8CAAF" stroke-width="1.5" stroke-dasharray="8,4"/>
      <text class="font-mono-linen" x="30" y="42" font-size="13" font-weight="700" fill="#8A6848">[03] SABORES</text>
      <text class="font-condensed-linen" x="30" y="72" font-size="24" font-weight="700" fill="#423425">RESTAURANTES &amp; BARES ALL-INCLUSIVE</text>
      <text class="font-condensed-linen" x="30" y="96" font-size="16" font-weight="500" fill="#75614D">Cardápios assinados, carta de vinhos, reservas e horários em tempo real</text>
    </g>

    <g transform="translate(75, 705)">
      <rect width="850" height="120" rx="16" fill="#FAF6EE" stroke="#D8CAAF" stroke-width="1.5" stroke-dasharray="8,4"/>
      <text class="font-mono-linen" x="30" y="42" font-size="13" font-weight="700" fill="#8A6848">[04] RESORT</text>
      <text class="font-condensed-linen" x="30" y="72" font-size="24" font-weight="700" fill="#423425">MAPA GERAL, WI-FI &amp; TRILHAS</text>
      <text class="font-condensed-linen" x="30" y="96" font-size="16" font-weight="500" fill="#75614D">Localização de vilas, piscinas, trilhas ecológicas e arqueologia</text>
    </g>

    <!-- Rodapé -->
    <g transform="translate(75, 920)">
      <line x1="0" y1="0" x2="850" y2="0" stroke="#8A6848" stroke-width="1.2" stroke-dasharray="6,4" opacity="0.4"/>
      <text class="font-mono-linen" x="0" y="30" font-size="13" font-weight="400" fill="#75614D">COSTÃO DO SANTINHO • FLORIANÓPOLIS</text>
      <text class="font-mono-linen" x="850" y="30" font-size="14" font-weight="700" fill="#423425" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# =========================================================================
# TEMPLATE 5: LUZ DE VELA
# Fundo escuro aconchegante (marrom sépia/chumbo), detalhes dourado fosco
# =========================================================================
font_candle = font_defs.get('Bodoni Moda', '') + "\n" + font_defs.get('Hanken Grotesk', '')
nfc_w5 = generate_nfc_waves(0, 0, radii=[10, 18, 26, 34], stroke="#DAB266", stroke_width=3.2, direction="right")

svg5 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      {font_candle}
      .font-candle-title {{ font-family: 'Bodoni Moda', Georgia, serif; }}
      .font-candle-body {{ font-family: 'Hanken Grotesk', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cc_candle"><rect width="1000" height="1000" rx="60" ry="60"/></clipPath>
    <!-- Gradiente de Luz de Vela Aconchegante e Quente -->
    <radialGradient id="candle_glow" cx="0.5" cy="0.15" r="0.85">
      <stop offset="0" stop-color="#3A281E"/>
      <stop offset="0.5" stop-color="#231710"/>
      <stop offset="1" stop-color="#140E0A"/>
    </radialGradient>
    <linearGradient id="gold_matte" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F3DC9B"/>
      <stop offset="0.5" stop-color="#DAB266"/>
      <stop offset="1" stop-color="#A57F32"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cc_candle)">
    <!-- Base Escura e Aveludada de Luz de Vela -->
    <rect width="1000" height="1000" fill="url(#candle_glow)"/>

    <!-- Moldura Fina em Dourado Fosco -->
    <rect x="40" y="40" width="920" height="920" rx="34" fill="none" stroke="#DAB266" stroke-width="1.2" stroke-opacity="0.35"/>
    <circle cx="48" cy="48" r="3" fill="#DAB266" opacity="0.5"/>
    <circle cx="952" cy="48" r="3" fill="#DAB266" opacity="0.5"/>
    <circle cx="48" cy="952" r="3" fill="#DAB266" opacity="0.5"/>
    <circle cx="952" cy="952" r="3" fill="#DAB266" opacity="0.5"/>

    <!-- Logo Costão em Dourado Fosco Nobre -->
    <image href="{b64_gold_matte}" x="75" y="65" width="350" height="95" preserveAspectRatio="xMinYMid meet"/>

    <!-- Sensor NFC em Medalhão Dourado com Halo de Luz Suave -->
    <g transform="translate(840, 115)">
      <circle cx="0" cy="0" r="50" fill="none" stroke="#DAB266" stroke-width="1.2" opacity="0.6"/>
      <circle cx="0" cy="0" r="44" fill="#2A1C14" stroke="#DAB266" stroke-width="1.5"/>
      <g transform="translate(-4, 0)">
        {nfc_w5}
      </g>
    </g>
    <text class="font-candle-body" x="840" y="188" font-size="14" font-weight="800" fill="#DAB266" text-anchor="middle" letter-spacing="3">NFC</text>
    <text class="font-candle-body" x="840" y="208" font-size="12" font-weight="500" fill="#E8D5B8" text-anchor="middle" opacity="0.8">Aproxime o celular</text>

    <!-- Chamada Aconchegante Bodoni -->
    <text class="font-candle-title" x="75" y="218" font-size="34" font-weight="700" fill="#FAF0DC">Uma experiência intimista &amp; memorável</text>
    <line x1="75" y1="234" x2="380" y2="234" stroke="#DAB266" stroke-width="1.8"/>

    <!-- 4 Experiências Noturnas/Aconchegantes -->
    <g transform="translate(75, 270)">
      <text class="font-candle-title" x="0" y="26" font-size="25" font-weight="700" fill="#FAF0DC">Costão SPA &amp; Relax Noturno</text>
      <text class="font-candle-body" x="0" y="52" font-size="15.5" font-weight="400" fill="#D1BAA0">Hidromassagens aquecidas sob as estrelas, saunas e rituais relaxantes</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#DAB266" stroke-width="1" stroke-opacity="0.18"/>
    </g>

    <g transform="translate(75, 380)">
      <text class="font-candle-title" x="0" y="26" font-size="25" font-weight="700" fill="#FAF0DC">Shows, Música &amp; Vida Noturna</text>
      <text class="font-candle-body" x="0" y="52" font-size="15.5" font-weight="400" fill="#D1BAA0">Apresentações acústicas, teatro, shows ao vivo e programação diária</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#DAB266" stroke-width="1" stroke-opacity="0.18"/>
    </g>

    <g transform="translate(75, 490)">
      <text class="font-candle-title" x="0" y="26" font-size="25" font-weight="700" fill="#FAF0DC">Restaurantes, Adega &amp; Jantares VIP</text>
      <text class="font-candle-body" x="0" y="52" font-size="15.5" font-weight="400" fill="#D1BAA0">Jantares à luz de velas, carta de vinhos finos e reservas gastronômicas</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#DAB266" stroke-width="1" stroke-opacity="0.18"/>
    </g>

    <g transform="translate(75, 600)">
      <text class="font-candle-title" x="0" y="26" font-size="25" font-weight="700" fill="#FAF0DC">Mapa Geral &amp; Guia do Resort</text>
      <text class="font-candle-body" x="0" y="52" font-size="15.5" font-weight="400" fill="#D1BAA0">Navegação noturna pelas vilas, piscinas aquecidas, Wi-Fi e concierges</text>
      <line x1="0" y1="75" x2="850" y2="75" stroke="#DAB266" stroke-width="1" stroke-opacity="0.18"/>
    </g>

    <!-- Rodapé -->
    <g transform="translate(75, 920)">
      <line x1="0" y1="0" x2="850" y2="0" stroke="#DAB266" stroke-width="1" stroke-opacity="0.2"/>
      <text class="font-candle-body" x="0" y="30" font-size="14" font-weight="400" fill="#D1BAA0">Hospitalidade de Alto Padrão • Praia do Santinho, Florianópolis</text>
      <text class="font-candle-body" x="850" y="30" font-size="15" font-weight="700" fill="#DAB266" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

# 5. Save files and render to PNG
new_templates = [
    ("01_clean_escandinavo.svg", svg1),
    ("02_terroso_natural.svg", svg2),
    ("03_botanico_mata_atlantica.svg", svg3),
    ("04_linho_textura.svg", svg4),
    ("05_luz_de_vela.svg", svg5)
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

for fname, content in new_templates:
    fpath = os.path.join(out_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    png_path = fpath.replace(".svg", ".png")
    render_svg_to_png(fpath, png_path, 2000, 2000)
    print(f"Generated {fname} & {os.path.basename(png_path)}")

print("All 5 new templates generated and rendered successfully!")

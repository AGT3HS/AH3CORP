import os, base64, subprocess
from PIL import Image, ImageDraw

raw_logo_path = 'BigBrain/handoff/guias_identidade_visual/logos/33_palace_praia_hotel/33_palace_praia_hotel_icon_2.jpeg'
img = Image.open(raw_logo_path).convert('RGBA')

# Remover fundo branco puro/quase branco da logo transformando em transparência alfa
datas = img.getdata()
new_data = []
for item in datas:
    # Se for tom de branco/cinza muito claro (fundo), torna transparente
    if item[0] > 225 and item[1] > 225 and item[2] > 225:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

img.putdata(new_data)
transparent_logo_path = 'BigBrain/handoff/guias_identidade_visual/logos/33_palace_praia_hotel/33_palace_praia_hotel_logo_transparente.png'
img.save(transparent_logo_path, format='PNG')
print('Logo transparente salva em:', transparent_logo_path)

with open(transparent_logo_path, 'rb') as f:
    logo_b64 = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

top_colors = [
    ('01_modelo_classico_cor_mae.svg', '#1B3A6B'),
    ('02_modelo_noturno_luxo.svg', '#0A1E36'),
    ('03_modelo_secundario_acento.svg', '#3D68A2'),
    ('04_modelo_monocromatico_autoridade.svg', '#1A242B')
]

hotel_dir = 'BigBrain/handoff/placas_hoteis_layout02/33_33_palace_praia_hotel'

for v_file, v_color in top_colors:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      @font-face {{
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400 800;
        src: local('Inter'), local('Segoe UI'), local('Arial');
      }}
      text {{ font-family: 'Inter', -apple-system, sans-serif; }}
    </style>
    <clipPath id="cardClip">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cardClip)">
    <rect width="1000" height="1000" fill="#FAF8F5"/>
    <path d="M0,0 L1000,0 L1000,540 Q500,440 0,540 Z" fill="{v_color}"/>

    <!-- LOGO OFICIAL 100% TRANSPARENTE SEM FUNDO BRANCO -->
    <image href="{logo_b64}" x="80" y="110" width="380" height="160" preserveAspectRatio="xMidYMid meet" />

    <g transform="translate(830, 95)">
      <g stroke="#F5A623" stroke-width="6" stroke-linecap="round" fill="none" transform="translate(0, 40)">
        <circle cx="-25" cy="0" r="3.5" fill="#F5A623" stroke="none"/>
        <path d="M-12,-18 C-3,-9 -3,9 -12,18"/>
        <path d="M3,-30 C18,-15 18,15 3,30"/>
        <path d="M18,-42 C38,-21 38,21 18,42"/>
      </g>
      <g transform="translate(0, 115)">
        <rect x="-44" y="-18" width="88" height="36" rx="18" fill="#F5A623"/>
        <text x="0" y="6" font-size="16" font-weight="800" fill="#12181A" text-anchor="middle" letter-spacing="1.5">NFC</text>
      </g>
      <text x="0" y="170" font-size="14" font-weight="500" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <g transform="translate(80, 600)">
      <text x="0" y="0" font-size="16" font-weight="800" fill="#12181A" letter-spacing="3">UM TOQUE LIBERA</text>
    </g>

    <g transform="translate(80, 640)">
      <circle cx="40" cy="40" r="40" fill="#12181A" fill-opacity="0.08"/>
      <g stroke="#12181A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(26, 26)">
        <path d="M2 9 C8 3 20 3 26 9"/>
        <path d="M6 14 C10 10 18 10 22 14"/>
        <circle cx="14" cy="20" r="2" fill="#12181A"/>
      </g>
      <text x="96" y="36" font-size="22" font-weight="700" fill="#12181A">Wi-Fi Instantâneo</text>
      <text x="96" y="60" font-size="15" font-weight="500" fill="#4B5563">Conexão sem senha manual</text>
    </g>

    <g transform="translate(540, 640)">
      <circle cx="40" cy="40" r="40" fill="#12181A" fill-opacity="0.08"/>
      <g stroke="#12181A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(26, 26)">
        <rect x="3" y="3" width="22" height="22" rx="4"/>
        <path d="M9 14 L13 18 L19 10"/>
      </g>
      <text x="96" y="36" font-size="22" font-weight="700" fill="#12181A">Serviços &amp; Lazer</text>
      <text x="96" y="60" font-size="15" font-weight="500" fill="#4B5563">Piscina, café e horários</text>
    </g>

    <g transform="translate(80, 755)">
      <circle cx="40" cy="40" r="40" fill="#12181A" fill-opacity="0.08"/>
      <g stroke="#12181A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(26, 26)">
        <path d="M5 3 L5 12 C5 15 8 17 11 17 L11 27"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M17 3 L17 12 C17 15 14 17 11 17"/>
        <path d="M23 3 C27 8 27 15 24 18 L24 27"/>
      </g>
      <text x="96" y="36" font-size="22" font-weight="700" fill="#12181A">Gastronomia &amp; Bar</text>
      <text x="96" y="60" font-size="15" font-weight="500" fill="#4B5563">Cardápio digital atualizado</text>
    </g>

    <g transform="translate(540, 755)">
      <circle cx="40" cy="40" r="40" fill="#12181A" fill-opacity="0.08"/>
      <g stroke="#12181A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(26, 26)">
        <polygon points="14,2 18,10 26,11 20,17 22,25 14,20 6,25 8,17 2,11 10,10"/>
      </g>
      <text x="96" y="36" font-size="22" font-weight="700" fill="#12181A">Avaliar no Google</text>
      <text x="96" y="60" font-size="15" font-weight="500" fill="#4B5563">Avaliação rápida em 1 toque</text>
    </g>

    <line x1="80" y1="880" x2="920" y2="880" stroke="#12181A" stroke-opacity="0.12" stroke-width="1.5"/>
    <g transform="translate(80, 920)">
      <text x="0" y="0" font-size="16" font-weight="600" fill="#6B7280" letter-spacing="1">EXPERIÊNCIA DO HÓSPEDE</text>
      <text x="840" y="0" font-size="16" font-weight="700" fill="{v_color}" text-anchor="end">palacepraiahotel.com.br</text>
    </g>
  </g>
</svg>'''
    with open(os.path.join(hotel_dir, v_file), 'w', encoding='utf-8') as f:
        f.write(svg)

print('4 placas do Palace Praia Hotel atualizadas!')

# Renderizar amostra com Chromium Headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

html_file = 'saida/render_palace_praia_transparent.html'
raw_png = 'saida/raw_palace_praia_transparent.png'
out_png = 'saida/33_palace_praia_hotel_cor_mae_transparente.png'

with open(os.path.join(hotel_dir, '01_modelo_classico_cor_mae.svg'), 'r', encoding='utf-8') as f:
    svg_data = f.read()

html_c = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{background:transparent;width:1000px;height:1000px;overflow:hidden;}}svg{{width:1000px;height:1000px;}}</style></head><body>{svg_data}</body></html>'''

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_c)

cmd = [edge_path, '--headless', '--disable-gpu', '--window-size=1000,1000', f'--screenshot={os.path.abspath(raw_png)}', f'file:///{os.path.abspath(html_file).replace(os.sep, "/")}']
subprocess.run(cmd, check=True)

img = Image.open(raw_png).convert('RGBA').crop((0,0,1000,1000))
mask = Image.new('L', (1000,1000), 0)
ImageDraw.Draw(mask).rounded_rectangle([(0,0),(1000,1000)], radius=60, fill=255)
img.putalpha(mask)
img.save(out_png, format='PNG')
print('Renderizado com sucesso:', out_png)

if os.path.exists(html_file): os.remove(html_file)
if os.path.exists(raw_png): os.remove(raw_png)

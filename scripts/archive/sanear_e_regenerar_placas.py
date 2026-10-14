#!/usr/bin/env python3
"""
Regenerador e Saneador de Placas NFC 100x100mm para os Hotéis de Florianópolis.
Regras aplicadas:
1. Expurgar hotéis inexistentes/desativados (Ponta do Coral).
2. Priorizar rigorosamente o arquivo '_logo_1.png' ou vetor oficial em vez do '_icon_2.jpeg' ou favicons pequenos.
3. Se a logo capturada for de outra rede (ex: Slaviero vinculada erroneamente a Ingleses Palace), aplicar tipografia de marca vetorial nativa com o nome exato do hotel.
4. Seguir o padrão canônico do guia-institucional.pdf.
"""

import os, sys, json, re, base64, glob, unicodedata, subprocess
from PIL import Image, ImageDraw

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

with open('scripts/data/sorted_150_hotels.json', 'r', encoding='utf-8') as f:
    hotels = json.load(f)

with open('scripts/data/brandfetch_all_150_data.json', 'r', encoding='utf-8') as f:
    bf_data = json.load(f)

bf_map = {}
for item in bf_data:
    domain = item.get('domain', '')
    site = item.get('site', '')
    nome = item.get('nome', '')
    if domain: bf_map[normalize(domain)] = item
    if site: bf_map[normalize(site)] = item
    if nome: bf_map[normalize(nome)] = item

all_logos_1 = glob.glob('guias_identidade_visual/logos/*/*_logo_1.*') + glob.glob('BigBrain/handoff/guias_identidade_visual/logos/*/*_logo_1.*')
all_logos_general = glob.glob('guias_identidade_visual/logos/*/*.*') + glob.glob('BigBrain/handoff/guias_identidade_visual/logos/*/*.*')

def get_hotel_logo_b64(hotel):
    nome = hotel.get('nome', '')
    nome_norm = normalize(nome)
    
    # Validação contra logos de redes atribuídas erroneamente a hotéis independentes
    if 'ingleses palace' in nome.lower():
        # Não usar logo de Slaviero
        return ""
        
    # 1. Procurar especificamente arquivo *_logo_1.* correspondente
    for p in all_logos_1:
        p_norm = normalize(p)
        if nome_norm in p_norm or (len(nome_norm) > 8 and nome_norm[:8] in p_norm):
            try:
                with open(p, 'rb') as f:
                    ext = os.path.splitext(p)[1].lower().replace('.', '')
                    mime = 'image/svg+xml' if ext == 'svg' else f'image/{ext}'
                    return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')
            except: pass
            
    # 2. Procurar em all_logos_general mas ignorando icons/favicons
    for p in all_logos_general:
        if 'icon' in p.lower() or 'favicon' in p.lower():
            continue
        p_norm = normalize(p)
        if nome_norm in p_norm or (len(nome_norm) > 8 and nome_norm[:8] in p_norm):
            try:
                with open(p, 'rb') as f:
                    ext = os.path.splitext(p)[1].lower().replace('.', '')
                    mime = 'image/svg+xml' if ext == 'svg' else f'image/{ext}'
                    return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')
            except: pass
            
    return ""

def get_hotel_colors(hotel):
    nome_norm = normalize(hotel.get('nome', ''))
    site_norm = normalize(hotel.get('site', ''))
    bf_item = bf_map.get(site_norm) or bf_map.get(nome_norm)
    
    colors = []
    if bf_item and 'cores' in bf_item:
        for c in bf_item['cores']:
            h = c.get('hex', '')
            if h and h.startswith('#') and len(h) == 7:
                if h.upper() not in ['#000000', '#FFFFFF', '#FFF', '#000']:
                    colors.append(h.upper())
                    
    default_palettes = [
        ['#1B3A6B', '#0A1E36', '#3D68A2', '#12181A'],
        ['#007A6C', '#072E27', '#25A18E', '#142823'],
        ['#A63A24', '#2B110B', '#C95D42', '#1E1412'],
        ['#36454F', '#182026', '#5F7382', '#121619'],
    ]
    rank = hotel.get('ranking', 1)
    base_default = default_palettes[rank % len(default_palettes)]
    
    c_mae = colors[0] if len(colors) > 0 else base_default[0]
    c_noturno = "#0A1E36" if c_mae != "#0A1E36" else "#051324"
    c_acento = colors[1] if len(colors) > 1 else base_default[2]
    c_mono = "#1A242B"
    return c_mae, c_noturno, c_acento, c_mono

def build_svg_card(hotel, variant_name, top_color, logo_b64):
    nome = hotel.get('nome', 'HOTEL')
    site = hotel.get('site', 'hotel.com.br').replace('https://', '').replace('http://', '').rstrip('/')
    if len(site) > 30: site = site[:28] + '...'
    
    if logo_b64:
        logo_markup = f'<image href="{logo_b64}" x="80" y="110" width="380" height="160" preserveAspectRatio="xMidYMid meet" />'
    else:
        display_nome = nome[:20].upper()
        logo_markup = f'''<g transform="translate(80, 160)">
          <text font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-size="34" font-weight="800" fill="#FFFFFF" letter-spacing="2">{display_nome}</text>
          <text font-family="'Plus Jakarta Sans', -apple-system, sans-serif" font-size="16" font-weight="600" fill="#FAF8F5" opacity="0.8" y="32" letter-spacing="4">FLORIANÓPOLIS</text>
        </g>'''

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
    <path d="M0,0 L1000,0 L1000,540 Q500,440 0,540 Z" fill="{top_color}"/>

    {logo_markup}

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
      <text x="840" y="0" font-size="16" font-weight="700" fill="{top_color}" text-anchor="end">{site}</text>
    </g>
  </g>
</svg>'''
    return svg

base_output = 'BigBrain/handoff/placas_hoteis_layout02'
os.makedirs(base_output, exist_ok=True)

# Limpar pasta antiga do Ponta do Coral
for folder in os.listdir(base_output):
    if 'ponta_do_coral' in folder:
        import shutil
        shutil.rmtree(os.path.join(base_output, folder))
        print("Pasta expurgada:", folder)

count = 0
for h in hotels:
    rank = h.get('ranking')
    if rank <= 40:
        continue
        
    nome_slug = re.sub(r'[^a-z0-9_]', '', unicodedata.normalize('NFKD', h['nome']).encode('ASCII', 'ignore').decode('ASCII').lower().replace(' ', '_'))
    folder_name = f"{rank:02d}_{rank:02d}_{nome_slug}"
    hotel_dir = os.path.join(base_output, folder_name)
    os.makedirs(hotel_dir, exist_ok=True)
    
    logo_b64 = get_hotel_logo_b64(h)
    c_mae, c_noturno, c_acento, c_mono = get_hotel_colors(h)
    
    variants = [
        ('01_modelo_classico_cor_mae.svg', c_mae),
        ('02_modelo_noturno_luxo.svg', c_noturno),
        ('03_modelo_secundario_acento.svg', c_acento),
        ('04_modelo_monocromatico_autoridade.svg', c_mono)
    ]
    
    for v_filename, v_color in variants:
        v_path = os.path.join(hotel_dir, v_filename)
        svg_content = build_svg_card(h, v_filename, v_color, logo_b64)
        with open(v_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
    count += 1

print(f"Concluído: {count} hotéis atualizados e saneados com sucesso!")

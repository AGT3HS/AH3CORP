#!/usr/bin/env python3
"""
AH3 — Gerador Parametrizado de Placas Inteligentes NFC 100x100mm (SVG / PNG)
Agente Encarregado: @Designer
Tipografia Canônica: Outfit (Títulos, Marca e CTAs) + Inter (Subtextos e Operacional)
Padrão: SVG 1000x1000, rx=60 (6mm), safe margin 90 un (9mm), curva canônica V530 Q500,480 0,530 Z.
Proibição Estrita de #000000 e #FFFFFF puros.
"""

import os
import sys
import re
import json
import base64
import argparse
import unicodedata
import glob
import pymupdf
from PIL import Image

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def find_hotel_asset(slug_or_name):
    norm_query = normalize(slug_or_name)
    
    # 1. Check in guias_identidade_visual logos
    logo_candidates = (
        glob.glob('BigBrain/handoff/guias_identidade_visual/logos/*/*.*') +
        glob.glob('guias_identidade_visual/logos/*/*.*') +
        glob.glob('BigBrain/modelos/logos/*.*')
    )
    logo_path = None
    for lp in logo_candidates:
        if norm_query in normalize(lp):
            logo_path = lp
            break
            
    # Fallback to default Jurerê if not found
    if not logo_path or not os.path.exists(logo_path):
        fallback_candidates = (
            glob.glob('BigBrain/handoff/guias_identidade_visual/logos/02_jurer_beach_village/*_logo_1.png') +
            glob.glob('guias_identidade_visual/logos/02_jurer_beach_village/*_logo_1.png')
        )
        if fallback_candidates:
            logo_path = fallback_candidates[0]
        else:
            logo_path = logo_candidates[0] if logo_candidates else ''

    return logo_path

def gerar_placa(nome, subtitulo="FLORIANÓPOLIS • BRASIL", cor_primaria="#276B75", cor_topo="#4DA2AD", cor_fundo="#FAF8F5", cor_destaque="#E8A825", logo_path=None, output_dir="saida/placas_nfc"):
    os.makedirs(output_dir, exist_ok=True)
    slug = normalize(nome)
    
    logo_b64 = ""
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            ext = os.path.splitext(logo_path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            logo_b64 = f"data:image/{ext};base64," + base64.b64encode(f.read()).decode('utf-8')
            
    logo_tag = f'<image x="0" y="0" width="135" height="135" preserveAspectRatio="xMidYMid meet" href="{logo_b64}"/>' if logo_b64 else ''
    text_x_offset = 155 if logo_b64 else 0

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Outfit:wght@600;700;800;900&amp;display=swap');
      .font-title {{ font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif; font-weight: 800; }}
      .font-sub {{ font-family: 'Outfit', 'Inter', sans-serif; font-weight: 600; }}
      .font-body {{ font-family: 'Inter', sans-serif; font-weight: 500; }}
      .font-bold {{ font-family: 'Inter', sans-serif; font-weight: 700; }}
    </style>
    <clipPath id="card-shape">
      <rect x="0" y="0" width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="topGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{cor_topo}"/>
      <stop offset="1" stop-color="{cor_primaria}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#card-shape)">
    <!-- Base Areia Nobre / Fundo Base -->
    <rect width="1000" height="1000" rx="60" ry="60" fill="{cor_fundo}"/>

    <!-- Topo Institucional com Curva Canônica Y=530 bordas / Y=480 centro -->
    <path d="M0,0 H1000 V530 Q500,480 0,530 Z" fill="url(#topGrad)"/>

    <!-- ZONA A: MARCA E IDENTIDADE (Outfit) -->
    <g transform="translate(90, 110)">
      {logo_tag}
      <g transform="translate({text_x_offset}, 42)">
        <text class="font-title" font-size="38" fill="#FAF8F5" letter-spacing="1.5">{nome[:24].upper()}</text>
        <text class="font-sub" font-size="14" fill="{cor_fundo}" letter-spacing="3" opacity="0.9" y="38">{subtitulo.upper()}</text>
      </g>
    </g>

    <!-- ZONA B: SENSOR NFC TÁTIL CANÔNICO (X: 700 a 910) -->
    <g fill="none" stroke="{cor_destaque}" stroke-width="14" stroke-linecap="round">
      <circle cx="720" cy="180" r="14" fill="{cor_destaque}" stroke="none"/>
      <path d="M 760 125 Q 830 180 760 235"/>
      <path d="M 800 95 Q 880 180 800 265"/>
      <path d="M 840 65 Q 930 180 840 295"/>
    </g>

    <!-- Pílula NFC (Outfit) -->
    <rect x="710" y="300" width="180" height="46" rx="23" fill="{cor_destaque}"/>
    <text x="800" y="333" class="font-title" font-size="30" fill="#12181A" text-anchor="middle" letter-spacing="3">NFC</text>
    <text x="800" y="378" class="font-body" font-size="28" fill="{cor_fundo}" text-anchor="middle">Aproxime o celular</text>

    <!-- ZONA C: CHAMADA 'UM TOQUE LIBERA' (Outfit) -->
    <text x="90" y="615" class="font-title" font-size="29" fill="{cor_primaria}" letter-spacing="4">UM TOQUE LIBERA</text>

    <!-- ZONA D: GRADE 2x2 DE ATIVAÇÃO COM ÍCONES VETORIAIS (Inter) -->
    <!-- Item 1: Avaliações Google -->
    <g transform="translate(90, 670)">
      <circle cx="40" cy="40" r="38" fill="{cor_primaria}" fill-opacity="0.12"/>
      <path d="M40 22 L45 33 L57 34 L48 43 L51 55 L40 48 L29 55 L32 43 L23 34 L35 33 Z" fill="{cor_primaria}"/>
      <text x="95" y="48" class="font-bold" font-size="36" fill="#12181A">Avaliações Google</text>
    </g>

    <!-- Item 2: Cardápio & Serviços -->
    <g transform="translate(540, 670)">
      <circle cx="40" cy="40" r="38" fill="{cor_primaria}" fill-opacity="0.12"/>
      <path d="M30 25 V45 M35 25 V45 M40 25 V55 M50 25 C50 35 45 40 45 55" stroke="{cor_primaria}" stroke-width="4" stroke-linecap="round"/>
      <text x="95" y="48" class="font-bold" font-size="36" fill="#12181A">Cardápio &amp; Pedidos</text>
    </g>

    <!-- Item 3: Wi-Fi & Conexão -->
    <g transform="translate(90, 810)">
      <circle cx="40" cy="40" r="38" fill="{cor_primaria}" fill-opacity="0.12"/>
      <path d="M26 34 A20 20 0 0 1 54 34 M31 41 A13 13 0 0 1 49 41 M40 48 A2 2 0 1 1 39.9 48" stroke="{cor_primaria}" stroke-width="4" stroke-linecap="round" fill="none"/>
      <text x="95" y="48" class="font-bold" font-size="36" fill="#12181A">Wi-Fi &amp; Serviços</text>
    </g>

    <!-- Item 4: Atendimento Direto -->
    <g transform="translate(540, 810)">
      <circle cx="40" cy="40" r="38" fill="{cor_primaria}" fill-opacity="0.12"/>
      <path d="M30 46 C30 35 34 30 40 30 C46 30 50 35 50 46 Z M26 48 H54 M40 26 V30" stroke="{cor_primaria}" stroke-width="4" stroke-linecap="round" fill="none"/>
      <text x="95" y="48" class="font-bold" font-size="36" fill="#12181A">Recepção &amp; Salão</text>
    </g>
  </g>
</svg>'''

    svg_file = os.path.join(output_dir, f"placa_nfc_{slug}.svg")
    png_file = os.path.join(output_dir, f"placa_nfc_{slug}.png")

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # Render PNG 300 DPI via PyMuPDF
    doc = pymupdf.open("pdf", pymupdf.open(stream=svg_content.encode("utf-8"), filetype="svg").convert_to_pdf())
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_file)
    
    print(f"OK: Placa SVG gerada em {svg_file}")
    print(f"OK: Placa PNG renderizada (300 DPI) em {png_file}")
    return svg_file, png_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gerador Parametrizado de Placas NFC AH3 (Outfit + Inter)")
    parser.add_argument("--nome", type=str, default="Jurerê Beach Village", help="Nome do Hotel/Restaurante")
    parser.add_argument("--subtitulo", type=str, default="FLORIANÓPOLIS • BRASIL", help="Subtítulo da marca")
    parser.add_argument("--cor_primaria", type=str, default="#276B75", help="Cor primária HEX")
    parser.add_argument("--cor_topo", type=str, default="#4DA2AD", help="Cor topo degradê HEX")
    parser.add_argument("--cor_fundo", type=str, default="#FAF8F5", help="Cor fundo base HEX")
    parser.add_argument("--cor_destaque", type=str, default="#E8A825", help="Cor destaque/NFC HEX")
    parser.add_argument("--logo", type=str, default=None, help="Caminho do arquivo de logo")
    parser.add_argument("--output", type=str, default="saida/placas_nfc", help="Diretório de saída")
    
    args = parser.parse_args()
    logo = args.logo or find_hotel_asset(args.nome)
    gerar_placa(
        nome=args.nome,
        subtitulo=args.subtitulo,
        cor_primaria=args.cor_primaria,
        cor_topo=args.cor_topo,
        cor_fundo=args.cor_fundo,
        cor_destaque=args.cor_destaque,
        logo_path=logo,
        output_dir=args.output
    )

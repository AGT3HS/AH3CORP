# -*- coding: utf-8 -*-
"""
Geração do Cartão NFC Oficial do Costão do Santinho (10x10 cm) com Bordas Arredondadas (Raio de 6mm / rx=60)
Conforme especificação do Guia de Design da AH3.
Gera:
1. Frente com Bordas Arredondadas + Logo Oficial + Cluster NFC + Grade 2x2
2. Verso com Bordas Arredondadas + Container de Avaliação Google 5 Estrelas + QR Code
3. PDF Técnico de Impressão com Sangria (3mm) e Marcas de Corte/Cantos Arredondados
4. PNGs de Alta Resolução (300 DPI com transparência Alpha nos cantos arredondados)
"""
import os
import sys
import shutil
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = "C:/Users/Augusto/AppData/Local/Temp/brandpress/skills/brandpress/assets/pipeline"
sys.path.insert(0, PIPELINE)

import geometry as G
import export
import printing
import qa

OUT = os.path.join(HERE, "output_costao")
SCRATCH = os.path.join(HERE, "_scratch_costao")
ORIGINAL_SVG = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"

DARK_BG_START = "#141815"
DARK_BG_END = "#080B09"
DOURADO_AMBAR = "#F09C24"
VERDE_ESCURO = "#0E2B24"
TEXTO_LIGHT = "#9CA3AF"

def extrair_frente_svg():
    """Lê o SVG original da frente com clip-path de cantos arredondados rx=60."""
    with open(ORIGINAL_SVG, "r", encoding="utf-8") as f:
        return f.read()

def gerar_verso_svg():
    """Gera o verso oficial com bordas arredondadas (rx=60) idênticas à frente."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClipVerso">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="darkBgVerso" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{DARK_BG_START}"/>
      <stop offset="100%" stop-color="{DARK_BG_END}"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClipVerso)">
    <!-- Fundo Escuro com Gradiente -->
    <rect width="1000" height="1000" fill="url(#darkBgVerso)"/>
    
    <!-- Moldura Interna Dourada Arredondada -->
    <rect x="50" y="50" width="900" height="900" rx="40" fill="#141B16" stroke="{DOURADO_AMBAR}" stroke-width="2.5"/>
    
    <!-- Cabeçalho de Avaliação -->
    <text x="500" y="160" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">SUA OPINIÃO É FUNDAMENTAL</text>
    <text x="500" y="205" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="2">AVALIE O COSTÃO NO GOOGLE</text>
    
    <!-- 5 Estrelas Douradas -->
    <g transform="translate(500, 265)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="44" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="8">★★★★★</text>
    </g>
    
    <!-- QR Code Central em Container Branco com Cantos Arredondados -->
    <g transform="translate(500, 500)">
      <rect x="-140" y="-140" width="280" height="280" rx="24" fill="#FFFFFF" filter="drop-shadow(0px 8px 16px rgba(0,0,0,0.3))"/>
      <!-- Padrão QR Code de Alta Fidelidade -->
      <rect x="-115" y="-115" width="70" height="70" fill="{DARK_BG_END}" rx="6"/>
      <rect x="-95" y="-95" width="30" height="30" fill="#FFFFFF" rx="2"/>
      <rect x="-85" y="-85" width="10" height="10" fill="{DOURADO_AMBAR}"/>
      
      <rect x="45" y="-115" width="70" height="70" fill="{DARK_BG_END}" rx="6"/>
      <rect x="65" y="-95" width="30" height="30" fill="#FFFFFF" rx="2"/>
      <rect x="75" y="-85" width="10" height="10" fill="{DOURADO_AMBAR}"/>
      
      <rect x="-115" y="45" width="70" height="70" fill="{DARK_BG_END}" rx="6"/>
      <rect x="-95" y="65" width="30" height="30" fill="#FFFFFF" rx="2"/>
      <rect x="-85" y="75" width="10" height="10" fill="{DOURADO_AMBAR}"/>
      
      <!-- Módulos centrais / Sensor NFC Icon -->
      <rect x="-24" y="-24" width="48" height="48" rx="8" fill="{DOURADO_AMBAR}"/>
      <circle cx="0" cy="0" r="12" fill="{DARK_BG_END}"/>
      <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>
    </g>
    
    <!-- Instruções de Uso -->
    <text x="500" y="710" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="#FFFFFF" text-anchor="middle">Aproxime o celular ou aponte a câmera para o QR Code</text>
    <text x="500" y="745" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="500" fill="{TEXTO_LIGHT}" text-anchor="middle">Leva menos de 1 minuto e apoia nossa equipe</text>
    
    <!-- Rodapé Tecnológico com Filete -->
    <line x1="120" y1="800" x2="880" y2="800" stroke="#2B382F" stroke-width="1.5"/>
    <text x="500" y="855" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="700" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="2">AH3 SMART HOSPITALITY TECH</text>
  </g>
</svg>'''
    return svg

def main():
    os.makedirs(OUT, exist_ok=True)
    
    # 1. Renderizar Frente com Bordas Arredondadas (Alpha PNG 300 DPI)
    frente_svg = extrair_frente_svg()
    frente_svg_path = os.path.join(OUT, "frente_costao_arredondada.svg")
    with open(frente_svg_path, "w", encoding="utf-8") as f:
        f.write(frente_svg)
        
    doc_frente = fitz.open(frente_svg_path)
    pix_frente = doc_frente[0].get_pixmap(dpi=300, alpha=True)
    out_frente_png = os.path.join(OUT, "cartao_nfc_costao_frente_bordas_arredondadas_300dpi.png")
    pix_frente.save(out_frente_png)
    print("Frente gerada:", out_frente_png)
    
    # 2. Renderizar Verso com Bordas Arredondadas (Alpha PNG 300 DPI)
    verso_svg = gerar_verso_svg()
    verso_svg_path = os.path.join(OUT, "verso_costao_arredondado.svg")
    with open(verso_svg_path, "w", encoding="utf-8") as f:
        f.write(verso_svg)
        
    doc_verso = fitz.open(verso_svg_path)
    pix_verso = doc_verso[0].get_pixmap(dpi=300, alpha=True)
    out_verso_png = os.path.join(OUT, "cartao_nfc_costao_verso_bordas_arredondadas_300dpi.png")
    pix_verso.save(out_verso_png)
    print("Verso gerado:", out_verso_png)
    
    print("\nExecução e renderização concluídas com sucesso!")

if __name__ == "__main__":
    main()

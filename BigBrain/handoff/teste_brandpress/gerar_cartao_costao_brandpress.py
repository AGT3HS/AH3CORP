# -*- coding: utf-8 -*-
"""
Recriação do Cartão NFC Oficial de Teste (Costão do Santinho Resort 10x10cm)
utilizando o pipeline técnico gráfico do Brandpress com:
- BleedBox (106 x 106 mm) e TrimBox (100 x 100 mm)
- Vetorização pura de elementos e tipografia
- Renderização de Frente e Verso em PDF de alta qualidade e PNGs para chat
"""
import os
import sys
import shutil
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = "C:/Users/Augusto/AppData/Local/Temp/brandpress/skills/brandpress/assets/pipeline"
sys.path.insert(0, PIPELINE)

import geometry as G
import fonts
import export
import printing
import qa
from typography import Typeface

OUT = os.path.join(HERE, "output_costao")
FONTS_DIR = os.path.join(HERE, "fonts")
SCRATCH = os.path.join(HERE, "_scratch_costao")

# Paleta Oficial Costão do Santinho
VERDE_ESCURO = "#0E2B24"
DARK_BG_START = "#141815"
DARK_BG_END = "#080B09"
DOURADO_AMBAR = "#F09C24"
OFF_WHITE = "#F8F9FA"
TEXTO_ESCURO = "#111827"
TEXTO_MUTED = "#4B5563"
TEXTO_LIGHT = "#9CA3AF"
BORDA_DIV = "#E5E7EB"

FAMILY = "manrope"
WEIGHTS = (400, 500, 600, 700)

def gerar_frente_svg(cw, ch, sx, sy, sw, sh):
    """Gera a Frente Oficial do Cartão NFC Costão do Santinho adaptada com sangria gráfica."""
    # Escala proporcional de 1000x1000 para a área segura sw, sh (100x100 mm)
    scale = sw / 1000.0
    
    svg = f'''
    <defs>
      <linearGradient id="darkBgCostao" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{DARK_BG_START}"/>
        <stop offset="100%" stop-color="{DARK_BG_END}"/>
      </linearGradient>
    </defs>
    
    <!-- Fundo Total com Sangria (106x106 mm) -->
    <rect width="{cw}" height="{ch}" fill="{OFF_WHITE}"/>
    
    <!-- Bloco Superior Dark com Sangria no topo e laterais -->
    <path d="M0,0 L{cw},0 L{cw},{sy + 430*scale} Q{cw/2},{sy + 485*scale} 0,{sy + 430*scale} Z" fill="url(#darkBgCostao)"/>
    
    <g transform="translate({sx}, {sy}) scale({scale})">
      <!-- 1. IDENTIDADE / LOGO COSTÃO DO SANTINHO (VETOR LUXO) -->
      <g transform="translate(80, 140)">
        <path d="M 0 35 C 0 15, 15 0, 35 0 C 55 0, 70 15, 70 35 C 70 55, 55 70, 35 70 C 15 70, 0 55, 0 35 Z" fill="none" stroke="{DOURADO_AMBAR}" stroke-width="4"/>
        <path d="M 12 35 C 12 22, 22 12, 35 12 C 48 12, 58 22, 58 35" fill="none" stroke="{DOURADO_AMBAR}" stroke-width="3" stroke-linecap="round"/>
        <circle cx="35" cy="35" r="8" fill="{DOURADO_AMBAR}"/>
        
        <text x="90" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" letter-spacing="1">COSTÃO</text>
        <text x="90" y="54" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="{DOURADO_AMBAR}" letter-spacing="3">DO SANTINHO</text>
        <text x="90" y="72" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="500" fill="{TEXTO_LIGHT}" letter-spacing="1.5">RESORT ALL-INCLUSIVE</text>
      </g>
      
      <!-- 2. CLUSTER NFC COM ONDAS E PÍLULA DOURADA -->
      <g transform="translate(830, 95)">
        <!-- Ondas NFC -->
        <g stroke="{DOURADO_AMBAR}" stroke-width="6" stroke-linecap="round" fill="none" transform="translate(0, 40)">
          <circle cx="-25" cy="0" r="3.5" fill="{DOURADO_AMBAR}" stroke="none"/>
          <path d="M-12,-18 C-3,-9 -3,9 -12,18"/>
          <path d="M3,-30 C18,-15 18,15 3,30"/>
          <path d="M18,-42 C38,-21 38,21 18,42"/>
        </g>
        <!-- Pílula [ NFC ] -->
        <g transform="translate(0, 115)">
          <rect x="-44" y="-18" width="88" height="36" rx="18" fill="{DOURADO_AMBAR}"/>
          <text x="0" y="6" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="{DARK_BG_END}" text-anchor="middle" letter-spacing="1.5">NFC</text>
        </g>
        <text x="0" y="170" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
      </g>
      
      <!-- 3. CHAMADA: UM TOQUE LIBERA -->
      <g transform="translate(80, 520)">
        <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#6B7280" letter-spacing="3">UM TOQUE LIBERA</text>
      </g>
      
      <!-- 4. GRADE 2x2: OS 4 PILARES REAIS DO RESORT -->
      <!-- Item 1: SPA & Relax -->
      <g transform="translate(80, 565)">
        <circle cx="40" cy="40" r="40" fill="{VERDE_ESCURO}" fill-opacity="0.10"/>
        <g stroke="{VERDE_ESCURO}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
          <path d="M16 26 C16 12 6 8 2 18 C2 24 10 26 16 26 Z"/>
          <path d="M16 26 C16 12 26 8 30 18 C30 24 22 26 16 26 Z"/>
          <path d="M16 26 C11 16 13 6 16 3 C19 6 21 16 16 26 Z"/>
        </g>
        <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{TEXTO_ESCURO}">Costão SPA &amp; Relax</text>
        <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{TEXTO_MUTED}">Massagens, hidro e rituais</text>
      </g>
      
      <!-- Item 2: Shows & Programação -->
      <g transform="translate(520, 565)">
        <circle cx="40" cy="40" r="40" fill="{VERDE_ESCURO}" fill-opacity="0.10"/>
        <g stroke="{VERDE_ESCURO}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
          <rect x="3" y="6" width="26" height="23" rx="4"/>
          <line x1="3" y1="13" x2="29" y2="13"/>
          <line x1="9" y1="2" x2="9" y2="7"/>
          <line x1="23" y1="2" x2="23" y2="7"/>
          <circle cx="10" cy="19" r="1.5" fill="{VERDE_ESCURO}"/>
          <circle cx="16" cy="19" r="1.5" fill="{VERDE_ESCURO}"/>
          <circle cx="22" cy="19" r="1.5" fill="{VERDE_ESCURO}"/>
        </g>
        <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{TEXTO_ESCURO}">Shows &amp; Programação</text>
        <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{TEXTO_MUTED}">Agenda diária e atrações</text>
      </g>
      
      <!-- Item 3: Restaurantes & Bares -->
      <g transform="translate(80, 715)">
        <circle cx="40" cy="40" r="40" fill="{VERDE_ESCURO}" fill-opacity="0.10"/>
        <g stroke="{VERDE_ESCURO}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
          <path d="M5 3 L5 12 C5 15 8 17 11 17 L11 29"/>
          <line x1="11" y1="3" x2="11" y2="12"/>
          <path d="M17 3 L17 12 C17 15 14 17 11 17"/>
          <path d="M23 3 C27 8 27 15 24 18 L24 29"/>
        </g>
        <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{TEXTO_ESCURO}">Restaurantes &amp; Bares</text>
        <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{TEXTO_MUTED}">Cardápios, reservas e horários</text>
      </g>
      
      <!-- Item 4: Mapa & Guia Resort -->
      <g transform="translate(520, 715)">
        <circle cx="40" cy="40" r="40" fill="{VERDE_ESCURO}" fill-opacity="0.10"/>
        <g stroke="{VERDE_ESCURO}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
          <polygon points="3 7 11 3 21 7 29 3 29 25 21 29 11 25 3 29"/>
          <line x1="11" y1="3" x2="11" y2="25"/>
          <line x1="21" y1="7" x2="21" y2="29"/>
        </g>
        <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="{TEXTO_ESCURO}">Mapa &amp; Guia Resort</text>
        <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="{TEXTO_MUTED}">Wi-Fi, trilhas e arqueologia</text>
      </g>
      
      <!-- 5. RODAPÉ COM FILETE -->
      <g transform="translate(80, 890)">
        <line x1="0" y1="0" x2="840" y2="0" stroke="{BORDA_DIV}" stroke-width="1.5"/>
        <text x="0" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="#6B7280">Experiência All-Inclusive na Praia do Santinho.</text>
        <text x="840" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{TEXTO_ESCURO}" text-anchor="end">costao.com.br</text>
      </g>
    </g>
    '''
    return G.svg_doc(cw, ch, svg)

def gerar_verso_svg(cw, ch, sx, sy, sw, sh):
    """Gera o Verso Oficial do Cartão NFC Costão do Santinho para Avaliação Google."""
    scale = sw / 1000.0
    
    svg = f'''
    <defs>
      <linearGradient id="darkBgVerso" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{DARK_BG_START}"/>
        <stop offset="100%" stop-color="{DARK_BG_END}"/>
      </linearGradient>
    </defs>
    
    <!-- Fundo Total com Sangria -->
    <rect width="{cw}" height="{ch}" fill="url(#darkBgVerso)"/>
    
    <g transform="translate({sx}, {sy}) scale({scale})">
      <!-- Moldura Central Dourada -->
      <rect x="80" y="80" width="840" height="840" rx="36" fill="#18201A" stroke="{DOURADO_AMBAR}" stroke-width="2.5"/>
      
      <!-- Cabeçalho de Avaliação -->
      <text x="500" y="190" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">SUA OPINIÃO É FUNDAMENTAL</text>
      <text x="500" y="235" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="2">AVALIE O COSTÃO NO GOOGLE</text>
      
      <!-- Estrelas Douradas -->
      <g transform="translate(500, 290)">
        <text x="0" y="0" font-size="44" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="8">★★★★★</text>
      </g>
      
      <!-- QR Code Vetorial em Container Branco -->
      <g transform="translate(500, 520)">
        <rect x="-140" y="-140" width="280" height="280" rx="20" fill="#FFFFFF"/>
        <!-- Padrão QR Code -->
        <rect x="-115" y="-115" width="70" height="70" fill="{DARK_BG_END}"/>
        <rect x="-95" y="-95" width="30" height="30" fill="#FFFFFF"/>
        <rect x="45" y="-115" width="70" height="70" fill="{DARK_BG_END}"/>
        <rect x="65" y="-95" width="30" height="30" fill="#FFFFFF"/>
        <rect x="-115" y="45" width="70" height="70" fill="{DARK_BG_END}"/>
        <rect x="-95" y="65" width="30" height="30" fill="#FFFFFF"/>
        <!-- Módulos centrais -->
        <rect x="-20" y="-20" width="40" height="40" fill="{DOURADO_AMBAR}"/>
        <circle cx="0" cy="0" r="10" fill="{DARK_BG_END}"/>
      </g>
      
      <!-- Instruções -->
      <text x="500" y="720" font-family="'Plus Jakarta Sans', sans-serif" font-size="17" font-weight="600" fill="#FFFFFF" text-anchor="middle">Aproxime o celular ou aponte a câmera para o QR Code</text>
      <text x="500" y="755" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="500" fill="{TEXTO_LIGHT}" text-anchor="middle">Leva menos de 1 minuto e apoia nossa equipe</text>
      
      <!-- Rodapé -->
      <line x1="140" y1="810" x2="860" y2="810" stroke="#2D3A30" stroke-width="1.5"/>
      <text x="500" y="860" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="1">AH3 SMART HOSPITALITY TECH</text>
    </g>
    '''
    return G.svg_doc(cw, ch, svg)

def main():
    os.makedirs(OUT, exist_ok=True)
    export.scratch_dir(SCRATCH)
    
    print("[1/3] Montando Peça de Impressão Gráfica (100x100mm + 3mm Bleed)...")
    piece = printing.PrintPiece(100, 100, bleed=3)
    cw, ch = piece.canvas
    sx, sy, sw, sh = piece.safe_box
    
    front_svg = gerar_frente_svg(cw, ch, sx, sy, sw, sh)
    back_svg = gerar_verso_svg(cw, ch, sx, sy, sw, sh)
    
    piece.add(front_svg, SCRATCH)
    piece.add(back_svg, SCRATCH)
    
    pdf_path = os.path.join(OUT, "cartao_nfc_costao_do_santinho_100x100_press.pdf")
    piece.save(pdf_path)
    
    print("[2/3] Executando Validação de QA...")
    boxes = qa.pdf_boxes(pdf_path)
    checks = [
        ("TrimBox e BleedBox configurados", qa.has_trimbox(pdf_path), f"Folha: {boxes[0]['media_mm']} mm, TrimBox ativo: {boxes[0]['trimbox'] is not None}"),
        ("Páginas do arquivo", len(boxes) == 2, "2 páginas (Frente e Verso)"),
    ]
    print(qa.report(checks))
    
    print("[3/3] Renderizando PNGs em Alta Resolução (300 DPI)...")
    doc = fitz.open(pdf_path)
    png_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        out_png = os.path.join(OUT, f"costao_nfc_page_{i+1}_300dpi.png")
        pix.save(out_png)
        png_paths.append(out_png)
        print(" -> Gerado:", out_png)
        
    shutil.rmtree(SCRATCH, ignore_errors=True)
    print("\nExecução concluída com sucesso.")

if __name__ == "__main__":
    main()

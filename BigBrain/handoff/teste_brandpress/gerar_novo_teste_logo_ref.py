# -*- coding: utf-8 -*-
"""
Novo Teste com Logo Oficial de Referência e Bordas Arredondadas Visíveis
Utiliza a logo fornecida pelo usuário (C:/Users/Augusto/AppData/Local/hermes/profiles/maestro/attachments/costao-do-santinho-resort.png)
Gera:
1. Frente do Cartão NFC 10x10 com cantos arredondados (rx=60) + Logo Oficial de Referência + Mockup de visualização com cantos arredondados destacados sobre fundo neutro contrastante
2. Verso do Cartão NFC 10x10 com cantos arredondados (rx=60) + Container de Avaliação Google 5 Estrelas
3. Exportação em PNG de alta resolução (300 DPI) para validação visual imediata
"""
import os
import sys
import base64
from PIL import Image, ImageDraw, ImageFilter
import fitz

OUT = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/output_costao_ref"
os.makedirs(OUT, exist_ok=True)

LOGO_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/teste_brandpress/logo_referencia.png"

# Paleta Oficial
DARK_BG_START = "#141815"
DARK_BG_END = "#080B09"
DOURADO_AMBAR = "#F09C24"
VERDE_ESCURO = "#0E2B24"
OFF_WHITE = "#F8F9FA"
TEXTO_ESCURO = "#111827"
TEXTO_MUTED = "#4B5563"
TEXTO_LIGHT = "#9CA3AF"
BORDA_DIV = "#E5E7EB"

# Carregar Logo em Base64
with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

def gerar_frente_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClipFrente">
      <rect x="0" y="0" width="1000" height="1000" rx="70" ry="70"/>
    </clipPath>
    <linearGradient id="darkBgCostao" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{DARK_BG_START}"/>
      <stop offset="100%" stop-color="{DARK_BG_END}"/>
    </linearGradient>
  </defs>

  <!-- Grupo com Corte Arredondado Obrigatório rx=70 -->
  <g clip-path="url(#cardClipFrente)">
    <!-- Base Clara Inferior -->
    <rect width="1000" height="1000" fill="{OFF_WHITE}"/>

    <!-- Divisão Superior Escura com Curva Suave -->
    <path d="M0,0 L1000,0 L1000,430 Q500,485 0,430 Z" fill="url(#darkBgCostao)"/>

    <!-- A) LOGO OFICIAL DE REFERÊNCIA FORNECIDA (Topo Esquerdo) -->
    <g transform="translate(70, 95)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="340" height="110" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) CLUSTER NFC COM ONDAS E PÍLULA DOURADA (Topo Direito) -->
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

      <!-- Texto Instrução -->
      <text x="0" y="170" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: UM TOQUE LIBERA -->
    <g transform="translate(80, 520)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#6B7280" letter-spacing="3">UM TOQUE LIBERA</text>
    </g>

    <!-- D) GRADE 2x2: OS 4 PILARES REAIS DO RESORT -->
    <!-- Item 1: Spa & Relax -->
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

    <!-- E) RODAPÉ COM FILETE ANATÔMICO -->
    <g transform="translate(80, 890)">
      <line x1="0" y1="0" x2="840" y2="0" stroke="{BORDA_DIV}" stroke-width="1.5"/>
      <text x="0" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="#6B7280">Experiência All-Inclusive na Praia do Santinho.</text>
      <text x="840" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="{TEXTO_ESCURO}" text-anchor="end">costao.com.br</text>
    </g>
    
    <!-- Linha de Contorno / Borda Perimetral Sutil -->
    <rect x="1" y="1" width="998" height="998" rx="69" fill="none" stroke="#D1D5DB" stroke-width="2"/>
  </g>
</svg>'''
    return svg

def gerar_verso_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClipVerso">
      <rect x="0" y="0" width="1000" height="1000" rx="70" ry="70"/>
    </clipPath>
    <linearGradient id="darkBgVerso" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{DARK_BG_START}"/>
      <stop offset="100%" stop-color="{DARK_BG_END}"/>
    </linearGradient>
  </defs>

  <!-- Grupo com Corte Arredondado Obrigatório rx=70 -->
  <g clip-path="url(#cardClipVerso)">
    <!-- Fundo Total Escuro -->
    <rect width="1000" height="1000" fill="url(#darkBgVerso)"/>
    
    <!-- Moldura Interna Dourada Arredondada -->
    <rect x="50" y="50" width="900" height="900" rx="46" fill="#141B16" stroke="{DOURADO_AMBAR}" stroke-width="2.5"/>
    
    <!-- Logo de Referência no Verso (Topo) -->
    <g transform="translate(340, 85)">
      <image href="data:image/png;base64,{logo_b64}" x="0" y="0" width="320" height="85" preserveAspectRatio="xMidYMid meet"/>
    </g>
    
    <!-- Chamada de Avaliação -->
    <text x="500" y="210" font-family="'Plus Jakarta Sans', sans-serif" font-size="24" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">SUA OPINIÃO É FUNDAMENTAL</text>
    <text x="500" y="245" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="2">AVALIE O RESORT NO GOOGLE</text>
    
    <!-- 5 Estrelas Douradas -->
    <g transform="translate(500, 300)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="44" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="8">★★★★★</text>
    </g>
    
    <!-- QR Code Central em Container Branco com Cantos Arredondados -->
    <g transform="translate(500, 520)">
      <rect x="-135" y="-135" width="270" height="270" rx="24" fill="#FFFFFF"/>
      <!-- Módulos QR Code de Alta Fidelidade -->
      <rect x="-110" y="-110" width="68" height="68" fill="{DARK_BG_END}" rx="6"/>
      <rect x="-90" y="-90" width="28" height="28" fill="#FFFFFF" rx="2"/>
      <rect x="-80" y="-80" width="8" height="8" fill="{DOURADO_AMBAR}"/>
      
      <rect x="42" y="-110" width="68" height="68" fill="{DARK_BG_END}" rx="6"/>
      <rect x="62" y="-90" width="28" height="28" fill="#FFFFFF" rx="2"/>
      <rect x="72" y="-80" width="8" height="8" fill="{DOURADO_AMBAR}"/>
      
      <rect x="-110" y="42" width="68" height="68" fill="{DARK_BG_END}" rx="6"/>
      <rect x="-90" y="62" width="28" height="28" fill="#FFFFFF" rx="2"/>
      <rect x="-80" y="72" width="8" height="8" fill="{DOURADO_AMBAR}"/>
      
      <!-- Sensor NFC Icon Central -->
      <rect x="-24" y="-24" width="48" height="48" rx="8" fill="{DOURADO_AMBAR}"/>
      <circle cx="0" cy="0" r="12" fill="{DARK_BG_END}"/>
      <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>
    </g>
    
    <!-- Instruções de Uso -->
    <text x="500" y="715" font-family="'Plus Jakarta Sans', sans-serif" font-size="18" font-weight="600" fill="#FFFFFF" text-anchor="middle">Aproxime o celular ou aponte a câmera para o QR Code</text>
    <text x="500" y="750" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="500" fill="{TEXTO_LIGHT}" text-anchor="middle">Leva menos de 1 minuto e apoia nossa equipe</text>
    
    <!-- Rodapé Tecnológico com Filete -->
    <line x1="120" y1="800" x2="880" y2="800" stroke="#2B382F" stroke-width="1.5"/>
    <text x="500" y="855" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="700" fill="{DOURADO_AMBAR}" text-anchor="middle" letter-spacing="2">AH3 SMART HOSPITALITY TECH</text>
    
    <!-- Linha de Contorno / Borda Perimetral Sutil -->
    <rect x="1" y="1" width="998" height="998" rx="69" fill="none" stroke="{DOURADO_AMBAR}" stroke-width="2" stroke-opacity="0.4"/>
  </g>
</svg>'''
    return svg

def criar_mockup_com_fundo(png_card_path, out_mockup_path, bg_color=(235, 238, 242, 255)):
    """Coloca o cartão com cantos arredondados sobre um fundo de palco com sombra suave para evidenciar o raio de curvatura."""
    card = Image.open(png_card_path).convert("RGBA")
    cw, ch = card.size
    
    # Criar canvas maior para respiro (margem de 80px)
    margin = 80
    stage_w = cw + margin * 2
    stage_h = ch + margin * 2
    
    # Fundo do palco
    stage = Image.new("RGBA", (stage_w, stage_h), bg_color)
    
    # Sombra do cartão arredondado
    shadow_mask = card.split()[-1]
    shadow = Image.new("RGBA", (stage_w, stage_h), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (cw, ch), (15, 23, 42, 90))
    shadow_layer.putalpha(shadow_mask)
    
    # Aplicar desfoque na sombra
    shadow_layer_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(radius=24))
    stage.paste(shadow_layer_blurred, (margin + 4, margin + 14), shadow_layer_blurred)
    
    # Colar o cartão arredondado sobre a sombra
    stage.paste(card, (margin, margin), card)
    
    stage.convert("RGB").save(out_mockup_path, "PNG", quality=95)
    print("Mockup gerado:", out_mockup_path)

def main():
    # 1. Salvar SVGs
    frente_svg = gerar_frente_svg()
    frente_svg_path = os.path.join(OUT, "frente_costao_ref.svg")
    with open(frente_svg_path, "w", encoding="utf-8") as f:
        f.write(frente_svg)
        
    verso_svg = gerar_verso_svg()
    verso_svg_path = os.path.join(OUT, "verso_costao_ref.svg")
    with open(verso_svg_path, "w", encoding="utf-8") as f:
        f.write(verso_svg)
        
    # 2. Renderizar PNGs Alpha 300 DPI
    doc_f = fitz.open(frente_svg_path)
    pix_f = doc_f[0].get_pixmap(dpi=300, alpha=True)
    frente_raw_png = os.path.join(OUT, "frente_costao_alpha_300dpi.png")
    pix_f.save(frente_raw_png)
    
    doc_v = fitz.open(verso_svg_path)
    pix_v = doc_v[0].get_pixmap(dpi=300, alpha=True)
    verso_raw_png = os.path.join(OUT, "verso_costao_alpha_300dpi.png")
    pix_v.save(verso_raw_png)
    
    # 3. Gerar Mockups com Cantos Arredondados Perfeitamente Visíveis
    frente_mockup_png = os.path.join(OUT, "cartao_nfc_costao_frente_oficial_mockup.png")
    criar_mockup_com_fundo(frente_raw_png, frente_mockup_png, (241, 245, 249, 255))
    
    verso_mockup_png = os.path.join(OUT, "cartao_nfc_costao_verso_oficial_mockup.png")
    criar_mockup_com_fundo(verso_raw_png, verso_mockup_png, (241, 245, 249, 255))
    
    print("\nNovo teste finalizado com sucesso!")

if __name__ == "__main__":
    main()

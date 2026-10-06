import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Resolução de cada slide em pixels (proporção idêntica à referência Bewiki: 1920 x 1080)
W, H = 1920, 1080

# Paleta de Cores Premium - Costão do Santinho
NAVY_DEEP = (0, 37, 66)       # #002542 (Fundo Capa)
NAVY_CARD = (10, 48, 80)      # #0A3050 (Cards Capa)
GOLD = (248, 175, 53)         # #F8AF35 (Acento Ouro)
GOLD_LIGHT = (253, 240, 214)  # #FDF0D6 (Pílula suave)
RED_ACCENT = (172, 24, 46)    # #AC182E (Acento SPA L'Occitane)
BG_LIGHT = (244, 246, 248)    # #F4F6F8 (Fundo Páginas Internas)
BG_CARD = (255, 255, 255)     # #FFFFFF (Cards Internos)
INK = (13, 34, 54)            # #0D2236 (Texto Principal)
MUTED = (91, 107, 122)        # #5B6B7A (Texto Secundário)
LINE = (228, 233, 238)        # #E4E9EE (Bordas Sutis)

# Diretórios
OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_FINAL = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf"

# Fontes do Windows
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_header(draw, kicker_text, title_text, subtitle_text=None, is_dark=False):
    kicker_font = get_font(FONT_SANS_BOLD, 22)
    title_font = get_font(FONT_SERIF_BOLD, 52)
    sub_font = get_font(FONT_SANS, 24)

    k_color = GOLD if is_dark else NAVY_DEEP
    t_color = (255, 255, 255) if is_dark else INK
    s_color = (200, 215, 230) if is_dark else MUTED

    y = 80
    draw.text((100, y), kicker_text.upper(), font=kicker_font, fill=k_color)
    y += 40
    draw.text((100, y), title_text, font=title_font, fill=t_color)
    y += 75
    if subtitle_text:
        draw.text((100, y), subtitle_text, font=sub_font, fill=s_color)

def draw_footer(draw, page_num, total_pages=8, is_dark=False):
    f_font = get_font(FONT_SANS, 18)
    f_color = (150, 180, 205) if is_dark else MUTED
    
    # Rodapé Esquerdo
    left_txt = "Proposta · Cartões Inteligentes NFC Costão do Santinho"
    draw.text((100, H - 70), left_txt, font=f_font, fill=f_color)
    
    # Rodapé Direito
    right_txt = f"{page_num:02d} / {total_pages:02d}"
    bbox = draw.textbbox((0, 0), right_txt, font=f_font)
    w = bbox[2] - bbox[0]
    draw.text((W - 100 - w, H - 70), right_txt, font=f_font, fill=f_color)
    
    # Linha divisória
    line_col = (20, 60, 95) if is_dark else LINE
    draw.line([(100, H - 90), (W - 100, H - 90)], fill=line_col, width=1)

def render_svg_card_with_shadow(svg_path, target_size=600):
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    card_img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    card_img = card_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    # Cria sombra difusa
    pad = 60
    shadow_img = Image.new("RGBA", (target_size + pad * 2, target_size + pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle([pad + 10, pad + 25, pad + target_size - 10, pad + target_size + 25], radius=35, fill=(0, 0, 0, 90))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(25))
    
    # Cola cartão sobre a sombra
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

print("Setup helper script pronto!")

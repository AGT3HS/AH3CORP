import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# DESIGN TOKENS & SOBRETONS (COSTÃO DO SANTINHO)
# ==============================================================================
# Fundos e Sobretons
BG_CREAM = (248, 246, 240)       # #F8F6F0 (Off-white / Creme editorial nobre)
BG_LIGHT_TINT = (240, 243, 246)  # #F0F3F6 (Sobretom azulado suave para alternância)
BG_DARK = (0, 37, 66)            # #002542 (Azul Marinho Nobre Capa)
BG_DARK_MID = (24, 52, 80)       # #183450 (Sobretom escuro)

# Cores dos Cards & Linhas
CARD_WHITE = (255, 255, 255)     # #FFFFFF (Cards com elevação)
CARD_WARM = (252, 250, 246)      # #FCFAF6 (Cards com sobretom quente)
BORDER_SUBTLE = (226, 230, 235)  # #E2E6EB (Borda ultrafina)
BORDER_WARM = (235, 230, 220)    # #EBE6DC

# Cores Institucionais
NAVY = (0, 43, 74)               # #002B4A (Petróleo Nobre)
NAVY_LIGHT = (44, 65, 89)        # #2C4159
GOLD = (248, 175, 53)            # #F8AF35 (Âmbar Ouro)
GOLD_MUTED = (212, 145, 30)      # #D4911E
GOLD_BG = (253, 240, 214)        # #FDF0D6 (Pílula suave)
RED_SPA = (172, 24, 46)          # #AC182E (Acento SPA L'Occitane)
GREEN_VAL = (30, 130, 76)        # #1E824C (Verde Sucesso/Google)
BLUE_GOOGLE = (26, 115, 232)     # #1A73E8 (Azul Google Oficial)

# Tipografia
TEXT_DARK = (13, 34, 54)         # #0D2236 (Títulos e ênfase)
TEXT_BODY = (40, 55, 70)         # #283746 (Corpo com alto contraste)
TEXT_MUTED = (95, 110, 125)      # #5F6E7D (Descrições)
TEXT_LIGHT = (255, 255, 255)
TEXT_LIGHT_MUTED = (195, 212, 230)

OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_FINAL = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf"

FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_shadow_card(draw_base, img_base, bbox, radius=20, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE, shadow_alpha=35, shadow_blur=22, shadow_offset=(0, 12)):
    """Desenha um card elegante com sombra difusa suave e sobretons realistas."""
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    pad = shadow_blur * 2
    
    # Criar camada de sombra
    s_img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    
    ox, oy = shadow_offset
    sx1 = pad + ox
    sy1 = pad + oy
    sx2 = sx1 + w
    sy2 = sy1 + h
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(0, 20, 40, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Colar sombra no fundo
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    
    # Desenhar o card sólido por cima com borda fina
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False, kicker_color=None):
    k_color = kicker_color if kicker_color else (GOLD if is_dark else NAVY)
    t_color = TEXT_LIGHT if is_dark else TEXT_DARK
    s_color = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    y = 75
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 18), fill=k_color)
    y += 34
    draw.text((100, y), title, font=get_font(FONT_SERIF_BOLD, 46), fill=t_color)
    y += 62
    if subtitle:
        # Permite quebras de linha em subtitles
        lines = subtitle.split("\n")
        for line in lines:
            draw.text((100, y), line, font=get_font(FONT_SANS, 21), fill=s_color)
            y += 30

def draw_footer(draw, page_num, is_dark=False):
    f_color = (130, 165, 195) if is_dark else TEXT_MUTED
    line_col = (25, 65, 100) if is_dark else BORDER_SUBTLE
    
    draw.line([(100, H - 75), (W - 100, H - 75)], fill=line_col, width=1)
    draw.text((100, H - 58), "Proposta · Cartões NFC Costão do Santinho", font=get_font(FONT_SANS, 16), fill=f_color)
    draw.text((W - 130, H - 58), f"{page_num}", font=get_font(FONT_SANS_BOLD, 18), fill=f_color)

def render_svg_card_with_shadow(svg_path, target_size=580):
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    mode = "RGBA" if pix.alpha else "RGB"
    card_img = Image.frombytes(mode, [pix.width, pix.height], pix.samples).convert("RGBA")
    card_img = card_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    pad = 80
    shadow_img = Image.new("RGBA", (target_size + pad * 2, target_size + pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle([pad + 15, pad + 35, pad + target_size - 15, pad + target_size + 35], radius=40, fill=(0, 15, 35, 120))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(32))
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

print("Setup completed successfully.")

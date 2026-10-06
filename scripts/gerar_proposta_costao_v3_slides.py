import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pymupdf
import math

from gerar_proposta_costao_v3 import (
    W, H, BG_CREAM, BG_LIGHT_TINT, BG_DARK, BG_DARK_MID, CARD_WHITE, CARD_WARM, 
    BORDER_SUBTLE, NAVY, NAVY_LIGHT, GOLD, GOLD_BG, GOLD_MUTED, RED_SPA, BLUE_GOOGLE,
    TEXT_DARK, TEXT_BODY, TEXT_MUTED, TEXT_LIGHT, TEXT_LIGHT_MUTED,
    FONT_SANS, FONT_SANS_BOLD, FONT_SERIF, FONT_SERIF_BOLD, get_font,
    draw_shadow_card, draw_header, draw_footer, render_svg_card_with_shadow, OUTPUT_DIR
)

outputs_dir = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"

# ==========================================
# SLIDE 1: CAPA PREMIUM
# ==========================================
def build_slide_1():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Circulo de decoração de fundo
    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=BG_DARK_MID)

    # Capa Editorial
    draw.text((120, H//2 - 200), "PROPOSTA COMERCIAL", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H//2 - 140), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)
    draw.text((120, H//2 - 50), "para a experiência", font=get_font(FONT_SERIF, 68), fill=TEXT_LIGHT)
    draw.text((120, H//2 + 40), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)

    draw.text((120, H//2 + 150), "Toda a infraestrutura, serviços e gastronomia do resort", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)
    draw.text((120, H//2 + 185), "acessíveis em um toque. Sempre atualizados.", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)

    # Rodapé institucional
    draw.text((120, H - 120), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H - 85), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 18), fill=TEXT_LIGHT_MUTED)

    # Mockup Físico com sombra pesada (direita)
    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    try:
        card_rendered = render_svg_card_with_shadow(svg_path, target_size=650)
        img.paste(card_rendered, (W - 850, 160), card_rendered)
    except:
        draw.rectangle((W-800, 200, W-150, 850), fill=(80,80,80))

    return img

# ==========================================
# SLIDE 8: AVALIAÇÕES GOOGLE (O Core Value Prop da Bewiki ref)
# ==========================================
def build_slide_8():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    kicker_txt = "O FOCO DO NOSSO SERVIÇO"
    title_txt = "Estadia melhor,\nmais avaliações,\nmais visibilidade."
    sub_txt = ("Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito\n"
               "a avaliar o hotel no Google no momento exato de encantamento. Mais avaliações \n"
               "recentes e notas altas ajudam o Costão a dominar as buscas em Florianópolis.")
    
    draw_header(draw, kicker_txt, title_txt, sub_txt, kicker_color=NAVY)
    draw_footer(draw, 5)

    # ==========================
    # CARD GOOGLE (UI Replica Bewiki)
    # --------------------------
    mockup_box = [W - 550, 190, W - 100, 480]
    draw_shadow_card(draw, img, mockup_box, radius=24, bg_color=CARD_WHITE)
    mx, my = mockup_box[0], mockup_box[1]
    
    # Faixa colorida do Google (azul, vermelho, amarelo, verde)
    gw = (mockup_box[2] - mockup_box[0]) / 4
    draw.rectangle([mx, my, mx+gw, my+6], fill=(66, 133, 244))      # Blue
    draw.rectangle([mx+gw, my, mx+gw*2, my+6], fill=(234, 67, 53))   # Red
    draw.rectangle([mx+gw*2, my, mx+gw*3, my+6], fill=(251, 188, 5)) # Yellow
    draw.rectangle([mx+gw*3, my, mx+gw*4, my+6], fill=(52, 168, 83)) # Green

    # Header Card
    draw.text((mx + 40, my + 45), "G", font=get_font(FONT_SANS_BOLD, 22), fill=(66, 133, 244)) # Logo Google stub
    draw.text((mx + 75, my + 45), "Avaliação Google", font=get_font(FONT_SANS_BOLD, 20), fill=TEXT_DARK)
    
    draw.text((mx + 40, my + 95), "Gostou da sua estadia?", font=get_font(FONT_SERIF_BOLD, 30), fill=TEXT_DARK)
    draw.text((mx + 40, my + 145), "Avalie o Costão no Google. Leva menos", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
    draw.text((mx + 40, my + 170), "de 1 minuto e ajuda outros hóspedes.", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
    
    # 5 stars
    stars_txt = "★ ★ ★ ★ ★"
    draw.text((mx + 40, my + 210), stars_txt, font=get_font(FONT_SANS_BOLD, 28), fill=GOLD)
    
    # CTA button
    btn_box = [mx + 220, my + 210, mx + 410, my + 250]
    draw.rounded_rectangle(btn_box, radius=12, fill=BLUE_GOOGLE)
    draw.text((btn_box[0] + 25, btn_box[1] + 9), "Avaliar no Google", font=get_font(FONT_SANS_BOLD, 14), fill=TEXT_LIGHT)


    # ==========================
    # FILEIRA DE 4 CARDS INFERIORES (Workflow)
    # --------------------------
    card_w = (W - 200 - 90) // 4  # Margem 100 dir/esq, 3 gaps de 30
    card_h = 320
    cy = 580
    cx = 100
    
    workflow = [
        ("Estadia\nmelhor", "Wi-Fi, mapa, horários e\nserviços a um toque:\nmenos atrito e mais\nautonomia para o hóspede.", NAVY),
        ("Convite\ncerto", "A página do cartão finaliza\ncom o botão 'Avaliar no\nGoogle' após solucionar a\ndúvida do hóspede.", GOLD_MUTED),
        ("Mais\navaliações", "Hóspedes satisfeitos\ncom a rapidez avaliam em\nmenos de 1 minuto, direto\ndo próprio navegador.", GOLD),
        ("Mais\nranking", "Volume e notas recentes\npesam diretamente na\nposição orgânica do\nhotel nas buscas locais.", NAVY)
    ]
    
    enum_font = get_font(FONT_SANS_BOLD, 20)
    tit_font = get_font(FONT_SERIF_BOLD, 28)
    des_font = get_font(FONT_SANS, 17)
    
    for idx, (titulo, desc, c_color) in enumerate(workflow):
        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=16, bg_color=CARD_WHITE)
        
        # Bolinha enumeradora
        draw.ellipse([cx + 35, cy + 40, cx + 75, cy + 80], fill=c_color)
        draw.text((cx + 50, cy + 48), f"{idx+1}", font=enum_font, fill=TEXT_LIGHT)
        
        # Texto
        lines_t = titulo.split("\n")
        ty = cy + 110
        for lt in lines_t:
            draw.text((cx + 35, ty), lt, font=tit_font, fill=TEXT_DARK)
            ty += 34
        
        ty += 15
        lines_d = desc.split("\n")
        for ld in lines_d:
            draw.text((cx + 35, ty), ld, font=des_font, fill=TEXT_MUTED)
            ty += 24
            
        cx += card_w + 30

    return img

print("Slide functions defined.")

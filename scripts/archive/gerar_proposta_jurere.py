import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# DESIGN TOKENS & PALETA DE CORES (JURERÊ BEACH VILLAGE)
# ==============================================================================
# Identidade Oficial: Turquesa Oceânico #4DA2AD / #276B75, Areia Nobre #FAF8F5, Âmbar Solar #E8A825
BG_CREAM = (250, 248, 245)       # #FAF8F5 (Areia Nobre / Off-white acolhedor)
BG_LIGHT_TINT = (242, 247, 248)  # #F2F7F8 (Toque de brisa marinha suave)
BG_DARK = (10, 30, 54)           # #0A1E36 (Navy Noturno / Mar Profundo Jurerê)
BG_DARK_MID = (18, 48, 76)       # #12304C (Sobretom marinho)

# Cores dos Cards & Linhas
CARD_WHITE = (255, 255, 255)     # #FFFFFF (Cards com elevação)
CARD_WARM = (253, 251, 247)      # #FDFBF7 (Cards com sobretom areia)
BORDER_SUBTLE = (225, 232, 236)  # #E1E8EC (Borda ultrafina)
BORDER_WARM = (235, 230, 220)    # #EBE6DC

# Cores Institucionais Jurerê Beach Village
TURQUOISE = (77, 162, 173)       # #4DA2AD (Cor-Mãe Oficial)
TURQUOISE_DARK = (39, 107, 117)  # #276B75 (Turquesa Oceânico Profundo)
AMBER_GOLD = (232, 168, 37)      # #E8A825 (Âmbar Solar de Ativação NFC)
AMBER_MUTED = (200, 140, 25)     # #C88C19
AMBER_BG = (254, 246, 230)       # #FEF6E6 (Pílula e destaque suave)
BLUE_GOOGLE = (26, 115, 232)     # #1A73E8 (Azul Google Oficial)

# Tipografia
TEXT_DARK = (18, 24, 26)         # #12181A (Obsidian Petróleo)
TEXT_BODY = (45, 58, 68)         # #2D3A44 (Corpo de texto)
TEXT_MUTED = (90, 101, 119)      # #5A6577 (Descrições e legendas)
TEXT_LIGHT = (255, 255, 255)
TEXT_LIGHT_MUTED = (205, 220, 230)

OUTPUT_DIR = "saida/proposta_jurere"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PDF_FINAL = "saida/proposta_jurere/Proposta_Comercial_Cartoes_NFC_Jurere_Beach_Village.pdf"
SVG_CARD_PATH = "saida/proposta_jurere/01_modelo_classico_cor_mae_jurere.svg"

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
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    pad = shadow_blur * 2
    
    s_img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    
    ox, oy = shadow_offset
    sx1 = pad + ox
    sy1 = pad + oy
    sx2 = sx1 + w
    sy2 = sy1 + h
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(10, 30, 50, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False, kicker_color=None):
    k_color = kicker_color if kicker_color else (AMBER_GOLD if is_dark else TURQUOISE_DARK)
    t_color = TEXT_LIGHT if is_dark else TEXT_DARK
    s_color = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    y = 75
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 18), fill=k_color)
    y += 38
    
    t_lines = title.split("\n")
    for tl in t_lines:
        draw.text((100, y), tl, font=get_font(FONT_SERIF_BOLD, 46), fill=t_color)
        y += 56
        
    y += 20
    if subtitle:
        lines = subtitle.split("\n")
        for line in lines:
            draw.text((100, y), line, font=get_font(FONT_SANS, 21), fill=s_color)
            y += 32

def draw_footer(draw, page_num, total_pages=8, is_dark=False):
    f_color = (130, 165, 185) if is_dark else TEXT_MUTED
    line_col = (20, 55, 85) if is_dark else BORDER_SUBTLE
    
    draw.line([(100, H - 75), (W - 100, H - 75)], fill=line_col, width=1)
    draw.text((100, H - 58), "Proposta · Cartões NFC Jurerê Beach Village", font=get_font(FONT_SANS, 16), fill=f_color)
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
    sdraw.rounded_rectangle([pad + 15, pad + 35, pad + target_size - 15, pad + target_size + 35], radius=40, fill=(0, 20, 40, 120))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(32))
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

# ==============================================================================
# SLIDE 1: CAPA
# ==============================================================================
def build_slide_1():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Detalhe geométrico de fundo
    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=BG_DARK_MID)

    draw.text((120, H//2 - 200), "PROPOSTA COMERCIAL", font=get_font(FONT_SANS_BOLD, 20), fill=AMBER_GOLD)
    draw.text((120, H//2 - 140), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)
    draw.text((120, H//2 - 50), "para a experiência", font=get_font(FONT_SERIF, 68), fill=TEXT_LIGHT)
    draw.text((120, H//2 + 40), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)

    draw.text((120, H//2 + 150), "Informação do resort, restaurantes, SPA e", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)
    draw.text((120, H//2 + 185), "programação a um toque do celular — sempre atualizados.", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)

    draw.text((120, H - 120), "Preparada para: Jurerê Beach Village", font=get_font(FONT_SANS_BOLD, 20), fill=AMBER_GOLD)
    draw.text((120, H - 85), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 18), fill=TEXT_LIGHT_MUTED)

    try:
        card_rendered = render_svg_card_with_shadow(SVG_CARD_PATH, target_size=650)
        img.paste(card_rendered, (W - 850, 160), card_rendered)
    except Exception as e:
        print("Card error slide 1:", e)
        draw.rectangle((W-800, 200, W-150, 850), fill=(80,80,80))

    return img

# ==============================================================================
# SLIDE 2: O PONTO DE PARTIDA
# ==============================================================================
def build_slide_2():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Mais tempo para o que importa.",
                "O hóspede chega com perguntas simples: qual é a senha do Wi-Fi? O que tem de programação\nhoje? Onde fica o restaurante? O SPA está aberto?", kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 2)

    card_w = (W - 200 - 60) // 3
    card_h = 560
    card_y = 280
    gap = 30

    colunas = [
        ("Hoje",
         "Informação espalhada entre\nrecepção, placas e papéis\nimpressos que envelhecem rápido.",
         TURQUOISE_DARK),
        ("O custo",
         "Equipe respondendo as mesmas\nperguntas e hóspede sem achar o\nque precisa.",
         AMBER_MUTED),
        ("A proposta",
         "Um cartão NFC no quarto: um toque\nabre tudo, atualizado.",
         AMBER_GOLD)
    ]

    for i, (titulo, desc, cor_top) in enumerate(colunas):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 12], radius=6, fill=cor_top)
        draw.text((cx + 45, card_y + 60), titulo, font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = card_y + 140
        for l in lines:
            draw.text((cx + 45, ly), l, font=get_font(FONT_SANS, 22), fill=TEXT_BODY)
            ly += 36

    return img

# ==============================================================================
# SLIDE 3: COMO FUNCIONA
# ==============================================================================
def build_slide_3():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "COMO FUNCIONA", "Três passos, nenhum aplicativo para baixar.",
                "Tecnologia nativa e intuitiva: basta aproximar o smartphone para acessar todo o resort.", kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 3)

    card_w = (W - 200 - 60) // 3
    card_h = 440
    card_y = 280
    gap = 30

    passos = [
        ("1", "Aproxime", "O hóspede encosta o celular no cartão. O\nNFC funciona na maioria dos\nsmartphones atuais.", TURQUOISE_DARK),
        ("2", "Abra", "A página do resort abre direto no\nnavegador: restaurantes, SPA,\nprogramação, mapa e Wi-Fi.", AMBER_MUTED),
        ("3", "Sempre atual", "O resort muda uma informação uma única\nvez e todos os cartões já mostram a\nversão nova.", AMBER_GOLD)
    ]

    for i, (num, titulo, desc, cor) in enumerate(passos):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20, bg_color=CARD_WHITE)

        draw.ellipse([cx + 45, card_y + 45, cx + 105, card_y + 105], fill=cor)
        draw.text((cx + 66, card_y + 57), num, font=get_font(FONT_SANS_BOLD, 32), fill=TEXT_LIGHT)

        draw.text((cx + 45, card_y + 140), titulo, font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = card_y + 210
        for l in lines:
            draw.text((cx + 45, ly), l, font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
            ly += 32

    cbox = [100, 770, W - 100, 870]
    draw_shadow_card(draw, img, cbox, radius=16, bg_color=CARD_WARM, border_color=BORDER_WARM)
    draw.text((140, 805), "O segredo: o cartão guarda só um link. O conteúdo vive na página — por isso nunca fica desatualizado.",
              font=get_font(FONT_SANS_BOLD, 22), fill=TURQUOISE_DARK)

    return img

# ==============================================================================
# SLIDE 4: CARTÃO · JURERÊ BEACH VILLAGE
# ==============================================================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO · JURERÊ BEACH VILLAGE", "Para quem está hospedado.",
                "Colocado no quarto e na recepção, libera num toque o que o hóspede mais procura.", kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 4)

    left_w = 1050
    cw = (left_w - 40) // 2
    ch = 240
    start_y = 280

    servicos = [
        ("Restaurantes & Bares", "ZPerry Restaurante, culinária contemporânea,\nbuffet de café da manhã e adega selecionada.", TURQUOISE_DARK),
        ("Serviço de Praia & Piscina", "Atendimento pé na areia com espreguiçadeiras,\ndrinks tropicais e toalhas de praia.", AMBER_MUTED),
        ("SPA & Relax", "Massagens terapêuticas, hidromassagem aquecida,\nsaunas seca e a vapor.", AMBER_GOLD),
        ("Concierge & Wi-Fi", "Rede e senha de alta velocidade, agendamento de\npasseios e programação diária.", TURQUOISE)
    ]

    for idx, (tit, desc, cor) in enumerate(servicos):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (cw + 40)
        cy = start_y + row * (ch + 35)

        bbox = [cx, cy, cx + cw, cy + ch]
        draw_shadow_card(draw, img, bbox, radius=18, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, cy + 25, cx + 8, cy + ch - 25], radius=4, fill=cor)
        draw.text((cx + 35, cy + 35), tit, font=get_font(FONT_SERIF_BOLD, 26), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = cy + 85
        for l in lines:
            draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
            ly += 28

    try:
        card_rendered = render_svg_card_with_shadow(SVG_CARD_PATH, target_size=560)
        img.paste(card_rendered, (W - 680, 260), card_rendered)
    except Exception as e:
        print("Card error slide 4:", e)

    draw.text((W - 640, 850), "Arte do cartão 10×10 cm — Modelo Clássico Cor-Mãe.", font=get_font(FONT_SANS_BOLD, 17), fill=TURQUOISE_DARK)

    return img

# ==============================================================================
# SLIDE 5: O QUE O HÓSPEDE VÊ (INTERFACE MOBILE-FIRST JURERÊ BEACH VILLAGE)
# ==============================================================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw.text((100, 80), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 18), fill=TURQUOISE_DARK)
    draw.text((100, 120), "Uma página única", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)
    draw.text((100, 175), "do resort.", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)

    draw.text((100, 255), "A página do cartão apresenta restaurantes e", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 290), "bares, SPA, programação de lazer, serviço", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 325), "de praia, além do Wi-Fi de alta velocidade.", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)

    callout_box = [100, 395, 660, 610]
    draw_shadow_card(draw, img, callout_box, radius=18, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE)
    draw.rounded_rectangle([100, 395, 108, 610], radius=4, fill=AMBER_GOLD)

    draw.text((135, 425), "Novo: convite para avaliar no Google", font=get_font(FONT_SANS_BOLD, 22), fill=TURQUOISE_DARK)
    draw.text((135, 465), "Ao fim da página, o hóspede satisfeito toca em", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 495), "'Avaliar no Google' e deixa sua nota em menos", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 525), "de 1 minuto — transformando encantamento em", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 555), "visibilidade orgânica.", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)

    draw.text((100, 650), "Um canal único para divulgar o que o resort quiser,", font=get_font(FONT_SANS_BOLD, 20), fill=TURQUOISE_DARK)
    draw.text((100, 680), "quando quiser. Sem limites de atualização.", font=get_font(FONT_SANS_BOLD, 20), fill=TURQUOISE_DARK)

    draw_footer(draw, 5)

    mockup_w = 340
    mockup_h = 700
    start_mx = 740
    gap_m = 40
    my = 110

    telas = [
        {
            "header": "JURERÊ BEACH VILLAGE", "kicker": "BEM-VINDO AO RESORT", "bg": TURQUOISE_DARK,
            "cards": [
                ("WI-FI GUEST", "Rede: JurereBeach_Guest\nSenha disponível no quarto"),
                ("ZPERRY RESTAURANTE", "Café: 06h30 às 10h30\nAlmoço e Jantar contemporâneo"),
                ("SERVIÇO DE PRAIA", "Atendimento exclusivo na areia\nEspreguiçadeiras e drinks"),
                ("CHECK-IN / OUT", "Check-in: 15h · Check-out: 11h")
            ]
        },
        {
            "header": "SPA & BEM-ESTAR", "kicker": "RELAXE EM JURERÊ", "bg": (28, 77, 85),
            "cards": [
                ("MASSAGENS & RITUAIS", "Terapias relaxantes e hidromassagem\nAgende pelo WhatsApp"),
                ("PISCINAS & SAUNAS", "Piscinas climatizadas adulto e infantil\nSauna seca e a vapor"),
                ("PROGRAMAÇÃO DE LAZER", "Recreação infantil e atividades\nConfira os horários diários")
            ]
        },
        {
            "header": "AGENDA & AVALIAÇÃO", "kicker": "HOJE NO RESORT", "bg": TURQUOISE_DARK,
            "cards": [
                ("17h · SUNSET NA PRAIA", "Deck da piscina · Música ao vivo"),
                ("19h · DEGUSTAÇÃO DE VINHOS", "Restaurante ZPerry · Adega"),
                ("20h30 · JANTAR ESPECIAL", "Menu à la carte do Chef"),
                ("★ ★ ★ ★ ★", "Avaliar no Google\nAjude outros viajantes!")
            ]
        }
    ]

    for col_idx, t in enumerate(telas):
        tx = start_mx + col_idx * (mockup_w + gap_m)
        bbox = [tx, my, tx + mockup_w, my + mockup_h]
        draw_shadow_card(draw, img, bbox, radius=32, bg_color=CARD_WHITE)

        draw.rounded_rectangle([tx + 8, my + 8, tx + mockup_w - 8, my + 115], radius=24, fill=t["bg"])
        draw.text((tx + 25, my + 30), t["kicker"], font=get_font(FONT_SANS_BOLD, 12), fill=AMBER_GOLD)
        draw.text((tx + 25, my + 55), t["header"], font=get_font(FONT_SERIF_BOLD, 18), fill=TEXT_LIGHT)

        cy = my + 130
        for ctitle, cdesc in t["cards"]:
            card_box_h = 105 if "\n" in cdesc else 85
            is_stars = "★" in ctitle
            box_bg = AMBER_BG if is_stars else BG_CREAM

            draw.rounded_rectangle([tx + 15, cy, tx + mockup_w - 15, cy + card_box_h], radius=14, fill=box_bg)

            if is_stars:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 20), fill=AMBER_GOLD)
                draw.text((tx + 30, cy + 45), cdesc.split("\n")[0], font=get_font(FONT_SANS_BOLD, 14), fill=TURQUOISE_DARK)
            else:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 13), fill=TURQUOISE_DARK)
                lines = cdesc.split("\n")
                ly = cy + 40
                for l in lines:
                    draw.text((tx + 30, ly), l, font=get_font(FONT_SANS, 13), fill=TEXT_MUTED)
                    ly += 18

            cy += card_box_h + 12

    return img

# ==============================================================================
# SLIDE 6: O FOCO DO NOSSO SERVIÇO (AVALIAÇÕES GOOGLE)
# ==============================================================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    kicker_txt = "O FOCO DO NOSSO SERVIÇO"
    title_txt = "Estadia melhor,\nmais avaliações,\nmais visibilidade."
    sub_txt = ("Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito\n"
               "a avaliar o resort no Google. Mais avaliações recentes e boas notas ajudam\n"
               "o Jurerê Beach Village a ser encontrado por quem busca onde ficar.")

    draw_header(draw, kicker_txt, title_txt, sub_txt, kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 6)

    mockup_box = [W - 550, 190, W - 100, 480]
    draw_shadow_card(draw, img, mockup_box, radius=24, bg_color=CARD_WHITE)
    mx, my = mockup_box[0], mockup_box[1]

    gw = (mockup_box[2] - mockup_box[0]) / 4
    draw.rectangle([mx, my, mx + gw, my + 6], fill=(66, 133, 244))
    draw.rectangle([mx + gw, my, mx + gw * 2, my + 6], fill=(234, 67, 53))
    draw.rectangle([mx + gw * 2, my, mx + gw * 3, my + 6], fill=(251, 188, 5))
    draw.rectangle([mx + gw * 3, my, mx + gw * 4, my + 6], fill=(52, 168, 83))

    draw.text((mx + 40, my + 45), "G", font=get_font(FONT_SANS_BOLD, 22), fill=(66, 133, 244))
    draw.text((mx + 75, my + 45), "Avaliação Google", font=get_font(FONT_SANS_BOLD, 20), fill=TEXT_DARK)

    draw.text((mx + 40, my + 95), "Gostou da sua estadia?", font=get_font(FONT_SERIF_BOLD, 30), fill=TEXT_DARK)
    draw.text((mx + 40, my + 145), "Avalie o Jurerê Beach Village no Google.", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
    draw.text((mx + 40, my + 170), "Leva menos de 1 minuto e ajuda outros viajantes.", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)

    draw.text((mx + 40, my + 210), "★ ★ ★ ★ ★", font=get_font(FONT_SANS_BOLD, 28), fill=AMBER_GOLD)

    btn_box = [mx + 220, my + 210, mx + 410, my + 250]
    draw.rounded_rectangle(btn_box, radius=12, fill=BLUE_GOOGLE)
    draw.text((btn_box[0] + 25, btn_box[1] + 9), "Avaliar no Google", font=get_font(FONT_SANS_BOLD, 14), fill=TEXT_LIGHT)

    card_w = (W - 200 - 90) // 4
    card_h = 320
    cy = 580
    cx = 100

    workflow = [
        ("Estadia\nmelhor", "Guia, programação e serviços a\num toque: menos atrito para o\nhóspede.", TURQUOISE_DARK),
        ("Convite\ncerto", "A página do cartão traz o botão\n'Avaliar no Google' no fim da\nvisita.", AMBER_MUTED),
        ("Mais\navaliações", "Hóspedes satisfeitos avaliam em\nmenos de 1 minuto, direto do\ncelular.", AMBER_GOLD),
        ("Mais\nranking", "Volume e nota das avaliações\npesam na posição do resort no\nGoogle.", TURQUOISE_DARK)
    ]

    enum_font = get_font(FONT_SANS_BOLD, 20)
    tit_font = get_font(FONT_SERIF_BOLD, 28)
    des_font = get_font(FONT_SANS, 17)

    for idx, (titulo, desc, c_color) in enumerate(workflow):
        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=16, bg_color=CARD_WHITE)

        draw.ellipse([cx + 35, cy + 40, cx + 75, cy + 80], fill=c_color)
        draw.text((cx + 50, cy + 48), f"{idx + 1}", font=enum_font, fill=TEXT_LIGHT)

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

# ==============================================================================
# SLIDE 7: POR QUE VALE PARA O HOTEL
# ==============================================================================
def build_slide_7():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O HOTEL", "Menos atrito, mais experiência.",
                "Benefícios práticos e imediatos para a operação e autoridade do Jurerê Beach Village.", kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 7)

    card_w = (W - 200 - 40) // 2
    card_h = 240
    start_y = 280

    beneficios = [
        ("Informação sempre correta",
         "Mudou a programação? A senha do Wi-Fi?\nEdita uma única vez, todos os cartões refletem na hora.", TURQUOISE_DARK),
        ("Recepção mais leve",
         "Perguntas repetidas passam a ser respondidas pelo próprio cartão,\nliberando a equipe para um atendimento mais acolhedor.", AMBER_MUTED),
        ("Percepção de modernidade",
         "Um gesto simples que o hóspede nota, elogia e comenta,\nalinhado ao perfil sofisticado de Jurerê.", AMBER_GOLD),
        ("Mais descoberta no resort",
         "Restaurantes, SPA, passeios e programação aparecem com clareza\npara quem já está dentro do hotel.", TURQUOISE)
    ]

    for idx, (tit, desc, cor) in enumerate(beneficios):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (card_w + 40)
        cy = start_y + row * (card_h + 35)

        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=18, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, cy + 25, cx + 8, cy + card_h - 25], radius=4, fill=cor)
        draw.text((cx + 35, cy + 35), tit, font=get_font(FONT_SERIF_BOLD, 26), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = cy + 85
        for l in lines:
            draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
            ly += 28

    return img

# ==============================================================================
# SLIDE 8: PRÓXIMOS PASSOS & INVESTIMENTO
# ==============================================================================
def build_slide_8():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Vamos testar juntos?",
                "Proposta de implantação dos cartões NFC no Jurerê Beach Village.", kicker_color=TURQUOISE_DARK)
    draw_footer(draw, 8)

    box_left = [100, 280, 1050, 850]
    draw_shadow_card(draw, img, box_left, radius=20, bg_color=CARD_WHITE)

    draw.text((145, 330), "Proposta de implantação Jurerê Beach Village", font=get_font(FONT_SERIF_BOLD, 30), fill=TEXT_DARK)

    itens = [
        ("Cartões NFC Jurerê Beach Village", "100 unidades em acrílico resinado nobre, já configuradas e funcionais.\nDurabilidade e suporte técnico de 2 anos na tecnologia de todas as placas."),
        ("Página e atualizações", "R$ 350,00 mensal — 1º mês incluso na proposta de implantação.\nAtualizações ilimitadas de conteúdo e suporte dedicado."),
        ("Prazo de entrega", "15 dias úteis a partir da validação das artes.")
    ]

    iy = 410
    for tit, dsc in itens:
        draw.text((145, iy), tit, font=get_font(FONT_SANS_BOLD, 20), fill=TURQUOISE_DARK)
        lines = dsc.split("\n")
        dy = iy + 30
        for l in lines:
            draw.text((145, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            dy += 24
        iy += 95

    # Passos 1 e 2
    passos_box_y = 690
    draw.rounded_rectangle([145, passos_box_y, 540, passos_box_y + 110], radius=14, fill=BG_CREAM)
    draw.text((165, passos_box_y + 20), "1", font=get_font(FONT_SANS_BOLD, 24), fill=TURQUOISE_DARK)
    draw.text((205, passos_box_y + 22), "Reunião para validar\nconteúdo e artes", font=get_font(FONT_SANS_BOLD, 17), fill=TEXT_DARK)

    draw.rounded_rectangle([570, passos_box_y, 965, passos_box_y + 110], radius=14, fill=BG_CREAM)
    draw.text((590, passos_box_y + 20), "2", font=get_font(FONT_SANS_BOLD, 24), fill=TURQUOISE_DARK)
    draw.text((630, passos_box_y + 22), "Ajustes com base no\nuso real", font=get_font(FONT_SANS_BOLD, 17), fill=TEXT_DARK)

    box_right = [1120, 280, W - 100, 850]
    draw_shadow_card(draw, img, box_right, radius=20, bg_color=CARD_WARM, border_color=BORDER_WARM)

    draw.text((1165, 330), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 18), fill=AMBER_MUTED)
    draw.text((1165, 375), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 54), fill=TURQUOISE_DARK)

    draw.text((1165, 460), "1º mês da página e atualizações incluso.", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_DARK)
    draw.text((1165, 510), "Forma de pagamento: PIX", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_DARK)
    draw.text((1165, 545), "• 50% na aprovação do pedido", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
    draw.text((1165, 575), "• 50% na entrega do material", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)

    draw.line([(1165, 635), (W - 145, 635)], fill=BORDER_WARM, width=1)

    draw.text((1165, 670), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 26), fill=TURQUOISE_DARK)
    draw.text((1165, 715), "Augusto Henrique Dos Santos", font=get_font(FONT_SANS_BOLD, 19), fill=TEXT_DARK)
    draw.text((1165, 745), "(48) 99908-8162", font=get_font(FONT_SANS, 18), fill=AMBER_MUTED)

    return img

def main():
    builders = [
        build_slide_1,
        build_slide_2,
        build_slide_3,
        build_slide_4,
        build_slide_5,
        build_slide_6,
        build_slide_7,
        build_slide_8
    ]

    images = []
    print("Gerando os 8 slides da proposta comercial...")
    for idx, builder in enumerate(builders):
        slide_img = builder()
        slide_path = os.path.join(OUTPUT_DIR, f"slide_{idx + 1}.png")
        slide_img.save(slide_path, "PNG", quality=95)
        images.append(slide_img)
        print(f"Slide {idx + 1} gerado: {slide_path}")

    # Salvar PDF composto
    images[0].save(
        PDF_FINAL,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=images[1:]
    )
    print("PDF Oficial gerado com sucesso em:", PDF_FINAL)

if __name__ == "__main__":
    main()

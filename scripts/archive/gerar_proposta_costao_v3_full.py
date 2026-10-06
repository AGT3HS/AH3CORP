import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# DESIGN TOKENS & SOBRETONS (COSTÃO DO SANTINHO)
# ==============================================================================
BG_CREAM = (248, 246, 240)       # #F8F6F0 (Off-white / Creme editorial nobre)
BG_LIGHT_TINT = (240, 243, 246)  # #F0F3F6 (Sobretom suave)
BG_DARK = (0, 37, 66)            # #002542 (Azul Marinho Nobre Capa)
BG_DARK_MID = (24, 52, 80)       # #183450 (Sobretom escuro)

CARD_WHITE = (255, 255, 255)     # #FFFFFF (Cards com elevação)
CARD_WARM = (252, 250, 246)      # #FCFAF6 (Cards com sobretom quente)
BORDER_SUBTLE = (226, 230, 235)  # #E2E6EB (Borda ultrafina)
BORDER_WARM = (235, 230, 220)    # #EBE6DC

NAVY = (0, 43, 74)               # #002B4A (Petróleo Nobre)
NAVY_LIGHT = (44, 65, 89)        # #2C4159
GOLD = (248, 175, 53)            # #F8AF35 (Âmbar Ouro)
GOLD_MUTED = (212, 145, 30)      # #D4911E
GOLD_BG = (253, 240, 214)        # #FDF0D6 (Pílula suave)
RED_SPA = (172, 24, 46)          # #AC182E (Acento SPA L'Occitane)
GREEN_VAL = (30, 130, 76)        # #1E824C (Verde Sucesso/Google)
BLUE_GOOGLE = (26, 115, 232)     # #1A73E8 (Azul Google Oficial)

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
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(0, 20, 40, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False, kicker_color=None):
    k_color = kicker_color if kicker_color else (GOLD if is_dark else NAVY)
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

def draw_footer(draw, page_num, total_pages=9, is_dark=False):
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

# ==============================================================================
# SLIDE 1: CAPA
# ==============================================================================
def build_slide_1():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=BG_DARK_MID)

    draw.text((120, H//2 - 200), "PROPOSTA COMERCIAL", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H//2 - 140), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)
    draw.text((120, H//2 - 50), "para a experiência", font=get_font(FONT_SERIF, 68), fill=TEXT_LIGHT)
    draw.text((120, H//2 + 40), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)

    draw.text((120, H//2 + 150), "Toda a infraestrutura, serviços e gastronomia do resort", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)
    draw.text((120, H//2 + 185), "acessíveis em um toque. Sempre atualizados.", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)

    draw.text((120, H - 120), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H - 85), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 18), fill=TEXT_LIGHT_MUTED)

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    try:
        card_rendered = render_svg_card_with_shadow(svg_path, target_size=650)
        img.paste(card_rendered, (W - 850, 160), card_rendered)
    except:
        draw.rectangle((W-800, 200, W-150, 850), fill=(80,80,80))

    return img

# ==============================================================================
# SLIDE 2: O PONTO DE PARTIDA
# ==============================================================================
def build_slide_2():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Mais tempo para o que importa.",
                "O hóspede chega com perguntas simples: qual é a senha do Wi-Fi? Até que horas vai o café da manhã?\nOnde agendo o SPA L'Occitane? O que o resort serve hoje no All-Inclusive?", kicker_color=NAVY)
    draw_footer(draw, 2)

    card_w = (W - 200 - 60) // 3
    card_h = 560
    card_y = 280
    gap = 30

    colunas = [
        ("Hoje",
         "Informação espalhada entre\nrecepção, murais, totens e\npapéis impressos que\nenvelhecem rápido e geram\nfricção no atendimento.",
         NAVY),
        ("O custo",
         "Equipe da recepção sobrecarregada\nrespondendo as mesmas dúvidas\nrepetitivas, e hóspede perdendo\ntempo sem achar o que precisa.",
         GOLD_MUTED),
        ("A proposta",
         "Um cartão NFC elegante no\nquarto e nos pontos de contato:\num toque abre tudo no navegador,\nsempre atualizado e sem baixar app.",
         GOLD)
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
                "Tecnologia nativa sem fricção: funciona direto por aproximação nos smartphones modernos.", kicker_color=NAVY)
    draw_footer(draw, 3)

    card_w = (W - 200 - 60) // 3
    card_h = 440
    card_y = 280
    gap = 30

    passos = [
        ("1", "Aproxime", "O hóspede encosta o celular no\ncartão. O chip NFC integrado abre a\npágina instantaneamente.", NAVY),
        ("2", "Abra", "A página oficial do Costão abre direto\nno navegador: Wi-Fi, horários, SPA,\nAll-Inclusive e programação do dia.", GOLD_MUTED),
        ("3", "Sempre atual", "A equipe do resort edita o cardápio ou\na agenda uma única vez e todos os\ncartões já exibem a versão nova.", GOLD)
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
    draw.text((140, 805), "O segredo: o cartão guarda apenas o link inteligente. O conteúdo vive na nuvem — por isso nunca desatualiza.",
              font=get_font(FONT_SANS_BOLD, 22), fill=NAVY)

    return img

# ==============================================================================
# SLIDE 4: CARTÃO 1 · COSTÃO GUEST EXPERIENCE
# ==============================================================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO 1 · COSTÃO GUEST EXPERIENCE", "Para quem está hospedado.",
                "Instalado nos quartos, recepção e lounges, libera em um toque tudo o que o hóspede procura.", kicker_color=NAVY)
    draw_footer(draw, 4)

    left_w = 1050
    cw = (left_w - 40) // 2
    ch = 240
    start_y = 280

    servicos = [
        ("Wi-Fi & Acesso", "Rede Costão Guest e regras de conexão\ndireto na tela, sem precisar ligar na recepção.", NAVY),
        ("Serviços & Lazer", "Piscinas aquecidas, transporte interno,\nquadras, transfer e horários de funcionamento.", GOLD_MUTED),
        ("Gastronomia & All-Inclusive", "Restaurantes do resort, horários do buffet,\ncardápios de drinks e snacks.", GOLD),
        ("Costão SPA L'Occitane", "Menu completo de massagens, terapias e\nagendamento direto pelo WhatsApp.", RED_SPA)
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

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    try:
        card_rendered = render_svg_card_with_shadow(svg_path, target_size=560)
        img.paste(card_rendered, (W - 680, 260), card_rendered)
    except:
        pass

    draw.text((W - 640, 850), "Arte do cartão 10×10 cm, em acrílico resinado nobre.", font=get_font(FONT_SANS_BOLD, 17), fill=NAVY)

    return img

# ==============================================================================
# SLIDE 5: O QUE O HÓSPEDE VÊ
# ==============================================================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw.text((100, 80), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 18), fill=NAVY)
    draw.text((100, 120), "Uma página que conecta", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)
    draw.text((100, 175), "todo o resort.", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)

    draw.text((100, 255), "Além das informações do quarto, a mesma página", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 290), "apresenta o All-Inclusive, o SPA L'Occitane, a agenda", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 325), "de shows diários e o Vacation Club.", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)

    callout_box = [100, 395, 660, 610]
    draw_shadow_card(draw, img, callout_box, radius=18, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE)
    draw.rounded_rectangle([100, 395, 108, 610], radius=4, fill=GOLD)

    draw.text((135, 425), "Novo: convite para avaliar no Google", font=get_font(FONT_SANS_BOLD, 22), fill=NAVY)
    draw.text((135, 465), "Ao fim da página, o hóspede satisfeito toca em", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 495), "'Avaliar no Google' e deixa sua nota em menos", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 525), "de 1 minuto — mais avaliações, mais visibilidade", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 555), "orgânica para o resort.", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)

    draw.text((100, 650), "Um canal único para divulgar o que o hotel quiser,", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY)
    draw.text((100, 680), "quando quiser. Sem limites de atualização.", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY)

    draw_footer(draw, 5)

    mockup_w = 340
    mockup_h = 700
    start_mx = 740
    gap_m = 40
    my = 110

    telas = [
        {
            "header": "COSTÃO DO SANTINHO", "kicker": "HOSPEDE-SE NO RESORT", "bg": NAVY,
            "cards": [
                ("WI-FI GUEST", "Rede: Costão Guest\nSenha: no cartão do quarto"),
                ("CHECK-IN / OUT", "Check-in: a partir das 15h\nCheck-out: até 12h"),
                ("CAFÉ DA MANHÃ", "07h às 10h30 · Restaurante"),
                ("TRANSPORTE", "Vans circulares todos os dias")
            ]
        },
        {
            "header": "ALL INCLUSIVE & SPA", "kicker": "SABOREIE & RELAXE", "bg": NAVY_LIGHT,
            "cards": [
                ("ALL INCLUSIVE", "Gastronomia, drinks, entretenimento\ne relax liberados"),
                ("SPA L'OCCITANE", "Massagens e tratamentos nobres\nAgende pelo WhatsApp"),
                ("VACATION CLUB", "Para voltar todo ano ao resort\nConheça os benefícios")
            ]
        },
        {
            "header": "AGENDA & AVALIAÇÃO", "kicker": "HOJE NO RESORT", "bg": NAVY,
            "cards": [
                ("17h · AULA DE DANÇA", "Salão principal · Recreação"),
                ("19h · MÚSICA AO VIVO", "Deck da praia · Acústico"),
                ("20h · TEATRO NOTURNO", "Espetáculo Encantos e Magia"),
                ("★ ★ ★ ★ ★", "Avaliar no Google / TripAdvisor\nAjude outros hóspedes!")
            ]
        }
    ]

    for col_idx, t in enumerate(telas):
        tx = start_mx + col_idx * (mockup_w + gap_m)
        bbox = [tx, my, tx + mockup_w, my + mockup_h]
        draw_shadow_card(draw, img, bbox, radius=32, bg_color=CARD_WHITE)

        draw.rounded_rectangle([tx + 8, my + 8, tx + mockup_w - 8, my + 115], radius=24, fill=t["bg"])
        draw.text((tx + 25, my + 30), t["kicker"], font=get_font(FONT_SANS_BOLD, 12), fill=GOLD)
        draw.text((tx + 25, my + 55), t["header"], font=get_font(FONT_SERIF_BOLD, 18), fill=TEXT_LIGHT)

        cy = my + 130
        for ctitle, cdesc in t["cards"]:
            card_box_h = 105 if "\n" in cdesc else 85
            is_stars = "★" in ctitle
            box_bg = GOLD_BG if is_stars else BG_CREAM

            draw.rounded_rectangle([tx + 15, cy, tx + mockup_w - 15, cy + card_box_h], radius=14, fill=box_bg)

            if is_stars:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
                draw.text((tx + 30, cy + 45), cdesc.split("\n")[0], font=get_font(FONT_SANS_BOLD, 14), fill=NAVY)
            else:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 13), fill=NAVY)
                lines = cdesc.split("\n")
                ly = cy + 40
                for l in lines:
                    draw.text((tx + 30, ly), l, font=get_font(FONT_SANS, 13), fill=TEXT_MUTED)
                    ly += 18

            cy += card_box_h + 12

    return img

# ==============================================================================
# SLIDE 6: O FOCO DO NOSSO SERVIÇO (REPLICA EXATA DO SLIDE 8 BEWIKI / IMAGE_0A17AD.PNG)
# ==============================================================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    kicker_txt = "O FOCO DO NOSSO SERVIÇO"
    title_txt = "Estadia melhor,\nmais avaliações,\nmais visibilidade."
    sub_txt = ("Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito\n"
               "a avaliar o hotel no Google. Mais avaliações recentes e boas notas ajudam\n"
               "o hotel a ser encontrado por quem busca onde ficar.")

    draw_header(draw, kicker_txt, title_txt, sub_txt, kicker_color=NAVY)
    draw_footer(draw, 6)

    # Card Google no Canto Superior Direito (Mockup UI Fiel)
    mockup_box = [W - 550, 190, W - 100, 480]
    draw_shadow_card(draw, img, mockup_box, radius=24, bg_color=CARD_WHITE)
    mx, my = mockup_box[0], mockup_box[1]

    gw = (mockup_box[2] - mockup_box[0]) / 4
    draw.rectangle([mx, my, mx + gw, my + 6], fill=(66, 133, 244))      # Blue
    draw.rectangle([mx + gw, my, mx + gw * 2, my + 6], fill=(234, 67, 53))   # Red
    draw.rectangle([mx + gw * 2, my, mx + gw * 3, my + 6], fill=(251, 188, 5)) # Yellow
    draw.rectangle([mx + gw * 3, my, mx + gw * 4, my + 6], fill=(52, 168, 83)) # Green

    draw.text((mx + 40, my + 45), "G", font=get_font(FONT_SANS_BOLD, 22), fill=(66, 133, 244))
    draw.text((mx + 75, my + 45), "Avaliação Google", font=get_font(FONT_SANS_BOLD, 20), fill=TEXT_DARK)

    draw.text((mx + 40, my + 95), "Gostou da sua estadia?", font=get_font(FONT_SERIF_BOLD, 30), fill=TEXT_DARK)
    draw.text((mx + 40, my + 145), "Avalie o Costão no Google. Leva menos", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
    draw.text((mx + 40, my + 170), "de 1 minuto e ajuda outros hóspedes.", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)

    # 5 stars
    draw.text((mx + 40, my + 210), "★ ★ ★ ★ ★", font=get_font(FONT_SANS_BOLD, 28), fill=GOLD)

    # Botão CTA Azul Google
    btn_box = [mx + 220, my + 210, mx + 410, my + 250]
    draw.rounded_rectangle(btn_box, radius=12, fill=BLUE_GOOGLE)
    draw.text((btn_box[0] + 25, btn_box[1] + 9), "Avaliar no Google", font=get_font(FONT_SANS_BOLD, 14), fill=TEXT_LIGHT)

    # Fileira de 4 Cards Inferiores (Workflow de 1 a 4)
    card_w = (W - 200 - 90) // 4
    card_h = 320
    cy = 580
    cx = 100

    workflow = [
        ("Estadia\nmelhor", "Wi-Fi, horários e serviços\na um toque: menos atrito\npara o hóspede.", NAVY),
        ("Convite\ncerto", "A página do cartão traz\no botão 'Avaliar no Google'\nno fim da visita.", GOLD_MUTED),
        ("Mais\navaliações", "Hóspedes satisfeitos avaliam\nem menos de 1 minuto, direto\ndo celular.", GOLD),
        ("Mais\nranking", "Volume e nota das avaliações\npesam na posição do hotel\nno Google.", NAVY)
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

    draw_header(draw, "POR QUE VALE PARA O HOTEL", "Menos atrito, mais experiência e mais receita.",
                "Quatro retornos diretos para a operação e posicionamento de mercado do resort.", kicker_color=NAVY)
    draw_footer(draw, 7)

    card_w = (W - 200 - 40) // 2
    card_h = 240
    start_y = 280

    beneficios = [
        ("Informação sempre correta",
         "Mudou o horário do café? A programação do show? A senha do Wi-Fi?\nEdita uma única vez na nuvem e todos os 100 cartões refletem na hora.", NAVY),
        ("Recepção e concierges mais leves",
         "Perguntas repetitivas passam a ser respondidas pelo próprio cartão,\nliberando a equipe para o atendimento nobre e acolhimento dos hóspedes.", GOLD_MUTED),
        ("Percepção de modernidade & luxo",
         "Um gesto simples e inovador que o hóspede nota, elogia e comenta,\nalinhado ao padrão de grandes resorts internacionais.", GOLD),
        ("Venda cruzada & consumo interno",
         "Shows noturnos, SPA L'Occitane, passeios e upgrade de diárias\naparecem com destaque para quem já está dentro do resort.", RED_SPA)
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
                "Proposta de implantação do lote piloto de cartões inteligentes no Costão do Santinho.", kicker_color=NAVY)
    draw_footer(draw, 8)

    box_left = [100, 280, 1050, 850]
    draw_shadow_card(draw, img, box_left, radius=20, bg_color=CARD_WHITE)

    draw.text((145, 330), "Proposta de Implantação Costão Guest", font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_DARK)

    itens = [
        ("Cartões Costão Guest Experience", "100 unidades em acrílico resinado nobre, já configuradas com chip NFC e QR Code de contingência."),
        ("Garantia de Tecnologia", "2 anos de garantia total na tecnologia e integridade dos chips de todas as placas."),
        ("Página Web & Atualizações em Nuvem", "R$ 350,00 mensal — 1º mês incluso na implantação. Atualizações ilimitadas de conteúdo."),
        ("Prazo de Entrega do Piloto", "15 dias úteis a partir da aprovação final das artes e URLs de destino.")
    ]

    iy = 410
    for tit, dsc in itens:
        draw.text((145, iy), tit, font=get_font(FONT_SANS_BOLD, 20), fill=NAVY)
        lines = dsc.split("\n")
        dy = iy + 30
        for l in lines:
            draw.text((145, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            dy += 24
        iy += 95

    box_right = [1120, 280, W - 100, 850]
    draw_shadow_card(draw, img, box_right, radius=20, bg_color=CARD_WARM, border_color=BORDER_WARM)

    draw.text((1165, 330), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 18), fill=GOLD_MUTED)
    draw.text((1165, 375), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 54), fill=NAVY)

    draw.text((1165, 460), "1º mês de hospedagem e atualizações incluso.", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_DARK)
    draw.text((1165, 510), "Forma de pagamento:", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_DARK)
    draw.text((1165, 545), "• 50% na aprovação do pedido (PIX)", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
    draw.text((1165, 575), "• 50% na entrega e ativação dos cartões", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)

    draw.line([(1165, 635), (W - 145, 635)], fill=BORDER_WARM, width=1)

    draw.text((1165, 670), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 26), fill=NAVY)
    draw.text((1165, 715), "Augusto Henrique Dos Santos", font=get_font(FONT_SANS_BOLD, 19), fill=TEXT_DARK)
    draw.text((1165, 745), "(48) 99908-8162", font=get_font(FONT_SANS, 18), fill=GOLD_MUTED)

    return img

# ==============================================================================
# SLIDE 9: PROPOSTA DE EXPANSÃO (SPA L'OCCITANE & ALL-INCLUSIVE)
# ==============================================================================
def build_slide_9():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PROPOSTA DE EXPANSÃO", "O próximo passo: o toque chega a mais lugares.",
                "Mesma tecnologia NFC e plataforma integrada: ampliação modular para outros centros de receita do resort.", kicker_color=NAVY)
    draw_footer(draw, 9)

    card_w = (W - 200 - 40) // 2
    card_h = 560
    card_y = 280

    b1 = [100, card_y, 100 + card_w, card_y + card_h]
    draw_shadow_card(draw, img, b1, radius=20, bg_color=CARD_WHITE)

    draw.text((145, card_y + 45), "CARTÃO · ALL-INCLUSIVE & RESTAURANTES", font=get_font(FONT_SANS_BOLD, 16), fill=GOLD_MUTED)
    draw.text((145, card_y + 80), "Gastronomia & Bares", font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_DARK)

    draw.text((145, card_y + 150), "Nas mesas, quiosques de praia e lounges,", font=get_font(FONT_SANS, 19), fill=TEXT_BODY)
    draw.text((145, card_y + 180), "um toque abre o cardápio completo, sem papel.", font=get_font(FONT_SANS, 19), fill=TEXT_BODY)

    itens_g = [
        "Cardápios de drinks, vinhos e petiscos sempre na versão do dia",
        "Prato ou rótulo esgotou? Atualiza na hora na nuvem",
        "Horários dos restaurantes temáticos e buffet principal"
    ]
    gy = card_y + 245
    for it in itens_g:
        draw.text((145, gy), f"• {it}", font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
        gy += 42

    draw.text((145, card_y + 460), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=NAVY)

    b2 = [100 + card_w + 40, card_y, W - 100, card_y + card_h]
    draw_shadow_card(draw, img, b2, radius=20, bg_color=CARD_WHITE)

    draw.text((b2[0] + 45, card_y + 45), "CARTÃO · COSTÃO SPA L'OCCITANE", font=get_font(FONT_SANS_BOLD, 16), fill=RED_SPA)
    draw.text((b2[0] + 45, card_y + 80), "Bem-Estar & Terapias", font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_DARK)

    draw.text((b2[0] + 45, card_y + 150), "Nas suítes de luxo e recepção do SPA,", font=get_font(FONT_SANS, 19), fill=TEXT_BODY)
    draw.text((b2[0] + 45, card_y + 180), "um toque libera agendamento e menu completo.", font=get_font(FONT_SANS, 19), fill=TEXT_BODY)

    itens_s = [
        "Menu completo de massagens corporais e tratamentos faciais",
        "Agendamento direto pelo WhatsApp do SPA com 1 clique",
        "Divulgação de pacotes de relaxamento e dias de noiva"
    ]
    sy = card_y + 245
    for it in itens_s:
        draw.text((b2[0] + 45, sy), f"• {it}", font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
        sy += 42

    draw.text((b2[0] + 45, card_y + 460), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=NAVY)

    return img

# ==============================================================================
# COMPILADOR GLOBAL DO PDF FINAL (9 SLIDES)
# ==============================================================================
def gerar_todos_os_slides_e_pdf():
    print("Iniciando geração completa da Proposta Comercial Costão do Santinho (v3)...")
    
    slides = [
        (1, build_slide_1),
        (2, build_slide_2),
        (3, build_slide_3),
        (4, build_slide_4),
        (5, build_slide_5),
        (6, build_slide_6),
        (7, build_slide_7),
        (8, build_slide_8),
        (9, build_slide_9),
    ]

    pdf = pymupdf.open()
    
    for num, builder_fn in slides:
        print(f"-> Renderizando Slide {num}...")
        img = builder_fn()
        png_path = os.path.join(OUTPUT_DIR, f"v3_costao_slide_{num}.png")
        img.save(png_path, quality=95)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(PDF_FINAL)
    pdf.close()
    print(f"=== SUCESSO: PDF Final gerado em {PDF_FINAL} ===")

if __name__ == "__main__":
    gerar_todos_os_slides_e_pdf()

import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# TOKENS DE IDENTIDADE VISUAL OFICIAL (COSTÃO DO SANTINHO GUIA)
# ==============================================================================
# Paleta Oficial extraída do Guia de Identidade Visual:
# Tom 1: #0D3B66 (Azul Oceano Profundo / Accent Oficial)
# Tom 2: #FAF0CA (Creme Areia Suave / Background Editorial Nobre)
# Tom 3: #F4D35E (Ouro Solar / Destaques e Estrelas)
# Tom 4: #EE964B (Âmbar / Acentos de Calor e Conversão)
# Tom 5: #1A2530 (Grafite Profundo / Tipografia de Alto Contraste)
# Tom Fundo Geral: #F5F4EE (Off-white Pedra / Areia)

BG_OFFWHITE = (245, 244, 238)    # #F5F4EE (Fundo geral nobre)
BG_SAND_CREAM = (250, 240, 202)  # #FAF0CA (Tom 2 do Guia)
BG_OCEAN_DARK = (13, 59, 102)    # #0D3B66 (Tom 1 do Guia - Azul Oceano Capa)
BG_OCEAN_DEEP = (10, 42, 74)     # #0A2A4A (Sobretom Marinho)

CARD_WHITE = (255, 255, 255)     # #FFFFFF (Cards com elevação)
CARD_WARM = (252, 250, 245)      # #FCFAF5
BORDER_SUBTLE = (220, 222, 215)  # Borda suave mineral
BORDER_GOLD = (244, 211, 94)     # #F4D35E

BLUE_OCEAN = (13, 59, 102)       # #0D3B66 (Azul Oceano)
GOLD_SOLAR = (244, 211, 94)      # #F4D35E (Tom 3)
AMBER_WARM = (238, 150, 75)      # #EE964B (Tom 4)
GRAPHITE_DARK = (26, 37, 48)     # #1A2530 (Tom 5)
STONE_MUTED = (138, 133, 120)    # #8A8578 (--stone do Guia)
BLUE_GOOGLE = (26, 115, 232)

TEXT_DARK = (26, 37, 48)         # #1A2530
TEXT_BODY = (75, 86, 79)         # #4B564F (--ink-soft do Guia)
TEXT_MUTED = (138, 133, 120)     # #8A8578
TEXT_LIGHT = (255, 255, 255)
TEXT_LIGHT_MUTED = (215, 228, 238)

OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_FINAL = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf"
LOGO_OFICIAL_PATH = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_logo.png"

# Tipografia conforme Guia: Playfair Display (Serif) + Inter/Arial (Sans)
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf" # Playfair/Georgia
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"    # Inter/Arial
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_shadow_card(draw_base, img_base, bbox, radius=20, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE, shadow_alpha=30, shadow_blur=22, shadow_offset=(0, 10)):
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
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(13, 37, 48, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False, kicker_color=None):
    k_color = kicker_color if kicker_color else (GOLD_SOLAR if is_dark else BLUE_OCEAN)
    t_color = TEXT_LIGHT if is_dark else TEXT_DARK
    s_color = TEXT_LIGHT_MUTED if is_dark else TEXT_BODY

    y = 70
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 18), fill=k_color)
    y += 38
    
    t_lines = title.split("\n")
    for tl in t_lines:
        draw.text((100, y), tl, font=get_font(FONT_SERIF_BOLD, 44), fill=t_color)
        y += 54
        
    y += 18
    if subtitle:
        lines = subtitle.split("\n")
        for line in lines:
            draw.text((100, y), line, font=get_font(FONT_SANS, 20), fill=s_color)
            y += 30

def draw_footer(draw, page_num, total_pages=9, is_dark=False):
    f_color = (160, 185, 205) if is_dark else STONE_MUTED
    line_col = (25, 75, 120) if is_dark else BORDER_SUBTLE
    
    draw.line([(100, H - 70), (W - 100, H - 70)], fill=line_col, width=1)
    draw.text((100, H - 52), "Costão do Santinho Resort · Proposta Comercial de Cartões Inteligentes NFC", font=get_font(FONT_SANS, 15), fill=f_color)
    draw.text((W - 130, H - 52), f"{page_num}", font=get_font(FONT_SANS_BOLD, 17), fill=f_color)

def render_svg_card_with_shadow(svg_path, target_size=580):
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    mode = "RGBA" if pix.alpha else "RGB"
    card_img = Image.frombytes(mode, [pix.width, pix.height], pix.samples).convert("RGBA")
    card_img = card_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    pad = 80
    shadow_img = Image.new("RGBA", (target_size + pad * 2, target_size + pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle([pad + 15, pad + 35, pad + target_size - 15, pad + target_size + 35], radius=40, fill=(5, 25, 45, 110))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(30))
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

# ==============================================================================
# SLIDE 1: CAPA (AZUL OCEANO #0D3B66 & OURO SOLAR #F4D35E)
# ==============================================================================
def build_slide_1():
    img = Image.new("RGB", (W, H), BG_OCEAN_DARK)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=BG_OCEAN_DEEP)

    # Logo oficial no topo da capa
    try:
        if os.path.exists(LOGO_OFICIAL_PATH):
            logo_img = Image.open(LOGO_OFICIAL_PATH).convert("RGBA")
            logo_img.thumbnail((320, 100), Image.Resampling.LANCZOS)
            img.paste(logo_img, (120, 110), logo_img)
    except:
        pass

    draw.text((120, H//2 - 180), "PROPOSTA COMERCIAL · IDENTIDADE OFICIAL", font=get_font(FONT_SANS_BOLD, 18), fill=GOLD_SOLAR)
    draw.text((120, H//2 - 120), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)
    draw.text((120, H//2 - 30), "para a experiência", font=get_font(FONT_SERIF, 68), fill=TEXT_LIGHT)
    draw.text((120, H//2 + 60), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 74), fill=TEXT_LIGHT)

    draw.text((120, H//2 + 165), "Toda a infraestrutura, serviços e gastronomia do resort", font=get_font(FONT_SANS, 23), fill=TEXT_LIGHT_MUTED)
    draw.text((120, H//2 + 200), "acessíveis em um único toque. Sempre atualizados.", font=get_font(FONT_SANS, 23), fill=TEXT_LIGHT_MUTED)

    draw.text((120, H - 110), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 19), fill=GOLD_SOLAR)
    draw.text((120, H - 80), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 17), fill=TEXT_LIGHT_MUTED)

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    try:
        card_rendered = render_svg_card_with_shadow(svg_path, target_size=640)
        img.paste(card_rendered, (W - 830, 180), card_rendered)
    except:
        pass

    return img

# ==============================================================================
# SLIDE 2: O PONTO DE PARTIDA (SOBRETONS #F5F4EE & #FAF0CA)
# ==============================================================================
def build_slide_2():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Mais tempo para o que importa.",
                "O hóspede chega com perguntas frequentes: qual a rede Wi-Fi? Horários do All-Inclusive?\nOnde agendo o SPA L'Occitane? Como peço transporte interno no resort?")
    draw_footer(draw, 2)

    card_w = (W - 200 - 60) // 3
    card_h = 560
    card_y = 270
    gap = 30

    colunas = [
        ("Hoje",
         "Informações espalhadas entre recepção,\nmurais e papéis impressos que\nenvelhecem rápido e geram fricção\nno atendimento ao hóspede.",
         BLUE_OCEAN),
        ("O custo",
         "Equipe da recepção sobrecarregada\nrespondendo as mesmas dúvidas\noperacionais, gerando esperas e perda\nde oportunidades de consumo.",
         AMBER_WARM),
        ("A proposta",
         "Um cartão NFC em acrílico resinado nobre\nno quarto e nos lounges: um toque\nabre tudo no celular, sem baixar app e\nsempre sincronizado em tempo real.",
         GOLD_SOLAR)
    ]

    for i, (titulo, desc, cor_top) in enumerate(colunas):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 12], radius=6, fill=cor_top)
        draw.text((cx + 40, card_y + 55), titulo, font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = card_y + 140
        for l in lines:
            draw.text((cx + 40, ly), l, font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
            ly += 36

    return img

# ==============================================================================
# SLIDE 3: COMO FUNCIONA
# ==============================================================================
def build_slide_3():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "COMO FUNCIONA", "Três passos, nenhum aplicativo para baixar.",
                "Tecnologia nativa sem fricção: funciona direto por aproximação nos smartphones modernos.")
    draw_footer(draw, 3)

    card_w = (W - 200 - 60) // 3
    card_h = 440
    card_y = 270
    gap = 30

    passos = [
        ("1", "Aproxime", "O hóspede encosta o smartphone no\ncartão 10x10cm. O chip NFC integrado\nabre o link instantaneamente.", BLUE_OCEAN),
        ("2", "Acesse", "A página oficial do Costão abre direto\nno navegador: Wi-Fi, horários, SPA,\nAll-Inclusive e programação diária.", AMBER_WARM),
        ("3", "Sempre Atual", "A equipe do resort edita cardápios ou\navisos na nuvem uma única vez e todos\nos cartões já refletem na hora.", GOLD_SOLAR)
    ]

    for i, (num, titulo, desc, cor) in enumerate(passos):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20, bg_color=CARD_WHITE)

        draw.ellipse([cx + 40, card_y + 45, cx + 100, card_y + 105], fill=cor)
        draw.text((cx + 62, card_y + 57), num, font=get_font(FONT_SANS_BOLD, 32), fill=TEXT_LIGHT if cor != GOLD_SOLAR else TEXT_DARK)

        draw.text((cx + 40, card_y + 140), titulo, font=get_font(FONT_SERIF_BOLD, 34), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = card_y + 210
        for l in lines:
            draw.text((cx + 40, ly), l, font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
            ly += 32

    cbox = [100, 760, W - 100, 860]
    draw_shadow_card(draw, img, cbox, radius=16, bg_color=BG_SAND_CREAM, border_color=BORDER_GOLD)
    draw.text((140, 795), "O segredo: o cartão guarda apenas o link inteligente. O conteúdo vive na nuvem — por isso nunca desatualiza.",
              font=get_font(FONT_SANS_BOLD, 22), fill=BLUE_OCEAN)

    return img

# ==============================================================================
# SLIDE 4: CARTÃO 1 · COSTÃO GUEST EXPERIENCE
# ==============================================================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO 1 · COSTÃO GUEST EXPERIENCE", "Para quem está hospedado no resort.",
                "Instalado nos quartos, recepção e áreas sociais, libera em um toque tudo o que o hóspede procura.")
    draw_footer(draw, 4)

    left_w = 1050
    cw = (left_w - 40) // 2
    ch = 240
    start_y = 270

    servicos = [
        ("Wi-Fi & Conexão", "Rede Costão Guest e regras de conexão direto\nna tela, sem ligar para a recepção.", BLUE_OCEAN),
        ("Serviços & Lazer", "Piscinas aquecidas, vans circulares, quadras\ne horários de todas as atrações.", AMBER_WARM),
        ("Gastronomia & Bares", "Restaurantes do resort, horários do buffet,\ncardápios de drinks e snacks.", GOLD_SOLAR),
        ("Costão SPA L'Occitane", "Menu completo de massagens e agendamento\ndireto pelo WhatsApp oficial.", (172, 24, 46))
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
        img.paste(card_rendered, (W - 680, 250), card_rendered)
    except:
        pass

    draw.text((W - 640, 840), "Arte do cartão 10×10 cm, em acrílico resinado nobre.", font=get_font(FONT_SANS_BOLD, 17), fill=BLUE_OCEAN)

    return img

# ==============================================================================
# SLIDE 5: O QUE O HÓSPEDE VÊ (MOCKUPS MOBILE)
# ==============================================================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw.text((100, 75), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 18), fill=BLUE_OCEAN)
    draw.text((100, 115), "Uma página que conecta", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)
    draw.text((100, 170), "todo o resort.", font=get_font(FONT_SERIF_BOLD, 46), fill=TEXT_DARK)

    draw.text((100, 250), "Além das informações do quarto, a mesma página", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 285), "apresenta o All-Inclusive, o SPA L'Occitane, a agenda", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)
    draw.text((100, 320), "de shows diários e o Vacation Club.", font=get_font(FONT_SANS, 21), fill=TEXT_BODY)

    callout_box = [100, 390, 660, 610]
    draw_shadow_card(draw, img, callout_box, radius=18, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE)
    draw.rounded_rectangle([100, 390, 108, 610], radius=4, fill=AMBER_WARM)

    draw.text((135, 420), "Novo: convite para avaliar no Google", font=get_font(FONT_SANS_BOLD, 22), fill=BLUE_OCEAN)
    draw.text((135, 460), "Ao fim da página, o hóspede satisfeito toca em", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 490), "'Avaliar no Google' e deixa sua nota em menos", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 520), "de 1 minuto — mais avaliações e maior nota", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
    draw.text((135, 550), "média para o posicionamento do resort.", font=get_font(FONT_SANS, 18), fill=TEXT_BODY)

    draw.text((100, 650), "Um canal único para divulgar o que o hotel quiser,", font=get_font(FONT_SANS_BOLD, 20), fill=BLUE_OCEAN)
    draw.text((100, 680), "quando quiser. Sem limites de atualização.", font=get_font(FONT_SANS_BOLD, 20), fill=BLUE_OCEAN)

    draw_footer(draw, 5)

    mockup_w = 340
    mockup_h = 700
    start_mx = 740
    gap_m = 40
    my = 110

    telas = [
        {
            "header": "COSTÃO DO SANTINHO", "kicker": "HOSPEDE-SE NO RESORT", "bg": BLUE_OCEAN,
            "cards": [
                ("WI-FI GUEST", "Rede: Costão Guest\nSenha: no cartão do quarto"),
                ("CHECK-IN / OUT", "Check-in: 15h · Check-out: 12h\nRecepção 24h à disposição"),
                ("CAFÉ DA MANHÃ", "07h às 10h30 · Restaurante"),
                ("TRANSPORTE", "Vans circulares todos os dias")
            ]
        },
        {
            "header": "ALL INCLUSIVE & SPA", "kicker": "SABOREIE & RELAXE", "bg": (20, 50, 80),
            "cards": [
                ("ALL INCLUSIVE", "Gastronomia, drinks, entretenimento\ne relax liberados"),
                ("SPA L'OCCITANE", "Massagens e tratamentos nobres\nAgende pelo WhatsApp"),
                ("VACATION CLUB", "Para voltar todo ano ao resort\nConheça os benefícios")
            ]
        },
        {
            "header": "AGENDA & AVALIAÇÃO", "kicker": "HOJE NO RESORT", "bg": BLUE_OCEAN,
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
        draw.text((tx + 25, my + 30), t["kicker"], font=get_font(FONT_SANS_BOLD, 12), fill=GOLD_SOLAR)
        draw.text((tx + 25, my + 55), t["header"], font=get_font(FONT_SERIF_BOLD, 18), fill=TEXT_LIGHT)

        cy = my + 130
        for ctitle, cdesc in t["cards"]:
            card_box_h = 105 if "\n" in cdesc else 85
            is_stars = "★" in ctitle
            box_bg = BG_SAND_CREAM if is_stars else BG_OFFWHITE

            draw.rounded_rectangle([tx + 15, cy, tx + mockup_w - 15, cy + card_box_h], radius=14, fill=box_bg)

            if is_stars:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 20), fill=AMBER_WARM)
                draw.text((tx + 30, cy + 45), cdesc.split("\n")[0], font=get_font(FONT_SANS_BOLD, 14), fill=BLUE_OCEAN)
            else:
                draw.text((tx + 30, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 13), fill=BLUE_OCEAN)
                lines = cdesc.split("\n")
                ly = cy + 40
                for l in lines:
                    draw.text((tx + 30, ly), l, font=get_font(FONT_SANS, 13), fill=STONE_MUTED)
                    ly += 18

            cy += card_box_h + 12

    return img

# ==============================================================================
# SLIDE 6: O FOCO DO NOSSO SERVIÇO (AVALIAÇÕES GOOGLE COM IDENTIDADE DO GUIA)
# ==============================================================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    kicker_txt = "O FOCO DO NOSSO SERVIÇO"
    title_txt = "Estadia melhor,\nmais avaliações,\nmais visibilidade."
    sub_txt = ("Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito\n"
               "a avaliar o hotel no Google. Mais avaliações recentes e boas notas ajudam\n"
               "o resort a ser encontrado por quem busca onde ficar em Florianópolis.")

    draw_header(draw, kicker_txt, title_txt, sub_txt)
    draw_footer(draw, 6)

    # Card Google no Canto Superior Direito
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
    draw.text((mx + 40, my + 145), "Avalie o Costão no Google. Leva menos", font=get_font(FONT_SANS, 16), fill=STONE_MUTED)
    draw.text((mx + 40, my + 170), "de 1 minuto e ajuda outros hóspedes.", font=get_font(FONT_SANS, 16), fill=STONE_MUTED)

    draw.text((mx + 40, my + 210), "★ ★ ★ ★ ★", font=get_font(FONT_SANS_BOLD, 28), fill=AMBER_WARM)

    btn_box = [mx + 220, my + 210, mx + 410, my + 250]
    draw.rounded_rectangle(btn_box, radius=12, fill=BLUE_GOOGLE)
    draw.text((btn_box[0] + 25, btn_box[1] + 9), "Avaliar no Google", font=get_font(FONT_SANS_BOLD, 14), fill=TEXT_LIGHT)

    # 4 Cards Inferiores
    card_w = (W - 200 - 90) // 4
    card_h = 320
    cy = 580
    cx = 100

    workflow = [
        ("Estadia\nmelhor", "Wi-Fi, horários e serviços\na um toque: menos atrito\npara o hóspede.", BLUE_OCEAN),
        ("Convite\ncerto", "A página do cartão traz\no botão 'Avaliar no Google'\nno fim da visita.", AMBER_WARM),
        ("Mais\navaliações", "Hóspedes satisfeitos avaliam\nem menos de 1 minuto, direto\ndo celular.", GOLD_SOLAR),
        ("Mais\nranking", "Volume e nota das avaliações\npesam na posição do hotel\nno Google.", BLUE_OCEAN)
    ]

    enum_font = get_font(FONT_SANS_BOLD, 20)
    tit_font = get_font(FONT_SERIF_BOLD, 28)
    des_font = get_font(FONT_SANS, 17)

    for idx, (titulo, desc, c_color) in enumerate(workflow):
        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=16, bg_color=CARD_WHITE)

        draw.ellipse([cx + 35, cy + 40, cx + 75, cy + 80], fill=c_color)
        draw.text((cx + 50, cy + 48), f"{idx + 1}", font=enum_font, fill=TEXT_LIGHT if c_color != GOLD_SOLAR else TEXT_DARK)

        lines_t = titulo.split("\n")
        ty = cy + 110
        for lt in lines_t:
            draw.text((cx + 35, ty), lt, font=tit_font, fill=TEXT_DARK)
            ty += 34

        ty += 15
        lines_d = desc.split("\n")
        for ld in lines_d:
            draw.text((cx + 35, ty), ld, font=des_font, fill=STONE_MUTED)
            ty += 24

        cx += card_w + 30

    return img

# ==============================================================================
# SLIDE 7: POR QUE VALE PARA O HOTEL
# ==============================================================================
def build_slide_7():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O HOTEL", "Menos atrito, mais experiência e mais receita.",
                "Quatro retornos diretos para a operação e posicionamento de mercado do resort.")
    draw_footer(draw, 7)

    card_w = (W - 200 - 40) // 2
    card_h = 240
    start_y = 270

    beneficios = [
        ("Informação sempre correta",
         "Mudou o horário do café? A programação do show? A senha do Wi-Fi?\nEdita uma única vez na nuvem e todos os 100 cartões refletem na hora.", BLUE_OCEAN),
        ("Recepção e concierges mais leves",
         "Perguntas repetitivas passam a ser respondidas pelo próprio cartão,\nliberando a equipe para o acolhimento nobre e personalizado dos hóspedes.", AMBER_WARM),
        ("Percepção de modernidade & luxo",
         "Um gesto simples e inovador que o hóspede nota, elogia e comenta,\nalinhado ao padrão de grandes resorts internacionais 5 estrelas.", GOLD_SOLAR),
        ("Venda cruzada & consumo interno",
         "Shows noturnos, SPA L'Occitane, passeios e upgrade de diárias\naparecem com destaque para quem já está dentro do resort.", (172, 24, 46))
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
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Vamos testar juntos?",
                "Proposta de implantação do lote piloto de cartões inteligentes no Costão do Santinho.")
    draw_footer(draw, 8)

    box_left = [100, 270, 1050, 850]
    draw_shadow_card(draw, img, box_left, radius=20, bg_color=CARD_WHITE)

    draw.text((145, 320), "Proposta de Implantação Costão Guest", font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_DARK)

    itens = [
        ("Cartões Costão Guest Experience", "100 unidades em acrílico resinado nobre, já configuradas com chip NFC e QR Code de contingência."),
        ("Garantia de Tecnologia", "2 anos de garantia total na tecnologia e integridade dos chips de todas as placas."),
        ("Página Web & Atualizações em Nuvem", "R$ 350,00 mensal — 1º mês incluso na implantação. Atualizações ilimitadas de conteúdo."),
        ("Prazo de Entrega do Piloto", "15 dias úteis a partir da aprovação final das artes e URLs de destino.")
    ]

    iy = 400
    for tit, dsc in itens:
        draw.text((145, iy), tit, font=get_font(FONT_SANS_BOLD, 20), fill=BLUE_OCEAN)
        lines = dsc.split("\n")
        dy = iy + 30
        for l in lines:
            draw.text((145, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
            dy += 24
        iy += 95

    box_right = [1120, 270, W - 100, 850]
    draw_shadow_card(draw, img, box_right, radius=20, bg_color=BG_SAND_CREAM, border_color=BORDER_GOLD)

    draw.text((1165, 320), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 18), fill=AMBER_WARM)
    draw.text((1165, 365), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 54), fill=BLUE_OCEAN)

    draw.text((1165, 450), "1º mês de hospedagem e atualizações incluso.", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_DARK)
    draw.text((1165, 500), "Forma de pagamento:", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_DARK)
    draw.text((1165, 535), "• 50% na aprovação do pedido (PIX)", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
    draw.text((1165, 565), "• 50% na entrega e ativação dos cartões", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)

    draw.line([(1165, 625), (W - 145, 625)], fill=BORDER_GOLD, width=1)

    draw.text((1165, 660), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 26), fill=BLUE_OCEAN)
    draw.text((1165, 705), "Augusto Henrique Dos Santos", font=get_font(FONT_SANS_BOLD, 19), fill=TEXT_DARK)
    draw.text((1165, 735), "(48) 99908-8162", font=get_font(FONT_SANS, 18), fill=AMBER_WARM)

    return img

# ==============================================================================
# SLIDE 9: PROPOSTA DE EXPANSÃO (SPA L'OCCITANE & ALL-INCLUSIVE)
# ==============================================================================
def build_slide_9():
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PROPOSTA DE EXPANSÃO", "O próximo passo: o toque chega a mais lugares.",
                "Mesma tecnologia NFC e plataforma integrada: ampliação modular para outros centros de receita do resort.")
    draw_footer(draw, 9)

    card_w = (W - 200 - 40) // 2
    card_h = 560
    card_y = 270

    b1 = [100, card_y, 100 + card_w, card_y + card_h]
    draw_shadow_card(draw, img, b1, radius=20, bg_color=CARD_WHITE)

    draw.text((145, card_y + 45), "CARTÃO · ALL-INCLUSIVE & RESTAURANTES", font=get_font(FONT_SANS_BOLD, 16), fill=AMBER_WARM)
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
        draw.text((145, gy), f"• {it}", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
        gy += 42

    draw.text((145, card_y + 460), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=BLUE_OCEAN)

    b2 = [100 + card_w + 40, card_y, W - 100, card_y + card_h]
    draw_shadow_card(draw, img, b2, radius=20, bg_color=CARD_WHITE)

    draw.text((b2[0] + 45, card_y + 45), "CARTÃO · COSTÃO SPA L'OCCITANE", font=get_font(FONT_SANS_BOLD, 16), fill=(172, 24, 46))
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
        draw.text((b2[0] + 45, sy), f"• {it}", font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
        sy += 42

    draw.text((b2[0] + 45, card_y + 460), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=BLUE_OCEAN)

    return img

# ==============================================================================
# COMPILADOR GLOBAL
# ==============================================================================
def gerar_proposta_oficial_costao():
    print("Gerando Proposta Comercial alinhada ao Guia de Identidade Visual do Costão do Santinho...")
    
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
        png_path = os.path.join(OUTPUT_DIR, f"proposta_oficial_costao_s{num}.png")
        img.save(png_path, quality=95)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(PDF_FINAL)
    pdf.close()
    print(f"=== SUCESSO: Nova Proposta Comercial Oficial gerada em {PDF_FINAL} ===")

if __name__ == "__main__":
    gerar_proposta_oficial_costao()

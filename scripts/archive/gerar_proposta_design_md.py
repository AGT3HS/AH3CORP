import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# TOKENS DE DESIGN RIGOROSAMENTE BASEADOS NO DESIGN.md
# ==============================================================================
PRIMARY = (0, 37, 66)           # #002542
PRIMARY_MID = (44, 65, 89)      # #2C4159
SECONDARY = (248, 175, 53)      # #F8AF35
SECONDARY_LIGHT = (253, 240, 214) # #FDF0D6
ACCENT_SPA = (172, 24, 46)      # #AC182E
NEUTRAL_BG = (244, 246, 248)    # #F4F6F8
NEUTRAL_CARD = (255, 255, 255)  # #FFFFFF
TEXT_INK = (13, 34, 54)         # #0D2236
TEXT_MUTED = (91, 107, 122)     # #5B6B7A
BORDER_SUBTLE = (228, 233, 238) # #E4E9EE
BLUE_GOOGLE = (26, 115, 232)

OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_FINAL = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Costao_DesignMD.pdf"
LOGO_PATH = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_logo.png"
CARD_SVG_PATH = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"

# Tipografia conforme DESIGN.md: Georgia (Serif) + Arial (Sans)
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    paragraphs = text.split("\n")
    lines = []
    for p in paragraphs:
        if not p.strip():
            lines.append("")
            continue
        words = p.split(" ")
        curr_line = words[0]
        for w in words[1:]:
            test_line = curr_line + " " + w
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                curr_line = test_line
            else:
                lines.append(curr_line)
                curr_line = w
        lines.append(curr_line)
    return lines

def draw_shadow_card(draw_base, img_base, bbox, radius=20, bg_color=NEUTRAL_CARD, border_color=BORDER_SUBTLE, shadow_alpha=20, shadow_blur=16, shadow_offset=(0, 6)):
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
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(0, 37, 66, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False):
    k_color = SECONDARY if is_dark else SECONDARY
    t_color = (255, 255, 255) if is_dark else TEXT_INK
    s_color = (215, 228, 238) if is_dark else TEXT_MUTED

    y = 65
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 15), fill=k_color)
    y += 32
    
    t_lines = title.split("\n")
    for tl in t_lines:
        draw.text((100, y), tl, font=get_font(FONT_SERIF_BOLD, 42), fill=t_color)
        y += 48
        
    y += 10
    if subtitle:
        lines = wrap_text(subtitle, get_font(FONT_SANS, 18), 1720, draw)
        for line in lines:
            draw.text((100, y), line, font=get_font(FONT_SANS, 18), fill=s_color)
            y += 26

def draw_footer(draw, page_num, total_pages=9, is_dark=False):
    f_color = (160, 185, 205) if is_dark else TEXT_MUTED
    line_col = PRIMARY_MID if is_dark else BORDER_SUBTLE
    
    draw.line([(100, H - 65), (W - 100, H - 65)], fill=line_col, width=1)
    draw.text((100, H - 48), "Costão do Santinho Resort · Proposta Comercial de Cartões Inteligentes NFC", font=get_font(FONT_SANS, 14), fill=f_color)
    draw.text((W - 130, H - 48), f"{page_num} / {total_pages}", font=get_font(FONT_SANS_BOLD, 16), fill=f_color)

def render_svg_card(svg_path, target_size=560):
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    mode = "RGBA" if pix.alpha else "RGB"
    card_img = Image.frombytes(mode, [pix.width, pix.height], pix.samples).convert("RGBA")
    card_img = card_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    pad = 80
    shadow_img = Image.new("RGBA", (target_size + pad * 2, target_size + pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle([pad + 15, pad + 35, pad + target_size - 15, pad + target_size + 35], radius=40, fill=(0, 20, 40, 100))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(28))
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

# ==============================================================================
# SLIDE 1: CAPA INSTITUCIONAL (#002542 & #F8AF35)
# ==============================================================================
def build_slide_1():
    img = Image.new("RGB", (W, H), PRIMARY)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=PRIMARY_MID)

    try:
        if os.path.exists(LOGO_PATH):
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
            logo_img.thumbnail((320, 95), Image.Resampling.LANCZOS)
            img.paste(logo_img, (120, 100), logo_img)
    except:
        pass

    draw.text((120, H//2 - 190), "PROPOSTA COMERCIAL · NFC GUEST EXPERIENCE", font=get_font(FONT_SANS_BOLD, 16), fill=SECONDARY)
    draw.text((120, H//2 - 135), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 72), fill=(255, 255, 255))
    draw.text((120, H//2 - 50), "para a experiência", font=get_font(FONT_SERIF, 66), fill=(255, 255, 255))
    draw.text((120, H//2 + 35), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 72), fill=(255, 255, 255))

    draw.text((120, H//2 + 145), "Toda a infraestrutura, serviços e gastronomia do resort", font=get_font(FONT_SANS, 22), fill=(215, 228, 238))
    draw.text((120, H//2 + 180), "acessíveis em um único toque. Sempre atualizados.", font=get_font(FONT_SANS, 22), fill=(215, 228, 238))

    draw.text((120, H - 110), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 18), fill=SECONDARY)
    draw.text((120, H - 80), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 16), fill=(215, 228, 238))

    try:
        card_rendered = render_svg_card(CARD_SVG_PATH, target_size=630)
        img.paste(card_rendered, (W - 820, 180), card_rendered)
    except:
        pass

    return img

# ==============================================================================
# SLIDE 2: O PONTO DE PARTIDA (3 CARDS FLUTUANTES)
# ==============================================================================
def build_slide_2():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Mais tempo para o que importa.",
                "O hóspede chega com perguntas frequentes: qual a rede Wi-Fi? Horários do All-Inclusive?\nOnde agendo o SPA L'Occitane? Como peço transporte interno no resort?")
    draw_footer(draw, 2)

    card_w = (W - 200 - 80) // 3
    card_h = 560
    card_y = 270
    gap = 40

    colunas = [
        ("Hoje",
         "Informações espalhadas entre recepção, murais e papéis impressos que envelhecem rápido e geram atrito no atendimento ao hóspede.",
         PRIMARY),
        ("O custo",
         "Equipe da recepção sobrecarregada respondendo as mesmas dúvidas operacionais, gerando esperas e perda de oportunidades de consumo.",
         SECONDARY),
        ("A proposta",
         "Um cartão NFC em acrílico resinado nobre no quarto: um toque abre tudo no celular, sem baixar app e sempre sincronizado em tempo real.",
         PRIMARY_MID)
    ]

    for i, (titulo, desc, cor_top) in enumerate(colunas):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20)

        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 10], radius=5, fill=cor_top)
        draw.text((cx + 35, card_y + 50), titulo, font=get_font(FONT_SERIF_BOLD, 34), fill=TEXT_INK)

        lines = wrap_text(desc, get_font(FONT_SANS, 21), card_w - 70, draw)
        ly = card_y + 130
        for l in lines:
            draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 21), fill=TEXT_MUTED)
            ly += 34

    return img

# ==============================================================================
# SLIDE 3: COMO FUNCIONA (3 ETAPAS NUMERADAS + CALLOUT)
# ==============================================================================
def build_slide_3():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "COMO FUNCIONA", "Três passos, nenhum aplicativo para baixar.",
                "Tecnologia nativa sem fricção: funciona direto por aproximação nos smartphones modernos.")
    draw_footer(draw, 3)

    card_w = (W - 200 - 80) // 3
    card_h = 440
    card_y = 270
    gap = 40

    passos = [
        ("1", "Aproxime", "O hóspede encosta o smartphone no cartão 10x10cm. O chip NFC integrado abre o link instantaneamente.", PRIMARY),
        ("2", "Acesse", "A página oficial do Costão abre direto no navegador: Wi-Fi, horários, SPA, All-Inclusive e programação diária.", SECONDARY),
        ("3", "Sempre Atual", "A equipe do resort edita cardápios ou avisos na nuvem uma única vez e todos os cartões já refletem na hora.", PRIMARY_MID)
    ]

    for i, (num, titulo, desc, cor) in enumerate(passos):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=20)

        draw.ellipse([cx + 35, card_y + 40, cx + 95, card_y + 100], fill=cor)
        draw.text((cx + 57, card_y + 52), num, font=get_font(FONT_SANS_BOLD, 30), fill=(255, 255, 255) if cor != SECONDARY else TEXT_INK)

        draw.text((cx + 35, card_y + 130), titulo, font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_INK)

        lines = wrap_text(desc, get_font(FONT_SANS, 20), card_w - 70, draw)
        ly = card_y + 195
        for l in lines:
            draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 20), fill=TEXT_MUTED)
            ly += 30

    cbox = [100, 755, W - 100, 855]
    draw_shadow_card(draw, img, cbox, radius=16, bg_color=SECONDARY_LIGHT, border_color=SECONDARY)
    draw.text((140, 790), "O segredo: o cartão guarda apenas o link inteligente. O conteúdo vive na nuvem — por isso nunca desatualiza.",
              font=get_font(FONT_SANS_BOLD, 21), fill=PRIMARY)

    return img

# ==============================================================================
# SLIDE 4: CARTÃO 1 · GUEST EXPERIENCE (SPECS & GRID 2x2)
# ==============================================================================
def build_slide_4():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO 1 · COSTÃO GUEST EXPERIENCE", "Para quem está hospedado no resort.",
                "Instalado nos quartos, recepção e áreas sociais, libera em um toque tudo o que o hóspede procura.")
    draw_footer(draw, 4)

    left_w = 1050
    cw = (left_w - 40) // 2
    ch = 240
    start_y = 270

    servicos = [
        ("Wi-Fi & Conexão", "Rede Costão Guest e regras de conexão direto na tela, sem ligar para a recepção.", PRIMARY),
        ("Serviços & Lazer", "Piscinas aquecidas, vans circulares, quadras e horários de todas as atrações.", SECONDARY),
        ("Gastronomia & Bares", "Restaurantes do resort, horários do buffet, cardápios de drinks e snacks.", PRIMARY_MID),
        ("Costão SPA L'Occitane", "Menu completo de massagens e agendamento direto pelo WhatsApp oficial.", ACCENT_SPA)
    ]

    for idx, (tit, desc, cor) in enumerate(servicos):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (cw + 40)
        cy = start_y + row * (ch + 35)

        bbox = [cx, cy, cx + cw, cy + ch]
        draw_shadow_card(draw, img, bbox, radius=16)

        draw.rounded_rectangle([cx, cy + 25, cx + 8, cy + ch - 25], radius=4, fill=cor)
        draw.text((cx + 30, cy + 30), tit, font=get_font(FONT_SERIF_BOLD, 25), fill=TEXT_INK)

        lines = wrap_text(desc, get_font(FONT_SANS, 17), cw - 60, draw)
        ly = cy + 78
        for l in lines:
            draw.text((cx + 30, ly), l, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            ly += 26

    try:
        card_rendered = render_svg_card(CARD_SVG_PATH, target_size=550)
        img.paste(card_rendered, (W - 680, 250), card_rendered)
    except:
        pass

    draw.text((W - 640, 835), "Arte do cartão 10×10 cm, em acrílico resinado nobre.", font=get_font(FONT_SANS_BOLD, 16), fill=PRIMARY)

    return img

# ==============================================================================
# SLIDE 5: O QUE O HÓSPEDE VÊ (MOCKUPS MOBILE)
# ==============================================================================
def build_slide_5():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw.text((100, 70), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 16), fill=SECONDARY)
    draw.text((100, 110), "Uma página que conecta", font=get_font(FONT_SERIF_BOLD, 44), fill=TEXT_INK)
    draw.text((100, 160), "todo o resort.", font=get_font(FONT_SERIF_BOLD, 44), fill=TEXT_INK)

    draw.text((100, 240), "Além das informações do quarto, a mesma página", font=get_font(FONT_SANS, 20), fill=TEXT_MUTED)
    draw.text((100, 272), "apresenta o All-Inclusive, o SPA L'Occitane, a agenda", font=get_font(FONT_SANS, 20), fill=TEXT_MUTED)
    draw.text((100, 304), "de shows diários e o Vacation Club.", font=get_font(FONT_SANS, 20), fill=TEXT_MUTED)

    callout_box = [100, 370, 660, 590]
    draw_shadow_card(draw, img, callout_box, radius=16)
    draw.rounded_rectangle([100, 370, 108, 590], radius=4, fill=SECONDARY)

    draw.text((130, 400), "Novo: convite para avaliar no Google", font=get_font(FONT_SANS_BOLD, 21), fill=PRIMARY)
    
    desc_callout = "Ao fim da página, o hóspede satisfeito toca em 'Avaliar no Google' e deixa sua nota em menos de 1 minuto — mais avaliações e maior nota média para o posicionamento do resort."
    lines_c = wrap_text(desc_callout, get_font(FONT_SANS, 17), 490, draw)
    cy_text = 440
    for lc in lines_c:
        draw.text((130, cy_text), lc, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
        cy_text += 26

    draw.text((100, 640), "Um canal único para divulgar o que o hotel quiser,", font=get_font(FONT_SANS_BOLD, 19), fill=PRIMARY)
    draw.text((100, 670), "quando quiser. Sem limites de atualização.", font=get_font(FONT_SANS_BOLD, 19), fill=PRIMARY)

    draw_footer(draw, 5)

    mockup_w = 340
    mockup_h = 700
    start_mx = 740
    gap_m = 40
    my = 100

    telas = [
        {
            "header": "COSTÃO DO SANTINHO", "kicker": "HOSPEDE-SE NO RESORT", "bg": PRIMARY,
            "cards": [
                ("WI-FI GUEST", "Rede: Costão Guest\nSenha: no cartão do quarto"),
                ("CHECK-IN / OUT", "Check-in: 15h · Check-out: 12h\nRecepção 24h à disposição"),
                ("CAFÉ DA MANHÃ", "07h às 10h30 · Restaurante"),
                ("TRANSPORTE", "Vans circulares todos os dias")
            ]
        },
        {
            "header": "ALL INCLUSIVE & SPA", "kicker": "SABOREIE & RELAXE", "bg": PRIMARY_MID,
            "cards": [
                ("ALL INCLUSIVE", "Gastronomia, drinks, entretenimento\ne relax liberados"),
                ("SPA L'OCCITANE", "Massagens e tratamentos nobres\nAgende pelo WhatsApp"),
                ("VACATION CLUB", "Para voltar todo ano ao resort\nConheça os benefícios")
            ]
        },
        {
            "header": "AGENDA & AVALIAÇÃO", "kicker": "HOJE NO RESORT", "bg": PRIMARY,
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
        draw_shadow_card(draw, img, bbox, radius=30)

        draw.rounded_rectangle([tx + 8, my + 8, tx + mockup_w - 8, my + 110], radius=22, fill=t["bg"])
        draw.text((tx + 25, my + 25), t["kicker"], font=get_font(FONT_SANS_BOLD, 12), fill=SECONDARY)
        draw.text((tx + 25, my + 50), t["header"], font=get_font(FONT_SERIF_BOLD, 18), fill=(255, 255, 255))

        cy = my + 125
        for ctitle, cdesc in t["cards"]:
            card_box_h = 100 if "\n" in cdesc else 80
            is_stars = "★" in ctitle
            box_bg = SECONDARY_LIGHT if is_stars else NEUTRAL_BG

            draw.rounded_rectangle([tx + 15, cy, tx + mockup_w - 15, cy + card_box_h], radius=14, fill=box_bg)

            if is_stars:
                draw.text((tx + 25, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 20), fill=SECONDARY)
                draw.text((tx + 25, cy + 45), cdesc.split("\n")[0], font=get_font(FONT_SANS_BOLD, 13), fill=PRIMARY)
            else:
                draw.text((tx + 25, cy + 15), ctitle, font=get_font(FONT_SANS_BOLD, 13), fill=PRIMARY)
                lines = cdesc.split("\n")
                ly = cy + 38
                for l in lines:
                    draw.text((tx + 25, ly), l, font=get_font(FONT_SANS, 13), fill=TEXT_MUTED)
                    ly += 18

            cy += card_box_h + 12

    return img

# ==============================================================================
# SLIDE 6: O FOCO DO NOSSO SERVIÇO (AVALIAÇÕES GOOGLE)
# ==============================================================================
def build_slide_6():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
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
    draw_shadow_card(draw, img, mockup_box, radius=22)
    mx, my = mockup_box[0], mockup_box[1]

    gw = (mockup_box[2] - mockup_box[0]) / 4
    draw.rectangle([mx, my, mx + gw, my + 6], fill=(66, 133, 244))
    draw.rectangle([mx + gw, my, mx + gw * 2, my + 6], fill=(234, 67, 53))
    draw.rectangle([mx + gw * 2, my, mx + gw * 3, my + 6], fill=(251, 188, 5))
    draw.rectangle([mx + gw * 3, my, mx + gw * 4, my + 6], fill=(52, 168, 83))

    draw.text((mx + 35, my + 45), "G", font=get_font(FONT_SANS_BOLD, 22), fill=(66, 133, 244))
    draw.text((mx + 70, my + 45), "Avaliação Google", font=get_font(FONT_SANS_BOLD, 20), fill=TEXT_INK)

    draw.text((mx + 35, my + 95), "Gostou da sua estadia?", font=get_font(FONT_SERIF_BOLD, 30), fill=TEXT_INK)
    draw.text((mx + 35, my + 145), "Avalie o Costão no Google. Leva menos", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
    draw.text((mx + 35, my + 170), "de 1 minuto e ajuda outros hóspedes.", font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)

    draw.text((mx + 35, my + 210), "★ ★ ★ ★ ★", font=get_font(FONT_SANS_BOLD, 28), fill=SECONDARY)

    btn_box = [mx + 220, my + 210, mx + 410, my + 250]
    draw.rounded_rectangle(btn_box, radius=12, fill=BLUE_GOOGLE)
    draw.text((btn_box[0] + 25, btn_box[1] + 9), "Avaliar no Google", font=get_font(FONT_SANS_BOLD, 14), fill=(255, 255, 255))

    # 4 Cards Inferiores Rigorosamente Alinhados
    card_w = (W - 200 - 90) // 4
    card_h = 320
    cy = 580
    cx = 100

    workflow = [
        ("Estadia\nmelhor", "Wi-Fi, horários e serviços a um toque: menos atrito para o hóspede.", PRIMARY),
        ("Convite\ncerto", "A página do cartão traz o botão 'Avaliar no Google' no fim da visita.", SECONDARY),
        ("Mais\navaliações", "Hóspedes satisfeitos avaliam em menos de 1 minuto, direto do celular.", PRIMARY_MID),
        ("Mais\nranking", "Volume e nota das avaliações pesam na posição do hotel no Google.", PRIMARY)
    ]

    enum_font = get_font(FONT_SANS_BOLD, 20)
    tit_font = get_font(FONT_SERIF_BOLD, 28)
    des_font = get_font(FONT_SANS, 17)

    for idx, (titulo, desc, c_color) in enumerate(workflow):
        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=16)

        draw.ellipse([cx + 30, cy + 35, cx + 70, cy + 75], fill=c_color)
        draw.text((cx + 45, cy + 43), f"{idx + 1}", font=enum_font, fill=(255, 255, 255) if c_color != SECONDARY else TEXT_INK)

        lines_t = titulo.split("\n")
        ty = cy + 95
        for lt in lines_t:
            draw.text((cx + 30, ty), lt, font=tit_font, fill=TEXT_INK)
            ty += 34

        ty += 10
        lines_d = wrap_text(desc, des_font, card_w - 60, draw)
        for ld in lines_d:
            draw.text((cx + 30, ty), ld, font=des_font, fill=TEXT_MUTED)
            ty += 24

        cx += card_w + 30

    return img

# ==============================================================================
# SLIDE 7: POR QUE VALE PARA O HOTEL
# ==============================================================================
def build_slide_7():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O HOTEL", "Menos atrito, mais experiência e mais receita.",
                "Quatro retornos diretos para a operação e posicionamento de mercado do resort.")
    draw_footer(draw, 7)

    card_w = (W - 200 - 40) // 2
    card_h = 240
    start_y = 270

    beneficios = [
        ("Informação sempre correta",
         "Mudou o horário do café? A programação do show? A senha do Wi-Fi?\nEdita uma única vez na nuvem e todos os 100 cartões refletem na hora.", PRIMARY),
        ("Recepção e concierges mais leves",
         "Perguntas repetitivas passam a ser respondidas pelo próprio cartão,\nliberando a equipe para o acolhimento nobre e personalizado dos hóspedes.", SECONDARY),
        ("Percepção de modernidade & luxo",
         "Um gesto simples e inovador que o hóspede nota, elogia e comenta,\nalinhado ao padrão de grandes resorts internacionais 5 estrelas.", PRIMARY_MID),
        ("Venda cruzada & consumo interno",
         "Shows noturnos, SPA L'Occitane, passeios e upgrade de diárias\naparecem com destaque para quem já está dentro do resort.", ACCENT_SPA)
    ]

    for idx, (tit, desc, cor) in enumerate(beneficios):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (card_w + 40)
        cy = start_y + row * (card_h + 35)

        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=16)

        draw.rounded_rectangle([cx, cy + 25, cx + 8, cy + card_h - 25], radius=4, fill=cor)
        draw.text((cx + 30, cy + 30), tit, font=get_font(FONT_SERIF_BOLD, 26), fill=TEXT_INK)

        lines = wrap_text(desc, get_font(FONT_SANS, 18), card_w - 60, draw)
        ly = cy + 80
        for l in lines:
            draw.text((cx + 30, ly), l, font=get_font(FONT_SANS, 18), fill=TEXT_MUTED)
            ly += 28

    return img

# ==============================================================================
# SLIDE 8: PRÓXIMOS PASSOS & INVESTIMENTO
# ==============================================================================
def build_slide_8():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Vamos testar juntos?",
                "Proposta de implantação do lote piloto de cartões inteligentes no Costão do Santinho.")
    draw_footer(draw, 8)

    box_left = [100, 270, 1050, 850]
    draw_shadow_card(draw, img, box_left, radius=20)

    draw.text((140, 320), "Proposta de Implantação Costão Guest", font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_INK)

    itens = [
        ("Cartões Costão Guest Experience", "100 unidades em acrílico resinado nobre, já configuradas com chip NFC e QR Code de contingência."),
        ("Garantia de Tecnologia", "2 anos de garantia total na tecnologia e integridade dos chips de todas as placas."),
        ("Página Web & Atualizações em Nuvem", "R$ 350,00 mensal — 1º mês incluso na implantação. Atualizações ilimitadas de conteúdo."),
        ("Prazo de Entrega do Piloto", "15 dias úteis a partir da aprovação final das artes e URLs de destino.")
    ]

    iy = 395
    for tit, dsc in itens:
        draw.text((140, iy), tit, font=get_font(FONT_SANS_BOLD, 19), fill=PRIMARY)
        lines = wrap_text(dsc, get_font(FONT_SANS, 17), 850, draw)
        dy = iy + 28
        for l in lines:
            draw.text((140, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            dy += 24
        iy += 95

    box_right = [1120, 270, W - 100, 850]
    draw_shadow_card(draw, img, box_right, radius=20, bg_color=SECONDARY_LIGHT, border_color=SECONDARY)

    draw.text((1160, 320), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 17), fill=SECONDARY)
    draw.text((1160, 365), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 54), fill=PRIMARY)

    draw.text((1160, 450), "1º mês de hospedagem e atualizações incluso.", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_INK)
    draw.text((1160, 500), "Forma de pagamento:", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_INK)
    draw.text((1160, 535), "• 50% na aprovação do pedido (PIX)", font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
    draw.text((1160, 565), "• 50% na entrega e ativação dos cartões", font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)

    draw.line([(1160, 625), (W - 140, 625)], fill=SECONDARY, width=1)

    draw.text((1160, 660), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 26), fill=PRIMARY)
    draw.text((1160, 705), "Augusto Henrique Dos Santos", font=get_font(FONT_SANS_BOLD, 19), fill=TEXT_INK)
    draw.text((1160, 735), "(48) 99908-8162", font=get_font(FONT_SANS, 18), fill=SECONDARY)

    return img

# ==============================================================================
# SLIDE 9: PROPOSTA DE EXPANSÃO (SPA L'OCCITANE & ALL-INCLUSIVE)
# ==============================================================================
def build_slide_9():
    img = Image.new("RGB", (W, H), NEUTRAL_BG)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PROPOSTA DE EXPANSÃO", "O próximo passo: o toque chega a mais lugares.",
                "Mesma tecnologia NFC e plataforma integrada: ampliação modular para outros centros de receita do resort.")
    draw_footer(draw, 9)

    card_w = (W - 200 - 40) // 2
    card_h = 560
    card_y = 270

    b1 = [100, card_y, 100 + card_w, card_y + card_h]
    draw_shadow_card(draw, img, b1, radius=20)

    draw.text((140, card_y + 40), "CARTÃO · ALL-INCLUSIVE & RESTAURANTES", font=get_font(FONT_SANS_BOLD, 16), fill=SECONDARY)
    draw.text((140, card_y + 75), "Gastronomia & Bares", font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_INK)

    draw.text((140, card_y + 145), "Nas mesas, quiosques de praia e lounges,", font=get_font(FONT_SANS, 19), fill=TEXT_MUTED)
    draw.text((140, card_y + 175), "um toque abre o cardápio completo, sem papel.", font=get_font(FONT_SANS, 19), fill=TEXT_MUTED)

    itens_g = [
        "Cardápios de drinks, vinhos e petiscos sempre na versão do dia",
        "Prato ou rótulo esgotou? Atualiza na hora na nuvem",
        "Horários dos restaurantes temáticos e buffet principal"
    ]
    gy = card_y + 240
    for it in itens_g:
        lines_it = wrap_text(f"• {it}", get_font(FONT_SANS, 17), card_w - 80, draw)
        for lit in lines_it:
            draw.text((140, gy), lit, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            gy += 24
        gy += 14

    draw.text((140, card_y + 470), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=PRIMARY)

    b2 = [100 + card_w + 40, card_y, W - 100, card_y + card_h]
    draw_shadow_card(draw, img, b2, radius=20)

    draw.text((b2[0] + 40, card_y + 40), "CARTÃO · COSTÃO SPA L'OCCITANE", font=get_font(FONT_SANS_BOLD, 16), fill=ACCENT_SPA)
    draw.text((b2[0] + 40, card_y + 75), "Bem-Estar & Terapias", font=get_font(FONT_SERIF_BOLD, 36), fill=TEXT_INK)

    draw.text((b2[0] + 40, card_y + 145), "Nas suítes de luxo e recepção do SPA,", font=get_font(FONT_SANS, 19), fill=TEXT_MUTED)
    draw.text((b2[0] + 40, card_y + 175), "um toque libera agendamento e menu completo.", font=get_font(FONT_SANS, 19), fill=TEXT_MUTED)

    itens_s = [
        "Menu completo de massagens corporais e tratamentos faciais",
        "Agendamento direto pelo WhatsApp do SPA com 1 clique",
        "Divulgação de pacotes de relaxamento e dias de noiva"
    ]
    sy = card_y + 240
    for it in itens_s:
        lines_is = wrap_text(f"• {it}", get_font(FONT_SANS, 17), card_w - 80, draw)
        for lis in lines_is:
            draw.text((b2[0] + 40, sy), lis, font=get_font(FONT_SANS, 17), fill=TEXT_MUTED)
            sy += 24
        sy += 14

    draw.text((b2[0] + 40, card_y + 470), "INVESTIMENTO: Solicite um orçamento complementar.", font=get_font(FONT_SANS_BOLD, 17), fill=PRIMARY)

    return img

# ==============================================================================
# COMPILADOR GLOBAL DESIGN.MD
# ==============================================================================
def gerar_proposta_design_md():
    print("Gerando Proposta Comercial baseada rigorosamente no DESIGN.md...")
    
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
        png_path = os.path.join(OUTPUT_DIR, f"proposta_designmd_s{num}.png")
        img.save(png_path, quality=95)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(PDF_FINAL)
    pdf.close()
    print(f"=== SUCESSO: Proposta Comercial gerada com DESIGN.md em {PDF_FINAL} ===")

if __name__ == "__main__":
    gerar_proposta_design_md()

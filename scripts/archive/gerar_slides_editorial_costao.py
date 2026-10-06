import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# Cores da Identidade Visual do Costão do Santinho
NAVY_DEEP = (0, 37, 66)        # #002542 (Fundo Capa)
NAVY_MID = (44, 65, 89)        # #2C4159
GOLD = (248, 175, 53)          # #F8AF35 (Acento Ouro)
GOLD_LIGHT = (253, 240, 214)   # #FDF0D6 (Pílula suave)
RED_ACCENT = (172, 24, 46)     # #AC182E (Acento SPA L'Occitane)
BG_LIGHT = (244, 246, 248)     # #F4F6F8 (Fundo Páginas Internas)
BG_CARD = (255, 255, 255)      # #FFFFFF (Cards Internos)
INK = (13, 34, 54)             # #0D2236 (Texto Principal)
MUTED = (91, 107, 122)         # #5B6B7A (Texto Secundário)
LINE = (228, 233, 238)         # #E4E9EE (Bordas Sutis)

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

def draw_header(draw, kicker_text, title_text, subtitle_text=None, is_dark=False):
    kicker_font = get_font(FONT_SANS_BOLD, 20)
    title_font = get_font(FONT_SERIF_BOLD, 46)
    sub_font = get_font(FONT_SANS, 22)

    k_color = GOLD if is_dark else GOLD
    t_color = (255, 255, 255) if is_dark else INK
    s_color = (200, 215, 230) if is_dark else MUTED

    y = 80
    draw.text((100, y), kicker_text.upper(), font=kicker_font, fill=k_color)
    y += 38
    draw.text((100, y), title_text, font=title_font, fill=t_color)
    y += 65
    if subtitle_text:
        draw.text((100, y), subtitle_text, font=sub_font, fill=s_color)

def draw_footer(draw, page_num, total_pages=8, is_dark=False):
    f_font = get_font(FONT_SANS, 18)
    f_color = (150, 180, 205) if is_dark else MUTED
    
    left_txt = "Proposta · Cartões NFC Costão do Santinho"
    draw.text((100, H - 70), left_txt, font=f_font, fill=f_color)
    
    right_txt = f"{page_num}"
    draw.text((W - 120, H - 70), right_txt, font=get_font(FONT_SANS_BOLD, 20), fill=f_color)
    
    line_col = (20, 60, 95) if is_dark else LINE
    draw.line([(100, H - 90), (W - 100, H - 90)], fill=line_col, width=1)

def render_svg_card_with_shadow(svg_path, target_size=580):
    doc = pymupdf.open(svg_path)
    pix = doc[0].get_pixmap(dpi=300)
    mode = "RGBA" if pix.alpha else "RGB"
    card_img = Image.frombytes(mode, [pix.width, pix.height], pix.samples).convert("RGBA")
    card_img = card_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    pad = 80
    shadow_img = Image.new("RGBA", (target_size + pad * 2, target_size + pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle([pad + 15, pad + 35, pad + target_size - 15, pad + target_size + 35], radius=40, fill=(0, 0, 0, 110))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(30))
    shadow_img.paste(card_img, (pad, pad), card_img)
    return shadow_img

# ==========================================
# SLIDE 1: CAPA (Estilo Bewiki Petróleo/Navy com Mockup)
# ==========================================
def build_slide_1():
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)

    # Detalhes orgânicos sutis no fundo
    draw.ellipse([(W - 700, -200), (W + 500, 1000)], fill=(0, 48, 85))

    # Kicker
    draw.text((120, 220), "PROPOSTA COMERCIAL", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)

    # Título Principal (Serifada elegante com quebras harmônicas)
    draw.text((120, 280), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))
    draw.text((120, 365), "para a experiência", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))
    draw.text((120, 450), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))

    # Subtítulo explicativo
    draw.text((120, 560), "Toda a infraestrutura, serviços All-Inclusive, SPA L'Occitane", font=get_font(FONT_SANS, 24), fill=(210, 225, 240))
    draw.text((120, 600), "e programação do resort acessíveis num toque, sem baixar aplicativo.", font=get_font(FONT_SANS, 24), fill=(210, 225, 240))

    # Rodapé da Capa
    draw.text((120, H - 100), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H - 70), "Por: Augusto · Equipe AH3 Intelligence", font=get_font(FONT_SANS, 18), fill=(180, 205, 225))

    # Mockup do Cartão 10x10cm com Sombra à Direita
    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    card_rendered = render_svg_card_with_shadow(svg_path, target_size=620)
    img.paste(card_rendered, (W - 820, 160), card_rendered)

    return img

# ==========================================
# SLIDE 2: O PONTO DE PARTIDA (3 Colunas Idêntico ao Bewiki)
# ==========================================
def build_slide_2():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Mais tempo para o que importa.",
                "O hóspede chega com perguntas simples: qual é a senha do Wi-Fi? Até que horas vai o café da manhã? Onde agendo o SPA? O que o resort tem hoje?")
    draw_footer(draw, 2)

    card_w = 540
    card_h = 560
    card_y = 280
    gap = 40

    cols_data = [
        {"title": "Hoje", "color": MUTED, "text": "Informação espalhada entre recepção, placas físicas e papéis impressos que desatualizam a cada troca de programação."},
        {"title": "O custo", "color": RED_ACCENT, "text": "Equipe da recepção respondendo às mesmas perguntas centenas de vezes e hóspede sem achar o que precisa no resort."},
        {"title": "A proposta", "color": GOLD, "text": "Um cartão NFC em cada apartamento e ponto de contato: um toque no celular abre o portal completo e sempre atualizado."}
    ]

    for i, c in enumerate(cols_data):
        cx = 100 + i * (card_w + gap)
        draw.rounded_rectangle([cx+4, card_y+4, cx+card_w+4, card_y+card_h+4], radius=20, fill=(230, 235, 240))
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=20, fill=BG_CARD)
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+16], radius=8, fill=c["color"])
        draw.rectangle([cx, card_y+8, cx+card_w, card_y+16], fill=c["color"])

        draw.text((cx + 40, card_y + 60), c["title"], font=get_font(FONT_SERIF_BOLD, 38), fill=c["color"])

        words = c["text"].split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 30:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        ty = card_y + 140
        for line in lines:
            draw.text((cx + 40, ty), line, font=get_font(FONT_SANS, 24), fill=INK)
            ty += 38

    return img

# ==========================================
# SLIDE 3: COMO FUNCIONA (3 Passos com Círculos + Callout Bege)
# ==========================================
def build_slide_3():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "COMO FUNCIONA", "Três passos, nenhum aplicativo para baixar.")
    draw_footer(draw, 3)

    card_w = 540
    card_h = 420
    card_y = 240
    gap = 40

    steps = [
        {"num": "1", "title": "Aproxime", "color": NAVY_DEEP, "desc": "O hóspede encosta a traseira do celular no cartão NFC posicionado no quarto ou na mesa."},
        {"num": "2", "title": "Abra", "color": NAVY_DEEP, "desc": "A notificação surge instantaneamente e a página do Costão abre no navegador, sem cadastro."},
        {"num": "3", "title": "Sempre atual", "color": GOLD, "desc": "Mudou o cardápio ou a atração do teatro? Altere na nuvem e todos os cartões refletem na hora."}
    ]

    for i, s in enumerate(steps):
        cx = 100 + i * (card_w + gap)
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=20, fill=BG_CARD)

        circ_x = cx + 45
        circ_y = card_y + 45
        draw.ellipse([circ_x, circ_y, circ_x + 64, circ_y + 64], fill=s["color"])
        draw.text((circ_x + 22, circ_y + 14), s["num"], font=get_font(FONT_SANS_BOLD, 30), fill=(255, 255, 255))

        draw.text((cx + 45, card_y + 140), s["title"], font=get_font(FONT_SERIF_BOLD, 34), fill=INK)

        words = s["desc"].split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 30:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))

        ty = card_y + 200
        for line in lines:
            draw.text((cx + 45, ty), line, font=get_font(FONT_SANS, 22), fill=MUTED)
            ty += 34

    box_y = 700
    draw.rounded_rectangle([100, box_y, W - 100, box_y + 140], radius=18, fill=GOLD_LIGHT)
    draw.text((140, box_y + 35), "O segredo: o cartão físico guarda apenas um link seguro e vitalício.", font=get_font(FONT_SANS_BOLD, 24), fill=NAVY_DEEP)
    draw.text((140, box_y + 75), "O conteúdo vive em uma página web leve e responsiva — atualizada em tempo real pela AH3 sem trocar o cartão.", font=get_font(FONT_SANS, 21), fill=INK)

    return img

# ==========================================
# SLIDE 4: O QUE PODE CONTER (Grid 2x3 com 6 Ícones + Callout)
# ==========================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O QUE PODE CONTER", "Um cartão, infinitas possibilidades de conteúdo.",
                "O conteúdo é uma página web leve e responsiva, personalizada para o Costão do Santinho. Você escolhe o que mostrar:")
    draw_footer(draw, 4)

    card_w = 540
    card_h = 190
    gap_x = 40
    gap_y = 25
    start_y = 260

    features = [
        {"icon": "📶", "title": "Wi-Fi em um toque", "desc": "Rede Costão Guest e senha copiados automaticamente, sem digitar."},
        {"icon": "🌸", "title": "SPA L'Occitane", "desc": "Menu completo de massagens, rituais relaxantes e agendamento direto."},
        {"icon": "🍴", "title": "Restaurantes & Bares", "desc": "Cardápios All-Inclusive, horários do buffet e reservas especiais."},
        {"icon": "🎭", "title": "Agenda & Shows", "desc": "Programação diária do resort, teatro noturno e gincanas infantis."},
        {"icon": "🗺️", "title": "Mapa & Guias", "desc": "Vans internas, rotas das trilhas ecológicas e pontos arqueológicos."},
        {"icon": "⭐", "title": "Avaliação TripAdvisor/Google", "desc": "Link direto para avaliar a estadia em 1 minuto durante o check-out."}
    ]

    for i, f in enumerate(features):
        row = i // 3
        col = i % 3
        cx = 100 + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=16, fill=BG_CARD)
        
        draw.ellipse([cx + 25, cy + 25, cx + 75, cy + 75], fill=NAVY_DEEP)
        draw.text((cx + 36, cy + 34), f["icon"], font=get_font(FONT_SANS, 24), fill=(255, 255, 255))

        draw.text((cx + 90, cy + 35), f["title"], font=get_font(FONT_SANS_BOLD, 22), fill=INK)

        words = f["desc"].split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 32:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))

        ty = cy + 85
        for line in lines:
            draw.text((cx + 30, ty), line, font=get_font(FONT_SANS, 19), fill=MUTED)
            ty += 28

    box_y = 710
    draw.rounded_rectangle([100, box_y, W - 100, box_y + 110], radius=16, fill=GOLD_LIGHT)
    draw.text((140, box_y + 40), "E mais: links para o Vacation Club, canais de room service, atendimento WhatsApp da recepção e transfer.", font=get_font(FONT_SANS_BOLD, 22), fill=NAVY_DEEP)

    return img

# ==========================================
# SLIDE 5: PÁGINA DO CARTÃO (Mockup Físico Grande + Bullets + Dor Resolvida)
# ==========================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO 01 · COSTÃO GUEST EXPERIENCE", "Para quem está hospedado no resort.",
                "Posicionada na cabeceira, mesa ou aparador do quarto, a plaquinha resolve 100% das dúvidas da estadia:")
    draw_footer(draw, 5)

    bx = 120
    by = 280

    bullets = [
        ("Costão SPA:", "Agendamento de massagens, banhos e rituais L'Occitane."),
        ("Shows & Lazer:", "Agenda diária de lazer, gincanas e atrações noturnas."),
        ("Gastronomia:", "Cardápios, horários do buffet All-Inclusive e reservas."),
        ("Guia & Mapa:", "Wi-Fi, transporte interno de vans e trilhas ecológicas.")
    ]

    for title, desc in bullets:
        draw.ellipse([bx, by + 8, bx + 16, by + 24], fill=GOLD)
        draw.text((bx + 35, by), title, font=get_font(FONT_SANS_BOLD, 24), fill=NAVY_DEEP)
        tw = draw.textbbox((0, 0), title, font=get_font(FONT_SANS_BOLD, 24))[2]
        draw.text((bx + 45 + tw, by), desc, font=get_font(FONT_SANS, 24), fill=INK)
        by += 65

    box_y = 600
    draw.rounded_rectangle([bx, box_y, bx + 700, box_y + 140], radius=18, fill=BG_CARD)
    draw.rounded_rectangle([bx, box_y, bx + 700, box_y + 140], radius=18, outline=LINE, width=1)
    draw.text((bx + 35, box_y + 35), "Mudou a programação ou horário do SPA? Atualiza na hora.", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((bx + 35, box_y + 75), "Sem precisar trocar a placa de acrílico nem incomodar o hóspede no quarto.", font=get_font(FONT_SANS, 20), fill=MUTED)

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    card_rendered = render_svg_card_with_shadow(svg_path, target_size=580)
    img.paste(card_rendered, (W - 800, 200), card_rendered)

    return img

# ==========================================
# SLIDE 6: O QUE O HÓSPEDE VÊ (3 Mockups Mobile Idêntico ao Bewiki)
# ==========================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw.text((100, 80), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((100, 120), "Uma página web leve,", font=get_font(FONT_SERIF_BOLD, 46), fill=INK)
    draw.text((100, 175), "rápida e completa.", font=get_font(FONT_SERIF_BOLD, 46), fill=INK)

    draw.text((100, 250), "Além das informações do quarto, a página", font=get_font(FONT_SANS, 22), fill=MUTED)
    draw.text((100, 285), "apresenta o All-Inclusive, SPA L'Occitane,", font=get_font(FONT_SANS, 22), fill=MUTED)
    draw.text((100, 320), "agenda do dia e convites de avaliação.", font=get_font(FONT_SANS, 22), fill=MUTED)

    callout_y = 390
    draw.rounded_rectangle([100, callout_y, 620, callout_y + 190], radius=14, fill=BG_CARD)
    draw.rectangle([100, callout_y, 108, callout_y + 190], fill=RED_ACCENT)

    draw.text((130, callout_y + 25), "Novo: avaliação em 1 clique", font=get_font(FONT_SANS_BOLD, 22), fill=RED_ACCENT)
    draw.text((130, callout_y + 65), "Ao fim da estadia, o hóspede toca em", font=get_font(FONT_SANS, 19), fill=INK)
    draw.text((130, callout_y + 95), "'Avaliar no TripAdvisor/Google' e deixa a nota", font=get_font(FONT_SANS, 19), fill=INK)
    draw.text((130, callout_y + 125), "em menos de 1 minuto — mais reputação e vendas.", font=get_font(FONT_SANS, 19), fill=INK)

    draw.text((100, 610), "Um canal exclusivo para divulgar o que o resort", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY_DEEP)
    draw.text((100, 640), "quiser, quando quiser, sem limites.", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY_DEEP)

    draw_footer(draw, 6)

    mockup_w = 340
    mockup_h = 680
    start_mx = 680
    gap_m = 40
    my = 120

    telas = [
        {
            "header": "COSTÃO DO SANTINHO", "sub": "Bem-vindo ao Resort", "bg": NAVY_DEEP,
            "cards": [
                ("WI-FI GUEST", "Rede: Costão Guest\nSenha: no cartão"),
                ("CHECK-IN / OUT", "Check-in: 15h · Out: 12h\nLate checkout na recepção"),
                ("CAFÉ DA MANHÃ", "07h às 10h30\nRestaurante Principal"),
                ("TRANSPORTE", "Vans circulares o dia todo")
            ]
        },
        {
            "header": "SABOREIE & RELAXE", "sub": "All Inclusive & SPA", "bg": NAVY_MID,
            "cards": [
                ("ALL INCLUSIVE", "Buffet, drinks, petiscos\nna praia e piscina aquecida"),
                ("SPA L'OCCITANE", "Massagens relaxantes e hidro\nAgende pelo WhatsApp"),
                ("VACATION CLUB", "Para voltar todo ano\nConheça os benefícios")
            ]
        },
        {
            "header": "AGENDA & AVALIAÇÃO", "sub": "Hoje no Resort", "bg": NAVY_DEEP,
            "cards": [
                ("17h · AULA DE DANÇA", "Salão principal com recreação"),
                ("19h · MÚSICA AO VIVO", "Deck da praia com acústico"),
                ("20h · TEATRO NOTURNO", "Espetáculo Encantos e Magia"),
                ("★ ★ ★ ★ ★", "Avaliar no TripAdvisor\nMais visibilidade para o resort")
            ]
        }
    ]

    for col_idx, t in enumerate(telas):
        tx = start_mx + col_idx * (mockup_w + gap_m)
        draw.rounded_rectangle([tx, my, tx+mockup_w, my+mockup_h], radius=32, fill=(240, 242, 245), outline=LINE, width=2)
        draw.rounded_rectangle([tx+8, my+8, tx+mockup_w-8, my+120], radius=24, fill=t["bg"])
        draw.text((tx+25, my+30), t["header"], font=get_font(FONT_SERIF_BOLD, 18), fill=(255, 255, 255))
        draw.text((tx+25, my+60), t["sub"], font=get_font(FONT_SANS, 14), fill=GOLD)

        cy = my + 135
        for ctitle, cdesc in t["cards"]:
            card_box_h = 105 if "\n" in cdesc else 85
            is_stars = "★" in ctitle
            box_bg = GOLD_LIGHT if is_stars else BG_CARD
            
            draw.rounded_rectangle([tx+15, cy, tx+mockup_w-15, cy+card_box_h], radius=14, fill=box_bg)
            
            if is_stars:
                draw.text((tx+30, cy+15), ctitle, font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
                draw.text((tx+30, cy+45), cdesc.split("\n")[0], font=get_font(FONT_SANS_BOLD, 14), fill=NAVY_DEEP)
            else:
                draw.text((tx+30, cy+15), ctitle, font=get_font(FONT_SANS_BOLD, 13), fill=NAVY_DEEP)
                lines = cdesc.split("\n")
                ly = cy + 40
                for l in lines:
                    draw.text((tx+30, ly), l, font=get_font(FONT_SANS, 13), fill=MUTED)
                    ly += 18
            
            cy += card_box_h + 12

    return img

# ==========================================
# SLIDE 7: POR QUE VALE PARA O NEGÓCIO (4 Grandes Cards)
# ==========================================
def build_slide_7():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O NEGÓCIO", "Menos atrito operacional, mais experiência.",
                "Quatro ganhos imediatos na rotina dos hóspedes e no fluxo de atendimento da equipe:")
    draw_footer(draw, 7)

    card_w = 820
    card_h = 240
    gap_x = 40
    gap_y = 30
    start_y = 250

    beneficios = [
        {"icon": "✓", "title": "Informação sempre correta", "desc": "Cardápio, horários e programação atualizados na nuvem em segundos. Acaba com placas velhas, papéis rasurados e hóspedes mal informados."},
        {"icon": "✓", "title": "Equipe mais leve e produtiva", "desc": "A recepção deixa de ser balcão de dúvidas repetitivas (como Wi-Fi e horários de piscina) e foca no acolhimento de alto padrão."},
        {"icon": "✓", "title": "Percepção de modernidade e luxo", "desc": "O hóspede percebe o Costão como um resort de vanguarda que usa tecnologia sem atrito, elegante e sem exigir downloads chatos."},
        {"icon": "✓", "title": "Venda cruzada e mais consumo", "desc": "Apresenta o SPA L'Occitane, passeios, jantares especiais e o Vacation Club diretamente na tela do hóspede todos os dias."}
    ]

    for i, b in enumerate(beneficios):
        row = i // 2
        col = i % 2
        cx = 100 + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=20, fill=BG_CARD)
        
        draw.ellipse([cx + 40, cy + 40, cx + 90, cy + 90], fill=GOLD)
        draw.text((cx + 53, cy + 48), b["icon"], font=get_font(FONT_SANS_BOLD, 26), fill=NAVY_DEEP)

        draw.text((cx + 115, cy + 45), b["title"], font=get_font(FONT_SERIF_BOLD, 30), fill=INK)

        words = b["desc"].split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 55:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))

        ty = cy + 110
        for line in lines:
            draw.text((cx + 40, ty), line, font=get_font(FONT_SANS, 21), fill=MUTED)
            ty += 32

    return img

# ==========================================
# SLIDE 8: PRÓXIMOS PASSOS E INVESTIMENTO (Layout Bewiki)
# ==========================================
def build_slide_8():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Vamos testar juntos?")
    draw_footer(draw, 8)

    lx = 100
    ly = 240

    specs = [
        ("Proposta:", "Implantação Piloto de Cartões Inteligentes NFC"),
        ("Quantidade:", "100 cartões acrílicos 10x10cm resinados"),
        ("Garantia:", "Substituição gratuita de qualquer cartão com falha"),
        ("Página Web:", "Hospedagem, suporte e atualizações inclusas"),
        ("Prazo de Entrega:", "7 a 10 dias úteis após aprovação das artes")
    ]

    for label, val in specs:
        draw.text((lx, ly), label, font=get_font(FONT_SANS_BOLD, 22), fill=NAVY_DEEP)
        lw = draw.textbbox((0, 0), label, font=get_font(FONT_SANS_BOLD, 22))[2]
        draw.text((lx + lw + 15, ly), val, font=get_font(FONT_SANS, 22), fill=INK)
        ly += 55

    passos_box_y = 540
    draw.rounded_rectangle([lx, passos_box_y, lx + 800, passos_box_y + 190], radius=18, fill=BG_CARD)
    draw.text((lx + 35, passos_box_y + 25), "1. Reunião de validação", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((lx + 35, passos_box_y + 55), "Alinhamos os links, serviços e horários reais do Costão.", font=get_font(FONT_SANS, 19), fill=MUTED)
    draw.text((lx + 35, passos_box_y + 105), "2. Ajustes com base no uso", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((lx + 35, passos_box_y + 135), "Acompanhamos as primeiras semanas e refinamos o conteúdo.", font=get_font(FONT_SANS, 19), fill=MUTED)

    rx = 1020
    ry = 220
    rw = 800
    rh = 510

    draw.rounded_rectangle([rx, ry, rx+rw, ry+rh], radius=24, fill=NAVY_DEEP)
    
    draw.text((rx + 50, ry + 45), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((rx + 50, ry + 95), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 64), fill=(255, 255, 255))
    
    draw.text((rx + 50, ry + 185), "• 100 Cartões Acrílicos 10x10cm Personalizados", font=get_font(FONT_SANS, 22), fill=(220, 235, 245))
    draw.text((rx + 50, ry + 225), "• Programação NFC NTAG213 e Criptografia", font=get_font(FONT_SANS, 22), fill=(220, 235, 245))
    draw.text((rx + 50, ry + 265), "• Criação da Web-App Oficial e Hospedagem AH3", font=get_font(FONT_SANS, 22), fill=(220, 235, 245))
    draw.text((rx + 50, ry + 305), "• Suporte contínuo e atualizações de conteúdo ilimitadas", font=get_font(FONT_SANS, 22), fill=(220, 235, 245))

    draw.line([(rx + 50, ry + 360), (rx + rw - 50, ry + 360)], fill=(20, 65, 105), width=1)
    draw.text((rx + 50, ry + 385), "50% na aprovação / 50% na entrega final.", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((rx + 50, ry + 420), "Vamos conversar? Augusto · Equipe AH3 Intelligence", font=get_font(FONT_SANS, 20), fill=(255, 255, 255))

    return img

def main():
    slides = [
        build_slide_1(),
        build_slide_2(),
        build_slide_3(),
        build_slide_4(),
        build_slide_5(),
        build_slide_6(),
        build_slide_7(),
        build_slide_8(),
    ]

    slide_paths = []
    for idx, slide_img in enumerate(slides):
        p = os.path.join(OUTPUT_DIR, f"costao_slide_{idx+1}.png")
        slide_img.save(p, "PNG")
        slide_paths.append(p)
        print(f"Slide {idx+1} gerado com sucesso!")

    doc = pymupdf.open()
    for p in slide_paths:
        img_doc = pymupdf.open(p)
        pdf_bytes = img_doc.convert_to_pdf()
        img_pdf = pymupdf.open("pdf", pdf_bytes)
        doc.insert_pdf(img_pdf)

    doc.save(PDF_FINAL)
    print(f"\nPDF Final criado com sucesso em: {PDF_FINAL}")

if __name__ == "__main__":
    main()

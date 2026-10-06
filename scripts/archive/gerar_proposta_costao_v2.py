import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# Paleta Oficial Costão do Santinho
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

def draw_footer(draw, page_num, total_pages=9, is_dark=False):
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
# SLIDE 1: CAPA
# ==========================================
def build_slide_1():
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 700, -200), (W + 500, 1000)], fill=(0, 48, 85))

    draw.text((120, 220), "PROPOSTA COMERCIAL", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)

    draw.text((120, 280), "Cartões NFC", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))
    draw.text((120, 365), "para a experiência", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))
    draw.text((120, 450), "dos hóspedes.", font=get_font(FONT_SERIF_BOLD, 68), fill=(255, 255, 255))

    draw.text((120, 560), "Toda a infraestrutura, serviços All-Inclusive, SPA L'Occitane", font=get_font(FONT_SANS, 24), fill=(210, 225, 240))
    draw.text((120, 600), "e programação do resort acessíveis num toque, sem baixar aplicativo.", font=get_font(FONT_SANS, 24), fill=(210, 225, 240))

    draw.text((120, H - 100), "Preparada para: Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H - 70), "Por: Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 18), fill=(180, 205, 225))

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    card_rendered = render_svg_card_with_shadow(svg_path, target_size=620)
    img.paste(card_rendered, (W - 820, 160), card_rendered)

    return img

# ==========================================
# SLIDE 2: O PONTO DE PARTIDA
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
# SLIDE 3: COMO FUNCIONA
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
        {"num": "1", "title": "Aproxime", "color": NAVY_DEEP, "desc": "O hóspede encosta o celular no cartão. O NFC funciona na maioria dos smartphones atuais."},
        {"num": "2", "title": "Abra", "color": NAVY_DEEP, "desc": "A página do hotel abre direto no navegador: Wi-Fi, horários, serviços, SPA, eventos e lazer."},
        {"num": "3", "title": "Sempre atual", "color": GOLD, "desc": "O hotel muda uma informação uma única vez e todos os cartões já mostram a versão nova."}
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
    draw.text((140, box_y + 35), "O segredo: o cartão guarda só um link. O conteúdo vive na página — por isso nunca fica desatualizado.", font=get_font(FONT_SANS_BOLD, 24), fill=NAVY_DEEP)
    draw.text((140, box_y + 75), "Atualizado em tempo real pela AH3 sem trocar nenhuma placa física.", font=get_font(FONT_SANS, 21), fill=INK)

    return img

# ==========================================
# SLIDE 4: CARTÃO 1 · COSTÃO GUEST EXPERIENCE
# ==========================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "CARTÃO 1 · COSTÃO GUEST EXPERIENCE", "Para quem está hospedado no resort.",
                "Colocado no quarto e na recepção, libera num toque o que o hóspede mais procura:")
    draw_footer(draw, 4)

    start_x = 100
    start_y = 260
    card_h = 100
    gap_y = 18

    items = [
        ("Wi-Fi & Acesso", "Rede e senha automáticas, sem precisar pedir na recepção."),
        ("SPA L'Occitane", "Menu completo de massagens, relaxamento e agendamento direto."),
        ("Gastronomia All-Inclusive", "Horários do buffet, cardápios dos restaurantes e bares da praia."),
        ("Shows & Lazer", "Programação do teatro, gincanas infantis, vans e mapas das trilhas.")
    ]

    for i, (title, desc) in enumerate(items):
        cy = start_y + i * (card_h + gap_y)
        draw.rounded_rectangle([start_x, cy, start_x + 920, cy + card_h], radius=16, fill=BG_CARD)
        
        draw.ellipse([start_x + 35, cy + 28, start_x + 47, cy + 40], fill=GOLD)
        draw.text((start_x + 60, cy + 20), title, font=get_font(FONT_SANS_BOLD, 24), fill=NAVY_DEEP)
        draw.text((start_x + 60, cy + 55), desc, font=get_font(FONT_SANS, 20), fill=MUTED)

    draw.text((start_x, H - 125), "Arte do cartão 10×10 cm, nas cores e fontes oficiais da marca.", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)

    svg_path = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.svg"
    card_rendered = render_svg_card_with_shadow(svg_path, target_size=640)
    img.paste(card_rendered, (W - 800, 200), card_rendered)

    return img

# ==========================================
# SLIDE 5: O QUE O HÓSPEDE VÊ
# ==========================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw.text((100, 80), "O QUE O HÓSPEDE VÊ", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((100, 120), "Uma página que conecta", font=get_font(FONT_SERIF_BOLD, 46), fill=INK)
    draw.text((100, 175), "toda a experiência.", font=get_font(FONT_SERIF_BOLD, 46), fill=INK)

    draw.text((100, 250), "Além das informações do quarto, a mesma página", font=get_font(FONT_SANS, 22), fill=MUTED)
    draw.text((100, 285), "apresenta o SPA L'Occitane, a gastronomia All-Inclusive,", font=get_font(FONT_SANS, 22), fill=MUTED)
    draw.text((100, 320), "o Vacation Club e a agenda de lazer do dia.", font=get_font(FONT_SANS, 22), fill=MUTED)

    callout_y = 390
    draw.rounded_rectangle([100, callout_y, 620, callout_y + 190], radius=14, fill=BG_CARD)
    draw.rectangle([100, callout_y, 108, callout_y + 190], fill=RED_ACCENT)

    draw.text((130, callout_y + 25), "Novo: convite para avaliar no Google", font=get_font(FONT_SANS_BOLD, 22), fill=RED_ACCENT)
    draw.text((130, callout_y + 65), "Ao fim da página, o hóspede satisfeito toca em", font=get_font(FONT_SANS, 19), fill=INK)
    draw.text((130, callout_y + 95), "'Avaliar no Google' e deixa sua nota em menos de", font=get_font(FONT_SANS, 19), fill=INK)
    draw.text((130, callout_y + 125), "1 minuto — mais avaliações e mais visibilidade.", font=get_font(FONT_SANS, 19), fill=INK)

    draw.text((100, 610), "Um canal único para divulgar o que o hotel", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY_DEEP)
    draw.text((100, 640), "quiser, quando quiser, sem limites.", font=get_font(FONT_SANS_BOLD, 20), fill=NAVY_DEEP)

    draw_footer(draw, 5)

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
                ("★ ★ ★ ★ ★", "Avaliar no Google / TripAdvisor\nMais visibilidade para o resort")
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
# SLIDE 6: O FOCO DO NOSSO SERVIÇO (SLIDE DO GOOGLE/RANKING)
# ==========================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O FOCO DO NOSSO SERVIÇO", "Estadia melhor, mais avaliações, mais visibilidade.",
                "Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito a avaliar o hotel no Google.\nMais avaliações recentes e boas notas ajudam o resort a ser encontrado por quem busca onde ficar.")
    draw_footer(draw, 6)

    card_w = 395
    card_h = 520
    card_y = 300
    gap = 30

    steps = [
        {
            "num": "1",
            "title": "Estadia melhor",
            "color": NAVY_DEEP,
            "desc": "Wi-Fi, horários, SPA e serviços a um toque: zero atrito e total autonomia para o hóspede."
        },
        {
            "num": "2",
            "title": "Convite certo",
            "color": NAVY_DEEP,
            "desc": "A página do cartão traz o botão 'Avaliar no Google' no momento exato de satisfação da visita."
        },
        {
            "num": "3",
            "title": "Mais avaliações",
            "color": RED_ACCENT,
            "desc": "Hóspedes satisfeitos avaliam em menos de 1 minuto, direto do celular, sem burocracia."
        },
        {
            "num": "4",
            "title": "Mais ranking",
            "color": GOLD,
            "desc": "Volume, constância e nota das avaliações disparam o posicionamento orgânico do resort no Google."
        }
    ]

    for i, s in enumerate(steps):
        cx = 100 + i * (card_w + gap)
        draw.rounded_rectangle([cx+3, card_y+3, cx+card_w+3, card_y+card_h+3], radius=20, fill=(230, 235, 240))
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=20, fill=BG_CARD)

        circ_x = cx + 40
        circ_y = card_y + 45
        draw.ellipse([circ_x, circ_y, circ_x + 64, circ_y + 64], fill=s["color"])
        draw.text((circ_x + 22, circ_y + 14), s["num"], font=get_font(FONT_SANS_BOLD, 30), fill=(255, 255, 255))

        draw.text((cx + 40, card_y + 145), s["title"], font=get_font(FONT_SERIF_BOLD, 32), fill=INK)

        words = s["desc"].split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 22:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))

        ty = card_y + 215
        for line in lines:
            draw.text((cx + 40, ty), line, font=get_font(FONT_SANS, 22), fill=MUTED)
            ty += 34

    return img

# ==========================================
# SLIDE 7: POR QUE VALE PARA O HOTEL
# ==========================================
def build_slide_7():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O HOTEL", "Menos atrito, mais experiência.",
                "Quatro ganhos imediatos na rotina dos hóspedes e no fluxo de atendimento da equipe:")
    draw_footer(draw, 7)

    card_w = 820
    card_h = 240
    gap_x = 40
    gap_y = 30
    start_y = 250

    beneficios = [
        {"icon": "✓", "title": "Informação sempre correta", "desc": "Mudou o horário do café? A senha do Wi-Fi? A atração do teatro? Edita uma única vez na nuvem e todos os cartões já mostram a versão nova."},
        {"icon": "✓", "title": "Recepção mais leve e produtiva", "desc": "Perguntas repetitivas passam a ser respondidas pelo próprio cartão. A equipe foca no acolhimento de alto padrão."},
        {"icon": "✓", "title": "Percepção de modernidade e luxo", "desc": "Um gesto simples e sem atrito que o hóspede nota, comenta e valoriza durante toda a estadia."},
        {"icon": "✓", "title": "Venda cruzada direta", "desc": "SPA L'Occitane, gastronomia All-Inclusive, passeios e o Vacation Club ganham destaque para quem já está dentro do resort."}
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
# SLIDE 8: PRÓXIMOS PASSOS E INVESTIMENTO
# ==========================================
def build_slide_8():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Vamos testar juntos?")
    draw_footer(draw, 8)

    lx = 100
    ly = 230

    draw.text((lx, ly), "Proposta de implantação Costão Guest Experience", font=get_font(FONT_SANS_BOLD, 24), fill=GOLD)
    ly += 45

    specs = [
        ("Cartões Costão Guest:", "100 unidades. Cartões já configurados e funcionais."),
        ("Garantia:", "Garantia de 2 anos na tecnologia de todas as placas."),
        ("Página e atualizações:", "R$ 350,00 mensal (incluso no piloto de implantação)."),
        ("Prazo de entrega:", "15 dias úteis após validação das artes.")
    ]

    for label, val in specs:
        draw.text((lx, ly), label, font=get_font(FONT_SANS_BOLD, 21), fill=NAVY_DEEP)
        lw = draw.textbbox((0, 0), label, font=get_font(FONT_SANS_BOLD, 21))[2]
        draw.text((lx + lw + 12, ly), val, font=get_font(FONT_SANS, 21), fill=INK)
        ly += 45

    draw.text((lx, ly + 10), "Expansão para SPA e Restaurantes: veja a próxima página.", font=get_font(FONT_SANS_BOLD, 19), fill=MUTED)

    passos_box_y = 500
    draw.rounded_rectangle([lx, passos_box_y, lx + 800, passos_box_y + 190], radius=18, fill=BG_CARD)
    draw.text((lx + 35, passos_box_y + 25), "1. Reunião para validar conteúdo e artes", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((lx + 35, passos_box_y + 55), "Alinhamos os links, fotos oficiais, serviços e horários reais do Costão.", font=get_font(FONT_SANS, 19), fill=MUTED)
    draw.text((lx + 35, passos_box_y + 105), "2. Ajustes com base no uso real", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((lx + 35, passos_box_y + 135), "Acompanhamos as primeiras semanas e refinamos o fluxo do hóspede.", font=get_font(FONT_SANS, 19), fill=MUTED)

    rx = 1020
    ry = 210
    rw = 800
    rh = 520

    draw.rounded_rectangle([rx, ry, rx+rw, ry+rh], radius=24, fill=NAVY_DEEP)
    
    draw.text((rx + 50, ry + 40), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((rx + 50, ry + 85), "R$ 4.900,00", font=get_font(FONT_SERIF_BOLD, 64), fill=(255, 255, 255))
    draw.text((rx + 50, ry + 160), "1º mês da página web responsiva e atualizações incluso.", font=get_font(FONT_SANS, 20), fill=(200, 220, 240))

    draw.text((rx + 50, ry + 215), "Forma de pagamento: PIX", font=get_font(FONT_SANS_BOLD, 22), fill=GOLD)
    draw.text((rx + 50, ry + 255), "• 50% na aprovação do pedido", font=get_font(FONT_SANS, 21), fill=(240, 245, 250))
    draw.text((rx + 50, ry + 290), "• 50% na entrega final do material", font=get_font(FONT_SANS, 21), fill=(240, 245, 250))

    draw.line([(rx + 50, ry + 350), (rx + rw - 50, ry + 350)], fill=(20, 65, 105), width=1)
    draw.text((rx + 50, ry + 380), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 26), fill=GOLD)
    draw.text((rx + 50, ry + 420), "Augusto Henrique Dos Santos  ·  (48) 99908-8162", font=get_font(FONT_SANS_BOLD, 22), fill=(255, 255, 255))

    return img

# ==========================================
# SLIDE 9: PROPOSTA DE EXPANSÃO
# ==========================================
def build_slide_9():
    img = Image.new("RGB", (W, H), BG_LIGHT)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PROPOSTA DE EXPANSÃO", "O próximo passo: o toque chega a mais lugares.",
                "Mesma tecnologia NFC: atualiza uma vez, todos os cartões refletem instantaneamente.")
    draw_footer(draw, 9)

    card_w = 820
    card_h = 420
    card_y = 230
    gap = 40

    expansoes = [
        {
            "kicker": "CARTÃO · SPA L'OCCITANE",
            "title": "Bem-estar & Rituais",
            "desc": "Nas salas de relaxamento, recepção do SPA e piscinas aquecidas, um toque abre o menu completo de tratamentos e rituais.",
            "bullets": [
                "Massagens, banhos e terapias sempre na versão atualizada",
                "Agendamento direto pelo WhatsApp da terapeuta",
                "Destaque para pacotes especiais e Day Use"
            ],
            "accent": RED_ACCENT
        },
        {
            "kicker": "CARTÃO · GASTRONOMIA & BARES",
            "title": "Restaurantes & Praia",
            "desc": "Nas mesas dos restaurantes temáticos, quiosques da praia e balcões, um toque abre os cardápios de drinks e pratos especiais.",
            "bullets": [
                "Cardápios de drinks, vinhos e pratos All-Inclusive do dia",
                "Prato ou drink esgotou? Atualiza na hora na nuvem",
                "Programação musical e jantares temáticos noturnos"
            ],
            "accent": GOLD
        }
    ]

    for i, exp in enumerate(expansoes):
        cx = 100 + i * (card_w + gap)
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=20, fill=BG_CARD)
        
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+14], radius=6, fill=exp["accent"])
        draw.rectangle([cx, card_y+6, cx+card_w, card_y+14], fill=exp["accent"])

        draw.text((cx + 40, card_y + 40), exp["kicker"], font=get_font(FONT_SANS_BOLD, 18), fill=exp["accent"])
        draw.text((cx + 40, card_y + 70), exp["title"], font=get_font(FONT_SERIF_BOLD, 32), fill=INK)

        words = exp["desc"].split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 50:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))

        ty = card_y + 120
        for line in lines:
            draw.text((cx + 40, ty), line, font=get_font(FONT_SANS, 20), fill=MUTED)
            ty += 30

        by = ty + 15
        for b in exp["bullets"]:
            draw.ellipse([cx + 40, by + 6, cx + 48, by + 14], fill=exp["accent"])
            draw.text((cx + 60, by), b, font=get_font(FONT_SANS, 19), fill=INK)
            by += 32

        draw.text((cx + 40, card_y + 345), "INVESTIMENTO", font=get_font(FONT_SANS_BOLD, 16), fill=MUTED)
        draw.text((cx + 40, card_y + 370), "Solicite um orçamento sob demanda.", font=get_font(FONT_SERIF_BOLD, 22), fill=NAVY_DEEP)

    box_c_y = 680
    draw.rounded_rectangle([100, box_c_y, W - 100, box_c_y + 110], radius=16, fill=NAVY_DEEP)
    draw.text((140, box_c_y + 25), "Vamos conversar?", font=get_font(FONT_SERIF_BOLD, 24), fill=GOLD)
    draw.text((140, box_c_y + 60), "Augusto Henrique Dos Santos  ·  (48) 99908-8162  ·  Equipe AH3 Intelligence", font=get_font(FONT_SANS_BOLD, 20), fill=(255, 255, 255))

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
        build_slide_9(),
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
    print(f"\nPDF Final completo de 9 páginas gerado com sucesso em: {PDF_FINAL}")

if __name__ == "__main__":
    main()

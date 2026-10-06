import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# DESIGN SYSTEM: LINEAR DARK PRECISION (TEXT-FIRST / EDITORIAL)
# ==============================================================================
BG_CANVAS = (8, 9, 10)            # #08090A (Marketing Black / Deep Void)
BG_PANEL = (15, 16, 17)           # #0F1011 (Panel Dark)
BG_SURFACE = (25, 26, 27)         # #191A1B (Elevated Surface Level 3)
BG_HOVER = (40, 40, 44)           # #28282C (Secondary Surface)

BORDER_SUBTLE = (255, 255, 255, 14)   # rgba(255,255,255,0.055)
BORDER_STANDARD = (255, 255, 255, 22) # rgba(255,255,255,0.085)
BORDER_ACCENT = (113, 112, 255, 80)

# Brand Linear Accent & Status
ACCENT_INDIGO = (94, 106, 210)    # #5E6AD2 (Brand Indigo)
ACCENT_VIOLET = (113, 112, 255)   # #7170FF (Interactive Violet)
ACCENT_HOVER = (130, 143, 255)    # #828FFF
GOLD_SOLAR = (244, 211, 94)       # #F4D35E (Dourado Costão)
EMERALD_GREEN = (16, 185, 129)    # #10B981 (Status Green)
RED_SPA = (172, 24, 46)

# Typography Luminance Steps
TEXT_PRIMARY = (247, 248, 248)    # #F7F8F8 (Near-white, zero eye strain)
TEXT_SECONDARY = (208, 214, 224)  # #D0D6E0 (Silver-gray body)
TEXT_TERTIARY = (138, 143, 152)   # #8A8F98 (Muted metadata)
TEXT_QUATERNARY = (98, 102, 109)  # #62666D (Subtle captions/timestamps)

FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"

OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_SAMPLE = "C:/Users/Augusto/Desktop/AH3/Proposta_Costao_Linear_Dark_Sample.pdf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_linear_card(draw_base, img_base, bbox, radius=12, bg_color=BG_PANEL, border_color=(255,255,255,20), shadow_alpha=40):
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    pad = 30
    
    # Layered subtle shadow
    s_img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    s_draw.rounded_rectangle([pad, pad + 8, pad + w, pad + h + 8], radius=radius, fill=(0, 0, 0, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(16))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    
    # Card surface
    c_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(c_img)
    c_draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=bg_color, outline=border_color, width=1)
    img_base.paste(c_img, (x1, y1), c_img)

def draw_header(draw, kicker, title, subtitle=None, kicker_color=ACCENT_VIOLET):
    y = 75
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 15), fill=kicker_color)
    y += 34
    
    lines_t = title.split("\n")
    for lt in lines_t:
        draw.text((100, y), lt, font=get_font(FONT_SANS_BOLD, 46), fill=TEXT_PRIMARY)
        y += 56
        
    y += 16
    if subtitle:
        lines_s = subtitle.split("\n")
        for ls in lines_s:
            draw.text((100, y), ls, font=get_font(FONT_SANS, 20), fill=TEXT_TERTIARY)
            y += 30

def draw_footer(draw, page_num, total_pages=5):
    draw.line([(100, H - 75), (W - 100, H - 75)], fill=(255, 255, 255, 20), width=1)
    draw.text((100, H - 56), "Costão do Santinho Resort · Linear Dark Editorial Proposal", font=get_font(FONT_SANS, 15), fill=TEXT_QUATERNARY)
    draw.text((W - 140, H - 56), f"0{page_num} / 0{total_pages}", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_TERTIARY)

# ==============================================================================
# SLIDE 1: COVER (LINEAR HERO)
# ==============================================================================
def build_slide_1():
    img = Image.new("RGBA", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    # Subtle background radial glow
    glow = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([100, 100, 700, 700], fill=(94, 106, 210, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    img.paste(glow, (W - 900, -100), glow)

    # Eyebrow Pill
    pill_box = [100, 160, 390, 200]
    draw.rounded_rectangle(pill_box, radius=20, fill=(255, 255, 255, 12), outline=(255, 255, 255, 28), width=1)
    draw.ellipse([116, 177, 124, 185], fill=EMERALD_GREEN)
    draw.text((135, 172), "TECNOLOGIA NFC EM NUVEM", font=get_font(FONT_SANS_BOLD, 13), fill=TEXT_SECONDARY)

    draw.text((100, 240), "A infraestrutura do resort,", font=get_font(FONT_SANS_BOLD, 72), fill=TEXT_PRIMARY)
    draw.text((100, 325), "em um toque.", font=get_font(FONT_SANS_BOLD, 72), fill=ACCENT_VIOLET)
    draw.text((100, 410), "Sempre sincronizada.", font=get_font(FONT_SANS_BOLD, 72), fill=TEXT_PRIMARY)

    draw.text((100, 525), "Substitua totens estáticos e papéis impressos por cartões inteligentes", font=get_font(FONT_SANS, 24), fill=TEXT_SECONDARY)
    draw.text((100, 565), "em acrílico resinado. Informações, gastronomia, SPA e avaliações em tempo real.", font=get_font(FONT_SANS, 24), fill=TEXT_TERTIARY)

    # Info card no canto inferior esquerdo
    draw.text((100, H - 160), "PROPOSTA COMERCIAL EXECUTIVA", font=get_font(FONT_SANS_BOLD, 16), fill=TEXT_QUATERNARY)
    draw.text((100, H - 130), "Costão do Santinho Resort", font=get_font(FONT_SANS_BOLD, 22), fill=TEXT_PRIMARY)
    draw.text((100, H - 98), "Augusto Henrique Dos Santos · (48) 99908-8162", font=get_font(FONT_SANS, 17), fill=TEXT_TERTIARY)

    # Right Card: System Specification
    r_box = [W - 720, 220, W - 100, 840]
    draw_linear_card(draw, img, r_box, radius=16, bg_color=BG_PANEL, border_color=BORDER_STANDARD)

    draw.text((r_box[0] + 45, r_box[1] + 45), "ESPECIFICAÇÃO DO PROJETO", font=get_font(FONT_SANS_BOLD, 15), fill=ACCENT_VIOLET)
    draw.text((r_box[0] + 45, r_box[1] + 75), "Padrão Linear Precision", font=get_font(FONT_SANS_BOLD, 30), fill=TEXT_PRIMARY)

    specs = [
        ("Dispositivos Físicos", "100 cartões NFC 10x10cm em acrílico resinado de alto padrão."),
        ("Infraestrutura em Nuvem", "Página web responsiva com latência <100ms e sem download de app."),
        ("Ciclo Google Reviews", "Integração direta para conversão de hóspedes satisfeitos em avaliações 5 estrelas."),
        ("Atualização Dinâmica", "Painel web para alteração imediata de Wi-Fi, cardápios, avisos e atrações.")
    ]

    sy = r_box[1] + 155
    for tit, dsc in specs:
        draw.text((r_box[0] + 45, sy), tit, font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_PRIMARY)
        lines = dsc.split("\n")
        dy = sy + 28
        for l in lines:
            draw.text((r_box[0] + 45, dy), l, font=get_font(FONT_SANS, 16), fill=TEXT_TERTIARY)
            dy += 22
        sy += 115

    return img.convert("RGB")

# ==============================================================================
# SLIDE 2: THE PROBLEM & SOLUTION (3 COLUMNS)
# ==============================================================================
def build_slide_2():
    img = Image.new("RGBA", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O PONTO DE PARTIDA", "Menos atrito no atendimento,\nmais foco na experiência.",
                "O hóspede moderno busca respostas imediatas sem fricção ou espera na recepção.")
    draw_footer(draw, 2)

    card_w = (W - 200 - 60) // 3
    card_h = 520
    card_y = 300
    gap = 30

    colunas = [
        ("O Cenário Atual",
         "Informações fragmentadas entre murais, papéis impressos e balcão.\n\nMaterial impresso envelhece rápido, gera custo constante de reposição e sobrecarrega a equipe com dúvidas simples de Wi-Fi e horários.",
         (255, 255, 255, 18), TEXT_TERTIARY),
        ("O Custo Operacional",
         "Recepção e concierges ocupados atendendo perguntas repetitivas.\n\nFilas nos horários de pico, hóspedes sem acesso fácil aos restaurantes e perda de oportunidades de consumo no SPA e serviços extras do resort.",
         (255, 255, 255, 24), TEXT_SECONDARY),
        ("A Solução NFC",
         "Um cartão de presença marcante instalado nos quartos e lounges.\n\nUm simples toque abre toda a estrutura do Costão no navegador do celular, sempre sincronizado e sem necessidade de baixar aplicativo.",
         BORDER_ACCENT, ACCENT_VIOLET)
    ]

    for i, (titulo, desc, b_color, t_accent) in enumerate(colunas):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_linear_card(draw, img, bbox, radius=14, bg_color=BG_PANEL, border_color=b_color)

        draw.text((cx + 40, card_y + 45), f"0{i+1}", font=get_font(FONT_SANS_BOLD, 16), fill=t_accent)
        draw.text((cx + 40, card_y + 80), titulo, font=get_font(FONT_SANS_BOLD, 30), fill=TEXT_PRIMARY)

        lines = desc.split("\n\n")
        ly = card_y + 155
        for p in lines:
            sublines = p.split("\n")
            for sl in sublines:
                draw.text((cx + 40, ly), sl, font=get_font(FONT_SANS, 18), fill=TEXT_SECONDARY)
                ly += 28
            ly += 14

    return img.convert("RGB")

# ==============================================================================
# SLIDE 3: GOOGLE REVIEWS CYCLE (SLIDE 6 TEXTUAL REFINADO)
# ==============================================================================
def build_slide_3():
    img = Image.new("RGBA", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "O FOCO DO NOSSO SERVIÇO", "Estadia melhor,\nmais avaliações no Google,\nmais visibilidade orgânica.",
                "O cartão conecta a conveniência do dia a dia ao aumento da nota média e autoridade do resort nas buscas.")
    draw_footer(draw, 3)

    # Top Right Highlight Card
    t_box = [W - 680, 200, W - 100, 480]
    draw_linear_card(draw, img, t_box, radius=16, bg_color=BG_PANEL, border_color=BORDER_ACCENT)

    draw.rounded_rectangle([t_box[0] + 40, t_box[1] + 40, t_box[0] + 190, t_box[1] + 70], radius=15, fill=(113, 112, 255, 30))
    draw.text((t_box[0] + 55, t_box[1] + 47), "GOOGLE REVIEWS", font=get_font(FONT_SANS_BOLD, 13), fill=ACCENT_VIOLET)

    draw.text((t_box[0] + 40, t_box[1] + 95), "Captura no Momento Certo", font=get_font(FONT_SANS_BOLD, 28), fill=TEXT_PRIMARY)
    draw.text((t_box[0] + 40, t_box[1] + 145), "Ao final da navegação rápida dos serviços, o hóspede", font=get_font(FONT_SANS, 17), fill=TEXT_SECONDARY)
    draw.text((t_box[0] + 40, t_box[1] + 172), "encontra o convite para avaliar no Google com 1 clique.", font=get_font(FONT_SANS, 17), fill=TEXT_SECONDARY)
    draw.text((t_box[0] + 40, t_box[1] + 215), "★ ★ ★ ★ ★", font=get_font(FONT_SANS_BOLD, 24), fill=GOLD_SOLAR)

    # Bottom 4 Flow Cards
    card_w = (W - 200 - 90) // 4
    card_h = 320
    cy = 570
    cx = 100

    fluxo = [
        ("1. Estadia Fluida", "Wi-Fi, cardápios e horários na mão do hóspede com zero tempo de espera.", ACCENT_VIOLET),
        ("2. Convite Sutil", "Botão 'Avaliar no Google' posicionado estrategicamente após a consulta.", TEXT_PRIMARY),
        ("3. Menos de 1 Minuto", "O hóspede avalia direto do celular autenticado, sem formulários longos.", GOLD_SOLAR),
        ("4. SEO & Ranking", "Volume crescente de notas 5 estrelas impulsionando o Costão no Google.", EMERALD_GREEN)
    ]

    for idx, (ftit, fdesc, fcor) in enumerate(fluxo):
        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_linear_card(draw, img, bbox, radius=12, bg_color=BG_PANEL, border_color=BORDER_STANDARD)

        draw.text((cx + 30, cy + 35), f"ETAPA 0{idx+1}", font=get_font(FONT_SANS_BOLD, 14), fill=fcor)
        draw.text((cx + 30, cy + 70), ftit.split(". ")[1], font=get_font(FONT_SANS_BOLD, 24), fill=TEXT_PRIMARY)

        lines = fdesc.split("\n")
        dy = cy + 130
        for l in lines:
            draw.text((cx + 30, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_TERTIARY)
            dy += 26

        cx += card_w + 30

    return img.convert("RGB")

# ==============================================================================
# SLIDE 4: VALUE CREATION & ROI (4 PILLARS)
# ==============================================================================
def build_slide_4():
    img = Image.new("RGBA", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "POR QUE VALE PARA O NEGÓCIO", "Quatro pilares de retorno mensurável.",
                "Transformação digital na ponta física com impacto direto na satisfação e faturamento.")
    draw_footer(draw, 4)

    card_w = (W - 200 - 40) // 2
    card_h = 240
    start_y = 280

    pilares = [
        ("1. Informação 100% Confiável",
         "Alterações de programação, horários ou regras são feitas na nuvem\ne refletem instantaneamente em todos os 100 cartões do hotel.", ACCENT_VIOLET),
        ("2. Produtividade da Equipe",
         "A recepção deixa de atuar como balcão de dúvidas repetitivas e ganha tempo\npara acolher hóspedes e prestar atendimento personalizado de alto valor.", TEXT_PRIMARY),
        ("3. Reputação & Conversão",
         "Aumento contínuo de avaliações orgânicas positivas no Google Meu Negócio,\nmelhorando a posição do resort frente aos concorrentes da Ilha.", GOLD_SOLAR),
        ("4. Venda Cruzada (Upsell)",
         "Destaque permanente para agendamento no SPA L'Occitane, restaurantes temáticos\ne passeios exclusivos para hóspedes que já estão no resort.", EMERALD_GREEN)
    ]

    for idx, (tit, desc, cor) in enumerate(pilares):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (card_w + 40)
        cy = start_y + row * (card_h + 35)

        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_linear_card(draw, img, bbox, radius=14, bg_color=BG_PANEL, border_color=BORDER_STANDARD)

        draw.text((cx + 40, cy + 40), tit, font=get_font(FONT_SANS_BOLD, 26), fill=TEXT_PRIMARY)
        lines = desc.split("\n")
        ly = cy + 95
        for l in lines:
            draw.text((cx + 40, ly), l, font=get_font(FONT_SANS, 18), fill=TEXT_TERTIARY)
            ly += 28

    return img.convert("RGB")

# ==============================================================================
# SLIDE 5: COMMERCIAL PROPOSAL & NEXT STEPS
# ==============================================================================
def build_slide_5():
    img = Image.new("RGBA", (W, H), BG_CANVAS)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "PRÓXIMOS PASSOS", "Proposta Comercial · Lote Piloto",
                "Implantação rápida com acompanhamento completo e garantia total de tecnologia.")
    draw_footer(draw, 5)

    # Left Column: Escopo do Piloto
    b_left = [100, 280, 1080, 840]
    draw_linear_card(draw, img, b_left, radius=16, bg_color=BG_PANEL, border_color=BORDER_STANDARD)

    draw.text((145, 330), "Escopo de Implantação Costão Guest", font=get_font(FONT_SANS_BOLD, 30), fill=TEXT_PRIMARY)

    itens = [
        ("100 Cartões NFC 10x10cm", "Fabricados em acrílico resinado de acabamento nobre, com chip NTAG213 e QR Code."),
        ("Página Web Dinâmica & Cloud", "Hospedagem segura em nuvem, carregamento instantâneo e design responsivo."),
        ("Garantia Integral de 2 Anos", "Cobertura contra defeitos de gravação e integridade física dos chips NFC."),
        ("Prazo de Entrega do Piloto", "15 dias úteis a partir da aprovação da ordem de serviço e URLs.")
    ]

    iy = 410
    for tit, dsc in itens:
        draw.text((145, iy), tit, font=get_font(FONT_SANS_BOLD, 20), fill=ACCENT_VIOLET)
        lines = dsc.split("\n")
        dy = iy + 28
        for l in lines:
            draw.text((145, dy), l, font=get_font(FONT_SANS, 17), fill=TEXT_TERTIARY)
            dy += 24
        iy += 95

    # Right Column: Investimento
    b_right = [1130, 280, W - 100, 840]
    draw_linear_card(draw, img, b_right, radius=16, bg_color=BG_PANEL, border_color=BORDER_ACCENT)

    draw.text((1175, 330), "INVESTIMENTO TOTAL", font=get_font(FONT_SANS_BOLD, 16), fill=ACCENT_VIOLET)
    draw.text((1175, 375), "R$ 4.900,00", font=get_font(FONT_SANS_BOLD, 54), fill=TEXT_PRIMARY)

    draw.text((1175, 460), "1º mês de hospedagem e suporte incluso.", font=get_font(FONT_SANS_BOLD, 16), fill=EMERALD_GREEN)
    draw.text((1175, 510), "Condições de Pagamento:", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_PRIMARY)
    draw.text((1175, 545), "• 50% na aprovação do pedido (PIX)", font=get_font(FONT_SANS, 17), fill=TEXT_SECONDARY)
    draw.text((1175, 575), "• 50% na entrega e ativação das placas", font=get_font(FONT_SANS, 17), fill=TEXT_SECONDARY)

    draw.line([(1175, 635), (W - 145, 635)], fill=(255, 255, 255, 20), width=1)

    draw.text((1175, 670), "Contato & Aprovação", font=get_font(FONT_SANS_BOLD, 22), fill=TEXT_PRIMARY)
    draw.text((1175, 710), "Augusto Henrique Dos Santos", font=get_font(FONT_SANS_BOLD, 18), fill=TEXT_SECONDARY)
    draw.text((1175, 740), "(48) 99908-8162", font=get_font(FONT_SANS, 18), fill=ACCENT_VIOLET)

    return img.convert("RGB")

# ==============================================================================
# COMPILADOR GLOBAL
# ==============================================================================
def gerar_proposta_linear_sample():
    print("Iniciando compilação da Proposta Editorial Dark (Linear Style)...")
    
    slides = [
        (1, build_slide_1),
        (2, build_slide_2),
        (3, build_slide_3),
        (4, build_slide_4),
        (5, build_slide_5),
    ]

    pdf = pymupdf.open()
    
    for num, builder_fn in slides:
        print(f"-> Renderizando Lâmina {num}...")
        img = builder_fn()
        png_path = os.path.join(OUTPUT_DIR, f"linear_dark_s{num}.png")
        img.save(png_path, quality=95)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(PDF_SAMPLE)
    pdf.close()
    print(f"=== SUCESSO: PDF Exemplo (Linear Dark) gerado em {PDF_SAMPLE} ===")

if __name__ == "__main__":
    gerar_proposta_linear_sample()

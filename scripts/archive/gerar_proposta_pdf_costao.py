import os
import sys
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import pymupdf

# Dimensões 1308 x 924 pt (proporção exata do guia de slides)
PAGE_WIDTH = 1308
PAGE_HEIGHT = 924

# Cores da Identidade Visual do Costão do Santinho
NAVY_DARK = colors.HexColor('#002B4A')      # #002B4A
NAVY_LIGHT = colors.HexColor('#2C4159')     # #2C4159
GOLD = colors.HexColor('#F8AF35')           # #F8AF35
GOLD_LIGHT = colors.HexColor('#FDF0D6')     # #FDF0D6 / chips
RED_ACCENT = colors.HexColor('#AC182E')     # #AC182E / SPA
BG_LIGHT = colors.HexColor('#F4F6F8')       # #F4F6F8
WHITE = colors.HexColor('#FFFFFF')
INK = colors.HexColor('#0D2236')
MUTED = colors.HexColor('#5B6B7A')
LINE_COLOR = colors.HexColor('#E4E9EE')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Capa não tem rodapé padrão nem paginação
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(MUTED)
        
        # Rodapé esquerdo
        footer_text = "PROPOSTA COMERCIAL · CARTÕES NFC COSTÃO DO SANTINHO"
        self.drawString(60, 45, footer_text)

        # Rodapé direito (numeração sequencial)
        page_str = f"{self._pageNumber:02d} / {page_count:02d}"
        self.drawRightString(PAGE_WIDTH - 60, 45, page_str)

        # Linha divisória sutil
        self.setStrokeColor(LINE_COLOR)
        self.setLineWidth(1)
        self.line(60, 65, PAGE_WIDTH - 60, 65)
        self.restoreState()

def create_proposal_pdf(output_pdf_path, card_png_path, logo_png_path):
    # Render SVG card to PNG if needed
    if not os.path.exists(card_png_path):
        svg_path = card_png_path.replace('.png', '.svg')
        if os.path.exists(svg_path):
            doc = pymupdf.open(svg_path)
            pix = doc[0].get_pixmap(dpi=300)
            pix.save(card_png_path)

    pdf = SimpleDocTemplate(
        output_pdf_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=60,
        rightMargin=60,
        topMargin=50,
        bottomMargin=80
    )

    styles = getSampleStyleSheet()

    # Tipografias & Estilos
    style_kicker = ParagraphStyle(
        'Kicker',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=GOLD,
        spaceAfter=8,
        textTransform='uppercase'
    )

    style_kicker_navy = ParagraphStyle(
        'KickerNavy',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=NAVY_DARK,
        spaceAfter=8,
        textTransform='uppercase'
    )

    style_title = ParagraphStyle(
        'MainTitle',
        fontName='Times-Bold', # Serifada clássica
        fontSize=38,
        leading=46,
        textColor=NAVY_DARK,
        spaceAfter=14
    )

    style_title_white = ParagraphStyle(
        'MainTitleWhite',
        fontName='Times-Bold',
        fontSize=46,
        leading=54,
        textColor=WHITE,
        spaceAfter=18
    )

    style_subtitle = ParagraphStyle(
        'Subtitle',
        fontName='Helvetica',
        fontSize=16,
        leading=24,
        textColor=MUTED,
        spaceAfter=24
    )

    style_subtitle_white = ParagraphStyle(
        'SubtitleWhite',
        fontName='Helvetica',
        fontSize=18,
        leading=26,
        textColor=WHITE,
        spaceAfter=30
    )

    style_body = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=14,
        leading=22,
        textColor=INK
    )

    story = []

    # ==========================================
    # 1. CAPA (Slide 1)
    # ==========================================
    # Fundo institucional escuro da marca
    def draw_cover_bg(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # Gradiente simulação com retângulos ou cor sólida nobre
        canvas_obj.setFillColor(NAVY_DARK)
        canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
        
        # Detalhe orgânico / curvas douradas decorativas
        canvas_obj.setFillColor(GOLD)
        canvas_obj.setStrokeColor(GOLD)
        canvas_obj.setLineWidth(3)
        p = canvas_obj.beginPath()
        p.moveTo(0, PAGE_HEIGHT * 0.4)
        p.curveTo(PAGE_WIDTH * 0.3, PAGE_HEIGHT * 0.6, PAGE_WIDTH * 0.6, PAGE_HEIGHT * 0.2, PAGE_WIDTH, PAGE_HEIGHT * 0.35)
        p.lineTo(PAGE_WIDTH, 0)
        p.lineTo(0, 0)
        p.close()
        canvas_obj.saveState()
        canvas_obj.setFillColor(colors.HexColor('#001F35'))
        canvas_obj.drawPath(p, fill=True, stroke=False)
        canvas_obj.restoreState()

        # Rodapé da Capa
        canvas_obj.setFont("Helvetica-Bold", 12)
        canvas_obj.setFillColor(GOLD)
        canvas_obj.drawString(60, 50, "PREPARADA PARA: COSTÃO DO SANTINHO RESORT")
        
        canvas_obj.setFont("Helvetica", 12)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.drawRightString(PAGE_WIDTH - 60, 50, "POR: EQUIPE DE OPERAÇÕES & DESIGN AH3")
        canvas_obj.restoreState()

    # Conteúdo da Capa
    cover_left = [
        Spacer(1, 100),
        Paragraph("PROPOSTA COMERCIAL", style_kicker),
        Spacer(1, 10),
        Paragraph("Cartões Inteligentes NFC para a experiência dos hóspedes do Costão.", style_title_white),
        Spacer(1, 12),
        Paragraph("Toda a infraestrutura, serviços All-Inclusive, SPA e programação do resort acessíveis num único toque no smartphone, sempre atualizados e sem aplicativo.", style_subtitle_white),
        Spacer(1, 40),
        Paragraph("✓ Sem download de app &nbsp;&nbsp;•&nbsp;&nbsp; ✓ Atualização em tempo real &nbsp;&nbsp;•&nbsp;&nbsp; ✓ Design padrão resort", ParagraphStyle('CoverBadges', fontName='Helvetica-Bold', fontSize=14, textColor=GOLD))
    ]

    card_img_cover = RLImage(card_png_path, width=420, height=420)

    cover_table = Table([[cover_left, card_img_cover]], colWidths=[700, 480])
    cover_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(cover_table)
    story.append(Spacer(1, 200)) # quebra de página manual pelo flowable ou PageBreak

    # ==========================================
    # 2. O PONTO DE PARTIDA (Slide 2)
    # ==========================================
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    ponto_partida = [
        Paragraph("O PONTO DE PARTIDA", style_kicker),
        Paragraph("Mais agilidade para quem hospeda, mais autonomia para quem descansa.", style_title),
        Paragraph("Em um resort com mais de 500 acomodações e dezenas de atrações diárias, as mesmas dúvidas se repetem centenas de vezes todos os dias na recepção e conciergerie:", style_subtitle),
        Spacer(1, 10),
        Paragraph("<i>\"Qual é o Wi-Fi do resort?\" &nbsp;•&nbsp; \"Onde vejo a programação infantil e shows de hoje?\" &nbsp;•&nbsp; \"Como agendar o SPA L'Occitane?\" &nbsp;•&nbsp; \"Quais restaurantes estão abertos no All-Inclusive?\"</i>", ParagraphStyle('Quotes', fontName='Helvetica-Oblique', fontSize=15, leading=22, textColor=NAVY_DARK, alignment=1)),
        Spacer(1, 40)
    ]

    # 3 Colunas: Hoje / O Custo / A Proposta
    col1 = [
        Paragraph("<b>HOJE</b>", ParagraphStyle('C1T', fontName='Helvetica-Bold', fontSize=16, textColor=RED_ACCENT, spaceAfter=8)),
        Paragraph("Informações espalhadas em totens distantes, papéis impressos que desatualizam a cada troca de cardápio/atração e sobrecarga contínua da recepção com perguntas básicas.", style_body)
    ]
    col2 = [
        Paragraph("<b>O CUSTO</b>", ParagraphStyle('C2T', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("Filas desnecessárias no balcão, hóspedes desinformados perdendo atrações e perda de receita direta em serviços de alto valor (como SPA, passeios e restaurantes especiais).", style_body)
    ]
    col3 = [
        Paragraph("<b>A PROPOSTA NFC</b>", ParagraphStyle('C3T', fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, spaceAfter=8)),
        Paragraph("Uma placa acrílica 10x10cm de alto padrão em cada apartamento e ponto de contato. O hóspede encosta o celular e acessa o portal completo instantaneamente.", style_body)
    ]

    t_3col = Table([[col1, col2, col3]], colWidths=[360, 360, 380])
    t_3col.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FFF2F2')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#F0F4F8')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#FFF9E6')),
        ('BOX', (0,0), (0,0), 1.5, RED_ACCENT),
        ('BOX', (1,0), (1,0), 1.5, NAVY_LIGHT),
        ('BOX', (2,0), (2,0), 1.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 22),
        ('BOTTOMPADDING', (0,0), (-1,-1), 22),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.extend(ponto_partida)
    story.append(t_3col)

    # ==========================================
    # 3. COMO FUNCIONA (Slide 3)
    # ==========================================
    story.append(PageBreak())

    como_funciona = [
        Paragraph("COMO FUNCIONA", style_kicker),
        Paragraph("Três passos simples. Zero aplicativo para baixar.", style_title),
        Paragraph("A tecnologia NFC conecta o mundo físico ao digital de forma invisível e intuitiva para hóspedes de qualquer faixa etária.", style_subtitle),
        Spacer(1, 30)
    ]

    p1 = [
        Paragraph("<font size=28 color='#F8AF35'><b>1</b></font>", ParagraphStyle('Num1', spaceAfter=10)),
        Paragraph("<b>APROXIME</b>", ParagraphStyle('ST1', fontName='Helvetica-Bold', fontSize=18, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("O hóspede encosta a traseira do iPhone ou smartphone Android na plaquinha do quarto ou da mesa.", style_body)
    ]
    p2 = [
        Paragraph("<font size=28 color='#F8AF35'><b>2</b></font>", ParagraphStyle('Num2', spaceAfter=10)),
        Paragraph("<b>ABRA</b>", ParagraphStyle('ST2', fontName='Helvetica-Bold', fontSize=18, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("Uma notificação nativa surge na tela. Ao tocar, a página exclusiva do Costão abre direto no navegador sem login nem senha.", style_body)
    ]
    p3 = [
        Paragraph("<font size=28 color='#F8AF35'><b>3</b></font>", ParagraphStyle('Num3', spaceAfter=10)),
        Paragraph("<b>SEMPRE ATUAL</b>", ParagraphStyle('ST3', fontName='Helvetica-Bold', fontSize=18, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("Mudou a programação do teatro ou o horário do almoço? Altere na nuvem uma única vez e todas as centenas de plaquinhas atualizam no mesmo segundo.", style_body)
    ]

    t_passos = Table([[p1, p2, p3]], colWidths=[360, 360, 380])
    t_passos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, LINE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 26),
        ('BOTTOMPADDING', (0,0), (-1,-1), 26),
        ('LEFTPADDING', (0,0), (-1,-1), 22),
        ('RIGHTPADDING', (0,0), (-1,-1), 22),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    destaque_box = Table([[
        Paragraph("<b>O cartão físico guarda apenas um link seguro e vitalício.</b> Toda a inteligência e o conteúdo vivem na nuvem da AH3, garantindo que o resort nunca mais precise reimprimir material por mudança de horário ou serviço.", ParagraphStyle('DText', fontName='Helvetica', fontSize=15, leading=22, textColor=NAVY_DARK, alignment=1))
    ]], colWidths=[1140])
    destaque_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GOLD_LIGHT),
        ('BOX', (0,0), (-1,-1), 1.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING', (0,0), (-1,-1), 25),
        ('RIGHTPADDING', (0,0), (-1,-1), 25),
    ]))

    story.extend(como_funciona)
    story.append(t_passos)
    story.append(Spacer(1, 35))
    story.append(destaque_box)

    # ==========================================
    # 4. PÁGINA DO CARTÃO (Slide 4)
    # ==========================================
    story.append(PageBreak())

    card_left = [
        Paragraph("CARTÃO 01 · COSTÃO GUEST EXPERIENCE", style_kicker),
        Paragraph("Para quem está hospedado no Costão.", style_title),
        Paragraph("Plaquinha inteligente em acrílico 10x10cm posicionada na cabeceira, mesa de trabalho ou aparador do apartamento. Um único ponto de contato que resolve 100% da estadia.", style_subtitle),
        Spacer(1, 10),
        Paragraph("<b>OS 4 PILARES INTEGRADOS NO CARTÃO:</b>", ParagraphStyle('PTitle', fontName='Helvetica-Bold', fontSize=14, textColor=NAVY_DARK, spaceAfter=14)),
        Paragraph("• <b>Costão SPA & Relax:</b> Agendamento direto de massagens, banhos e rituais L'Occitane.", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Shows & Programação:</b> Agenda diária de lazer, gincanas infantis e espetáculos noturnos.", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Restaurantes & Bares:</b> Cardápios, horários do buffet All-Inclusive e reservas especiais.", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Mapa & Guia Resort:</b> Senha do Wi-Fi, transporte interno de vans e trilhas ecológicas.", style_body),
        Spacer(1, 24),
        Paragraph("<font color='#5B6B7A'><i>Especificação: Formato 100×100mm, canto arredondado R6mm, gravação acrílica com chip NTAG213 resinado à prova d'água.</i></font>", ParagraphStyle('Spec', fontName='Helvetica', fontSize=12, leading=16))
    ]

    card_right = [
        RLImage(card_png_path, width=440, height=440)
    ]

    t_card_page = Table([[card_left, card_right]], colWidths=[650, 490])
    t_card_page.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(t_card_page)

    # ==========================================
    # 5. O QUE O CLIENTE VÊ (Slide 5)
    # ==========================================
    story.append(PageBreak())

    oque_ve_left = [
        Paragraph("O QUE O HÓSPEDE VÊ", style_kicker),
        Paragraph("Uma página personalizada, rápida e elegante.", style_title),
        Paragraph("Ao aproximar o smartphone do cartão, o hóspede é direcionado para a web-app oficial da sua estadia com a identidade visual completa do Costão do Santinho:", style_subtitle),
        Spacer(1, 10),
        Paragraph("• <b>Boas-vindas personalizadas</b> com acesso direto a reservas e canais de ajuda.", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Horários operacionais essenciais</b> (Café, Piscinas, Check-in/out, Vans).", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Atalhos rápidos para o All-Inclusive</b>, SPA e Vacation Club.", style_body),
        Spacer(1, 6),
        Paragraph("• <b>Agenda do dia em tempo real</b> com sincronização automática.", style_body),
        Spacer(1, 25),
        Table([[
            Paragraph("<font color='#AC182E'><b>NOVO: AVALIAÇÃO EM 1 CLIQUE</b></font><br/><font size=12>Convite sutil e estratégico para avaliar o resort no TripAdvisor/Google durante o momento de maior encantamento da estadia.</font>", ParagraphStyle('BoxEval', fontName='Helvetica', fontSize=13, leading=18, textColor=INK))
        ]], colWidths=[580], style=[
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF2F2')),
            ('BOX', (0,0), (-1,-1), 1.5, RED_ACCENT),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 16),
            ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ]),
        Spacer(1, 15),
        Paragraph("<font color='#5B6B7A' size=11><i>* Exemplo de página web interativa — conteúdo ilustrativo, a ser ajustado com a gerência do Costão do Santinho.</i></font>", ParagraphStyle('N1', fontName='Helvetica', fontSize=11))
    ]

    # Simulação visual de tela mobile com caixas e cores reais da Home do Costão
    tela_mockup = [
        Paragraph("<b>📱 INTERFACE WEB-APP MOBILE</b>", ParagraphStyle('M1', fontName='Helvetica-Bold', fontSize=13, textColor=MUTED, alignment=1, spaceAfter=10)),
        Table([
            [Paragraph("<b>COSTÃO DO SANTINHO</b><br/><font size=10 color='#F8AF35'>BEM-VINDO AO RESORT</font>", ParagraphStyle('MHead', fontName='Helvetica-Bold', fontSize=14, textColor=WHITE, alignment=1))],
            [Paragraph("<b>Wi-Fi:</b> Costão Guest &nbsp;•&nbsp; <b>Café:</b> 07h às 10h30", ParagraphStyle('MB1', fontName='Helvetica', fontSize=12, textColor=INK))],
            [Paragraph("<b>SPA L'OCCITANE:</b> Massagens & Rituais de Relax", ParagraphStyle('MB2', fontName='Helvetica-Bold', fontSize=12, textColor=RED_ACCENT))],
            [Paragraph("<b>ALL-INCLUSIVE:</b> Gastronomia, Drinks & Lazer", ParagraphStyle('MB3', fontName='Helvetica-Bold', fontSize=12, textColor=NAVY_DARK))],
            [Paragraph("<b>AGENDA HOJE:</b> 17h Dança &nbsp;•&nbsp; 19h Show &nbsp;•&nbsp; 20h Teatro", ParagraphStyle('MB4', fontName='Helvetica', fontSize=12, textColor=INK))],
            [Paragraph("★ ★ ★ ★ ★<br/><font size=11 color='#002B4A'><b>Avaliar no TripAdvisor</b></font>", ParagraphStyle('MB5', fontName='Helvetica-Bold', fontSize=13, textColor=GOLD, alignment=1))]
        ], colWidths=[380], style=[
            ('BACKGROUND', (0,0), (0,0), NAVY_DARK),
            ('BACKGROUND', (0,1), (0,1), WHITE),
            ('BACKGROUND', (0,2), (0,2), colors.HexColor('#FFF5F5')),
            ('BACKGROUND', (0,3), (0,3), colors.HexColor('#F0F7FF')),
            ('BACKGROUND', (0,4), (0,4), WHITE),
            ('BACKGROUND', (0,5), (0,5), GOLD_LIGHT),
            ('BOX', (0,0), (-1,-1), 2, NAVY_DARK),
            ('INNERGRID', (0,0), (-1,-1), 1, LINE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 16),
            ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ])
    ]

    t_oque_ve = Table([[oque_ve_left, tela_mockup]], colWidths=[680, 460])
    t_oque_ve.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(t_oque_ve)

    # ==========================================
    # 6. FOCO DO SERVIÇO: AVALIAÇÕES (Slide 6)
    # ==========================================
    story.append(PageBreak())

    avaliacoes_page = [
        Paragraph("O FOCO DO NOSSO SERVIÇO", style_kicker),
        Paragraph("Estadia memorável. Mais avaliações 5 estrelas. Liderança consolidada.", style_title),
        Paragraph("A reputação online no TripAdvisor e Google é o maior acelerador de reservas diretas. Facilitamos o caminho para o hóspede avaliar no segundo de maior satisfação.", style_subtitle),
        Spacer(1, 20)
    ]

    # Card de Avaliação em destaque
    box_stars = Table([[
        Paragraph("<b>AVALIAÇÃO DO HÓSPEDE</b><br/><font size=14 color='#5B6B7A'>Gostou da sua estadia no Costão do Santinho Resort?</font><br/><br/><font size=32 color='#F8AF35'>★ ★ ★ ★ ★</font><br/><br/><font size=14 color='#002B4A'><b>[ Avaliar no TripAdvisor / Google ]</b></font>", ParagraphStyle('StarB', fontName='Helvetica', fontSize=16, leading=22, textColor=NAVY_DARK, alignment=1))
    ]], colWidths=[700])
    box_stars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 2, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 25),
        ('BOTTOMPADDING', (0,0), (-1,-1), 25),
        ('LEFTPADDING', (0,0), (-1,-1), 30),
        ('RIGHTPADDING', (0,0), (-1,-1), 30),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))

    # 4 Etapas do ciclo virtuoso
    e1 = [Paragraph("<b>1. Estadia Fluida</b>", ParagraphStyle('E1', fontName='Helvetica-Bold', fontSize=15, textColor=NAVY_DARK, spaceAfter=6)), Paragraph("Sem filas, dúvidas sanadas no quarto e acesso fácil a todo o resort.", style_body)]
    e2 = [Paragraph("<b>2. Convite Certo</b>", ParagraphStyle('E2', fontName='Helvetica-Bold', fontSize=15, textColor=GOLD, spaceAfter=6)), Paragraph("O hóspede encontra o botão de avaliação após uma experiência positiva.", style_body)]
    e3 = [Paragraph("<b>3. Mais Reviews</b>", ParagraphStyle('E3', fontName='Helvetica-Bold', fontSize=15, textColor=NAVY_DARK, spaceAfter=6)), Paragraph("Aumento expressivo no volume e frequência de notas 5 estrelas.", style_body)]
    e4 = [Paragraph("<b>4. Ranking & Vendas</b>", ParagraphStyle('E4', fontName='Helvetica-Bold', fontSize=15, textColor=RED_ACCENT, spaceAfter=6)), Paragraph("Melhor posicionamento nos motores de busca e mais reservas diretas.", style_body)]

    t_etapas = Table([[e1, e2, e3, e4]], colWidths=[270, 270, 270, 270])
    t_etapas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, LINE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.extend(avaliacoes_page)
    story.append(box_stars)
    story.append(Spacer(1, 40))
    story.append(t_etapas)

    # ==========================================
    # 7. POR QUE VALE PARA O NEGÓCIO (Slide 7)
    # ==========================================
    story.append(PageBreak())

    pq_vale = [
        Paragraph("POR QUE VALE PARA O COSTÃO DO SANTINHO", style_kicker),
        Paragraph("Menos atrito operacional, mais faturamento e sofisticação.", style_title),
        Paragraph("A implementação das plaquinhas inteligentes entrega retorno imediato em 4 frentes estratégicas da governança e recepção:", style_subtitle),
        Spacer(1, 30)
    ]

    b1 = [
        Paragraph("<b>INFORMAÇÃO 100% EXATA</b>", ParagraphStyle('B1T', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("Zero impressos obsoletos. Qualquer alteração de programação, clima ou regras de restaurantes é refletida instantaneamente.", style_body)
    ]
    b2 = [
        Paragraph("<b>EQUIPE LEVE E FOCO EM ATENDER</b>", ParagraphStyle('B2T', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY_DARK, spaceAfter=8)),
        Paragraph("A recepção e o time de conciergerie deixam de ser 'balcão de informações repetitivas' para focar em relacionamento de alto padrão.", style_body)
    ]
    b3 = [
        Paragraph("<b>VENDA CRUZADA DE SERVIÇOS</b>", ParagraphStyle('B3T', fontName='Helvetica-Bold', fontSize=16, textColor=RED_ACCENT, spaceAfter=8)),
        Paragraph("Aumento imediato de agendamentos no SPA L'Occitane, adesão ao Vacation Club e consumo nos bares da praia e piscina.", style_body)
    ]
    b4 = [
        Paragraph("<b>PERCEPÇÃO DE MODERNIDADE</b>", ParagraphStyle('B4T', fontName='Helvetica-Bold', fontSize=16, textColor=GOLD, spaceAfter=8)),
        Paragraph("Reforça o posicionamento do Costão como resort contemporâneo de ponta, integrando tecnologia invisível ao luxo à beira-mar.", style_body)
    ]

    t_4beneficios = Table([
        [b1, b2],
        [b3, b4]
    ], colWidths=[550, 550])
    t_4beneficios.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, LINE_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 1, LINE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
        ('LEFTPADDING', (0,0), (-1,-1), 24),
        ('RIGHTPADDING', (0,0), (-1,-1), 24),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    story.extend(pq_vale)
    story.append(t_4beneficios)

    # ==========================================
    # 8. PRÓXIMOS PASSOS E INVESTIMENTO (Slide 8)
    # ==========================================
    story.append(PageBreak())

    prox_passos_left = [
        Paragraph("PRÓXIMOS PASSOS", style_kicker),
        Paragraph("Vamos testar juntos no resort?", style_title),
        Paragraph("Estrutura completa de implantação piloto ou total, com acompanhamento de dados de uso e suporte técnico dedicado:", style_subtitle),
        Spacer(1, 10),
        Paragraph("<b>1. Validação de Conteúdo:</b> Reunião rápida de alinhamento com a gerência para refinamento final dos links e serviços.", style_body),
        Spacer(1, 10),
        Paragraph("<b>2. Produção e Envio:</b> Fabricação das plaquinhas com corte laser, resina protetora e chips configurados.", style_body),
        Spacer(1, 10),
        Paragraph("<b>3. Ativação e Treinamento:</b> Entrega dos painéis de controle e treinamento rápido da equipe de recepção/concierge.", style_body),
        Spacer(1, 25),
        Paragraph("<b>GARANTIA VITALÍCIA:</b> Substituição imediata de qualquer peça com falha física de leitura NFC.", ParagraphStyle('Garantia', fontName='Helvetica-Bold', fontSize=13, textColor=NAVY_DARK))
    ]

    investimento_box = [
        Paragraph("<b>PROPOSTA DE IMPLANTAÇÃO</b>", ParagraphStyle('InvK', fontName='Helvetica-Bold', fontSize=13, textColor=GOLD, alignment=1, spaceAfter=8)),
        Paragraph("<b>LOTE PILOTO RESORT (100 CARTÕES)</b>", ParagraphStyle('InvT', fontName='Helvetica-Bold', fontSize=18, textColor=NAVY_DARK, alignment=1, spaceAfter=14)),
        Paragraph("<font size=32 color='#002B4A'><b>R$ 4.900,00</b></font>", ParagraphStyle('InvVal', fontName='Helvetica-Bold', fontSize=32, alignment=1, spaceAfter=12)),
        Paragraph("• 100 Cartões Acrílicos 10x10cm Personalizados<br/>• Programação NFC NTAG213 e Criptografia<br/>• Hospedagem Dedicada & Painel de Atualização AH3<br/>• Suporte técnico e atualizações ilimitadas na nuvem", ParagraphStyle('InvItens', fontName='Helvetica', fontSize=13, leading=20, textColor=INK)),
        Spacer(1, 14),
        Paragraph("<font size=11 color='#5B6B7A'><i>Condições: 50% na aprovação / 50% na entrega final.<br/>Prazo de produção: 7 a 10 dias úteis.</i></font>", ParagraphStyle('InvCond', fontName='Helvetica', fontSize=11, leading=16, alignment=1)),
        Spacer(1, 15),
        Table([[
            Paragraph("<b>VAMOS CONVERSAR?</b><br/><font size=12>Equipe de Parcerias Estratégicas AH3<br/>contato@ah3intelligence.com.br</font>", ParagraphStyle('ContatoB', fontName='Helvetica-Bold', fontSize=13, textColor=WHITE, alignment=1))
        ]], colWidths=[380], style=[
            ('BACKGROUND', (0,0), (-1,-1), NAVY_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ])
    ]

    t_invest = Table([[
        prox_passos_left,
        Table([[investimento_box]], style=[
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 2, GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 20),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ('LEFTPADDING', (0,0), (-1,-1), 20),
            ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ])
    ]], colWidths=[660, 480])
    t_invest.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(t_invest)

    # Build PDF
    pdf.build(story, canvasmaker=NumberedCanvas, onFirstPage=draw_cover_bg)
    print("PDF successfully generated at:", output_pdf_path)

if __name__ == "__main__":
    pdf_out = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf"
    card_png = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_card_10x10.png"
    logo_png = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/01_costao_do_santinho_logo.png"
    create_proposal_pdf(pdf_out, card_png, logo_png)

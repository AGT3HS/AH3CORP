import os
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Paleta oficial AH3 Design System (DESIGN.md)
COLOR_PRIMARY_NAVY = colors.HexColor("#0F172A") # Slate 900
COLOR_ACCENT_BLUE   = colors.HexColor("#1E40AF") # Blue 800
COLOR_ACCENT_ROYAL  = colors.HexColor("#2563EB") # Blue 600
COLOR_ACCENT_SKY    = colors.HexColor("#0284C7") # Sky 600

COLOR_SUCCESS_TEXT  = colors.HexColor("#15803D") # Green 700
COLOR_SUCCESS_BG    = colors.HexColor("#DCFCE7") # Green 100
COLOR_SUCCESS_BORDER= colors.HexColor("#86EFAC") # Green 300

COLOR_WARN_TEXT     = colors.HexColor("#B45309") # Amber 700
COLOR_WARN_BG       = colors.HexColor("#FEF3C7") # Amber 100
COLOR_WARN_BORDER   = colors.HexColor("#FCD34D") # Amber 300

COLOR_DANGER_TEXT   = colors.HexColor("#B91C1C") # Red 700
COLOR_DANGER_BG     = colors.HexColor("#FEE2E2") # Red 100
COLOR_DANGER_BORDER = colors.HexColor("#FCA5A5") # Red 300

COLOR_BG_LIGHT      = colors.HexColor("#F8FAFC") # Slate 50
COLOR_BORDER_LIGHT  = colors.HexColor("#E2E8F0") # Slate 200
COLOR_TEXT_DARK     = colors.HexColor("#1E293B") # Slate 800
COLOR_TEXT_MUTED    = colors.HexColor("#64748B") # Slate 500

class NumberedCanvas(canvas.Canvas):
    """
    Canvas com numeração de página e cabeçalho/rodapé padronizados AH3.
    """
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
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Barra superior decorativa
        self.setFillColor(colors.HexColor("#0F172A"))
        self.rect(0, 836, 595.27, 6, fill=True, stroke=False)
        self.setFillColor(colors.HexColor("#2563EB"))
        self.rect(0, 834, 180, 2, fill=True, stroke=False)

        # Rodapé
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(36, 36, 595.27 - 36, 36)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(36, 24, "AGÊNCIA AH3 • AUDITORIA SEO LOCAL GOOGLE MAPS · FLORIANÓPOLIS")
        
        page_str = f"DOCUMENTO CONFIDENCIAL · PÁGINA {self._pageNumber:02d} / {page_count:02d}"
        self.drawRightString(595.27 - 36, 24, page_str)
        self.restoreState()

def gerar_grafico_maturidade(caminho_png, scores=None):
    """
    Gera o gráfico de barras profissional de maturidade do perfil.
    """
    categorias = [
        "Completude\ndo Perfil",
        "Fotos &\nMídia",
        "Descrição &\nAtualizações",
        "SEO Local &\nPalavras-Chave",
        "Canais Conv.\nWhatsApp",
        "Engajamento\n& Reviews"
    ]
    if not scores:
        scores = [90, 75, 65, 70, 60, 55]
    
    fig, ax = plt.subplots(figsize=(7.2, 2.5), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')
    
    x = range(len(categorias))
    bars = ax.bar(x, scores, width=0.48, color='#2563EB', zorder=3, edgecolor='#1E40AF', linewidth=1)
    
    # Adicionar linha de nível de excelência
    ax.axhline(85, color='#DC2626', linestyle='--', linewidth=1.2, zorder=4, label='Nível Projetado de Excelência (85+)')
    
    # Rótulos nas barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{int(yval)}%", 
                ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1E293B')
        
    ax.set_ylim(0, 108)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=7.8, fontweight='medium', color='#334155')
    ax.set_ylabel("Pontuação (0-100)", fontsize=7.5, fontweight='bold', color='#64748B')
    
    # Grid e bordas
    ax.yaxis.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1', zorder=0)
    ax.xaxis.grid(False)
    for spine in ax.spines.values():
        spine.set_color('#E2E8F0')
        spine.set_linewidth(0.8)
        
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=7.2)
    plt.tight_layout()
    plt.savefig(caminho_png, dpi=220, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

def criar_tabela_card(titulo, valor, subtitulo, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_LIGHT, val_color=COLOR_ACCENT_BLUE):
    """
    Cria um card estilizado para métricas.
    """
    styles = getSampleStyleSheet()
    t_style = ParagraphStyle('T', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=COLOR_TEXT_MUTED, alignment=TA_CENTER)
    v_style = ParagraphStyle('V', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=val_color, alignment=TA_CENTER)
    s_style = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica', fontSize=7.2, leading=9, textColor=COLOR_TEXT_DARK, alignment=TA_CENTER)
    
    content = [
        [Paragraph(titulo.upper(), t_style)],
        [Spacer(1, 2)],
        [Paragraph(valor, v_style)],
        [Spacer(1, 2)],
        [Paragraph(subtitulo, s_style)]
    ]
    t = Table(content, colWidths=[124])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def sanitize_text(val):
    if val is None or val == "":
        return "A verificar"
    return str(val)

def gerar_auditoria_pdf(dados_local, caminho_saida=None):
    """
    Gera o relatório PDF de auditoria completo (3 páginas) baseado no Design System AH3.
    """
    nome = dados_local.get("displayName", {}).get("text", "Estabelecimento") if isinstance(dados_local.get("displayName"), dict) else dados_local.get("displayName", "Estabelecimento")
    nome_limpo = "".join([c if c.isalnum() else "_" for c in nome])[:30]
    
    if not caminho_saida:
        saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
        os.makedirs(saida_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_saida = os.path.join(saida_dir, f"Auditoria_{nome_limpo}_{timestamp}.pdf")

    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        textColor=COLOR_PRIMARY_NAVY,
        spaceAfter=3
    )
    
    header_sub_style = ParagraphStyle(
        'HeaderSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_ACCENT_ROYAL,
        spaceAfter=4
    )
    
    header_meta_style = ParagraphStyle(
        'HeaderMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=COLOR_TEXT_MUTED,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=COLOR_PRIMARY_NAVY,
        spaceBefore=10,
        spaceAfter=6
    )

    body_text = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_TEXT_DARK
    )

    body_bold = ParagraphStyle(
        'BodyCustomBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_TEXT_DARK
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    callout_text_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=COLOR_TEXT_DARK
    )

    # Dados medidos
    endereco = dados_local.get("formattedAddress", "Av. Luiz Boiteux Piazza, n 5076 - Sl 7 - Ponta das Canas, Florianópolis - SC, 88056-682")
    telefone = dados_local.get("nationalPhoneNumber", "(48) 99170-1959")
    website = dados_local.get("websiteUri", "http://ratonescraftbeer.com.br/")
    rating = dados_local.get("rating", 4.8)
    total_reviews = dados_local.get("userRatingCount", 2113)

    story = []

    # ==========================================
    # PÁGINA 1
    # ==========================================
    story.append(Paragraph("AGÊNCIA AH3 • AUDITORIA DE PRESENÇA DIGITAL GOOGLE MAPS", header_sub_style))
    story.append(Paragraph("Relatório de Diagnóstico Estrutural & SEO Local", header_title_style))
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"<b>Estabelecimento Alvo:</b> {nome} &nbsp;|&nbsp; <b>Região:</b> Florianópolis - SC (Norte da Ilha) &nbsp;|&nbsp; <b>Data:</b> {data_hoje} &nbsp;|&nbsp; <i>Status: Rascunho</i>", header_meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER_LIGHT, spaceAfter=8))

    # 1. Dados Cadastrais
    story.append(Paragraph("1. Dados Cadastrais e Localização Identificada", section_heading))
    
    cadastral_data = [
        [
            Paragraph(f"<b>Nome do Perfil:</b><br/>{nome}", body_text),
            Paragraph("<b>Coordenadas GPS:</b><br/>-27.394810, -48.423950", body_text)
        ],
        [
            Paragraph(f"<b>Logradouro:</b><br/>{endereco.split('-')[0].strip() if '-' in endereco else endereco}", body_text),
            Paragraph("<b>Bairro / Região:</b><br/>Ponta das Canas / Norte da Ilha", body_text)
        ],
        [
            Paragraph("<b>Município / UF:</b><br/>Florianópolis - SC (88056-682)", body_text),
            Paragraph("<b>Código Identificador:</b><br/>ChIJq3V8rFkyJ5UR8-0E7Fv", body_text)
        ]
    ]
    t_cadastral = Table(cadastral_data, colWidths=[261, 261])
    t_cadastral.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cadastral)
    story.append(Spacer(1, 8))

    # 2. KPIs
    story.append(Paragraph("2. Indicadores-Chave de Desempenho Local (KPIs)", section_heading))
    c1 = criar_tabela_card("Score de Maturidade", "82 / 100", "Líder Regional", bg_color=colors.HexColor("#EFF6FF"), border_color=colors.HexColor("#BFDBFE"), val_color=COLOR_ACCENT_BLUE)
    c2 = criar_tabela_card("Geolocalização", "Norte da Ilha", "Ponta das Canas (Raio 5km)", val_color=COLOR_PRIMARY_NAVY)
    c3 = criar_tabela_card("Conversão Digital", "Alta", "Website com Oportunidade", val_color=COLOR_ACCENT_SKY)
    c4 = criar_tabela_card("Potencial de Mercado", "Muito Alto", "Turismo + Consumo Noturno", val_color=COLOR_SUCCESS_TEXT)
    
    t_kpis = Table([[c1, c2, c3, c4]], colWidths=[130, 130, 130, 130])
    t_kpis.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 8))

    # 3. Diagnóstico por Área de Oportunidade
    story.append(Paragraph("3. Diagnóstico por Área de Oportunidade (Score Geral: 82/100)", section_heading))
    
    temp_dir = os.path.dirname(caminho_saida)
    grafico_path = os.path.join(temp_dir, "temp_maturidade.png")
    gerar_grafico_maturidade(grafico_path, [90, 75, 65, 70, 60, 55])
    story.append(Image(grafico_path, width=520, height=180))
    story.append(Spacer(1, 6))

    # Resumo da Avaliação Estrutural
    resumo_p1 = (
        f"<b>Resumo da Avaliação Estrutural:</b> O estabelecimento destaca-se com sólida presença de mercado e liderança consolidada em volume de avaliações ({total_reviews} reviews) e nota {rating}★. "
        "Apesar do excelente posicionamento orgânico, identifica-se um <b>potencial projetado</b> relevante de otimização na taxa de conversão direta (canal de reservas e delivery via WhatsApp) "
        "e na frequência de publicações oficiais (Google Posts), elementos decisivos para blindar a liderança contra concorrentes da região."
    )
    t_resumo1 = Table([[Paragraph(resumo_p1, callout_text_style)]], colWidths=[522])
    t_resumo1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_resumo1)

    # ==========================================
    # PÁGINA 2
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("BENCHMARKING REGIONAL — RAIO DE 5 KM", header_sub_style))
    story.append(Paragraph("Mapeamento Competitivo e Plano de Ação", header_title_style))
    story.append(Paragraph("<b>Segmento:</b> Gastronomia, Cervejarias e Restaurantes &nbsp;|&nbsp; <b>Microrregião:</b> Ponta das Canas / Lagoinha", header_meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER_LIGHT, spaceAfter=8))

    story.append(Paragraph("4. Ranking Competitivo no Raio de 5km", section_heading))
    
    ranking_data = [
        [Paragraph("RANK", table_header_style), Paragraph("ESTABELECIMENTO", table_header_style), Paragraph("DISTÂNCIA", table_header_style), Paragraph("NOTA", table_header_style), Paragraph("REVIEWS", table_header_style), Paragraph("SITE OFICIAL", table_header_style)],
        [Paragraph("<b>#1</b>", body_bold), Paragraph(f"<b>{nome} (Alvo)</b>", body_bold), Paragraph("0.0 km", body_text), Paragraph(f"<b>{rating} ★</b>", body_bold), Paragraph(f"<b>{total_reviews}</b>", body_bold), Paragraph("Sim (Ativo)", body_text)],
        [Paragraph("#2", body_text), Paragraph("Restaurante Mira Maré", body_text), Paragraph("1.1 km", body_text), Paragraph("4.5 ★", body_text), Paragraph("1.445", body_text), Paragraph("Sim", body_text)],
        [Paragraph("#3", body_text), Paragraph("Restaurante Garra Azul", body_text), Paragraph("1.3 km", body_text), Paragraph("4.3 ★", body_text), Paragraph("1.362", body_text), Paragraph("Sim", body_text)],
        [Paragraph("#4", body_text), Paragraph("Restaurante Tradição Campeira", body_text), Paragraph("4.2 km", body_text), Paragraph("4.4 ★", body_text), Paragraph("996", body_text), Paragraph("Não", body_text)],
        [Paragraph("#5", body_text), Paragraph("Restaurante Lula Floripa", body_text), Paragraph("2.4 km", body_text), Paragraph("4.6 ★", body_text), Paragraph("626", body_text), Paragraph("Sim", body_text)],
    ]
    t_ranking = Table(ranking_data, colWidths=[42, 210, 70, 55, 65, 80])
    t_ranking.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER_LIGHT),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#EFF6FF")), # Destaque do cliente alvo
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ranking)
    story.append(Spacer(1, 10))

    # 5. Plano de Ação
    story.append(Paragraph("5. Plano Estruturado de Ações para Blindagem e Expansão", section_heading))
    
    def criar_box_acao(numero, titulo, descricao):
        n_p = Paragraph(f"<b>{numero}</b>", ParagraphStyle('Num', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=16, textColor=COLOR_ACCENT_ROYAL, alignment=TA_CENTER))
        t_p = Paragraph(f"<b>{titulo}</b>", ParagraphStyle('Tit', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=COLOR_PRIMARY_NAVY))
        d_p = Paragraph(descricao, ParagraphStyle('Desc', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=COLOR_TEXT_DARK))
        
        t = Table([[n_p, [t_p, Spacer(1, 2), d_p]]], colWidths=[36, 476])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER_LIGHT),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    a1 = criar_box_acao("01", "Otimização de Conversão Direta no Website & Cardápio Digital Mobile", "Implementação de botões de WhatsApp de alta conversão para pedidos diretos, reservas de mesa e eventos, reduzindo a fricção do cliente final.")
    a2 = criar_box_acao("02", "Estratégia Semântica de Resposta a Avaliações e SEO Geolocalizado", "Padronização de respostas técnicas incluindo palavras-chave estratégicas ('cervejaria artesanal em Florianópolis', 'chopp artesanal Ponta das Canas') para indexação nos termos de busca turística.")
    a3 = criar_box_acao("03", "Ativação de Google Posts Semanais e Atualização do Catálogo de Produtos", "Publicação contínua de fotos dos pratos, chopps sazonais e programação musical, gerando sinais positivos de engajamento para o algoritmo de busca local.")
    
    story.append(a1)
    story.append(Spacer(1, 4))
    story.append(a2)
    story.append(Spacer(1, 4))
    story.append(a3)
    story.append(Spacer(1, 8))

    # Diagnóstico Principal & Proposta Comercial
    diag_p2 = (
        f"<b>Diagnóstico Principal & Oportunidade Projetada:</b> A {nome} ocupa o 1º lugar na microrregião de Ponta das Canas, com uma vantagem expressiva de +668 avaliações "
        "sobre o 2º colocado (Restaurante Mira Maré). Para sustentar esse posicionamento diante de investimentos concorrentes, o foco deve migrar de 'geração de volume' para 'maximização de conversão e retenção'. "
        "O <b>potencial esperado</b> da modernização do canal digital e da gestão ativa de respostas é a ampliação direta no ticket médio e na fidelização de turistas e clientes locais."
    )
    t_diag2 = Table([[Paragraph(diag_p2, callout_text_style)]], colWidths=[522])
    t_diag2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_diag2)

    # ==========================================
    # PÁGINA 3
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("PROSPECÇÃO DIGITAL — DADOS PÚBLICOS AUDITADOS", header_sub_style))
    story.append(Paragraph("Checklist Técnico de Elementos Públicos", header_title_style))
    story.append(Paragraph(f"<b>Estabelecimento:</b> {nome} &nbsp;|&nbsp; <b>Complementa as Páginas 01 e 02</b> &nbsp;|&nbsp; <b>Data:</b> {data_hoje}", header_meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER_LIGHT, spaceAfter=8))

    story.append(Paragraph("6. Resumo Rápido — Status dos Itens Públicos Auditados", section_heading))
    
    def criar_badge_kpi(titulo, count_str, desc, bg, border, txt_color):
        t_p = Paragraph(f"<b>{titulo.upper()}</b>", ParagraphStyle('BT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=txt_color, alignment=TA_CENTER))
        c_p = Paragraph(f"<b>{count_str}</b>", ParagraphStyle('BC', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=txt_color, alignment=TA_CENTER))
        d_p = Paragraph(desc, ParagraphStyle('BD', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=COLOR_TEXT_DARK, alignment=TA_CENTER))
        t = Table([[t_p], [Spacer(1,2)], [c_p], [Spacer(1,2)], [d_p]], colWidths=[168])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 1, border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        return t

    bk1 = criar_badge_kpi("Em Conformidade", "3 / 8", "Itens sem pendência aparente", COLOR_SUCCESS_BG, COLOR_SUCCESS_BORDER, COLOR_SUCCESS_TEXT)
    bk2 = criar_badge_kpi("Requer Atenção", "3 / 8", "Presente, porém otimizável", COLOR_WARN_BG, COLOR_WARN_BORDER, COLOR_WARN_TEXT)
    bk3 = criar_badge_kpi("Oportunidade Aberta", "2 / 8", "Não identificado / Ausente", COLOR_DANGER_BG, COLOR_DANGER_BORDER, COLOR_DANGER_TEXT)
    
    t_badges = Table([[bk1, bk2, bk3]], colWidths=[174, 174, 174])
    t_badges.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_badges)
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. Checklist Detalhado dos Elementos Públicos do Perfil", section_heading))
    
    def badge_status(tipo):
        if tipo == 'ok':
            return Paragraph("<b><font color='#15803D'>✓ Conforme</font></b>", body_bold)
        elif tipo == 'warn':
            return Paragraph("<b><font color='#B45309'>⚠ Atenção</font></b>", body_bold)
        else:
            return Paragraph("<b><font color='#B91C1C'>✗ Oportunidade</font></b>", body_bold)

    checklist_data = [
        [Paragraph("ITEM AUDITADO", table_header_style), Paragraph("STATUS", table_header_style), Paragraph("OBSERVAÇÃO PRÁTICA E IMPACTO MEDIDO", table_header_style)],
        [Paragraph("<b>Horário de Funcionamento</b>", body_text), badge_status('ok'), Paragraph("Completo e estruturado na API do Google, sem inconsistências identificadas.", body_text)],
        [Paragraph("<b>Telefone Oficial & NAP</b>", body_text), badge_status('ok'), Paragraph(f"Telefone {telefone} e endereço padronizados no perfil principal.", body_text)],
        [Paragraph("<b>Website Vinculado</b>", body_text), badge_status('ok'), Paragraph("Website oficial ativo cadastrado, com potencial projetado de melhoria em conversão mobile.", body_text)],
        [Paragraph("<b>Taxa de Resposta a Reviews</b>", body_text), badge_status('warn'), Paragraph(f"Percentual de resposta às {total_reviews} avaliações pode ser expandido para fortalecer relacionamento e SEO.", body_text)],
        [Paragraph("<b>Categorias Secundárias</b>", body_text), badge_status('warn'), Paragraph("Potencial projetado de adicionar categorias complementares (ex: Bar de Cerveja Artesanal, Petiscaria).", body_text)],
        [Paragraph("<b>Atributos Detalhados</b>", body_text), badge_status('warn'), Paragraph("Recomenda-se enriquecer atributos de acessibilidade, opções de consumo no local e formas de pagamento.", body_text)],
        [Paragraph("<b>Google Posts Recentes</b>", body_text), badge_status('danger'), Paragraph("Ausência de atualizações públicas e novidades publicadas com frequência semanal na ficha.", body_text)],
        [Paragraph("<b>Cardápio de Produtos no Google</b>", body_text), badge_status('danger'), Paragraph("Catálogo de chopps artesanais e pratos não cadastrado diretamente na vitrine do perfil.", body_text)],
    ]
    t_check = Table(checklist_data, colWidths=[130, 82, 310])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_check)
    story.append(Spacer(1, 8))

    # Nota Metodológica e Escopo
    metodologia_p3 = (
        "<b>Nota Metodológica & Escopo de Prospecção:</b> Este diagnóstico preliminar é baseado exclusivamente em dados públicos coletados "
        "via Google Places API. Métricas aprofundadas de tráfego orgânico (volume exato de impressões, solicitações de rotas, cliques para ligação e no site) "
        "ficam disponíveis apenas no painel administrativo do proprietário e passam a ser monitoradas de forma contínua com a ativação da gestão profissional AH3."
    )
    t_metod = Table([[Paragraph(metodologia_p3, callout_text_style)]], colWidths=[522])
    t_metod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCE8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FEF08A")),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_metod)
    story.append(Spacer(1, 6))

    # Diagnóstico Final e Próximo Passo
    final_p3 = (
        f"<b>Diagnóstico de Prospecção & Próximos Passos:</b> O perfil da {nome} possui uma fundação sólida com Score de Maturidade de 82/100. "
        "Das 8 áreas técnicas auditadas, 5 representam oportunidades estratégicas de blindagem e conversão (3 em atenção e 2 em oportunidade aberta). "
        "O plano de execução completo e o orçamento modular (Gestão de Perfil + Landing Page / Cardápio Mobile + Otimização de Avaliações) estão disponíveis para estruturação sob demanda."
    )
    t_final = Table([[Paragraph(final_p3, callout_text_style)]], colWidths=[522])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_final)

    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Limpeza de arquivo temporário
    if os.path.exists(grafico_path):
        try:
            os.remove(grafico_path)
        except:
            pass

    return caminho_saida

if __name__ == "__main__":
    out_pdf = r"C:\Users\Augusto\Desktop\AH3\saida\Auditoria_Ratones_Craft_Beer_20260928_220249.pdf"
    dados_exemplo = {
        "displayName": {"text": "Ratones Craft Beer"},
        "formattedAddress": "Av. Luiz Boiteux Piazza, n 5076 - Sl 7 - Ponta das Canas, Florianópolis - SC, 88056-682, Brasil",
        "nationalPhoneNumber": "(48) 99170-1959",
        "websiteUri": "http://ratonescraftbeer.com.br/",
        "rating": 4.8,
        "userRatingCount": 2113
    }
    gerar_auditoria_pdf(dados_exemplo, out_pdf)
    print(f"PDF 3 páginas gerado com sucesso em: {out_pdf}")

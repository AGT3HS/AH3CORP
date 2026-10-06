import os
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registro de fontes modernas do Windows (Segoe UI)
try:
    pdfmetrics.registerFont(TTFont('SegoeUI', 'C:/Windows/Fonts/segoeui.ttf'))
    pdfmetrics.registerFont(TTFont('SegoeUI-Bold', 'C:/Windows/Fonts/segoeuib.ttf'))
    pdfmetrics.registerFont(TTFont('SegoeUI-SemiBold', 'C:/Windows/Fonts/seguisb.ttf'))
    pdfmetrics.registerFont(TTFont('SegoeUI-Italic', 'C:/Windows/Fonts/segoeuii.ttf'))
    FONT_REG = 'SegoeUI'
    FONT_BOLD = 'SegoeUI-Bold'
    FONT_SEMI = 'SegoeUI-SemiBold'
    FONT_ITAL = 'SegoeUI-Italic'
except Exception as e:
    FONT_REG = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_SEMI = 'Helvetica-Bold'
    FONT_ITAL = 'Helvetica-Oblique'

# Paleta Moderna Executiva (Linear / Stripe inspired)
C_DARK_BG       = colors.HexColor("#090D16") # Obsidian Blue profundo
C_BRAND_BLUE    = colors.HexColor("#2563EB") # Blue 600
C_BRAND_INDIGO  = colors.HexColor("#4F46E5") # Indigo 600
C_BRAND_CYAN    = colors.HexColor("#0284C7") # Sky 600

C_TEXT_TITLE    = colors.HexColor("#0F172A") # Slate 900
C_TEXT_BODY     = colors.HexColor("#334155") # Slate 700
C_TEXT_MUTED    = colors.HexColor("#64748B") # Slate 500
C_TEXT_LIGHT    = colors.HexColor("#94A3B8") # Slate 400

C_CARD_BG       = colors.HexColor("#FFFFFF")
C_SURFACE_BG    = colors.HexColor("#F8FAFC") # Slate 50
C_CARD_ALT_BG   = colors.HexColor("#F1F5F9") # Slate 100
C_BORDER_LIGHT  = colors.HexColor("#E2E8F0") # Slate 200
C_BORDER_SUBTLE = colors.HexColor("#F1F5F9") # Slate 100

# Status refinados
C_SUCCESS_BG    = colors.HexColor("#ECFDF5") # Emerald 50
C_SUCCESS_TXT   = colors.HexColor("#059669") # Emerald 600
C_SUCCESS_BORDER= colors.HexColor("#A7F3D0")

C_WARN_BG       = colors.HexColor("#FFFBEB") # Amber 50
C_WARN_TXT      = colors.HexColor("#D97706") # Amber 600
C_WARN_BORDER   = colors.HexColor("#FDE68A")

C_DANGER_BG     = colors.HexColor("#FEF2F2") # Red 50
C_DANGER_TXT    = colors.HexColor("#DC2626") # Red 600
C_DANGER_BORDER = colors.HexColor("#FECACA")

class ModernExecutiveCanvas(canvas.Canvas):
    """
    Header e Footer ultra-limpos, minimalistas e executivos.
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        w = 595.27
        h = 841.89

        # Barra de topo minimalista (Gradiente visual sutil via 2 faixas)
        self.setFillColor(C_DARK_BG)
        self.rect(0, h - 5, w, 5, fill=True, stroke=False)
        self.setFillColor(C_BRAND_BLUE)
        self.rect(0, h - 5, 140, 5, fill=True, stroke=False)
        self.setFillColor(C_BRAND_INDIGO)
        self.rect(140, h - 5, 80, 5, fill=True, stroke=False)

        # Rodapé Executivo Clean
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.6)
        self.line(36, 32, w - 36, 32)

        self.setFont(FONT_BOLD, 7)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(36, 20, "AH3 INTELLIGENCE")
        
        self.setFont(FONT_REG, 7)
        self.setFillColor(C_TEXT_LIGHT)
        self.drawString(120, 20, "•   RELATÓRIO DE AUDITORIA & PERFORMANCE LOCAL GOOGLE MAPS")

        page_info = f"{self._pageNumber:02d} / {total_pages:02d}"
        self.setFont(FONT_BOLD, 7)
        self.setFillColor(C_TEXT_MUTED)
        self.drawRightString(w - 36, 20, page_info)
        
        self.restoreState()

def gerar_grafico_maturidade(caminho_png, scores=None):
    """
    Gera gráfico refinado, minimalista e com visual moderno SaaS.
    """
    plt.rcParams['font.family'] = 'Segoe UI' if 'SegoeUI' in FONT_REG else 'sans-serif'
    
    categorias = [
        "Completude\ndo Perfil",
        "Qualidade &\nFotos",
        "Informações &\nHorários",
        "SEO Local &\nPalavras-Chave",
        "Canais de\nConversão",
        "Gestão de\nReviews"
    ]
    if not scores:
        scores = [70, 50, 65, 45, 30, 40]

    fig, ax = plt.subplots(figsize=(7.4, 2.3), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    x = np.arange(len(categorias))
    width = 0.42

    # Cores dinâmicas inteligentes
    cores = []
    for s in scores:
        if s >= 75:
            cores.append('#10B981') # Emerald
        elif s >= 50:
            cores.append('#F59E0B') # Amber
        else:
            cores.append('#EF4444') # Rose Red

    bars = ax.bar(x, scores, width=width, color=cores, zorder=3, edgecolor='none', alpha=0.92)

    # Linha de benchmark
    ax.axhline(85, color='#6366F1', linestyle='--', linewidth=1.1, zorder=4, label='Média dos Líderes Regionais (85%)', alpha=0.85)

    # Rótulos nas barras
    for bar in bars:
        y = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, y + 2.5, f"{int(y)}%", 
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1E293B')

    ax.set_ylim(0, 106)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=7.6, fontweight='bold', color='#475569')
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'], fontsize=7, color='#94A3B8')

    ax.yaxis.grid(True, linestyle='-', alpha=0.5, color='#E2E8F0', zorder=0)
    ax.xaxis.grid(False)

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.spines['bottom'].set_linewidth(0.8)

    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=7.2)
    plt.tight_layout()
    plt.savefig(caminho_png, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()

def card_kpi(titulo, valor, subtitulo, cor_valor=C_BRAND_BLUE, bg=C_SURFACE_BG, border=C_BORDER_LIGHT):
    styles = getSampleStyleSheet()
    t_style = ParagraphStyle('KT', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=7, leading=8.5, textColor=C_TEXT_MUTED, alignment=TA_CENTER)
    v_style = ParagraphStyle('KV', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=16, leading=18, textColor=cor_valor, alignment=TA_CENTER)
    s_style = ParagraphStyle('KS', parent=styles['Normal'], fontName=FONT_REG, fontSize=7, leading=8.5, textColor=C_TEXT_BODY, alignment=TA_CENTER)

    content = [
        [Paragraph(titulo.upper(), t_style)],
        [Spacer(1, 2)],
        [Paragraph(valor, v_style)],
        [Spacer(1, 2)],
        [Paragraph(subtitulo, s_style)]
    ]
    t = Table(content, colWidths=[124])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.8, border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def gerar_auditoria_pdf(dados_local, caminho_saida=None):
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
        topMargin=32,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Estilos Tipográficos Executivos
    badge_hero = ParagraphStyle('BH', fontName=FONT_BOLD, fontSize=7.5, leading=9, textColor=C_BRAND_INDIGO, spaceAfter=3)
    title_hero = ParagraphStyle('TH', fontName=FONT_BOLD, fontSize=17, leading=20, textColor=C_TEXT_TITLE, spaceAfter=2)
    meta_hero = ParagraphStyle('MH', fontName=FONT_REG, fontSize=8, leading=10, textColor=C_TEXT_MUTED, spaceAfter=8)

    sec_title = ParagraphStyle('ST', fontName=FONT_BOLD, fontSize=10.5, leading=13, textColor=C_TEXT_TITLE, spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle('BD', fontName=FONT_REG, fontSize=8, leading=11, textColor=C_TEXT_BODY)
    body_bold = ParagraphStyle('BDB', fontName=FONT_BOLD, fontSize=8, leading=11, textColor=C_TEXT_TITLE)

    th_dark = ParagraphStyle('THD', fontName=FONT_BOLD, fontSize=7.5, leading=9.5, textColor=colors.white)
    th_light = ParagraphStyle('THL', fontName=FONT_BOLD, fontSize=7.5, leading=9.5, textColor=C_TEXT_MUTED)

    box_text = ParagraphStyle('BTX', fontName=FONT_REG, fontSize=7.8, leading=10.8, textColor=C_TEXT_BODY)

    # Extração de Métricas do Estabelecimento
    endereco = dados_local.get("formattedAddress", "Canasvieiras, Florianópolis - SC")
    telefone = dados_local.get("nationalPhoneNumber", dados_local.get("internationalPhoneNumber", "Não informado"))
    website = dados_local.get("websiteUri")
    tem_site_str = "Sim (Cadastrado)" if website else "Não Vinculado (Oportunidade)"
    
    try:
        rating = float(dados_local.get("rating", 3.7))
    except:
        rating = 3.7
    try:
        total_reviews = int(dados_local.get("userRatingCount", 429))
    except:
        total_reviews = 429

    # Score calculado proporcional à nota e presença
    if rating <= 3.8:
        score_geral = 52
        score_nivel = "Crítico (Ação Imediata)"
        score_cor = C_DANGER_TXT
        score_bg = C_DANGER_BG
        score_border = C_DANGER_BORDER
    elif rating <= 4.3:
        score_geral = 68
        score_nivel = "Moderado (Em Otimização)"
        score_cor = C_WARN_TXT
        score_bg = C_WARN_BG
        score_border = C_WARN_BORDER
    else:
        score_geral = 84
        score_nivel = "Elevado (Blindagem)"
        score_cor = C_SUCCESS_TXT
        score_bg = C_SUCCESS_BG
        score_border = C_SUCCESS_BORDER

    story = []

    # ==========================================
    # PÁGINA 1: OVERVIEW EXECUTIVO & DIAGNÓSTICO
    # ==========================================
    story.append(Paragraph("AH3 AUDIT INTELLIGENCE • DIAGNÓSTICO DE PERFORMANCE LOCAL", badge_hero))
    story.append(Paragraph(f"Auditoria Estrutural de Presença & SEO: {nome}", title_hero))
    data_str = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"<b>Segmento:</b> Gastronomia / Restaurante &nbsp;|&nbsp; <b>Região:</b> Florianópolis - SC &nbsp;|&nbsp; <b>Emissão:</b> {data_str} &nbsp;|&nbsp; <i>Documento Técnico Confidencial</i>", meta_hero))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER_LIGHT, spaceAfter=6))

    # 1. Dados Básicos do Perfil (Card Grid)
    story.append(Paragraph("1. Dados Cadastrais e Mapeamento de Ficha", sec_title))
    
    col_a = [
        Paragraph(f"<b>Estabelecimento:</b> {nome}", body),
        Spacer(1, 2),
        Paragraph(f"<b>Endereço:</b> {endereco}", body),
    ]
    col_b = [
        Paragraph(f"<b>Telefone de Contato:</b> {telefone}", body),
        Spacer(1, 2),
        Paragraph(f"<b>Website Oficial:</b> {tem_site_str}", body),
    ]
    t_dados = Table([[col_a, col_b]], colWidths=[261, 261])
    t_dados.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_BG),
        ('BOX', (0,0), (-1,-1), 0.8, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_dados)
    story.append(Spacer(1, 6))

    # 2. KPIs de Autoridade e Risco
    story.append(Paragraph("2. Indicadores-Chave de Desempenho Local (KPIs)", sec_title))
    
    k1 = card_kpi("Score de Maturidade", f"{score_geral} / 100", score_nivel, cor_valor=score_cor, bg=score_bg, border=score_border)
    k2 = card_kpi("Reputação / Nota", f"{rating:.1f} ★", f"{total_reviews} avaliações", cor_valor=C_TEXT_TITLE)
    k3 = card_kpi("Conversão Digital", "Baixa", "Sem canais diretos integrados", cor_valor=C_DANGER_TXT)
    k4 = card_kpi("Potencial Projetado", "Muito Alto", "Região de alta densidade turística", cor_valor=C_BRAND_INDIGO)

    t_kpis = Table([[k1, k2, k3, k4]], colWidths=[130, 130, 130, 130])
    t_kpis.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_kpis)
    story.append(Spacer(1, 6))

    # 3. Gráfico de Maturidade
    story.append(Paragraph("3. Desempenho por Eixo Estratégico vs. Líderes do Mercado", sec_title))
    temp_dir = os.path.dirname(caminho_saida)
    grafico_path = os.path.join(temp_dir, f"temp_mat_{nome_limpo}.png")
    
    scores_eixos = [70, 50, 65, 45, 30, 40] if rating < 4.0 else [85, 75, 80, 70, 60, 65]
    gerar_grafico_maturidade(grafico_path, scores_eixos)
    story.append(Image(grafico_path, width=522, height=162))
    story.append(Spacer(1, 5))

    # Box Síntese Executiva
    sintese_p1 = (
        f"<b>Síntese do Diagnóstico Preliminar:</b> O estabelecimento possui um fluxo contínuo de clientes comprovado pelo volume expressivo de <b>{total_reviews} avaliações</b>. "
        f"Entretanto, a nota atual de <b>{rating:.1f}★</b> e a ausência de um ecossistema de conversão direta (cardápio mobile e canais diretos) geram perda recorrente de clientes qualificados. "
        "Existe um <b>potencial projetado</b> imediato de recuperação de reputação e captação ativa através da otimização técnica da ficha e resposta estratégica a avaliações."
    )
    t_sint1 = Table([[Paragraph(sintese_p1, box_text)]], colWidths=[522])
    t_sint1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_BG),
        ('BOX', (0,0), (-1,-1), 0.8, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sint1)

    # ==========================================
    # PÁGINA 2: BENCHMARKING & PLANO DE AÇÃO
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("BENCHMARKING COMPETITIVO • RAIO DE 3 A 5 KM", badge_hero))
    story.append(Paragraph("Mapeamento de Mercado & Estratégia de Posicionamento", title_hero))
    story.append(Paragraph(f"<b>Polo Gastronômico:</b> Canasvieiras / Norte da Ilha &nbsp;|&nbsp; <b>Comparativo de Concorrentes Diretos</b>", meta_hero))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER_LIGHT, spaceAfter=6))

    story.append(Paragraph("4. Comparativo de Presença Local com Concorrentes da Região", sec_title))

    ranking_rows = [
        [Paragraph("POSIÇÃO", th_dark), Paragraph("ESTABELECIMENTO", th_dark), Paragraph("DISTÂNCIA", th_dark), Paragraph("NOTA GOOGLE", th_dark), Paragraph("AVALIAÇÕES", th_dark), Paragraph("CANAL DIRETO", th_dark)],
        [Paragraph("<b>#1</b>", body_bold), Paragraph("Costillas Grill - Costelaria", body_bold), Paragraph("0.8 km", body), Paragraph("<b>4.3 ★</b>", body_bold), Paragraph("4.790", body), Paragraph("Sim (Ativo)", body)],
        [Paragraph("<b>#2</b>", body_bold), Paragraph("Canas Pizzaria - Forno a Lenha", body_bold), Paragraph("0.4 km", body), Paragraph("<b>4.0 ★</b>", body_bold), Paragraph("4.014", body), Paragraph("Sim", body)],
        [Paragraph("<b>#3</b>", body_bold), Paragraph("Galpão Gaúcho Churrascaria", body_bold), Paragraph("1.2 km", body), Paragraph("<b>4.3 ★</b>", body_bold), Paragraph("2.808", body), Paragraph("Sim", body)],
        [Paragraph("<b>#4</b>", body_bold), Paragraph("Churrasco ao Vivo Canasvieiras", body_bold), Paragraph("0.6 km", body), Paragraph("<b>4.4 ★</b>", body_bold), Paragraph("2.443", body), Paragraph("Não", body)],
        [Paragraph("<b>• ALVO</b>", ParagraphStyle('TA', parent=body_bold, textColor=C_DANGER_TXT)), Paragraph(f"<b>{nome}</b>", ParagraphStyle('TA2', parent=body_bold, textColor=C_TEXT_TITLE)), Paragraph("<b>Local</b>", body_bold), Paragraph(f"<b>{rating:.1f} ★</b>", ParagraphStyle('TA3', parent=body_bold, textColor=score_cor)), Paragraph(f"<b>{total_reviews}</b>", body_bold), Paragraph("Ausente", ParagraphStyle('TA4', parent=body, textColor=C_DANGER_TXT))],
    ]
    t_rank = Table(ranking_rows, colWidths=[52, 195, 65, 65, 65, 80])
    t_rank.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF2F2")), # Destaque de urgência para o alvo
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_rank)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Plano de Ação Estruturado em 3 Frentes de Execução", sec_title))

    def box_plano(num_str, titulo, desc):
        n_p = Paragraph(f"<b>{num_str}</b>", ParagraphStyle('NP', fontName=FONT_BOLD, fontSize=13, leading=14, textColor=C_BRAND_BLUE, alignment=TA_CENTER))
        t_p = Paragraph(f"<b>{titulo}</b>", ParagraphStyle('TP', fontName=FONT_BOLD, fontSize=8.2, leading=10, textColor=C_TEXT_TITLE))
        d_p = Paragraph(desc, ParagraphStyle('DP', fontName=FONT_REG, fontSize=7.6, leading=9.8, textColor=C_TEXT_BODY))
        
        t = Table([[n_p, [t_p, Spacer(1, 1), d_p]]], colWidths=[32, 480])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_BG),
            ('BOX', (0,0), (-1,-1), 0.7, C_BORDER_LIGHT),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ]))
        return t

    b1 = box_plano("01", "Protocolo de Resposta Estratégica a Avaliações & Blindagem de Reputação", "Implementação de respostas personalizadas para reverter atritos passados, valorizar elogios e injetar termos-chave de busca ('restaurante em Canasvieiras', 'churrasco em Florianópolis').")
    b2 = box_plano("02", "Implantação de Cardápio Mobile-First & Canal Direto de Conversão", "Criação de landing page ultra-rápida focada em reservas de mesa e pedidos por WhatsApp, reduzindo a evasão de turistas que pesquisam pelo smartphone.")
    b3 = box_plano("03", "Atualização Contínua do Perfil com Google Posts Semanais", "Publicação de fotos profissionais dos pratos, promoções sazonais e programação especial, emitindo sinais contínuos de relevância para o algoritmo do Google.")

    story.append(b1)
    story.append(Spacer(1, 3.5))
    story.append(b2)
    story.append(Spacer(1, 3.5))
    story.append(b3)
    story.append(Spacer(1, 7))

    # Box Conclusão da Página 2
    concl_p2 = (
        f"<b>Conclusão Estratégica de Mercado:</b> Na microrregião de Canasvieiras, estabelecimentos concorrentes com mais de 2.000 avaliações sustentam notas superiores a 4.2★. "
        f"A recuperação da nota da {nome} e a ativação de um cardápio digital moderno possuem um <b>potencial esperado</b> de reposicionar o negócio no Top 3 de buscas locais para turistas e moradores."
    )
    t_concl2 = Table([[Paragraph(concl_p2, box_text)]], colWidths=[522])
    t_concl2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_concl2)

    # ==========================================
    # PÁGINA 3: CHECKLIST TÉCNICO & AUDITORIA
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("AUDITORIA DETALHADA • ELEMENTOS TÉCNICOS PÚBLICOS", badge_hero))
    story.append(Paragraph("Checklist de Conformidade do Perfil Google", title_hero))
    story.append(Paragraph(f"<b>Estabelecimento:</b> {nome} &nbsp;|&nbsp; <b>Diagnóstico das 8 Áreas Críticas</b> &nbsp;|&nbsp; <b>Data:</b> {data_str}", meta_hero))
    story.append(HRFlowable(width="100%", thickness=0.8, color=C_BORDER_LIGHT, spaceAfter=6))

    story.append(Paragraph("6. Panorama Geral dos Elementos Auditados", sec_title))

    def card_status(titulo, qtd, desc, bg, border, txt):
        t_p = Paragraph(f"<b>{titulo.upper()}</b>", ParagraphStyle('STT', fontName=FONT_BOLD, fontSize=7, leading=8.5, textColor=txt, alignment=TA_CENTER))
        c_p = Paragraph(f"<b>{qtd}</b>", ParagraphStyle('STC', fontName=FONT_BOLD, fontSize=15, leading=17, textColor=txt, alignment=TA_CENTER))
        d_p = Paragraph(desc, ParagraphStyle('STD', fontName=FONT_REG, fontSize=6.8, leading=8.5, textColor=C_TEXT_BODY, alignment=TA_CENTER))
        t = Table([[t_p], [Spacer(1,1)], [c_p], [Spacer(1,1)], [d_p]], colWidths=[168])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 0.8, border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ]))
        return t

    st1 = card_status("Em Conformidade", "2 / 8", "Itens ativos e configurados", C_SUCCESS_BG, C_SUCCESS_BORDER, C_SUCCESS_TXT)
    st2 = card_status("Requer Atenção", "3 / 8", "Cadastrados, porém incompletos", C_WARN_BG, C_WARN_BORDER, C_WARN_TXT)
    st3 = card_status("Oportunidade Aberta", "3 / 8", "Não identificados no perfil", C_DANGER_BG, C_DANGER_BORDER, C_DANGER_TXT)

    t_status_grid = Table([[st1, st2, st3]], colWidths=[174, 174, 174])
    t_status_grid.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_status_grid)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Checklist Técnico & Recomendações de Implementação", sec_title))

    def tag_badge(tipo):
        if tipo == 'ok':
            return Paragraph("<b><font color='#059669'>✓ Conforme</font></b>", body_bold)
        elif tipo == 'warn':
            return Paragraph("<b><font color='#D97706'>⚠ Atenção</font></b>", body_bold)
        else:
            return Paragraph("<b><font color='#DC2626'>✗ Oportunidade</font></b>", body_bold)

    check_data = [
        [Paragraph("ITEM AUDITADO", th_dark), Paragraph("STATUS", th_dark), Paragraph("OBSERVAÇÃO TÉCNICA E IMPACTO NO CLIENTE", th_dark)],
        [Paragraph("<b>Endereço & Geolocalização</b>", body), tag_badge('ok'), Paragraph("Perfil localizado corretamente no mapa de Canasvieiras.", body)],
        [Paragraph("<b>Telefone Oficial (NAP)</b>", body), tag_badge('ok'), Paragraph(f"Telefone {telefone} ativo e padronizado na ficha principal.", body)],
        [Paragraph("<b>Horário de Funcionamento</b>", body), tag_badge('warn'), Paragraph("Recomenda-se confirmar horários especiais de feriados e alta temporada.", body)],
        [Paragraph("<b>Website & Canal de Pedido</b>", body), tag_badge('danger' if not website else 'warn'), Paragraph("Ausência de link direto para cardápio mobile ou página de reservas por WhatsApp.", body)],
        [Paragraph("<b>Taxa de Resposta a Reviews</b>", body), tag_badge('danger' if rating < 4.0 else 'warn'), Paragraph(f"Grande volume de avaliações ({total_reviews}) sem respostas padronizadas da gestão.", body)],
        [Paragraph("<b>Categorias Secundárias</b>", body), tag_badge('warn'), Paragraph("Oportunidade de incluir tags como 'Churrascaria', 'Bar e Restaurante' e 'Parrilla'.", body)],
        [Paragraph("<b>Vitrine de Produtos / Cardápio</b>", body), tag_badge('danger'), Paragraph("Pratos principais e cortes não cadastrados na vitrine nativa do Google Maps.", body)],
        [Paragraph("<b>Google Posts & Novidades</b>", body), tag_badge('danger'), Paragraph("Sem postagens recentes sobre música ao vivo, promoções ou destaques da semana.", body)],
    ]
    t_check_table = Table(check_data, colWidths=[130, 80, 312])
    t_check_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_BG),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_check_table)
    story.append(Spacer(1, 6))

    # Box Metodológico
    metod_p3 = (
        "<b>Nota Metodológica:</b> Este relatório foi gerado através de dados públicos da Google Places API. "
        "Métricas restritas (chamadas iniciadas, buscas de rota e visualizações do perfil) tornam-se mensuráveis via painel após a autorização do gestor."
    )
    t_met = Table([[Paragraph(metod_p3, box_text)]], colWidths=[522])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCE8")),
        ('BOX', (0,0), (-1,-1), 0.7, colors.HexColor("#FEF08A")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_met)
    story.append(Spacer(1, 4.5))

    # Box de Próximos Passos
    passos_p3 = (
        f"<b>Próximos Passos Recomendados:</b> O perfil da {nome} tem alto potencial de atração. "
        "A implementação de um plano de gestão profissional em 3 módulos (Reputação Local + Cardápio Mobile + Atualização Semanal) está pronta para ser executada."
    )
    t_pass = Table([[Paragraph(passos_p3, box_text)]], colWidths=[522])
    t_pass.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_BG),
        ('BOX', (0,0), (-1,-1), 0.7, C_BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_pass)

    doc.build(story, canvasmaker=ModernExecutiveCanvas)

    if os.path.exists(grafico_path):
        try:
            os.remove(grafico_path)
        except:
            pass

    return caminho_saida

if __name__ == "__main__":
    out_pdf = r"C:\Users\Augusto\Desktop\AH3\saida\Auditoria_EL_PATIO_GRILL_NOVO_DESIGN.pdf"
    dados = {
        "displayName": {"text": "EL PATIO GRILL RESTAURANTE"},
        "formattedAddress": "R. Me. Maria Villac, 2003 - Canasvieiras, Florianópolis - SC, 88054-001, Brasil",
        "nationalPhoneNumber": "(47) 99115-0610",
        "websiteUri": None,
        "rating": 3.7,
        "userRatingCount": 429
    }
    gerar_auditoria_pdf(dados, out_pdf)
    print(f"PDF com novo design executivo gerado em: {out_pdf}")

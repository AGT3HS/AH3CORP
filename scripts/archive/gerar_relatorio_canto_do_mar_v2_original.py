import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group

# Cores exatas do design v2
C_BG_PAGE      = colors.HexColor("#FAFAF5") # Fundo bege claro suave
C_CARD_BG      = colors.HexColor("#FFFFFF") # Branco puro dos cards
C_DARK_HERO    = colors.HexColor("#1F2430") # Fundo azul-marinho escuro do Hero e CTA
C_ORANGE       = colors.HexColor("#F26A21") # Laranja vibrante de destaque e badges
C_GREEN        = colors.HexColor("#1E9E5A") # Verde de status / conformidade
C_AMBER        = colors.HexColor("#E8A317") # Âmbar / Atenção
C_RED          = colors.HexColor("#D6403A") # Vermelho / Crítico
C_BORDER       = colors.HexColor("#E5E1DA") # Borda sutil dos cards
C_TEXT_DARK    = colors.HexColor("#1F2430") # Texto principal quase preto
C_TEXT_MUTED   = colors.HexColor("#6B7280") # Texto secundário / cinza médio
C_BAR_BG       = colors.HexColor("#F1EEE9") # Fundo das barras cinza claro
C_CALLOUT_BG   = colors.HexColor("#FDEBDD") # Fundo suave do callout p1 e linha de destaque p2

W, H = A4 # 595.28, 841.89

class ReportBuilder:
    def __init__(self, filename):
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.filename = filename

    def draw_header_footer(self, page_num, subtitle_p, doc_subtitle):
        c = self.c
        # Fundo da página
        c.setFillColor(C_BG_PAGE)
        c.rect(0, 0, W, H, fill=True, stroke=False)
        
        # Linha laranja de topo
        c.setFillColor(C_ORANGE)
        c.rect(0, H - 6, W, 6, fill=True, stroke=False)
        
        # Header text
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(40, H - 32, f"AUDITORIA DE PRESENÇA DIGITAL  ·  {subtitle_p.upper()}")
        
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(40, H - 60, "Canto do Mar Ponta das Canas")
        
        c.setFont("Helvetica", 9.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(40, H - 76, doc_subtitle)
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(C_TEXT_DARK)
        c.drawRightString(W - 40, H - 32, f"Página 0{page_num} / 03")
        
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawRightString(W - 40, H - 46, "Florianópolis - SC  ·  04/10/2026")
        
        # Linha divisória header
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1.0)
        c.line(40, H - 92, W - 40, H - 92)
        
        # Linha divisória footer
        c.line(40, 38, W - 40, 38)
        
        c.setFont("Helvetica", 8)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(40, 24, "Prospecção Digital  ·  Canto do Mar Ponta das Canas")
        c.drawRightString(W - 40, 24, f"Página 0{page_num} / 03")
        
        # 3 Barrinhas centrais de paginação
        cx = W / 2.0 - 28
        for i in range(1, 4):
            c.setFillColor(C_ORANGE if i == page_num else C_BORDER)
            c.rect(cx + (i - 1) * 20, 22, 16, 4, fill=True, stroke=False)

    def draw_section_header(self, y_top, num_str, title_str, sub_str):
        c = self.c
        # Badge quadrada laranja
        c.setFillColor(C_ORANGE)
        c.rect(40, y_top - 20, 20, 20, fill=True, stroke=False)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.white)
        c.drawCentredString(50, y_top - 14, num_str)
        
        # Título
        c.setFont("Helvetica-Bold", 12.5)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(68, y_top - 15, title_str)
        
        # Subtítulo cinza ao lado
        tw = c.stringWidth(title_str, "Helvetica-Bold", 12.5)
        c.setFont("Helvetica", 9)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(74 + tw, y_top - 15, f"· {sub_str}")

    def draw_rounded_card(self, x, y, w, h, fill_color=C_CARD_BG, stroke_color=C_BORDER, line_width=0.8):
        c = self.c
        c.setFillColor(fill_color)
        c.setStrokeColor(stroke_color)
        c.setLineWidth(line_width)
        c.rect(x, y, w, h, fill=True, stroke=True)

    def build_page_1(self):
        c = self.c
        self.draw_header_footer(1, "Google Maps & Local SEO", "Diagnóstico estratégico de posicionamento e captação de clientes locais")
        
        # --- HERO BOX ---
        y_hero = H - 112
        h_hero = 92
        c.setFillColor(C_DARK_HERO)
        c.rect(40, y_hero - h_hero, W - 80, h_hero, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(60, y_hero - 22, "O QUE A AUDITORIA MOSTRA")
        
        c.setFont("Helvetica-Bold", 17)
        c.setFillColor(colors.white)
        c.drawString(60, y_hero - 46, "Você é o 9º no Google Maps da região.")
        
        c.setFont("Helvetica", 9.5)
        c.setFillColor(colors.HexColor("#D1D5DB"))
        c.drawString(60, y_hero - 66, "A nota é excelente (4,6), mas os 3 primeiros têm de 7 a 12 vezes mais avaliações. Volume e recência são")
        c.drawString(60, y_hero - 79, "o que separa você do Top 3.")
        
        # --- SEÇÃO 01: DADOS CADASTRAIS (NAP) ---
        y_sec1 = y_hero - h_hero - 14
        self.draw_section_header(y_sec1, "01", "Dados cadastrais", "Perfil Google Business")
        
        y_card1 = y_sec1 - 28
        h_card1 = 96
        self.draw_rounded_card(40, y_card1 - h_card1, W - 80, h_card1)
        
        # Linha 1: Nome, Categoria, Status
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 18, "NOME OFICIAL")
        c.drawString(250, y_card1 - 18, "CATEGORIA")
        c.drawString(430, y_card1 - 18, "STATUS")
        
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_card1 - 32, "Canto do Mar Ponta das Canas")
        c.drawString(250, y_card1 - 32, "Restaurante de Frutos do Mar")
        
        # Status verde com check
        c.setFillColor(C_GREEN)
        c.setStrokeColor(C_GREEN)
        c.setLineWidth(1.6)
        c.line(432, y_card1 - 28, 435, y_card1 - 25)
        c.line(435, y_card1 - 25, 439, y_card1 - 32)
        c.drawString(444, y_card1 - 32, "Perfil verificado")
        
        # Linha 2: Endereço
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 52, "ENDEREÇO")
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_card1 - 66, "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC, 88056-730")
        
        # Linha 3: Telefone, GPS, Região
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 82, "TELEFONE: (48) 3261-0872     GPS: -27.39836, -48.43072     Microrregião Norte da Ilha")

        # --- SEÇÃO 02: INDICADORES-CHAVE ---
        y_sec2 = y_card1 - h_card1 - 14
        self.draw_section_header(y_sec2, "02", "Indicadores-chave", "Métricas de relevância local")
        
        y_kpi = y_sec2 - 28
        h_kpi = 84
        w_kpi = (W - 80 - 30) / 4.0 # 4 cards
        
        kpis = [
            ("SCORE DE PRESENÇA", "58", " /100", "-16 pts vs. média do Top 3", "", C_ORANGE, C_ORANGE),
            ("TOTAL DE AVALIAÇÕES", "178", "", "Líder regional: 2.114", "", C_ORANGE, C_ORANGE),
            ("NOTA MÉDIA", "4,6", " ★", "Satisfação comprovada", "", C_ORANGE, C_ORANGE),
            ("POTENCIAL DE GANHO", "+42%", "", "Tráfego incremental no Top 3", "", C_GREEN, C_GREEN),
        ]
        
        for i, (k_label, k_val, k_unit, k_sub1, k_sub2, c_val, c_top) in enumerate(kpis):
            kx = 40 + i * (w_kpi + 10)
            self.draw_rounded_card(kx, y_kpi - h_kpi, w_kpi, h_kpi)
            # Faixa superior do card
            c.setFillColor(c_top)
            c.rect(kx, y_kpi - 4, w_kpi, 4, fill=True, stroke=False)
            
            c.setFont("Helvetica-Bold", 6.8)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(kx + 12, y_kpi - 18, k_label)
            
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(c_val)
            c.drawString(kx + 12, y_kpi - 48, k_val)
            
            if k_unit:
                vw = c.stringWidth(k_val, "Helvetica-Bold", 24)
                if "★" in k_unit:
                    c.setFont("Helvetica-Bold", 16)
                    c.setFillColor(colors.HexColor("#E8A317"))
                    c.drawString(kx + 12 + vw, y_kpi - 48, k_unit)
                else:
                    c.setFont("Helvetica", 10.5)
                    c.setFillColor(C_TEXT_MUTED)
                    c.drawString(kx + 12 + vw, y_kpi - 48, k_unit)
            
            c.setFont("Helvetica", 7.8)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(kx + 12, y_kpi - 66, k_sub1)

        # --- SEÇÃO 03: PILARES LOCAIS (GRÁFICO DIDÁTICO) ---
        y_sec3 = y_kpi - h_kpi - 14
        self.draw_section_header(y_sec3, "03", "Pilares locais", "Pontuação atual vs. meta de 80% (Top 3)")
        
        y_bars = y_sec3 - 28
        h_bars = 196
        self.draw_rounded_card(40, y_bars - h_bars, W - 80, h_bars)
        
        # Barras explicadas
        bars_data = [
            ("Dados Cadastrais (NAP)", "Consistência de Nome, Endereço e Tel.", 92, C_GREEN),
            ("Fotos do Perfil", "Qualidade visual da fachada e pratos", 72, C_AMBER),
            ("Volume de Avaliações", "Total acumulado de clientes (178)", 68, C_AMBER),
            ("Recência (Frequência)", "Ritmo de novas avaliações no mês", 40, C_RED),
            ("Taxa de Resposta (SAC)", "% de comentários respondidos", 22, C_RED),
            ("Cardápio Digital Próprio", "Menu mobile sem taxas/intermediários", 15, C_RED)
        ]
        
        bar_start_x = 210
        bar_max_w = 265
        
        for i, (b_name, b_desc, b_pct, b_color) in enumerate(bars_data):
            by = y_bars - 24 - i * 28
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(54, by, b_name)
            
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(54, by - 9, b_desc)
            
            # Fundo da barra
            c.setFillColor(C_BAR_BG)
            c.rect(bar_start_x, by - 6, bar_max_w, 14, fill=True, stroke=False)
            
            # Preenchimento
            fill_w = bar_max_w * (b_pct / 99.9)
            c.setFillColor(b_color)
            c.rect(bar_start_x, by - 6, fill_w, 14, fill=True, stroke=False)
            
            # Valor percentual
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(bar_start_x + bar_max_w + 12, by - 4, f"{b_pct}%")
            
        # Linha tracejada da meta de 80%
        meta_x = bar_start_x + bar_max_w * 0.80
        c.setStrokeColor(C_DARK_HERO)
        c.setLineWidth(1.0)
        c.setDash(3, 3)
        c.line(meta_x, y_bars - 12, meta_x, y_bars - h_bars + 14)
        c.setDash() # reset dash
        
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C_DARK_HERO)
        c.drawCentredString(meta_x, y_bars - h_bars + 6, "Meta 80%")

        # --- CALLOUT DIAGNÓSTICO EXECUTIVO (P1) ---
        y_callout = y_bars - h_bars - 12
        h_callout = 60
        self.draw_rounded_card(40, y_callout - h_callout, W - 80, h_callout, fill_color=C_CALLOUT_BG, stroke_color=C_BORDER)
        c.setFillColor(C_ORANGE)
        c.rect(40, y_callout - h_callout, 4, h_callout, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(C_ORANGE)
        c.drawString(56, y_callout - 16, "Diagnóstico executivo")
        
        c.setFont("Helvetica", 8.8)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_callout - 32, "Nota alta (4,6) e dados cadastrais (NAP) validados, mas apenas 178 avaliações contra 1.445 do Mira Maré e 1.362")
        c.drawString(56, y_callout - 45, "do Garra Azul. Acelerar a recência e a captação contínua de reviews é o fator decisivo para furar o Top 3.")
        
        c.showPage()

    def build_page_2(self):
        c = self.c
        self.draw_header_footer(2, "Benchmarking & Estratégia", "Análise competitiva do raio local e plano de aceleração")
        
        # --- SEÇÃO 04: RANKING COMPETITIVO ---
        y_sec4 = H - 100
        self.draw_section_header(y_sec4, "04", "Ranking competitivo", "Google Maps, Ponta das Canas")
        
        y_tbl = y_sec4 - 28
        h_tbl = 278
        self.draw_rounded_card(40, y_tbl - h_tbl, W - 80, h_tbl)
        
        # Header da tabela
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_tbl - 18, "POS.")
        c.drawString(106, y_tbl - 18, "ESTABELECIMENTO")
        c.drawString(330, y_tbl - 18, "NOTA")
        c.drawString(378, y_tbl - 18, "AVALIAÇÕES")
        c.drawString(450, y_tbl - 18, "CARDÁPIO · WHATSAPP")
        
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.5)
        c.line(50, y_tbl - 26, W - 50, y_tbl - 26)
        
        rows = [
            ("1º", "Ratones Craft Beer", "Bar e choperia", "4,8 ★", "2.114", "Sim", "Sim", False),
            ("2º", "Restaurante Mira Maré", "Frutos do mar", "4,5 ★", "1.445", "Sim", "Sim", False),
            ("3º", "Restaurante Garra Azul", "Frutos do mar", "4,3 ★", "1.362", "Sim", "Sim", False),
            ("4º-8º", "Outros 5 estabelecimentos", "Tradição Campeira, Canto da Lagoinha, Lula Floripa, etc.", "4,4-4,7", "493 a 998", "varia", "varia", False),
            ("9º", "Canto do Mar Ponta das Canas", "Alvo auditado (Frutos do mar)", "4,6 ★", "178", "Sim", "Sim", True),
            ("10º-11º", "Vento Suli e Baleia Branca", "Frutos do mar", "4,3-4,5", "72 a 157", "varia", "varia", False)
        ]
        
        for i, (pos, name, cat, nota, revs, cardapio, whats, is_target) in enumerate(rows):
            ry = y_tbl - 44 - i * 40
            
            if is_target:
                c.setFillColor(C_CALLOUT_BG)
                c.rect(41, ry - 14, W - 82, 38, fill=True, stroke=False)
            
            # Pos
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(C_ORANGE if is_target else C_TEXT_DARK)
            c.drawString(56, ry, pos)
            
            # Nome e Categoria
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(106, ry, name)
            
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(106, ry - 10, cat)
            
            # Nota
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(C_ORANGE if is_target else C_TEXT_DARK)
            c.drawString(330, ry, nota)
            
            # Avaliações
            c.setFont("Helvetica-Bold" if is_target else "Helvetica", 9.5)
            c.setFillColor(C_ORANGE if is_target else C_TEXT_DARK)
            c.drawString(378, ry, revs)
            
            # Checks ou 'varia'
            if cardapio == "Sim":
                c.setStrokeColor(C_GREEN)
                c.setLineWidth(1.6)
                c.line(466, ry - 4, 469, ry - 1)
                c.line(469, ry - 1, 473, ry - 7)
                c.line(516, ry - 4, 519, ry - 1)
                c.line(519, ry - 1, 523, ry - 7)
            else:
                c.setFont("Helvetica", 8)
                c.setFillColor(C_TEXT_MUTED)
                c.drawString(464, ry - 4, "varia")
                
            # Divisória da linha
            if i < len(rows) - 1:
                c.setStrokeColor(C_BORDER)
                c.setLineWidth(0.5)
                c.line(50, ry - 14, W - 50, ry - 14)

        # --- A DISTÂNCIA EM AVALIAÇÕES (GRÁFICO HORIZONTAL) ---
        y_dist = y_tbl - h_tbl - 12
        h_dist = 104
        self.draw_rounded_card(40, y_dist - h_dist, W - 80, h_dist)
        
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_dist - 18, "A distância em avaliações")
        
        dist_bars = [
            ("Líder (Ratones)", 2114, C_TEXT_MUTED, "2.114"),
            ("Mira Maré", 1445, C_TEXT_MUTED, "1.445"),
            ("Garra Azul", 1362, C_TEXT_MUTED, "1.362"),
            ("Canto do Mar", 178, C_ORANGE, "178")
        ]
        
        for i, (d_name, d_val, d_col, d_txt) in enumerate(dist_bars):
            dy = y_dist - 38 - i * 16
            c.setFont("Helvetica", 8.5)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(56, dy, d_name)
            
            # Barra
            bw_max = 320
            bw = (d_val / 2114.0) * bw_max
            c.setFillColor(d_col)
            c.rect(150, dy - 2, bw, 10, fill=True, stroke=False)
            
            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(156 + bw, dy, d_txt)

        # --- SEÇÃO 05: PLANO DE AÇÃO ---
        y_sec5 = y_dist - h_dist - 14
        self.draw_section_header(y_sec5, "05", "Plano de ação", "3 pilares para subir no ranking")
        
        y_plan = y_sec5 - 28
        h_plan = 152
        w_plan = (W - 80 - 20) / 3.0
        
        plan_cards = [
            ("01", "IMPACTO IMEDIATO", "Cardápio mobile próprio",
             "Página web mobile com pratos,\nvalores do buffet e fotos\nprofissionais, indexada no Google.",
             "Prazo: 7 a 10 dias", "Meta: zero desistência"),
            ("02", "ACELERAÇÃO DE REVIEWS", "Motor de avaliações 5 estrelas",
             "Displays NFC e QR Code no caixa\ne nas mesas para coletar de 40 a\n65 novas avaliações por mês.",
             "Prazo: imediato", "Meta: +350 avaliações"),
            ("03", "SEO & REPUTAÇÃO", "Resposta ágil a feedbacks",
             "Rotina semanal para responder\n99.9% dos comentários com\npalavras-chave como 'buffet livre' e\n'frutos do mar'.",
             "Prazo: contínuo", "Meta: nota 4,7")
        ]
        
        for i, (p_num, p_tag, p_title, p_desc, p_term, p_meta) in enumerate(plan_cards):
            px = 40 + i * (w_plan + 10)
            self.draw_rounded_card(px, y_plan - h_plan, w_plan, h_plan)
            
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(C_ORANGE)
            c.drawString(px + 14, y_plan - 24, p_num)
            
            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawRightString(px + w_plan - 14, y_plan - 18, p_tag)
            
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(px + 14, y_plan - 44, p_title)
            
            # Descrição multi-linha
            c.setFont("Helvetica", 8.2)
            c.setFillColor(C_TEXT_MUTED)
            lines = p_desc.split("\n")
            for li, line_t in enumerate(lines):
                c.drawString(px + 14, y_plan - 60 - li * 11, line_t)
                
            # Divisória do rodapé do card
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.8)
            c.line(px + 14, y_plan - 116, px + w_plan - 14, y_plan - 116)
            
            c.setFont("Helvetica", 7.8)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(px + 14, y_plan - 130, p_term)
            
            c.setFont("Helvetica-Bold", 8.2)
            c.setFillColor(C_ORANGE)
            c.drawString(px + 14, y_plan - 142, p_meta)
            
        c.showPage()

    def build_page_3(self):
        c = self.c
        self.draw_header_footer(3, "Auditoria Ponto a Ponto", "Resumo executivo, checklist completo e próximos passos")
        
        # --- SEÇÃO 06: RESUMO DE STATUS ---
        y_sec6 = H - 100
        self.draw_section_header(y_sec6, "06", "Resumo de status", "10 itens auditados")
        
        y_stat = y_sec6 - 28
        h_stat = 60
        w_stat = (W - 80 - 20) / 3.0
        
        stat_boxes = [
            ("CONFORME", "5", " /10", "Cadastro e itens básicos\nvalidados", C_GREEN),
            ("ATENÇÃO", "3", " /10", "Oportunidades de\nrefinamento", C_AMBER),
            ("CRÍTICO", "2", " /10", "Ausências que geram\nevasão de clientes", C_RED)
        ]
        
        for i, (s_tag, s_val, s_tot, s_sub, s_col) in enumerate(stat_boxes):
            sx = 40 + i * (w_stat + 10)
            self.draw_rounded_card(sx, y_stat - h_stat, w_stat, h_stat)
            # Faixa lateral colorida
            c.setFillColor(s_col)
            c.rect(sx, y_stat - h_stat, 4, h_stat, fill=True, stroke=False)
            
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(s_col)
            c.drawString(sx + 14, y_stat - 16, s_tag)
            
            c.setFont("Helvetica-Bold", 24)
            c.drawString(sx + 14, y_stat - 44, s_val)
            
            c.setFont("Helvetica", 9.5)
            c.setFillColor(C_TEXT_MUTED)
            vw = c.stringWidth(s_val, "Helvetica-Bold", 24)
            c.drawString(sx + 14 + vw, y_stat - 44, s_tot)
            
            c.setFont("Helvetica", 7.5)
            lines = s_sub.split("\n")
            for li, line_t in enumerate(lines):
                c.drawString(sx + 56, y_stat - 34 - li * 10, line_t)
                
        # Barra empilhada logo abaixo
        c.setFillColor(C_GREEN)
        c.rect(40, y_stat - h_stat - 6, (W - 80) * 0.5, 5, fill=True, stroke=False)
        c.setFillColor(C_AMBER)
        c.rect(40 + (W - 80) * 0.5, y_stat - h_stat - 6, (W - 80) * 0.3, 5, fill=True, stroke=False)
        c.setFillColor(C_RED)
        c.rect(40 + (W - 80) * 0.8, y_stat - h_stat - 6, (W - 80) * 0.2, 5, fill=True, stroke=False)

        # --- SEÇÃO 07: CHECKLIST DETALHADO (COM EXPLICAÇÕES DIDÁTICAS) ---
        y_sec7 = y_stat - h_stat - 20
        self.draw_section_header(y_sec7, "07", "Checklist detalhado", "Item a item")
        
        y_chk = y_sec7 - 28
        h_chk = 318
        self.draw_rounded_card(40, y_chk - h_chk, W - 80, h_chk)
        
        chk_items = [
            ("ok", "01. Nome comercial (Consistência Cadastral · NAP)", "Nome, Endereço e Telefone idênticos ao ponto físico, sem palavras-chave indevidas."),
            ("ok", "02. Endereço e marcador GPS", "Pino geográfico posicionado corretamente no endereço cadastrado."),
            ("ok", "03. Telefone com DDD local", "Linha fixa (48) 3261-0872 com discagem direta funcional."),
            ("ok", "04. Horários de atendimento", "Horários de almoço e semana preenchidos no perfil."),
            ("ok", "05. Fotos e galeria", "Boas fotos mostrando buffet e salão de clientes."),
            ("warn", "06. Volume de avaliações  (FATOR Nº 1)", "178 avaliações, cerca de 92% abaixo do líder regional (2.114)."),
            ("warn", "07. Taxa de resposta a reviews (Gestão de SAC)", "Poucas opiniões respondidas; responder aos feedbacks eleva engajamento e nota."),
            ("warn", "08. Recência das avaliações (Frequência no mês)", "Fluxo intermitente; o algoritmo do Google favorece perfis com novos reviews recentes."),
            ("crit", "09. Website / cardápio digital próprio", "Sem página própria; clientes desistem de visitar por não ver opções e valores."),
            ("crit", "10. Botão de WhatsApp direto", "Sem atalho para reservas de mesas, eventos ou pedidos de viagem.")
        ]
        
        for i, (status, title_t, desc_t) in enumerate(chk_items):
            iy = y_chk - 20 - i * 30
            
            # Badge de status
            bx = 56
            by = iy - 8
            if status == "ok":
                c.setFillColor(C_GREEN)
                c.rect(bx, by, 16, 16, fill=True, stroke=False)
                c.setStrokeColor(colors.white)
                c.setLineWidth(1.6)
                c.line(bx + 4, by + 8, bx + 7, by + 5)
                c.line(bx + 7, by + 5, bx + 12, by + 12)
            elif status == "warn":
                c.setFillColor(C_AMBER)
                c.rect(bx, by, 16, 16, fill=True, stroke=False)
                c.setFont("Helvetica-Bold", 10.5)
                c.setFillColor(colors.white)
                c.drawCentredString(bx + 8, by + 4, "!")
            elif status == "crit":
                c.setFillColor(C_RED)
                c.rect(bx, by, 16, 16, fill=True, stroke=False)
                c.setStrokeColor(colors.white)
                c.setLineWidth(1.6)
                c.line(bx + 4.5, by + 4.5, bx + 11.5, by + 11.5)
                c.line(bx + 11.5, by + 4.5, bx + 4.5, by + 11.5)
                
            # Textos
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(82, iy + 2, title_t)
            
            c.setFont("Helvetica", 8)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(82, iy - 9, desc_t)
            
            if i < len(chk_items) - 1:
                c.setStrokeColor(C_BORDER)
                c.setLineWidth(0.4)
                c.line(50, iy - 14, W - 50, iy - 14)

        # --- COBERTURA METODOLÓGICA ---
        y_cov = y_chk - h_chk - 12
        h_cov = 52
        self.draw_rounded_card(40, y_cov - h_cov, W - 80, h_cov)
        
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C_ORANGE)
        c.drawString(56, y_cov - 16, "COBERTURA DA AUDITORIA:  65% ON-SERP AUDITADO  ·  35% OFF-SERP (FASE 2)")
        
        # Barra horizontal de cobertura (65% laranja / 35% cinza)
        c.setFillColor(C_BAR_BG)
        c.rect(56, y_cov - 26, W - 112, 6, fill=True, stroke=False)
        c.setFillColor(C_ORANGE)
        c.rect(56, y_cov - 26, (W - 112) * 0.65, 6, fill=True, stroke=False)
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_cov - 42, "Fase 2: SEO local no site, backlinks e Search Console. Requer acesso de leitura ao Google Meu Negócio.")

        # --- PRÓXIMO PASSO RECOMENDADO (CTA HERO DARK) ---
        y_cta = y_cov - h_cov - 12
        h_cta = 86
        c.setFillColor(C_DARK_HERO)
        c.rect(40, y_cta - h_cta, W - 80, h_cta, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(60, y_cta - 20, "PRÓXIMO PASSO RECOMENDADO")
        
        c.setFont("Helvetica-Bold", 9.8)
        c.setFillColor(colors.white)
        c.drawString(60, y_cta - 38, "Implantar o cardápio mobile próprio e as placas inteligentes NFC/QR Code no restaurante para")
        c.drawString(60, y_cta - 52, "acelerar a captação de avaliações e escalar posições no ranking local.")
        
        c.setFont("Helvetica", 8.8)
        c.setFillColor(colors.HexColor("#D1D5DB"))
        c.drawString(60, y_cta - 72, "Fale conosco para ativar a implementação:  [seu WhatsApp]  ·  [seu e-mail]")
        
        c.showPage()

    def build(self):
        self.build_page_1()
        self.build_page_2()
        self.build_page_3()
        self.c.save()
        print(f"[✓] PDF V2 Gerado com sucesso: {self.filename}")

if __name__ == "__main__":
    saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
    os.makedirs(saida_dir, exist_ok=True)
    pdf_out = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_v2_Atualizada.pdf")
    builder = ReportBuilder(pdf_out)
    builder.build()

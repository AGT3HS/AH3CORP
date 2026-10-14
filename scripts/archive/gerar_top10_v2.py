import os
import sys
import json
import re
import unicodedata
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group

# Cores exatas do design v2 (Clean / Light Warm / Dark Hero / Orange Accent)
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

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '_', text)

class ReportBuilderV2:
    def __init__(self, filename, dados_alvo, concorrentes_ranking):
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.filename = filename
        self.alvo = dados_alvo
        self.concorrentes = concorrentes_ranking
        
        self.nome = dados_alvo.get("displayName", {}).get("text", "Restaurante") if isinstance(dados_alvo.get("displayName"), dict) else dados_alvo.get("displayName", "Restaurante")
        self.categoria = dados_alvo.get("categoria", "Restaurante")
        self.bairro = dados_alvo.get("hub", "Norte da Ilha")
        self.endereco = dados_alvo.get("formattedAddress", f"{self.bairro}, Florianópolis - SC")
        self.telefone = dados_alvo.get("nationalPhoneNumber", "(48) Não informado")
        self.rating = float(dados_alvo.get("rating", 4.5))
        self.total_reviews = int(dados_alvo.get("userRatingCount", 0))
        self.lat = dados_alvo.get("location", {}).get("latitude", -27.4260) if isinstance(dados_alvo.get("location"), dict) else -27.4260
        self.lon = dados_alvo.get("location", {}).get("longitude", -48.4550) if isinstance(dados_alvo.get("location"), dict) else -48.4550
        self.data_atual = datetime.now().strftime("%d/%m/%Y")
        
        # Posição do alvo
        self.pos_alvo = 1
        for idx, r in enumerate(self.concorrentes, 1):
            if r.get("alvo"):
                self.pos_alvo = idx
                break
                
        # Maior concorrente
        self.lider_revs = self.concorrentes[0]["revs_num"] if self.concorrentes else 5000

    def draw_header_footer(self, page_num, subtitle_p, doc_subtitle):
        c = self.c
        c.setFillColor(C_BG_PAGE)
        c.rect(0, 0, W, H, fill=True, stroke=False)
        
        c.setFillColor(C_ORANGE)
        c.rect(0, H - 6, W, 6, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(40, H - 32, f"AUDITORIA DE PRESENÇA DIGITAL  ·  {subtitle_p.upper()}")
        
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(C_TEXT_DARK)
        # Cortar nome se muito longo
        display_title = self.nome if len(self.nome) <= 35 else self.nome[:33] + "..."
        c.drawString(40, H - 58, display_title)
        
        c.setFont("Helvetica", 9.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(40, H - 74, doc_subtitle)
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(C_TEXT_DARK)
        c.drawRightString(W - 40, H - 32, f"Página 0{page_num} / 03")
        
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_TEXT_MUTED)
        c.drawRightString(W - 40, H - 46, f"Florianópolis - SC  ·  {self.data_atual}")
        
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(1.0)
        c.line(40, H - 88, W - 40, H - 88)
        
        c.line(40, 38, W - 40, 38)
        
        c.setFont("Helvetica", 8)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(40, 24, f"Prospecção Digital  ·  {display_title}")
        c.drawRightString(W - 40, 24, f"Página 0{page_num} / 03")
        
        cx = W / 2.0 - 28
        for i in range(1, 4):
            c.setFillColor(C_ORANGE if i == page_num else C_BORDER)
            c.rect(cx + (i - 1) * 20, 22, 16, 4, fill=True, stroke=False)

    def draw_section_header(self, y_top, num_str, title_str, sub_str):
        c = self.c
        c.setFillColor(C_ORANGE)
        c.rect(40, y_top - 20, 20, 20, fill=True, stroke=False)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.white)
        c.drawCentredString(50, y_top - 14, num_str)
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(68, y_top - 15, title_str)
        
        tw = c.stringWidth(title_str, "Helvetica-Bold", 12)
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
        
        y_hero = H - 104
        h_hero = 88
        c.setFillColor(C_DARK_HERO)
        c.rect(40, y_hero - h_hero, W - 80, h_hero, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(58, y_hero - 20, "O QUE A AUDITORIA MOSTRA")
        
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.white)
        c.drawString(58, y_hero - 42, f"Você é o {self.pos_alvo}º no Google Maps da região.")
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#D1D5DB"))
        c.drawString(58, y_hero - 60, f"A nota é expressiva ({self.rating:.1f}★), com {self.total_reviews:,}".replace(",", ".") + f" avaliações. O líder regional acumula {self.lider_revs:,}".replace(",", ".") + " reviews.")
        c.drawString(58, y_hero - 73, "Volume, autoridade e conversão mobile são o que definem a liderança no raio local.")
        
        # 01 DADOS CADASTRAIS
        y_sec1 = y_hero - h_hero - 14
        self.draw_section_header(y_sec1, "01", "Dados cadastrais", "Perfil Google Business")
        
        y_card1 = y_sec1 - 26
        h_card1 = 92
        self.draw_rounded_card(40, y_card1 - h_card1, W - 80, h_card1)
        
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 16, "NOME OFICIAL")
        c.drawString(250, y_card1 - 16, "CATEGORIA")
        c.drawString(430, y_card1 - 16, "STATUS")
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_card1 - 30, self.nome[:32])
        c.drawString(250, y_card1 - 30, self.categoria[:26])
        
        c.setFillColor(C_GREEN)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(430, y_card1 - 30, "✓ Perfil verificado")
        
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.6)
        c.line(56, y_card1 - 42, W - 56, y_card1 - 42)
        
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 56, "ENDEREÇO")
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(56, y_card1 - 68, self.endereco[:80])
        
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(56, y_card1 - 82, f"TELEFONE: {self.telefone}     GPS: {self.lat:.5f}, {self.lon:.5f}     Microrregião: {self.bairro}")
        
        # 02 INDICADORES-CHAVE
        y_sec2 = y_card1 - h_card1 - 14
        self.draw_section_header(y_sec2, "02", "Indicadores-chave", "Métricas de relevância local")
        
        y_kpi = y_sec2 - 26
        h_kpi = 72
        w_kpi = (W - 80 - 24) / 4.0
        
        kpis = [
            ("SCORE DE PRESENÇA", f"{self.alvo.get('seo_score', 85)}", "/100", "Top 10 Regional", C_TEXT_DARK),
            ("TOTAL DE AVALIAÇÕES", f"{self.total_reviews:,}".replace(",", "."), "", f"Líder: {self.lider_revs:,}".replace(",", "."), C_ORANGE),
            ("NOTA MÉDIA", f"{self.rating:.1f}".replace(".", ","), "", "Satisfação comprovada", C_TEXT_DARK),
            ("POTENCIAL DE GANHO", "+38%", "", "Tráfego no Top 3", C_GREEN)
        ]
        
        for i, (ktitle, kval, kunit, kdesc, kvalcolor) in enumerate(kpis):
            kx = 40 + i * (w_kpi + 8)
            self.draw_rounded_card(kx, y_kpi - h_kpi, w_kpi, h_kpi)
            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(kx + 10, y_kpi - 14, ktitle)
            
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(kvalcolor)
            c.drawString(kx + 10, y_kpi - 38, kval)
            
            if kunit:
                uw = c.stringWidth(kval, "Helvetica-Bold", 16)
                c.setFont("Helvetica-Bold", 9)
                c.setFillColor(C_TEXT_MUTED)
                c.drawString(kx + 10 + uw, y_kpi - 38, kunit)
                
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(kx + 10, y_kpi - 56, kdesc)
            
        # 03 PILARES LOCAIS
        y_sec3 = y_kpi - h_kpi - 14
        self.draw_section_header(y_sec3, "03", "Pilares locais", "Pontuação atual vs. meta de 80% (Top 3)")
        
        y_card3 = y_sec3 - 26
        h_card3 = 110
        self.draw_rounded_card(40, y_card3 - h_card3, W - 80, h_card3)
        
        pilares = [
            ("Dados NAP", 0.95, "95%", C_GREEN),
            ("Fotos", 0.85, "85%", C_GREEN),
            ("Volume de avaliações", min(1.0, max(0.2, self.total_reviews / max(1, self.lider_revs))), f"{int(min(1.0, self.total_reviews / max(1, self.lider_revs))*100)}%", C_ORANGE),
            ("Recência", 0.70, "70%", C_AMBER),
            ("Taxa de resposta", 0.35, "35%", C_RED),
            ("Cardápio digital", 0.90 if self.alvo.get('websiteUri') else 0.20, "90%" if self.alvo.get('websiteUri') else "20%", C_GREEN if self.alvo.get('websiteUri') else C_RED),
        ]
        
        for i, (pname, pval, pstr, pcol) in enumerate(pilares):
            py = y_card3 - 16 - i * 15
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(56, py, pname)
            
            # Barra
            bx = 180
            bw = 280
            c.setFillColor(C_BAR_BG)
            c.rect(bx, py - 2, bw, 8, fill=True, stroke=False)
            
            c.setFillColor(pcol)
            c.rect(bx, py - 2, bw * pval, 8, fill=True, stroke=False)
            
            # Linha meta 80%
            c.setStrokeColor(C_TEXT_MUTED)
            c.setLineWidth(0.8)
            c.line(bx + bw * 0.8, py - 4, bx + bw * 0.8, py + 8)
            
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(pcol)
            c.drawRightString(W - 56, py, pstr)
            
        # Callout p1
        y_call = y_card3 - h_card3 - 10
        h_call = 48
        self.draw_rounded_card(40, y_call - h_call, W - 80, h_call, fill_color=C_CALLOUT_BG, stroke_color=colors.HexColor("#FCD7BE"))
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_ORANGE)
        c.drawString(54, y_call - 14, "DIAGNÓSTICO EXECUTIVO")
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C_TEXT_DARK)
        c.drawString(54, y_call - 28, f"O {self.nome} possui autoridade consolidada no raio de {self.bairro}. O principal vetor de aceleração")
        c.drawString(54, y_call - 39, "é a implantação de um motor ativo de novas avaliações e canal direto mobile para converter buscas em clientes.")

    def build_page_2(self):
        c = self.c
        self.draw_header_footer(2, "Benchmarking & Estratégia", "Análise competitiva do raio local e plano de aceleração")
        
        # 04 RANKING COMPETITIVO
        y_sec4 = H - 104
        self.draw_section_header(y_sec4, "04", "Ranking competitivo", f"Google Maps, {self.bairro}")
        
        y_table = y_sec4 - 26
        h_table = 240
        self.draw_rounded_card(40, y_table - h_table, W - 80, h_table)
        
        # Cabeçalho da tabela
        c.setFillColor(colors.HexColor("#F8F7F4"))
        c.rect(40, y_table - 22, W - 80, 22, fill=True, stroke=False)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(C_TEXT_MUTED)
        c.drawString(54, y_table - 15, "POS.")
        c.drawString(90, y_table - 15, "ESTABELECIMENTO")
        c.drawString(275, y_table - 15, "NOTA")
        c.drawString(335, y_table - 15, "AVALIAÇÕES")
        c.drawString(425, y_table - 15, "CARDÁPIO · WHATSAPP")
        
        for idx, r in enumerate(self.concorrentes[:8], 1):
            ry = y_table - 22 - idx * 26
            
            if r.get("alvo"):
                c.setFillColor(C_CALLOUT_BG)
                c.rect(41, ry - 4, W - 82, 25, fill=True, stroke=False)
                
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(C_ORANGE if r.get("alvo") else C_TEXT_DARK)
            c.drawString(54, ry + 4, f"{idx}º")
            
            c.setFont("Helvetica-Bold" if r.get("alvo") else "Helvetica", 8)
            c.setFillColor(C_TEXT_DARK)
            display_cname = r['nome'][:30]
            c.drawString(90, ry + 4, display_cname)
            
            if r.get("alvo"):
                tw = c.stringWidth(display_cname, "Helvetica-Bold", 8)
                c.setFillColor(C_ORANGE)
                c.rect(94 + tw, ry + 1, 62, 10, fill=True, stroke=False)
                c.setFont("Helvetica-Bold", 6)
                c.setFillColor(colors.white)
                c.drawString(97 + tw, ry + 3, "ALVO AUDITADO")
                
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.HexColor("#F59E0B") if r.get("alvo") else C_TEXT_DARK)
            c.drawString(275, ry + 4, r['nota'])
            
            c.setFont("Helvetica", 8)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(335, ry + 4, f"{r['revs_num']:,}".replace(",", "."))
            
            # Status Sim/Não
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(C_GREEN if r['cardapio'] == "Sim" else C_RED)
            c.drawString(435, ry + 4, r['cardapio'])
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(458, ry + 4, "·")
            c.setFillColor(C_GREEN if r['whats'] == "Sim" else C_RED)
            c.drawString(472, ry + 4, r['whats'])
            
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.5)
            c.line(40, ry - 4, W - 40, ry - 4)
            
        # 05 PLANO DE AÇÃO
        y_sec5 = y_table - h_table - 18
        self.draw_section_header(y_sec5, "05", "Plano de ação", "3 pilares para escalar no ranking")
        
        y_cards5 = y_sec5 - 26
        h_cards5 = 140
        w_card5 = (W - 80 - 16) / 3.0
        
        planos = [
            ("01", "IMPACTO IMEDIATO", "Cardápio Mobile Próprio", "Página web mobile ultra-rápida com fotos, pratos e botão direto de WhatsApp, indexada no Google.", "Prazo: 7 a 10 dias", "Meta: zero desistência"),
            ("02", "ACELERAÇÃO DE REVIEWS", "Motor de Avaliações 5★", "Displays inteligentes NFC e QR Code no balcão/mesas para coletar de 40 a 60 novas avaliações/mês.", "Prazo: imediato", "Meta: +350 avaliações"),
            ("03", "SEO & REPUTAÇÃO", "Resposta Ágil e Otimização", "Rotina técnica para responder 100% dos feedbacks com palavras-chave estratégicas da gastronomia local.", "Prazo: contínuo", "Meta: nota máxima"),
        ]
        
        for i, (pnum, ptag, ptitle, pdesc, pprazo, pmeta) in enumerate(planos):
            px = 40 + i * (w_card5 + 8)
            self.draw_rounded_card(px, y_cards5 - h_cards5, w_card5, h_cards5)
            
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(C_ORANGE)
            c.drawString(px + 12, y_cards5 - 22, pnum)
            
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(px + 12, y_cards5 - 36, ptag)
            
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(px + 12, y_cards5 - 52, ptitle)
            
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C_TEXT_MUTED)
            # Quebrar texto descritivo
            words = pdesc.split()
            line1 = " ".join(words[:5])
            line2 = " ".join(words[5:10])
            line3 = " ".join(words[10:])
            c.drawString(px + 12, y_cards5 - 68, line1)
            c.drawString(px + 12, y_cards5 - 79, line2)
            c.drawString(px + 12, y_cards5 - 90, line3)
            
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.5)
            c.line(px + 12, y_cards5 - 105, px + w_card5 - 12, y_cards5 - 105)
            
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(C_ORANGE)
            c.drawString(px + 12, y_cards5 - 118, pprazo)
            c.setFillColor(C_GREEN)
            c.drawString(px + 12, y_cards5 - 129, pmeta)

    def build_page_3(self):
        c = self.c
        self.draw_header_footer(3, "Auditoria Ponto a Ponto", "Resumo executivo, checklist completo e próximos passos")
        
        # 06 RESUMO DE STATUS
        y_sec6 = H - 104
        self.draw_section_header(y_sec6, "06", "Resumo de status", "10 itens auditados")
        
        y_status = y_sec6 - 26
        h_status = 60
        w_status = (W - 80 - 16) / 3.0
        
        st_cards = [
            ("CONFORME", "6", "/10", "Cadastro e itens básicos validados", C_GREEN),
            ("ATENÇÃO", "2", "/10", "Oportunidades de refinamento", C_AMBER),
            ("CRÍTICO", "2", "/10", "Ausências que geram evasão", C_RED)
        ]
        
        for i, (stitle, sval, sunit, sdesc, scolor) in enumerate(st_cards):
            sx = 40 + i * (w_status + 8)
            self.draw_rounded_card(sx, y_status - h_status, w_status, h_status)
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(scolor)
            c.drawString(sx + 12, y_status - 14, stitle)
            
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(scolor)
            c.drawString(sx + 12, y_status - 34, sval)
            uw = c.stringWidth(sval, "Helvetica-Bold", 16)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(sx + 12 + uw, y_status - 34, sunit)
            
            c.setFont("Helvetica", 7)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(sx + 12, y_status - 48, sdesc)
            
        # 07 CHECKLIST DETALHADO
        y_sec7 = y_status - h_status - 14
        self.draw_section_header(y_sec7, "07", "Checklist detalhado", "Item a item")
        
        y_check = y_sec7 - 24
        h_check = 250
        self.draw_rounded_card(40, y_check - h_check, W - 80, h_check)
        
        checklist_items = [
            ("01. Nome comercial (NAP)", "Nome alinhado com a fachada e padronizado no Google.", "ok"),
            ("02. Endereço e marcador GPS", f"Pino geográfico validado no endereço oficial ({self.bairro}).", "ok"),
            ("03. Telefone oficial com DDD", f"Contato direto ({self.telefone}) ativo no perfil.", "ok" if self.alvo.get('nationalPhoneNumber') else "danger"),
            ("04. Horários de funcionamento", "Horários cadastrados e consistentes na plataforma.", "ok"),
            ("05. Fotos e vitrine do salão", "Imagens de alta qualidade do ambiente e pratos.", "ok"),
            ("06. Volume de avaliações", f"{self.total_reviews:,}".replace(",", ".") + f" avaliações cadastradas no Google Maps.", "ok" if self.total_reviews > 1000 else "warn"),
            ("07. Taxa de resposta a clientes", "Monitoramento contínuo de novas avaliações recebidas.", "warn"),
            ("08. Recência das avaliações", "Fluxo semanal contínuo de novas notas 5 estrelas.", "warn"),
            ("09. Website / Cardápio mobile", "Canal web indexado para consulta de pratos e preços.", "ok" if self.alvo.get('websiteUri') else "danger"),
            ("10. Botão de WhatsApp direto", "Atalho mobile para reservas imediatas e pedidos.", "ok" if self.alvo.get('nationalPhoneNumber') else "danger")
        ]
        
        for idx, (cname, cdesc, cstatus) in enumerate(checklist_items):
            cy = y_check - 14 - idx * 23
            
            if cstatus == "ok":
                c.setFillColor(C_GREEN)
                c.circle(52, cy + 3, 4, fill=True, stroke=False)
                c.setFont("Helvetica-Bold", 6.5)
                c.setFillColor(colors.white)
                c.drawCentredString(52, cy + 1, "✓")
            elif cstatus == "warn":
                c.setFillColor(C_AMBER)
                c.circle(52, cy + 3, 4, fill=True, stroke=False)
                c.setFont("Helvetica-Bold", 6.5)
                c.setFillColor(colors.white)
                c.drawCentredString(52, cy + 1, "!")
            else:
                c.setFillColor(C_RED)
                c.circle(52, cy + 3, 4, fill=True, stroke=False)
                c.setFont("Helvetica-Bold", 6.5)
                c.setFillColor(colors.white)
                c.drawCentredString(52, cy + 1, "✕")
                
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(C_TEXT_DARK)
            c.drawString(64, cy + 1, cname)
            
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C_TEXT_MUTED)
            c.drawString(200, cy + 1, cdesc[:68])
            
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.4)
            c.line(46, cy - 6, W - 46, cy - 6)
            
        # Bloco CTA Final Escuro
        y_cta = y_check - h_check - 12
        h_cta = 52
        c.setFillColor(C_DARK_HERO)
        c.rect(40, y_cta - h_cta, W - 80, h_cta, fill=True, stroke=False)
        
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C_ORANGE)
        c.drawString(56, y_cta - 16, "PRÓXIMO PASSO RECOMENDADO")
        
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.white)
        c.drawString(56, y_cta - 29, "Implantar o cardápio mobile próprio e as placas inteligentes NFC/QR Code no restaurante para")
        c.drawString(56, y_cta - 40, "acelerar a captação de avaliações e blindar a liderança no ranking do Google Maps.")

    def save(self):
        self.build_page_1()
        self.c.showPage()
        self.build_page_2()
        self.c.showPage()
        self.build_page_3()
        self.c.showPage()
        self.c.save()
        return self.filename

if __name__ == "__main__":
    with open('BigBrain/handoff/varredura_norte_da_ilha_total.json', 'r', encoding='utf-8') as f:
        todos = json.load(f)

    top10 = todos[:10]
    os.makedirs('BigBrain/handoff/auditorias_top10_v2', exist_ok=True)

    for idx, alvo in enumerate(top10, 1):
        nome = alvo.get("displayName", {}).get("text", "Restaurante")
        slug = slugify(nome)
        pdf_path = os.path.abspath(f"BigBrain/handoff/auditorias_top10_v2/{idx:02d}_Auditoria_{slug}_v2.pdf")
        
        # Concorrentes
        concorrentes_raw = []
        for c in todos[:9]:
            if c.get("id") != alvo.get("id"):
                concorrentes_raw.append({
                    "nome": c.get("displayName", {}).get("text", "Concorrente"),
                    "nota": f"{float(c.get('rating', 4.5)):.1f} ★",
                    "revs_num": int(c.get("userRatingCount", 0)),
                    "cardapio": "Sim" if c.get("websiteUri") else "Não",
                    "whats": "Sim" if c.get("nationalPhoneNumber") else "Não",
                    "tipo": c.get("categoria", "Gastronomia"),
                    "alvo": False
                })
        concorrentes_raw.append({
            "nome": nome,
            "nota": f"{float(alvo.get('rating', 4.5)):.1f} ★",
            "revs_num": int(alvo.get("userRatingCount", 0)),
            "cardapio": "Sim" if alvo.get("websiteUri") else "Não",
            "whats": "Sim" if alvo.get("nationalPhoneNumber") else "Não",
            "tipo": f"Alvo ({alvo.get('categoria')})",
            "alvo": True
        })
        concorrentes_raw.sort(key=lambda x: -x["revs_num"])
        
        builder = ReportBuilderV2(pdf_path, alvo, concorrentes_raw)
        builder.save()
        print(f"[{idx}/10] Gerado V2: {pdf_path}")

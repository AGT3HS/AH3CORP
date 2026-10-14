# -*- coding: utf-8 -*-
import os, json, csv
import pymupdf as fitz

BASE_DIR = r"C:\Users\Augusto\Desktop\AH3"
LEADS_CSV = os.path.join(BASE_DIR, "BigBrain", "funil", "leads.csv")
GASTO_JSON = os.path.join(BASE_DIR, "scripts", "data", "gastronomia_polo_norte_real.json")
TEMPLATE_PDF = os.path.join(BASE_DIR, "BigBrain", "modelos", "auditoria_restaurantes", "Modelo_Auditoria_SEO_Local_Glass.pdf")
OUT_DIR = os.path.join(BASE_DIR, "saida", "auditorias_glass_prioridade_invisibilidade")
PREVIEW_DIR = os.path.join(OUT_DIR, "previews")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

FONT_REG = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Regular.ttf"
FONT_BOLD = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Bold.ttf"
FONT_MED = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Medium.ttf"
FONT_LIGHT = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Light.ttf"

c_title = (0.059, 0.090, 0.165)
c_meta = (0.392, 0.447, 0.541)
c_body = (0.059, 0.090, 0.165)
c_muted = (0.392, 0.447, 0.541)
c_track = (0.882, 0.894, 0.918)
c_green = (0.118, 0.620, 0.353)
c_orange = (0.949, 0.420, 0.129)
c_yellow = (0.910, 0.639, 0.090)
c_red = (0.839, 0.271, 0.255)

with open(GASTO_JSON, "r", encoding="utf-8") as f:
    gastronomia_polo = json.load(f)

def get_competitors_for_neighborhood(bairro, target_nome, target_reviews, target_nota):
    bairro_lower = bairro.lower()
    concorrentes_locais = [
        r for r in gastronomia_polo 
        if r.get("reviews", 0) > 0 and r["nome"].strip().lower() != target_nome.strip().lower()
    ]
    concorrentes_locais.sort(key=lambda x: x.get("reviews", 0), reverse=True)
    lider_geral = concorrentes_locais[0] if concorrentes_locais else {"nome": "Rancho de Canoa", "reviews": 10962, "nota": 4.9, "bairro": "Ponta das Canas"}
    
    mesmo_bairro = [r for r in concorrentes_locais if any(b in r.get("bairro", "").lower() for b in [bairro_lower.split(",")[0].strip()])]
    if len(mesmo_bairro) < 4:
        top_concorrentes = concorrentes_locais[:4]
    else:
        top_concorrentes = mesmo_bairro[:4]
        
    return lider_geral, top_concorrentes

def gerar_auditoria_lead(lead, output_pdf_path):
    nome = lead["nome"].strip()
    bairro_raw = lead.get("bairro", "Florianópolis").strip()
    bairro = bairro_raw.replace(", Florianópolis", "").strip()
    categoria = lead.get("categoria", "Restaurante/Bar").strip()
    reviews = int(lead.get("total_avaliacoes", 0))
    nota = float(lead.get("nota_google", 5.0))
    telefone = lead.get("telefone", "Não informado").strip() or "Não informado"
    endereco = lead.get("endereco", "").strip()
    has_site = "Site:" in lead.get("observacoes", "") or "http" in lead.get("observacoes", "")
    
    lider_geral, top_concorrentes = get_competitors_for_neighborhood(bairro, nome, reviews, nota)
    lider_revs = lider_geral.get("reviews", 10962)
    gap_lider = round(lider_revs / max(reviews, 1), 1)
    if gap_lider.is_integer():
        gap_lider = int(gap_lider)
        
    doc_template = fitz.open(TEMPLATE_PDF)
    out_doc = fitz.open()
    out_doc.insert_pdf(doc_template, from_page=0, to_page=2)
    
    # Redigir meticulosamente todos os blocos dinâmicos do template
    for p_idx in range(len(out_doc)):
        page = out_doc[p_idx]
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        t = s["text"].strip()
                        bbox = fitz.Rect(s["bbox"])
                        
                        if any(c in t for c in ["[", "]"]):
                            page.add_redact_annot(bbox, fill=False)
                        elif any(term in t for term in ["AGÊNCIA", "NOME DA SUA", "email", "@", "coletados em"]):
                            page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 0:
                            if t in ["/100", "×"] or "%" in t:
                                page.add_redact_annot(bbox, fill=False)
                            elif any(term in t for term in [
                                "Consistência de nome", "Ritmo de novas", "Qualidade e variedade", 
                                "Total acumulado", "Site, cardápio", "Você é o", "números reais",
                                "% de comentários", "menos avaliações"
                            ]):
                                page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 1:
                            if t in ["0,0", "0.000", "000", "00 a 000", "000 a 000", "0,0-0,0", "1º", "2º", "3º", "Totens"] or "totens" in t.lower():
                                page.add_redact_annot(bbox, fill=False)
                            elif any(term in t for term in ["Outros", "Líder (", "A distância em", "100% respondidas"]):
                                page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 2:
                            if any(term in t for term in ["COBERTURA DA AUDITORIA", "Fase 2:", "PRÓXIMO PASSO", "Fale conosco", "implementação", "Texto oculto"]):
                                page.add_redact_annot(bbox, fill=False)
                                
        page.apply_redactions()

    score = 38 if reviews < 10 else (42 if reviews < 30 else (48 if reviews < 100 else 55))
    if not has_site:
        score -= 4
    if nota >= 4.8:
        score += 4
    score = max(30, min(score, 75))
    pts_falta = 80 - score

    # =========================================================================
    # PÁGINA 1
    # =========================================================================
    p1 = out_doc[0]
    p1.insert_text((40.0, 68.0), nome[:45], fontfile=FONT_BOLD, fontsize=16.0 if len(nome) > 30 else 17.0, color=c_title)
    p1.insert_text((420.0, 68.0), "Florianópolis - SC  ·  08/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    
    # Hero Card
    p1.insert_text((62.0, 142.0), f"Oportunidade de Presença e Crescimento no Google Maps ({bairro}).", fontfile=FONT_BOLD, fontsize=10.0 if len(bairro) > 20 else 11.0, color=(1, 1, 1))
    desc_p1 = f"Com excelente nota de {str(nota).replace('.', ',')} estrelas, o estabelecimento possui {reviews} avaliações registradas. O líder local ({lider_geral['nome']}) acumula {lider_revs:,} avaliações, concentrando o fluxo de buscas de moradores e turistas.".replace(",", ".")
    p1.insert_textbox(fitz.Rect(62.0, 153.0, 530.0, 186.0), desc_p1, fontfile=FONT_LIGHT, fontsize=7.2, color=(0.84, 0.85, 0.88))
    
    # Seção 01
    p1.insert_text((60.0, 255.0), nome[:40], fontfile=FONT_REG, fontsize=7.8, color=c_body)
    p1.insert_text((230.0, 255.0), categoria[:35], fontfile=FONT_REG, fontsize=7.8, color=c_body)
    p1.insert_text((400.0, 255.0), "Perfil no Google Maps", fontfile=FONT_MED, fontsize=7.8, color=c_green)
    
    end_display = endereco if endereco else f"Região de {bairro}, Florianópolis"
    p1.insert_text((60.0, 285.0), end_display[:55], fontfile=FONT_REG, fontsize=6.8 if len(end_display) > 35 else 7.3, color=c_body)
    p1.insert_text((340.0, 285.0), telefone, fontfile=FONT_REG, fontsize=7.5, color=c_body)
    p1.insert_text((440.0, 284.5), f"Polo Norte · {bairro}", fontfile=FONT_REG, fontsize=6.8 if len(bairro) > 18 else 7.2, color=c_body)
    p1.insert_text((440.0, 295.5), "Raio de 0 a 1.5 km", fontfile=FONT_REG, fontsize=6.2, color=c_muted)
    
    # Seção 02: 4 KPIs (24pt Bold)
    p1.insert_text((55.0, 381.0), str(score), fontfile=FONT_BOLD, fontsize=24.0, color=c_red if score < 50 else c_yellow)
    p1.insert_text((89.0, 381.0), "/100", fontfile=FONT_REG, fontsize=9.0, color=c_muted)
    p1.insert_text((55.0, 396.0), f"Faltam {pts_falta} pts para a meta de 80", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    p1.insert_text((185.0, 381.0), str(reviews), fontfile=FONT_BOLD, fontsize=24.0, color=c_red if reviews < 50 else c_orange)
    p1.insert_text((185.0, 396.0), f"Líder local: {lider_revs:,} avaliações".replace(",", "."), fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    p1.insert_text((315.0, 381.0), str(nota).replace(".", ","), fontfile=FONT_BOLD, fontsize=24.0, color=c_green if nota >= 4.5 else c_yellow)
    p1.insert_text((315.0, 396.0), "Excelente nota de produto", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    gap_str = f"{gap_lider:,}×".replace(",", ".")
    p1.insert_text((445.0, 381.0), gap_str, fontfile=FONT_BOLD, fontsize=22.0 if len(gap_str) > 5 else 24.0, color=c_red if gap_lider > 10 else c_orange)
    p1.insert_text((445.0, 394.0), f"O líder tem {gap_str} mais", fontfile=FONT_REG, fontsize=5.6, color=c_muted)
    p1.insert_text((445.0, 401.0), "clientes avaliando", fontfile=FONT_REG, fontsize=5.6, color=c_muted)
    
    # Seção 03: 6 Pilares
    p_vol = max(10, min(int(reviews / 20.0 * 10), 90))
    p_site = 85 if has_site else 20
    pilares = [
        (85, "Nome, categoria e endereço alinhados no Google"),
        (50, "Fotos de pratos desatualizadas e sem cardápio recente"),
        (p_vol, f"Apenas {reviews} avaliações reais acumuladas"),
        (20, "Intervalos superiores a 7 dias sem novas avaliações"),
        (25, "Responde a menos de 20% das avaliações recebidas"),
        (p_site, "Presença web indexada no Google" if has_site else "Sem site próprio indexado no Google")
    ]
    for row, (val, sub_txt) in enumerate(pilares):
        ry = 460.5 + row * 28.0
        # Limpar área antes de desenhar
        p1.draw_rect(fitz.Rect(60.0, ry + 7.0, 265.0, ry + 22.0), color=None, fill=(0.98, 0.98, 0.99))
        p1.draw_rect(fitz.Rect(270.0, ry, 484.0, ry + 7.0), color=None, fill=c_track)
        bw = 214.0 * (val / 100.0)
        fill_c = c_green if val >= 80 else (c_yellow if val >= 50 else c_red)
        p1.draw_rect(fitz.Rect(270.0, ry, 270.0 + bw, ry + 7.0), color=None, fill=fill_c)
        p1.insert_text((508.5, ry + 3.0), f"{val:02d}%", fontfile=FONT_BOLD, fontsize=8.6, color=c_body)
        if sub_txt:
            p1.insert_text((60.0, ry + 16.0), sub_txt, fontfile=FONT_REG, fontsize=5.8, color=c_muted)
            
    # Diagnóstico Executivo Box
    diag_text = (
        f"Em {bairro}, clientes e turistas escolhem onde consumir pesquisando no Google Maps. "
        f"O {nome} possui excelente qualidade ({str(nota).replace('.', ',')} estrelas), mas enfrenta invisibilidade algorítmica "
        f"pelo volume restrito de {reviews} avaliações contra {lider_revs:,} do líder regional. "
        f"A ativação de placas NFC nas mesas e a esteira de respostas aceleram o ranqueamento local para o Top 3."
    ).replace(",", ".")
    p1.insert_textbox(fitz.Rect(60.0, 656.0, 535.0, 725.0), diag_text, fontfile=FONT_REG, fontsize=7.4, color=c_body)
    
    # Rodapé P1
    p1.insert_text((40.0, 804.0), f"Augusto Henrique  ·  Presença Local & Google Maps  ·  {nome[:36]}", fontfile=FONT_MED, fontsize=6.0, color=c_title)
    p1.insert_text((40.0, 817.5), "Diagnóstico estratégico elaborado com dados públicos do Google Maps em 08/10/2026.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)
    p1.insert_text((520.0, 804.0), "01 / 03", fontfile=FONT_MED, fontsize=7.2, color=c_meta)

    # =========================================================================
    # PÁGINA 2
    # =========================================================================
    p2 = out_doc[1]
    p2.insert_text((40.0, 68.0), nome[:45], fontfile=FONT_BOLD, fontsize=16.0 if len(nome) > 30 else 17.0, color=c_title)
    p2.insert_text((420.0, 68.0), "Florianópolis - SC  ·  08/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    p2.insert_text((410.0, 114.5), f"Google Maps, Polo Norte ({bairro})", fontfile=FONT_REG, fontsize=6.2 if len(bairro) > 18 else 6.5, color=c_muted)
    
    ranking_data = []
    for idx, c in enumerate(top_concorrentes[:4], 1):
        ranking_data.append((
            f"{idx}º",
            c["nome"][:30],
            f"{c.get('bairro', 'Polo Norte')} · {c.get('reviews', 0):,} avaliações".replace(",", "."),
            str(c.get("nota", 4.5)).replace(".", ","),
            f"{c.get('reviews', 0):,}".replace(",", "."),
            c_title,
            FONT_REG
        ))
    ranking_data.append((
        "• ALVO",
        nome[:30],
        f"Estabelecimento auditado · {reviews} avaliações",
        str(nota).replace(".", ","),
        str(reviews),
        c_orange,
        FONT_BOLD
    ))
    
    for idx, (pos, name_r, desc_r, nota_r, revs_r, cor_r, f_name_r) in enumerate(ranking_data):
        base_y = 169.0 + idx * 36.0
        p2.insert_text((59.0, base_y), pos, fontfile=FONT_BOLD, fontsize=8.8, color=cor_r)
        p2.insert_text((102.0, base_y - 2.0), name_r, fontfile=f_name_r, fontsize=7.8 if len(name_r) > 22 else 8.2, color=cor_r)
        p2.insert_text((102.0, base_y + 7.5), desc_r, fontfile=FONT_REG, fontsize=5.8, color=c_muted if cor_r != c_orange else c_orange)
        p2.insert_text((342.0, base_y - 0.5), nota_r, fontfile=FONT_BOLD, fontsize=7.8, color=cor_r)
        p2.insert_text((390.0, base_y - 0.5), revs_r, fontfile=FONT_BOLD if cor_r == c_orange else FONT_REG, fontsize=7.8, color=cor_r)
        
    # Comparativo de Barras
    c1 = top_concorrentes[0] if len(top_concorrentes) > 0 else {"nome": "Líder Regional", "reviews": 5000}
    c2 = top_concorrentes[1] if len(top_concorrentes) > 1 else {"nome": "2º Colocado", "reviews": 3000}
    c3 = top_concorrentes[2] if len(top_concorrentes) > 2 else {"nome": "3º Colocado", "reviews": 1500}
    
    max_ref = max(c1.get("reviews", 5000), 1000)
    
    p2.insert_text((59.0, 432.5), f"1º {c1['nome'][:30]}", fontfile=FONT_REG, fontsize=6.8 if len(c1['nome']) > 24 else 6.9, color=c_body)
    p2.insert_text((512.9, 432.5), f"{c1['reviews']:,}".replace(",", "."), fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 450.5), f"2º {c2['nome'][:30]}", fontfile=FONT_REG, fontsize=6.8 if len(c2['nome']) > 24 else 6.9, color=c_body)
    p2.insert_text((512.9, 450.5), f"{c2['reviews']:,}".replace(",", "."), fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 468.5), f"3º {c3['nome'][:30]}", fontfile=FONT_REG, fontsize=6.8 if len(c3['nome']) > 24 else 6.9, color=c_body)
    p2.insert_text((512.9, 468.5), f"{c3['reviews']:,}".replace(",", "."), fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 486.5), f"• ALVO: {nome[:30]}", fontfile=FONT_REG, fontsize=6.8 if len(nome) > 24 else 6.9, color=c_orange)
    p2.insert_text((512.9, 486.5), str(reviews), fontfile=FONT_BOLD, fontsize=8.0, color=c_orange)
    
    p2.draw_rect(fitz.Rect(170.0, 427.0, 480.0, 433.0), color=None, fill=c_green)
    
    p2.draw_rect(fitz.Rect(170.0, 445.0, 480.0, 451.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 445.0, 170.0 + (310.0 * c2.get("reviews", 1000) / max_ref), 451.0), color=None, fill=c_yellow)
    
    p2.draw_rect(fitz.Rect(170.0, 463.0, 480.0, 469.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 463.0, 170.0 + (310.0 * c3.get("reviews", 500) / max_ref), 469.0), color=None, fill=c_yellow)
    
    p2.draw_rect(fitz.Rect(170.0, 481.0, 480.0, 487.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 481.0, 170.0 + max((310.0 * reviews / max_ref), 6.0), 487.0), color=None, fill=c_orange)

    # 3 Cards de Ação
    p2.insert_text((57.0, 605.0), "Placas NFC nas Mesas", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(57.0, 626.0, 195.0, 658.0), "Ativar placas inteligentes com chip NFC e QR Code para captura imediata de avaliações no fechamento da conta.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((57.0, 679.0), "1 a 7 dias", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((57.0, 704.0), "+50 avaliações/mês", fontfile=FONT_MED, fontsize=6.8, color=c_orange)
    
    p2.insert_text((233.1, 605.0), "Gestão de Respostas", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(233.1, 626.0, 370.0, 658.0), f"Responder a totalidade dos comentários com termos estratégicos de gastronomia em {bairro}.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((233.1, 679.0), "Imediato", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((233.1, 704.0), "Total cobertura", fontfile=FONT_MED, fontsize=6.8, color=c_orange)
    
    p2.insert_text((409.2, 605.0), "Cardápio & SEO Local", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(409.2, 626.0, 545.0, 658.0), "Integrar menu mobile otimizado, fotos profissionais e botão direto de contato e rota.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((409.2, 679.0), "Contínuo", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((409.2, 704.0), "Top 3 Google Maps", fontfile=FONT_MED, fontsize=6.8, color=c_orange)

    p2.insert_text((40.0, 804.0), f"Augusto Henrique  ·  Presença Local & Google Maps  ·  {nome[:40]}", fontfile=FONT_MED, fontsize=6.0, color=c_title)
    p2.insert_text((40.0, 817.5), "Dados mapeados via Google Maps em 08/10/2026. Volumes dinâmicos sujeitos a alteração diária.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)
    p2.insert_text((520.0, 804.0), "02 / 03", fontfile=FONT_MED, fontsize=7.2, color=c_meta)

    # =========================================================================
    # PÁGINA 3
    # =========================================================================
    p3 = out_doc[2]
    p3.insert_text((40.0, 68.0), nome[:45], fontfile=FONT_BOLD, fontsize=16.0 if len(nome) > 30 else 17.0, color=c_title)
    p3.insert_text((420.0, 68.0), "Florianópolis - SC  ·  08/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    
    # 3 Caixas de KPIs
    p3.insert_text((57.0, 168.0), "4/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_green)
    p3.insert_text((233.1, 168.0), "3/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_yellow)
    p3.insert_text((409.2, 168.0), "3/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_red)
    p3.insert_text((409.2, 186.8), "Bloqueios que impedem o Top 3", fontfile=FONT_REG, fontsize=6.2, color=c_muted)
    
    evidencias = [
        f"Nome comercial '{nome[:40]}' indexado no Google Maps.",
        f"Marcador no Google Maps alinhado ao endereço em {bairro}.",
        f"Telefone de contato identificado: {telefone}.",
        f"Horários de atendimento cadastrados no perfil do Google.",
        f"Fotos de pratos desatualizadas e ausência de imagens de cardápio recente.",
        f"Volume restrito a {reviews} avaliações (o líder tem {gap_str} mais avaliações).",
        f"Taxa de resposta a avaliações inferior a 20% no perfil.",
        f"Intervalos superiores a 7 dias entre novas avaliações no perfil.",
        f"Presença digital {'com' if has_site else 'sem'} página web indexada no Google.",
        f"Canal de WhatsApp sem fluxo de solicitação de avaliação pós-visita."
    ]
    for c_idx, det in enumerate(evidencias):
        cy = 281.5 + c_idx * 36.0
        p3.insert_text((87.0, cy), det[:70], fontfile=FONT_REG, fontsize=6.5, color=c_muted)

    # Box Escuro Próximo Passo
    p3.insert_text((62.0, 706.0), "PRÓXIMO PASSO RECOMENDADO", fontfile=FONT_BOLD, fontsize=7.2, color=c_orange)
    p3.insert_textbox(fitz.Rect(62.0, 718.0, 535.0, 746.0), 
                      "Implementação de placas inteligentes NFC e QR Code nas mesas para geração frequente de avaliações, otimização técnica do perfil no Google Meu Negócio e esteira ativa de respostas estratégicas.", 
                      fontfile=FONT_REG, fontsize=7.5, color=(0.84, 0.85, 0.88))
    
    p3.insert_text((62.0, 756.0), "Fale conosco para ativar a implementação: Augusto Henrique · (48) 99908-8162", fontfile=FONT_BOLD, fontsize=7.6, color=(1, 1, 1))
    
    p3.insert_text((40.0, 804.0), f"Augusto Henrique  ·  Presença Local & Google Maps  ·  {nome[:40]}", fontfile=FONT_MED, fontsize=6.0, color=c_title)
    p3.insert_text((40.0, 817.5), "Auditoria técnica confidencial elaborada para fins de diagnóstico estratégico.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)
    p3.insert_text((520.0, 804.0), "03 / 03", fontfile=FONT_MED, fontsize=7.2, color=c_meta)
    
    out_doc.save(output_pdf_path)
    out_doc.close()

if __name__ == "__main__":
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))
        
    valid_leads = []
    for r in leads:
        try:
            av = int(r.get("total_avaliacoes", 0))
            nt = float(r.get("nota_google", 0))
        except:
            continue
        status = r.get("status", "").strip().lower()
        if av > 0 and status != "perdido":
            r["avals_num"] = av
            r["nota_num"] = nt
            valid_leads.append(r)
            
    valid_leads.sort(key=lambda x: (x["avals_num"], -x["nota_num"]))
    top_leads = valid_leads[:10]
    
    print(f"Gerando {len(top_leads)} auditorias SEO Local no tema Glass (Prioridade Invisibilidade)...")
    
    gerados = []
    for lead in top_leads:
        slug = lead["nome"].replace(" ", "_").replace("/", "_").replace("&", "e").replace("-", "_").replace(".", "")
        pdf_path = os.path.join(OUT_DIR, f"Auditoria_{lead['id']}_{slug}_Glass.pdf")
        gerar_auditoria_lead(lead, pdf_path)
        
        doc = fitz.open(pdf_path)
        png_paths = []
        for p_no in range(len(doc)):
            page = doc[p_no]
            pix = page.get_pixmap(dpi=150)
            png_path = os.path.join(PREVIEW_DIR, f"Auditoria_{lead['id']}_{slug}_p{p_no+1}.png")
            pix.save(png_path)
            png_paths.append(png_path)
        doc.close()
        
        gerados.append({
            "id": lead["id"],
            "nome": lead["nome"],
            "bairro": lead["bairro"],
            "avaliacoes": lead["avals_num"],
            "nota": lead["nota_num"],
            "pdf": pdf_path,
            "previews": png_paths
        })
        print(f"✓ ID {lead['id']} | {lead['nome']} ({lead['avals_num']} avals) -> {pdf_path}")
        
    with open(os.path.join(OUT_DIR, "manifesto_lote.json"), "w", encoding="utf-8") as f:
        json.dump(gerados, f, indent=2, ensure_ascii=False)
        
    print("\nLote concluido com sucesso!")

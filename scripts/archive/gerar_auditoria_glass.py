# -*- coding: utf-8 -*-
"""
Engine Unificada e Canônica de Geração de Auditorias SEO Local / Presença Google Maps - AH3
Suporta oficialmente as 3 Variantes Visuais Homologadas:
  1. glass: Template Matriz V1-4 (Páginas 6-8)
  2. bege: Warm Editorial
  3. preto: Dark Mode Elegance
"""

import os
import sys
import argparse
import pymupdf as fitz

BASE_DIR = r"C:\Users\Augusto\Desktop\AH3"
PDF_GLASS = r"C:\Users\Augusto\AppData\Local\hermes\profiles\maestro\attachments\Guia_Padrao_Auditoria_SEO_Local-V1-4.pdf"
PDF_BEGE = r"C:\Users\Augusto\AppData\Local\hermes\profiles\maestro\attachments\Modelo_Auditoria_SEO_Local_bege.pdf"
PDF_PRETO = r"C:\Users\Augusto\AppData\Local\hermes\profiles\maestro\attachments\Modelo_Auditoria_SEO_Local_Preto.pdf"

FONT_REG = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Regular.ttf"
FONT_BOLD = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Bold.ttf"
FONT_MED = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Medium.ttf"
FONT_LIGHT = r"C:/Users/Augusto/Desktop/AH3/fonts/Poppins-Light.ttf"

def gerar_auditoria(tema="glass", output_pdf_path=None):
    tema = tema.lower()
    if tema == "glass":
        template_path = PDF_GLASS
        default_out = "saida/Auditoria_Chico_Restaurante_Glass.pdf"
        c_title = (0.059, 0.090, 0.165)
        c_meta = (0.392, 0.447, 0.541)
        c_body = (0.059, 0.090, 0.165)
        c_muted = (0.392, 0.447, 0.541)
        c_track = (0.882, 0.894, 0.918)
    elif tema == "bege":
        template_path = PDF_BEGE
        default_out = "saida/Auditoria_Chico_Restaurante_Bege.pdf"
        c_title = (0.12, 0.14, 0.19)
        c_meta = (0.45, 0.48, 0.53)
        c_body = (0.12, 0.14, 0.19)
        c_muted = (0.45, 0.48, 0.53)
        c_track = (0.882, 0.894, 0.918)
    elif tema == "preto":
        template_path = PDF_PRETO
        default_out = "saida/Auditoria_Chico_Restaurante_Preto.pdf"
        c_title = (1.0, 1.0, 1.0)
        c_meta = (0.65, 0.68, 0.73)
        c_body = (0.92, 0.94, 0.96)
        c_muted = (0.60, 0.63, 0.68)
        c_track = (0.22, 0.25, 0.30)
    else:
        raise ValueError(f"Tema inválido '{tema}'. Escolha entre: glass, bege, preto.")

    out_file = output_pdf_path if output_pdf_path else os.path.join(BASE_DIR, default_out)
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)

    c_green = (0.118, 0.620, 0.353)
    c_orange = (0.949, 0.420, 0.129)
    c_yellow = (0.910, 0.639, 0.090)
    c_red = (0.839, 0.271, 0.255)

    doc_template = fitz.open(template_path)
    out_doc = fitz.open()
    
    if tema == "glass":
        out_doc.insert_pdf(doc_template, from_page=5, to_page=7)
    else:
        out_doc.insert_pdf(doc_template, from_page=0, to_page=2)

    for p_idx, page in enumerate(out_doc):
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        t = s["text"].strip()
                        bbox = fitz.Rect(s["bbox"])
                        if any(c in t for c in ["[", "]"]):
                            page.add_redact_annot(bbox, fill=False)
                        elif "AGÊNCIA" in t or "NOME DA SUA" in t or "AH3" in t or "email" in t.lower() or "@" in t:
                            page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 0:
                            if "Qualidade" in t or "Total acumulado" in t or "Site, cardápio" in t or t in ["/100", "×"]:
                                page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 1:
                            if t in ["0,0", "0.000", "000", "00 a 000", "000 a 000", "0,0-0,0", "1º", "2º", "3º", "Totens"] or "totens" in t.lower():
                                page.add_redact_annot(bbox, fill=False)
                        elif p_idx == 2:
                            if "Fale conosco" in t or "implementação" in t or "Texto oculto" in t:
                                page.add_redact_annot(bbox, fill=False)
        page.apply_redactions()

    # PÁGINA 1
    p1 = out_doc[0]
    p1.insert_text((40.0, 68.0), "Chico Restaurante", fontfile=FONT_BOLD, fontsize=18.0, color=c_title)
    p1.insert_text((420.0, 68.0), "Florianópolis - SC  ·  07/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    
    p1.insert_text((62.0, 146.0), "Você é o 9º no Google Maps no raio de 2 km.", fontfile=FONT_BOLD, fontsize=14.0, color=(1, 1, 1))
    p1.insert_textbox(fitz.Rect(62.0, 154.0, 530.0, 182.0), 
                      "Mesmo com boa nota (4,5 estrelas), vizinhos na mesma praia a menos de 80 metros dominam as buscas com até 5x mais avaliações, site e cardápio ativos.", 
                      fontfile=FONT_LIGHT, fontsize=7.8, color=(0.84, 0.85, 0.88) if tema != "preto" else (0.80, 0.82, 0.86))
    
    p1.insert_text((60.0, 255.0), "Bar e Restaurante do Chico", fontfile=FONT_REG, fontsize=8.0, color=c_body)
    p1.insert_text((230.0, 255.0), "Restaurante de Frutos do Mar", fontfile=FONT_REG, fontsize=8.0, color=c_body)
    p1.insert_text((400.0, 255.0), "Perfil verificado", fontfile=FONT_MED, fontsize=8.0, color=c_green)
    
    p1.insert_text((60.0, 285.0), "Estr. Jorn. Jaime de Arruda Ramos, 1294 - Praia da Lagoinha", fontfile=FONT_REG, fontsize=7.6, color=c_body)
    p1.insert_text((340.0, 285.0), "(48) 3284-2502", fontfile=FONT_REG, fontsize=8.0, color=c_body)
    p1.insert_text((440.0, 284.5), "-27.38920, -48.42110", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p1.insert_text((440.0, 295.5), "Raio de 2 km · Lagoinha do Norte", fontfile=FONT_REG, fontsize=6.2, color=c_muted)
    
    p1.insert_text((52.0, 385.0), "44", fontfile=FONT_BOLD, fontsize=22.0, color=c_title if tema=="preto" else (0.36, 0.38, 0.45))
    p1.insert_text((82.0, 385.0), "/100", fontfile=FONT_REG, fontsize=9.0, color=c_muted)
    p1.insert_text((52.0, 399.0), "Faltam 36 pts para a meta de 80", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    p1.insert_text((183.25, 385.0), "183", fontfile=FONT_BOLD, fontsize=22.0, color=c_title if tema=="preto" else (0.36, 0.38, 0.45))
    p1.insert_text((183.25, 399.0), "Líder no polo (1,2 km): 1.445", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    p1.insert_text((314.5, 385.0), "4,5", fontfile=FONT_BOLD, fontsize=22.0, color=c_title if tema=="preto" else (0.36, 0.38, 0.45))
    p1.insert_text((314.5, 399.0), "Boa nota, mas baixo volume", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    p1.insert_text((445.75, 385.0), "7,9", fontfile=FONT_BOLD, fontsize=22.0, color=c_title if tema=="preto" else (0.36, 0.38, 0.45))
    p1.insert_text((485.0, 385.0), "×", fontfile=FONT_BOLD, fontsize=12.0, color=c_muted)
    p1.insert_text((445.75, 399.0), "menos avaliações que o líder", fontfile=FONT_REG, fontsize=5.8, color=c_muted)
    
    pilares = [
        (85, None),
        (58, "Fotos de pratos desatualizadas e sem menu"),
        (35, "Total acumulado muito baixo (183)"),
        (28, None),
        (20, None),
        (25, "Sem site próprio ou cardápio online")
    ]
    for row, (val, sub_txt) in enumerate(pilares):
        ry = 460.5 + row * 28.0
        p1.draw_rect(fitz.Rect(270.0, ry, 484.0, ry + 7.0), color=None, fill=c_track)
        bw = 214.0 * (val / 100.0)
        fill_c = c_green if val >= 80 else (c_yellow if val >= 50 else (0.839, 0.271, 0.255))
        p1.draw_rect(fitz.Rect(270.0, ry, 270.0 + bw, ry + 7.0), color=None, fill=fill_c)
        p1.insert_text((508.5, ry + 3.0), f"{val:02d}%", fontfile=FONT_BOLD, fontsize=8.6, color=c_body)
        if sub_txt:
            sub_y = 472.0 + row * 28.0
            p1.insert_text((60.0, sub_y), sub_txt, fontfile=FONT_REG, fontsize=5.8, color=c_muted)
            
    p1.insert_textbox(fitz.Rect(65.0, 658.0, 535.0, 688.0), 
                      "Na Praia da Lagoinha, o Canto da Lagoinha (a 60m), Lula Floripa (a 80m) e Rancho do Pescador capturam os turistas pelo Google Maps. O Chico perde clientes na própria calçada pela falta de coleta ativa e ausência de cardápio digital.", 
                      fontfile=FONT_REG, fontsize=7.8, color=c_body)
    
    p1.insert_text((40.0, 804.0), "Augusto Henrique  ·  Presença Local & Google Maps  ·  Chico Restaurante", fontfile=FONT_MED, fontsize=6.8, color=c_title)
    p1.insert_text((40.0, 817.5), "Dados coletados em 07/10/2026, busca anônima no raio de 2 km a partir da Praia da Lagoinha. Valores do Google Maps variam diariamente.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)

    # PÁGINA 2
    p2 = out_doc[1]
    p2.insert_text((40.0, 68.0), "Chico Restaurante", fontfile=FONT_BOLD, fontsize=18.0, color=c_title)
    p2.insert_text((420.0, 68.0), "Florianópolis - SC  ·  07/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    p2.insert_text((410.0, 114.5), "Google Maps, Raio de 2 km (Lagoinha)", fontfile=FONT_REG, fontsize=6.5, color=c_muted)
    
    ranking_data = [
        ("1º", "Restaurante Mira Maré", "Frutos do Mar (a 1,2 km · Ponta das Canas)", "4,5", "1.445", c_title, FONT_REG),
        ("2º", "Restaurante Garra Azul", "Frutos do Mar (a 1,3 km · Ponta das Canas)", "4,3", "1.362", c_title, FONT_REG),
        ("3º", "Canto da Lagoinha", "Frutos do Mar Pé na Areia (a 60m do Chico)", "4,6", "984", c_title, FONT_BOLD),
        ("4º-8º", "Lula Floripa, Rancho do Pescador, 1983...", "Vizinhos da Lagoinha e Ponta das Canas (a 80m a 500m)", "4,6-4,7", "263 a 763", c_title, FONT_REG),
        ("9º", "Bar e Restaurante do Chico", "Alvo auditado · 9º no raio de 2 km", "4,5", "183", c_orange, FONT_BOLD),
        ("10º", "Canto do Mar Ponta das Canas", "Frutos do Mar (a 1,6 km)", "4,6", "178", c_title, FONT_REG)
    ]
    for idx, (pos, name, desc, nota, revs, cor, f_name) in enumerate(ranking_data):
        base_y = 169.0 + idx * 36.0
        p2.insert_text((59.0, base_y), pos, fontfile=FONT_BOLD, fontsize=8.8, color=cor)
        p2.insert_text((102.0, base_y - 2.0), name, fontfile=f_name, fontsize=8.2, color=cor)
        p2.insert_text((102.0, base_y + 7.5), desc, fontfile=FONT_REG, fontsize=5.8, color=c_muted if cor != c_orange else c_orange)
        p2.insert_text((342.0, base_y - 0.5), nota, fontfile=FONT_BOLD, fontsize=7.8, color=cor)
        p2.insert_text((390.0, base_y - 0.5), revs, fontfile=FONT_BOLD if cor == c_orange else FONT_REG, fontsize=7.8, color=cor)
        
    p2.insert_text((59.0, 432.5), "Líder do polo (Mira Maré - 1,2 km)", fontfile=FONT_REG, fontsize=6.9, color=c_body)
    p2.insert_text((512.9, 432.5), "1.445", fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 450.5), "Vizinho 1 (Canto da Lagoinha - 60m)", fontfile=FONT_REG, fontsize=6.9, color=c_body)
    p2.insert_text((512.9, 450.5), "984", fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 468.5), "Vizinho 2 (Lula Floripa - 80m)", fontfile=FONT_REG, fontsize=6.9, color=c_body)
    p2.insert_text((512.9, 468.5), "626", fontfile=FONT_BOLD, fontsize=8.0, color=c_title)
    
    p2.insert_text((59.0, 486.5), "Chico Restaurante (Auditado)", fontfile=FONT_REG, fontsize=6.9, color=c_orange)
    p2.insert_text((512.9, 486.5), "183", fontfile=FONT_BOLD, fontsize=8.0, color=c_orange)
    
    p2.draw_rect(fitz.Rect(170.0, 427.0, 480.0, 433.0), color=None, fill=c_green)
    p2.draw_rect(fitz.Rect(170.0, 445.0, 480.0, 451.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 445.0, 170.0 + (310.0 * 984 / 1445), 451.0), color=None, fill=c_yellow)
    p2.draw_rect(fitz.Rect(170.0, 463.0, 480.0, 469.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 463.0, 170.0 + (310.0 * 626 / 1445), 469.0), color=None, fill=c_yellow)
    p2.draw_rect(fitz.Rect(170.0, 481.0, 480.0, 487.0), color=None, fill=c_track)
    p2.draw_rect(fitz.Rect(170.0, 481.0, 170.0 + (310.0 * 183 / 1445), 487.0), color=None, fill=c_orange)

    # 3 Cards de Ação (100% livres de totens)
    p2.insert_text((57.0, 605.0), "Placas NFC nas Mesas", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(57.0, 626.0, 195.0, 658.0), "Ativar placas inteligentes com chip NFC e QR Code para coleta instantânea no fechamento de conta.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((57.0, 679.0), "1 a 7 dias", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((57.0, 704.0), "+60 avaliações/mês", fontfile=FONT_MED, fontsize=6.8, color=c_orange)
    
    p2.insert_text((233.1, 605.0), "Gestão de Respostas", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(233.1, 626.0, 370.0, 658.0), "Responder 100% dos comentários com palavras-chave estratégicas de frutos do mar e praia.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((233.1, 679.0), "Imediato", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((233.1, 704.0), "100% respondidas", fontfile=FONT_MED, fontsize=6.8, color=c_orange)
    
    p2.insert_text((409.2, 605.0), "Cardápio & SEO Local", fontfile=FONT_BOLD, fontsize=9.2, color=c_title)
    p2.insert_textbox(fitz.Rect(409.2, 626.0, 545.0, 658.0), "Integrar menu mobile otimizado, fotos oficiais da praia e botão de contato direto.", fontfile=FONT_REG, fontsize=6.8, color=c_muted)
    p2.insert_text((409.2, 679.0), "Contínuo", fontfile=FONT_REG, fontsize=7.4, color=c_body)
    p2.insert_text((409.2, 704.0), "Top 3 Google Maps", fontfile=FONT_MED, fontsize=6.8, color=c_orange)

    # Rodapé P2
    p2.insert_text((40.0, 804.0), "Augusto Henrique  ·  Presença Local & Google Maps  ·  Chico Restaurante", fontfile=FONT_MED, fontsize=6.8, color=c_title)
    p2.insert_text((40.0, 817.5), "Dados coletados em 07/10/2026, busca anônima no raio de 2 km a partir da Praia da Lagoinha. Valores do Google Maps variam diariamente.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)

    # PÁGINA 3
    p3 = out_doc[2]
    p3.insert_text((40.0, 68.0), "Chico Restaurante", fontfile=FONT_BOLD, fontsize=18.0, color=c_title)
    p3.insert_text((420.0, 68.0), "Florianópolis - SC  ·  07/10/2026", fontfile=FONT_REG, fontsize=7.2, color=c_meta)
    
    # Seção 06: Resumo de Status (3 Caixas de KPIs)
    p3.insert_text((57.0, 168.0), "4/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_green)
    p3.insert_text((233.1, 168.0), "3/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_yellow)
    p3.insert_text((409.2, 168.0), "3/10", fontfile=FONT_BOLD, fontsize=20.0, color=c_red)
    p3.insert_text((409.2, 186.8), "Bloqueios que impedem o Top 3", fontfile=FONT_REG, fontsize=6.2, color=c_muted)
    
    evidencias_chico = [
        "Nome comercial padronizado e sem violações de diretrizes do Google.",
        "Marcador no Google Maps alinhado à entrada na Praia da Lagoinha.",
        "Telefone com DDD local (48) verificado e funcionando.",
        "Horários de atendimento e temporada cadastrados no perfil.",
        "Fotos de pratos desatualizadas e ausência de imagens de cardápio.",
        "Apenas 183 avaliações, quase 8x menos que o líder do polo (1.445).",
        "Taxa de resposta a avaliações inferior a 20% no perfil.",
        "Intervalos superiores a 7 dias entre novas avaliações no perfil.",
        "Sem site próprio ou cardápio online indexável no Google Maps.",
        "Canal de WhatsApp sem mensagem automática de recepção."
    ]
    for c_idx, det in enumerate(evidencias_chico):
        cy = 281.5 + c_idx * 36.0
        p3.insert_text((87.0, cy), det, fontfile=FONT_REG, fontsize=6.5, color=c_muted)

    # Bloco Dark Próximo Passo
    p3.insert_text((66.0, 722.0), "Atualização total do Google Meu Negócio com rotina de posts semanais e placas NFC", fontfile=FONT_MED, fontsize=8.4, color=(1, 1, 1))
    p3.insert_text((66.0, 734.5), "para acelerar a captação de clientes na Praia da Lagoinha e colocar seu restaurante no Top 3.", fontfile=FONT_REG, fontsize=8.0, color=(0.88, 0.90, 0.94))
    
    # Chamada Comercial e Contato (Sem e-mails)
    p3.insert_text((66.0, 762.0), "Fale conosco e entenda como fazer seu restaurante lucrar mais:", fontfile=FONT_REG, fontsize=7.2, color=(0.97, 0.64, 0.46))
    p3.insert_text((330.0, 762.0), "Augusto Henrique · (48) 99908-8162", fontfile=FONT_BOLD, fontsize=7.4, color=(1, 1, 1))
    
    # Rodapé P3
    p3.insert_text((40.0, 804.0), "Augusto Henrique  ·  Presença Local & Google Maps  ·  Chico Restaurante", fontfile=FONT_MED, fontsize=6.8, color=c_title)
    p3.insert_text((40.0, 817.5), "Dados coletados em 07/10/2026, busca anônima no raio de 2 km a partir da Praia da Lagoinha. Valores do Google Maps variam diariamente.", fontfile=FONT_REG, fontsize=5.6, color=c_muted)

    out_doc.save(out_file)
    doc_template.close()
    out_doc.close()
    print(f"Auditoria SEO Local [{tema.upper()}] gerada com sucesso em: {out_file}")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador Unificado de Auditorias SEO Local AH3")
    parser.add_argument("--tema", choices=["glass", "bege", "preto", "all"], default="all", help="Tema da auditoria")
    parser.add_argument("--saida", help="Caminho do arquivo de saída")
    args = parser.parse_args()
    
    if args.tema == "all":
        for t in ["glass", "bege", "preto"]:
            gerar_auditoria(t)
    else:
        gerar_auditoria(args.tema, args.saida)

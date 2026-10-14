import pymupdf as fitz
import io
import os
from PIL import Image

def generate_exact_jurere_proposal():
    # 1. Renderizar o arquivo oficial do modelo 01_modelo_classico_cor_mae.svg com resolução ultra nítida (300 DPI = 4167x4167 px)
    svg_path = 'BigBrain/handoff/placas_hoteis_layout02/02_02_jurer_beach_village/01_modelo_classico_cor_mae.svg'
    doc_svg = fitz.open(svg_path)
    pix_svg = doc_svg[0].get_pixmap(dpi=300, alpha=True)
    
    os.makedirs('saida/proposta_jurere', exist_ok=True)
    placa_png_path = 'saida/proposta_jurere/placa_01_modelo_classico_cor_mae_jurere_oficial.png'
    pix_svg.save(placa_png_path)
    print(f"Placa oficial salva em {placa_png_path} ({pix_svg.width}x{pix_svg.height} px)")

    # 2. Abrir o PDF original de referência
    pdf_in = 'C:/Users/Augusto/AppData/Local/hermes/profiles/designer/attachments/Proposta.pdf'
    doc = fitz.open(pdf_in)

    # === PÁGINA 1 (Capa) ===
    p1 = doc[0]
    # Substituir "Preparada para: Costão do Santinho Resort"
    for b in p1.get_text('blocks'):
        if 'Preparada para:' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=(0.0902, 0.2157, 0.3686))
            p1.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Preparada para: Jurerê Beach Village", fontname="helv", fontsize=11.5, color=(1, 1, 1))

    # Na Capa, substituir o cartão pela placa oficial 01_modelo_classico_cor_mae (#4DA2AD)
    # Área exata do cartão na P1: (551.25, 150.0, 911.25, 510.0) -> 360x360 pt
    card_p1_rect = fitz.Rect(551.25, 150.0, 911.25, 510.0)
    # Cobrir o cartão antigo
    p1.draw_rect(fitz.Rect(545, 140, 920, 520), color=None, fill=(0.0902, 0.2157, 0.3686))
    # Inserir a placa oficial do Jurerê com cantos curvos e cor #4DA2AD
    p1.insert_image(card_p1_rect, filename=placa_png_path)

    # Atualizar C O S TA O . C O M . B R na P1
    for b in p1.get_text('blocks'):
        if 'C O S TA O' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 40, r_box.y0 - 3, r_box.x1 + 40, r_box.y1 + 3), color=None, fill=(0.0902, 0.2157, 0.3686))
            p1.insert_text(fitz.Point(625.0, r_box.y1 - 2), "J U R E R E B E A C H V I L L A G E . C O M . B R", fontname="helv", fontsize=8.5, color=(0.65, 0.95, 0.99))

    # === PÁGINA 2 ===
    p2 = doc[1]
    for b in p2.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p2.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p2.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p2.insert_text(fitz.Point(920, r_box.y1 - 2), "2", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 3 ===
    p3 = doc[2]
    for b in p3.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p3.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p3.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p3.insert_text(fitz.Point(920, r_box.y1 - 2), "3", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 4 (Apresentação Técnica da Placa 10x10) ===
    p4 = doc[3]
    # Área exata do cartão na P4: (65.25, 120.0, 519.75, 574.5) -> 454.5x454.5 pt
    card_p4_rect = fitz.Rect(65.25, 120.0, 519.75, 574.5)
    p4.draw_rect(fitz.Rect(55, 110, 530, 585), color=None, fill=(0.9451, 0.9882, 0.9922))
    p4.insert_image(card_p4_rect, filename=placa_png_path)

    # Atualizar textos da lateral direita da Página 4
    for b in p4.get_text('blocks'):
        if 'C A R T Ã O · C O S T Ã O' in b[4] or 'CARTÃO · COSTÃO' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "C A R T Ã O · J U R E R Ê B E A C H V I L L A G E", fontname="helv", fontsize=9.0, color=(0.302, 0.635, 0.678))
        if 'Costão SPA & Relax' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Piscinas & Hidro", fontname="helv", fontsize=11.0, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p4.insert_text(fitz.Point(920, r_box.y1 - 2), "4", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 5 (Página do Hóspede) ===
    p5 = doc[4]
    for b in p5.get_text('blocks'):
        if 'Costão do' in b[4] or 'Santinho' in b[4]:
            r_box = fitz.Rect(b[:4])
            p5.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 20, r_box.y1 + 2), color=None, fill=(0.0706, 0.0941, 0.1020))
            p5.insert_text(fitz.Point(r_box.x0, r_box.y0 + 16), "Jurerê Beach", fontname="helv", fontsize=15, color=(1, 1, 1))
            p5.insert_text(fitz.Point(r_box.x0, r_box.y0 + 34), "Village", fontname="helv", fontsize=15, color=(1, 1, 1))
        if 'C O S T Ã O S PA & R E L A X' in b[4]:
            r_box = fitz.Rect(b[:4])
            p5.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=(1, 1, 1))
            p5.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "P I S C I N A S & H I D R O", fontname="helv", fontsize=8, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p5.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p5.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p5.insert_text(fitz.Point(920, r_box.y1 - 2), "5", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 6 (Avaliações Google) ===
    p6 = doc[5]
    for b in p6.get_text('blocks'):
        if 'Avalie o Costão no Google' in b[4]:
            r_box = fitz.Rect(b[:4])
            p6.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 20, r_box.y1 + 3), color=None, fill=(1, 1, 1))
            p6.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Avalie o Jurerê Beach Village no Google. Leva menos de 1 minuto", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p6.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p6.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p6.insert_text(fitz.Point(920, r_box.y1 - 2), "6", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 7 ===
    p7 = doc[6]
    for b in p7.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p7.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.0902, 0.2157, 0.3686))
            p7.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))
            p7.insert_text(fitz.Point(920, r_box.y1 - 2), "7", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))

    # === PÁGINA 8 (Condições Comerciais & Fechamento) ===
    p8 = doc[7]
    for b in p8.get_text('blocks'):
        if 'Proposta de implantação Costão do Santinho' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 40, r_box.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Proposta de implantação Jurerê Beach Village", fontname="helv", fontsize=13, color=(0.07, 0.09, 0.10))
        if 'Cartões NFC Costão' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 20, r_box.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=11, color=(0.07, 0.09, 0.10))
        if '109 unidades.' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y0 + 10), "100 unidades. Cartões já configurados e funcionais. Suporte", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y0 + 22), "técnico de 2 anos na tecnologia de todas as placas.", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p8.insert_text(fitz.Point(920, r_box.y1 - 2), "8", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    out_pdf = 'saida/proposta_jurere/Proposta_Comercial_Jurere_Beach_Village_Placa_01_Oficial.pdf'
    doc.save(out_pdf)
    print(f"Sucesso! PDF final com a placa oficial #4DA2AD gerado em: {out_pdf}")

    # Exportar imagens em alta resolução dos slides
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_out = f'saida/proposta_jurere/slide_oficial_placa01_{i+1:02d}.png'
        pix.save(img_out)

if __name__ == '__main__':
    generate_exact_jurere_proposal()

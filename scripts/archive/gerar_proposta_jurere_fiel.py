import pymupdf as fitz
import io
import os
from PIL import Image

def rebuild_pdf_exact_layout():
    pdf_in = 'C:/Users/Augusto/AppData/Local/hermes/profiles/designer/attachments/Proposta.pdf'
    doc = fitz.open(pdf_in)

    # 1. Substituir a imagem da logo (xref 16) com a logo oficial Jurerê Beach Village em alta definição
    logo_path = 'guias_identidade_visual/logos/02_jurer_beach_village/02_jurer_beach_village_logo_1.png'
    img = Image.open(logo_path).convert('RGBA')
    r, g, b, a = img.split()
    white_img = Image.merge('RGBA', (Image.new('L', img.size, 255), Image.new('L', img.size, 255), Image.new('L', img.size, 255), a))

    target_logo = Image.new('RGBA', (2048, 619), (0, 0, 0, 0))
    w, h = white_img.size
    ratio = min(1750 / w, 480 / h)
    new_size = (int(w * ratio), int(h * ratio))
    resized_logo = white_img.resize(new_size, Image.Resampling.LANCZOS)
    offset_x = (2048 - new_size[0]) // 2
    offset_y = (619 - new_size[1]) // 2
    target_logo.paste(resized_logo, (offset_x, offset_y), resized_logo)

    bio = io.BytesIO()
    target_logo.save(bio, format='PNG')
    doc[0].replace_image(16, stream=bio.getvalue())

    # === PÁGINA 1 ===
    p1 = doc[0]
    # Substituir "Preparada para: Costão do Santinho Resort"
    for b in p1.get_text('blocks'):
        if 'Preparada para:' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=(0.0902, 0.2157, 0.3686))
            p1.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Preparada para: Jurerê Beach Village", fontname="helv", fontsize=11.5, color=(1, 1, 1))

    # Na P1 dentro da plaquinha:
    for b in p1.get_text('blocks'):
        if 'Costão SPA & Relax' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=(0.9569, 0.9373, 0.9176))
            p1.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "SPA & Relax", fontname="helv", fontsize=7.9, color=(0.07, 0.09, 0.10))
        if 'costao.com.br' in b[4] and b[0] > 550:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(580, r_box.y0 - 2, 885, r_box.y1 + 2), color=None, fill=(0.9569, 0.9373, 0.9176))
            p1.insert_text(fitz.Point(580.05, r_box.y1 - 1.5), "Florianópolis • Santa Catarina", fontname="helv", fontsize=5.8, color=(0.42, 0.40, 0.36))
            p1.insert_text(fitz.Point(795.0, r_box.y1 - 1.5), "jurerebeachvillage.com.br", fontname="helv", fontsize=5.8, color=(0.07, 0.09, 0.10))
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

    # === PÁGINA 4 ===
    p4 = doc[3]
    for b in p4.get_text('blocks'):
        if 'Costão SPA & Relax' in b[4]:
            r_box = fitz.Rect(b[:4])
            if b[0] < 500: # dentro da plaquinha
                p4.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=(0.9569, 0.9373, 0.9176))
                p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "SPA & Relax", fontname="helv", fontsize=10.0, color=(0.07, 0.09, 0.10))
            else: # texto na coluna lateral
                p4.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=(0.9451, 0.9882, 0.9922))
                p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "SPA & Relax", fontname="helv", fontsize=11.0, color=(0.07, 0.09, 0.10))
        if 'costao.com.br' in b[4] and b[0] < 500:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(101.61, r_box.y0 - 2, 485.0, r_box.y1 + 2), color=None, fill=(0.9569, 0.9373, 0.9176))
            p4.insert_text(fitz.Point(101.61, r_box.y1 - 2), "Florianópolis • Santa Catarina", fontname="helv", fontsize=7.3, color=(0.42, 0.40, 0.36))
            p4.insert_text(fitz.Point(380.0, r_box.y1 - 2), "jurerebeachvillage.com.br", fontname="helv", fontsize=7.3, color=(0.07, 0.09, 0.10))
        if 'C A R T Ã O · C O S T Ã O' in b[4] or 'CARTÃO · COSTÃO' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "C A R T Ã O · J U R E R Ê B E A C H V I L L A G E", fontname="helv", fontsize=9.0, color=(0.302, 0.635, 0.678))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p4.insert_text(fitz.Point(920, r_box.y1 - 2), "4", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 5 ===
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
            p5.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "S PA & R E L A X", fontname="helv", fontsize=8, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p5.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p5.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p5.insert_text(fitz.Point(920, r_box.y1 - 2), "5", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 6 ===
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

    # === PÁGINA 8 ===
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

    out_pdf = 'saida/proposta_jurere/Proposta_Comercial_Jurere_Beach_Village_Layout_Original.pdf'
    doc.save(out_pdf)
    print(f"Sucesso absoluto: {out_pdf}")

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        pix.save(f'saida/proposta_jurere/slide_fiel_{i+1:02d}.png')

if __name__ == '__main__':
    rebuild_pdf_exact_layout()

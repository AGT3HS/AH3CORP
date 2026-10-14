import pymupdf # PyMuPDF
import os
import io

def build_jurere_proposta():
    # 1. Renderizar a placa canônica oficial do Jurerê Beach Village em PNG 300DPI
    svg_path = 'BigBrain/handoff/placas_hoteis_layout02/02_02_jurer_beach_village/01_modelo_classico_cor_mae.svg'
    doc_svg = pymupdf.open(svg_path)
    pix_svg = doc_svg[0].get_pixmap(dpi=300, alpha=True)
    os.makedirs('saida/proposta_jurere', exist_ok=True)
    placa_png_path = 'saida/proposta_jurere/placa_01_modelo_classico_cor_mae_jurere.png'
    pix_svg.save(placa_png_path)
    print(f"Placa oficial renderizada em {placa_png_path} ({pix_svg.width}x{pix_svg.height})")

    # 2. Abrir o documento PDF original (Proposta.pdf)
    pdf_in_path = 'C:/Users/Augusto/AppData/Local/hermes/profiles/designer/attachments/Proposta.pdf'
    doc = pymupdf.open(pdf_in_path)

    # Cores Jurerê Beach Village
    # Navy do hotel / texto / fundo escuro:
    # Topo Turquesa: #4DA2AD -> (0.302, 0.635, 0.678)
    # Turquesa Escuro: #276B75 -> (0.153, 0.420, 0.459)
    # Destaque Âmbar: #E8A825 -> (0.910, 0.659, 0.145)
    # Dark Navy: #0A1E36 -> (0.039, 0.118, 0.212)
    # Areia Nobre: #FAF8F5 -> (0.980, 0.973, 0.961)

    # Processar cada página adaptando textos, rodapés e inserindo a placa oficial 01_modelo_classico_cor_mae

    # === PÁGINA 1 (Capa) ===
    p1 = doc[0]
    # Substituir "Preparada para: Costão do Santinho Resort"
    for b in p1.get_text('blocks'):
        if 'Preparada para:' in b[4]:
            r = pymupdf.Rect(b[:4])
            # Cobrir com a cor de fundo do slide da capa
            p1.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 4, r.x1 + 60, r.y1 + 4), color=None, fill=(0.0902, 0.2157, 0.3686))
            p1.insert_text(pymupdf.Point(r.x0, r.y1 - 3), "Preparada para: Jurerê Beach Village", fontname="helv", fontsize=11.5, color=(1, 1, 1))

    # Cobrir e substituir o cartão inteiro da capa com a placa oficial com cantos arredondados
    # Retângulo exato do cartão na P1: (551.25, 150.0, 911.25, 510.0)
    card_p1_rect = pymupdf.Rect(551.25, 150.0, 911.25, 510.0)
    # Cobrir a área do cartão antigo para não vazar texto antigo
    p1.draw_rect(pymupdf.Rect(545, 140, 920, 520), color=None, fill=(0.0902, 0.2157, 0.3686))
    # Inserir a imagem da placa oficial 01_modelo_classico_cor_mae
    p1.insert_image(card_p1_rect, filename=placa_png_path)

    # === PÁGINA 2 ===
    p2 = doc[1]
    # Atualizar rodapé
    for b in p2.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p2.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p2.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p2.insert_text(pymupdf.Point(920, r.y1 - 2), "2", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 3 ===
    p3 = doc[2]
    # Atualizar rodapé
    for b in p3.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p3.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p3.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p3.insert_text(pymupdf.Point(920, r.y1 - 2), "3", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 4 (Apresentação do Cartão 10x10) ===
    p4 = doc[3]
    # Cobrir o cartão antigo e inserir a placa oficial
    # Retângulo exato do cartão na P4: (65.25, 120.0, 519.75, 574.5)
    card_p4_rect = pymupdf.Rect(65.25, 120.0, 519.75, 574.5)
    p4.draw_rect(pymupdf.Rect(55, 110, 530, 585), color=None, fill=(0.9451, 0.9882, 0.9922))
    p4.insert_image(card_p4_rect, filename=placa_png_path)

    # Atualizar textos da lateral direita
    for b in p4.get_text('blocks'):
        if 'C A R T Ã O · C O S T Ã O' in b[4] or 'CARTÃO · COSTÃO' in b[4]:
            r = pymupdf.Rect(b[:4])
            p4.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 4, r.x1 + 50, r.y1 + 4), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(pymupdf.Point(r.x0, r.y1 - 3), "C A R T Ã O · J U R E R Ê B E A C H V I L L A G E", fontname="helv", fontsize=9, color=(0.302, 0.635, 0.678))
        if 'Costão SPA & Relax' in b[4]:
            r = pymupdf.Rect(b[:4])
            p4.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 20, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "SPA & Bem-Estar", fontname="helv", fontsize=11, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p4.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p4.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p4.insert_text(pymupdf.Point(920, r.y1 - 2), "4", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 5 (Interface Mobile) ===
    p5 = doc[4]
    for b in p5.get_text('blocks'):
        if 'Costão do' in b[4] or 'Santinho' in b[4]:
            r = pymupdf.Rect(b[:4])
            p5.draw_rect(pymupdf.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 20, r.y1 + 2), color=None, fill=(0.0706, 0.0941, 0.1020))
            p5.insert_text(pymupdf.Point(r.x0, r.y0 + 16), "Jurerê Beach", fontname="helv", fontsize=15, color=(1, 1, 1))
            p5.insert_text(pymupdf.Point(r.x0, r.y0 + 34), "Village", fontname="helv", fontsize=15, color=(1, 1, 1))
        if 'C O S T Ã O S PA & R E L A X' in b[4]:
            r = pymupdf.Rect(b[:4])
            p5.draw_rect(pymupdf.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 10, r.y1 + 2), color=None, fill=(1, 1, 1))
            p5.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "S PA & B E M - E S TA R", fontname="helv", fontsize=8, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p5.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p5.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p5.insert_text(pymupdf.Point(920, r.y1 - 2), "5", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 6 (Google Avaliações) ===
    p6 = doc[5]
    for b in p6.get_text('blocks'):
        if 'Avalie o Costão no Google' in b[4]:
            r = pymupdf.Rect(b[:4])
            p6.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 20, r.y1 + 3), color=None, fill=(1, 1, 1))
            p6.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Avalie o Jurerê Beach Village no Google. Leva menos de 1 minuto", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p6.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p6.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p6.insert_text(pymupdf.Point(920, r.y1 - 2), "6", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # === PÁGINA 7 (Por que vale para o hotel) ===
    p7 = doc[6]
    for b in p7.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p7.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.0902, 0.2157, 0.3686))
            p7.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))
            p7.insert_text(pymupdf.Point(920, r.y1 - 2), "7", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))

    # === PÁGINA 8 (Investimento & Fechamento) ===
    p8 = doc[7]
    for b in p8.get_text('blocks'):
        if 'Proposta de implantação Costão do Santinho' in b[4]:
            r = pymupdf.Rect(b[:4])
            p8.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 40, r.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(pymupdf.Point(r.x0, r.y1 - 3), "Proposta de implantação Jurerê Beach Village", fontname="helv", fontsize=13, color=(0.07, 0.09, 0.10))
        if 'Cartões NFC Costão' in b[4]:
            r = pymupdf.Rect(b[:4])
            p8.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 20, r.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=11, color=(0.07, 0.09, 0.10))
        if '109 unidades.' in b[4]:
            r = pymupdf.Rect(b[:4])
            p8.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(pymupdf.Point(r.x0, r.y0 + 10), "100 unidades. Cartões já configurados e funcionais. Suporte", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
            p8.insert_text(pymupdf.Point(r.x0, r.y0 + 22), "técnico de 2 anos na tecnologia de todas as placas.", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
        if 'Proposta · Cartões NFC' in b[4]:
            r = pymupdf.Rect(b[:4])
            p8.draw_rect(pymupdf.Rect(r.x0 - 5, r.y0 - 3, r.x1 + 10, r.y1 + 3), color=None, fill=(0.9451, 0.9882, 0.9922))
            p8.insert_text(pymupdf.Point(r.x0, r.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p8.insert_text(pymupdf.Point(920, r.y1 - 2), "8", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # Salvar o documento adaptado
    pdf_out_path = 'saida/proposta_jurere/Proposta_Comercial_Jurere_Beach_Village_Final.pdf'
    doc.save(pdf_out_path)
    print(f"Documento final salvo com sucesso em {pdf_out_path}")

    # Exportar as 8 páginas como imagens de alta fidelidade
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_out = f'saida/proposta_jurere/slide_{i+1:02d}.png'
        pix.save(img_out)
        print(f"Exportada lâmina {i+1} -> {img_out}")

if __name__ == '__main__':
    build_jurere_proposta()

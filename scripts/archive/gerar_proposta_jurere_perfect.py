import os
import subprocess
from PIL import Image, ImageDraw
import pymupdf as fitz

def build_perfect_proposal():
    os.makedirs('saida/proposta_jurere', exist_ok=True)
    
    # 1. Ler o SVG oficial da plaquinha com a cor #4DA2AD
    svg_path = 'BigBrain/handoff/placas_hoteis_layout02/02_02_jurer_beach_village/01_modelo_classico_cor_mae.svg'
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # 2. Criar HTML de renderização exata a 2000x2000 px para nitidez absoluta das fontes Outfit e Inter
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ background: transparent; width: 2000px; height: 2000px; overflow: hidden; }}
  svg {{ width: 2000px; height: 2000px; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

    html_file = 'saida/proposta_jurere/render_placa_2000.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 3. Renderizar com Headless Edge com renderização nativa de fontes web
    screenshot_raw = 'saida/proposta_jurere/placa_raw_2000.png'
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--window-size=2000,2000",
        f"--screenshot={os.path.abspath(screenshot_raw)}",
        f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)

    # 4. Processar a imagem com recorte de cantos arredondados perfeito (rx=120 px na escala 2000x2000)
    img_card = Image.open(screenshot_raw).convert('RGBA')
    img_card = img_card.crop((0, 0, 2000, 2000))
    
    mask = Image.new('L', (2000, 2000), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (2000, 2000)], radius=120, fill=255)
    img_card.putalpha(mask)
    
    placa_png_final = 'saida/proposta_jurere/01_modelo_classico_cor_mae_jurere_final.png'
    img_card.save(placa_png_final, format='PNG')
    print("Placa oficial com fontes perfeitas e cantos arredondados gerada com sucesso!")

    # 5. Inserir a plaquinha no PDF original de referência mantendo o layout e proporções intocadas
    pdf_in = 'C:/Users/Augusto/AppData/Local/hermes/profiles/designer/attachments/Proposta.pdf'
    doc = fitz.open(pdf_in)

    # === PÁGINA 1 (Capa) ===
    p1 = doc[0]
    # Cor de fundo exata da Capa: (0.0902, 0.2157, 0.3686) -> #17375E
    bg_p1 = (0.0902, 0.2157, 0.3686)
    
    # Substituir "Preparada para: Costão do Santinho Resort"
    for b in p1.get_text('blocks'):
        if 'Preparada para:' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=bg_p1)
            p1.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Preparada para: Jurerê Beach Village", fontname="helv", fontsize=11.5, color=(1, 1, 1))

    # Cobrir a área total de sombra e elementos vetoriais antigos da Capa com a cor de fundo do slide
    p1.draw_rect(fitz.Rect(505, 115, 960, 570), color=None, fill=bg_p1)
    
    # Inserir a placa oficial nos limites perfeitos: (551.25, 150.0, 911.25, 510.0)
    card_p1_rect = fitz.Rect(551.25, 150.0, 911.25, 510.0)
    p1.insert_image(card_p1_rect, filename=placa_png_final)

    for b in p1.get_text('blocks'):
        if 'C O S TA O' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 40, r_box.y0 - 3, r_box.x1 + 40, r_box.y1 + 3), color=None, fill=bg_p1)
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
    p4.insert_image(card_p4_rect, filename=placa_png_final)

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

    out_pdf = 'saida/proposta_jurere/Proposta_Comercial_Jurere_Beach_Village_Final_Aprovada.pdf'
    doc.save(out_pdf)
    print(f"Sucesso! PDF final gerado em: {out_pdf}")

    # Exportar imagens para conferência
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_out = f'saida/proposta_jurere/slide_final_aprovado_{i+1:02d}.png'
        pix.save(img_out)

if __name__ == '__main__':
    build_perfect_proposal()

import os
import subprocess
from PIL import Image, ImageDraw
import pymupdf as fitz

def build_pristine_proposal():
    os.makedirs('saida/proposta_jurere', exist_ok=True)
    
    # 1. Ler o SVG oficial da plaquinha com a cor #4DA2AD
    svg_path = 'BigBrain/handoff/placas_hoteis_layout02/02_02_jurer_beach_village/01_modelo_classico_cor_mae.svg'
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # 2. Criar HTML de renderização a 2000x2000 px
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

    # 3. Renderizar com Headless Edge
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
    print("Placa oficial transparente gerada com sucesso!")

    # 5. Processar o PDF original e eliminar os blocos/sombras duras de todas as lâminas
    pdf_in = 'C:/Users/Augusto/AppData/Local/hermes/profiles/designer/attachments/Proposta.pdf'
    doc = fitz.open(pdf_in)

    bg_dark = (0.0902, 0.2157, 0.3686)   # #17375E
    bg_light = (0.9451, 0.9882, 0.9922)  # #F1FCFD

    # ==================== PÁGINA 1 ====================
    p1 = doc[0]
    for b in p1.get_text('blocks'):
        if 'Preparada para:' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=bg_dark)
            p1.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Preparada para: Jurerê Beach Village", fontname="helv", fontsize=11.5, color=(1, 1, 1))

    # Limpar completamente a área da sombra antiga e inserir a placa limpa
    p1.draw_rect(fitz.Rect(500, 110, 965, 575), color=None, fill=bg_dark)
    card_p1_rect = fitz.Rect(551.25, 150.0, 911.25, 510.0)
    p1.insert_image(card_p1_rect, filename=placa_png_final)

    for b in p1.get_text('blocks'):
        if 'C O S TA O' in b[4]:
            r_box = fitz.Rect(b[:4])
            p1.draw_rect(fitz.Rect(r_box.x0 - 40, r_box.y0 - 3, r_box.x1 + 40, r_box.y1 + 3), color=None, fill=bg_dark)
            p1.insert_text(fitz.Point(625.0, r_box.y1 - 2), "J U R E R E B E A C H V I L L A G E . C O M . B R", fontname="helv", fontsize=8.5, color=(0.65, 0.95, 0.99))

    # ==================== PÁGINA 2 ====================
    p2 = doc[1]
    # Eliminar o quadrado de deslocamento ciano/duplo atrás dos 3 cards
    p2.draw_rect(fitz.Rect(40, 215, 950, 465), color=None, fill=bg_light)
    # Redesenhar os 3 cards brancos limpos e elegantes
    for x_offset, header_color in [
        (46.5, (0.302, 0.635, 0.678)),
        (351.75, (0.788, 0.541, 0.071)),
        (657.0, (0.090, 0.216, 0.369))
    ]:
        card_r = fitz.Rect(x_offset, 225.0, x_offset + 277.5, 450.0)
        p2.draw_rect(card_r, color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
        p2.draw_rect(fitz.Rect(x_offset, 225.0, x_offset + 277.5, 231.75), color=None, fill=header_color)

    for b in p2.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p2.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p2.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p2.insert_text(fitz.Point(920, r_box.y1 - 2), "2", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    p2.insert_text(fitz.Point(65.0, 275.0), "01", fontname="helv", fontsize=24, color=(0.302, 0.635, 0.678))
    p2.insert_text(fitz.Point(65.0, 310.0), "Sem aplicativo", fontname="helv", fontsize=15, color=(0.07, 0.09, 0.10))
    p2.insert_text(fitz.Point(65.0, 345.0), "O hóspede aproxima o celular e acessa\ntudo instantaneamente, sem precisar\nbaixar nenhum aplicativo.", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))

    p2.insert_text(fitz.Point(370.0, 275.0), "02", fontname="helv", fontsize=24, color=(0.788, 0.541, 0.071))
    p2.insert_text(fitz.Point(370.0, 310.0), "Mais avaliações", fontname="helv", fontsize=15, color=(0.07, 0.09, 0.10))
    p2.insert_text(fitz.Point(370.0, 345.0), "Aumente as notas e o volume de\navaliações 5 estrelas no Google Meu\nNegócio do Jurerê Beach Village.", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))

    p2.insert_text(fitz.Point(675.0, 275.0), "03", fontname="helv", fontsize=24, color=(0.090, 0.216, 0.369))
    p2.insert_text(fitz.Point(675.0, 310.0), "Presença de luxo", fontname="helv", fontsize=15, color=(0.07, 0.09, 0.10))
    p2.insert_text(fitz.Point(675.0, 345.0), "Peça tátil de alto padrão em acrílico\n100x100mm, harmonizada com a\narquitetura e a identidade do hotel.", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))

    # ==================== PÁGINA 3 ====================
    p3 = doc[2]
    for b in p3.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p3.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p3.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p3.insert_text(fitz.Point(920, r_box.y1 - 2), "3", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # ==================== PÁGINA 4 ====================
    p4 = doc[3]
    # Limpar completamente a área da sombra dura e do cartão antigo da P4
    p4.draw_rect(fitz.Rect(15, 80, 570, 640), color=None, fill=bg_light)
    card_p4_rect = fitz.Rect(65.25, 120.0, 519.75, 574.5)
    p4.insert_image(card_p4_rect, filename=placa_png_final)

    for b in p4.get_text('blocks'):
        if 'C A R T Ã O · C O S T Ã O' in b[4] or 'CARTÃO · COSTÃO' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 4, r_box.x1 + 60, r_box.y1 + 4), color=None, fill=bg_light)
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "C A R T Ã O · J U R E R Ê B E A C H V I L L A G E", fontname="helv", fontsize=9.0, color=(0.302, 0.635, 0.678))
        if 'Costão SPA & Relax' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 2, r_box.y0 - 2, r_box.x1 + 10, r_box.y1 + 2), color=None, fill=bg_light)
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Piscinas & Hidro", fontname="helv", fontsize=11.0, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p4.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p4.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p4.insert_text(fitz.Point(920, r_box.y1 - 2), "4", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # ==================== PÁGINA 5 ====================
    p5 = doc[4]
    # Limpar a sombra offset sob os mockups da P5
    p5.draw_rect(fitz.Rect(380, 45, 765, 575), color=None, fill=bg_light)
    
    # Redesenhar a tela do celular 1
    p5.draw_rect(fitz.Rect(386.25, 54.0, 552.75, 556.5), color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
    p5.draw_rect(fitz.Rect(386.25, 54.0, 552.75, 166.5), color=None, fill=(0.07, 0.09, 0.10))
    p5.insert_text(fitz.Point(405.0, 105.0), "Jurerê Beach", fontname="helv", fontsize=15, color=(1, 1, 1))
    p5.insert_text(fitz.Point(405.0, 125.0), "Village", fontname="helv", fontsize=15, color=(1, 1, 1))
    p5.insert_text(fitz.Point(405.0, 148.0), "BEM-VINDO AO HOTEL", fontname="helv", fontsize=7.5, color=(0.302, 0.635, 0.678))

    menu_items = [
        ("Restaurante Fajã", "Cardápio e reservas"),
        ("Piscinas & Hidro", "Horários e toalhas"),
        ("Programação Infantil", "Atividades de recreação"),
        ("Pé na Areia", "Serviços de praia"),
        ("Room Service", "Pedidos no quarto"),
        ("Recepção & Concierge", "Atendimento direto")
    ]
    y_pos = 195.0
    for title, sub in menu_items:
        p5.insert_text(fitz.Point(405.0, y_pos), title, fontname="helv", fontsize=9.0, color=(0.07, 0.09, 0.10))
        p5.insert_text(fitz.Point(405.0, y_pos + 11), sub, fontname="helv", fontsize=7.0, color=(0.45, 0.50, 0.55))
        p5.draw_line(fitz.Point(395.0, y_pos + 18), fitz.Point(545.0, y_pos + 18), color=(0.90, 0.93, 0.94), width=0.5)
        y_pos += 37.5

    p5.draw_rect(fitz.Rect(393.75, 506.25, 545.25, 547.5), color=None, fill=(0.302, 0.635, 0.678))
    p5.insert_text(fitz.Point(425.0, 530.0), "Avaliar no Google", fontname="helv", fontsize=9.5, color=(1, 1, 1))

    # Redesenhar a tela do celular 2
    p5.draw_rect(fitz.Rect(581.25, 54.0, 747.75, 436.5), color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
    p5.draw_rect(fitz.Rect(591.75, 99.75, 737.25, 165.75), color=None, fill=bg_light)
    p5.insert_text(fitz.Point(605.0, 125.0), "Jurerê Beach Village", fontname="helv", fontsize=10.5, color=(0.07, 0.09, 0.10))
    p5.insert_text(fitz.Point(605.0, 142.0), "4.8 ★★★★★ (2.418 avaliações)", fontname="helv", fontsize=7.5, color=(0.788, 0.541, 0.071))

    p5.draw_rect(fitz.Rect(588.75, 254.25, 740.25, 357.0), color=None, fill=(0.258, 0.521, 0.957))
    p5.insert_text(fitz.Point(620.0, 290.0), "Google Avaliações", fontname="helv", fontsize=11, color=(1, 1, 1))
    p5.insert_text(fitz.Point(630.0, 312.0), "★★★★★", fontname="helv", fontsize=13, color=(0.97, 0.68, 0.20))
    p5.draw_rect(fitz.Rect(594.75, 327.0, 734.25, 346.5), color=None, fill=(0.090, 0.216, 0.369))
    p5.insert_text(fitz.Point(625.0, 340.0), "Escrever uma avaliação", fontname="helv", fontsize=8.0, color=(1, 1, 1))

    for b in p5.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p5.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p5.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p5.insert_text(fitz.Point(920, r_box.y1 - 2), "5", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # ==================== PÁGINA 6 ====================
    p6 = doc[5]
    p6.draw_rect(fitz.Rect(545, 60, 930, 345), color=None, fill=bg_light)
    p6.draw_rect(fitz.Rect(551.25, 69.0, 915.0, 331.5), color=None, fill=(0.258, 0.521, 0.957))
    p6.insert_text(fitz.Point(645.0, 160.0), "Jurerê Beach Village", fontname="helv", fontsize=16, color=(1, 1, 1))
    p6.insert_text(fitz.Point(635.0, 185.0), "no Google Meu Negócio", fontname="helv", fontsize=12, color=(0.90, 0.95, 1.0))
    p6.insert_text(fitz.Point(645.0, 238.0), "★ ★ ★ ★ ★", fontname="helv", fontsize=22, color=(0.97, 0.68, 0.20))
    p6.draw_rect(fitz.Rect(639.0, 271.5, 827.25, 312.75), color=None, fill=(0.090, 0.216, 0.369))
    p6.insert_text(fitz.Point(670.0, 297.0), "Deixar uma avaliação 5 estrelas", fontname="helv", fontsize=9.0, color=(1, 1, 1))

    p6.draw_rect(fitz.Rect(60, 480, 930, 640), color=None, fill=bg_light)
    cards_p6 = [
        (65.25, "1. Aproximação", "Hóspede toca o celular na placa do quarto ou restaurante."),
        (282.0, "2. Abertura Direta", "O navegador abre diretamente a tela de avaliação com 5 estrelas."),
        (498.75, "3. Escrita Rápida", "Basta digitar o elogio e clicar em publicar em menos de 1 min."),
        (715.5, "4. Indexação Local", "Mais relevância e posições de destaque no Google Maps e busca.")
    ]
    for x_c, tit, txt in cards_p6:
        p6.draw_rect(fitz.Rect(x_c, 483.75, x_c + 201.0, 626.25), color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
        p6.insert_text(fitz.Point(x_c + 15, 520.0), tit, fontname="helv", fontsize=11, color=(0.07, 0.09, 0.10))
        p6.insert_text(fitz.Point(x_c + 15, 545.0), txt, fontname="helv", fontsize=8.5, color=(0.40, 0.45, 0.50))

    for b in p6.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p6.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p6.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p6.insert_text(fitz.Point(920, r_box.y1 - 2), "6", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    # ==================== PÁGINA 7 ====================
    p7 = doc[6]
    p7.draw_rect(fitz.Rect(55, 195, 925, 525), color=None, fill=bg_dark)
    blocks_p7 = [
        (65.25, 207.0, "Recepção & Concierge", "Cartão no balcão de check-in / atendimento agiliza o acesso à programação e serviços."),
        (499.5, 207.0, "Apartamentos & Suítes", "Posicionado na mesa de cabeceira ou bancada para acesso fácil a room service e lazer."),
        (65.25, 375.0, "Restaurante & Bar", "Acesso ao cardápio digital do Fajã e carta de vinhos sem cardápios físicos engordurados."),
        (499.5, 375.0, "Área de Piscinas & Praia", "Placas resistentes a umidade para atendimento rápido no serviço pé na areia.")
    ]
    for x_b, y_b, tit, txt in blocks_p7:
        p7.draw_rect(fitz.Rect(x_b, y_b, x_b + 416.25, y_b + 142.5), color=(0.20, 0.35, 0.50), fill=(0.12, 0.28, 0.47), width=1)
        p7.insert_text(fitz.Point(x_b + 20, y_b + 40), tit, fontname="helv", fontsize=13, color=(1, 1, 1))
        p7.insert_text(fitz.Point(x_b + 20, y_b + 75), txt, fontname="helv", fontsize=9.5, color=(0.80, 0.90, 0.95))

    for b in p7.get_text('blocks'):
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p7.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_dark)
            p7.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))
            p7.insert_text(fitz.Point(920, r_box.y1 - 2), "7", fontname="helv", fontsize=9, color=(0.65, 0.75, 0.85))

    # ==================== PÁGINA 8 ====================
    p8 = doc[7]
    p8.draw_rect(fitz.Rect(55, 155, 930, 525), color=None, fill=bg_light)
    
    p8.draw_rect(fitz.Rect(65.25, 166.5, 511.5, 511.5), color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
    p8.insert_text(fitz.Point(85.0, 205.0), "Escopo do Projeto", fontname="helv", fontsize=15, color=(0.07, 0.09, 0.10))
    p8.insert_text(fitz.Point(85.0, 245.0), "• 100 Placas NFC 100x100mm personalizadas com a marca", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(85.0, 275.0), "• Configuração e integração do link de destino (Cardápio / Avaliações)", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(85.0, 305.0), "• Acrílico nobre de alta durabilidade com proteção UV e água", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(85.0, 335.0), "• QR Code de contingência embutido em alta resolução", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(85.0, 365.0), "• Suporte técnico especializado de 2 anos nos chips NFC", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(85.0, 395.0), "• Entrega física pronta para ativação imediata no hotel", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))

    p8.draw_rect(fitz.Rect(546.0, 292.5, 915.0, 511.5), color=(0.85, 0.92, 0.94), fill=(1, 1, 1), width=1)
    p8.insert_text(fitz.Point(575.0, 330.0), "Investimento Total", fontname="helv", fontsize=15, color=(0.07, 0.09, 0.10))
    p8.insert_text(fitz.Point(575.0, 365.0), "100 unidades · Cartões NFC Ativos", fontname="helv", fontsize=10.5, color=(0.302, 0.635, 0.678))
    p8.draw_line(fitz.Point(575.0, 403.5), fitz.Point(888.0, 403.5), color=(0.85, 0.90, 0.92), width=1)
    p8.insert_text(fitz.Point(575.0, 445.0), "✓ Entrega expressa inclusa em Florianópolis", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))
    p8.insert_text(fitz.Point(575.0, 475.0), "✓ Configuração prévia e suporte de homologação", fontname="helv", fontsize=9.5, color=(0.35, 0.40, 0.45))

    for b in p8.get_text('blocks'):
        if 'Proposta de implantação Costão do Santinho' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 40, r_box.y1 + 3), color=None, fill=(1, 1, 1))
            p8.insert_text(fitz.Point(r_box.x0, r_box.y1 - 3), "Proposta de implantação Jurerê Beach Village", fontname="helv", fontsize=13, color=(0.07, 0.09, 0.10))
        if 'Proposta · Cartões NFC' in b[4]:
            r_box = fitz.Rect(b[:4])
            p8.draw_rect(fitz.Rect(r_box.x0 - 5, r_box.y0 - 3, r_box.x1 + 10, r_box.y1 + 3), color=None, fill=bg_light)
            p8.insert_text(fitz.Point(r_box.x0, r_box.y1 - 2), "Proposta · Cartões NFC Jurerê Beach Village", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))
            p8.insert_text(fitz.Point(920, r_box.y1 - 2), "8", fontname="helv", fontsize=9, color=(0.42, 0.47, 0.50))

    out_pdf = 'saida/proposta_jurere/Proposta_Comercial_Jurere_Beach_Village_Pristine.pdf'
    doc.save(out_pdf)
    print(f"Sucesso total! PDF sem sombras duras gerado em: {out_pdf}")

    # Exportar TODAS as 8 lâminas em imagens PNG
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_out = f'saida/proposta_jurere/slide_pristine_{i+1:02d}.png'
        pix.save(img_out)
        print(f"Exportada lâmina {i+1}: {img_out}")

if __name__ == '__main__':
    build_pristine_proposal()

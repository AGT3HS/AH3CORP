import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# ==============================================================================
# DESIGN TOKENS OFICIAIS (GUIA DE IDENTIDADE COSTÃO DO SANTINHO)
# ==============================================================================
BG_OFFWHITE = (245, 244, 238)    # #F5F4EE
BG_SAND_CREAM = (250, 240, 202)  # #FAF0CA
BG_OCEAN_DARK = (13, 59, 102)    # #0D3B66
BG_OCEAN_DEEP = (10, 42, 74)     # #0A2A4A

CARD_WHITE = (255, 255, 255)
BORDER_SUBTLE = (220, 222, 215)
BORDER_GOLD = (244, 211, 94)

BLUE_OCEAN = (13, 59, 102)       # #0D3B66
GOLD_SOLAR = (244, 211, 94)      # #F4D35E
AMBER_WARM = (238, 150, 75)      # #EE964B
GRAPHITE_DARK = (26, 37, 48)     # #1A2530
STONE_MUTED = (138, 133, 120)    # #8A8578
RED_SPA = (172, 24, 46)

TEXT_DARK = (26, 37, 48)         # #1A2530
TEXT_BODY = (75, 86, 79)         # #4B564F
TEXT_LIGHT = (255, 255, 255)

OUTPUT_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"
PDF_FINAL = "C:/Users/Augusto/Desktop/AH3/Proposta_Comercial_Costao_Alternativa.pdf"

# Tipografia
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    paragraphs = text.split("\n")
    lines = []
    for p in paragraphs:
        if not p.strip():
            lines.append("")
            continue
        words = p.split(" ")
        curr_line = words[0]
        for w in words[1:]:
            test_line = curr_line + " " + w
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                curr_line = test_line
            else:
                lines.append(curr_line)
                curr_line = w
        lines.append(curr_line)
    return lines

# ==============================================================================
# NOVA ESTRUTURA: ESTILO MAIS MINIMALISTA E EDITORIAL
# ==============================================================================
def draw_layout_base(img, title, kicker=None):
    draw = ImageDraw.Draw(img)
    if kicker:
        draw.text((80, 60), kicker.upper(), font=get_font(FONT_SANS_BOLD, 14), fill=STONE_MUTED)
    draw.text((80, 90), title, font=get_font(FONT_SERIF_BOLD, 48), fill=TEXT_DARK)
    draw.line([(80, 160), (300, 160)], fill=BLUE_OCEAN, width=3)
    return draw

def build_slide_minimal(page_num, title, content_block, kicker="CONCEITO"):
    img = Image.new("RGB", (W, H), BG_OFFWHITE)
    draw = draw_layout_base(img, title, kicker)
    
    # Grid diferenciado: texto longo solto, sem cards pesados
    lines = wrap_text(content_block, get_font(FONT_SERIF, 24), 1000, draw)
    y = 220
    for l in lines:
        draw.text((80, y), l, font=get_font(FONT_SERIF, 24), fill=TEXT_BODY)
        y += 40
    
    # Elemento gráfico lateral (barra de cor)
    draw.rectangle([W-150, 0, W, H], fill=BLUE_OCEAN)
    
    # Rodapé
    draw.text((80, H-60), f"Costão • {page_num}", font=get_font(FONT_SANS, 14), fill=STONE_MUTED)
    return img

def build_slide_showcase(page_num, title, items, kicker="DETALHES"):
    img = Image.new("RGB", (W, H), CARD_WHITE)
    draw = draw_layout_base(img, title, kicker)
    
    # Grid de fotos/cards super minimalista
    by = 220
    for tit, desc in items:
        draw.text((80, by), tit, font=get_font(FONT_SANS_BOLD, 22), fill=BLUE_OCEAN)
        draw.text((80, by+30), desc, font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
        by += 100
        
    return img

def gerar_proposta_alternativa():
    print("Gerando Proposta Comercial Criativa (Estrutura Experimental)...")
    
    slides = [
        lambda: build_slide_minimal(1, "A Nova Experiência\nCostão do Santinho", 
                                    "Redefinimos a jornada do hóspede.\nMenos fricção, mais encantamento.\nTecnologia invisível que opera a favor do serviço.", "PROPOSTA"),
        lambda: build_slide_showcase(2, "Pilares Estratégicos", 
                                    [("Conexão Nativiva", "Um toque para o mundo do resort."),
                                     ("Gestão em Tempo Real", "Informação que evolui com o dia."),
                                     ("Conversão Assertiva", "Captura de avaliações sem esforço.")], "BENEFÍCIOS"),
        lambda: build_slide_minimal(3, "Compromisso de Entrega", 
                                    "Implantação rápida, suporte contínuo e\nzero necessidade de treinamento complexo.\nO resort foca no hóspede, nós cuidamos da tecnologia.")
    ]

    pdf = pymupdf.open()
    for num, builder_fn in enumerate(slides, 1):
        img = builder_fn()
        png_path = os.path.join(OUTPUT_DIR, f"proposta_alt_s{num}.png")
        img.save(png_path)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(PDF_FINAL)
    pdf.close()
    print(f"=== SUCESSO: Proposta Criativa Teste gerada em {PDF_FINAL} ===")

if __name__ == "__main__":
    gerar_proposta_alternativa()

import os
import pymupdf
from PIL import Image

from gerar_proposta_costao_v3 import OUTPUT_DIR, PDF_FINAL
from gerar_proposta_costao_v3_slides import build_slide_1, build_slide_8

def build_pdf_proposta():
    print("Gerando Slides de alta fidelidade...")
    
    s1 = build_slide_1()
    s8 = build_slide_8()
    
    s1_path = os.path.join(OUTPUT_DIR, "v3_costao_s1.png")
    s8_path = os.path.join(OUTPUT_DIR, "v3_costao_s8.png")
    
    s1.save(s1_path)
    s8.save(s8_path)
    print(f"-> Slides renderizados em PNG.")
    
    # Montando PDF (apenas de teste dos dois slides refeitos para aprovação gráfica rápida)
    pdf = pymupdf.open()
    
    for pt in [s1_path, s8_path]:
        img_doc = pymupdf.open(pt)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()
        
    pdf_teste = PDF_FINAL.replace(".pdf", "_v3_Preview.pdf")
    pdf.save(pdf_teste)
    pdf.close()
    
    print(f"-> PDF Preview exportado puro com sucesso: {pdf_teste}")

if __name__ == "__main__":
    build_pdf_proposta()

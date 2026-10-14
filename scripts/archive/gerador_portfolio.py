import os
import subprocess
import pymupdf

BASE_DIR = r"C:\Users\Augusto\Desktop\AH3\BigBrain\portfolioreferencias"
HTML_DIR = os.path.join(BASE_DIR, "html_pdfs")
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
PREVIEW_DIR = os.path.join(BASE_DIR, "previews")
WEB_DIR = os.path.join(BASE_DIR, "paginas_web")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_pdf_and_png(html_content, name, width_px=1200, height_px=1697):
    html_path = os.path.join(HTML_DIR, f"{name}.html")
    pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")
    png_path = os.path.join(PREVIEW_DIR, f"{name}.png")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    
    # Gerar PNG de alta resolução da página 1 via PyMuPDF
    doc = pymupdf.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=150)
    pix.save(png_path)
    doc.close()
    
    print(f"[✓] Gerado: {name} -> {pdf_path} & {png_path}")
    return pdf_path, png_path

print("Setup de geracao configurado com sucesso.")

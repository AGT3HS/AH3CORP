"""
Script Gerador da Proposta Comercial Oficial 'Aceleração Gastronômica' (8 Slides)
Fiel ao design, cores, tipografia, proporções e estrutura de beta.pdf,
incorporando com destaque a caixa oficial:
- Badge: NOVO · VISIBILIDADE EM IA
- Título: Camada IA: faça a IA recomendar o cliente.
- Texto: Toda proposta pode incluir visibilidade em IA (ChatGPT, Gemini, busca com IA), apoiada em perfil, avaliações e dados.
"""

import os
import subprocess
import base64
import pymupdf

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def generate_proposal_html():
    img1_path = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\beta_extracted_imgs\page_6_img_1.png"
    img2_path = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\beta_extracted_imgs\page_6_img_2.png"
    
    img1_b64 = get_base64_image(img1_path)
    img2_b64 = get_base64_image(img2_path)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Proposta Comercial · Aceleração Gastronômica</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,600&display=swap" rel="stylesheet">
<style>
  @page {{
    size: 842pt 595pt;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0d0f12;
    color: #f6f5f0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 842pt;
    height: 595pt;
    page-break-after: always;
    position: relative;
    overflow: hidden;
    background: #0e1015;
    padding: 36pt 42pt 22pt 42pt;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .slide-body {{
    height: 488pt;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Elementos Comuns e Tipografia */
  .footer {{
    height: 22pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #1f232b;
    padding-top: 6pt;
    flex-shrink: 0;
  }}
  .footer-brand {{
    font-size: 10pt;
    font-weight: 300;
    letter-spacing: 2px;
    color: #6f7076;
    text-transform: uppercase;
  }}
  .footer-brand span {{
    font-weight: 700;
    color: #ff5a36;
  }}
  .footer-page {{
    font-size: 10.5pt;
    font-weight: 500;
    color: #6f7076;
    font-variant-numeric: tabular-nums;
  }}

  .kicker {{
    font-size: 10.5pt;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #ff5a36;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 6pt;
    margin-bottom: 4pt;
  }}
  
  .slide-header {{
    flex-shrink: 0;
  }}
  .slide-title {{
    font-size: 33pt;
    font-weight: 700;
    line-height: 1.15;
    color: #f6f5f0;
    letter-spacing: -0.5px;
  }}
  .slide-subtitle {{
    font-size: 14.5pt;
    font-weight: 300;
    color: #b6b7bd;
    margin-top: 4pt;
    line-height: 1.35;
  }}

  /* Header com Ícone Lateral */
  .header-with-icon {{
    display: flex;
    align-items: flex-start;
    gap: 16pt;
    flex-shrink: 0;
  }}
  .header-icon-box {{
    width: 58pt;
    height: 58pt;
    background: #2b1714;
    border: 1px solid #5a2820;
    border-radius: 14pt;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .header-icon-box svg {{
    width: 30pt;
    height: 30pt;
    stroke: #ff5a36;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }}

  /* SLIDE 1: CAPA */
  .s1-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }}
  .s1-kicker-left {{
    font-size: 11pt;
    font-weight: 400;
    letter-spacing: 3px;
    color: #9c9da4;
    text-transform: uppercase;
  }}
  .s1-badge-right {{
    border: 1px solid #5a2820;
    background: #1c1414;
    color: #c9c4bc;
    font-size: 9.5pt;
    font-weight: 400;
    letter-spacing: 1.5px;
    padding: 5pt 14pt;
    border-radius: 6pt;
    text-transform: uppercase;
  }}
  .s1-hero {{
    flex-shrink: 0;
  }}
  .s1-hero-line {{
    font-size: 48pt;
    font-weight: 800;
    line-height: 1.08;
    color: #f6f5f0;
    letter-spacing: -1px;
  }}
  .s1-hero-line.highlight {{
    color: #ff5a36;
  }}
  .s1-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14pt;
  }}
  .s1-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 12pt;
    padding: 16pt 20pt;
    display: flex;
    align-items: center;
    gap: 16pt;
  }}
  .s1-card-icon {{
    width: 44pt;
    height: 44pt;
    background: #2b1714;
    border-radius: 10pt;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .s1-card-icon svg {{
    width: 24pt;
    height: 24pt;
    stroke: #ff5a36;
    fill: none;
    stroke-width: 2;
  }}
  .s1-card-title {{
    font-size: 15pt;
    font-weight: 700;
    color: #f6f5f0;
    line-height: 1.2;
  }}
  .s1-card-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
    margin-top: 3pt;
  }}
  .s1-bottom-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12pt;
    color: #9c9da4;
    padding: 4pt 2pt;
    flex-shrink: 0;
  }}
  .s1-bottom-bar strong {{
    color: #f6f5f0;
    font-weight: 600;
  }}

  /* SLIDE 2: VISÃO GERAL COM CAIXA IA */
  .s2-cycle-grid {{
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr;
    align-items: center;
    gap: 14pt;
  }}
  .s2-cycle-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 14pt;
    padding: 22pt 22pt;
    position: relative;
    height: 215pt;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .s2-watermark {{
    position: absolute;
    top: 14pt;
    right: 18pt;
    font-size: 50pt;
    font-weight: 800;
    color: #232732;
    line-height: 1;
  }}
  .s2-card-icon {{
    width: 44pt;
    height: 44pt;
    background: #2b1714;
    border-radius: 12pt;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .s2-card-icon svg {{
    width: 24pt;
    height: 24pt;
    stroke: #ff5a36;
    fill: none;
    stroke-width: 2;
  }}
  .s2-card-title {{
    font-size: 17pt;
    font-weight: 700;
    color: #f6f5f0;
    line-height: 1.2;
    margin-top: 10pt;
  }}
  .s2-card-desc {{
    font-size: 11.5pt;
    font-weight: 300;
    color: #9c9da4;
    line-height: 1.45;
    margin-top: 6pt;
  }}
  .s2-arrow {{
    font-size: 24pt;
    color: #ff5a36;
    font-weight: 700;
  }}
  
  .s2-bottom-container {{
    display: grid;
    grid-template-columns: 1fr 1.25fr;
    gap: 16pt;
  }}
  .s2-restart-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-left: 4.5pt solid #f7c765;
    border-radius: 12pt;
    padding: 18pt 20pt;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .s2-restart-title {{
    font-size: 14pt;
    font-weight: 700;
    color: #f7c765;
    margin-bottom: 4pt;
  }}
  .s2-restart-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #eae7df;
    line-height: 1.45;
  }}

  .s2-ia-box {{
    background: #17191e;
    border: 1px solid #3d221c;
    border-left: 4.5pt solid #ff5a36;
    border-radius: 12pt;
    padding: 18pt 20pt;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .s2-ia-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4pt;
    background: #ff5a36;
    color: #ffffff;
    font-size: 8.5pt;
    font-weight: 800;
    letter-spacing: 1.2px;
    padding: 3pt 8pt;
    border-radius: 4pt;
    text-transform: uppercase;
    margin-bottom: 6pt;
    width: fit-content;
  }}
  .s2-ia-title {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #f6f5f0;
    line-height: 1.25;
    margin-bottom: 4pt;
  }}
  .s2-ia-desc {{
    font-size: 10.5pt;
    font-weight: 300;
    color: #b6b7bd;
    line-height: 1.4;
  }}

  /* SLIDE 3: PILAR 1 FOTOS */
  .s3-content-grid {{
    display: grid;
    grid-template-columns: 240pt 1fr;
    gap: 20pt;
  }}
  .s3-hero-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 14pt;
    padding: 22pt;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 225pt;
  }}
  .s3-giant-num {{
    font-size: 105pt;
    font-weight: 800;
    color: #ff5a36;
    line-height: 0.85;
    letter-spacing: -3px;
  }}
  .s3-giant-label {{
    font-size: 16pt;
    font-weight: 700;
    color: #f6f5f0;
    line-height: 1.2;
    margin-top: 12pt;
  }}
  .s3-details-col {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 225pt;
  }}
  .s3-item-row {{
    display: flex;
    flex-direction: column;
    gap: 3pt;
  }}
  .s3-item-title {{
    font-size: 15pt;
    font-weight: 700;
    color: #f6f5f0;
  }}
  .s3-item-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
  }}
  .s3-pills-row {{
    display: flex;
    align-items: center;
    gap: 8pt;
    margin-top: 4pt;
  }}
  .s3-pills-label {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
  }}
  .s3-pill {{
    background: #1f232b;
    border: 1px solid #2d323e;
    color: #f6f5f0;
    font-size: 10.5pt;
    font-weight: 600;
    padding: 5pt 12pt;
    border-radius: 6pt;
  }}
  .s3-stats-container {{
    display: flex;
    flex-direction: column;
    gap: 8pt;
  }}
  .s3-stats-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14pt;
  }}
  .s3-stat-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 12pt;
    padding: 16pt 20pt;
    display: flex;
    align-items: center;
    gap: 16pt;
  }}
  .s3-stat-num {{
    font-size: 34pt;
    font-weight: 800;
    color: #ff5a36;
    line-height: 1;
    flex-shrink: 0;
  }}
  .s3-stat-desc {{
    font-size: 10.5pt;
    font-weight: 300;
    color: #efece4;
    line-height: 1.35;
  }}
  .s3-footnote {{
    font-size: 9pt;
    color: #6f7076;
    margin-top: 2pt;
  }}

  /* SLIDE 4 & 5: LISTA DE CHECKS + CARDS LATERAIS */
  .two-col-layout {{
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 22pt;
    height: 290pt;
  }}
  .check-list {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .check-item {{
    display: flex;
    align-items: flex-start;
    gap: 12pt;
  }}
  .check-icon {{
    width: 24pt;
    height: 24pt;
    background: #132b1e;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2pt;
  }}
  .check-icon svg {{
    width: 13pt;
    height: 13pt;
    stroke: #3ddc84;
    stroke-width: 2.5;
    fill: none;
  }}
  .check-title {{
    font-size: 14.5pt;
    font-weight: 700;
    color: #f6f5f0;
    line-height: 1.2;
  }}
  .check-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
    line-height: 1.35;
  }}

  .right-cards-stack {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14pt;
  }}
  .stat-card-highlight {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 14pt;
    padding: 20pt 22pt;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .stat-giant-val {{
    font-size: 48pt;
    font-weight: 800;
    color: #ff5a36;
    line-height: 1;
    margin-bottom: 8pt;
  }}
  .stat-text {{
    font-size: 11.5pt;
    font-weight: 300;
    color: #efece4;
    line-height: 1.4;
  }}
  .stat-source {{
    font-size: 8.5pt;
    color: #6f7076;
    margin-top: 8pt;
  }}

  .result-card-green {{
    background: #111e18;
    border: 1px solid #1e3d2b;
    border-radius: 14pt;
    padding: 18pt 22pt;
  }}
  .result-tag {{
    font-size: 9.5pt;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #3ddc84;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 4pt;
    margin-bottom: 6pt;
  }}
  .result-text {{
    font-size: 12.5pt;
    font-weight: 500;
    color: #f6f5f0;
    line-height: 1.4;
  }}

  .alert-card-red {{
    background: #231414;
    border: 1px solid #4a2020;
    border-left: 5pt solid #ff5a36;
    border-radius: 14pt;
    padding: 20pt 22pt;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .alert-text-top {{
    font-size: 12.5pt;
    font-weight: 300;
    color: #f6f5f0;
    line-height: 1.45;
    margin-bottom: 10pt;
  }}
  .alert-text-top strong {{
    color: #ff5a36;
    font-weight: 700;
  }}
  .alert-punchline {{
    font-size: 14pt;
    font-weight: 700;
    color: #f6f5f0;
  }}

  .bottom-callout-banner {{
    background: #17191e;
    border: 1px solid #252830;
    border-left: 4.5pt solid #ff5a36;
    border-radius: 10pt;
    padding: 14pt 20pt;
    font-size: 13pt;
    color: #f6f5f0;
    line-height: 1.35;
    flex-shrink: 0;
  }}
  .bottom-callout-banner strong {{
    color: #ff5a36;
    font-weight: 700;
  }}

  /* SLIDE 6: PILAR 4 NFC */
  .s6-middle-grid {{
    display: grid;
    grid-template-columns: 160pt 160pt 1fr;
    gap: 18pt;
    align-items: center;
    height: 165pt;
  }}
  .s6-mockup-img {{
    width: 160pt;
    height: 160pt;
    object-fit: contain;
    border-radius: 12pt;
  }}
  .s6-benefits {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 160pt;
  }}
  .s6-benefit-item {{
    display: flex;
    align-items: center;
    gap: 10pt;
    font-size: 12.5pt;
    font-weight: 600;
    color: #f6f5f0;
  }}

  .s6-pricing-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 14pt;
  }}
  .s6-price-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 12pt;
    padding: 16pt 20pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .s6-price-card.featured {{
    background: #1f1b13;
    border: 1px solid #5a441e;
  }}
  .s6-price-label {{
    font-size: 12pt;
    font-weight: 300;
    color: #9c9da4;
    line-height: 1.25;
  }}
  .s6-price-card.featured .s6-price-label {{
    color: #f7c765;
    font-weight: 500;
  }}
  .s6-price-val {{
    font-size: 24pt;
    font-weight: 800;
    color: #f6f5f0;
  }}
  .s6-price-card.featured .s6-price-val {{
    color: #f7c765;
  }}

  /* SLIDE 7: INVESTIMENTO */
  .s7-grid {{
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 22pt;
    height: 300pt;
  }}
  .s7-items-list {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .s7-item-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12pt 0;
    border-bottom: 1px solid #1f232b;
  }}
  .s7-item-info-title {{
    font-size: 14.5pt;
    font-weight: 700;
    color: #f6f5f0;
  }}
  .s7-item-info-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
  }}
  .s7-item-price {{
    font-size: 22pt;
    font-weight: 800;
    color: #f6f5f0;
    text-align: right;
  }}
  .s7-item-row.bonus .s7-item-info-title {{
    color: #f7c765;
  }}
  .s7-item-row.bonus .s7-item-info-desc {{
    color: #c9a95f;
  }}
  .s7-item-row.bonus .s7-item-price {{
    color: #f7c765;
    font-size: 17pt;
  }}
  .s7-bonus-sub {{
    font-size: 9.5pt;
    color: #c9a95f;
    font-weight: 400;
  }}

  .s7-package-card {{
    background: #0d1e15;
    border: 1px solid #1c4530;
    border-radius: 16pt;
    padding: 22pt;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .s7-rec-badge {{
    display: inline-block;
    background: #f7c765;
    color: #1a1a12;
    font-size: 9pt;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 3pt 10pt;
    border-radius: 4pt;
    text-transform: uppercase;
    width: fit-content;
  }}
  .s7-pack-name {{
    font-size: 16pt;
    font-weight: 700;
    color: #f6f5f0;
    margin-top: 6pt;
  }}
  .s7-pack-price {{
    font-size: 52pt;
    font-weight: 800;
    color: #f7c765;
    line-height: 1;
    margin: 6pt 0;
  }}
  .s7-pack-savings {{
    font-size: 11.5pt;
    color: #9db8a8;
    margin-bottom: 8pt;
  }}
  .s7-pack-savings strong {{
    color: #3ddc84;
  }}
  .s7-pack-terms {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #f6f5f0;
    border-top: 1px solid #1c4530;
    padding-top: 8pt;
    margin-bottom: 8pt;
  }}
  .s7-pack-breakeven {{
    font-size: 10pt;
    color: #e7efe9;
    line-height: 1.4;
    background: #091710;
    padding: 9pt 12pt;
    border-radius: 8pt;
  }}
  .s7-pack-breakeven strong {{
    color: #3ddc84;
  }}

  .s7-guarantees-bar {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12pt;
    border-top: 1px solid #1f232b;
    padding-top: 12pt;
    flex-shrink: 0;
  }}
  .s7-guarantee-item {{
    display: flex;
    align-items: center;
    gap: 8pt;
    font-size: 11pt;
    font-weight: 600;
    color: #f6f5f0;
  }}

  /* SLIDE 8: PRÓXIMO PASSO */
  .s8-steps-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16pt;
  }}
  .s8-step-card {{
    background: #17191e;
    border: 1px solid #252830;
    border-radius: 14pt;
    padding: 22pt;
    height: 145pt;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .s8-step-num {{
    font-size: 34pt;
    font-weight: 800;
    color: #ff5a36;
    line-height: 1;
  }}
  .s8-step-title {{
    font-size: 16pt;
    font-weight: 700;
    color: #f6f5f0;
  }}
  .s8-step-desc {{
    font-size: 11pt;
    font-weight: 300;
    color: #9c9da4;
  }}

  .s8-cta-card {{
    background: linear-gradient(135deg, #ff5a36, #d9381e);
    border-radius: 14pt;
    padding: 22pt 26pt;
    display: flex;
    align-items: center;
    gap: 20pt;
    box-shadow: 0 10pt 25pt rgba(255, 90, 54, 0.25);
  }}
  .s8-cta-icon-box {{
    width: 52pt;
    height: 52pt;
    background: #000000;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .s8-cta-icon-box svg {{
    width: 28pt;
    height: 28pt;
    stroke: #ffffff;
    fill: none;
    stroke-width: 2;
  }}
  .s8-cta-main-text {{
    font-size: 18.5pt;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
  }}
  .s8-cta-sub-text {{
    font-size: 12pt;
    font-weight: 300;
    color: #ffe4dc;
    margin-top: 4pt;
  }}

  .s8-urgency-note {{
    font-size: 12pt;
    color: #9c9da4;
    text-align: center;
    flex-shrink: 0;
  }}
  .s8-urgency-note strong {{
    color: #f6f5f0;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: CAPA -->
<div class="slide">
  <div class="slide-body">
    <div class="s1-top">
      <div class="s1-kicker-left">P R O P O S T A &nbsp; D E &nbsp; P A R C E R I A</div>
      <div class="s1-badge-right">ORÇAMENTO EXCLUSIVO #2026/742</div>
    </div>
    <div class="s1-hero">
      <div class="s1-hero-line">Quem vê, pede.</div>
      <div class="s1-hero-line">Quem acha, vai.</div>
      <div class="s1-hero-line highlight">Quem prova, volta.</div>
    </div>
    <div class="s1-grid" style="grid-template-columns: 1fr 1fr; grid-template-rows: auto auto;">
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">30 fotos profissionais</div>
          <div class="s1-card-desc">Pratos que dão água na boca</div>
        </div>
      </div>
      <div class="s1-card" style="grid-row: span 2;">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        </div>
        <div>
          <div class="s1-card-title">Estratégia Anti-Taxa iFood</div>
          <div class="s1-card-desc" style="line-height:1.4; margin-top:6px;">Uso da plataforma como isca para atrair clientes para o WhatsApp.</div>
        </div>
      </div>
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">Google Meu Negócio</div>
          <div class="s1-card-desc">Apareça quando a fome bater</div>
        </div>
      </div>
    </div>
    <div class="s1-bottom-bar">
      <div>• Proposta reservada por <strong>10 dias corridos</strong></div>
      <div>• No ar em <strong>7 dias</strong>, sem parar sua cozinha</div>
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">01</div>
  </div>
</div>

<!-- SLIDE 2: VISÃO GERAL COM CAIXA OFICIAL IA -->
<div class="slide">
  <div class="slide-body">
    <div class="slide-header">
      <div class="kicker">V I S Ã O &nbsp; G E R A L</div>
      <div class="slide-title">Um ciclo que enche<br>sua casa e seu caixa.</div>
    </div>
    
    <div class="s2-cycle-grid">
      <div class="s2-cycle-card">
        <div class="s2-watermark">1</div>
        <div class="s2-card-icon">
          <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
        </div>
        <div>
          <div class="s2-card-title">Fotos</div>
          <div class="s2-card-desc">O cliente sente o gosto antes de pedir.</div>
        </div>
      </div>
      <div class="s2-arrow">→</div>
      <div class="s2-cycle-card">
        <div class="s2-watermark">2</div>
        <div class="s2-card-icon">
          <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        </div>
        <div>
          <div class="s2-card-title">Google Meu Negócio</div>
          <div class="s2-card-desc">Quem busca “restaurante perto de mim” vê você primeiro.</div>
        </div>
      </div>
      <div class="s2-arrow">→</div>
      <div class="s2-cycle-card">
        <div class="s2-watermark">3</div>
        <div class="s2-card-icon">
          <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        </div>
        <div>
          <div class="s2-card-title">iFood</div>
          <div class="s2-card-desc">O pedido entra e a margem fica com você.</div>
        </div>
      </div>
    </div>

    <!-- Bloco Inferior: Ciclo Recomeça + Caixa Oficial de IA -->
    <div class="s2-bottom-container">
      <div class="s2-restart-card">
        <div class="s2-restart-title">E o ciclo recomeça.</div>
        <div class="s2-restart-desc">O cliente feliz avalia na plaquinha, o ranking sobe e chegam mais clientes.</div>
      </div>
      <div class="s2-ia-box">
        <div class="s2-ia-badge">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          NOVO · VISIBILIDADE EM IA
        </div>
        <div class="s2-ia-title">Camada IA: faça a IA recomendar o cliente.</div>
        <div class="s2-ia-desc">Toda proposta pode incluir visibilidade em IA (ChatGPT, Gemini, busca com IA), apoiada em perfil, avaliações e dados.</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">02</div>
  </div>
</div>

<!-- SLIDE 3: PILAR 1 FOTOS -->
<div class="slide">
  <div class="slide-body">
    <div class="header-with-icon">
      <div class="header-icon-box">
        <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
      </div>
      <div>
        <div class="kicker">P I L A R &nbsp; 1</div>
        <div class="slide-title">Fotos que dão água na boca</div>
        <div class="slide-subtitle">O cliente come com os olhos. Vamos fazer ele pedir.</div>
      </div>
    </div>

    <div class="s3-content-grid">
      <div class="s3-hero-card">
        <div class="s3-giant-num">30</div>
        <div class="s3-giant-label">fotos dos seus<br>pratos reais</div>
      </div>
      <div class="s3-details-col">
        <div class="s3-item-row">
          <div class="s3-item-title">Planejado antes do clique</div>
          <div class="s3-item-desc">Direção criativa e identidade visual do seu restaurante</div>
        </div>
        <div class="s3-item-row">
          <div class="s3-item-title">Um dia. Zero bagunça.</div>
          <div class="s3-item-desc">Seus pratos reais, sem prato extra e sem parar a cozinha</div>
        </div>
        <div class="s3-item-row">
          <div class="s3-item-title">Pronto para postar</div>
          <div class="s3-item-desc">Edição profissional e formato certo para cada canal</div>
        </div>
        <div class="s3-pills-row">
          <div class="s3-pills-label">Prontas para usar em:</div>
          <div class="s3-pill">iFood</div>
          <div class="s3-pill">Google</div>
          <div class="s3-pill">Instagram</div>
          <div class="s3-pill">WhatsApp</div>
        </div>
      </div>
    </div>

    <div class="s3-stats-container">
      <div class="s3-stats-grid">
        <div class="s3-stat-card">
          <div class="s3-stat-num">+28%</div>
          <div class="s3-stat-desc">no desejo de compra com cardápios bem detalhados, com fotos e descrições</div>
        </div>
        <div class="s3-stat-card">
          <div class="s3-stat-num">18%</div>
          <div class="s3-stat-desc">escolhem onde comer pela foto do prato e do ambiente</div>
        </div>
      </div>
      <div class="s3-footnote">Fontes: estudo da Universidade Cornell, citado pelo Sebrae (+28%); pesquisa Reclame Aqui e Abrasel (18%).</div>
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">03</div>
  </div>
</div>

<!-- SLIDE 4: PILAR 2 GOOGLE MEU NEGÓCIO -->
<div class="slide">
  <div class="slide-body">
    <div class="header-with-icon">
      <div class="header-icon-box">
        <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
      </div>
      <div>
        <div class="kicker">P I L A R &nbsp; 2</div>
        <div class="slide-title">Google Meu Negócio</div>
        <div class="slide-subtitle">Quando a fome bater, seu restaurante já está na tela.</div>
      </div>
    </div>

    <div class="two-col-layout">
      <div class="check-list">
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Perfil que converte</div>
            <div class="check-desc">Ficha completa e SEO local para aparecer no topo</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">As buscas certas</div>
            <div class="check-desc">Palavras que o seu cliente realmente digita</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Sempre em movimento</div>
            <div class="check-desc">Postagens semanais mantêm cardápio e loja em dia</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Reputação que atrai</div>
            <div class="check-desc">Respostas humanizadas e relatório mensal</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Pronto para as IAs</div>
            <div class="check-desc">Preparado para ser recomendado pelas IAs</div>
          </div>
        </div>
      </div>

      <div class="right-cards-stack">
        <div class="stat-card-highlight">
          <div class="stat-giant-val">76%</div>
          <div class="stat-text">das pessoas que buscam algo por perto no celular <strong>visitam um negócio em até 1 dia.</strong> Quem aparece primeiro leva o pedido.</div>
          <div class="stat-source">Fonte: Think with Google</div>
        </div>
        <div class="result-card-green">
          <div class="result-tag">↑ RESULTADO ESPERADO</div>
          <div class="result-text">Mais gente na porta, sem pagar por cada cliente novo.</div>
        </div>
      </div>
    </div>

    <div class="bottom-callout-banner">
      <strong>Enquanto sua ficha está parada,</strong> o concorrente está enchendo a mesa que era sua.
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">04</div>
  </div>
</div>

<!-- SLIDE 5: PILAR 3 IFOOD -->
<div class="slide">
  <div class="slide-body">
    <div class="header-with-icon">
      <div class="header-icon-box">
        <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
      </div>
      <div>
        <div class="kicker">P I L A R &nbsp; 3</div>
        <div class="slide-title">Otimização do iFood</div>
        <div class="slide-subtitle">Venda mais. E fique com mais de cada venda.</div>
      </div>
    </div>

    <div class="two-col-layout">
      <div class="check-list">
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Preço à prova de comissão</div>
            <div class="check-desc">Cada prato calculado para sobrar lucro após a taxa</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Combos que aumentam o ticket</div>
            <div class="check-desc">Prato + bebida + sobremesa: o cliente leva mais e você lucra mais</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Cardápio que dá vontade</div>
            <div class="check-desc">Fotos e textos que levam o dedo ao “adicionar”</div>
          </div>
        </div>
        <div class="check-item">
          <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
          <div>
            <div class="check-title">Cliente que volta</div>
            <div class="check-desc">Cupons segmentados e Clube iFood transformam o 1º pedido em hábito</div>
          </div>
        </div>
      </div>

      <div class="right-cards-stack">
        <div class="alert-card-red" style="padding: 16pt 22pt;">
          <div class="alert-text-top" style="font-size: 11.5pt;"><strong>O iFood é a maior vitrine de delivery do Brasil,</strong> mas deixar 20% a 27% de comissão em toda venda mata o seu lucro.</div>
          <div class="alert-text-top" style="font-size: 11.5pt; margin-bottom: 0;">A nossa estratégia usa o iFood apenas como isca para atrair novos clientes. Assim que o cliente faz o primeiro pedido, nós entregamos uma experiência que o faz pedir sempre direto pelo seu WhatsApp, <strong>revertendo todo o lucro da compra para você.</strong></div>
        </div>
        <div class="result-card-green">
          <div class="result-tag">↑ RESULTADO ESPERADO</div>
          <div class="result-text">Conquiste o cliente no iFood, mas lucre através do WhatsApp.</div>
        </div>
      </div>
    </div>

    <div class="bottom-callout-banner">
      <strong>Seu cardápio no iFood é sua vitrine mais lucrativa</strong> quando os combos e preços estão bem calibrados.
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">05</div>
  </div>
</div>

<!-- SLIDE 6: INVESTIMENTO -->
<div class="slide">
  <div class="slide-body">
    <div class="slide-header">
      <div class="kicker">I N V E S T I M E N T O</div>
      <div class="slide-title">Um investimento. Resultado que continua.</div>
      <div class="slide-subtitle">Pague uma vez. As fotos são suas para sempre. Parcelamento disponível.</div>
    </div>

    <div class="s7-grid">
      <div class="s7-items-list">
        <div class="s7-item-row">
          <div>
            <div class="s7-item-info-title">30 fotos profissionais</div>
            <div class="s7-item-info-desc">1 dia de captação no local</div>
          </div>
          <div class="s7-item-price">R$ 500</div>
        </div>
        <div class="s7-item-row">
          <div>
            <div class="s7-item-info-title">Google Meu Negócio</div>
            <div class="s7-item-info-desc">Domínio Local</div>
          </div>
          <div class="s7-item-price">R$ 500</div>
        </div>
        <div class="s7-item-row">
          <div>
            <div class="s7-item-info-title">Otimização do iFood</div>
            <div class="s7-item-info-desc">Máquina de Vendas</div>
          </div>
          <div class="s7-item-price">R$ 800</div>
        </div>

      </div>

      <div class="s7-package-card">
        <div>
          <div class="s7-rec-badge">RECOMENDADO</div>
          <div class="s7-pack-name">Pacote Aceleração Total</div>
          <div class="s7-pack-price">R$ 1.399</div>
          <div class="s7-pack-savings">Você leva R$ 1.800 em serviços · <strong>Economia de R$ 401</strong></div>
        </div>
        <div>
          <div class="s7-pack-terms">PIX à vista ou até 3× de R$ 466,33 no cartão</div>
          <div class="s7-pack-breakeven">Com ticket médio de R$ 60, bastam <strong>24 pedidos a mais no mês</strong> (menos de 1 por dia) para cobrir o investimento em faturamento.</div>
        </div>
      </div>
    </div>

    <div class="s7-guarantees-bar">
      <div class="s7-guarantee-item">
        <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div>Sem mensalidade obrigatória</div>
      </div>
      <div class="s7-guarantee-item">
        <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div>Fotos de uso livre e permanente</div>
      </div>
      <div class="s7-guarantee-item">
        <div class="check-icon"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div>Zero impacto na cozinha</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">06</div>
  </div>
</div>

<!-- SLIDE 7: PRÓXIMO PASSO -->
<div class="slide">
  <div class="slide-body">
    <div class="slide-header">
      <div class="kicker">P R Ó X I M O &nbsp; P A S S O</div>
      <div class="slide-title">Vamos colocar seu restaurante<br>na frente de quem está com fome?</div>
    </div>

    <div class="s8-steps-grid">
      <div class="s8-step-card">
        <div class="s8-step-num">1</div>
        <div>
          <div class="s8-step-title">Você aprova</div>
          <div class="s8-step-desc">PIX à vista ou até 3× no cartão</div>
        </div>
      </div>
      <div class="s8-step-card">
        <div class="s8-step-num">2</div>
        <div>
          <div class="s8-step-title">Agendamos as fotos</div>
          <div class="s8-step-desc">1 dia de captação, sem parar a cozinha</div>
        </div>
      </div>
      <div class="s8-step-card">
        <div class="s8-step-num">3</div>
        <div>
          <div class="s8-step-title">Tudo no ar em 7 dias</div>
          <div class="s8-step-desc">Fotos, Google e Otimização do iFood</div>
        </div>
      </div>
    </div>

    <div class="s8-cta-card">
      <div class="s8-cta-icon-box">
        <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      </div>
      <div>
        <div class="s8-cta-main-text">Responda esta mensagem e a gente agenda o dia das fotos.</div>
        <div class="s8-cta-sub-text">Seu restaurante mais perto de quem já está com fome.</div>
      </div>
    </div>

    <div class="s8-urgency-note">• Proposta reservada por <strong>10 dias corridos</strong>. Depois disso, os valores podem mudar.</div>
  </div>
  <div class="footer">
    <div class="footer-brand">ACELERAÇÃO <span>GASTRONÔMICA</span></div>
    <div class="footer-page">07</div>
  </div>
</div>

</body>
</html>
"""
    return html

def main():
    html_content = generate_proposal_html()
    
    html_path = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\proposta_aceleracao_sem_nfc.html"
    pdf_path = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\Proposta_Aceleracao_Gastronomica_Sem_NFC.pdf"
    preview_dir = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\previews_aceleracao_sem_nfc"
    
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML salvo em: {html_path}")
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_exe = p
            break
            
    if not edge_exe:
        print("Erro: Microsoft Edge não encontrado!")
        return

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    print("Gerando PDF via Microsoft Edge Headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_path):
        print(f"PDF gerado com sucesso: {pdf_path}")
    else:
        print(f"Erro ao gerar PDF: {res.stderr}")
        return

    print("Renderizando previews PNG (150 DPI)...")
    doc = pymupdf.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        p = os.path.join(preview_dir, f"slide_{i+1:02d}.png")
        pix.save(p)
        print(f"Preview salvo: {p}")
    print("Concluído com sucesso!")

if __name__ == "__main__":
    main()

import os
import subprocess
import pymupdf

HTML_DIR = "saida/10_modelos_completos_html"
PDF_DIR = "BigBrain/handoff/10_modelos_completos_seo"
PNG_DIR = "saida/previews_10_modelos_completos"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# DEFINIÇÃO DOS 10 MODELOS COMPLETOS COM DESIGN, TIPOGRAFIA, CORES E LAYOUT DIFERENTES
MODELOS = [
    {
        "id": "01",
        "nome": "Warm Editorial & Classic Michelin",
        "tag": "Modelo 01 · Warm Sand / Terracota / Serif Header",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">',
        "font_body": "'Plus Jakarta Sans', sans-serif",
        "font_h": "'Playfair Display', serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg_page": "#FAFAF5",
        "card_bg": "#FFFFFF",
        "hero_bg": "#1F2430",
        "hero_text": "#FFFFFF",
        "accent": "#F26A21",
        "border": "#E5E1DA",
        "text_dark": "#1F2430",
        "text_muted": "#6B7280",
        "card_shadow": "0 1px 3px rgba(0,0,0,0.04)",
        "hero_border": "none",
        "hero_radius": "6px",
        "badge_shape": "rounded"
    },
    {
        "id": "02",
        "nome": "Deep Dark Executive (Obsidian & Sky Blue)",
        "tag": "Modelo 02 · Dark Mode / High Contrast / Neon Accents",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">',
        "font_body": "'Plus Jakarta Sans', sans-serif",
        "font_h": "'Plus Jakarta Sans', sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg_page": "#0D111A",
        "card_bg": "#141B2D",
        "hero_bg": "#1B243B",
        "hero_text": "#FFFFFF",
        "accent": "#38BDF8",
        "border": "#263352",
        "text_dark": "#F8FAFC",
        "text_muted": "#94A3B8",
        "card_shadow": "none",
        "hero_border": "1px solid #38BDF8",
        "hero_radius": "8px",
        "badge_shape": "pill"
    },
    {
        "id": "03",
        "nome": "McKinsey Pure Clean White (Corporate Standard)",
        "tag": "Modelo 03 · White Minimal / Navy Accent / High Trust",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">',
        "font_body": "'Inter', sans-serif",
        "font_h": "'Inter', sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg_page": "#FFFFFF",
        "card_bg": "#F8FAFC",
        "hero_bg": "#0F172A",
        "hero_text": "#FFFFFF",
        "accent": "#0284C7",
        "border": "#E2E8F0",
        "text_dark": "#0F172A",
        "text_muted": "#64748B",
        "card_shadow": "0 1px 2px rgba(0,0,0,0.05)",
        "hero_border": "none",
        "hero_radius": "4px",
        "badge_shape": "square"
    },
    {
        "id": "04",
        "nome": "Linear Dev Dark (Void Black & Indigo Precision)",
        "tag": "Modelo 04 · Linear UI / Micro-borders / Tech Glow",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@500;700&display=swap" rel="stylesheet">',
        "font_body": "'Geist', sans-serif",
        "font_h": "'Geist', sans-serif",
        "font_mono": "'Geist Mono', monospace",
        "bg_page": "#08090A",
        "card_bg": "#121316",
        "hero_bg": "linear-gradient(135deg, #18191E 0%, #0F1012 100%)",
        "hero_text": "#EDEDED",
        "accent": "#818CF8",
        "border": "#222429",
        "text_dark": "#EDEDED",
        "text_muted": "#8A8F98",
        "card_shadow": "none",
        "hero_border": "1px solid #31353D",
        "hero_radius": "10px",
        "badge_shape": "pill"
    },
    {
        "id": "05",
        "nome": "Google Native Material (Official Local SERP)",
        "tag": "Modelo 05 · Material 3 / Google Blue / Card Layout",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&family=Roboto+Mono:wght@500;700&display=swap" rel="stylesheet">',
        "font_body": "'Roboto', sans-serif",
        "font_h": "'Roboto', sans-serif",
        "font_mono": "'Roboto Mono', monospace",
        "bg_page": "#F8F9FA",
        "card_bg": "#FFFFFF",
        "hero_bg": "#1A73E8",
        "hero_text": "#FFFFFF",
        "accent": "#1A73E8",
        "border": "#DADCE0",
        "text_dark": "#202124",
        "text_muted": "#5F6368",
        "card_shadow": "0 1px 3px rgba(60,64,67,0.15)",
        "hero_border": "none",
        "hero_radius": "8px",
        "badge_shape": "rounded"
    },
    {
        "id": "06",
        "nome": "Swiss Brutalist (Stark Monochrome & Red Accent)",
        "tag": "Modelo 06 · Bauhaus / Heavy Lines / Asymmetric",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Epilogue:wght@400;500;600;700;800&family=Space+Mono:wght@700&display=swap" rel="stylesheet">',
        "font_body": "'Epilogue', sans-serif",
        "font_h": "'Syne', sans-serif",
        "font_mono": "'Space Mono', monospace",
        "bg_page": "#F4F4F0",
        "card_bg": "#FFFFFF",
        "hero_bg": "#1A1A1A",
        "hero_text": "#FFFFFF",
        "accent": "#D9381E",
        "border": "#1A1A1A",
        "text_dark": "#1A1A1A",
        "text_muted": "#555555",
        "card_shadow": "none",
        "hero_border": "2px solid #1A1A1A",
        "hero_radius": "0px",
        "badge_shape": "square"
    },
    {
        "id": "07",
        "nome": "Emerald Local Growth (Sustainable High ROI)",
        "tag": "Modelo 07 · Deep Forest / Emerald Accent / Organic Growth",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@500&display=swap" rel="stylesheet">',
        "font_body": "'DM Sans', sans-serif",
        "font_h": "'DM Sans', sans-serif",
        "font_mono": "'DM Mono', monospace",
        "bg_page": "#061A14",
        "card_bg": "#0B261E",
        "hero_bg": "#10382D",
        "hero_text": "#ECFDF5",
        "accent": "#10B981",
        "border": "#1A4F40",
        "text_dark": "#ECFDF5",
        "text_muted": "#6EE7B7",
        "card_shadow": "none",
        "hero_border": "1px solid #10B981",
        "hero_radius": "8px",
        "badge_shape": "pill"
    },
    {
        "id": "08",
        "nome": "Boutique Sunset Island (Floripa Premium)",
        "tag": "Modelo 08 · Midnight Violet / Sunset Rose / Coastal Luxury",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Satoshi:wght@400;500;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">',
        "font_body": "'Satoshi', sans-serif",
        "font_h": "'Cabinet Grotesk', sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg_page": "#0F0C1B",
        "card_bg": "#181429",
        "hero_bg": "#211C38",
        "hero_text": "#FAF5FF",
        "accent": "#F43F5E",
        "border": "#372F5E",
        "text_dark": "#FAF5FF",
        "text_muted": "#C084FC",
        "card_shadow": "none",
        "hero_border": "1px solid #F43F5E",
        "hero_radius": "10px",
        "badge_shape": "rounded"
    },
    {
        "id": "09",
        "nome": "Stripe Fintech Slate (Nordic Blue & Data Dense)",
        "tag": "Modelo 09 · Slate Navy / Sky Blue / High Density",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@500;700&display=swap" rel="stylesheet">',
        "font_body": "'Plus Jakarta Sans', sans-serif",
        "font_h": "'Plus Jakarta Sans', sans-serif",
        "font_mono": "'Fira Code', monospace",
        "bg_page": "#0A101D",
        "card_bg": "#0F172A",
        "hero_bg": "#1E293B",
        "hero_text": "#F1F5F9",
        "accent": "#6366F1",
        "border": "#334155",
        "text_dark": "#F1F5F9",
        "text_muted": "#94A3B8",
        "card_shadow": "none",
        "hero_border": "1px solid #6366F1",
        "hero_radius": "6px",
        "badge_shape": "square"
    },
    {
        "id": "10",
        "nome": "Cyber Radar Local (High Contrast Neon Grid)",
        "tag": "Modelo 10 · Cyber Black / Cyan Neon / Radar Aesthetic",
        "font_link": '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">',
        "font_body": "'Space Grotesk', sans-serif",
        "font_h": "'Space Grotesk', sans-serif",
        "font_mono": "'Space Mono', monospace",
        "bg_page": "#05070A",
        "card_bg": "#0C1017",
        "hero_bg": "#111823",
        "hero_text": "#FFFFFF",
        "accent": "#00F0FF",
        "border": "#1B2A3D",
        "text_dark": "#FFFFFF",
        "text_muted": "#7B8FA6",
        "card_shadow": "none",
        "hero_border": "1px solid #00F0FF",
        "hero_radius": "4px",
        "badge_shape": "pill"
    }
]

def render_html_completo(m):
    # Gera o relatório completo de 3 páginas exatamente com TODAS as informações de SEO Local da referência
    top_line = f'<div style="height: 4px; background: {m["accent"]}; position: absolute; top: 0; left: 0; right: 0;"></div>'

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{m['nome']} — Paixão Restaurante</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{m['font_link']}
<style>
  :root {{
    --bg-page: {m['bg_page']};
    --card-bg: {m['card_bg']};
    --hero-bg: {m['hero_bg']};
    --hero-text: {m['hero_text']};
    --accent: {m['accent']};
    --border: {m['border']};
    --text-dark: {m['text_dark']};
    --text-muted: {m['text_muted']};
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  @page {{
    size: 210mm 297mm;
    margin: 0;
  }}

  body {{
    background-color: var(--bg-page);
    font-family: {m['font_body']};
    color: var(--text-dark);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page-container {{
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    background: var(--bg-page);
    padding: 16mm 16mm 12mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    page-break-inside: avoid;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
  }}

  h1, h2, h3, .heading {{ font-family: {m['font_h']}; }}
  .mono {{ font-family: {m['font_mono']}; }}

  /* Header */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}
  .tag-eyebrow {{
    font-size: 8px;
    font-weight: 800;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}
  .doc-title {{
    font-size: 19px;
    font-weight: 800;
    color: var(--text-dark);
    margin-top: 2px;
  }}
  .doc-sub {{
    font-size: 9px;
    color: var(--text-muted);
  }}
  .header-meta {{
    text-align: right;
    font-size: 8px;
    color: var(--text-muted);
  }}
  .badge-p {{
    font-size: 8.5px;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 2px;
  }}

  /* Section Header */
  .sec-header {{
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 9px 0 5px 0;
  }}
  .sec-num {{
    background: var(--accent);
    color: #FFFFFF;
    font-size: 8px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: {('20px' if m['badge_shape']=='pill' else '3px' if m['badge_shape']=='rounded' else '0px')};
  }}
  .sec-title {{
    font-size: 11px;
    font-weight: 700;
    color: var(--text-dark);
  }}
  .sec-sub {{
    font-size: 8.5px;
    color: var(--text-muted);
  }}

  /* Hero Box */
  .hero-box {{
    background: var(--hero-bg);
    color: var(--hero-text);
    border: {m['hero_border']};
    border-radius: {m['hero_radius']};
    padding: 10px 14px;
    margin-top: 8px;
  }}
  .hero-eyebrow {{
    font-size: 7.5px;
    font-weight: 800;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .hero-h {{
    font-size: 13px;
    font-weight: 800;
    margin: 2px 0;
  }}
  .hero-p {{
    font-size: 8.5px;
    color: rgba(255,255,255,0.8);
    line-height: 1.35;
  }}

  /* Cards */
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 7px 10px;
    box-shadow: {m['card_shadow']};
  }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}

  /* NAP Table */
  .nap-tbl {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  .nap-tbl td {{ padding: 3.5px 5px; border-bottom: 1px solid var(--border); }}
  .nap-l {{ color: var(--text-muted); font-weight: 600; width: 105px; }}
  .nap-v {{ color: var(--text-dark); font-weight: 600; }}

  /* KPIs */
  .kpi-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 8px;
    box-shadow: {m['card_shadow']};
  }}
  .kpi-lbl {{ font-size: 7px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }}
  .kpi-val {{ font-size: 15px; font-weight: 800; color: var(--text-dark); margin: 1px 0; }}
  .kpi-sub {{ font-size: 7px; color: var(--text-muted); }}

  /* Pilares */
  .p-row {{ display: flex; align-items: center; font-size: 8px; margin-bottom: 3.5px; }}
  .p-name {{ width: 120px; color: var(--text-muted); font-weight: 600; }}
  .p-bar {{ flex: 1; height: 5px; background: rgba(128,128,128,0.15); border-radius: 3px; margin: 0 8px; overflow: hidden; }}
  .p-fill {{ height: 100%; background: var(--accent); border-radius: 3px; }}
  .p-val {{ width: 30px; text-align: right; font-weight: 700; color: var(--text-dark); }}

  /* Competitors */
  .c-tbl {{ width: 100%; border-collapse: collapse; font-size: 8px; }}
  .c-tbl th {{ background: rgba(128,128,128,0.08); color: var(--text-muted); font-size: 7px; font-weight: 700; text-transform: uppercase; padding: 4px 6px; text-align: left; border-bottom: 1px solid var(--border); }}
  .c-tbl td {{ padding: 4px 6px; border-bottom: 1px solid var(--border); color: var(--text-muted); }}
  .c-tbl tr.target {{ background: rgba(242,106,33,0.1); font-weight: 700; }}
  .c-tbl tr.target td {{ color: var(--text-dark); border-top: 1px solid var(--accent); border-bottom: 1px solid var(--accent); }}

  /* Checklist Item */
  .ck-item {{ display: flex; align-items: flex-start; gap: 6px; padding: 3.5px 0; border-bottom: 1px solid var(--border); font-size: 8px; }}
  .ck-ico {{ width: 11px; height: 11px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 6.5px; font-weight: 800; flex-shrink: 0; margin-top: 1px; background: var(--accent); color: #FFF; }}
  .ck-txt strong {{ color: var(--text-dark); font-weight: 700; font-size: 8px; }}
  .ck-txt p {{ color: var(--text-muted); font-size: 7.5px; margin-top: 0.5px; }}

  /* Footer */
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 5px;
    font-size: 7.5px;
    color: var(--text-muted);
  }}
</style>
</head>
<body>

<!-- PÁGINA 1: DADOS CADASTRAIS & SERP AUDIT -->
<div class="page-container">
  {top_line}
  <div>
    <div class="header">
      <div>
        <div class="tag-eyebrow">AUDITORIA DE PRESENÇA DIGITAL · GOOGLE MAPS & LOCAL SEO</div>
        <div class="doc-title">Paixão Restaurante & Pizzaria</div>
        <div class="doc-sub">Diagnóstico estratégico de posicionamento e captação de clientes locais</div>
      </div>
      <div class="header-meta">
        <div class="badge-p mono">Página 01 / 03</div>
        <div>Florianópolis - SC · Ingleses</div>
      </div>
    </div>

    <!-- Hero -->
    <div class="hero-box">
      <div class="hero-eyebrow">O QUE A AUDITORIA MOSTRA</div>
      <div class="hero-h">Líder Absoluto em Volume no Norte da Ilha (1º no Google Maps)</div>
      <div class="hero-p">Você é o 1º no Google Maps da região com 5.385 avaliações e nota 4,5★. O volume é massivo, mas para blindar o topo contra concorrentes de Santo Antônio e Canasvieiras, a prioridade é acelerar avaliações 5 estrelas e otimizar a conversão mobile.</div>
    </div>

    <!-- 01 Dados Cadastrais -->
    <div class="sec-header">
      <span class="sec-num mono">01</span>
      <span class="sec-title">Dados cadastrais</span>
      <span class="sec-sub">· Perfil Google Business</span>
    </div>
    <div class="card" style="padding: 4px 8px;">
      <table class="nap-tbl">
        <tr>
          <td class="nap-l">NOME OFICIAL:</td>
          <td class="nap-v">Paixão Restaurante & Pizzaria <span style="color:var(--accent); font-size:7.5px;">✓ Perfil Verificado</span></td>
          <td class="nap-l">CATEGORIA:</td>
          <td class="nap-v">Frutos do Mar / Pizzaria</td>
        </tr>
        <tr>
          <td class="nap-l">ENDEREÇO:</td>
          <td class="nap-v" colspan="3">Estrada Dom João Becker, 329 - Praia dos Ingleses, Florianópolis - SC, 88058-600</td>
        </tr>
        <tr>
          <td class="nap-l">TELEFONE:</td>
          <td class="nap-v mono">(48) 3269-1355</td>
          <td class="nap-l">GPS:</td>
          <td class="nap-v mono">-27.43611, -48.39098 (Norte da Ilha)</td>
        </tr>
      </table>
    </div>

    <!-- 02 Indicadores-chave -->
    <div class="sec-header">
      <span class="sec-num mono">02</span>
      <span class="sec-title">Indicadores-chave</span>
      <span class="sec-sub">· Métricas de relevância local</span>
    </div>
    <div class="grid-4">
      <div class="kpi-card">
        <div class="kpi-lbl">SCORE DE PRESENÇA</div>
        <div class="kpi-val mono" style="color:var(--accent);">90<small style="font-size:9px; color:var(--text-muted);">/100</small></div>
        <div class="kpi-sub">Líder Regional Isolado</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">TOTAL DE AVALIAÇÕES</div>
        <div class="kpi-val mono">5.385</div>
        <div class="kpi-sub">Top 1 da Microrregião</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">NOTA MÉDIA</div>
        <div class="kpi-val mono">4,5 <small style="font-size:10px;">★</small></div>
        <div class="kpi-sub">Satisfação Comprovada</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">POTENCIAL DE GANHO</div>
        <div class="kpi-val mono" style="color:var(--accent);">+35%</div>
        <div class="kpi-sub">Tráfego Incremental Mobile</div>
      </div>
    </div>

    <!-- 03 Pilares Locais -->
    <div class="sec-header">
      <span class="sec-num mono">03</span>
      <span class="sec-title">Pilares locais</span>
      <span class="sec-sub">· Pontuação atual vs. meta de 80% (Padrão Ouro)</span>
    </div>
    <div class="card">
      <div class="p-row">
        <span class="p-name">Dados NAP & GPS</span>
        <div class="p-bar"><div class="p-fill" style="width: 95%;"></div></div>
        <span class="p-val mono">95%</span>
      </div>
      <div class="p-row">
        <span class="p-name">Volume de avaliações</span>
        <div class="p-bar"><div class="p-fill" style="width: 98%;"></div></div>
        <span class="p-val mono">98%</span>
      </div>
      <div class="p-row">
        <span class="p-name">Vitrine & Fotos</span>
        <div class="p-bar"><div class="p-fill" style="width: 85%;"></div></div>
        <span class="p-val mono">85%</span>
      </div>
      <div class="p-row">
        <span class="p-name">Recência de novos reviews</span>
        <div class="p-bar"><div class="p-fill" style="width: 72%;"></div></div>
        <span class="p-val mono">72%</span>
      </div>
      <div class="p-row">
        <span class="p-name">Taxa de resposta da gestão</span>
        <div class="p-bar"><div class="p-fill" style="width: 40%;"></div></div>
        <span class="p-val mono">40%</span>
      </div>
      <div class="p-row" style="margin-bottom:0;">
        <span class="p-name">Cardápio digital mobile</span>
        <div class="p-bar"><div class="p-fill" style="width: 78%;"></div></div>
        <span class="p-val mono">78%</span>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome']}</span>
    <span class="mono">Página 01 / 03</span>
  </div>
</div>

<!-- PÁGINA 2: BENCHMARKING & ESTRATÉGIA -->
<div class="page-container">
  {top_line}
  <div>
    <div class="header">
      <div>
        <div class="tag-eyebrow">AUDITORIA DE PRESENÇA DIGITAL · BENCHMARKING & ESTRATÉGIA</div>
        <div class="doc-title">Paixão Restaurante & Pizzaria</div>
        <div class="doc-sub">Análise competitiva do raio local e plano de aceleração</div>
      </div>
      <div class="header-meta">
        <div class="badge-p mono">Página 02 / 03</div>
        <div>Florianópolis - SC · Raio 2.5 km</div>
      </div>
    </div>

    <!-- 04 Ranking Competitivo -->
    <div class="sec-header">
      <span class="sec-num mono">04</span>
      <span class="sec-title">Ranking competitivo</span>
      <span class="sec-sub">· Google Maps, Norte da Ilha</span>
    </div>
    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="c-tbl">
        <thead>
          <tr>
            <th style="width: 30px;">POS.</th>
            <th>ESTABELECIMENTO</th>
            <th>NICHO / CATEGORIA</th>
            <th>NOTA</th>
            <th>AVALIAÇÕES</th>
            <th>CARDÁPIO · WHATSAPP</th>
          </tr>
        </thead>
        <tbody>
          <tr class="target">
            <td><strong>1º</strong></td>
            <td>Paixão Restaurante & Pizzaria (Alvo Auditado)</td>
            <td>Frutos do Mar & Pizza</td>
            <td><strong>4,5</strong></td>
            <td><strong>5.385</strong></td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>2º</td>
            <td>Don Zarichta Pizzaria Artesanal</td>
            <td>Pizzaria & Italiana</td>
            <td>4,9</td>
            <td>5.230</td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>3º</td>
            <td>Costillas Grill - Costelaria</td>
            <td>Carnes & Parrilla</td>
            <td>4,3</td>
            <td>4.791</td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>4º</td>
            <td>Freguesia Bar</td>
            <td>Frutos do Mar & Bar</td>
            <td>4,4</td>
            <td>4.377</td>
            <td>Não · Sim</td>
          </tr>
          <tr>
            <td>5º</td>
            <td>Villa do Porto Gastronomia</td>
            <td>Frutos do Mar & Bar</td>
            <td>4,6</td>
            <td>3.983</td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>6º</td>
            <td>Antonio's Restaurante</td>
            <td>Frutos do Mar</td>
            <td>4,7</td>
            <td>3.918</td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>7º</td>
            <td>Camarão Chef Seghetto</td>
            <td>Frutos do Mar</td>
            <td>4,6</td>
            <td>3.857</td>
            <td>Sim · Sim</td>
          </tr>
          <tr>
            <td>8º</td>
            <td>Pizzaria Happy</td>
            <td>Pizzaria Delivery</td>
            <td>4,6</td>
            <td>3.771</td>
            <td>Sim · Sim</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 05 Plano de Ação -->
    <div class="sec-header" style="margin-top:10px;">
      <span class="sec-num mono">05</span>
      <span class="sec-title">Plano de ação</span>
      <span class="sec-sub">· 3 pilares para consolidar a liderança</span>
    </div>
    <div class="grid-3">
      <div class="card" style="border-top: 2.5px solid var(--accent);">
        <div style="font-size:7px; font-weight:800; color:var(--accent); text-transform:uppercase;">01 · IMPACTO IMEDIATO</div>
        <div style="font-size:9.5px; font-weight:700; color:var(--text-dark); margin: 2px 0;">Cardápio mobile próprio</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Página web mobile com fotos profissionais dos pratos e valores, indexada com alta velocidade no Google.</p>
        <div style="margin-top: 4px; font-size:7px; color:var(--accent); font-weight:700;">Prazo: 7 a 10 dias · Meta: zero desistência</div>
      </div>
      <div class="card" style="border-top: 2.5px solid var(--accent);">
        <div style="font-size:7px; font-weight:800; color:var(--accent); text-transform:uppercase;">02 · ACELERAÇÃO DE REVIEWS</div>
        <div style="font-size:9.5px; font-weight:700; color:var(--text-dark); margin: 2px 0;">Motor de avaliações 5 estrelas</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Displays inteligentes com NFC e QR Code no caixa e nas mesas para coletar de 60 a 90 novas avaliações por mês.</p>
        <div style="margin-top: 4px; font-size:7px; color:var(--accent); font-weight:700;">Prazo: imediato · Meta: +500 reviews/ano</div>
      </div>
      <div class="card" style="border-top: 2.5px solid var(--accent);">
        <div style="font-size:7px; font-weight:800; color:var(--accent); text-transform:uppercase;">03 · SEO & REPUTAÇÃO</div>
        <div style="font-size:9.5px; font-weight:700; color:var(--text-dark); margin: 2px 0;">Resposta ágil a feedbacks</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Rotina semanal para responder a totalidade dos comentários com termos como 'frutos do mar' e 'pizza ingleses'.</p>
        <div style="margin-top: 4px; font-size:7px; color:var(--accent); font-weight:700;">Prazo: contínuo · Meta: nota 4,7★</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome']}</span>
    <span class="mono">Página 02 / 03</span>
  </div>
</div>

<!-- PÁGINA 3: AUDITORIA PONTO A PONTO -->
<div class="page-container">
  {top_line}
  <div>
    <div class="header">
      <div>
        <div class="tag-eyebrow">AUDITORIA DE PRESENÇA DIGITAL · AUDITORIA PONTO A PONTO</div>
        <div class="doc-title">Paixão Restaurante & Pizzaria</div>
        <div class="doc-sub">Resumo executivo, checklist completo e próximos passos</div>
      </div>
      <div class="header-meta">
        <div class="badge-p mono">Página 03 / 03</div>
        <div>Auditoria Técnica Final</div>
      </div>
    </div>

    <!-- 06 Resumo de Status -->
    <div class="sec-header">
      <span class="sec-num mono">06</span>
      <span class="sec-title">Resumo de status</span>
      <span class="sec-sub">· 10 itens auditados</span>
    </div>
    <div class="grid-3">
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 15px; font-weight:800; color:var(--accent);">7/10</div>
        <div>
          <div style="font-size: 7.5px; font-weight:700; color:var(--accent);">CONFORME</div>
          <div style="font-size: 6.5px; color:var(--text-muted);">Cadastro e itens básicos validados</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 15px; font-weight:800; color:var(--accent);">2/10</div>
        <div>
          <div style="font-size: 7.5px; font-weight:700; color:var(--accent);">ATENÇÃO</div>
          <div style="font-size: 6.5px; color:var(--text-muted);">Oportunidades de refinamento</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 15px; font-weight:800; color:var(--accent);">1/10</div>
        <div>
          <div style="font-size: 7.5px; font-weight:700; color:var(--accent);">CRÍTICO</div>
          <div style="font-size: 6.5px; color:var(--text-muted);">Gargalos de conversão direta</div>
        </div>
      </div>
    </div>

    <!-- 07 Checklist Detalhado -->
    <div class="sec-header" style="margin-top:8px;">
      <span class="sec-num mono">07</span>
      <span class="sec-title">Checklist detalhado</span>
      <span class="sec-sub">· Item a item</span>
    </div>
    <div class="card" style="padding: 2px 8px;">
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>01. Nome comercial (NAP):</strong> <p>Nome limpo, alinhado com a fachada, sem palavras-chave indevidas.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>02. Endereço e marcador GPS:</strong> <p>Pino geográfico posicionado corretamente na Praia dos Ingleses.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>03. Telefone com DDD local:</strong> <p>Linha fixa (48) 3269-1355 com discagem direta funcional.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>04. Horários de atendimento:</strong> <p>Horários sincronizados e atualizados para almoço e jantar.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>05. Fotos e galeria:</strong> <p>Boas fotos mostrando pratos de frutos do mar, pizzas e ambiente do salão.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>06. Volume de avaliações (FATOR Nº 1):</strong> <p>5.385 avaliações, consolidando a maior autoridade do Norte da Ilha.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico" style="background:#F59E0B;">!</div>
        <div class="ck-txt"><strong>07. Taxa de resposta:</strong> <p>Volume expressivo de opiniões sem resposta; perde-se engajamento semântico no Google.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico" style="background:#F59E0B;">!</div>
        <div class="ck-txt"><strong>08. Recência das avaliações:</strong> <p>Fluxo intermitente; o algoritmo favorece perfis com novas notas a cada semana.</p></div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>09. Website / cardápio digital:</strong> <p>Página cadastrada, necessitando de refinamento mobile para carregamento instantâneo.</p></div>
      </div>
      <div class="ck-item" style="border-bottom:none;">
        <div class="ck-ico">✓</div>
        <div class="ck-txt"><strong>10. Botão de WhatsApp direto:</strong> <p>Canal de contato ativo para reservas e atendimento ao turista.</p></div>
      </div>
    </div>

    <!-- CTA Final -->
    <div class="card" style="margin-top: 6px; border: 1.5px solid var(--accent); padding: 7px 10px;">
      <div style="font-size: 7px; font-weight:800; color:var(--accent); text-transform:uppercase;">PRÓXIMO PASSO RECOMENDADO</div>
      <div style="font-size: 8.5px; font-weight:700; color:var(--text-dark); margin-top:1px;">Implantar o cardápio mobile próprio e as placas inteligentes NFC/QR Code no restaurante para acelerar a captação de avaliações e blindar o 1º lugar no ranking local.</div>
      <div style="font-size: 7.5px; color:var(--text-muted); margin-top:2px;">Fale com a AH3 para ativar a implementação: (48) 99908-8162 · contato@ah3.com.br</div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome']}</span>
    <span class="mono">Página 03 / 03</span>
  </div>
</div>

</body>
</html>
"""
    return html

def main():
    for m in MODELOS:
        m_id = m["id"]
        slug = f"modelo_{m_id}_{m['nome'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace('&', 'e')}"
        html_file = f"{HTML_DIR}/{slug}.html"
        pdf_file = f"{PDF_DIR}/Modelo_{m_id}.pdf"
        png_p1 = f"{PNG_DIR}/Modelo_{m_id}_p1.png"
        png_p2 = f"{PNG_DIR}/Modelo_{m_id}_p2.png"
        png_p3 = f"{PNG_DIR}/Modelo_{m_id}_p3.png"

        # 1. Escrever HTML
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(render_html_completo(m))

        # 2. Compilar PDF via Edge Headless
        cmd = f'"{EDGE_BIN}" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw --print-to-pdf="{os.path.abspath(pdf_file)}" "{os.path.abspath(html_file)}"'
        subprocess.run(cmd, shell=True, check=True)

        # 3. Converter as 3 páginas em PNG
        doc = pymupdf.open(pdf_file)
        doc[0].get_pixmap(dpi=150).save(png_p1)
        doc[1].get_pixmap(dpi=150).save(png_p2)
        doc[2].get_pixmap(dpi=150).save(png_p3)

        print(f"[OK] Modelo {m_id} gerado com sucesso (3 Páginas): {m['nome']}")

if __name__ == "__main__":
    main()

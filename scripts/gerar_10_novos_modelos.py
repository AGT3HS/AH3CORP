import os
import subprocess
import pymupdf

# Diretórios de saída
HTML_DIR = "saida/modelos_10_html"
PDF_DIR = "BigBrain/handoff/catalogo_10_modelos_novos"
PNG_DIR = "saida/previews_10_modelos"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 10 DEFINIÇÕES COMPLETAS DE MODELOS (DESIGN, TIPOGRAFIA, CORES E LAYOUT ESTRUTURAL DIFERENTES)
MODELOS = [
    {
        "id": "01",
        "nome_estilo": "Semrush & BrightLocal SEO Authority (Dark Data Grid)",
        "tag": "SaaS / SEO Tool Diagnostic",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">',
        "font_family": "'Inter', sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg": "#0B0E14",
        "surface": "#121722",
        "card": "#182030",
        "border": "#222D42",
        "primary": "#38BDF8",
        "accent": "#F97316",
        "text": "#F8FAFC",
        "text_muted": "#94A3B8",
        "layout_type": "grid_bento",
        "desc": "Estrutura inspirada nas ferramentas globais de SEO (Semrush/Ahrefs) com blocos analíticos modulares e grid de densidade máxima."
    },
    {
        "id": "02",
        "nome_estilo": "McKinsey & Boston Consulting Editorial (Executive White)",
        "tag": "White Clean Corporate / High Trust",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">',
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "font_heading": "'Playfair Display', serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg": "#FFFFFF",
        "surface": "#F8FAFC",
        "card": "#FFFFFF",
        "border": "#E2E8F0",
        "primary": "#0F172A",
        "accent": "#C2410C",
        "text": "#0F172A",
        "text_muted": "#64748B",
        "layout_type": "editorial_clean",
        "desc": "Design corporativo impresso de alto padrão para consultorias executivas. Fundo branco impecável, tipografia serifada nos títulos e tabelas de alta legibilidade."
    },
    {
        "id": "03",
        "nome_estilo": "Linear Dark Precision (Silicon Valley Dev Standard)",
        "tag": "Ultra-Minimalist Dark / Violet Glow",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@500;700&display=swap" rel="stylesheet">',
        "font_family": "'Geist', sans-serif",
        "font_mono": "'Geist Mono', monospace",
        "bg": "#08090A",
        "surface": "#0F1012",
        "card": "#141518",
        "border": "#222429",
        "primary": "#818CF8",
        "accent": "#A855F7",
        "text": "#EDEDED",
        "text_muted": "#8A8F98",
        "layout_type": "linear_precision",
        "desc": "Layout de precisão milimétrica no estilo Linear.app, com micro-bordas sutis, cantos elegantes e indicadores verticais finos."
    },
    {
        "id": "04",
        "nome_estilo": "Gastronomy & Michelin Guide (Tuscan Warm Minimalist)",
        "tag": "Hospitality & Foodservice Focused",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,600;0,6..72,700;1,6..72,400&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">',
        "font_family": "'Outfit', sans-serif",
        "font_heading": "'Newsreader', serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg": "#FAF7F2",
        "surface": "#F2EBE0",
        "card": "#FFFFFF",
        "border": "#E5D9C8",
        "primary": "#854D0E",
        "accent": "#B45309",
        "text": "#292524",
        "text_muted": "#78716C",
        "layout_type": "hospitality_editorial",
        "desc": "Layout desenhado exclusivamente para o nicho de restaurantes e alta gastronomia, com tons terracota quentes, estilo de carta de vinhos e selos editoriais."
    },
    {
        "id": "05",
        "nome_estilo": "Google Maps Local Pack Intelligence (Official SERP)",
        "tag": "Google Native UI Diagnostic",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Product+Sans:wght@400;700&family=Roboto:wght@400;500;700;900&family=Roboto+Mono:wght@500;700&display=swap" rel="stylesheet">',
        "font_family": "'Roboto', -apple-system, sans-serif",
        "font_mono": "'Roboto Mono', monospace",
        "bg": "#FFFFFF",
        "surface": "#F8F9FA",
        "card": "#FFFFFF",
        "border": "#DADCE0",
        "primary": "#1A73E8",
        "accent": "#EA4335",
        "text": "#202124",
        "text_muted": "#5F6368",
        "layout_type": "google_serp_native",
        "desc": "Layout que reproduz visualmente os componentes do Google Maps / Search Console, gerando reconhecimento imediato por parte do dono do restaurante."
    },
    {
        "id": "06",
        "nome_estilo": "Cyberpunk Local Radar (Neon Grid Audit)",
        "tag": "High-Contrast Cyber Diagnostic",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">',
        "font_family": "'Space Grotesk', sans-serif",
        "font_mono": "'Space Mono', monospace",
        "bg": "#05070A",
        "surface": "#0C1017",
        "card": "#111823",
        "border": "#00F0FF",
        "primary": "#00F0FF",
        "accent": "#FF0055",
        "text": "#FFFFFF",
        "text_muted": "#7B8FA6",
        "layout_type": "cyber_radar",
        "desc": "Layout de impacto visual extremo com linhas geométricas neon, tipografia monoespacial marcante e estética de radar de tráfego."
    },
    {
        "id": "07",
        "nome_estilo": "Stripe Atlas & Financial Ledger (Nordic Navy Slate)",
        "tag": "Fintech / High-Conversion Precision",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@500;700&display=swap" rel="stylesheet">',
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "font_mono": "'Fira Code', monospace",
        "bg": "#0A101D",
        "surface": "#0F172A",
        "card": "#1E293B",
        "border": "#334155",
        "primary": "#38BDF8",
        "accent": "#6366F1",
        "text": "#F1F5F9",
        "text_muted": "#94A3B8",
        "layout_type": "fintech_navy",
        "desc": "Estilo corporativo escandinavo inspirado na Stripe e Vercel, com cards contrastantes em azul marinho profundo e tipografia densa."
    },
    {
        "id": "08",
        "nome_estilo": "Swiss Typographic & Bauhaus Minimal (Stark Mono)",
        "tag": "International Typographic Style",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Epilogue:wght@400;500;600;700;800&family=Space+Mono:wght@700&display=swap" rel="stylesheet">',
        "font_family": "'Epilogue', sans-serif",
        "font_heading": "'Syne', sans-serif",
        "font_mono": "'Space Mono', monospace",
        "bg": "#F4F4F0",
        "surface": "#EAEAE4",
        "card": "#FFFFFF",
        "border": "#1A1A1A",
        "primary": "#1A1A1A",
        "accent": "#D9381E",
        "text": "#1A1A1A",
        "text_muted": "#555555",
        "layout_type": "swiss_bauhaus",
        "desc": "Design suíço brutalista refinado: bordas pretas sólidas de 1.5px a 2px, títulos monumentais, números gigantes e forte assimetria estruturada."
    },
    {
        "id": "09",
        "nome_estilo": "Emerald Local Growth (Organic Sustainable Metric)",
        "tag": "Performance & High ROI Green",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@500&display=swap" rel="stylesheet">',
        "font_family": "'DM Sans', sans-serif",
        "font_mono": "'DM Mono', monospace",
        "bg": "#061A14",
        "surface": "#0B261E",
        "card": "#10382D",
        "border": "#1A4F40",
        "primary": "#10B981",
        "accent": "#34D399",
        "text": "#ECFDF5",
        "text_muted": "#6EE7B7",
        "layout_type": "emerald_growth",
        "desc": "Tema verde esmeralda com foco em crescimento orgânico, conversão e retenção, transmitindo solidez e prosperidade financeira."
    },
    {
        "id": "10",
        "nome_estilo": "Boutique Beach Club & Sunset Island (Floripa Premium)",
        "tag": "Coastal Luxury & Gastro Bar",
        "font_import": '<link href="https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Satoshi:wght@400;500;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">',
        "font_family": "'Satoshi', sans-serif",
        "font_heading": "'Cabinet Grotesk', sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "bg": "#0F0C1B",
        "surface": "#181429",
        "card": "#211C38",
        "border": "#372F5E",
        "primary": "#F43F5E",
        "accent": "#FB923C",
        "text": "#FAF5FF",
        "text_muted": "#C084FC",
        "layout_type": "coastal_sunset",
        "desc": "Desenvolvido sob medida para a Ilha de Florianópolis (Jurerê, Ingleses, Santo Antônio): gradientes de pôr do sol, sofisticação noturna e alto apelo turístico."
    }
]

def render_html_modelo(m):
    # Gera o arquivo HTML de 3 páginas completo baseado nas especificações do modelo
    is_light = m["bg"] in ["#FFFFFF", "#FAF7F2", "#F4F4F0"]
    border_val = m["border"]
    
    font_h = m.get("font_heading", m["font_family"])
    
    # Customizações estruturais por layout
    top_bar_html = '<div style="height: 4px; background: linear-gradient(90deg, #4285F4 0%, #EA4335 32%, #FBBC05 68%, #34A853 100%); position: absolute; top:0; left:0; right:0;"></div>' if m["layout_type"] != "swiss_bauhaus" else '<div style="height: 6px; background: #1A1A1A; position: absolute; top:0; left:0; right:0;"></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Modelo {m['id']} — {m['nome_estilo']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{m['font_import']}
<style>
  :root {{
    --bg-page: {m['bg']};
    --surface: {m['surface']};
    --card: {m['card']};
    --border: {border_val};
    --primary: {m['primary']};
    --accent: {m['accent']};
    --text: {m['text']};
    --text-muted: {m['text_muted']};
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  @page {{
    size: 210mm 297mm;
    margin: 0;
  }}

  body {{
    background-color: var(--bg-page);
    font-family: {m['font_family']};
    color: var(--text);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page-container {{
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    background: var(--surface);
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

  h1, h2, h3, .heading {{
    font-family: {font_h};
  }}

  .mono {{
    font-family: {m['font_mono']};
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 10px;
  }}

  .header-tag {{
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--primary);
    text-transform: uppercase;
  }}

  .header-title {{
    font-size: 19px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
    margin-top: 2px;
  }}

  .header-sub {{
    font-size: 9.5px;
    color: var(--text-muted);
  }}

  .badge-page {{
    background: var(--card);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 8px;
    font-weight: 700;
    color: var(--text);
  }}

  .hero-box {{
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
  }}

  .hero-rank {{
    background: var(--accent);
    color: #FFFFFF;
    font-weight: 800;
    font-size: 18px;
    padding: 6px 14px;
    border-radius: 6px;
    text-align: center;
  }}
  .hero-rank span {{
    display: block;
    font-size: 7.5px;
    letter-spacing: 0.05em;
  }}

  .sec-title {{
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 10px 0 6px 0;
  }}
  .sec-badge {{
    font-size: 8px;
    font-weight: 800;
    background: var(--primary);
    color: {('#000' if is_light else '#FFF')};
    padding: 1px 5px;
    border-radius: 3px;
  }}
  .sec-h {{
    font-size: 11px;
    font-weight: 700;
    color: var(--text);
  }}
  .sec-hint {{
    font-size: 9px;
    color: var(--text-muted);
  }}

  .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}

  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 10px;
  }}

  .kpi-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 7px 9px;
  }}
  .kpi-lbl {{ font-size: 7.5px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }}
  .kpi-val {{ font-size: 16px; font-weight: 800; color: var(--text); margin: 2px 0; }}
  .kpi-sub {{ font-size: 7px; color: var(--text-muted); }}

  .nap-table {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  .nap-table td {{ padding: 4px 6px; border-bottom: 1px solid var(--border); }}
  .nap-l {{ color: var(--text-muted); font-weight: 600; width: 110px; }}
  .nap-v {{ color: var(--text); font-weight: 600; }}

  .pillar-row {{ display: flex; align-items: center; font-size: 8px; margin-bottom: 4px; }}
  .pillar-name {{ width: 120px; color: var(--text-muted); font-weight: 600; }}
  .pillar-bar {{ flex: 1; height: 5px; background: rgba(128,128,128,0.15); border-radius: 3px; margin: 0 8px; position: relative; overflow: hidden; }}
  .pillar-fill {{ height: 100%; background: var(--primary); border-radius: 3px; }}
  .pillar-val {{ width: 30px; text-align: right; font-weight: 700; color: var(--text); }}

  .tbl-comp {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  .tbl-comp th {{ background: rgba(128,128,128,0.08); color: var(--text-muted); font-size: 7px; font-weight: 700; text-transform: uppercase; padding: 5px 6px; text-align: left; border-bottom: 1.5px solid var(--border); }}
  .tbl-comp td {{ padding: 5px 6px; border-bottom: 1px solid var(--border); color: var(--text-muted); }}
  .tbl-comp tr.target-row {{ background: rgba(249, 115, 22, 0.12); font-weight: 700; }}
  .tbl-comp tr.target-row td {{ color: var(--text); border-top: 1.5px solid var(--accent); border-bottom: 1.5px solid var(--accent); }}

  .ck-item {{ display: flex; align-items: flex-start; gap: 6px; padding: 4px 0; border-bottom: 1px solid var(--border); font-size: 8px; }}
  .ck-ico {{ width: 12px; height: 12px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 7px; font-weight: 800; flex-shrink: 0; margin-top: 1px; background: var(--primary); color: {('#000' if is_light else '#FFF')}; }}
  .ck-txt strong {{ color: var(--text); font-weight: 700; font-size: 8.5px; }}
  .ck-txt p {{ color: var(--text-muted); font-size: 7.5px; margin-top: 1px; }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid var(--border);
    padding-top: 6px;
    font-size: 7.5px;
    color: var(--text-muted);
  }}
</style>
</head>
<body>

<!-- PÁGINA 1 -->
<div class="page-container">
  {top_bar_html}
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Modelo {m['id']} · {m['tag']}</div>
        <div class="header-title">Paixão Restaurante & Pizzaria</div>
        <div class="header-sub">Diagnóstico de Posicionamento, Autoridade Local e Conversão Mobile</div>
      </div>
      <div style="text-align:right;">
        <div class="badge-page mono">PÁGINA 01 / 03</div>
        <div style="font-size: 8px; color: var(--text-muted); margin-top:3px;">Florianópolis · Ingleses</div>
      </div>
    </div>

    <!-- Hero -->
    <div class="hero-box">
      <div>
        <h3 style="font-size: 14px; font-weight: 800; color: var(--text);">Líder Absoluto em Volume no Norte da Ilha</h3>
        <p style="font-size: 9px; color: var(--text-muted); margin-top: 2px;">Perfil com <strong>5.385 avaliações</strong> e nota <strong>4.5 ★</strong>. 1º lugar na busca local.<br>Oportunidade crítica: blindagem de liderança e implementação de cardápio próprio.</p>
      </div>
      <div class="hero-rank mono">
        1º<span>LUGAR</span>
      </div>
    </div>

    <!-- NAP -->
    <div class="sec-title">
      <span class="sec-badge mono">01</span>
      <span class="sec-h">Consistência Cadastral & Sinal de NAP</span>
      <span class="sec-hint">· Indexação Google Places</span>
    </div>
    <div class="card" style="padding: 4px 8px;">
      <table class="nap-table">
        <tr>
          <td class="nap-l">Nome Oficial (NAP):</td>
          <td class="nap-v">Paixão Restaurante & Pizzaria <span style="color:var(--primary); font-size:7.5px; font-weight:800;">✓ Verificado</span></td>
          <td class="nap-l">Categoria Primária:</td>
          <td class="nap-v">Frutos do Mar / Pizzaria</td>
        </tr>
        <tr>
          <td class="nap-l">Endereço Completo:</td>
          <td class="nap-v" colspan="3">Estrada Dom João Becker, 259 - Praia dos Ingleses, Florianópolis - SC, 88058-601</td>
        </tr>
        <tr>
          <td class="nap-l">Telefone Oficial:</td>
          <td class="nap-v mono">(48) 3269-1002</td>
          <td class="nap-l">Coordenadas GPS:</td>
          <td class="nap-v mono">-27.43501, -48.39512</td>
        </tr>
      </table>
    </div>

    <!-- KPIs -->
    <div class="sec-title">
      <span class="sec-badge mono">02</span>
      <span class="sec-h">Scorecard de Autoridade & SERP</span>
      <span class="sec-hint">· Métricas do Algoritmo Local</span>
    </div>
    <div class="grid-4">
      <div class="kpi-card">
        <div class="kpi-lbl">Score SEO Local</div>
        <div class="kpi-val mono" style="color:var(--primary);">90<small style="font-size:9px; color:var(--text-muted);">/100</small></div>
        <div class="kpi-sub">Autoridade Máxima</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">Volume Reviews</div>
        <div class="kpi-val mono" style="color:var(--accent);">5.385</div>
        <div class="kpi-sub">1º no Norte da Ilha</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">Nota Média</div>
        <div class="kpi-val mono">4.5 <small style="font-size:10px;">★</small></div>
        <div class="kpi-sub">Satisfação Comprovada</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-lbl">Potencial Ganho</div>
        <div class="kpi-val mono" style="color:var(--primary);">+35%</div>
        <div class="kpi-sub">Conversão Direta</div>
      </div>
    </div>

    <!-- Pilares -->
    <div class="sec-title">
      <span class="sec-badge mono">03</span>
      <span class="sec-h">Auditoria dos 6 Pilares Algorítmicos</span>
      <span class="sec-hint">· Performance vs. Meta Ouro (80%)</span>
    </div>
    <div class="card">
      <div class="pillar-row">
        <span class="pillar-name">1. Consistência NAP & GPS</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 95%;"></div></div>
        <span class="pillar-val mono">95%</span>
      </div>
      <div class="pillar-row">
        <span class="pillar-name">2. Volume de Avaliações</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 98%;"></div></div>
        <span class="pillar-val mono">98%</span>
      </div>
      <div class="pillar-row">
        <span class="pillar-name">3. Vitrine & Qualidade Fotos</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 85%;"></div></div>
        <span class="pillar-val mono">85%</span>
      </div>
      <div class="pillar-row">
        <span class="pillar-name">4. Recência de Novos Reviews</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 72%;"></div></div>
        <span class="pillar-val mono">72%</span>
      </div>
      <div class="pillar-row">
        <span class="pillar-name">5. Taxa de Resposta a Clientes</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 40%; background: var(--accent);"></div></div>
        <span class="pillar-val mono">40%</span>
      </div>
      <div class="pillar-row" style="margin-bottom:0;">
        <span class="pillar-name">6. Cardápio Mobile & Conversão</span>
        <div class="pillar-bar"><div class="pillar-fill" style="width: 30%; background: var(--accent);"></div></div>
        <span class="pillar-val mono">30%</span>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome_estilo']}</span>
    <span class="mono">Página 01 / 03</span>
  </div>
</div>

<!-- PÁGINA 2 -->
<div class="page-container">
  {top_bar_html}
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Modelo {m['id']} · Inteligência Competitiva</div>
        <div class="header-title">Benchmarking & Análise de Raio Local</div>
        <div class="header-sub">Mapeamento de Fluxo de Busca e Desempenho Regional</div>
      </div>
      <div style="text-align:right;">
        <div class="badge-page mono">PÁGINA 02 / 03</div>
        <div style="font-size: 8px; color: var(--text-muted); margin-top:3px;">Raio: 2.5 km · Norte da Ilha</div>
      </div>
    </div>

    <!-- Tabela Concorrentes -->
    <div class="sec-title">
      <span class="sec-badge mono">04</span>
      <span class="sec-h">Ranking de Visibilidade no Google Maps</span>
      <span class="sec-hint">· Top Estabelecimentos</span>
    </div>
    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="tbl-comp">
        <thead>
          <tr>
            <th style="width: 30px;">Pos.</th>
            <th>Estabelecimento</th>
            <th>Nicho / Categoria</th>
            <th>Nota</th>
            <th>Avaliações</th>
            <th>Cardápio</th>
            <th>WhatsApp</th>
          </tr>
        </thead>
        <tbody>
          <tr class="target-row">
            <td><strong>1º</strong></td>
            <td>Paixão Restaurante & Pizzaria <span style="background:var(--accent); color:#FFF; font-size:6.5px; padding:1px 4px; border-radius:3px;">ALVO AUDITADO</span></td>
            <td>Frutos do Mar & Pizza</td>
            <td><strong>4.5 ★</strong></td>
            <td><strong>5.385</strong></td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>2º</td>
            <td>Don Zarichta Pizzaria Artesanal</td>
            <td>Pizzaria & Italiana</td>
            <td>4.9 ★</td>
            <td>5.230</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>3º</td>
            <td>Costillas Grill - Costelaria</td>
            <td>Carnes & Parrilla</td>
            <td>4.3 ★</td>
            <td>4.791</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>4º</td>
            <td>Freguesia Bar</td>
            <td>Frutos do Mar & Bar</td>
            <td>4.4 ★</td>
            <td>4.377</td>
            <td>Não</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>5º</td>
            <td>Villa do Porto Gastronomia</td>
            <td>Frutos do Mar & Bar</td>
            <td>4.6 ★</td>
            <td>3.983</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>6º</td>
            <td>Antonio's Restaurante</td>
            <td>Frutos do Mar</td>
            <td>4.7 ★</td>
            <td>3.918</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>7º</td>
            <td>Camarão Chef Seghetto</td>
            <td>Frutos do Mar</td>
            <td>4.6 ★</td>
            <td>3.857</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
          <tr>
            <td>8º</td>
            <td>Pizzaria Happy</td>
            <td>Pizzaria Delivery</td>
            <td>4.6 ★</td>
            <td>3.771</td>
            <td>Sim</td>
            <td>Sim</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 3 Pilares -->
    <div class="sec-title">
      <span class="sec-badge mono">05</span>
      <span class="sec-h">Plano Estratégico de Blindagem & Conversão</span>
      <span class="sec-hint">· 3 Pilares Operacionais</span>
    </div>
    <div class="grid-3">
      <div class="card" style="border-top: 2.5px solid var(--primary);">
        <div style="font-size:7.5px; font-weight:800; color:var(--primary); text-transform:uppercase;">Pilar 01 · Imediato</div>
        <div style="font-size:10px; font-weight:700; color:var(--text); margin: 3px 0;">Cardápio Mobile Próprio</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Página web veloz com fotos dos pratos indexada no Google, eliminando desistências na busca.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--primary); font-weight:700;">Prazo: 7 a 10 dias</div>
      </div>
      <div class="card" style="border-top: 2.5px solid var(--accent);">
        <div style="font-size:7.5px; font-weight:800; color:var(--accent); text-transform:uppercase;">Pilar 02 · Salão</div>
        <div style="font-size:10px; font-weight:700; color:var(--text); margin: 3px 0;">Motor de Reviews 5★</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Displays inteligentes com NFC e QR Code no balcão e mesas para coletar +80 avaliações por mês.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--accent); font-weight:700;">Prazo: Imediato</div>
      </div>
      <div class="card" style="border-top: 2.5px solid var(--primary);">
        <div style="font-size:7.5px; font-weight:800; color:var(--primary); text-transform:uppercase;">Pilar 03 · Reputação</div>
        <div style="font-size:10px; font-weight:700; color:var(--text); margin: 3px 0;">Gestão Ativa de Feedback</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Rotina semanal de resposta à totalidade dos comentários utilizando palavras-chave semânticas.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--primary); font-weight:700;">Prazo: Contínuo</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome_estilo']}</span>
    <span class="mono">Página 02 / 03</span>
  </div>
</div>

<!-- PÁGINA 3 -->
<div class="page-container">
  {top_bar_html}
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Modelo {m['id']} · Checklist Executivo</div>
        <div class="header-title">Diagnóstico Ponto a Ponto & Próximos Passos</div>
        <div class="header-sub">Status dos 10 Fatores de Ranqueamento do Google Maps</div>
      </div>
      <div style="text-align:right;">
        <div class="badge-page mono">PÁGINA 03 / 03</div>
        <div style="font-size: 8px; color: var(--text-muted); margin-top:3px;">Auditoria Técnica Final</div>
      </div>
    </div>

    <!-- Status Geral -->
    <div class="sec-title">
      <span class="sec-badge mono">06</span>
      <span class="sec-h">Distribuição dos Fatores Auditados</span>
      <span class="sec-hint">· Resumo Geral</span>
    </div>
    <div class="grid-3">
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 16px; font-weight:800; color:var(--primary);">7/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--primary);">CONFORME</div>
          <div style="font-size: 7px; color:var(--text-muted);">Itens validados e ativos</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 16px; font-weight:800; color:var(--accent);">2/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--accent);">ATENÇÃO</div>
          <div style="font-size: 7px; color:var(--text-muted);">Oportunidade de ganho</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div class="mono" style="font-size: 16px; font-weight:800; color:var(--accent);">1/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--accent);">CRÍTICO</div>
          <div style="font-size: 7px; color:var(--text-muted);">Gargalo de conversão</div>
        </div>
      </div>
    </div>

    <!-- Checklist -->
    <div class="sec-title">
      <span class="sec-badge mono">07</span>
      <span class="sec-h">Checklist de Conformidade Técnica</span>
      <span class="sec-hint">· 10 Fatores Críticos</span>
    </div>
    <div class="card" style="padding: 2px 10px;">
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>01. Nome Comercial (NAP):</strong>
          <p>Nome limpo, alinhado à fachada física e sem infrações de diretrizes do Google.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>02. Geolocalização e Pino GPS:</strong>
          <p>Marcador de rota posicionado com precisão na Praia dos Ingleses.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>03. Telefone Oficial com Discagem Direta:</strong>
          <p>Contato fixo e atendimento configurado com funcionalidade mobile.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>04. Horários de Atendimento Sincronizados:</strong>
          <p>Períodos de almoço e jantar consistentes com a operação real.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>05. Qualidade Visual da Galeria:</strong>
          <p>Fotos atraentes de pratos, frutos do mar, pizzas e ambiente do restaurante.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>06. Densidade de Avaliações:</strong>
          <p>Volume massivo de 5.385 reviews consolidando a autoridade de busca no bairro.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico" style="background:var(--accent);">!</div>
        <div class="ck-txt">
          <strong>07. Taxa de Resposta a Feedbacks:</strong>
          <p>Grande volume de comentários sem respostas da gestão. Perda de relevância semântica.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico" style="background:var(--accent);">!</div>
        <div class="ck-txt">
          <strong>08. Recência e Fluxo de Notas:</strong>
          <p>Necessidade de incentivo constante para manter o algoritmo sempre aquecido.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico" style="background:var(--accent);">✕</div>
        <div class="ck-txt">
          <strong>09. Cardápio Digital Mobile Otimizado:</strong>
          <p>Ausência de página própria com pratos e valores, gerando dispersão de clientes para concorrentes.</p>
        </div>
      </div>
      <div class="ck-item" style="border-bottom:none;">
        <div class="ck-ico">✓</div>
        <div class="ck-txt">
          <strong>10. Botão Direto de WhatsApp / Atendimento:</strong>
          <p>Canal de comunicação configurado para reservas e pedidos de clientes.</p>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="card" style="margin-top: 8px; border: 1.5px solid var(--primary); padding: 8px 12px;">
      <div style="font-size: 7.5px; font-weight:800; color:var(--primary); text-transform:uppercase;">Próximo Passo Recomendado</div>
      <div style="font-size: 9.5px; font-weight:700; color:var(--text); margin-top:1px;">Ativação do Cardápio Mobile Próprio & Displays Inteligentes NFC</div>
      <p style="font-size: 7.5px; color:var(--text-muted); margin-top:1px; line-height:1.35;">Sustente a liderança do Paixão Restaurante com um motor ativo de avaliações 5 estrelas e catálogo mobile veloz para turistas e moradores.</p>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · {m['nome_estilo']}</span>
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
        slug = f"modelo_{m_id}_{m['layout_type']}"
        html_file = f"{HTML_DIR}/{slug}.html"
        pdf_file = f"{PDF_DIR}/Modelo_{m_id}_{m['layout_type']}.pdf"
        png_p1 = f"{PNG_DIR}/Modelo_{m_id}_p1.png"
        
        # 1. Escrever HTML
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(render_html_modelo(m))
            
        # 2. Compilar PDF via Edge Headless
        cmd = f'"{EDGE_BIN}" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw --print-to-pdf="{os.path.abspath(pdf_file)}" "{os.path.abspath(html_file)}"'
        subprocess.run(cmd, shell=True, check=True)
        
        # 3. Gerar Preview PNG da Página 1
        doc = pymupdf.open(pdf_file)
        pix = doc[0].get_pixmap(dpi=150)
        pix.save(png_p1)
        
        print(f"[OK] Modelo {m_id} gerado: {m['nome_estilo']} -> {pdf_file}")

if __name__ == "__main__":
    main()

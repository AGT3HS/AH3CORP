import json, os, glob, re, base64

# 1. Carregar lista dos hotéis
with open(r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_hotelaria_florianopolis.json', 'r', encoding='utf-8') as f:
    hotels = json.load(f)

# 2. Carregar dados de logos auditadas
with open(r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_top40.json', 'r', encoding='utf-8') as f:
    logos_info = json.load(f)

logos_map = {item['ranking']: item for item in logos_info}

top40 = hotels[:40]
output_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual'
logos_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual\logos'
os.makedirs(output_dir, exist_ok=True)

# Cores e estilos por hotel/categoria
category_palettes = {
    'Resort All-Inclusive / 5 Estrelas': ['#1B3B2B', '#D4AF37', '#F5F5F0', '#2C3E50', '#8C7B63'],
    'Resort Pé na Areia': ['#0D3B66', '#EE964B', '#F4F1DE', '#112233', '#E09F3E'],
    'Hotel Boutique / Luxo': ['#1A1A1A', '#C5A880', '#F9F8F6', '#333333', '#8A7968'],
    'Hotel Corporativo / Executivo': ['#0F2027', '#203A43', '#2C5364', '#F8F9FA', '#007BFF'],
    'Hotel & Long/Short Stay': ['#FF5A5F', '#00A699', '#484848', '#767676', '#F7F7F7'],
    'Hotel Urbano Central': ['#1E293B', '#3B82F6', '#F1F5F9', '#64748B', '#0F172A'],
    'Hotel Pé na Areia': ['#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8', '#03045E']
}

default_palette = ['#1B2420', '#C5A880', '#F5F4EE', '#4B564F', '#8A8578']

def clean_slug(s):
    s = re.sub(r'[^a-zA-Z0-9_-]', '_', s)
    return re.sub(r'_+', '_', s).strip('_').lower()

generated_count = 0

for h in top40:
    rank = h['ranking']
    nome = h['nome']
    unidade = h.get('unidade', '')
    cat = h.get('categoria', 'Hotel')
    reg = h.get('regiao', 'Florianópolis')
    quartos = h.get('quartos', 0)
    diaria = h.get('diaria_media', 0)
    site = h.get('site', '')
    
    logo_meta = logos_map.get(rank, {})
    logo_file = logo_meta.get('arquivo', '-')
    
    # Resolver caminho da logo e embedding base64 se existir
    logo_data_uri = ""
    logo_html_tag = ""
    
    if logo_file and logo_file != '-':
        logo_path = os.path.join(logos_dir, logo_file)
        if os.path.exists(logo_path):
            try:
                with open(logo_path, 'rb') as lf:
                    raw_bytes = lf.read()
                    if logo_file.endswith('.svg'):
                        # Se for SVG, pode colocar inline ou base64
                        b64 = base64.b64encode(raw_bytes).decode('utf-8')
                        logo_data_uri = f"data:image/svg+xml;base64,{b64}"
                    elif logo_file.endswith('.png'):
                        b64 = base64.b64encode(raw_bytes).decode('utf-8')
                        logo_data_uri = f"data:image/png;base64,{b64}"
                    elif logo_file.endswith('.jpg') or logo_file.endswith('.jpeg'):
                        b64 = base64.b64encode(raw_bytes).decode('utf-8')
                        logo_data_uri = f"data:image/jpeg;base64,{b64}"
                    elif logo_file.endswith('.webp'):
                        b64 = base64.b64encode(raw_bytes).decode('utf-8')
                        logo_data_uri = f"data:image/webp;base64,{b64}"
            except:
                pass

    if logo_data_uri:
        logo_html_tag = f'<img src="{logo_data_uri}" alt="Logo {nome}" />'
    elif logo_file and logo_file != '-':
        logo_html_tag = f'<img src="logos/{logo_file}" alt="Logo {nome}" />'
    else:
        logo_html_tag = f'<div style="font-size: 28px; font-weight: 800; color: #1B2420; letter-spacing: -0.02em;">{nome.upper()}</div><p style="font-size: 12px; color: #8A8578; margin-top: 8px;">(Logotipo não disponível publicamente — buscar Kit Oficial de Imprensa)</p>'

    palette = category_palettes.get(cat, default_palette)
    
    # Template HTML do Guia Visual
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{nome} — Guia de Identidade Visual (AH3)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #F8F9FA;
    --surface: #FFFFFF;
    --ink: #111827;
    --ink-soft: #4B5563;
    --line: #E5E7EB;
    --primary: {palette[0]};
    --accent: {palette[1]};
    --stone: #6B7280;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--ink);
    font-family: 'Plus Jakarta Sans', sans-serif;
    line-height: 1.6;
    padding: 32px 20px;
  }}
  .wrap {{
    max-width: 900px;
    margin: 0 auto;
  }}
  .hero {{
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  }}
  .kicker {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin-bottom: 8px;
  }}
  h1 {{
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    color: var(--ink);
    line-height: 1.15;
    margin-bottom: 12px;
  }}
  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid var(--line);
  }}
  .meta-item b {{
    display: block;
    font-size: 11px;
    color: var(--stone);
    text-transform: uppercase;
  }}
  .meta-item span {{
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
  }}
  .section {{
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  }}
  h2 {{
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .logo-box {{
    background: #FFFFFF;
    border: 1px dashed #CBD5E1;
    border-radius: 12px;
    padding: 48px 24px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 180px;
    margin-bottom: 20px;
  }}
  .logo-box img {{
    max-height: 110px;
    max-width: 320px;
    object-fit: contain;
  }}
  .swatches {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
  }}
  .swatch {{
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
    background: #FFFFFF;
  }}
  .swatch .fill {{
    height: 70px;
  }}
  .swatch .info {{
    padding: 10px;
    font-size: 12px;
  }}
  .swatch .info b {{
    display: block;
    font-size: 13px;
    margin-bottom: 2px;
  }}
  .rules {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
  }}
  .rules div {{
    background: #F9FAFB;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 16px;
  }}
  .rules div h3 {{
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .rules div p {{
    font-size: 12px;
    color: var(--ink-soft);
  }}
  footer {{
    text-align: center;
    font-size: 12px;
    color: var(--stone);
    padding: 20px 0;
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="kicker">Auditoria AH3 · Ranking #{rank:02d} Florianópolis</div>
      <h1>Guia de Identidade Visual<br>{nome}</h1>
      <p style="color: var(--ink-soft); font-size: 15px;">Parâmetros visuais, tipografia, paleta e ativos oficiais extraídos para padronização de touchpoints físicos (Plaquinhas 10x10 NFC) e comunicação estratégica.</p>
      
      <div class="meta-grid">
        <div class="meta-item">
          <b>Capacidade Instalada</b>
          <span>{quartos} Quartos / UHs</span>
        </div>
        <div class="meta-item">
          <b>Diária Média</b>
          <span>R$ {diaria:,.2f}</span>
        </div>
        <div class="meta-item">
          <b>Localização / Bairro</b>
          <span>{reg}</span>
        </div>
        <div class="meta-item">
          <b>Canal Oficial</b>
          <span><a href="{site}" target="_blank" style="color: var(--accent); text-decoration: none;">Acessar Site ↗</a></span>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="kicker">Ativo Vetorial / Imagem</div>
      <h2>Logotipo Oficial Anexado</h2>
      <div class="logo-box">
        {logo_html_tag}
      </div>
      <div class="rules">
        <div>
          <h3>Fidelidade e Proporção</h3>
          <p>Preservar área de respiro mínima de 20% ao redor do logotipo e contraste adequado no fundo escuro ou claro.</p>
        </div>
        <div>
          <h3>Aplicação em Placas NFC</h3>
          <p>Alinhamento estrito à esquerda do topo escuro nas plaquinhas 10x10 cm, isolando a área do chip NFC à direita.</p>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="kicker">Sistema Cromático</div>
      <h2>Paleta Institucional Detectada</h2>
      <div class="swatches">
        <div class="swatch"><div class="fill" style="background: {palette[0]};"></div><div class="info"><b>Primária</b><code>{palette[0]}</code></div></div>
        <div class="swatch"><div class="fill" style="background: {palette[1]};"></div><div class="info"><b>Acento / Destaque</b><code>{palette[1]}</code></div></div>
        <div class="swatch"><div class="fill" style="background: {palette[2]};"></div><div class="info"><b>Superfície Clara</b><code>{palette[2]}</code></div></div>
        <div class="swatch"><div class="fill" style="background: {palette[3]};"></div><div class="info"><b>Texto / Detalhes</b><code>{palette[3]}</code></div></div>
        <div class="swatch"><div class="fill" style="background: {palette[4]};"></div><div class="info"><b>Neutro de Apoio</b><code>{palette[4]}</code></div></div>
      </div>
    </div>

    <footer>
      AH3 Intelligence & Design Ops · Guia Técnico de Uso Interno · {nome}
    </footer>
  </div>
</body>
</html>
"""
    
    slug_name = f"{rank:02d}_{clean_slug(nome)[:30]}.html"
    out_file = os.path.join(output_dir, slug_name)
    with open(out_file, 'w', encoding='utf-8') as f_out:
        f_out.write(html)
        
    generated_count += 1

print(f"Total de Guias de Identidade Visual gerados: {generated_count}")

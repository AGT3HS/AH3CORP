import json, os, glob, re, base64

# 1. Carregar lista dos hotéis
with open(r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_hotelaria_florianopolis.json', 'r', encoding='utf-8') as f:
    hotels = json.load(f)

# 2. Carregar dados de logos auditadas
logos_map = {}
for lpath in [r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_150.json', r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_top40.json']:
    if os.path.exists(lpath):
        try:
            with open(lpath, 'r', encoding='utf-8') as lf:
                for item in json.load(lf):
                    if item['ranking'] not in logos_map:
                        logos_map[item['ranking']] = item
        except Exception:
            pass

output_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual'
logos_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual\logos'
os.makedirs(output_dir, exist_ok=True)

# Paletas e tokens
category_palettes = {
    'Resort All-Inclusive / 5 Estrelas': ['#1B3B2B', '#D4AF37', '#F5F5F0', '#2C3E50', '#8C7B63'],
    'Resort Pé na Areia': ['#0D3B66', '#EE964B', '#F4F1DE', '#112233', '#E09F3E'],
    'Hotel Boutique / Luxo': ['#1A1A1A', '#C5A880', '#F9F8F6', '#333333', '#8A7968'],
    'Hotel Corporativo / Executivo': ['#0F2027', '#203A43', '#2C5364', '#F8F9FA', '#007BFF'],
    'Hotel & Long/Short Stay': ['#FF5A5F', '#00A699', '#484848', '#767676', '#F7F7F7'],
    'Hotel Urbano Central': ['#1E293B', '#3B82F6', '#F1F5F9', '#64748B', '#0F172A'],
    'Hotel Pé na Areia': ['#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8', '#03045E'],
    'Hotel de Lazer': ['#1E3A8A', '#F59E0B', '#F8FAFC', '#334155', '#D97706'],
    'Pousada Boutique': ['#4A3B32', '#C6A982', '#FAF7F2', '#2B211B', '#8C7A6B']
}

default_palette = ['#1B2420', '#C5A880', '#F5F4EE', '#4B564F', '#8A8578']

def clean_slug(s):
    s = re.sub(r'[^a-zA-Z0-9_-]', '_', s)
    return re.sub(r'_+', '_', s).strip('_').lower()

generated_count = 0

for idx, h in enumerate(hotels):
    rank = h.get('ranking') or idx + 1
    nome = h['nome']
    unidade = h.get('unidade', '')
    cat = h.get('categoria', 'Hotel')
    reg = h.get('regiao', 'Florianópolis')
    quartos = h.get('quartos', 0)
    diaria = h.get('diaria_media', 0)
    site = h.get('site', '')
    
    logo_meta = logos_map.get(rank, {})
    logo_file = logo_meta.get('arquivo', '-')
    
    logo_data_uri = ""
    logo_html_tag = ""
    
    if logo_file and logo_file != '-':
        logo_path = os.path.join(logos_dir, logo_file)
        if os.path.exists(logo_path):
            try:
                with open(logo_path, 'rb') as lf:
                    raw_bytes = lf.read()
                    if logo_file.endswith('.svg'):
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
            except Exception:
                pass
                
    if logo_data_uri:
        logo_html_tag = f'<img src="{logo_data_uri}" alt="Logo Oficial - {nome}" style="max-height: 90px; max-width: 260px; object-fit: contain;">'
    else:
        logo_html_tag = f'<div style="font-family: \'Cinzel\', serif; font-size: 22px; font-weight: 700; letter-spacing: 2px; color: #D4AF37;">{nome.upper()}</div>'

    palette = category_palettes.get(cat, default_palette)
    p_primary, p_gold, p_bg, p_card, p_accent = palette

    slug = f"{rank:02d}_{clean_slug(nome)[:30]}"
    file_name = f"{slug}.html"
    file_path = os.path.join(output_dir, file_name)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guia de Identidade Visual · {nome}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --c-primary: {p_primary};
            --c-gold: {p_gold};
            --c-bg: #090D0E;
            --c-card: #12181A;
            --c-card-border: #1E282C;
            --c-text: #E5EAE8;
            --c-muted: #8E9E98;
            --c-accent: {p_accent};
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: var(--c-bg);
            color: var(--c-text);
            font-family: 'Plus Jakarta Sans', sans-serif;
            line-height: 1.6;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(145deg, #131B1E, #0D1315);
            border: 1px solid var(--c-card-border);
            border-radius: 16px;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--c-gold), transparent);
        }}
        .badge-rank {{
            background: rgba(212, 175, 55, 0.15);
            color: var(--c-gold);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }}
        .hotel-title {{
            font-family: 'Cinzel', serif;
            font-size: 32px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 8px;
        }}
        .hotel-meta {{
            color: var(--c-muted);
            font-size: 15px;
        }}
        .logo-box {{
            background: #FFFFFF;
            padding: 20px 30px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            min-width: 260px;
            min-height: 110px;
        }}
        .grid-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        .card {{
            background: var(--c-card);
            border: 1px solid var(--c-card-border);
            border-radius: 14px;
            padding: 30px;
        }}
        .card-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--c-gold);
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .palette-row {{
            display: flex;
            gap: 12px;
            margin-top: 15px;
        }}
        .swatch {{
            flex: 1;
            height: 70px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 8px;
            font-size: 11px;
            font-weight: 600;
            color: #FFFFFF;
            text-shadow: 0 1px 2px rgba(0,0,0,0.8);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .data-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 14px;
        }}
        .data-label {{ color: var(--c-muted); }}
        .data-val {{ font-weight: 600; color: #FFF; }}
        .btn-site {{
            display: inline-block;
            margin-top: 15px;
            padding: 8px 16px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            color: #FFF;
            text-decoration: none;
            border-radius: 6px;
            font-size: 13px;
            transition: all 0.2s;
        }}
        .btn-site:hover {{
            background: var(--c-gold);
            color: #000;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <span class="badge-rank">RANKING OFICIAL #{rank:02d}</span>
                <h1 class="hotel-title">{nome}</h1>
                <div class="hotel-meta">{unidade} · {reg} · {cat}</div>
            </div>
            <div class="logo-box">
                {logo_html_tag}
            </div>
        </div>

        <div class="grid-cards">
            <div class="card">
                <div class="card-title">Identidade Visual & Cores</div>
                <p style="font-size: 14px; color: var(--c-muted); margin-bottom: 15px;">Paleta cromática institucional baseada nos ativos oficiais e arquitetura de marca do empreendimento.</p>
                <div class="palette-row">
                    <div class="swatch" style="background: {p_primary};">{p_primary}</div>
                    <div class="swatch" style="background: {p_gold}; color: #000; text-shadow: none;">{p_gold}</div>
                    <div class="swatch" style="background: {p_accent};">{p_accent}</div>
                    <div class="swatch" style="background: {p_card};">{p_card}</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">Métricas de Operação</div>
                <div class="data-row">
                    <span class="data-label">Capacidade Declarada</span>
                    <span class="data-val">{quartos} Apartamentos</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Diária Média Estimada</span>
                    <span class="data-val">R$ {diaria:.2f}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Status do Logotipo</span>
                    <span class="data-val">{logo_meta.get('qualidade', 'Auditado / Vetorizado')}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Presença Digital</span>
                    <span class="data-val"><a href="{site}" target="_blank" class="btn-site">Visitar Website Oficial →</a></span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    generated_count += 1

print(f"\nSucesso: {generated_count} guias de identidade visual consolidados em {output_dir}!")

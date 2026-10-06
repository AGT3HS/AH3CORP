import openpyxl, json, glob, os, re, unicodedata

wb_path = 'C:/Users/Augusto/Desktop/AH3/Auditoria_Hotelaria_Florianopolis.xlsx'
wb = openpyxl.load_workbook(wb_path, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

guias_files = {}
for d in ['C:/Users/Augusto/Desktop/AH3/guias_identidade_visual']:
    for f in glob.glob(os.path.join(d, '*.html')):
        guias_files[os.path.basename(f)] = f.replace('\\', '/')

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

# Mapear propostas em PDF
pdf_propostas = {}
for pdf in glob.glob('C:/Users/Augusto/Desktop/AH3/*.pdf'):
    bname = os.path.basename(pdf)
    norm_pdf = normalize(bname)
    pdf_propostas[norm_pdf] = pdf.replace('\\', '/')

# Mapear plaquinhas 10x10
placas_map = {}
for p in glob.glob('C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/*.svg') + glob.glob('C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/*.png'):
    bname = os.path.basename(p)
    if 'card_10x10' in bname or 'card' in bname or 'placa' in bname:
        placas_map[normalize(bname)] = p.replace('\\', '/')

data = []
for r in rows[1:]:
    ranking = r[0]
    nome = r[1]
    unidade = r[2] or ''
    cat = r[3] or ''
    bairro = r[4] or ''
    quartos = r[5] or 0
    diaria = r[6] or 0
    site = r[7] or ''
    iv_status = r[8] or ''
    placa_status = r[9] or ''
    prop_status = r[10] or ''
    venda_status = r[11] or 'Não Iniciado'
    valor = r[12] or 0
    
    norm_nome = normalize(nome)
    
    # Guia
    guia_match = None
    for gname, gpath in guias_files.items():
        prefix_match = re.match(r'^(\d+)_', gname)
        if prefix_match and int(prefix_match.group(1)) == ranking:
            guia_match = gpath
            break
        norm_gname = normalize(gname)
        if norm_nome in norm_gname or norm_gname in norm_nome:
            guia_match = gpath
            break

    # Plaquinha
    placa_match = None
    for pnorm, ppath in placas_map.items():
        if norm_nome[:6] in pnorm or f"{ranking:02d}" in pnorm or f"{ranking:03d}" in pnorm:
            placa_match = ppath
            break

    # Proposta PDF
    pdf_match = None
    for pnorm, ppath in pdf_propostas.items():
        if norm_nome[:6] in pnorm:
            pdf_match = ppath
            break

    data.append({
        'ranking': ranking,
        'nome': nome,
        'unidade': unidade,
        'categoria': cat,
        'bairro': bairro,
        'quartos': quartos,
        'diaria': diaria,
        'site': site,
        'tem_guia': bool(guia_match),
        'guia_path': guia_match or '',
        'tem_placa': bool(placa_match),
        'placa_path': placa_match or '',
        'tem_pdf': bool(pdf_match),
        'pdf_path': pdf_match or '',
        'status_venda': venda_status,
        'valor': valor
    })

data_json = json.dumps(data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auditoria Hotelaria Florianópolis — Painel de Controle (AH3)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0b0f17;
  --card: #131b26;
  --border: #1e293b;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --accent: #f97316;
  --accent-glow: rgba(249, 115, 22, 0.15);
  --success: #10b981;
  --danger: #ef4444;
  --warning: #f59e0b;
  --purple: #8b5cf6;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  padding: 24px;
  min-height: 100vh;
}}
.header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 20px;
}}
.title-block h1 {{
  font-size: 24px;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.badge-live {{
  font-size: 11px;
  background: #064e3b;
  color: #34d399;
  padding: 4px 10px;
  border-radius: 9999px;
  font-weight: 700;
  text-transform: uppercase;
  border: 1px solid #059669;
}}
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}}
.kpi-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
}}
.kpi-val {{
  font-size: 28px;
  font-weight: 800;
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
}}
.controls {{
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}}
.search-input {{
  flex: 1;
  min-width: 280px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  font-family: inherit;
  font-size: 14px;
}}
.search-input:focus {{
  outline: none;
  border-color: var(--accent);
}}
.select-filter {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  font-family: inherit;
  font-size: 14px;
}}
.table-container {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow-x: auto;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}
th {{
  background: #0f1622;
  color: var(--muted);
  text-align: left;
  padding: 14px 16px;
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
}}
td {{
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}}
tr:hover {{
  background: rgba(255, 255, 255, 0.02);
}}
.tag-done {{
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}}
.tag-pending {{
  background: rgba(148, 163, 184, 0.15);
  color: var(--muted);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
}}
.site-badge {{
  background: rgba(249, 115, 22, 0.2);
  color: #fb923c;
  padding: 4px 8px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 12px;
  border: 1px solid rgba(249, 115, 22, 0.3);
  display: inline-block;
}}
.site-badge:hover {{
  background: var(--accent);
  color: #fff;
}}
.btn-group {{
  display: flex;
  gap: 6px;
  align-items: center;
}}
.btn-action {{
  background: #1e293b;
  color: #fff;
  border: 1px solid #334155;
  padding: 6px 10px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 11px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}}
.btn-action:hover {{
  background: var(--accent);
  border-color: var(--accent);
}}
.btn-placa {{
  background: rgba(139, 92, 246, 0.15);
  color: #c4b5fd;
  border: 1px solid rgba(139, 92, 246, 0.3);
}}
.btn-placa:hover {{
  background: var(--purple);
  color: #fff;
  border-color: var(--purple);
}}
.btn-pdf {{
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}}
.btn-pdf:hover {{
  background: var(--danger);
  color: #fff;
  border-color: var(--danger);
}}
.btn-disabled {{
  opacity: 0.35;
  cursor: not-allowed;
  pointer-events: none;
}}
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>🏢 Auditoria Hotelaria Florianópolis <span class="badge-live">Base Contínua</span></h1>
      <p style="color: var(--muted); font-size: 13px; margin-top: 4px;">AH3 Intelligence & Design Ops · Priorização por Quartos e Diária Média</p>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div style="color: var(--muted); font-size: 12px; font-weight: 600;">Total Mapeado</div>
      <div class="kpi-val" id="kpi-total" style="color: var(--accent);">0</div>
    </div>
    <div class="kpi-card">
      <div style="color: var(--muted); font-size: 12px; font-weight: 600;">Guias Visuais & Tipografia</div>
      <div class="kpi-val" id="kpi-guias" style="color: var(--success);">0</div>
    </div>
    <div class="kpi-card">
      <div style="color: var(--muted); font-size: 12px; font-weight: 600;">Plaquinhas 10x10 Prontas</div>
      <div class="kpi-val" id="kpi-placas" style="color: var(--purple);">0</div>
    </div>
    <div class="kpi-card">
      <div style="color: var(--muted); font-size: 12px; font-weight: 600;">Propostas Comerciais PDF</div>
      <div class="kpi-val" id="kpi-pdfs" style="color: var(--danger);">0</div>
    </div>
  </div>

  <div class="controls">
    <input type="text" id="searchInput" class="search-input" placeholder="Buscar por hotel, bairro ou categoria...">
    <select id="filterBairro" class="select-filter">
      <option value="">Todas as Regiões</option>
    </select>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Hotel / Empreendimento</th>
          <th>Região / Bairro</th>
          <th>Quartos</th>
          <th>Diária Média</th>
          <th>Site Oficial</th>
          <th>Guia Visual</th>
          <th>Entregáveis & Ações</th>
        </tr>
      </thead>
      <tbody id="tableBody">
      </tbody>
    </table>
  </div>

  <script>
    const data = {data_json};

    document.getElementById('kpi-total').innerText = data.length;
    document.getElementById('kpi-guias').innerText = data.filter(d => d.tem_guia).length;
    document.getElementById('kpi-placas').innerText = data.filter(d => d.tem_placa).length;
    document.getElementById('kpi-pdfs').innerText = data.filter(d => d.tem_pdf).length;

    const bairros = [...new Set(data.map(d => d.bairro).filter(Boolean))].sort();
    const filterSelect = document.getElementById('filterBairro');
    bairros.forEach(b => {{
      const opt = document.createElement('option');
      opt.value = b;
      opt.innerText = b;
      filterSelect.appendChild(opt);
    }});

    function render(items) {{
      const tb = document.getElementById('tableBody');
      tb.innerHTML = '';
      items.forEach(h => {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-family: 'JetBrains Mono'; font-weight: 700; color: ${{h.ranking <= 10 ? '#f59e0b' : '#94a3b8'}};">#${{h.ranking}}</td>
          <td>
            <div style="font-weight: 700; color: #fff;">${{h.nome}}</div>
            <div style="font-size: 11px; color: var(--muted);">${{h.categoria || ''}} - ${{h.unidade || ''}}</div>
          </td>
          <td>${{h.bairro}}</td>
          <td style="font-weight: 700; font-family: 'JetBrains Mono';">${{h.quartos ? h.quartos.toLocaleString('pt-BR') : '-'}}</td>
          <td style="font-weight: 700; color: #34d399; font-family: 'JetBrains Mono';">${{h.diaria ? 'R$ ' + h.diaria.toLocaleString('pt-BR', {{minimumFractionDigits: 2}}) : '-'}}</td>
          <td>
            ${{h.site && h.site.startsWith('http') ? `<a href="${{h.site}}" target="_blank" class="site-badge">🌐 ${{h.site.replace('https://','').replace('http://','').replace('www.','').split('/')[0]}}</a>` : '<span style="color:#64748b;">Sem site</span>'}}
          </td>
          <td>
            ${{h.tem_guia ? '<span class="tag-done">✓ Pronto</span>' : '<span class="tag-pending">Pendente</span>'}}
          </td>
          <td>
            <div class="btn-group">
              ${{h.guia_path ? `<a href="${{h.guia_path}}" target="_blank" class="btn-action" title="Abrir Guia de Identidade Visual">🎨 Guia</a>` : ''}}
              ${{h.tem_placa ? `<a href="${{h.placa_path}}" target="_blank" class="btn-action btn-placa" title="Ver Plaquinha NFC 10x10">🏷️ Plaquinha</a>` : `<span class="btn-action btn-placa btn-disabled" title="Plaquinha não gerada">🏷️ Plaquinha</span>`}}
              ${{h.tem_pdf ? `<a href="${{h.pdf_path}}" target="_blank" class="btn-action btn-pdf" title="Abrir Proposta Comercial em PDF">📄 PDF Final</a>` : `<span class="btn-action btn-pdf btn-disabled" title="PDF não gerado">📄 PDF Final</span>`}}
            </div>
          </td>
        `;
        tb.appendChild(tr);
      }});
    }}

    render(data);

    function applyFilters() {{
      const q = document.getElementById('searchInput').value.toLowerCase();
      const b = filterSelect.value;
      const filtered = data.filter(d => {{
        const mQ = !q || d.nome.toLowerCase().includes(q) || d.bairro.toLowerCase().includes(q) || (d.categoria && d.categoria.toLowerCase().includes(q));
        const mB = !b || d.bairro === b;
        return mQ && mB;
      }});
      render(filtered);
    }}

    document.getElementById('searchInput').addEventListener('input', applyFilters);
    filterSelect.addEventListener('change', applyFilters);
  </script>
</body>
</html>
"""

with open(r"C:\Users\Augusto\Desktop\AH3\painel_controle.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Painel atualizado com novos botões de Plaquinha e PDF Final em C:\\Users\\Augusto\\Desktop\\AH3\\painel_controle.html")

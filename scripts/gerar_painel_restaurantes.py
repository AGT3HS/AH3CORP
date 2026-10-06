import json
import os
import csv

INPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_enriquecido.json"
CSV_FILE = "BigBrain/handoff/restaurantes_norte_da_ilha.csv"
HTML_FILE = "painel_controle.html"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ordenar por Bairro e depois por Nota decrescente
data = sorted(data, key=lambda x: (x.get("bairro", ""), -float(x.get("nota", 0)), -int(x.get("avaliacoes", 0))))

# 1. Salvar CSV
fields = [
    "nome", "bairro", "categoria", "nota", "avaliacoes", "faixa_preco",
    "status", "endereco", "telefone", "whatsapp", "site", "instagram",
    "ifood", "maps_url", "possivel_rede"
]

with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"CSV salvo em: {CSV_FILE}")

# 2. Gerar Painel HTML Oficial (painel_controle.html)
json_str = json.dumps(data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AH3 · Painel de Prospecção de Restaurantes (Norte da Ilha)</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: rgba(18, 24, 38, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent: #FF5A1F;
      --accent-glow: rgba(255, 90, 31, 0.25);
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --success: #10B981;
      --warning: #F59E0B;
      --danger: #EF4444;
      --ig-pink: #E1306C;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 24px;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(255, 90, 31, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.04) 0%, transparent 40%);
    }}

    .container {{
      max-width: 1600px;
      margin: 0 auto;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
      flex-wrap: wrap;
      gap: 16px;
    }}

    .brand-title {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .badge-ah3 {{
      background: var(--accent);
      color: #fff;
      font-weight: 800;
      font-size: 13px;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }}

    h1 {{
      font-size: 22px;
      font-weight: 700;
      color: #fff;
    }}

    .stats-bar {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .stat-pill {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 13px;
    }}

    .stat-pill strong {{
      color: var(--accent);
      font-size: 15px;
    }}

    /* Filtros e Controles */
    .controls-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 14px;
      margin-bottom: 20px;
      background: var(--card-bg);
      padding: 18px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      backdrop-filter: blur(8px);
    }}

    .form-group label {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}

    .form-control {{
      width: 100%;
      background: #0f1422;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 10px 12px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
      transition: all 0.2s;
    }}

    .form-control:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-glow);
    }}

    .btn-export {{
      background: linear-gradient(135deg, var(--accent) 0%, #e04812 100%);
      color: #fff;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.2s;
      height: 40px;
      margin-top: auto;
    }}

    .btn-export:hover {{
      opacity: 0.9;
    }}

    /* Tabela */
    .table-container {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow-x: auto;
      backdrop-filter: blur(8px);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    th {{
      background: rgba(15, 20, 34, 0.95);
      padding: 14px 16px;
      font-weight: 600;
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
      white-space: nowrap;
    }}

    td {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--card-border);
      color: var(--text);
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    .badge {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }}

    .badge-bairro {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .badge-cat {{ background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }}
    .badge-status-open {{ background: rgba(16, 185, 129, 0.15); color: #34D399; }}
    .badge-status-temp {{ background: rgba(245, 158, 11, 0.15); color: #FBBF24; }}
    .badge-rede {{ background: rgba(239, 68, 68, 0.15); color: #F87171; }}

    .rating-box {{
      display: flex;
      align-items: center;
      gap: 4px;
      font-weight: 700;
      color: #FBBF24;
    }}

    .btn-action {{
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-right: 4px;
      transition: transform 0.1s;
    }}

    .btn-action:hover {{
      transform: translateY(-1px);
    }}

    .btn-ig {{
      background: rgba(225, 48, 108, 0.15);
      color: #ff5b94;
      border: 1px solid rgba(225, 48, 108, 0.4);
    }}

    .btn-wa {{
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }}

    .btn-maps {{
      background: rgba(255, 255, 255, 0.08);
      color: #CBD5E1;
      border: 1px solid var(--card-border);
    }}

    .btn-disabled {{
      opacity: 0.3;
      pointer-events: none;
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      border: 1px solid transparent;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand-title">
        <span class="badge-ah3">AH3 OPS</span>
        <div>
          <h1>Painel de Prospecção · Restaurantes Florianópolis</h1>
          <p style="font-size: 13px; color: var(--text-muted);">Varredura de SEO Local & Oportunidades Comerciais (Ponta das Canas, Canasvieiras e Jurerê)</p>
        </div>
      </div>
      <div class="stats-bar">
        <div class="stat-pill">Total Auditado: <strong id="total-count">0</strong></div>
        <div class="stat-pill">Com Instagram: <strong id="ig-count">0</strong></div>
        <div class="stat-pill">Com WhatsApp Direto: <strong id="wa-count">0</strong></div>
      </div>
    </header>

    <div class="controls-grid">
      <div class="form-group">
        <label>Buscar por Nome / Endereço</label>
        <input type="text" id="search-input" class="form-control" placeholder="Digite para filtrar...">
      </div>
      <div class="form-group">
        <label>Bairro</label>
        <select id="bairro-filter" class="form-control">
          <option value="">Todos os Bairros</option>
          <option value="Canasvieiras">Canasvieiras</option>
          <option value="Jurerê">Jurerê / Tradicional</option>
          <option value="Jurerê Internacional">Jurerê Internacional</option>
          <option value="Ponta das Canas">Ponta das Canas</option>
        </select>
      </div>
      <div class="form-group">
        <label>Categoria de Culinária</label>
        <select id="cat-filter" class="form-control">
          <option value="">Todas as Categorias</option>
          <option value="Japonesa">Japonesa / Sushi</option>
          <option value="Italiana">Italiana / Massas</option>
          <option value="Frutos do Mar">Frutos do Mar</option>
          <option value="Pizzaria">Pizzaria</option>
          <option value="Hamburgueria">Hamburgueria</option>
          <option value="Brasileira">Brasileira</option>
          <option value="Bar">Bar / Choperia</option>
          <option value="Café">Café / Bistrô</option>
          <option value="Padaria">Padaria</option>
        </select>
      </div>
      <div class="form-group">
        <label>Nota Mínima</label>
        <select id="rating-filter" class="form-control">
          <option value="0">Todas as notas</option>
          <option value="4.0">≥ 4.0 ⭐</option>
          <option value="4.5">≥ 4.5 ⭐</option>
          <option value="4.8">≥ 4.8 ⭐</option>
        </select>
      </div>
      <div class="form-group">
        <label>Ações Rápidas</label>
        <button class="btn-export" onclick="exportCSV()">📥 Exportar Lista (CSV)</button>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Restaurante</th>
            <th>Bairro</th>
            <th>Categoria</th>
            <th>Avaliação</th>
            <th>Preço</th>
            <th>Status</th>
            <th>Ações Rápidas (Auditoria & Contato)</th>
          </tr>
        </thead>
        <tbody id="table-body">
        </tbody>
      </table>
    </div>
  </div>

  <script>
    const data = {json_str};

    function renderTable() {{
      const search = document.getElementById('search-input').value.toLowerCase();
      const bairro = document.getElementById('bairro-filter').value;
      const cat = document.getElementById('cat-filter').value;
      const minRating = parseFloat(document.getElementById('rating-filter').value) || 0;

      const filtered = data.filter(item => {{
        const matchSearch = item.nome.toLowerCase().includes(search) || item.endereco.toLowerCase().includes(search);
        const matchBairro = !bairro || item.bairro.includes(bairro);
        const matchCat = !cat || item.categoria.includes(cat);
        const matchRating = (parseFloat(item.nota) || 0) >= minRating;
        return matchSearch && matchBairro && matchCat && matchRating;
      }});

      document.getElementById('total-count').textContent = filtered.length;
      document.getElementById('ig-count').textContent = filtered.filter(i => i.instagram !== 'não encontrado').length;
      document.getElementById('wa-count').textContent = filtered.filter(i => i.whatsapp.startsWith('http')).length;

      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      filtered.forEach(item => {{
        const tr = document.createElement('tr');

        const igBtn = item.instagram !== 'não encontrado' 
          ? `<a href="${{item.instagram}}" target="_blank" class="btn-action btn-ig">📸 Instagram</a>` 
          : `<span class="btn-action btn-disabled">📸 Sem IG</span>`;

        const waBtn = item.whatsapp.startsWith('http')
          ? `<a href="${{item.whatsapp}}" target="_blank" class="btn-action btn-wa">💬 WhatsApp</a>`
          : `<span class="btn-action btn-disabled">💬 Sem WA</span>`;

        const mapsBtn = `<a href="${{item.maps_url}}" target="_blank" class="btn-action btn-maps">📍 Maps</a>`;

        const statusBadge = item.status === 'aberto' 
          ? `<span class="badge badge-status-open">Aberto</span>` 
          : `<span class="badge badge-status-temp">Temp. Fechado</span>`;

        const redeBadge = item.possivel_rede ? ` <span class="badge badge-rede">Possível Rede</span>` : '';

        tr.innerHTML = `
          <td>
            <strong>${{item.nome}}</strong>${{redeBadge}}
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 3px;">${{item.endereco}}</div>
          </td>
          <td><span class="badge badge-bairro">${{item.bairro}}</span></td>
          <td><span class="badge badge-cat">${{item.categoria}}</span></td>
          <td>
            <div class="rating-box">⭐ ${{item.nota}} <span style="font-size: 11px; color: var(--text-muted); font-weight: normal;">(${{item.avaliacoes}})</span></div>
          </td>
          <td style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #CBD5E1;">${{item.faixa_preco}}</td>
          <td>${{statusBadge}}</td>
          <td>
            ${{igBtn}}
            ${{waBtn}}
            ${{mapsBtn}}
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function exportCSV() {{
      const headers = ["Nome", "Bairro", "Categoria", "Nota", "Avaliacoes", "Faixa_Preco", "Status", "Endereco", "Telefone", "WhatsApp", "Site", "Instagram", "iFood", "Google_Maps_URL"];
      const rows = data.map(item => [
        `"${{item.nome.replace(/"/g, '""')}}"`,
        `"${{item.bairro}}"`,
        `"${{item.categoria}}"`,
        item.nota,
        item.avaliacoes,
        `"${{item.faixa_preco}}"`,
        `"${{item.status}}"`,
        `"${{item.endereco.replace(/"/g, '""')}}"`,
        `"${{item.telefone}}"`,
        `"${{item.whatsapp}}"`,
        `"${{item.site}}"`,
        `"${{item.instagram}}"`,
        `"${{item.ifood}}"`,
        `"${{item.maps_url}}"`
      ]);

      const csvContent = "data:text/csv;charset=utf-8,\uFEFF" + [headers.join(","), ...rows.map(e => e.join(","))].join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "prospeccao_restaurantes_ah3.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    document.getElementById('search-input').addEventListener('input', renderTable);
    document.getElementById('bairro-filter').addEventListener('change', renderTable);
    document.getElementById('cat-filter').addEventListener('change', renderTable);
    document.getElementById('rating-filter').addEventListener('change', renderTable);

    renderTable();
  </script>
</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Painel oficial gerado com sucesso em: {HTML_FILE}")

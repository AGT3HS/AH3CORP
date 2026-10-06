import openpyxl, json, glob, os, re, unicodedata

wb_path = 'C:/Users/Augusto/Desktop/AH3/Top_150_Hoteis_Florianopolis_Ranking.xlsx'
wb = openpyxl.load_workbook(wb_path, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

guias_files = {}
for d in ['C:/Users/Augusto/Desktop/AH3/guias_identidade_visual', 'C:/Users/Augusto/Desktop/AH3/guias_50_hoteis_famosos']:
    for f in glob.glob(os.path.join(d, '*.html')):
        guias_files[os.path.basename(f)] = f.replace('\\', '/')

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

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

    placa_file = None
    placas = glob.glob('C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10/*.svg')
    for p in placas:
        norm_p = normalize(os.path.basename(p))
        if norm_nome[:6] in norm_p:
            placa_file = p.replace('\\', '/')
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
        'tem_placa': bool(placa_file),
        'placa_path': placa_file or '',
        'status_venda': venda_status,
        'valor': valor
    })

data_json = json.dumps(data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Painel de Controle — Top 150 Hotéis Floripa (AH3)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
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
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  padding: 24px;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}
.header h1 { font-size: 24px; font-weight: 800; color: #fff; }
.header p { color: var(--muted); font-size: 14px; margin-top: 4px; }
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--card);
  border: 1px solid var(--border);
  padding: 18px;
  border-radius: 12px;
}
.stat-card span { font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
.stat-card strong { font-size: 26px; color: #fff; display: block; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }

.controls {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
.search-box {
  flex: 1;
  background: var(--card);
  border: 1px solid var(--border);
  padding: 12px 16px;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  outline: none;
}
.search-box:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }

.table-wrapper {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 14px;
}
th {
  background: #0f1722;
  padding: 14px 16px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  border-bottom: 1px solid var(--border);
}
td {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
tr:hover { background: rgba(255,255,255,0.02); }
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
.badge-ready {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.badge-ready:hover {
  background: var(--success);
  color: #fff;
}
.badge-pending {
  background: rgba(148, 163, 184, 0.1);
  color: var(--muted);
  border: 1px solid rgba(148, 163, 184, 0.2);
  cursor: default;
}
.badge-warning {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
.hotel-name { font-weight: 700; color: #fff; }
.hotel-meta { font-size: 12px; color: var(--muted); margin-top: 2px; }

/* Modal Drawer */
.modal {
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.85);
  backdrop-filter: blur(8px);
  z-index: 9999;
  justify-content: center;
  align-items: center;
}
.modal.active { display: flex; }
.modal-content {
  width: 92vw;
  height: 92vh;
  background: #0f172a;
  border: 1px solid var(--border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.modal-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: #1e293b;
  border-bottom: 1px solid var(--border);
}
.modal-bar h3 { font-size: 16px; color: #fff; }
.modal-close {
  background: #ef4444;
  color: #fff;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
}
.modal-iframe {
  flex: 1;
  width: 100%;
  border: none;
  background: #fff;
}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Top 150 Hotéis Florianópolis — Painel Interativo AH3</h1>
    <p>Visualização instantânea de Identidade Visual, Plaquinhas 10x10 e Status Operacional</p>
  </div>
</div>

<div class="stats" id="stats-container"></div>

<div class="controls">
  <input type="text" id="search" class="search-box" placeholder="Filtrar por nome do hotel, bairro, categoria..." onkeyup="renderTable()">
</div>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th style="width: 50px;">#</th>
        <th>Hotel / Empreendimento</th>
        <th>Bairro</th>
        <th>Quartos</th>
        <th>Diária Média</th>
        <th>Identidade Visual</th>
        <th>Plaquinha 10x10</th>
        <th>Status Venda</th>
      </tr>
    </thead>
    <tbody id="table-body"></tbody>
  </table>
</div>

<div id="modal" class="modal">
  <div class="modal-content">
    <div class="modal-bar">
      <h3 id="modal-title">Visualização</h3>
      <button class="modal-close" onclick="fecharModal()">✕ Fechar</button>
    </div>
    <iframe id="modal-frame" class="modal-iframe" src=""></iframe>
  </div>
</div>

<script>
const hotels = """ + data_json + """;

function renderStats() {
  const total = hotels.length;
  const ivProntas = hotels.filter(h => h.tem_guia).length;
  const totalQuartos = hotels.reduce((acc, h) => acc + (parseInt(h.quartos) || 0), 0);
  
  document.getElementById('stats-container').innerHTML = `
    <div class="stat-card">
      <span>Total de Hotéis</span>
      <strong>${total}</strong>
    </div>
    <div class="stat-card">
      <span>Identidades Prontas</span>
      <strong style="color: #34d399;">${ivProntas}</strong>
    </div>
    <div class="stat-card">
      <span>Capacidade Total</span>
      <strong>${totalQuartos} quartos</strong>
    </div>
  `;
}

function renderTable() {
  const query = document.getElementById('search').value.toLowerCase();
  const tbody = document.getElementById('table-body');
  
  const filtered = hotels.filter(h => {
    return h.nome.toLowerCase().includes(query) || 
           h.bairro.toLowerCase().includes(query) || 
           h.categoria.toLowerCase().includes(query);
  });
  
  tbody.innerHTML = filtered.map(h => {
    const btnIv = h.tem_guia 
      ? `<button class="badge badge-ready" onclick="abrirModal('${h.guia_path}', '${h.nome} — Guia de Identidade')">👁️ Ver Guia</button>`
      : `<span class="badge badge-pending">Pendente</span>`;
      
    const btnPlaca = h.tem_placa 
      ? `<button class="badge badge-ready" onclick="abrirModal('${h.placa_path}', '${h.nome} — Plaquinha 10x10')">📐 Ver Placa</button>`
      : `<span class="badge badge-pending">Pendente</span>`;
      
    return `
      <tr>
        <td style="font-family: 'JetBrains Mono'; color: var(--muted);">${h.ranking}</td>
        <td>
          <div class="hotel-name">${h.nome}</div>
          <div class="hotel-meta">${h.categoria} ${h.site ? `• <a href="${h.site}" target="_blank" style="color: var(--accent); text-decoration: none;">Site Oficial ↗</a>` : ''}</div>
        </td>
        <td>${h.bairro}</td>
        <td style="font-family: 'JetBrains Mono'; font-weight: 600;">${h.quartos}</td>
        <td style="font-family: 'JetBrains Mono';">R$ ${h.diaria}</td>
        <td>${btnIv}</td>
        <td>${btnPlaca}</td>
        <td><span class="badge badge-warning">${h.status_venda}</span></td>
      </tr>
    `;
  }).join('');
}

function abrirModal(path, title) {
  document.getElementById('modal-title').innerText = title;
  document.getElementById('modal-frame').src = path;
  document.getElementById('modal').classList.add('active');
}

function fecharModal() {
  document.getElementById('modal').classList.remove('active');
  document.getElementById('modal-frame').src = '';
}

renderStats();
renderTable();
</script>
</body>
</html>
"""

with open('C:/Users/Augusto/Desktop/AH3/painel_controle.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('PAINEL_GERADO_COM_SUCESSO')

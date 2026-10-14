#!/usr/bin/env python3
"""
AH3 — Gerador Central do Painel de Controle Oficial (painel_controle.html)
Agente Encarregado: @Maestro
Visualização Direta e Integrada:
1. Identidade Visual (Guias de marca interativos completos em modal/drawer ou embutidos)
2. Plaquinhas NFC 100x100mm (Renderização visual em cards com preview de arte, modelos clássico, noturno, acento e autoridade)
3. Propostas Comerciais & Auditorias (Visualizador interativo de slides/páginas em alta definição direto no navegador)
4. Funil CRM & Disparo WhatsApp com status integrado
5. Mapeamento Top 150 Hotéis com filtros e ativos vinculados
6. Diário de Bordo (Ledger) e Playbook de Objeções
"""

import os
import sys
import glob
import json
import csv
import re
import unicodedata
import openpyxl

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
LEADS_CSV = os.path.join(ROOT_DIR, "BigBrain/funil/leads.csv")
XLSX_PATH = os.path.join(ROOT_DIR, "Auditoria_Hotelaria_Florianopolis.xlsx")
HANDOFF_DIR = os.path.join(ROOT_DIR, "BigBrain/handoff")
LEDGER_DIR = os.path.join(ROOT_DIR, "BigBrain/ledger")
OUTPUT_HTML = os.path.join(ROOT_DIR, "painel_controle.html")

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

# 1. Carregar Dados de Leads (CRM)
leads = []
if os.path.exists(LEADS_CSV):
    with open(LEADS_CSV, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get('nome', '')
            slug = normalize(nome)
            
            # Placas
            placas_lead = []
            placa_files = glob.glob(f"{ROOT_DIR}/BigBrain/handoff/*{slug}*.svg") + glob.glob(f"{ROOT_DIR}/saida/placas_nfc/*{slug}*.svg")
            for pf in placa_files:
                png = pf.replace('.svg', '.png')
                placas_lead.append({
                    'nome': os.path.basename(pf),
                    'svg': os.path.relpath(pf, ROOT_DIR).replace('\\', '/'),
                    'png': os.path.relpath(png, ROOT_DIR).replace('\\', '/') if os.path.exists(png) else os.path.relpath(pf, ROOT_DIR).replace('\\', '/')
                })
            
            # Propostas
            props_lead = []
            prop_files = glob.glob(f"{ROOT_DIR}/BigBrain/handoff/*{slug}*.pdf") + glob.glob(f"{ROOT_DIR}/saida/*{slug}*.pdf")
            for prf in prop_files:
                base = os.path.splitext(os.path.basename(prf))[0]
                slides = sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/{base}/*.png"))
                props_lead.append({
                    'nome': os.path.basename(prf),
                    'pdf': os.path.relpath(prf, ROOT_DIR).replace('\\', '/'),
                    'slides': [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in slides]
                })

            row['placas'] = placas_lead
            row['propostas'] = props_lead
            leads.append(row)

# 2. Carregar Dados do Excel (Top 150 Hotéis) com Vinculação de Ativos
hoteis_data = []
if os.path.exists(XLSX_PATH):
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    for r in rows[1:]:
        if not r or not r[1]: continue
        ranking = int(r[0])
        nome = r[1]
        unidade = r[2] or ''
        cat = r[3] or 'Hotel'
        bairro = r[4] or 'Florianópolis'
        quartos = r[5] or 0
        diaria = r[6] or 0
        site = r[7] or ''
        status_venda = r[11] or 'Não Iniciado'
        valor = r[12] or 0

        # 1. Guia Identidade Visual
        guia_html = None
        guia_paths = glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking:02d}_*/identidade/*.html") or \
                     glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking}_*/identidade/*.html") or \
                     glob.glob(f"{ROOT_DIR}/BigBrain/handoff/guias_identidade_visual/{ranking:02d}_*.html") or \
                     glob.glob(f"{ROOT_DIR}/BigBrain/handoff/guias_identidade_visual/{ranking}_*.html")
        if guia_paths:
            guia_html = os.path.relpath(guia_paths[0], ROOT_DIR).replace('\\', '/')

        # 2. Placas NFC
        placas = []
        placa_paths = sorted(glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking:02d}_*/placas_nfc/*.svg") or \
                             glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking}_*/placas_nfc/*.svg"))
        for p in placa_paths:
            png = p.replace('.svg', '.png')
            placas.append({
                'nome': os.path.basename(p),
                'svg': os.path.relpath(p, ROOT_DIR).replace('\\', '/'),
                'png': os.path.relpath(png, ROOT_DIR).replace('\\', '/') if os.path.exists(png) else os.path.relpath(p, ROOT_DIR).replace('\\', '/')
            })

        # 3. Propostas
        propostas = []
        prop_paths = sorted(glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking:02d}_*/propostas/*.pdf") or \
                            glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking}_*/propostas/*.pdf"))
        if ranking == 1:
            c1 = glob.glob(f"{ROOT_DIR}/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf")
            prop_paths.extend(c1)

        for pr in prop_paths:
            base_name = os.path.splitext(os.path.basename(pr))[0]
            slides = sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/{base_name}/*.png"))
            if not slides and ranking == 2:
                slides = sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/proposta_jurere/*.png"))
            slides_rel = [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in slides]
            
            propostas.append({
                'nome': os.path.basename(pr),
                'pdf': os.path.relpath(pr, ROOT_DIR).replace('\\', '/'),
                'slides': slides_rel
            })

        if ranking == 2 and propostas and not propostas[0]['slides']:
            propostas[0]['slides'] = [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/proposta_jurere/*.png"))]

        hoteis_data.append({
            'ranking': ranking,
            'nome': nome,
            'unidade': unidade,
            'categoria': cat,
            'bairro': bairro,
            'quartos': quartos,
            'diaria': diaria,
            'site': site,
            'tem_guia': bool(guia_html),
            'guia_path': guia_html,
            'tem_placa': len(placas) > 0,
            'placas': placas,
            'tem_proposta': len(propostas) > 0,
            'propostas': propostas,
            'status_venda': status_venda,
            'valor': valor
        })

# 3. Carregar Entregáveis de Handoff
handoff_items = []
if os.path.exists(HANDOFF_DIR):
    for f in sorted(os.listdir(HANDOFF_DIR)):
        fpath = os.path.join(HANDOFF_DIR, f)
        if os.path.isfile(fpath):
            ext = os.path.splitext(f)[1].lower()
            base = os.path.splitext(f)[0]
            slides = []
            if ext == '.pdf':
                slides = [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/{base}/*.png"))]

            handoff_items.append({
                'nome': f,
                'tipo': ext.replace('.', '').upper(),
                'tamanho_kb': round(os.path.getsize(fpath) / 1024, 1),
                'path': os.path.relpath(fpath, ROOT_DIR).replace('\\', '/'),
                'slides': slides,
                'is_image': ext in ['.png', '.jpg', '.jpeg', '.svg']
            })

# 4. Carregar Ledger Recente
ledger_entries = []
if os.path.exists(LEDGER_DIR):
    ledger_files = sorted(glob.glob(os.path.join(LEDGER_DIR, "*.md")), reverse=True)
    for lf in ledger_files[:4]:
        fname = os.path.basename(lf)
        with open(lf, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith('-'):
                    ledger_entries.append({'data': fname.replace('.md', ''), 'texto': line.strip().lstrip('- ')})

# Estatísticas Gerais
total_leads = len(leads)
leads_auditados = len([l for l in leads if l.get('status') == 'auditado'])
leads_abordados = len([l for l in leads if l.get('status') in ['abordado', 'respondeu', 'proposta_enviada', 'fechado']])
total_hoteis_mapeados = len(hoteis_data)
total_guias_prontos = sum(1 for h in hoteis_data if h['tem_guia'])
total_placas_geradas = sum(len(h['placas']) for h in hoteis_data)

leads_json = json.dumps(leads, ensure_ascii=False)
hoteis_json = json.dumps(hoteis_data, ensure_ascii=False)
handoff_json = json.dumps(handoff_items, ensure_ascii=False)
ledger_json = json.dumps(ledger_entries[:25], ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AH3 Command Center — Painel de Controle Operacional</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #090d16;
  --card: #111827;
  --card-hover: #1f2937;
  --border: #1f293d;
  --border-light: #2d3748;
  --text: #f3f4f6;
  --muted: #9ca3af;
  --accent: #f97316;
  --accent-glow: rgba(249, 115, 22, 0.25);
  --success: #10b981;
  --danger: #ef4444;
  --warning: #f59e0b;
  --info: #38bdf8;
  --purple: #a855f7;
  --whatsapp: #25D366;
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
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 20px;
}}
.title-block h1 {{
  font-size: 26px;
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
  border-radius: 20px;
  font-weight: 700;
  border: 1px solid #059669;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* KPI CARDS */
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}}
.kpi-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: transform 0.2s, border-color 0.2s;
}}
.kpi-card:hover {{
  transform: translateY(-2px);
  border-color: var(--accent);
}}
.kpi-label {{
  font-size: 11px;
  color: var(--muted);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.kpi-value {{
  font-size: 24px;
  font-weight: 800;
  color: #fff;
}}

/* NAV TABS */
.nav-tabs {{
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 12px;
  overflow-x: auto;
}}
.tab-btn {{
  background: #111827;
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}}
.tab-btn:hover, .tab-btn.active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  box-shadow: 0 4px 12px var(--accent-glow);
}}
.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

/* SEARCH & FILTERS */
.filter-bar {{
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}}
.search-input {{
  background: #0d131f;
  border: 1px solid var(--border);
  color: #fff;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-family: inherit;
  flex: 1;
  min-width: 250px;
}}
.search-input:focus {{
  outline: none;
  border-color: var(--accent);
}}
.select-filter {{
  background: #0d131f;
  border: 1px solid var(--border);
  color: #fff;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
}}

/* KANBAN CRM */
.kanban-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  overflow-x: auto;
  align-items: start;
}}
.kanban-col {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  min-height: 520px;
}}
.kanban-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-weight: 700;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}}
.lead-card {{
  background: #0d131f;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
  transition: transform 0.2s, border-color 0.2s;
}}
.lead-card:hover {{
  transform: translateY(-2px);
  border-color: var(--accent);
}}
.lead-title {{ font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 4px; }}
.lead-meta {{ font-size: 12px; color: var(--muted); margin-bottom: 8px; }}
.lead-actions {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}}
.btn-wa {{
  background: #064e3b;
  color: #34d399;
  border: 1px solid #059669;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: background 0.2s;
}}
.btn-wa:hover {{
  background: #059669;
  color: #fff;
}}
.btn-action {{
  background: #1e293b;
  color: #cbd5e1;
  border: 1px solid var(--border);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}}
.btn-action:hover {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}

/* TABLES */
.table-container {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}
th, td {{
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}}
th {{
  background: #0d131f;
  color: var(--muted);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.05em;
}}
tr:hover td {{ background: var(--card-hover); }}

/* BUTTONS & BADGES */
.btn {{
  background: var(--accent);
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: opacity 0.2s;
}}
.btn:hover {{ opacity: 0.9; }}
.badge {{
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}}
.badge-success {{ background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); }}
.badge-warning {{ background: rgba(245, 158, 11, 0.2); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); }}
.badge-info {{ background: rgba(56, 189, 248, 0.2); color: var(--info); border: 1px solid rgba(56, 189, 248, 0.3); }}
.badge-purple {{ background: rgba(168, 85, 247, 0.2); color: var(--purple); border: 1px solid rgba(168, 85, 247, 0.3); }}

/* MODAL / VIEWER */
.modal-overlay {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: none;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
}}
.modal-overlay.active {{ display: flex; }}
.modal-window {{
  background: #111827;
  border: 1px solid var(--border-light);
  border-radius: 16px;
  width: 95vw;
  max-width: 1200px;
  height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  overflow: hidden;
}}
.modal-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: #0d131f;
}}
.modal-title {{
  font-size: 18px;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 10px;
}}
.modal-close {{
  background: #1e293b;
  color: #fff;
  border: 1px solid var(--border);
  border-radius: 8px;
  width: 32px;
  height: 32px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.modal-close:hover {{
  background: var(--danger);
}}
.modal-body {{
  flex: 1;
  overflow: auto;
  padding: 24px;
  background: #090d16;
}}
.modal-iframe {{
  width: 100%;
  height: 100%;
  border: none;
  background: #fff;
  border-radius: 8px;
}}

/* PLACAS & PROPOSTAS GRIDS DENTRO DO MODAL OU TAB */
.placas-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}}
.placa-card {{
  background: #111827;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: transform 0.2s, border-color 0.2s;
}}
.placa-card:hover {{
  transform: translateY(-4px);
  border-color: var(--accent);
}}
.placa-preview {{
  width: 200px;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  background: #1e293b;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
}}
.placa-preview img {{
  width: 100%;
  height: 100%;
  object-fit: contain;
}}
.placa-title {{
  font-size: 12px;
  font-weight: 700;
  color: #cbd5e1;
  text-align: center;
}}

/* SLIDES VIEWER */
.slides-container {{
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}}
.slide-box {{
  background: #111827;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}}
.slide-box img {{
  width: 100%;
  display: block;
}}
.slide-header {{
  padding: 10px 16px;
  background: #0d131f;
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
}}

/* PLAYBOOK CARDS */
.playbook-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}}
.playbook-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}}
.playbook-card h3 {{
  color: var(--accent);
  font-size: 15px;
  font-weight: 700;
}}
.playbook-script {{
  background: #0d131f;
  border: 1px solid var(--border);
  padding: 14px;
  border-radius: 8px;
  font-size: 12px;
  color: #cbd5e1;
  line-height: 1.6;
  white-space: pre-wrap;
}}
</style>
</head>
<body>

<div class="header">
  <div class="title-block">
    <h1>AH3 Command Center <span class="badge-live">Live Matrix</span></h1>
    <p style="color: var(--muted); font-size: 13px; margin-top: 4px;">Orquestração Estratégica, CRM de Hospitalidade & Estação de Governança AH3</p>
  </div>
  <div>
    <button class="btn" onclick="alert('Para sincronizar os dados, execute no terminal:\\npython scripts/atualizar_painel_controle.py')">🔄 Sincronizar Base</button>
  </div>
</div>

<!-- KPI CARDS -->
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-label">Leads no Funil</span>
    <span class="kpi-value">{total_leads}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Auditados (Prontos)</span>
    <span class="kpi-value" style="color: var(--info);">{leads_auditados}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Abordados / Negociação</span>
    <span class="kpi-value" style="color: var(--warning);">{leads_abordados}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Top 150 Hotéis Floripa</span>
    <span class="kpi-value" style="color: var(--success);">{total_hoteis_mapeados}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Guias de Marca</span>
    <span class="kpi-value" style="color: var(--purple);">{total_guias_prontos}</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-label">Placas NFC 100x100</span>
    <span class="kpi-value" style="color: var(--accent);">{total_placas_geradas}</span>
  </div>
</div>

<div class="nav-tabs">
  <button class="tab-btn active" onclick="openTab('tab-kanban')">📊 1. Funil CRM & Disparo WhatsApp</button>
  <button class="tab-btn" onclick="openTab('tab-mercado')">🏢 2. Mapeamento Top 150 Hotéis & Ativos</button>
  <button class="tab-btn" onclick="openTab('tab-handoff')">🛡️ 3. Quality Station (Handoff)</button>
  <button class="tab-btn" onclick="openTab('tab-playbook')">💬 4. Playbook de Objeções (WhatsApp)</button>
  <button class="tab-btn" onclick="openTab('tab-proposta')">📑 5. Simulador de Propostas</button>
  <button class="tab-btn" onclick="openTab('tab-ledger')">⏱️ 6. Diário de Bordo (Ledger)</button>
</div>

<!-- 1. CRM KANBAN -->
<div id="tab-kanban" class="tab-content active">
  <div class="filter-bar">
    <input type="text" id="crm-search" class="search-input" placeholder="🔍 Buscar por nome do estabelecimento..." oninput="renderKanban()">
    <select id="crm-bairro-filter" class="select-filter" onchange="renderKanban()">
      <option value="">Todos os Bairros</option>
      <option value="Canasvieiras">Canasvieiras</option>
      <option value="Ponta das Canas">Ponta das Canas</option>
      <option value="Cachoeira do Bom Jesus">Cachoeira do Bom Jesus</option>
      <option value="Lagoinha">Praia da Lagoinha</option>
      <option value="Moema">Moema (Teste)</option>
    </select>
  </div>
  <div class="kanban-grid" id="kanban-board"></div>
</div>

<!-- 2. MAPEAMENTO TOP 150 HOTÉIS & ATIVOS DIRETOS -->
<div id="tab-mercado" class="tab-content">
  <div class="filter-bar">
    <input type="text" id="hotel-search" class="search-input" placeholder="🔍 Buscar hotel por nome, bairro ou categoria..." oninput="renderHoteis()">
    <select id="hotel-filtro-ativo" class="select-filter" onchange="renderHoteis()">
      <option value="">Todos os Estabelecimentos</option>
      <option value="com_proposta">Com Proposta Pronta</option>
      <option value="com_guia">Com Guia de Identidade Visual</option>
      <option value="com_placa">Com Placas NFC Geradas</option>
    </select>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Estabelecimento</th>
          <th>Bairro</th>
          <th>Quartos</th>
          <th>Diária</th>
          <th>Guia de Marca</th>
          <th>Placas NFC (10x10)</th>
          <th>Proposta Comercial</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody id="hoteis-tbody"></tbody>
    </table>
  </div>
</div>

<!-- 3. QUALITY STATION / HANDOFF -->
<div id="tab-handoff" class="tab-content">
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Entregável / Arquivo</th>
          <th>Tipo</th>
          <th>Tamanho</th>
          <th>Compliance Anti-Promessa</th>
          <th>Visualização Direta</th>
        </tr>
      </thead>
      <tbody id="handoff-tbody"></tbody>
    </table>
  </div>
</div>

<!-- 4. PLAYBOOK DE OBJEÇÕES -->
<div id="tab-playbook" class="tab-content">
  <div style="margin-bottom: 20px;">
    <h3>Playbook de Resposta Rápida a Objeções (WhatsApp)</h3>
    <p style="color: var(--muted); font-size: 13px; margin-top: 4px;">Cópias testadas em conformidade com as 8 Travas (sem palavras proibidas, diretas e com foco em processo).</p>
  </div>
  <div class="playbook-grid">
    <div class="playbook-card">
      <h3>1. Objeção: "Já temos agência / marketing"</h3>
      <div class="playbook-script" id="script-1">Perfeito! A maioria dos nossos clientes também já possui agência de redes sociais. O nosso trabalho é complementar e focado 100% no momento físico do cliente na mesa/quarto e na captura de avaliações no Google Maps através da Placa Inteligente NFC. 

Isso costuma alimentar a própria agência com depoimentos reais e novos clientes buscando no Maps. Se quiser, posso te mandar o PDF de 2 minutos mostrando como funciona.</div>
      <button class="btn btn-action" onclick="copyText('script-1')">📋 Copiar Resposta</button>
    </div>

    <div class="playbook-card">
      <h3>2. Objeção: "Quanto custa o serviço?"</h3>
      <div class="playbook-script" id="script-2">Trabalhamos com 3 formatos modulares para atender a necessidade exata do estabelecimento:

• Plano Essencial (R$ 1.850/mês): Otimização Google Meu Negócio + Placas NFC e Funil de Avaliações.
• Plano Crescimento (R$ 3.200/mês): Inclui Cardápio Digital responsivo e gestão ativa de respostas.
• Plano Domínio (R$ 5.400/mês): Com tráfego hiperlocal e benchmarking contínuo.

Montamos um diagnóstico prévio do perfil de vocês sem custo. Posso te encaminhar o PDF aqui?</div>
      <button class="btn btn-action" onclick="copyText('script-2')">📋 Copiar Resposta</button>
    </div>

    <div class="playbook-card">
      <h3>3. Objeção: "Estamos na entressafra / sem verba agora"</h3>
      <div class="playbook-script" id="script-3">Compreendo perfeitamente o momento da sazonalidade em Florianópolis! Justamente por isso, a maioria dos estabelecimentos aproveita este período para estruturar a reputação no Google e as placas NFC antes do pico da temporada, para que a casa já entre ranqueada no topo das buscas dos turistas.

Podemos deixar o diagnóstico e o planejamento alinhados para quando fizer mais sentido para vocês.</div>
      <button class="btn btn-action" onclick="copyText('script-3')">📋 Copiar Resposta</button>
    </div>

    <div class="playbook-card">
      <h3>4. Objeção: "Como funciona a Placa Inteligente NFC?"</h3>
      <div class="playbook-script" id="script-4">A placa é uma peça de mesa/balcão de 10x10cm com a identidade visual de vocês. O cliente apenas aproxima o celular (iPhone ou Android) e abre instantaneamente o canal que você escolher:

• Avaliações no Google (com filtro inteligente de satisfação)
• Cardápio Digital / Wi-Fi
• WhatsApp de Reservas

Zero necessidade de baixar aplicativo ou digitar link longo.</div>
      <button class="btn btn-action" onclick="copyText('script-4')">📋 Copiar Resposta</button>
    </div>
  </div>
</div>

<!-- 5. SIMULADOR DE PROPOSTAS -->
<div id="tab-proposta" class="tab-content">
  <div style="background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
    <h3 style="margin-bottom: 10px;">Estrutura Padrão de Propostas Modulares AH3 (9 Slides)</h3>
    <p style="color: var(--muted); font-size: 13px;">Formatada com tokens de design profissionais, ancoragem tripla e entregáveis operacionais.</p>
  </div>
  <div class="playbook-grid">
    <div class="playbook-card">
      <h3>Plano Essencial</h3>
      <div style="font-size: 26px; font-weight: 800; color: #fff;">R$ 1.850<span style="font-size: 13px; color: var(--muted);">/mês</span></div>
      <ul style="margin-left: 20px; font-size: 13px; color: var(--muted); line-height: 1.8;">
        <li>Otimização Google Meu Negócio</li>
        <li>2 Placas Inteligentes NFC 100x100mm</li>
        <li>Funil de Avaliações Direto no Google</li>
        <li>Relatório Mensal de Performance</li>
      </ul>
    </div>
    <div class="playbook-card" style="border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow);">
      <div class="badge badge-warning" style="align-self: flex-start;">Recomendado</div>
      <h3>Plano Crescimento</h3>
      <div style="font-size: 26px; font-weight: 800; color: #fff;">R$ 3.200<span style="font-size: 13px; color: var(--muted);">/mês</span></div>
      <ul style="margin-left: 20px; font-size: 13px; color: var(--muted); line-height: 1.8;">
        <li>Tudo do Plano Essencial</li>
        <li>5 Placas Inteligentes NFC 100x100mm</li>
        <li>Cardápio Digital Responsivo & Room Service</li>
        <li>Gestão Ativa de Respostas no Google</li>
        <li>Linha Editorial de Conteúdo Local</li>
      </ul>
    </div>
    <div class="playbook-card">
      <h3>Plano Domínio</h3>
      <div style="font-size: 26px; font-weight: 800; color: #fff;">R$ 5.400<span style="font-size: 13px; color: var(--muted);">/mês</span></div>
      <ul style="margin-left: 20px; font-size: 13px; color: var(--muted); line-height: 1.8;">
        <li>Tudo do Plano Crescimento</li>
        <li>10 Placas Inteligentes NFC 100x100mm</li>
        <li>Tráfego Pago Hiperlocal (Planejamento)</li>
        <li>Benchmarking Competitivo Contínuo</li>
        <li>Suporte Prioritário Direto</li>
      </ul>
    </div>
  </div>
</div>

<!-- 6. DIÁRIO DE BORDO (LEDGER) -->
<div id="tab-ledger" class="tab-content">
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Data</th>
          <th>Evento / Decisão Operacional (@Maestro)</th>
        </tr>
      </thead>
      <tbody id="ledger-tbody"></tbody>
    </table>
  </div>
</div>

<!-- MODAL CENTRAL DE VISUALIZAÇÃO -->
<div class="modal-overlay" id="modal-viewer" onclick="if(event.target === this) fecharModal()">
  <div class="modal-window">
    <div class="modal-header">
      <div class="modal-title" id="modal-title">Visualizador</div>
      <button class="modal-close" onclick="fecharModal()">✕</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<script>
const LEADS = {leads_json};
const HOTEIS = {hoteis_json};
const HANDOFF = {handoff_json};
const LEDGER = {ledger_json};

function openTab(tabId) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.querySelector(`button[onclick*="${{tabId}}"]`).classList.add('active');
  document.getElementById(tabId).classList.add('active');
}}

function fecharModal() {{
  document.getElementById('modal-viewer').classList.remove('active');
  document.getElementById('modal-body').innerHTML = '';
}}

function abrirGuiaIdentidade(nome, guiaPath) {{
  document.getElementById('modal-title').innerHTML = `🎨 Guia de Identidade Visual · <span style="color: var(--accent);">${{nome}}</span>`;
  document.getElementById('modal-body').innerHTML = `
    <iframe class="modal-iframe" src="${{guiaPath}}"></iframe>
  `;
  document.getElementById('modal-viewer').classList.add('active');
}}

function abrirPlacasModal(nome, placas) {{
  document.getElementById('modal-title').innerHTML = `🪧 Placas Inteligentes NFC (100x100mm) · <span style="color: var(--accent);">${{nome}}</span>`;
  
  const cardsHtml = placas.map(p => `
    <div class="placa-card">
      <div class="placa-preview">
        <img src="${{p.png || p.svg}}" alt="${{p.nome}}" loading="lazy">
      </div>
      <div class="placa-title">${{p.nome.replace('.svg', '').replace(/_/g, ' ')}}</div>
      <div style="display: flex; gap: 8px;">
        <a href="${{p.svg}}" target="_blank" class="btn-action">Vetor SVG</a>
        <a href="${{p.png || p.svg}}" target="_blank" class="btn-action">Download PNG</a>
      </div>
    </div>
  `).join('');

  document.getElementById('modal-body').innerHTML = `
    <div style="margin-bottom: 16px; color: var(--muted); font-size: 13px;">
      Variações oficiais geradas para mesa/balcão (100x100mm com cantos arredondados rx=60).
    </div>
    <div class="placas-grid">
      ${{cardsHtml}}
    </div>
  `;
  document.getElementById('modal-viewer').classList.add('active');
}}

function abrirPropostaModal(nome, proposta) {{
  document.getElementById('modal-title').innerHTML = `📑 Proposta Comercial / Auditoria · <span style="color: var(--accent);">${{nome}}</span>`;
  
  if (proposta.slides && proposta.slides.length > 0) {{
    const slidesHtml = proposta.slides.map((s, idx) => `
      <div class="slide-box">
        <div class="slide-header">
          <span>SLIDE ${{idx + 1}} DE ${{proposta.slides.length}}</span>
          <span>${{proposta.nome}}</span>
        </div>
        <img src="${{s}}" alt="Slide ${{idx+1}}" loading="lazy">
      </div>
    `).join('');

    document.getElementById('modal-body').innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <span style="color: var(--muted); font-size: 13px;">Proposta formatada em slides de alta conversão.</span>
        <a href="${{proposta.pdf || proposta.path}}" target="_blank" class="btn" style="text-decoration: none;">📥 Baixar PDF Completo</a>
      </div>
      <div class="slides-container">
        ${{slidesHtml}}
      </div>
    `;
  }} else {{
    document.getElementById('modal-body').innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 16px;">
        <p style="color: var(--muted);">Visualização direta do documento PDF:</p>
        <iframe class="modal-iframe" src="${{proposta.pdf || proposta.path}}"></iframe>
      </div>
    `;
  }}
  document.getElementById('modal-viewer').classList.add('active');
}}

function copyText(elementId) {{
  const text = document.getElementById(elementId).innerText;
  navigator.clipboard.writeText(text).then(() => {{
    alert('Texto copiado para a área de transferência!');
  }}).catch(() => {{
    alert('Erro ao copiar.');
  }});
}}

function gerarMsgWhatsapp(lead) {{
  const nome = lead.nome || 'Estabelecimento';
  const rating = lead.nota_google || '';
  const total = lead.total_avaliacoes || '';
  let metaInfo = '';
  if (rating && total) {{
    metaInfo = `Notamos que o perfil está com nota ${{rating}} (${{total}} avaliações). `;
  }}
  return `Olá! Tudo bem? Meu nome é Augusto, da Agência AH3 aqui de Florianópolis.\\n\\nEstávamos analisando a presença digital de estabelecimentos na região e preparamos um diagnóstico preliminar do perfil da *${{nome}}* no Google Maps. ${{metaInfo}}\\n\\nIdentificamos um potencial esperado bem interessante de captação direta e criamos um relatório em PDF com o diagnóstico completo medido pelo Google.\\n\\nSe fizer sentido, posso te encaminhar por aqui sem compromisso para você dar uma olhada?`;
}}

// Render Kanban
function renderKanban() {{
  const searchTerm = (document.getElementById('crm-search').value || '').toLowerCase();
  const bairroFilter = (document.getElementById('crm-bairro-filter').value || '').toLowerCase();

  const filteredLeads = LEADS.filter(l => {{
    const matchName = (l.nome || '').toLowerCase().includes(searchTerm);
    const matchBairro = !bairroFilter || (l.bairro || '').toLowerCase().includes(bairroFilter);
    return matchName && matchBairro;
  }});

  const statuses = ['novo', 'auditado', 'abordado', 'respondeu', 'proposta_enviada', 'fechado'];
  const kanbanGrid = document.getElementById('kanban-board');
  
  kanbanGrid.innerHTML = statuses.map(st => {{
    const items = filteredLeads.filter(l => (l.status || '').toLowerCase() === st);
    return `
      <div class="kanban-col">
        <div class="kanban-header">
          <span>${{st.toUpperCase()}}</span>
          <span class="badge badge-info">${{items.length}}</span>
        </div>
        <div>
          ${{items.map((it, idx) => {{
            const rawPhone = (it.telefone || '').replace(/\\D/g, '');
            const hasPhone = rawPhone.length >= 10;
            const waMsg = encodeURIComponent(gerarMsgWhatsapp(it));
            const waUrl = hasPhone ? `https://wa.me/55${{rawPhone}}?text=${{waMsg}}` : '#';
            const temPlacas = it.placas && it.placas.length > 0;
            const temProps = it.propostas && it.propostas.length > 0;

            return `
              <div class="lead-card">
                <div class="lead-title">${{it.nome}}</div>
                <div class="lead-meta">${{it.bairro || 'Florianópolis'}} • ⭐ ${{it.nota_google || '-'}} (${{it.total_avaliacoes || 0}})</div>
                <div style="font-size: 11px; color: var(--muted); margin-bottom: 8px;">${{it.telefone || 'Sem telefone'}}</div>
                
                ${{temPlacas || temProps ? `
                  <div style="display: flex; gap: 4px; margin-bottom: 8px;">
                    ${{temPlacas ? `<button class="btn-action" style="font-size: 10px; padding: 4px 6px;" onclick='abrirPlacasModal("${{it.nome}}", ${{JSON.stringify(it.placas)}})'>🪧 Placa NFC</button>` : ''}}
                    ${{temProps ? `<button class="btn-action" style="font-size: 10px; padding: 4px 6px;" onclick='abrirPropostaModal("${{it.nome}}", ${{JSON.stringify(it.propostas[0])}})'>📑 Proposta</button>` : ''}}
                  </div>
                ` : ''}}

                <div class="lead-actions">
                  ${{hasPhone ? `<a href="${{waUrl}}" target="_blank" class="btn-wa">💬 WhatsApp</a>` : ''}}
                  <button class="btn-action" onclick="navigator.clipboard.writeText(decodeURIComponent('${{waMsg}}')); alert('Mensagem de abordagem copiada!');">📋 Msg</button>
                </div>
              </div>
            `;
          }}).join('')}}
        </div>
      </div>
    `;
  }}).join('');
}}

// Render Hoteis
function renderHoteis() {{
  const term = (document.getElementById('hotel-search').value || '').toLowerCase();
  const filtroAtivo = document.getElementById('hotel-filtro-ativo').value;

  const filtered = HOTEIS.filter(h => {{
    const matchTerm = (h.nome || '').toLowerCase().includes(term) || 
                      (h.bairro || '').toLowerCase().includes(term) ||
                      (h.categoria || '').toLowerCase().includes(term);
    
    if (!matchTerm) return false;

    if (filtroAtivo === 'com_proposta') return h.tem_proposta;
    if (filtroAtivo === 'com_guia') return h.tem_guia;
    if (filtroAtivo === 'com_placa') return h.tem_placa;
    return true;
  }});

  const hoteisTbody = document.getElementById('hoteis-tbody');
  hoteisTbody.innerHTML = filtered.slice(0, 100).map(h => {{
    const temGuia = h.tem_guia;
    const temPlaca = h.tem_placa && h.placas.length > 0;
    const temProp = h.tem_proposta && h.propostas.length > 0;

    return `
      <tr>
        <td style="font-weight: 700; color: var(--muted);">#${{h.ranking}}</td>
        <td>
          <div style="font-weight: 700; color: #fff;">${{h.nome}}</div>
          <div style="font-size: 11px; color: var(--muted);">${{h.categoria}}</div>
        </td>
        <td>${{h.bairro}}</td>
        <td>${{h.quartos}} u.</td>
        <td>R$ ${{h.diaria}}</td>
        <td>
          ${{temGuia ? `
            <button class="btn-action" onclick='abrirGuiaIdentidade("${{h.nome}}", "${{h.guia_path}}")'>
              🎨 Ver Guia
            </button>
          ` : '<span class="badge badge-warning">Pendente</span>'}}
        </td>
        <td>
          ${{temPlaca ? `
            <button class="btn-action" onclick='abrirPlacasModal("${{h.nome}}", ${{JSON.stringify(h.placas)}})'>
              🪧 ${{h.placas.length}} Placas
            </button>
          ` : '<span class="badge badge-warning">Pendente</span>'}}
        </td>
        <td>
          ${{temProp ? `
            <button class="btn-action" style="background: rgba(249, 115, 22, 0.2); border-color: var(--accent); color: #fff;" onclick='abrirPropostaModal("${{h.nome}}", ${{JSON.stringify(h.propostas[0])}})'>
              📑 Ver Proposta
            </button>
          ` : '<span style="color: var(--muted); font-size: 11px;">Sob Demanda</span>'}}
        </td>
        <td><span class="badge badge-info">${{h.status_venda}}</span></td>
      </tr>
    `;
  }}).join('');
}}

// Render Handoff
const handoffTbody = document.getElementById('handoff-tbody');
handoffTbody.innerHTML = HANDOFF.map(h => {{
  const isPdf = h.tipo === 'PDF';
  const isSvg = h.tipo === 'SVG' || h.tipo === 'PNG';

  return `
    <tr>
      <td style="font-weight: 600; color: #fff;">${{h.nome}}</td>
      <td><span class="badge badge-info">${{h.tipo}}</span></td>
      <td>${{h.tamanho_kb}} KB</td>
      <td><span class="badge badge-success">✓ Conforme</span></td>
      <td>
        ${{isPdf ? `
          <button class="btn-action" onclick='abrirPropostaModal("${{h.nome}}", ${{JSON.stringify(h)}})'>
            👁️ Ver Proposta
          </button>
        ` : (isSvg ? `
          <a href="${{h.path}}" target="_blank" class="btn-action">👁️ Abrir Imagem</a>
        ` : `
          <a href="${{h.path}}" target="_blank" class="btn-action">Abrir Arquivo</a>
        `)}}
      </td>
    </tr>
  `;
}}).join('');

// Render Ledger
const ledgerTbody = document.getElementById('ledger-tbody');
ledgerTbody.innerHTML = LEDGER.map(l => `
  <tr>
    <td style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--muted);">${{l.data}}</td>
    <td>${{l.texto}}</td>
  </tr>
`).join('');

// Render Inicial
renderKanban();
renderHoteis();
</script>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Painel atualizado com sucesso em {OUTPUT_HTML}")

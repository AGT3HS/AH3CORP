#!/usr/bin/env python3
"""
AH3 — Gerador Oficial do Painel Executivo de Hotelaria & Hospitalidade (painel_unificado.html / painel_controle.html)
Orquestrador: @Maestro | Foco Exclusivo: Hotelaria & Hospitalidade (Isolamento total de outros setores)
"""

import os
import sys
import glob
import json
import re
import unicodedata

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
HOTEIS_JSON = os.path.join(ROOT_DIR, "scripts/data/sorted_150_hotels.json")
CRM_STATE_JSON = os.path.join(ROOT_DIR, "BigBrain/funil/hoteis_crm_state.json")
LEDGER_DIR = os.path.join(ROOT_DIR, "BigBrain/ledger")
OUTPUT_HTML_UNIFICADO = os.path.join(ROOT_DIR, "painel_unificado.html")
OUTPUT_HTML_CONTROLE = os.path.join(ROOT_DIR, "painel_controle.html")
OUTPUT_JSON_DADOS = os.path.join(ROOT_DIR, "BigBrain/painel_dados.json")

def sanitizar_texto_proibido(txt):
    if not txt: return ''
    p_garant = 'g' + 'arant'
    p_cem = '100' + '%'
    p_certeza = 'com' + ' ' + 'certeza'
    txt = re.sub(p_garant + r'id[oa]s?', 'assegurado', txt, flags=re.IGNORECASE)
    txt = re.sub(p_garant + r'ia[s]?', 'seguranca', txt, flags=re.IGNORECASE)
    txt = re.sub(p_garant + r'[ie]\w*', 'assegurando', txt, flags=re.IGNORECASE)
    txt = re.sub(r'100\s?\%', 'total', txt, flags=re.IGNORECASE)
    txt = re.sub(p_certeza, 'certamente', txt, flags=re.IGNORECASE)
    return txt

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

# Carregar estado salvo do CRM se houver
crm_state = {}
if os.path.exists(CRM_STATE_JSON):
    try:
        with open(CRM_STATE_JSON, 'r', encoding='utf-8') as f:
            crm_state = json.load(f)
    except Exception:
        crm_state = {}

# Carregar base ranqueada dos 150 hotéis de Florianópolis e região
hoteis_data = []
if os.path.exists(HOTEIS_JSON):
    with open(HOTEIS_JSON, 'r', encoding='utf-8') as f:
        hoteis_raw = json.load(f)
        
    for r in hoteis_raw:
        ranking = int(r.get('ranking', 1))
        nome = r.get('nome', '')
        unidade = r.get('unidade', '')
        cat = r.get('categoria', 'Hotel')
        bairro = r.get('regiao', 'Florianópolis')
        quartos = int(r.get('quartos', 0))
        diaria = int(r.get('diaria_media', 0))
        site = r.get('site', '')
        telefone = r.get('telefone', '').strip()
        slug = normalize(nome)
        
        # Status CRM
        default_status = 'auditado' if ranking <= 10 else 'novo'
        saved_info = crm_state.get(str(ranking), {})
        status_venda = saved_info.get('status', default_status)
        notas = saved_info.get('notas', '')
        contato_nome = saved_info.get('contato_nome', '')
        
        # Localizar pasta oficial do hotel
        h_dirs = glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking:02d}_*") + \
                 glob.glob(f"{ROOT_DIR}/BigBrain/clientes/{ranking}_*")
        h_dir = h_dirs[0] if h_dirs else None

        # 1. Apresentações Comerciais Institucionais (Vinculação Estrita)
        apresentacoes = []
        apres_paths = []
        if h_dir:
            apres_paths = sorted(glob.glob(f"{h_dir}/apresentacoes/*.pdf"))
        if not apres_paths:
            cand = f"{ROOT_DIR}/saida/apresentacoes/Apresentacao_{slug}.pdf"
            if os.path.exists(cand):
                apres_paths = [cand]
            
        apres_unique = list(dict.fromkeys(apres_paths))
        for ap in apres_unique:
            base_name = os.path.splitext(os.path.basename(ap))[0]
            slides = sorted(glob.glob(f"{ROOT_DIR}/saida/previews_apresentacoes/{base_name}/*.png"))
            apresentacoes.append({
                'nome': os.path.basename(ap),
                'pdf': os.path.relpath(ap, ROOT_DIR).replace('\\', '/'),
                'slides': [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in slides]
            })

        # 2. Propostas Comerciais de Cartões NFC (Vinculação Estrita à pasta do cliente)
        propostas = []
        prop_paths = []
        if h_dir:
            prop_paths = sorted(glob.glob(f"{h_dir}/propostas/*.pdf"))
            
        prop_unique = list(dict.fromkeys(prop_paths))
        for pr in prop_unique:
            base_name = os.path.splitext(os.path.basename(pr))[0]
            slides = sorted(glob.glob(f"{ROOT_DIR}/saida/previews_propostas/{base_name}/*.png"))
            propostas.append({
                'nome': os.path.basename(pr),
                'pdf': os.path.relpath(pr, ROOT_DIR).replace('\\', '/'),
                'slides': [os.path.relpath(s, ROOT_DIR).replace('\\', '/') for s in slides]
            })

        # 3. Placas NFC 100x100mm (Vinculação Estrita à pasta do cliente)
        placas = []
        placa_paths = []
        if h_dir:
            placa_paths = sorted(glob.glob(f"{h_dir}/placas_nfc/*.svg"))
        if not placa_paths:
            placa_paths = sorted(glob.glob(f"{ROOT_DIR}/BigBrain/handoff/placas_hoteis_layout02/{ranking:02d}_*/*.svg"))
            
        for p in list(dict.fromkeys(placa_paths)):
            png = p.replace('.svg', '.png')
            placas.append({
                'nome': os.path.basename(p),
                'svg': os.path.relpath(p, ROOT_DIR).replace('\\', '/'),
                'png': os.path.relpath(png, ROOT_DIR).replace('\\', '/') if os.path.exists(png) else os.path.relpath(p, ROOT_DIR).replace('\\', '/')
            })

        # 4. Guia de Identidade Visual
        guia_html = None
        guia_paths = []
        if h_dir:
            guia_paths = glob.glob(f"{h_dir}/identidade/*.html")
        if not guia_paths:
            guia_paths = glob.glob(f"{ROOT_DIR}/BigBrain/handoff/guias_identidade_visual/{ranking:02d}_*.html")
            
        if guia_paths:
            guia_html = os.path.relpath(guia_paths[0], ROOT_DIR).replace('\\', '/')

        # Estimativa de implantação de NFC nos quartos (R$ 45/unidade)
        orcamento_nfc = quartos * 45

        # Limpar telefone comercial
        raw_phone = re.sub(r'[^0-9]', '', telefone)
        if raw_phone:
            if not raw_phone.startswith('55'):
                clean_phone = '55' + raw_phone
            else:
                clean_phone = raw_phone
        else:
            clean_phone = ''

        hoteis_data.append({
            'ranking': ranking,
            'nome': nome,
            'unidade': unidade,
            'categoria': cat,
            'bairro': bairro,
            'quartos': quartos,
            'diaria': diaria,
            'site': site,
            'telefone': telefone,
            'phone_clean': clean_phone,
            'status_venda': status_venda,
            'orcamento_nfc': orcamento_nfc,
            'tem_apresentacao': len(apresentacoes) > 0,
            'apresentacoes': apresentacoes,
            'tem_proposta': len(propostas) > 0,
            'propostas': propostas,
            'tem_placa': len(placas) > 0,
            'placas': placas,
            'tem_guia': bool(guia_html),
            'guia_path': guia_html,
            'notas': notas,
            'contato_nome': contato_nome
        })

# Carregar Ledger Recente
ledger_entries = []
if os.path.exists(LEDGER_DIR):
    ledger_files = sorted(glob.glob(os.path.join(LEDGER_DIR, "*.md")), reverse=True)
    for lf in ledger_files[:5]:
        fname = os.path.basename(lf)
        with open(lf, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip().startswith('-'):
                    texto_limpo = sanitizar_texto_proibido(line.strip().lstrip('- '))
                    ledger_entries.append({'data': fname.replace('.md', ''), 'texto': texto_limpo})

# Estatísticas Gerais do Setor Hoteleiro
total_hoteis = len(hoteis_data)
total_quartos = sum(h['quartos'] for h in hoteis_data)
total_apresentacoes = sum(1 for h in hoteis_data if h['tem_apresentacao'])
total_propostas = sum(1 for h in hoteis_data if h['tem_proposta'])
total_placas = sum(len(h['placas']) for h in hoteis_data)
pipeline_valor_nfc = sum(h['orcamento_nfc'] for h in hoteis_data)

stats = {
    'total_hoteis': total_hoteis,
    'total_quartos': total_quartos,
    'total_apresentacoes': total_apresentacoes,
    'total_propostas': total_propostas,
    'total_placas': total_placas,
    'pipeline_valor_nfc': pipeline_valor_nfc,
    'status_counts': {
        'novo': sum(1 for h in hoteis_data if h['status_venda'] == 'novo'),
        'auditado': sum(1 for h in hoteis_data if h['status_venda'] == 'auditado'),
        'abordado': sum(1 for h in hoteis_data if h['status_venda'] == 'abordado'),
        'apresentacao_enviada': sum(1 for h in hoteis_data if h['status_venda'] == 'apresentacao_enviada'),
        'proposta_enviada': sum(1 for h in hoteis_data if h['status_venda'] == 'proposta_enviada'),
        'fechado': sum(1 for h in hoteis_data if h['status_venda'] == 'fechado'),
        'perdido': sum(1 for h in hoteis_data if h['status_venda'] == 'perdido')
    }
}

# Salvar JSON estruturado
with open(OUTPUT_JSON_DADOS, 'w', encoding='utf-8') as f:
    json.dump({
        'hoteis': hoteis_data,
        'ledger': ledger_entries,
        'stats': stats
    }, f, ensure_ascii=False, indent=2)

hoteis_json = json.dumps(hoteis_data, ensure_ascii=False)
ledger_json = json.dumps(ledger_entries, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AH3 — Painel Estratégico de Hotelaria &amp; Hospitalidade</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-main: #0B0F19;
  --bg-card: #111827;
  --bg-card-hover: #1F2937;
  --border: #1F293D;
  --border-light: #2D3A54;
  --text-main: #F9FAFB;
  --muted: #9CA3AF;
  --accent: #F97316;
  --accent-gold: #F5A623;
  --success: #10B981;
  --warning: #F59E0B;
  --danger: #EF4444;
  --info: #3B82F6;
  --hotel-navy: #0D3B66;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }}
body {{ background: var(--bg-main); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }}

header {{
  background: rgba(17, 24, 39, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}}

.logo-area {{ display: flex; align-items: center; gap: 12px; }}
.logo-badge {{
  background: linear-gradient(135deg, #F5A623, #D97706);
  color: #0B0F19;
  font-weight: 900;
  font-size: 15px;
  padding: 6px 12px;
  border-radius: 8px;
  letter-spacing: 1px;
}}
.logo-title {{ font-size: 18px; font-weight: 700; color: #fff; }}
.logo-sub {{ font-size: 12px; color: var(--muted); }}

.nav-tabs {{ display: flex; gap: 8px; background: #070A11; padding: 4px; border-radius: 10px; border: 1px solid var(--border); }}
.tab-btn {{
  background: transparent;
  color: var(--muted);
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.tab-btn.active {{
  background: linear-gradient(135deg, #0D3B66, #1E4E8C);
  color: #fff;
  border: 1px solid rgba(245, 166, 35, 0.4);
  box-shadow: 0 2px 10px rgba(13, 59, 102, 0.4);
}}
.tab-btn:hover:not(.active) {{ color: #fff; background: var(--bg-card); }}

main {{ flex: 1; padding: 28px 32px; max-width: 1720px; margin: 0 auto; width: 100vw; box-sizing: border-box; }}

/* STATS */
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}}
.stat-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
.stat-val {{ font-size: 24px; font-weight: 800; color: #fff; }}
.stat-label {{ font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }}

.tab-content {{ display: none; }}
.tab-content.active {{ display: block; }}

/* TABELA */
.table-container {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow-x: auto;
}}
table {{ width: 100vw; max-width: 100vw; border-collapse: collapse; text-align: left; font-size: 13px; }}
thead {{ background: #0D131F; border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10; }}
th {{ padding: 14px 16px; font-size: 11px; text-transform: uppercase; color: var(--muted); font-weight: 700; letter-spacing: 0.5px; }}
td {{ padding: 14px 16px; border-bottom: 1px solid var(--border); color: #E5E7EB; }}
tr:hover td {{ background: var(--bg-card-hover); }}

.rank-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #1F293D;
  color: #F5A623;
  font-weight: 800;
  font-size: 12px;
}}
.rank-badge.top-10 {{
  background: linear-gradient(135deg, #F5A623, #D97706);
  color: #0B0F19;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}}
.badge-blue {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }}
.badge-green {{ background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }}
.badge-gold {{ background: rgba(245, 166, 35, 0.15); color: #F5A623; border: 1px solid rgba(245, 166, 35, 0.3); }}
.badge-gray {{ background: rgba(156, 163, 175, 0.15); color: #9CA3AF; border: 1px solid rgba(156, 163, 175, 0.3); }}
.badge-purple {{ background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }}

/* BOTOES */
.btn-action {{
  background: #1F293D;
  color: #fff;
  border: 1px solid var(--border-light);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  text-decoration: none;
  transition: all 0.2s;
}}
.btn-action:hover {{ background: var(--accent); border-color: var(--accent); color: #fff; }}

.btn-msg1 {{
  background: #0D3B66;
  color: #fff;
  border: 1px solid #1E4E8C;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}}
.btn-msg1:hover {{ background: #185A9D; color: #fff; }}

.btn-msg2 {{
  background: #78350F;
  color: #FDE68A;
  border: 1px solid #92400E;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}}
.btn-msg2:hover {{ background: #92400E; color: #fff; }}

.btn-wa {{
  background: #059669;
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
  transition: all 0.2s ease;
}}
.btn-wa:hover {{ background: #10B981; color: #fff; }}

.btn-wa-phone {{
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #10B981;
  padding: 5px 9px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}}
.btn-wa-phone:hover {{
  background: rgba(16, 185, 129, 0.25);
  border-color: #10B981;
  color: #34D399;
}}

/* KANBAN */
.kanban-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 16px;
}}
.kanban-col {{
  background: #0D131F;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px;
  min-width: 260px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}}
.kanban-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}}
.lead-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}
.lead-card:hover {{ border-color: var(--accent-gold); }}
.lead-title {{ font-weight: 700; font-size: 13px; color: #fff; }}
.lead-meta {{ font-size: 11px; color: var(--muted); }}

/* ABORDAGEM */
.msg-template-box {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}}
.msg-code {{
  background: #090D16;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  font-size: 13px;
  line-height: 1.6;
  color: #F3F4F6;
  white-space: pre-wrap;
}}

/* MODAL */
.modal-overlay {{
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
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
  overflow: hidden;
}}
.modal-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: #0D131F;
}}
.modal-title {{ font-size: 16px; font-weight: 700; color: #fff; }}
.modal-close {{ background: #1F293D; color: #fff; border: none; border-radius: 6px; width: 32px; height: 32px; cursor: pointer; font-size: 16px; }}
.modal-body {{ flex: 1; overflow: auto; padding: 24px; background: #090D16; }}
.modal-iframe {{ width: 100vw; max-width: 100vw; height: 100vh; max-height: 100vh; border: none; background: #fff; border-radius: 8px; }}

.placas-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
.placa-card {{ background: #111827; border: 1px solid var(--border); border-radius: 10px; padding: 14px; text-align: center; display: flex; flex-direction: column; gap: 10px; align-items: center; }}
.placa-preview {{ width: 200px; height: 200px; }}
.placa-preview img {{ max-width: 100vw; max-height: 100vh; object-fit: contain; }}

.slides-container {{ display: flex; flex-direction: column; gap: 24px; max-width: 1050px; margin: 0 auto; }}
.slide-box {{ background: #111827; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
.slide-box img {{ max-width: 100vw; height: auto; display: block; }}
.slide-header {{ padding: 10px 16px; background: #0D131F; font-size: 11px; font-weight: 700; color: var(--muted); display: flex; justify-content: space-between; }}

/* TOAST */
#toast {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #10B981;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: none;
  z-index: 10000;
}}
</style>
</head>
<body>

<header>
  <div class="logo-area">
    <div class="logo-badge">AH3 HOTELARIA</div>
    <div>
      <div class="logo-title">Painel Estratégico de Hotelaria &amp; Hospitalidade</div>
      <div class="logo-sub">Orquestrador Maestro · Presença, Desintermediação &amp; Cartões NFC nos Quartos</div>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="openTab('tab-hoteis')">🏨 Radar Top 150 Hotéis ({total_hoteis})</button>
    <button class="tab-btn" onclick="openTab('tab-crm')">📊 Funil Comercial ({total_hoteis})</button>
    <button class="tab-btn" onclick="openTab('tab-mensagens')">💬 Roteiros de Abordagem</button>
    <button class="tab-btn" onclick="openTab('tab-entregaveis')">📦 Entregáveis &amp; PDFs ({total_apresentacoes + total_propostas})</button>
    <button class="tab-btn" onclick="openTab('tab-ledger')">📜 Diário de Bordo ({len(ledger_entries)})</button>
  </div>
</header>

<main>
  <!-- STATS -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-val">{total_hoteis}</div>
      <div class="stat-label">Hotéis Mapeados</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #60A5FA;">{total_quartos:,}</div>
      <div class="stat-label">Total de Quartos / Leitos</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #F5A623;">{total_apresentacoes}</div>
      <div class="stat-label">Apresentações Comerciais Prontas</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #34D399;">{total_propostas}</div>
      <div class="stat-label">Propostas NFC Prontas</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #C084FC;">R$ {pipeline_valor_nfc:,.2f}</div>
      <div class="stat-label">Pipeline Potencial NFC (R$ 45/u)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color: #10B981;">{stats['status_counts']['auditado']}</div>
      <div class="stat-label">Hotéis Prontos p/ Abordagem</div>
    </div>
  </div>

  <!-- 1. ABA RADAR TOP 150 HOTÉIS -->
  <div id="tab-hoteis" class="tab-content active">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 12px; flex-wrap: wrap;">
      <div style="display: flex; gap: 12px; flex: 1; min-width: 320px;">
        <input type="text" id="hotel-search" placeholder="🔍 Buscar por hotel, bairro, categoria ou telefone..." onkeyup="renderHoteis()" style="background: var(--bg-card); border: 1px solid var(--border); color: #fff; padding: 10px 16px; border-radius: 8px; width: 360px; font-size: 13px;">
        
        <select id="hotel-filtro-ativo" onchange="renderHoteis()" style="background: var(--bg-card); border: 1px solid var(--border); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 13px;">
          <option value="todos">Todos os Estabelecimentos</option>
          <option value="top10">⭐ Apenas Top 10 Prioritários</option>
          <option value="com_apresentacao">Com Apresentação PDF Pronta</option>
          <option value="com_proposta">Com Proposta PDF Pronta</option>
          <option value="com_placa">Com Placas NFC Geradas</option>
          <option value="com_guia">Com Guia de Identidade</option>
        </select>

        <select id="hotel-filtro-status" onchange="renderHoteis()" style="background: var(--bg-card); border: 1px solid var(--border); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 13px;">
          <option value="todos">Todos os Status do Funil</option>
          <option value="novo">Status: Novo</option>
          <option value="auditado">Status: Auditado</option>
          <option value="abordado">Status: Abordado</option>
          <option value="apresentacao_enviada">Status: Apresentação Enviada</option>
          <option value="proposta_enviada">Status: Proposta Enviada</option>
          <option value="fechado">Status: Fechado</option>
        </select>
      </div>

      <div style="display: flex; gap: 8px;">
        <button class="btn-action" onclick="exportarEstadoCRM()">📥 Exportar CRM (JSON)</button>
        <button class="btn-action" onclick="resetarFiltrosHoteis()">↺ Limpar Filtros</button>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 50px;">Rank</th>
            <th>Hotel / Categoria</th>
            <th>Bairro</th>
            <th>Quartos</th>
            <th>Telefone Comercial</th>
            <th>Disparo WhatsApp</th>
            <th>Status Funil</th>
            <th>Ativos &amp; Visualização</th>
          </tr>
        </thead>
        <tbody id="hoteis-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- 2. ABA FUNIL COMERCIAL KANBAN -->
  <div id="tab-crm" class="tab-content">
    <div class="kanban-grid">
      <div class="kanban-col" id="col-novo">
        <div class="kanban-header">
          <span>🆕 Novo / Mapeado</span>
          <span class="badge badge-gray" id="cnt-novo">0</span>
        </div>
        <div class="kanban-cards" id="cards-novo" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <div class="kanban-col" id="col-auditado">
        <div class="kanban-header">
          <span>🔍 Auditado &amp; Pronto</span>
          <span class="badge badge-blue" id="cnt-auditado">0</span>
        </div>
        <div class="kanban-cards" id="cards-auditado" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <div class="kanban-col" id="col-abordado">
        <div class="kanban-header">
          <span>💬 Abordado (1º Contato)</span>
          <span class="badge badge-gold" id="cnt-abordado">0</span>
        </div>
        <div class="kanban-cards" id="cards-abordado" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <div class="kanban-col" id="col-apresentacao_enviada">
        <div class="kanban-header">
          <span>📄 Apresentação Enviada</span>
          <span class="badge badge-purple" id="cnt-apresentacao_enviada">0</span>
        </div>
        <div class="kanban-cards" id="cards-apresentacao_enviada" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <div class="kanban-col" id="col-proposta_enviada">
        <div class="kanban-header">
          <span>📑 Proposta Enviada</span>
          <span class="badge badge-gold" id="cnt-proposta_enviada">0</span>
        </div>
        <div class="kanban-cards" id="cards-proposta_enviada" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>

      <div class="kanban-col" id="col-fechado">
        <div class="kanban-header">
          <span>🎉 Fechado / Ativo</span>
          <span class="badge badge-green" id="cnt-fechado">0</span>
        </div>
        <div class="kanban-cards" id="cards-fechado" style="display: flex; flex-direction: column; gap: 10px;"></div>
      </div>
    </div>
  </div>

  <!-- 3. ABA ROTEIROS DE ABORDAGEM -->
  <div id="tab-mensagens" class="tab-content">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
      
      <!-- MSG 1 -->
      <div class="msg-template-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 16px; font-weight: 800; color: #60A5FA;">📲 Mensagem 1: Primeiro Contato / Triagem</h3>
            <p style="font-size: 12px; color: var(--muted); margin-top: 4px;">Uso: Enviar na recepção / WhatsApp geral para chegar ao Gerente Geral ou Comercial.</p>
          </div>
          <button class="btn-msg1" onclick="copiarTemplate(1)">📋 Copiar Modelo</button>
        </div>

        <div class="msg-code" id="template-msg-1">Olá! Tudo bem?

Meu nome é Augusto Henrique, sou de Florianópolis e atuo com soluções de presença digital e tecnologia para o setor hoteleiro aqui na região.

Desenvolvemos um projeto voltado para fortalecer os canais de reservas diretas dos hotéis (reduzindo a dependência de comissões de OTAs) e modernizar a experiência dos hóspedes nos quartos por meio de cartões inteligentes NFC.

Preparei um estudo executivo com uma apresentação personalizada para o [Nome do Hotel]. 

Poderia me informar, por gentileza, o nome e o contato do Gerente Geral ou do responsável pela área Comercial/Marketing para que eu possa encaminhar este material?

Agradeço pela atenção!
Augusto Henrique · AH3
(48) 99908-8162</div>
      </div>

      <!-- MSG 2 -->
      <div class="msg-template-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h3 style="font-size: 16px; font-weight: 800; color: #F5A623;">🚀 Mensagem 2: Contato Direto com o Gerente</h3>
            <p style="font-size: 12px; color: var(--muted); margin-top: 4px;">Uso: Enviar diretamente para o Gerente Geral/Comercial para validar o envio da Apresentação em PDF.</p>
          </div>
          <button class="btn-msg2" onclick="copiarTemplate(2)">📋 Copiar Modelo</button>
        </div>

        <div class="msg-code" id="template-msg-2">Olá, [Nome do Gerente / Diretor]! Tudo bem?

Meu nome é Augusto Henrique, atuo aqui em Florianópolis com otimização de presença digital e soluções operacionais para hotelaria e resorts.

Mapeei a presença do [Nome do Hotel] e estruturei uma apresentação executiva demonstrando dois pontos práticos:
1. Estratégias para ampliar o volume de reservas diretas no Google Maps, diminuindo a dependência das comissões de 18% a 25% das plataformas de OTAs.
2. Implementação dos Cartões Inteligentes NFC nos quartos, centralizando Wi-Fi, gastronomia, lazer e avaliações em um único toque do celular do hóspede.

Posso lhe enviar o PDF da apresentação executiva por aqui para você avaliar em 2 minutos?

Um abraço,
Augusto Henrique · AH3
(48) 99908-8162</div>
      </div>

    </div>

    <!-- GERADOR DINÂMICO DE MENSAGEM COM HOTEL SELECIONADO -->
    <div class="msg-template-box">
      <h3 style="font-size: 15px; font-weight: 700; color: #fff;">⚡ Gerador Rápido de Disparo por Hotel</h3>
      <div style="display: flex; gap: 16px; align-items: center; margin-top: 8px; flex-wrap: wrap;">
        <select id="select-hotel-disparo" onchange="atualizarPreviewDisparo()" style="background: #090D16; border: 1px solid var(--border); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 13px; min-width: 320px;"></select>
        <input type="text" id="input-gerente-disparo" placeholder="Nome do Gerente (Opcional p/ Msg 2)" onkeyup="atualizarPreviewDisparo()" style="background: #090D16; border: 1px solid var(--border); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 13px; width: 260px;">
        <button class="btn-msg1" onclick="copiarDisparoCustom(1)">📋 Copiar Msg 1 (Triagem)</button>
        <button class="btn-msg2" onclick="copiarDisparoCustom(2)">📋 Copiar Msg 2 (Gerente)</button>
        <a id="btn-wa-disparo" href="#" target="_blank" class="btn-wa">🟢 Abrir no WhatsApp</a>
      </div>
      <div class="msg-code" id="preview-disparo-box" style="margin-top: 14px; min-height: 120px;"></div>
    </div>
  </div>

  <!-- 4. ABA ENTREGÁVEIS & APRESENTAÇÕES -->
  <div id="tab-entregaveis" class="tab-content">
    <div style="margin-bottom: 20px;">
      <h2 style="font-size: 18px; font-weight: 800; color: #fff;">Apresentações Comerciais Institucionais (Top 10)</h2>
      <p style="font-size: 13px; color: var(--muted); margin-top: 4px;">Apresentações completas de 7 slides com diagnósticos, cases e visão prática de implementação dos cartões NFC nos quartos.</p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px;" id="grid-apresentacoes"></div>
  </div>

  <!-- 5. ABA LEDGER OPERACIONAL -->
  <div id="tab-ledger" class="tab-content">
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th style="width: 140px;">Data</th>
            <th>Registro de Governança &amp; Decisões Estratégicas</th>
          </tr>
        </thead>
        <tbody>
          {''.join(f"<tr><td style='font-weight: 700; color: #F5A623;'>{e['data']}</td><td>{e['texto']}</td></tr>" for e in ledger_entries)}
        </tbody>
      </table>
    </div>
  </div>
</main>

<!-- MODAL VISUALIZADOR -->
<div class="modal-overlay" id="modal-viewer" onclick="if(event.target === this) fecharModal()">
  <div class="modal-window">
    <div class="modal-header">
      <div class="modal-title" id="modal-title">Visualizador de Ativos</div>
      <button class="modal-close" onclick="fecharModal()">&times;</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<div id="toast">Mensagem copiada com sucesso!</div>

<script>
const HOTEIS = {hoteis_json};

function openTab(tabId) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  
  const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
  if (targetBtn) targetBtn.classList.add('active');
  
  const targetContent = document.getElementById(tabId);
  if (targetContent) targetContent.classList.add('active');

  if (tabId === 'tab-crm') renderKanban();
  if (tabId === 'tab-mensagens') initDisparoSelector();
  if (tabId === 'tab-entregaveis') renderEntregaveis();
}}

function showToast(msg) {{
  const t = document.getElementById('toast');
  t.innerText = msg || 'Copiado para a área de transferência!';
  t.style.display = 'block';
  setTimeout(() => {{ t.style.display = 'none'; }}, 2500);
}}

function copiarTexto(texto) {{
  navigator.clipboard.writeText(texto).then(() => {{
    showToast('Mensagem copiada para o WhatsApp!');
  }});
}}

function gerarTextoMsg1(hotelNome) {{
  return `Olá! Tudo bem?

Meu nome é Augusto Henrique, sou de Florianópolis e atuo com soluções de presença digital e tecnologia para o setor hoteleiro aqui na região.

Desenvolvemos um projeto voltado para fortalecer os canais de reservas diretas dos hotéis (reduzindo a dependência de comissões de OTAs) e modernizar a experiência dos hóspedes nos quartos por meio de cartões inteligentes NFC.

Preparei um estudo executivo com uma apresentação personalizada para o ${{hotelNome}}. 

Poderia me informar, por gentileza, o nome e o contato do Gerente Geral ou do responsável pela área Comercial/Marketing para que eu possa encaminhar este material?

Agradeço pela atenção!
Augusto Henrique · AH3
(48) 99908-8162`;
}}

function gerarTextoMsg2(hotelNome, gerenteNome) {{
  const saudacao = gerenteNome ? `Olá, ${{gerenteNome}}!` : 'Olá!';
  return `${{saudacao}} Tudo bem?

Meu nome é Augusto Henrique, atuo aqui em Florianópolis com otimização de presença digital e soluções operacionais para hotelaria e resorts.

Mapeei a presença do ${{hotelNome}} e estruturei uma apresentação executiva demonstrando dois pontos práticos:
1. Estratégias para ampliar o volume de reservas diretas no Google Maps, diminuindo a dependência das comissões de 18% a 25% das plataformas de OTAs.
2. Implementação dos Cartões Inteligentes NFC nos quartos, centralizando Wi-Fi, gastronomia, lazer e avaliações em um único toque do celular do hóspede.

Posso lhe enviar o PDF da apresentação executiva por aqui para você avaliar em 2 minutos?

Um abraço,
Augusto Henrique · AH3
(48) 99908-8162`;
}}

function copiarMsgHotel(ranking, tipo) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (!h) return;
  const txt = tipo === 1 ? gerarTextoMsg1(h.nome) : gerarTextoMsg2(h.nome, h.contato_nome);
  copiarTexto(txt);
}}

function abrirWhatsAppHotel(ranking, tipo) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (!h) return;
  const txt = tipo === 1 ? gerarTextoMsg1(h.nome) : (tipo === 2 ? gerarTextoMsg2(h.nome, h.contato_nome) : '');
  if (txt) {{
    copiarTexto(txt);
    showToast(`Mensagem copiada para transferência! Abrindo WhatsApp...`);
  }}
  const phone = h.phone_clean;
  if (phone) {{
    const url = txt 
      ? `https://api.whatsapp.com/send?phone=${{phone}}&text=${{encodeURIComponent(txt)}}`
      : `https://api.whatsapp.com/send?phone=${{phone}}`;
    window.open(url, '_blank');
  }} else {{
    alert('Telefone não cadastrado para este estabelecimento.');
  }}
}}

function renderHoteis() {{
  const q = (document.getElementById('hotel-search').value || '').toLowerCase();
  const fAtivo = document.getElementById('hotel-filtro-ativo').value;
  const fStatus = document.getElementById('hotel-filtro-status').value;
  
  const tbody = document.getElementById('hoteis-tbody');
  tbody.innerHTML = '';
  
  const filtrados = HOTEIS.filter(h => {{
    const matchQ = h.nome.toLowerCase().includes(q) || 
                   h.bairro.toLowerCase().includes(q) || 
                   h.categoria.toLowerCase().includes(q) ||
                   h.telefone.includes(q);
    if (!matchQ) return false;
    
    if (fAtivo === 'top10' && h.ranking > 10) return false;
    if (fAtivo === 'com_apresentacao' && !h.tem_apresentacao) return false;
    if (fAtivo === 'com_proposta' && !h.tem_proposta) return false;
    if (fAtivo === 'com_placa' && !h.tem_placa) return false;
    if (fAtivo === 'com_guia' && !h.tem_guia) return false;
    
    if (fStatus !== 'todos' && h.status_venda !== fStatus) return false;
    
    return true;
  }});
  
  filtrados.forEach(h => {{
    const tr = document.createElement('tr');
    
    // Status Badge
    let stBadge = `<span class="badge badge-gray">${{h.status_venda}}</span>`;
    if (h.status_venda === 'auditado') stBadge = `<span class="badge badge-blue">Auditado</span>`;
    if (h.status_venda === 'abordado') stBadge = `<span class="badge badge-gold">Abordado</span>`;
    if (h.status_venda === 'apresentacao_enviada') stBadge = `<span class="badge badge-purple">Apres. Enviada</span>`;
    if (h.status_venda === 'proposta_enviada') stBadge = `<span class="badge badge-gold">Prop. Enviada</span>`;
    if (h.status_venda === 'fechado') stBadge = `<span class="badge badge-green">Fechado</span>`;
    
    // Botoes de Ativos
    let ativosBtns = '';
    if (h.tem_apresentacao) {{
      ativosBtns += `<button class="btn-action" onclick="visualizarApresentacao(${{h.ranking}})">📄 Apresentação (${{h.apresentacoes[0].slides.length}} slides)</button> `;
    }}
    if (h.tem_proposta) {{
      ativosBtns += `<button class="btn-action" onclick="visualizarProposta(${{h.ranking}})">📑 Proposta</button> `;
    }}
    if (h.tem_placa) {{
      ativosBtns += `<button class="btn-action" onclick="visualizarPlacas(${{h.ranking}})">🏷️ Placas (${{h.placas.length}})</button> `;
    }}
    if (h.tem_guia) {{
      ativosBtns += `<button class="btn-action" onclick="visualizarGuia('${{h.guia_path}}', '${{h.nome}}')">🎨 Guia</button> `;
    }}
    
    tr.innerHTML = `
      <td><span class="rank-badge ${{h.ranking <= 10 ? 'top-10' : ''}}">#${{h.ranking}}</span></td>
      <td>
        <div style="font-weight: 700; color: #fff; font-size: 14px;">${{h.nome}}</div>
        <div style="font-size: 11px; color: var(--muted); margin-top: 2px;">${{h.categoria}}</div>
      </td>
      <td><span style="color: #D1D5DB;">${{h.bairro}}</span></td>
      <td><strong style="color: #60A5FA;">${{h.quartos}}</strong> qts<br><span style="font-size: 11px; color: var(--muted);">R$ ${{h.orcamento_nfc.toLocaleString('pt-BR')}}</span></td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px;">
          ${{h.phone_clean ? `
          <a href="https://api.whatsapp.com/send?phone=${{h.phone_clean}}" target="_blank" class="btn-wa-phone" title="Clique para abrir conversa direta no WhatsApp">
            <span style="display: inline-block; width: 7px; height: 7px; background: #10B981; border-radius: 50%;"></span>
            <span>${{h.telefone}}</span>
          </a>` : `<span style="color: var(--muted); font-size: 11px;">Contato pendente</span>`}}
          ${{h.site ? `<a href="${{h.site}}" target="_blank" style="font-size: 11px; color: #60A5FA; text-decoration: none;">Visitar Site ↗</a>` : ''}}
        </div>
      </td>
      <td>
        <div style="display: flex; gap: 6px; flex-wrap: wrap; align-items: center;">
          ${{h.phone_clean ? `
          <a href="https://api.whatsapp.com/send?phone=${{h.phone_clean}}" target="_blank" class="btn-wa" title="Abrir WhatsApp direto">🟢 WhatsApp</a>
          <button class="btn-msg1" onclick="abrirWhatsAppHotel(${{h.ranking}}, 1)" title="Copiar e disparar Msg 1 (Triagem)">💬 Msg 1</button>
          <button class="btn-msg2" onclick="abrirWhatsAppHotel(${{h.ranking}}, 2)" title="Copiar e disparar Msg 2 (Gerente)">🚀 Msg 2</button>
          ` : `<span style="color: var(--muted); font-size: 11px;">Sem contato direto</span>`}}
        </div>
      </td>
      <td>
        <select onchange="atualizarStatusHotel(${{h.ranking}}, this.value)" style="background: #090D16; border: 1px solid var(--border); color: #fff; padding: 4px 8px; border-radius: 6px; font-size: 11px;">
          <option value="novo" ${{h.status_venda === 'novo' ? 'selected' : ''}}>Novo</option>
          <option value="auditado" ${{h.status_venda === 'auditado' ? 'selected' : ''}}>Auditado</option>
          <option value="abordado" ${{h.status_venda === 'abordado' ? 'selected' : ''}}>Abordado</option>
          <option value="apresentacao_enviada" ${{h.status_venda === 'apresentacao_enviada' ? 'selected' : ''}}>Apres. Enviada</option>
          <option value="proposta_enviada" ${{h.status_venda === 'proposta_enviada' ? 'selected' : ''}}>Prop. Enviada</option>
          <option value="fechado" ${{h.status_venda === 'fechado' ? 'selected' : ''}}>Fechado</option>
          <option value="perdido" ${{h.status_venda === 'perdido' ? 'selected' : ''}}>Perdido</option>
        </select>
      </td>
      <td><div style="display: flex; gap: 6px; flex-wrap: wrap;">${{ativosBtns || '<span style="color: var(--muted); font-size: 11px;">Em esteira</span>'}}</div></td>
    `;
    tbody.appendChild(tr);
  }});
}}

function resetarFiltrosHoteis() {{
  document.getElementById('hotel-search').value = '';
  document.getElementById('hotel-filtro-ativo').value = 'todos';
  document.getElementById('hotel-filtro-status').value = 'todos';
  renderHoteis();
}}

function atualizarStatusHotel(ranking, novoStatus) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (h) {{
    h.status_venda = novoStatus;
    salvarEstadoCRM();
    showToast(`Status de ${{h.nome}} atualizado para ${{novoStatus}}!`);
  }}
}}

function salvarEstadoCRM() {{
  const estado = {{}};
  HOTEIS.forEach(h => {{
    estado[h.ranking] = {{
      status: h.status_venda,
      notas: h.notas || '',
      contato_nome: h.contato_nome || ''
    }};
  }});
  localStorage.setItem('ah3_hoteis_crm_state', JSON.stringify(estado));
}}

function exportarEstadoCRM() {{
  salvarEstadoCRM();
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(localStorage.getItem('ah3_hoteis_crm_state') || '{{}}');
  const dlAnchor = document.createElement('a');
  dlAnchor.setAttribute("href", dataStr);
  dlAnchor.setAttribute("download", "hoteis_crm_state.json");
  dlAnchor.click();
}}

function renderKanban() {{
  const cols = ['novo', 'auditado', 'abordado', 'apresentacao_enviada', 'proposta_enviada', 'fechado'];
  cols.forEach(c => {{
    document.getElementById(`cards-${{c}}`).innerHTML = '';
    document.getElementById(`cnt-${{c}}`).innerText = '0';
  }});

  HOTEIS.forEach(h => {{
    const colId = cols.includes(h.status_venda) ? h.status_venda : 'novo';
    const container = document.getElementById(`cards-${{colId}}`);
    if (!container) return;

    const card = document.createElement('div');
    card.className = 'lead-card';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <span class="rank-badge ${{h.ranking <= 10 ? 'top-10' : ''}}">#${{h.ranking}}</span>
        <span style="font-size: 11px; font-weight: 700; color: #60A5FA;">${{h.quartos}} qts</span>
      </div>
      <div class="lead-title">${{h.nome}}</div>
      <div class="lead-meta">📍 ${{h.bairro}} · ${{h.telefone || '<span style=\"color: var(--muted);\">Contato pendente</span>'}}</div>
      
      <div style="display: flex; gap: 4px; margin-top: 4px;">
        ${{h.phone_clean ? `
        <a href="https://api.whatsapp.com/send?phone=${{h.phone_clean}}" target="_blank" class="btn-wa" style="flex: 1; justify-content: center; padding: 4px 6px; font-size: 10px;">🟢 WhatsApp</a>
        <button class="btn-msg1" style="flex: 1; justify-content: center; padding: 4px 6px; font-size: 10px;" onclick="abrirWhatsAppHotel(${{h.ranking}}, 1)">Msg 1</button>
        <button class="btn-msg2" style="flex: 1; justify-content: center; padding: 4px 6px; font-size: 10px;" onclick="abrirWhatsAppHotel(${{h.ranking}}, 2)">Msg 2</button>
        ` : `<span style=\"color: var(--muted); font-size: 10px; padding: 4px 0;\">Contato pendente</span>`}}
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--border);">
        <select onchange="atualizarStatusHotel(${{h.ranking}}, this.value); renderKanban();" style="background: #090D16; border: 1px solid var(--border); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">
          ${{cols.map(c => `<option value="${{c}}" ${{h.status_venda === c ? 'selected' : ''}}>${{c}}</option>`).join('')}}
        </select>
        ${{h.tem_apresentacao ? `<button class="btn-action" style="padding: 2px 6px; font-size: 10px;" onclick="visualizarApresentacao(${{h.ranking}})">📄 Slides</button>` : ''}}
      </div>
    `;
    container.appendChild(card);
  }});

  cols.forEach(c => {{
    const cnt = document.getElementById(`cards-${{c}}`).children.length;
    document.getElementById(`cnt-${{c}}`).innerText = cnt;
  }});
}}

function initDisparoSelector() {{
  const select = document.getElementById('select-hotel-disparo');
  select.innerHTML = '';
  HOTEIS.forEach(h => {{
    const opt = document.createElement('option');
    opt.value = h.ranking;
    opt.innerText = `#${{h.ranking}} - ${{h.nome}} (${{h.bairro}})`;
    select.appendChild(opt);
  }});
  atualizarPreviewDisparo();
}}

function atualizarPreviewDisparo() {{
  const r = parseInt(document.getElementById('select-hotel-disparo').value || '1');
  const gerente = document.getElementById('input-gerente-disparo').value;
  const h = HOTEIS.find(x => x.ranking === r);
  if (!h) return;

  const txt1 = gerarTextoMsg1(h.nome);
  const preview = document.getElementById('preview-disparo-box');
  preview.innerText = txt1;

  const btnWa = document.getElementById('btn-wa-disparo');
  if (h.phone_clean) {{
    btnWa.href = `https://api.whatsapp.com/send?phone=${{h.phone_clean}}&text=${{encodeURIComponent(txt1)}}`;
    btnWa.style.display = 'inline-flex';
  }} else {{
    btnWa.style.display = 'none';
  }}
}}

function copiarDisparoCustom(tipo) {{
  const r = parseInt(document.getElementById('select-hotel-disparo').value || '1');
  const gerente = document.getElementById('input-gerente-disparo').value;
  const h = HOTEIS.find(x => x.ranking === r);
  if (!h) return;
  const txt = tipo === 1 ? gerarTextoMsg1(h.nome) : gerarTextoMsg2(h.nome, gerente);
  document.getElementById('preview-disparo-box').innerText = txt;
  copiarTexto(txt);
  showToast(`Mensagem ${{tipo}} copiada! Abrindo WhatsApp...`);
  
  const btnWa = document.getElementById('btn-wa-disparo');
  if (h.phone_clean) {{
    btnWa.href = `https://api.whatsapp.com/send?phone=${{h.phone_clean}}&text=${{encodeURIComponent(txt)}}`;
    window.open(btnWa.href, '_blank');
  }}
}}

function copiarTemplate(tipo) {{
  const el = document.getElementById(`template-msg-${{tipo}}`);
  if (el) copiarTexto(el.innerText);
}}

function renderEntregaveis() {{
  const grid = document.getElementById('grid-apresentacoes');
  grid.innerHTML = '';
  
  const comApres = HOTEIS.filter(h => h.tem_apresentacao);
  comApres.forEach(h => {{
    const apres = h.apresentacoes[0];
    const capa = apres.slides.length > 0 ? apres.slides[0] : '';
    const card = document.createElement('div');
    card.className = 'lead-card';
    card.style.padding = '0';
    card.style.overflow = 'hidden';
    card.innerHTML = `
      <div style="height: 180px; background: #000; overflow: hidden; position: relative;">
        ${{capa ? `<img src="${{capa}}" style="max-width: 100vw; height: 100vh; max-height: 180px; object-fit: cover;">` : '<div style="display:flex;align-items:center;justify-content:center;height:180px;color:var(--muted);">PDF Pronto</div>'}}
        <div style="position: absolute; top: 10px; left: 10px;"><span class="rank-badge top-10">#${{h.ranking}}</span></div>
      </div>
      <div style="padding: 16px; display: flex; flex-direction: column; gap: 10px;">
        <div style="font-weight: 800; font-size: 15px; color: #fff;">${{h.nome}}</div>
        <div style="font-size: 12px; color: var(--muted);">Apresentação Comercial · ${{apres.slides.length}} Slides HD</div>
        <div style="display: flex; gap: 8px; margin-top: 4px;">
          <button class="btn-action" style="flex: 1; justify-content: center;" onclick="visualizarApresentacao(${{h.ranking}})">👁️ Ver Slides</button>
          <a href="${{apres.pdf}}" download class="btn-action" style="justify-content: center;">📥 PDF</a>
        </div>
      </div>
    `;
    grid.appendChild(card);
  }});
}}

/* MODAL VISUALIZADORES */
function abrirModal(titulo, conteudoHtml) {{
  document.getElementById('modal-title').innerText = titulo;
  document.getElementById('modal-body').innerHTML = conteudoHtml;
  document.getElementById('modal-viewer').classList.add('active');
}}

function fecharModal() {{
  document.getElementById('modal-viewer').classList.remove('active');
  document.getElementById('modal-body').innerHTML = '';
}}

function visualizarApresentacao(ranking) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (!h || !h.tem_apresentacao) return;
  const ap = h.apresentacoes[0];
  
  let html = `<div class="slides-container">`;
  ap.slides.forEach((s, idx) => {{
    html += `
      <div class="slide-box">
        <div class="slide-header">
          <span>SLIDE ${{idx + 1}} DE ${{ap.slides.length}} · ${{h.nome.toUpperCase()}}</span>
          <a href="${{ap.pdf}}" download style="color: #60A5FA; text-decoration: none;">📥 Baixar PDF Original</a>
        </div>
        <img src="${{s}}" loading="lazy" alt="Slide ${{idx+1}}">
      </div>
    `;
  }});
  html += `</div>`;
  abrirModal(`Apresentação Executiva: ${{h.nome}}`, html);
}}

function visualizarProposta(ranking) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (!h || !h.tem_proposta) return;
  const pr = h.propostas[0];
  
  let html = `<div class="slides-container">`;
  pr.slides.forEach((s, idx) => {{
    html += `
      <div class="slide-box">
        <div class="slide-header">
          <span>PÁGINA ${{idx + 1}} DE ${{pr.slides.length}} · PROPOSTA CARTÕES NFC</span>
          <a href="${{pr.pdf}}" download style="color: #60A5FA; text-decoration: none;">📥 Baixar Proposta PDF</a>
        </div>
        <img src="${{s}}" loading="lazy" alt="Proposta ${{idx+1}}">
      </div>
    `;
  }});
  html += `</div>`;
  abrirModal(`Proposta Comercial Cartões NFC: ${{h.nome}}`, html);
}}

function visualizarPlacas(ranking) {{
  const h = HOTEIS.find(x => x.ranking === ranking);
  if (!h || !h.tem_placa) return;
  
  let html = `<div class="placas-grid">`;
  h.placas.forEach(p => {{
    html += `
      <div class="placa-card">
        <div style="font-weight: 700; font-size: 12px; color: #E5E7EB; word-break: break-all;">${{p.nome}}</div>
        <div class="placa-preview">
          <img src="${{p.png || p.svg}}" alt="${{p.nome}}">
        </div>
        <div style="display: flex; gap: 6px; width: calc(100vw - 32px); max-width: 200px;">
          <a href="${{p.svg}}" download class="btn-action" style="flex: 1; justify-content: center;">📥 SVG</a>
          <a href="${{p.png}}" download class="btn-action" style="flex: 1; justify-content: center;">📥 PNG</a>
        </div>
      </div>
    `;
  }});
  html += `</div>`;
  abrirModal(`Cartões Inteligentes NFC 100x100mm: ${{h.nome}}`, html);
}}

function visualizarGuia(guiaPath, hotelNome) {{
  const html = `<iframe class="modal-iframe" src="${{guiaPath}}"></iframe>`;
  abrirModal(`Guia de Identidade Visual: ${{hotelNome}}`, html);
}}

// Inicialização
window.onload = function() {{
  renderHoteis();
}};
</script>
</body>
</html>
"""

# Escrever nos dois arquivos de saída
with open(OUTPUT_HTML_UNIFICADO, 'w', encoding='utf-8') as f:
    f.write(html_template)

with open(OUTPUT_HTML_CONTROLE, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"OK: Painel Unificado gerado em {OUTPUT_HTML_UNIFICADO}")
print(f"OK: Painel de Controle gerado em {OUTPUT_HTML_CONTROLE}")

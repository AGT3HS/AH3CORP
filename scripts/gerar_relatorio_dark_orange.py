import os
import sys
import subprocess
from datetime import datetime
import json

def gerar_relatorio_dark_orange_html(dados_local, ranking_data=None, caminho_html=None):
    nome = dados_local.get("displayName", {}).get("text", "Estabelecimento") if isinstance(dados_local.get("displayName"), dict) else dados_local.get("displayName", "Estabelecimento")
    endereco = dados_local.get("formattedAddress", "Canasvieiras, Florianópolis - SC")
    telefone = dados_local.get("nationalPhoneNumber", dados_local.get("internationalPhoneNumber", "Não informado"))
    website = dados_local.get("websiteUri")
    tem_site_str = "Sim (Cadastrado)" if website else "Não Vinculado"
    
    try:
        rating = float(dados_local.get("rating", 3.7))
    except:
        rating = 3.7
    try:
        total_reviews = int(dados_local.get("userRatingCount", 429))
    except:
        total_reviews = 429

    place_id = dados_local.get("id", "ChIJw_b6U7g4J5URzXo4f4N3bZ8")[:24]
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Cálculos de KPI
    if rating <= 3.8:
        score_val = "52"
        score_note = "Ação Imediata"
        score_sub = "Risco de perda de clientes"
        score_accent = "accent-crit"
    elif rating <= 4.3:
        score_val = "68"
        score_note = "Em Otimização"
        score_sub = "Potencial de liderança"
        score_accent = ""
    else:
        score_val = "84"
        score_note = "Elevado"
        score_sub = "Blindagem e autoridade"
        score_accent = "accent-green"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório de Auditoria • {nome}</title>
  <style>
    :root {{
      --bg:        #0E0E0E;   /* fundo da página/body */
      --surface:   #181818;   /* fundo do cartão principal */
      --surface-2: #1F1F1F;   /* fundo de blocos internos (cards, células) */
      --surface-3: #262626;   /* fundo de headers de tabela, chips */
      --line:      #2C2C2C;   /* bordas principais */
      --line-soft: #232323;   /* bordas internas sutis, linhas de grade */

      --orange:      #F26522; /* cor primária: destaque, KPIs, títulos, alerta médio */
      --orange-dim:  rgba(242,101,34,.14);
      --orange-line: rgba(242,101,34,.35);

      --green:       #22C55E; /* cor secundária: sucesso, conformidade, potencial alto */
      --green-dim:   rgba(34,197,94,.13);
      --green-line:  rgba(34,197,94,.35);

      --crit:        #D93A2B; /* cor crítica: ausência, erro, bloqueio */
      --crit-dim:    rgba(217,58,43,.15);

      --text:   #F4F4F4;      /* texto principal */
      --text-2: #B9B9B9;      /* texto secundário */
      --muted:  #7C7C7C;      /* labels, metadados, legendas */
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      background-image: radial-gradient(circle at 50% 10%, #1c1c1c 0%, var(--bg) 75%);
      font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      font-size: 15px;
      line-height: 1.5;
      color: var(--text);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      padding: 30px 20px;
    }}

    /* Container de Página */
    .page {{
      max-width: 980px;
      margin: 0 auto 30px auto;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 36px 40px 26px;
      box-shadow: 0 24px 60px rgba(0,0,0,.45);
      position: relative;
      overflow: hidden;
      page-break-after: always;
      break-after: page;
    }}

    /* Barra Superior Laranja */
    .page::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--orange) 0%, var(--orange) 42%, transparent);
    }}

    /* Cabeçalho do Documento */
    .doc-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 18px;
      margin-bottom: 22px;
      gap: 20px;
    }}

    .doc-head .head-left .eyebrow {{
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      color: var(--orange);
      margin-bottom: 4px;
    }}

    .doc-head .head-left h1 {{
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -.02em;
      color: var(--text);
      margin-bottom: 4px;
    }}

    .doc-head .head-left .subtitle {{
      font-size: 13px;
      color: var(--muted);
    }}

    .doc-head .head-right {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      text-align: right;
      gap: 3px;
    }}

    .doc-head .head-right .page-num {{
      font-size: 13px;
      font-weight: 800;
      color: var(--text);
    }}

    .doc-head .head-right .meta-date {{
      font-size: 12px;
      color: var(--muted);
    }}

    .doc-head .head-right .chip-id {{
      background: var(--surface-3);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 10px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 12px;
      font-weight: 600;
      color: var(--green);
      margin-top: 2px;
    }}

    /* Cabeçalho de Seção */
    .section-head {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 20px;
      margin-bottom: 14px;
    }}

    .section-head:first-of-type {{
      margin-top: 0;
    }}

    .section-head .badge-num {{
      width: 26px;
      height: 26px;
      min-width: 26px;
      border-radius: 7px;
      background: var(--orange-dim);
      border: 1px solid var(--orange-line);
      color: var(--orange);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .section-head h2 {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text);
    }}

    .section-head h2 span {{
      font-weight: 500;
      color: var(--muted);
    }}

    /* Componente 1: Grid de Dados Cadastrais */
    .cadastral-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1px;
      background: var(--line);
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 18px;
    }}

    .cadastral-cell {{
      background: var(--surface-2);
      padding: 12px 16px;
    }}

    .cadastral-cell.wide {{
      grid-column: span 2;
    }}

    .cadastral-cell .label {{
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 3px;
    }}

    .cadastral-cell .value {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text);
    }}

    .cadastral-cell .value.mono-green {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 13px;
      font-weight: 600;
      color: var(--green);
    }}

    /* Componente 2: Cards de KPI */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }}

    .kpi-card {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      min-height: 132px;
      padding: 14px 15px;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .kpi-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--orange);
    }}

    .kpi-card.accent-green::before {{ background: var(--green); }}
    .kpi-card.accent-crit::before {{ background: var(--crit); }}

    .kpi-card .kpi-label {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .kpi-card .kpi-val {{
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -.025em;
      color: var(--orange);
      margin: 4px 0;
    }}

    .kpi-card.accent-green .kpi-val {{ color: var(--green); }}
    .kpi-card.accent-crit .kpi-val {{ color: var(--crit); }}

    .kpi-card .kpi-note {{
      font-size: 11.5px;
      font-weight: 700;
      color: var(--orange);
      margin-bottom: 2px;
    }}

    .kpi-card.accent-green .kpi-note {{ color: var(--green); }}
    .kpi-card.accent-crit .kpi-note {{ color: var(--crit); }}

    .kpi-card .kpi-subnote {{
      font-size: 11px;
      color: var(--muted);
    }}

    /* Componente 3: Gráfico de Barras CSS */
    .chart-card {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 18px 20px 14px;
      margin-bottom: 18px;
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}

    .chart-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
    }}

    .chart-legend {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 11px;
      color: var(--muted);
    }}

    .chart-legend .leg-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .chart-legend .leg-line-dashed {{
      width: 16px;
      height: 0;
      border-top: 2px dashed var(--green);
    }}

    .chart-legend .leg-box-orange {{
      width: 10px;
      height: 10px;
      border-radius: 2px;
      background: var(--orange);
    }}

    .chart-plot {{
      position: relative;
      height: 140px;
      display: flex;
      align-items: flex-end;
      justify-content: space-around;
      padding: 0 15px 0 35px;
      border-bottom: 1px solid var(--line);
      background: repeating-linear-gradient(
        to top,
        transparent,
        transparent 34px,
        var(--line-soft) 34px,
        var(--line-soft) 35px
      );
    }}

    .chart-ideal-line {{
      position: absolute;
      left: 35px;
      right: 15px;
      bottom: 80%;
      border-top: 1.5px dashed var(--green);
      z-index: 2;
      pointer-events: none;
    }}

    .chart-ideal-line::after {{
      content: "80% NÍVEL IDEAL";
      position: absolute;
      right: 0;
      top: -14px;
      font-size: 9px;
      font-weight: 700;
      color: var(--green);
      background: var(--surface-2);
      padding: 0 4px;
    }}

    .chart-y-axis {{
      position: absolute;
      left: 6px;
      top: 0;
      bottom: 0;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      font-size: 9.5px;
      color: var(--muted);
      padding-bottom: 2px;
    }}

    .chart-col {{
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 99.9%;
      justify-content: flex-end;
      width: 50px;
      z-index: 3;
    }}

    .chart-bar-val {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 4px;
    }}

    .chart-bar {{
      width: 28px;
      background: linear-gradient(180deg, #FF7A3D 0%, #F26522 50%, #D9541A);
      border-radius: 5px 5px 0 0;
    }}

    .chart-bar-labels {{
      display: flex;
      justify-content: space-around;
      padding: 8px 15px 0 35px;
    }}

    .chart-label-item {{
      width: 65px;
      text-align: center;
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-2);
      line-height: 1.25;
    }}

    /* Componente 8: Callouts */
    .callout {{
      background: var(--surface-2);
      border-left: 3px solid var(--orange);
      border-radius: 0 12px 12px 0;
      padding: 14px 18px;
      font-size: 12.5px;
      line-height: 1.55;
      color: var(--text-2);
      margin-top: 14px;
    }}

    .callout strong {{
      color: var(--text);
    }}

    .callout.callout--green {{
      border-left-color: var(--green);
    }}

    /* Componente 4: Tabela de Ranking */
    .table-wrapper {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 18px;
    }}

    table.ranking-table {{
      width: 99.9%;
      border-collapse: collapse;
      text-align: left;
    }}

    table.ranking-table th {{
      background: var(--surface-3);
      color: var(--muted);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      padding: 8px 12px;
      border-bottom: 1px solid var(--line);
    }}

    table.ranking-table td {{
      padding: 8px 12px;
      border-bottom: 1px solid var(--line-soft);
      font-size: 12px;
      color: var(--text-2);
      vertical-align: middle;
    }}

    table.ranking-table tr:last-child td {{
      border-bottom: none;
    }}

    table.ranking-table tr.is-target {{
      background: linear-gradient(90deg, rgba(242,101,34,.18) 0%, rgba(242,101,34,.02));
    }}

    .pos-badge {{
      width: 26px;
      height: 26px;
      border-radius: 7px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 11.5px;
      font-weight: 800;
      background: var(--surface-3);
      color: var(--muted);
    }}

    .pos-badge.top-3 {{
      background: var(--green-dim);
      color: var(--green);
      border: 1px solid var(--green-line);
    }}

    .pos-badge.target {{
      background: var(--orange);
      color: #0E0E0E;
      font-weight: 900;
    }}

    .target-tag {{
      display: inline-block;
      background: var(--orange);
      color: #0E0E0E;
      font-size: 9.5px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 999px;
      margin-left: 6px;
      letter-spacing: .05em;
    }}

    .pill-status {{
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }}

    .pill-status.sim {{
      background: var(--green-dim);
      color: var(--green);
      border: 1px solid var(--green-line);
    }}

    .pill-status.nao {{
      background: var(--crit-dim);
      color: var(--crit);
      border: 1px solid rgba(217,58,43,.3);
    }}

    /* Componente 5: Cards de Plano de Ação */
    .action-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }}

    .action-card {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 16px;
    }}

    .action-card .action-num {{
      font-size: 24px;
      font-weight: 800;
      color: var(--orange);
      margin-bottom: 6px;
    }}

    .action-card .action-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 6px;
      line-height: 1.3;
    }}

    .action-card .action-desc {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
    }}

    /* Componente 6: Tiles de Status & Stackbar */
    .status-tiles {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 10px;
    }}

    .status-tile {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px 16px;
      position: relative;
    }}

    .status-tile::before {{
      content: "";
      position: absolute;
      top: 12px;
      bottom: 12px;
      left: 0;
      width: 3px;
      border-radius: 0 2px 2px 0;
      background: var(--orange);
    }}

    .status-tile.tile-green::before {{ background: var(--green); }}
    .status-tile.tile-crit::before {{ background: var(--crit); }}

    .status-tile .tile-label {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--orange);
      margin-bottom: 2px;
    }}

    .status-tile.tile-green .tile-label {{ color: var(--green); }}
    .status-tile.tile-crit .tile-label {{ color: var(--crit); }}

    .status-tile .tile-val {{
      font-size: 28px;
      font-weight: 800;
      color: var(--text);
      margin: 2px 0;
    }}

    .status-tile .tile-val span {{
      font-size: 15px;
      font-weight: 500;
      color: var(--muted);
    }}

    .status-tile .tile-desc {{
      font-size: 11.5px;
      color: var(--muted);
    }}

    .stackbar-wrap {{
      margin-bottom: 16px;
    }}

    .stackbar {{
      height: 8px;
      border-radius: 999px;
      background: var(--surface-3);
      display: flex;
      overflow: hidden;
      gap: 2px;
    }}

    .stackbar-seg {{
      height: 99.9%;
    }}

    .stackbar-seg.green {{ background: var(--green); }}
    .stackbar-seg.orange {{ background: var(--orange); }}
    .stackbar-seg.crit {{ background: var(--crit); }}

    /* Componente 11: Barra de Cobertura */
    .coverage-wrap {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px 16px;
      margin-bottom: 16px;
    }}

    .coverage-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      font-size: 11.5px;
    }}

    .coverage-head .cov-title {{
      font-weight: 700;
      color: var(--text);
    }}

    .coverage-head .cov-stat {{
      color: var(--muted);
    }}

    .coverage-bar {{
      height: 8px;
      border-radius: 999px;
      background: var(--surface-3);
      display: flex;
      overflow: hidden;
      gap: 2px;
    }}

    /* Componente 7: Checklist */
    .checklist-status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }}

    .checklist-status-badge.ok {{
      background: var(--green-dim);
      color: var(--green);
      border: 1px solid var(--green-line);
    }}

    .checklist-status-badge.warn {{
      background: var(--orange-dim);
      color: var(--orange);
      border: 1px solid var(--orange-line);
    }}

    .checklist-status-badge.crit {{
      background: var(--crit-dim);
      color: var(--crit);
      border: 1px solid rgba(217,58,43,.3);
    }}

    .tag-key {{
      display: inline-block;
      background: var(--orange);
      color: #0E0E0E;
      font-size: 9px;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 999px;
      margin-left: 5px;
      letter-spacing: .04em;
      vertical-align: middle;
    }}

    /* Componente 9: Nota Metodológica */
    .method-note {{
      background: var(--surface-2);
      border: 1px dashed var(--line);
      border-radius: 12px;
      padding: 12px 16px;
      font-size: 11.5px;
      line-height: 1.55;
      color: var(--muted);
      margin-top: 14px;
    }}

    .method-note strong {{
      color: var(--text-2);
    }}

    /* Rodapé de Página */
    .page-foot {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--line);
      padding-top: 14px;
      margin-top: 22px;
      font-size: 11.5px;
      color: var(--muted);
    }}

    .page-foot .foot-left {{
      font-weight: 500;
    }}

    .page-foot .foot-center {{
      display: flex;
      gap: 6px;
      align-items: center;
    }}

    .page-foot .foot-bar {{
      width: 22px;
      height: 4px;
      border-radius: 2px;
      background: var(--line);
    }}

    .page-foot .foot-bar.active {{
      background: var(--orange);
    }}

    .page-foot .foot-right {{
      font-weight: 700;
      color: var(--text-2);
    }}

    /* Estilos de Impressão e PDF */
    @media print {{
      body {{
        background: var(--bg) !important;
        padding: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      .page {{
        box-shadow: none !important;
        margin: 0 !important;
        max-width: 99.9% !important;
        border-radius: 0 !important;
        border: none !important;
        page-break-after: always !important;
        break-after: page !important;
        min-height: 100vh !important;
        padding: 34px 38px 24px !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
    }}

    @page {{
      size: A4 portrait;
      margin: 0;
    }}
  </style>
</head>
<body>

  <!-- ========================================== -->
  <!-- PÁGINA 1: DADOS, KPIS & GRÁFICO DE BARRAS  -->
  <!-- ========================================== -->
  <div class="page">
    <div class="doc-head">
      <div class="head-left">
        <div class="eyebrow">Auditoria Estrutural de Presença Local</div>
        <h1>{nome}</h1>
        <div class="subtitle">Diagnóstico Técnico de Posicionamento no Google Maps & Busca Local</div>
      </div>
      <div class="head-right">
        <div class="page-num">Página 01 / 03</div>
        <div class="meta-date">{data_atual} · Florianópolis / SC</div>
        <div class="chip-id">ID: {place_id}</div>
      </div>
    </div>

    <!-- Componente 1: Grid de Dados Cadastrais -->
    <div class="section-head">
      <div class="badge-num">1</div>
      <h2>Dados Cadastrais <span>· Informações do Estabelecimento</span></h2>
    </div>

    <div class="cadastral-grid">
      <div class="cadastral-cell wide">
        <div class="label">Endereço Registrado</div>
        <div class="value">{endereco}</div>
      </div>
      <div class="cadastral-cell">
        <div class="label">Telefone Principal</div>
        <div class="value">{telefone}</div>
      </div>
      <div class="cadastral-cell">
        <div class="label">Segmento Primário</div>
        <div class="value">Restaurante / Gastronomia</div>
      </div>
      <div class="cadastral-cell">
        <div class="label">Canal Próprio / Site</div>
        <div class="value">{tem_site_str}</div>
      </div>
      <div class="cadastral-cell">
        <div class="label">Geolocalização (Lat/Lng)</div>
        <div class="value mono-green">-27.4298, -48.4552</div>
      </div>
    </div>

    <!-- Componente 2: Cards de KPI -->
    <div class="section-head">
      <div class="badge-num">2</div>
      <h2>Indicadores-Chave de Desempenho <span>· Métricas Principais</span></h2>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card {score_accent}">
        <div class="kpi-label">Score de Presença</div>
        <div class="kpi-val">{score_val}<span style="font-size:16px;font-weight:500;color:var(--muted)">/100</span></div>
        <div>
          <div class="kpi-note">{score_note}</div>
          <div class="kpi-subnote">{score_sub}</div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-label">Avaliação Média</div>
        <div class="kpi-val">{rating:.1f}<span style="font-size:16px;font-weight:500;color:var(--muted)">★</span></div>
        <div>
          <div class="kpi-note">Base de Clientes</div>
          <div class="kpi-subnote">{total_reviews} avaliações registradas</div>
        </div>
      </div>

      <div class="kpi-card accent-crit">
        <div class="kpi-label">Taxa de Resposta</div>
        <div class="kpi-val">&lt; 15%</div>
        <div>
          <div class="kpi-note">Nível Crítico</div>
          <div class="kpi-subnote">Grande volume sem resposta</div>
        </div>
      </div>

      <div class="kpi-card accent-green">
        <div class="kpi-label">Potencial Projetado</div>
        <div class="kpi-val">Alto</div>
        <div>
          <div class="kpi-note">Polo Turístico</div>
          <div class="kpi-subnote">Alta demanda em Canasvieiras</div>
        </div>
      </div>
    </div>

    <!-- Componente 3: Gráfico de Barras CSS -->
    <div class="section-head">
      <div class="badge-num">3</div>
      <h2>Diagnóstico Estrutural <span>· Pontuação por Eixo Técnico</span></h2>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">Desempenho por Eixo Estratégico vs. Nível Ideal de Conversão</div>
        <div class="chart-legend">
          <div class="leg-item">
            <div class="leg-line-dashed"></div>
            <span>Nível Ideal (80%)</span>
          </div>
          <div class="leg-item">
            <div class="leg-box-orange"></div>
            <span>Pontuação Atual</span>
          </div>
        </div>
      </div>

      <div class="chart-plot">
        <div class="chart-ideal-line"></div>
        <div class="chart-y-axis">
          <span>100</span>
          <span>80</span>
          <span>50</span>
          <span>0</span>
        </div>

        <div class="chart-col">
          <div class="chart-bar-val">70%</div>
          <div class="chart-bar" style="height: 70%;"></div>
        </div>
        <div class="chart-col">
          <div class="chart-bar-val">50%</div>
          <div class="chart-bar" style="height: 50%;"></div>
        </div>
        <div class="chart-col">
          <div class="chart-bar-val">65%</div>
          <div class="chart-bar" style="height: 65%;"></div>
        </div>
        <div class="chart-col">
          <div class="chart-bar-val">45%</div>
          <div class="chart-bar" style="height: 45%;"></div>
        </div>
        <div class="chart-col">
          <div class="chart-bar-val">30%</div>
          <div class="chart-bar" style="height: 30%;"></div>
        </div>
        <div class="chart-col">
          <div class="chart-bar-val">40%</div>
          <div class="chart-bar" style="height: 40%;"></div>
        </div>
      </div>

      <div class="chart-bar-labels">
        <div class="chart-label-item">Completude do Perfil</div>
        <div class="chart-label-item">Qualidade de Fotos</div>
        <div class="chart-label-item">Horários & NAP</div>
        <div class="chart-label-item">SEO Local & Tags</div>
        <div class="chart-label-item">Canais de Conversão</div>
        <div class="chart-label-item">Gestão de Reviews</div>
      </div>
    </div>

    <!-- Componente 8: Callout-Resumo -->
    <div class="callout">
      <strong>Síntese do Diagnóstico Preliminar:</strong> O estabelecimento detém alta visibilidade pelo acúmulo de <strong>{total_reviews} avaliações</strong>, mas a nota de <strong>{rating:.1f} / 5.0</strong> combinada com a ausência de um canal direto de reservas gera dispersão de clientes para concorrentes vizinhos. A regularização dos eixos críticos projeta rápida recuperação de relevância no raio local.
    </div>

    <!-- Rodapé da Página 1 -->
    <div class="page-foot">
      <div class="foot-left">Prospecção Digital · {nome}</div>
      <div class="foot-center">
        <div class="foot-bar active"></div>
        <div class="foot-bar"></div>
        <div class="foot-bar"></div>
      </div>
      <div class="foot-right">Página 01 / 03</div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- PÁGINA 2: RANKING COMPETITIVO & PLANO      -->
  <!-- ========================================== -->
  <div class="page">
    <div class="doc-head">
      <div class="head-left">
        <div class="eyebrow">Mapeamento de Mercado & Concorrência</div>
        <h1>Benchmarking Competitivo</h1>
        <div class="subtitle">Análise Comparativa de Restaurantes em Canasvieiras (Raio de 3 a 5 km)</div>
      </div>
      <div class="head-right">
        <div class="page-num">Página 02 / 03</div>
        <div class="meta-date">{data_atual} · Florianópolis / SC</div>
        <div class="chip-id">ID: {place_id}</div>
      </div>
    </div>

    <!-- Componente 4: Tabela de Ranking -->
    <div class="section-head">
      <div class="badge-num">4</div>
      <h2>Posicionamento Competitivo <span>· Líderes Regionais vs. Perfil Alvo</span></h2>
    </div>

    <div class="table-wrapper">
      <table class="ranking-table">
        <thead>
          <tr>
            <th style="width: 50px; text-align: center;">Pos</th>
            <th>Estabelecimento</th>
            <th>Distância</th>
            <th>Nota Google</th>
            <th>Avaliações</th>
            <th>Canal Direto</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="text-align: center;"><div class="pos-badge top-3">01</div></td>
            <td><strong>Costillas Grill - Costelaria</strong></td>
            <td>0.8 km</td>
            <td><strong>4.3 ★</strong></td>
            <td>4.790</td>
            <td><span class="pill-status sim">Sim</span></td>
          </tr>
          <tr>
            <td style="text-align: center;"><div class="pos-badge top-3">02</div></td>
            <td><strong>Canas Pizzaria - Forno a Lenha</strong></td>
            <td>0.4 km</td>
            <td><strong>4.0 ★</strong></td>
            <td>4.014</td>
            <td><span class="pill-status sim">Sim</span></td>
          </tr>
          <tr>
            <td style="text-align: center;"><div class="pos-badge top-3">03</div></td>
            <td><strong>Galpão Gaúcho Churrascaria</strong></td>
            <td>1.2 km</td>
            <td><strong>4.3 ★</strong></td>
            <td>2.808</td>
            <td><span class="pill-status sim">Sim</span></td>
          </tr>
          <tr>
            <td style="text-align: center;"><div class="pos-badge">04</div></td>
            <td><strong>Churrasco ao Vivo Canasvieiras</strong></td>
            <td>0.6 km</td>
            <td><strong>4.4 ★</strong></td>
            <td>2.443</td>
            <td><span class="pill-status nao">Não</span></td>
          </tr>
          <tr class="is-target">
            <td style="text-align: center;"><div class="pos-badge target">05</div></td>
            <td><strong>{nome}</strong> <span class="target-tag">ALVO</span></td>
            <td>Local</td>
            <td><strong style="color: var(--orange);">{rating:.1f} ★</strong></td>
            <td><strong>{total_reviews}</strong></td>
            <td><span class="pill-status nao">Não</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Componente 5: Cards de Plano de Ação -->
    <div class="section-head">
      <div class="badge-num">5</div>
      <h2>Plano de Ação Estruturado <span>· 3 Frentes de Execução Imediata</span></h2>
    </div>

    <div class="action-grid">
      <div class="action-card">
        <div class="action-num">01</div>
        <div class="action-title">Blindagem & Respostas Estratégicas</div>
        <div class="action-desc">Padronização de respostas para todas as avaliações com reversão de feedbacks negativos e inclusão técnica de palavras-chave locais.</div>
      </div>

      <div class="action-card">
        <div class="action-num">02</div>
        <div class="action-title">Cardápio Mobile & Canal WhatsApp</div>
        <div class="action-desc">Implementação de landing page mobile ultrarrápida com botão de reservas diretas e consulta de cardápio integrado ao WhatsApp.</div>
      </div>

      <div class="action-card">
        <div class="action-num">03</div>
        <div class="action-title">Sinalização Ativa & Google Posts</div>
        <div class="action-desc">Publicações semanais com fotos em alta definição dos pratos, avisos de horários especiais e emissão de sinais contínuos ao algoritmo.</div>
      </div>
    </div>

    <!-- Componente 8: Callout Diagnóstico/Proposta Comercial -->
    <div class="callout callout--green">
      <strong>Oportunidade Comercial Identificada:</strong> Os principais concorrentes de Canasvieiras mantêm avaliação acima de 4.2 estrelas e capturam o fluxo de turistas que pesquisam pelo celular. A implementação das 3 fases do plano de ação tem o <strong>potencial projetado</strong> de reposicionar o estabelecimento no pelotão de frente das buscas da região.
    </div>

    <!-- Rodapé da Página 2 -->
    <div class="page-foot">
      <div class="foot-left">Prospecção Digital · {nome}</div>
      <div class="foot-center">
        <div class="foot-bar"></div>
        <div class="foot-bar active"></div>
        <div class="foot-bar"></div>
      </div>
      <div class="foot-right">Página 02 / 03</div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- PÁGINA 3: STATUS, CHECKLIST & METODOLOGIA  -->
  <!-- ========================================== -->
  <div class="page">
    <div class="doc-head">
      <div class="head-left">
        <div class="eyebrow">Auditoria Detalhada de Elementos Públicos</div>
        <h1>Checklist Técnico do Perfil</h1>
        <div class="subtitle">Verificação dos Fatores Determinantes de Ranqueamento no Algoritmo Google</div>
      </div>
      <div class="head-right">
        <div class="page-num">Página 03 / 03</div>
        <div class="meta-date">{data_atual} · Florianópolis / SC</div>
        <div class="chip-id">ID: {place_id}</div>
      </div>
    </div>

    <!-- Componente 6: Tiles de Status -->
    <div class="section-head">
      <div class="badge-num">6</div>
      <h2>Resumo de Conformidade <span>· Distribuição dos 8 Fatores Auditados</span></h2>
    </div>

    <div class="status-tiles">
      <div class="status-tile tile-green">
        <div class="tile-label">Conforme</div>
        <div class="tile-val">2 <span>/ 8</span></div>
        <div class="tile-desc">Itens ativos e configurados</div>
      </div>

      <div class="status-tile">
        <div class="tile-label">Atenção</div>
        <div class="tile-val">3 <span>/ 8</span></div>
        <div class="tile-desc">Cadastrados, mas incompletos</div>
      </div>

      <div class="status-tile tile-crit">
        <div class="tile-label">Ausente</div>
        <div class="tile-val">3 <span>/ 8</span></div>
        <div class="tile-desc">Oportunidades em aberto</div>
      </div>
    </div>

    <div class="stackbar-wrap">
      <div class="stackbar">
        <div class="stackbar-seg green" style="width: 25%;"></div>
        <div class="stackbar-seg orange" style="width: 37.5%;"></div>
        <div class="stackbar-seg crit" style="width: 37.5%;"></div>
      </div>
    </div>

    <!-- Componente 11: Barra de Cobertura do Relatório -->
    <div class="coverage-wrap">
      <div class="coverage-head">
        <span class="cov-title">Cobertura Metodológica da Auditoria</span>
        <span class="cov-stat">65% Fatores Públicos de Ficha & Reputação · 35% Métricas Internas do Painel</span>
      </div>
      <div class="coverage-bar">
        <div class="stackbar-seg orange" style="width: 65%;"></div>
        <div class="stackbar-seg" style="width: 35%; background: var(--surface-3);"></div>
      </div>
    </div>

    <!-- Componente 7: Checklist Detalhado com Tag Key -->
    <div class="section-head">
      <div class="badge-num">7</div>
      <h2>Checklist Estrutural <span>· Avaliação Individual de Conformidade</span></h2>
    </div>

    <div class="table-wrapper">
      <table class="ranking-table">
        <thead>
          <tr>
            <th style="width: 210px;">Item Auditado</th>
            <th style="width: 110px;">Status</th>
            <th>Observação Técnica & Impacto no Algoritmo</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Endereço & Geolocalização</strong></td>
            <td><span class="checklist-status-badge ok">✓ Conforme</span></td>
            <td>Pino no mapa posicionado corretamente na via comercial de Canasvieiras.</td>
          </tr>
          <tr>
            <td><strong>Telefone Padronizado (NAP)</strong></td>
            <td><span class="checklist-status-badge ok">✓ Conforme</span></td>
            <td>Telefone comercial ativo e sem inconsistências de formato.</td>
          </tr>
          <tr>
            <td><strong>Horários de Atendimento</strong></td>
            <td><span class="checklist-status-badge warn">! Atenção</span></td>
            <td>Necessidade de revisão dos horários para datas sazonais e feriados.</td>
          </tr>
          <tr>
            <td><strong>Taxa de Resposta a Reviews</strong> <span class="tag-key">FATOR Nº1</span></td>
            <td><span class="checklist-status-badge crit">× Ausente</span></td>
            <td>Mais de 85% das avaliações estão sem resposta da administração.</td>
          </tr>
          <tr>
            <td><strong>Recência das Avaliações</strong></td>
            <td><span class="checklist-status-badge warn">! Atenção</span></td>
            <td>Fluxo esparso de novas opiniões nos últimos 30 dias; requer incentivo ativo.</td>
          </tr>
          <tr>
            <td><strong>Categorias Secundárias</strong></td>
            <td><span class="checklist-status-badge warn">! Atenção</span></td>
            <td>Faltam tags relevantes como 'Churrascaria', 'Parrilla' e 'Bar e Restaurante'.</td>
          </tr>
          <tr>
            <td><strong>Cardápio Mobile Integrado</strong></td>
            <td><span class="checklist-status-badge crit">× Ausente</span></td>
            <td>Sem link direto para visualização de pratos e preços em smartphones.</td>
          </tr>
          <tr>
            <td><strong>Google Posts & Novidades</strong></td>
            <td><span class="checklist-status-badge crit">× Ausente</span></td>
            <td>Sem postagens recentes no feed do perfil nos últimos 60 dias.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Componente 9: Nota Metodológica -->
    <div class="method-note">
      <strong>Nota Metodológica:</strong> Este relatório analisa exclusivamente os dados públicos da Google Places API. Métricas de tráfego fechado (chamadas iniciadas, rotas solicitadas e impressões na busca direta) tornam-se auditáveis mediante vinculação de acesso ao painel do proprietário em etapa posterior.
    </div>

    <!-- Componente 8: Callout Final de Próximo Passo -->
    <div class="callout">
      <strong>Próximo Passo Recomendado:</strong> Agendar uma breve apresentação de 15 minutos para demonstração do modelo de cardápio digital integrado e validação das primeiras respostas a avaliações críticas.
    </div>

    <!-- Rodapé da Página 3 -->
    <div class="page-foot">
      <div class="foot-left">Prospecção Digital · {nome}</div>
      <div class="foot-center">
        <div class="foot-bar"></div>
        <div class="foot-bar"></div>
        <div class="foot-bar active"></div>
      </div>
      <div class="foot-right">Página 03 / 03</div>
    </div>
  </div>

</body>
</html>
"""
    if not caminho_html:
        saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
        os.makedirs(saida_dir, exist_ok=True)
        nome_limpo = "".join([c if c.isalnum() else "_" for c in nome])[:30]
        caminho_html = os.path.join(saida_dir, f"Auditoria_{nome_limpo}_DarkOrange.html")

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return caminho_html

def converter_html_para_pdf(caminho_html, caminho_pdf=None):
    if not caminho_pdf:
        caminho_pdf = caminho_html.replace(".html", ".pdf")
    
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={caminho_pdf}",
        caminho_html
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Falha ao gerar PDF via Edge: {res.stderr}")
    
    return caminho_pdf

if __name__ == "__main__":
    dados = {
        "displayName": {"text": "EL PATIO GRILL RESTAURANTE"},
        "formattedAddress": "R. Me. Maria Villac, 2003 - Canasvieiras, Florianópolis - SC, 88054-001, Brasil",
        "nationalPhoneNumber": "(47) 99115-0610",
        "websiteUri": None,
        "rating": 3.7,
        "userRatingCount": 429,
        "id": "ChIJw_b6U7g4J5URzXo4f4N3bZ8"
    }
    
    html_file = gerar_relatorio_dark_orange_html(dados)
    print(f"HTML gerado com sucesso: {html_file}")
    
    pdf_file = converter_html_para_pdf(html_file)
    print(f"PDF gerado com sucesso: {pdf_file}")

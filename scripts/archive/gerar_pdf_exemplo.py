import os
import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("C:/Users/Augusto/Desktop/AH3/.env")
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def buscar_place_detalhes(place_query):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.location,places.businessStatus,places.types,places.primaryTypeDisplayName,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours"
    }
    r = requests.post(url, headers=headers, json={"textQuery": place_query, "languageCode": "pt-BR", "maxResultCount": 1})
    if r.status_code == 200 and r.json().get("places"):
        return r.json()["places"][0]
    return None

def gerar_pdf_exemplo_canto_do_mar():
    print("[*] Coletando dados reais de Canto do Mar Ponta das Canas...")
    alvo = buscar_place_detalhes("Canto do Mar Ponta das Canas Florianopolis")
    
    nome = alvo.get("displayName", {}).get("text", "Canto do Mar Ponta das Canas")
    endereco = alvo.get("formattedAddress", "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC")
    telefone = alvo.get("nationalPhoneNumber", "(48) 3261-0872")
    website = alvo.get("websiteUri", "https://cantodomarfloripa.com.br")
    rating = float(alvo.get("rating", 4.6))
    total_reviews = int(alvo.get("userRatingCount", 178))
    place_id = alvo.get("id", "ChIJw_b6U7g4J5URzXo4f4N3bZ8")[:24]
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # 10 Concorrentes Reais (Mix Diretos + Cross-Nicho)
    concorrentes_mix = [
        {"pos": "01", "nome": "Gaivota", "tipo": "Cross-Nicho (Geral)", "dist": "0.30 km", "rating": "4.4 ★", "reviews": "335", "canal": "Não", "destaque": False},
        {"pos": "02", "nome": "Ocean House", "tipo": "Direto (Frutos do Mar)", "dist": "0.39 km", "rating": "4.6 ★", "reviews": "475", "canal": "Não", "destaque": False},
        {"pos": "03", "nome": "A Toca Choperia e Petiscaria", "tipo": "Cross-Nicho (Bar/Chopp)", "dist": "0.39 km", "rating": "4.9 ★", "reviews": "165", "canal": "Sim", "destaque": False},
        {"pos": "04", "nome": "Restaurante Mira Maré", "tipo": "Direto (Frutos do Mar)", "dist": "0.50 km", "rating": "4.5 ★", "reviews": "1.445", "canal": "Sim", "destaque": False},
        {"pos": "05", "nome": "Restaurante Garra Azul", "tipo": "Direto (Frutos do Mar)", "dist": "0.51 km", "rating": "4.3 ★", "reviews": "1.362", "canal": "Sim", "destaque": False},
        {"pos": "06", "nome": "Baleia Branca RestoBar", "tipo": "Direto (RestoBar Praia)", "dist": "0.52 km", "rating": "4.3 ★", "reviews": "72", "canal": "Sim", "destaque": False},
        {"pos": "07", "nome": "Ponta da Praia", "tipo": "Direto (Frutos do Mar)", "dist": "0.53 km", "rating": "4.7 ★", "reviews": "217", "canal": "Sim", "destaque": False},
        {"pos": "08", "nome": "Ratones Craft Beer", "tipo": "Cross-Nicho (Choperia/Pub)", "dist": "0.91 km", "rating": "4.8 ★", "reviews": "2.114", "canal": "Sim", "destaque": False},
        {"pos": "09", "nome": "Restaurante Marinheiro's", "tipo": "Direto (Frutos do Mar)", "dist": "1.14 km", "rating": "4.6 ★", "reviews": "444", "canal": "Sim", "destaque": False},
        {"pos": "10", "nome": "Restaurante Lula Floripa", "tipo": "Direto (Lagoinha do Norte)", "dist": "1.25 km", "rating": "4.6 ★", "reviews": "626", "canal": "Sim", "destaque": False},
    ]

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório Executivo de Auditoria • {nome}</title>
  <style>
    :root {{
      --bg:        #0B0F17;
      --surface:   #111827;
      --surface-2: #1E293B;
      --surface-3: #334155;
      --line:      #334155;
      --line-soft: #1E293B;
      --orange:    #F97316;
      --orange-dim: rgba(249, 115, 22, 0.12);
      --green:     #10B981;
      --green-dim:  rgba(16, 185, 129, 0.12);
      --red:       #EF4444;
      --red-dim:   rgba(239, 68, 68, 0.12);
      --text:      #F8FAFC;
      --text-muted:#94A3B8;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      font-size: 13.5px;
      line-height: 1.45;
      color: var(--text);
      padding: 20px;
    }}

    .page {{
      max-width: 960px;
      margin: 0 auto 25px auto;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 30px 36px 24px;
      page-break-after: always;
      break-after: page;
      position: relative;
    }}

    .page::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--orange) 0%, #EA580C 50%, transparent);
      border-radius: 14px 14px 0 0;
    }}

    .doc-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 18px;
      margin-bottom: 20px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      font-weight: 700;
      color: var(--orange);
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .brand-dot {{ width: 8px; height: 8px; background: var(--orange); border-radius: 50%; }}

    h1 {{ font-size: 22px; font-weight: 800; color: #FFFFFF; margin-top: 4px; }}
    .subtitle {{ font-size: 13px; color: var(--text-muted); }}

    .head-right {{ text-align: right; font-size: 11px; color: var(--text-muted); }}
    .chip-id {{
      display: inline-block;
      background: var(--surface-2);
      border: 1px solid var(--line);
      padding: 3px 8px;
      border-radius: 6px;
      font-family: monospace;
      margin-top: 5px;
      color: var(--orange);
    }}

    /* Grid de KPIs */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 22px;
    }}

    .kpi-card {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 14px;
    }}

    .kpi-label {{ font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }}
    .kpi-val {{ font-size: 24px; font-weight: 800; color: #FFFFFF; margin: 4px 0; }}
    .kpi-val.orange {{ color: var(--orange); }}
    .kpi-val.green {{ color: var(--green); }}
    .kpi-sub {{ font-size: 11px; color: var(--text-muted); }}

    /* Seções */
    .section-head {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 18px 0 12px 0;
    }}
    .badge-num {{
      background: var(--orange);
      color: #FFFFFF;
      width: 22px;
      height: 22px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
    }}
    h2 {{ font-size: 15px; font-weight: 700; color: #FFFFFF; }}
    h2 span {{ color: var(--text-muted); font-weight: 400; font-size: 13px; }}

    /* Tabelas */
    .table-wrapper {{
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 18px;
    }}
    table {{ width: 99.9%; border-collapse: collapse; text-align: left; font-size: 12.5px; }}
    th {{
      background: var(--surface-3);
      color: #FFFFFF;
      padding: 10px 12px;
      font-weight: 600;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    td {{
      padding: 9px 12px;
      border-top: 1px solid var(--line-soft);
      color: var(--text);
    }}
    tr.is-target {{
      background: rgba(249, 115, 22, 0.12);
      border-left: 3px solid var(--orange);
      font-weight: 700;
    }}
    tr.is-target td {{ color: #FFFFFF; }}

    .pos-badge {{
      display: inline-block;
      width: 24px;
      height: 24px;
      line-height: 24px;
      text-align: center;
      border-radius: 6px;
      font-weight: 700;
      font-size: 11px;
      background: var(--surface-3);
      color: var(--text-muted);
    }}
    .pos-badge.target {{ background: var(--orange); color: #FFFFFF; }}

    .target-tag {{
      display: inline-block;
      background: var(--orange);
      color: #FFFFFF;
      font-size: 10px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 4px;
      margin-left: 6px;
    }}

    .pill {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
    }}
    .pill.sim {{ background: var(--green-dim); color: var(--green); border: 1px solid rgba(16,185,129,0.3); }}
    .pill.nao {{ background: var(--red-dim); color: var(--red); border: 1px solid rgba(239,68,68,0.3); }}

    /* Cards de Diagnóstico e Ação */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 16px;
    }}
    .box {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 14px;
    }}
    .box-title {{ font-size: 13px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }}
    .box-p {{ font-size: 12px; color: var(--text-muted); line-height: 1.5; }}

    .action-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 20px;
    }}
    .action-card {{
      background: var(--surface-2);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 14px;
      border-top: 3px solid var(--orange);
    }}
    .action-num {{ font-size: 16px; font-weight: 800; color: var(--orange); margin-bottom: 4px; }}
    .action-title {{ font-size: 12.5px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px; }}
    .action-desc {{ font-size: 11.5px; color: var(--text-muted); line-height: 1.45; }}

    .callout {{
      background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(30, 41, 59, 0.6) 99.9%);
      border: 1px solid rgba(249, 115, 22, 0.4);
      border-radius: 10px;
      padding: 16px;
      margin-top: 10px;
    }}
    .callout-title {{ font-size: 14px; font-weight: 800; color: var(--orange); margin-bottom: 4px; }}
    .callout-text {{ font-size: 12px; color: #E2E8F0; line-height: 1.5; }}

    .page-foot {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--line);
      padding-top: 14px;
      margin-top: 20px;
      font-size: 11px;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <!-- PÁGINA 1: VISÃO GERAL & AUDITORIA DE PRESENÇA -->
  <div class="page">
    <div class="doc-head">
      <div>
        <div class="brand"><div class="brand-dot"></div> AH3 Gestão & Presença Local</div>
        <h1>Relatório de Diagnóstico & Presença Local</h1>
        <div class="subtitle">Auditoria de Visibilidade, Avaliações e Conversão Digital</div>
      </div>
      <div class="head-right">
        <div><strong>Página 01 / 02</strong></div>
        <div>{data_atual} · Florianópolis / SC</div>
        <div class="chip-id">ID: {place_id}</div>
      </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Nota Google</div>
        <div class="kpi-val orange">{rating:.1f} ★</div>
        <div class="kpi-sub">Média de avaliações</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total de Reviews</div>
        <div class="kpi-val">{total_reviews}</div>
        <div class="kpi-sub">Volume consolidado</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Canal Direto</div>
        <div class="kpi-val green">Ativo</div>
        <div class="kpi-sub">Site / Cardápio linkado</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Score de Liderança</div>
        <div class="kpi-val orange">58 / 100</div>
        <div class="kpi-sub">Potencial de expansão</div>
      </div>
    </div>

    <!-- Diagnóstico Estratégico -->
    <div class="section-head">
      <div class="badge-num">1</div>
      <h2>Raio-X de Presença Local <span>· {nome}</span></h2>
    </div>

    <div class="grid-2">
      <div class="box">
        <div class="box-title">📍 Endereço & Cobertura</div>
        <div class="box-p">{endereco}</div>
        <div class="box-p" style="margin-top: 6px;"><strong>Telefone:</strong> {telefone}</div>
      </div>
      <div class="box">
        <div class="box-title">⚠️ Oportunidade Crítica de Volume</div>
        <div class="box-p">Embora a nota ({rating:.1f}★) seja excelente, o volume de {total_reviews} avaliações coloca o restaurante abaixo do top of mind da orla, onde concorrentes a 500m já superam 1.400 avaliações.</div>
      </div>
    </div>

    <!-- Pilares de Otimização -->
    <div class="section-head">
      <div class="badge-num">2</div>
      <h2>Pilares de Atração & Conversão Local</h2>
    </div>

    <div class="grid-2">
      <div class="box">
        <div class="box-title">💬 Blindagem & Volume de Avaliações</div>
        <div class="box-p">Implementação de processo sistemático de solicitação de avaliações pós-refeição e resposta estratégica a todas as avaliações para ganhar relevância no ranqueamento.</div>
      </div>
      <div class="box">
        <div class="box-title">📲 Conversão Direta no WhatsApp</div>
        <div class="box-p">Facilidade de acesso ao cardápio e botão de reserva rápida para transformar turistas navegando no Google Maps em clientes na mesa com zero fricção.</div>
      </div>
    </div>

    <div class="page-foot">
      <div>AH3 • Inteligência & Otimização de Presença Local</div>
      <div>Confidencial · Elaborado para {nome}</div>
    </div>
  </div>

  <!-- PÁGINA 2: BENCHMARKING DE 10 CONCORRENTES (DIRETOS + CROSS-NICHO) -->
  <div class="page">
    <div class="doc-head">
      <div>
        <div class="brand"><div class="brand-dot"></div> AH3 Gestão & Presença Local</div>
        <h1>Benchmarking Competitivo Hiperlocal</h1>
        <div class="subtitle">Mapeamento de 10 Polos Concorrentes (Praia, Frutos do Mar & Cross-Nicho)</div>
      </div>
      <div class="head-right">
        <div><strong>Página 02 / 02</strong></div>
        <div>{data_atual} · Florianópolis / SC</div>
        <div class="chip-id">Ponta das Canas & Microrregião</div>
      </div>
    </div>

    <!-- Tabela de Ranking Mix 10 -->
    <div class="section-head">
      <div class="badge-num">3</div>
      <h2>Posicionamento Competitivo <span>· Raio Imediato (0.3 a 1.3 km)</span></h2>
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th style="width: 45px; text-align: center;">Pos</th>
            <th>Estabelecimento</th>
            <th>Proposta / Categoria</th>
            <th style="text-align: center;">Distância</th>
            <th style="text-align: center;">Nota Google</th>
            <th style="text-align: center;">Avaliações</th>
            <th style="text-align: center;">Canal Direto</th>
          </tr>
        </thead>
        <tbody>
          <tr class="is-target">
            <td style="text-align: center;"><div class="pos-badge target">•</div></td>
            <td><strong>{nome}</strong> <span class="target-tag">ALVO</span></td>
            <td>Direto (Frutos do Mar / Praia)</td>
            <td style="text-align: center;">Local</td>
            <td style="text-align: center; color: var(--orange);"><strong>{rating:.1f} ★</strong></td>
            <td style="text-align: center;"><strong>{total_reviews}</strong></td>
            <td style="text-align: center;"><span class="pill sim">Sim</span></td>
          </tr>
"""

    for c in concorrentes_mix:
        pill_cls = "sim" if c["canal"] == "Sim" else "nao"
        is_cross = "Cross-Nicho" in c["tipo"]
        tipo_style = "color: #94A3B8; font-style: italic;" if is_cross else "color: #E2E8F0;"
        html_content += f"""
          <tr>
            <td style="text-align: center;"><div class="pos-badge">{c['pos']}</div></td>
            <td><strong>{c['nome']}</strong></td>
            <td style="{tipo_style}">{c['tipo']}</td>
            <td style="text-align: center; color: var(--text-muted);">{c['dist']}</td>
            <td style="text-align: center;"><strong>{c['rating']}</strong></td>
            <td style="text-align: center;">{c['reviews']}</td>
            <td style="text-align: center;"><span class="pill {pill_cls}">{c['canal']}</span></td>
          </tr>
"""

    html_content += f"""
        </tbody>
      </table>
    </div>

    <!-- Plano de Ação Estruturado -->
    <div class="section-head">
      <div class="badge-num">4</div>
      <h2>Plano de Ação para Captura de Liderança</h2>
    </div>

    <div class="action-grid">
      <div class="action-card">
        <div class="action-num">01</div>
        <div class="action-title">Alavancagem de Volume</div>
        <div class="action-desc">Criação de rotina de coleta de avaliações para ultrapassar a barreira dos 500 reviews e consolidar autoridade frente ao Mira Maré e Garra Azul.</div>
      </div>
      <div class="action-card">
        <div class="action-num">02</div>
        <div class="action-title">Cardápio & WhatsApp</div>
        <div class="action-desc">Otimização dos links diretos de atendimento para canalizar o fluxo turístico sem intermediários.</div>
      </div>
      <div class="action-card">
        <div class="action-num">03</div>
        <div class="action-title">Postagens & Destaque Visual</div>
        <div class="action-desc">Atualização contínua de fotos dos pratos e pratos do dia para manter o perfil aquecido nas buscas do Google Maps.</div>
      </div>
    </div>

    <!-- Callout Final de Proposta -->
    <div class="callout">
      <div class="callout-title">💡 Próximo Passo Estratégico</div>
      <div class="callout-text">Com o ajuste na tração de avaliações e padronização das respostas locais, o <strong>{nome}</strong> possui todos os atributos de qualidade para se consolidar como a principal escolha gastronômica da orla de Ponta das Canas.</div>
    </div>

    <div class="page-foot">
      <div>AH3 • Inteligência & Otimização de Presença Local</div>
      <div>Confidencial · Elaborado para {nome}</div>
    </div>
  </div>

</body>
</html>
"""

    saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
    os.makedirs(saida_dir, exist_ok=True)
    caminho_html = os.path.join(saida_dir, "Auditoria_Exemplo_Canto_do_Mar_Mix10.html")
    caminho_pdf = os.path.join(saida_dir, "Auditoria_Exemplo_Canto_do_Mar_Mix10.pdf")

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] HTML gerado: {caminho_html}")

    # Converter para PDF via Edge Headless
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
    if res.returncode == 0 and os.path.exists(caminho_pdf):
        print(f"[✓] PDF gerado com sucesso: {caminho_pdf}")
        return caminho_pdf
    else:
        raise RuntimeError(f"Erro na conversão PDF: {res.stderr}")

if __name__ == "__main__":
    gerar_pdf_exemplo_canto_do_mar()

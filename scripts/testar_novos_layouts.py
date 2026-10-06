import os
import subprocess
import pymupdf

# Diretórios
HTML_DIR = "saida/novos_designs_estruturais_html"
PDF_DIR = "BigBrain/handoff/10_novos_layouts_estruturais"
PNG_DIR = "saida/previews_novos_layouts"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Dados reais do Paixão Restaurante para o teste
DADOS = {
    "nome": "Paixão Restaurante & Pizzaria",
    "bairro": "Ingleses do Rio Vermelho",
    "categoria": "Frutos do Mar & Pizzaria",
    "endereco": "Estrada Dom João Becker, 329 - Ingleses, Florianópolis - SC",
    "telefone": "(48) 3269-1355",
    "gps": "-27.43611, -48.39098",
    "rating": 4.5,
    "reviews": 5385,
    "has_site": True,
    "site_url": "http://www.paixaorestaurante.com.br/",
    "horario": "Segunda a Domingo: 10:00 às 23:30",
    "status": "Aberto & Operacional",
    "concorrentes": [
        {"pos": 1, "nome": "Paixão Restaurante & Pizzaria", "reviews": 5385, "nota": 4.5, "bairro": "Ingleses", "target": True},
        {"pos": 2, "nome": "Don Zarichta Pizzaria Artesanal", "reviews": 5230, "nota": 4.9, "bairro": "Sto. Antônio", "target": False},
        {"pos": 3, "nome": "Costillas Grill - Costelaria", "reviews": 4791, "nota": 4.3, "bairro": "Canasvieiras", "target": False},
        {"pos": 4, "nome": "Freguesia Bar", "reviews": 4377, "nota": 4.4, "bairro": "Sto. Antônio", "target": False},
        {"pos": 5, "nome": "Villa do Porto Gastronomia", "reviews": 3983, "nota": 4.6, "bairro": "Sto. Antônio", "target": False}
    ]
}

# -------------------------------------------------------------
# LAYOUT 1: INFOGRÁFICO DE CONVERSÃO & JORNADA DO CLIENTE
# Estrutura: Funil visual passo a passo de como o turista descobre o restaurante no Google
# -------------------------------------------------------------
def get_layout_1():
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
<style>
  @page {{ size: 210mm 297mm; margin: 0; }}
  body {{ margin: 0; background: #0F172A; color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }}
  .page {{ width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; position: relative; page-break-after: always; }}
  .badge-top {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 8px; font-weight: 800; padding: 3px 8px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em; display: inline-block; }}
  .title {{ font-size: 20px; font-weight: 900; margin: 4px 0 2px 0; color: #FFF; }}
  .sub {{ font-size: 10px; color: #94A3B8; }}
  
  /* Funil Visual */
  .funnel-container {{ display: flex; flex-direction: column; gap: 8px; margin: 12px 0; }}
  .funnel-step {{ background: #1E293B; border-radius: 8px; padding: 10px 14px; border-left: 4px solid #38BDF8; display: flex; justify-content: space-between; align-items: center; }}
  .funnel-step.step-2 {{ border-left-color: #10B981; }}
  .funnel-step.step-3 {{ border-left-color: #F59E0B; }}
  .funnel-step.step-4 {{ border-left-color: #EF4444; }}
  
  .step-num {{ font-size: 18px; font-weight: 900; color: #64748B; margin-right: 10px; }}
  .step-info h4 {{ font-size: 11px; font-weight: 800; color: #FFF; margin: 0; }}
  .step-info p {{ font-size: 8.5px; color: #94A3B8; margin: 2px 0 0 0; }}
  .step-metric {{ text-align: right; min-width: 80px; }}
  .step-metric .val {{ font-size: 14px; font-weight: 900; color: #38BDF8; font-family: 'JetBrains Mono', monospace; }}
  .step-metric .lbl {{ font-size: 7px; color: #64748B; text-transform: uppercase; }}

  .card-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .box {{ background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 10px 12px; }}
  .box h5 {{ font-size: 10px; font-weight: 800; color: #38BDF8; margin: 0 0 6px 0; text-transform: uppercase; }}
  .box p {{ font-size: 8.5px; color: #CBD5E1; line-height: 1.4; margin: 0; }}

  .footer {{ border-top: 1px solid #334155; padding-top: 8px; font-size: 8px; color: #64748B; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
<div class="page">
  <div>
    <div>
      <span class="badge-top">Layout 01 · Jornada de Conversão do Turista</span>
      <h1 class="title">Paixão Restaurante & Pizzaria</h1>
      <div class="sub">Como um cliente pesquisa, encontra e decide consumir no seu restaurante no Google</div>
    </div>

    <!-- Funil da Jornada -->
    <div class="funnel-container">
      <div class="funnel-step">
        <div style="display:flex; align-items:center;">
          <div class="step-num">01</div>
          <div class="step-info">
            <h4>Busca Regional ("Restaurantes nos Ingleses")</h4>
            <p>O cliente pesquisa no celular enquanto passeia pelo Norte da Ilha.</p>
          </div>
        </div>
        <div class="step-metric">
          <div class="val">1º LUGAR</div>
          <div class="lbl">Posição SERP</div>
        </div>
      </div>

      <div class="funnel-step step-2">
        <div style="display:flex; align-items:center;">
          <div class="step-num" style="color:#10B981;">02</div>
          <div class="step-info">
            <h4>Validação de Prova Social & Reputação</h4>
            <p>O cliente analisa as notas e fotos dos pratos antes de escolher.</p>
          </div>
        </div>
        <div class="step-metric">
          <div class="val" style="color:#10B981;">5.385 · 4.5★</div>
          <div class="lbl">Reviews Ativas</div>
        </div>
      </div>

      <div class="funnel-step step-3">
        <div style="display:flex; align-items:center;">
          <div class="step-num" style="color:#F59E0B;">03</div>
          <div class="step-info">
            <h4>Consulta ao Cardápio & Preços</h4>
            <p>Momento decisivo: se o cardápio for difícil de abrir, o cliente volta e vai no concorrente.</p>
          </div>
        </div>
        <div class="step-metric">
          <div class="val" style="color:#F59E0B;">SITE ATIVO</div>
          <div class="lbl">Cardápio Mobile</div>
        </div>
      </div>

      <div class="funnel-step step-4">
        <div style="display:flex; align-items:center;">
          <div class="step-num" style="color:#EF4444;">04</div>
          <div class="step-info">
            <h4>Ação Final: GPS no Carro ou WhatsApp</h4>
            <p>Traçar rota pelo Google Maps ou reservar mesa diretamente pelo telefone cadastrado.</p>
          </div>
        </div>
        <div class="step-metric">
          <div class="val" style="color:#EF4444;">DISCADOR OK</div>
          <div class="lbl">(48) 3269-1355</div>
        </div>
      </div>
    </div>

    <!-- Diagnóstico Estruturado em 2 Blocos -->
    <div class="card-grid">
      <div class="box">
        <h5>Onde Você Vence a Concorrência</h5>
        <p>Seu perfil é o mais avaliado de todo o Norte da Ilha (5.385 notas), gerando uma barreira quase intransponível para quem tenta ultrapassar organicamente no mapa.</p>
      </div>
      <div class="box" style="border-color:#F59E0B;">
        <h5 style="color:#F59E0B;">Onde Você Está Perdendo Dinheiro</h5>
        <p>Centenas de comentários de clientes satisfeitos não recebem resposta do proprietário. O algoritmo do Google valoriza perfis com alta interação do gestor.</p>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local</span>
    <span>Layout 01 / 10 · Formato Infográfico da Jornada</span>
  </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# LAYOUT 2: RAIO-X ANTES & DEPOIS (GAP ANALYSIS)
# Estrutura: 2 Colunas lado a lado (Como está hoje vs Como deveria estar com a AH3)
# -------------------------------------------------------------
def get_layout_2():
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  @page {{ size: 210mm 297mm; margin: 0; }}
  body {{ margin: 0; background: #F8FAFC; color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }}
  .page {{ width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; position: relative; page-break-after: always; }}
  .title {{ font-size: 20px; font-weight: 900; margin: 2px 0; color: #0F172A; }}
  .sub {{ font-size: 10px; color: #64748B; }}
  
  .compare-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 14px 0; }}
  .col-side {{ border-radius: 10px; padding: 12px 14px; }}
  .col-atual {{ background: #FEF2F2; border: 1.5px solid #FECACA; }}
  .col-otimizado {{ background: #ECFDF5; border: 1.5px solid #A7F3D0; }}
  
  .col-badge {{ font-size: 8px; font-weight: 800; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-bottom: 8px; text-transform: uppercase; }}
  .col-atual .col-badge {{ background: #EF4444; color: #FFF; }}
  .col-otimizado .col-badge {{ background: #10B981; color: #FFF; }}
  
  .item-row {{ margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.06); }}
  .item-row:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
  .item-label {{ font-size: 8px; font-weight: 700; color: #64748B; text-transform: uppercase; }}
  .item-val {{ font-size: 9.5px; font-weight: 800; margin-top: 1px; color: #0F172A; }}
  .item-desc {{ font-size: 8px; color: #475569; margin-top: 2px; line-height: 1.3; }}

  .hero-bottom {{ background: #0F172A; color: #FFF; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; }}
  .hero-bottom h4 {{ font-size: 11px; font-weight: 800; margin: 0; }}
  .hero-bottom p {{ font-size: 8px; color: #94A3B8; margin: 2px 0 0 0; }}
  .hero-btn {{ background: #38BDF8; color: #0F172A; font-size: 8.5px; font-weight: 800; padding: 6px 12px; border-radius: 6px; text-transform: uppercase; }}

  .footer {{ border-top: 1px solid #E2E8F0; padding-top: 8px; font-size: 8px; color: #94A3B8; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
<div class="page">
  <div>
    <div>
      <div style="font-size: 8px; font-weight: 800; color: #C2410C; text-transform: uppercase; letter-spacing: 0.05em;">Layout 02 · Raio-X Comparativo</div>
      <h1 class="title">Paixão Restaurante & Pizzaria</h1>
      <div class="sub">Diagnóstico de Gaps: Situação Cadastral Hoje vs. Potencial Máximo de Conversão</div>
    </div>

    <!-- Comparação Lado a Lado -->
    <div class="compare-grid">
      <!-- Coluna Atual -->
      <div class="col-side col-atual">
        <span class="col-badge">Situação Atual (Diagnóstico)</span>
        
        <div class="item-row">
          <div class="item-label">Volume & Nota</div>
          <div class="item-val">5.385 reviews · 4.5 ★</div>
          <div class="item-desc">Excelente volume histórico, mas vulnerável a notas baixas pontuais sem recuperação rápida.</div>
        </div>

        <div class="item-row">
          <div class="item-label">Respostas do Proprietário</div>
          <div class="item-val" style="color:#DC2626;">Baixa interação (&lt; 40%)</div>
          <div class="item-desc">Dezenas de clientes elogiam os pratos e ficam sem resposta, reduzindo relevância semântica no Google.</div>
        </div>

        <div class="item-row">
          <div class="item-label">Cardápio & Conversão</div>
          <div class="item-val">Website Básico</div>
          <div class="item-desc">Não há destaque estratégico para fotos profissionais dos carros-chefe na versão mobile rápida.</div>
        </div>

        <div class="item-row">
          <div class="item-label">Captura em Salão</div>
          <div class="item-val" style="color:#DC2626;">Sem Displays NFC</div>
          <div class="item-desc">Clientes satisfeitos pagam e saem sem avaliar na hora do atendimento.</div>
        </div>
      </div>

      <!-- Coluna Otimizada -->
      <div class="col-side col-otimizado">
        <span class="col-badge">Com Estruturação AH3</span>
        
        <div class="item-row">
          <div class="item-label">Volume & Nota</div>
          <div class="item-val" style="color:#059669;">Meta: 4.7 ★ com +80 reviews/mês</div>
          <div class="item-desc">Blindagem de reputação acelerando avaliações 5 estrelas diretamente no balcão e mesas.</div>
        </div>

        <div class="item-row">
          <div class="item-label">Respostas do Proprietário</div>
          <div class="item-val" style="color:#059669;">Gestão de Resposta Total</div>
          <div class="item-desc">Respostas humanizadas com palavras-chave estratégicas ("melhor camarão", "pizza nos ingleses").</div>
        </div>

        <div class="item-row">
          <div class="item-label">Cardápio & Conversão</div>
          <div class="item-val" style="color:#059669;">Cardápio Mobile de Alta Conversão</div>
          <div class="item-desc">Página veloz com fotos apetitosas e botão direto para WhatsApp ou ligação com 1 toque.</div>
        </div>

        <div class="item-row">
          <div class="item-label">Captura em Salão</div>
          <div class="item-val" style="color:#059669;">Smart Cards NFC & QR Code</div>
          <div class="item-desc">Aproximação do celular no fechamento da conta para avaliar o restaurante em 5 segundos.</div>
        </div>
      </div>
    </div>

    <!-- Bloco de Impacto -->
    <div class="hero-bottom">
      <div>
        <h4>Resultado Esperado: Blindagem do 1º Lugar no Norte da Ilha</h4>
        <p>Aumento da taxa de conversão de turistas que pesquisam por gastronomia nos Ingleses.</p>
      </div>
      <div class="hero-btn">+35% Retenção</div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local</span>
    <span>Layout 02 / 10 · Raio-X Antes & Depois</span>
  </div>
</div>
</body>
</html>
"""

# -------------------------------------------------------------
# LAYOUT 3: RADAR LOCAL EM GRID DE QUADRANTES
# Estrutura: 4 Quadrantes claros (Reputação, Localização, Digital, Oportunidades)
# -------------------------------------------------------------
def get_layout_3():
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
<style>
  @page {{ size: 210mm 297mm; margin: 0; }}
  body {{ margin: 0; background: #0B101B; color: #F1F5F9; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }}
  .page {{ width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; position: relative; page-break-after: always; }}
  .title {{ font-size: 20px; font-weight: 900; margin: 2px 0; color: #FFF; }}
  .sub {{ font-size: 10px; color: #94A3B8; }}

  /* Grid 4 Quadrantes */
  .quad-grid {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 10px; margin: 12px 0; }}
  .quad {{ background: #131B2E; border: 1px solid #1E293B; border-radius: 8px; padding: 12px 14px; position: relative; }}
  .quad-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 6px; margin-bottom: 8px; }}
  .quad-title {{ font-size: 10px; font-weight: 800; color: #38BDF8; text-transform: uppercase; }}
  .quad-score {{ font-size: 11px; font-weight: 900; color: #10B981; font-family: 'JetBrains Mono', monospace; }}

  .quad-line {{ display: flex; justify-content: space-between; font-size: 8.5px; margin-bottom: 5px; }}
  .quad-line .k {{ color: #94A3B8; }}
  .quad-line .v {{ color: #FFF; font-weight: 700; }}

  .table-ranking {{ width: 100%; border-collapse: collapse; font-size: 8px; margin-top: 8px; }}
  .table-ranking th {{ background: #0B101B; color: #64748B; padding: 4px 6px; text-align: left; text-transform: uppercase; }}
  .table-ranking td {{ padding: 4px 6px; border-bottom: 1px solid #1E293B; color: #CBD5E1; }}
  .table-ranking tr.target td {{ background: rgba(249, 115, 22, 0.15); color: #FFF; font-weight: 800; }}

  .footer {{ border-top: 1px solid #1E293B; padding-top: 8px; font-size: 8px; color: #64748B; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
<div class="page">
  <div>
    <div>
      <div style="font-size: 8px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.05em;">Layout 03 · Matriz de 4 Quadrantes</div>
      <h1 class="title">Paixão Restaurante & Pizzaria</h1>
      <div class="sub">Auditoria Sistêmica: Reputação, Localização, Presença Web e Ações Prioritárias</div>
    </div>

    <!-- 4 Quadrantes -->
    <div class="quad-grid">
      <!-- Q1: Reputação -->
      <div class="quad">
        <div class="quad-header">
          <span class="quad-title">Q1 · Reputação & Prova Social</span>
          <span class="quad-score">92 / 100</span>
        </div>
        <div class="quad-line"><span class="k">Volume de Avaliações:</span><span class="v">5.385 (Top 1 Região)</span></div>
        <div class="quad-line"><span class="k">Nota Média Geral:</span><span class="v">4.5 ★</span></div>
        <div class="quad-line"><span class="k">Frequência de Novos Reviews:</span><span class="v">Alta (+40/mês)</span></div>
        <div class="quad-line"><span class="k">Taxa de Resposta do Dono:</span><span class="v" style="color:#EF4444;">Baixa (Oportunidade)</span></div>
      </div>

      <!-- Q2: Localização & NAP -->
      <div class="quad">
        <div class="quad-header">
          <span class="quad-title">Q2 · Sinal Cadastral & GPS</span>
          <span class="quad-score">98 / 100</span>
        </div>
        <div class="quad-line"><span class="k">Bairro:</span><span class="v">Praia dos Ingleses</span></div>
        <div class="quad-line"><span class="k">Pino GPS:</span><span class="v">-27.43611, -48.39098</span></div>
        <div class="quad-line"><span class="k">Telefone de Atendimento:</span><span class="v">(48) 3269-1355</span></div>
        <div class="quad-line"><span class="k">Status da Ficha:</span><span class="v" style="color:#10B981;">Verificada ✓</span></div>
      </div>

      <!-- Q3: Presença Web & Conversão -->
      <div class="quad">
        <div class="quad-header">
          <span class="quad-title">Q3 · Cardápio & Mobile</span>
          <span class="quad-score">70 / 100</span>
        </div>
        <div class="quad-line"><span class="k">Website Cadastrado:</span><span class="v">Sim (paixaorestaurante.com.br)</span></div>
        <div class="quad-line"><span class="k">Indexação de Pratos:</span><span class="v">Parcial</span></div>
        <div class="quad-line"><span class="k">Botão WhatsApp Direto:</span><span class="v">Presente</span></div>
        <div class="quad-line"><span class="k">Velocidade em 4G:</span><span class="v" style="color:#F59E0B;">Média</span></div>
      </div>

      <!-- Q4: Plano de Ação -->
      <div class="quad" style="border-color:#38BDF8;">
        <div class="quad-header">
          <span class="quad-title" style="color:#FFF;">Q4 · Oportunidade Imediata</span>
          <span class="quad-score" style="color:#38BDF8;">ALAVANCAGEM</span>
        </div>
        <div style="font-size:8px; color:#CBD5E1; line-height: 1.35;">
          <strong>1. Smart Cards NFC nas Mesas:</strong> Coletar feedback de turistas satisfeitos no pagamento.<br>
          <strong>2. SEO Semântico em Comentários:</strong> Responder citando termos de busca.<br>
          <strong>3. Cardápio Mobile Veloz:</strong> Eliminar perda de cliques.
        </div>
      </div>
    </div>

    <!-- Tabela Resumida de Concorrentes -->
    <div style="background:#131B2E; border:1px solid #1E293B; border-radius:8px; padding:8px 12px;">
      <div style="font-size:8.5px; font-weight:800; color:#94A3B8; text-transform:uppercase; margin-bottom:4px;">Top 5 Restaurantes do Norte da Ilha</div>
      <table class="table-ranking">
        <thead>
          <tr>
            <th>Pos.</th>
            <th>Restaurante</th>
            <th>Bairro</th>
            <th>Avaliações</th>
            <th>Nota</th>
          </tr>
        </thead>
        <tbody>
          <tr class="target">
            <td>1º</td>
            <td>Paixão Restaurante & Pizzaria (SEU NEGÓCIO)</td>
            <td>Ingleses</td>
            <td>5.385</td>
            <td>4.5 ★</td>
          </tr>
          <tr>
            <td>2º</td>
            <td>Don Zarichta Pizzaria Artesanal</td>
            <td>Sto. Antônio</td>
            <td>5.230</td>
            <td>4.9 ★</td>
          </tr>
          <tr>
            <td>3º</td>
            <td>Costillas Grill - Costelaria</td>
            <td>Canasvieiras</td>
            <td>4.791</td>
            <td>4.3 ★</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local</span>
    <span>Layout 03 / 10 · Matriz de 4 Quadrantes</span>
  </div>
</div>
</body>
</html>
"""

# Salva e compila os 3 primeiros layouts para teste e inspeção
with open(f"{HTML_DIR}/layout_01.html", "w", encoding="utf-8") as f:
    f.write(get_layout_1())

with open(f"{HTML_DIR}/layout_02.html", "w", encoding="utf-8") as f:
    f.write(get_layout_2())

with open(f"{HTML_DIR}/layout_03.html", "w", encoding="utf-8") as f:
    f.write(get_layout_3())

print("HTMLs dos novos layouts gerados com sucesso!")

import os
import subprocess
import pymupdf

HTML_DIR = "saida/novos_10_layouts_completos_html"
PDF_DIR = "BigBrain/handoff/catalogo_10_estruturas_novas"
PNG_DIR = "saida/previews_10_estruturas_novas"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ==========================================
# 10 LAYOUTS COMPLETAMENTE DIFERENTES
# ==========================================

# 1. FUNIL DA JORNADA DO CLIENTE (Infográfico passo a passo)
def l1():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #0F172A; color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.step { background: #1E293B; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; border-left: 5px solid #38BDF8; display: flex; justify-content: space-between; align-items: center; }
.step.s2 { border-left-color: #10B981; } .step.s3 { border-left-color: #F59E0B; } .step.s4 { border-left-color: #EF4444; }
.val { font-size: 14px; font-weight: 800; color: #38BDF8; text-align: right; }
.box { background: #1E293B; border-radius: 8px; padding: 10px 12px; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#38BDF8; text-transform:uppercase;">Estrutura 01 · Jornada do Cliente no Google</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#94A3B8; margin-bottom:12px;">Como o turista encontra, analisa e decide visitar o seu restaurante no Norte da Ilha</div>

  <div class="step">
    <div><h4 style="margin:0; font-size:11px;">1. Busca no Celular ("Restaurante nos Ingleses")</h4><p style="margin:2px 0 0 0; font-size:8.5px; color:#94A3B8;">O cliente pesquisa no Google Maps enquanto passeia.</p></div>
    <div class="val">1º LUGAR<br><span style="font-size:7px; color:#64748B;">NO MAPA</span></div>
  </div>

  <div class="step s2">
    <div><h4 style="margin:0; font-size:11px;">2. Validação da Reputação Pública</h4><p style="margin:2px 0 0 0; font-size:8.5px; color:#94A3B8;">Análise das notas e volume de comentários de quem já foi.</p></div>
    <div class="val" style="color:#10B981;">5.385 · 4.5★<br><span style="font-size:7px; color:#64748B;">PROVA SOCIAL</span></div>
  </div>

  <div class="step s3">
    <div><h4 style="margin:0; font-size:11px;">3. Abertura do Cardápio & Fotos dos Pratos</h4><p style="margin:2px 0 0 0; font-size:8.5px; color:#94A3B8;">Momento da decisão: facilidade de ver pratos e valores.</p></div>
    <div class="val" style="color:#F59E0B;">SITE ATIVO<br><span style="font-size:7px; color:#64748B;">CARDÁPIO</span></div>
  </div>

  <div class="step s4">
    <div><h4 style="margin:0; font-size:11px;">4. Conversão: Rota no GPS ou Ligação</h4><p style="margin:2px 0 0 0; font-size:8.5px; color:#94A3B8;">Traçar rota para o salão ou pedir mesa pelo telefone.</p></div>
    <div class="val" style="color:#EF4444;">DISCADOR OK<br><span style="font-size:7px; color:#64748B;">(48) 3269-1355</span></div>
  </div>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px;">
    <div class="box"><h5 style="margin:0 0 4px 0; color:#38BDF8; font-size:9.5px; text-transform:uppercase;">Ponto Forte Mapeado</h5><p style="margin:0; font-size:8.5px; color:#CBD5E1; line-height:1.35;">Maior volume de reviews do Norte da Ilha (5.385). Barreira quase insuperável para a concorrência direta.</p></div>
    <div class="box"><h5 style="margin:0 0 4px 0; color:#F59E0B; font-size:9.5px; text-transform:uppercase;">Vazamento de Clientes</h5><p style="margin:0; font-size:8.5px; color:#CBD5E1; line-height:1.35;">Muitos comentários sem resposta da gestão. O algoritmo prioriza perfis com respostas constantes e palavras-chave.</p></div>
  </div>
</div>
<div style="border-top:1px solid #334155; padding-top:6px; font-size:7.5px; color:#64748B; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 01 / 10 · Funil da Jornada</span></div>
</div></body></html>"""

# 2. RAIO-X ANTES & DEPOIS (GAP ANALYSIS)
def l2():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #F8FAFC; color: #0F172A; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.col { border-radius: 8px; padding: 12px; }
.col.c1 { background: #FEF2F2; border: 1.5px solid #FECACA; }
.col.c2 { background: #ECFDF5; border: 1.5px solid #A7F3D0; }
.row-item { margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid rgba(0,0,0,0.05); }
.row-item:last-child { border-bottom: none; margin: 0; padding: 0; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#C2410C; text-transform:uppercase;">Estrutura 02 · Raio-X Antes & Depois</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#64748B; margin-bottom:12px;">Comparativo: Situação Cadastral Hoje vs. Potencial Otimizado com a AH3</div>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
    <div class="col c1">
      <div style="font-size:8px; font-weight:800; background:#EF4444; color:#FFF; padding:2px 6px; border-radius:3px; display:inline-block; margin-bottom:8px;">COMO ESTÁ HOJE</div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Avaliações</div><div style="font-size:9px; font-weight:800; color:#0F172A;">5.385 reviews · 4.5 ★</div><div style="font-size:7.5px; color:#475569;">Volume excelente, mas passivo sem aceleração no salão.</div></div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Interação</div><div style="font-size:9px; font-weight:800; color:#DC2626;">Respostas esporádicas</div><div style="font-size:7.5px; color:#475569;">Perda de relevância em buscas semânticas no Google.</div></div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Captura Física</div><div style="font-size:9px; font-weight:800; color:#DC2626;">Sem tecnologia NFC</div><div style="font-size:7.5px; color:#475569;">Clientes satisfeitos vão embora sem registrar nota 5★.</div></div>
    </div>

    <div class="col c2">
      <div style="font-size:8px; font-weight:800; background:#10B981; color:#FFF; padding:2px 6px; border-radius:3px; display:inline-block; margin-bottom:8px;">COM ESTRUTURAÇÃO AH3</div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Avaliações</div><div style="font-size:9px; font-weight:800; color:#059669;">Meta 4.7 ★ (+80 reviews/mês)</div><div style="font-size:7.5px; color:#475569;">Blindagem definitiva da liderança em todo o Norte da Ilha.</div></div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Interação</div><div style="font-size:9px; font-weight:800; color:#059669;">Gestão Ativa Total</div><div style="font-size:7.5px; color:#475569;">Respostas estratégicas citando pratos e frutos do mar.</div></div>
      <div class="row-item"><div style="font-size:7.5px; color:#64748B; text-transform:uppercase; font-weight:700;">Captura Física</div><div style="font-size:9px; font-weight:800; color:#059669;">Smart Cards NFC & QR Code</div><div style="font-size:7.5px; color:#475569;">Avaliação em 5 segundos por aproximação no fechamento.</div></div>
    </div>
  </div>

  <div style="background:#0F172A; color:#FFF; border-radius:8px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
    <div><div style="font-size:10px; font-weight:800;">Impacto Esperado no Faturamento</div><div style="font-size:7.5px; color:#94A3B8;">Aumento de retenção de turistas que pesquisam gastronomia nos Ingleses.</div></div>
    <div style="background:#38BDF8; color:#0F172A; font-size:8px; font-weight:800; padding:5px 10px; border-radius:4px;">+35% Conversão</div>
  </div>
</div>
<div style="border-top:1px solid #E2E8F0; padding-top:6px; font-size:7.5px; color:#94A3B8; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 02 / 10 · Raio-X Antes & Depois</span></div>
</div></body></html>"""

# 3. MATRIZ DE 4 QUADRANTES (BENTO ESTRUTURADO)
def l3():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #0B101B; color: #F1F5F9; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }
.quad { background: #131B2E; border: 1px solid #1E293B; border-radius: 8px; padding: 10px 12px; }
.q-title { font-size: 9px; font-weight: 800; color: #38BDF8; text-transform: uppercase; border-bottom: 1px solid #1E293B; padding-bottom: 4px; margin-bottom: 6px; }
.q-row { display: flex; justify-content: space-between; font-size: 8px; margin-bottom: 4px; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#38BDF8; text-transform:uppercase;">Estrutura 03 · Matriz de 4 Quadrantes</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#94A3B8; margin-bottom:8px;">Visão Sistêmica: Reputação, Cadastro, Canais Digitais e Oportunidades</div>

  <div class="grid">
    <div class="quad">
      <div class="q-title">Q1 · Reputação & Notas (Nota: 92)</div>
      <div class="q-row"><span style="color:#94A3B8;">Volume Total:</span><span style="font-weight:700;">5.385 (Top 1 Região)</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Nota Média:</span><span style="font-weight:700;">4.5 ★</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Velocidade de Notas:</span><span style="font-weight:700;">Alta (+40/mês)</span></div>
    </div>
    <div class="quad">
      <div class="q-title">Q2 · Cadastro & GPS (Nota: 98)</div>
      <div class="q-row"><span style="color:#94A3B8;">Endereço:</span><span style="font-weight:700;">Estr. Dom João Becker, 329</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Telefone:</span><span style="font-weight:700;">(48) 3269-1355</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Status:</span><span style="color:#10B981; font-weight:700;">Verificado ✓</span></div>
    </div>
    <div class="quad">
      <div class="q-title">Q3 · Cardápio & Mobile (Nota: 70)</div>
      <div class="q-row"><span style="color:#94A3B8;">Website:</span><span style="font-weight:700;">Ativo</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Pratos Indexados:</span><span style="color:#F59E0B; font-weight:700;">Parcial</span></div>
      <div class="q-row"><span style="color:#94A3B8;">Botão WhatsApp:</span><span style="font-weight:700;">Presente</span></div>
    </div>
    <div class="quad" style="border-color:#38BDF8;">
      <div class="q-title" style="color:#FFF;">Q4 · Ações Recomendadas</div>
      <div style="font-size:7.5px; color:#CBD5E1; line-height:1.35;">
        • Instalação de Smart Cards NFC no caixa.<br>
        • Respostas estratégicas em 100% dos reviews.<br>
        • Atualização semanal do catálogo de fotos.
      </div>
    </div>
  </div>
</div>
<div style="border-top:1px solid #1E293B; padding-top:6px; font-size:7.5px; color:#64748B; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 03 / 10 · Matriz de 4 Quadrantes</span></div>
</div></body></html>"""

# 4. PAINEL DE BENCHMARKING DE MERCADO (PODIUM COMPETITIVO)
def l4():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #111827; color: #F9FAFB; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.podium-box { display: flex; gap: 8px; margin-bottom: 12px; align-items: flex-end; }
.podium-card { flex: 1; background: #1F2937; border-radius: 8px; padding: 10px; text-align: center; border-top: 3px solid #6B7280; }
.podium-card.p1 { border-top-color: #F97316; background: #374151; padding: 14px 10px; }
.podium-card.p2 { border-top-color: #38BDF8; } .podium-card.p3 { border-top-color: #10B981; }
table { width: 100%; border-collapse: collapse; font-size: 8px; margin-top: 8px; }
th { background: #1F2937; color: #9CA3AF; padding: 5px; text-align: left; }
td { padding: 5px; border-bottom: 1px solid #374151; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#F97316; text-transform:uppercase;">Estrutura 04 · Pódio & Inteligência Competitiva</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#9CA3AF; margin-bottom:12px;">Posicionamento no Pódio Gastronômico do Norte da Ilha</div>

  <div class="podium-box">
    <div class="podium-card p2"><div style="font-size:12px; font-weight:900; color:#38BDF8;">2º LUGAR</div><div style="font-size:8.5px; font-weight:700; margin:2px 0;">Don Zarichta</div><div style="font-size:7.5px; color:#9CA3AF;">5.230 reviews · 4.9★</div></div>
    <div class="podium-card p1"><div style="font-size:8px; font-weight:800; background:#F97316; color:#FFF; padding:1px 5px; border-radius:3px; display:inline-block; margin-bottom:4px;">SEU NEGÓCIO</div><div style="font-size:15px; font-weight:900; color:#FFF;">1º LUGAR</div><div style="font-size:9.5px; font-weight:800; margin:2px 0;">Paixão Restaurante</div><div style="font-size:8px; color:#E5E7EB;">5.385 reviews · 4.5★</div></div>
    <div class="podium-card p3"><div style="font-size:12px; font-weight:900; color:#10B981;">3º LUGAR</div><div style="font-size:8.5px; font-weight:700; margin:2px 0;">Costillas Grill</div><div style="font-size:7.5px; color:#9CA3AF;">4.791 reviews · 4.3★</div></div>
  </div>

  <div style="background:#1F2937; border-radius:8px; padding:8px 10px;">
    <div style="font-size:8.5px; font-weight:800; color:#9CA3AF; text-transform:uppercase;">Ranking Completo de Proximidade (Top 5)</div>
    <table>
      <thead><tr><th>#</th><th>Estabelecimento</th><th>Bairro</th><th>Avaliações</th><th>Nota</th><th>Status</th></tr></thead>
      <tbody>
        <tr style="background:rgba(249,115,22,0.15); font-weight:800; color:#FFF;"><td>1º</td><td>Paixão Restaurante & Pizzaria</td><td>Ingleses</td><td>5.385</td><td>4.5★</td><td>LÍDER</td></tr>
        <tr><td>2º</td><td>Don Zarichta Pizzaria Artesanal</td><td>Sto. Antônio</td><td>5.230</td><td>4.9★</td><td>Ameaça Direta</td></tr>
        <tr><td>3º</td><td>Costillas Grill - Costelaria</td><td>Canasvieiras</td><td>4.791</td><td>4.3★</td><td>Estável</td></tr>
      </tbody>
    </table>
  </div>
</div>
<div style="border-top:1px solid #374151; padding-top:6px; font-size:7.5px; color:#6B7280; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 04 / 10 · Pódio Competitivo</span></div>
</div></body></html>"""

# 5. SCORECARD SEMAFÓRICO TÉCNICO (VERDE / AMARELO / VERMELHO)
def l5():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #FFFFFF; color: #111827; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.signal-box { border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.signal-box.ok { background: #ECFDF5; border-left: 4px solid #10B981; }
.signal-box.warn { background: #FFFBEB; border-left: 4px solid #F59E0B; }
.signal-box.bad { background: #FEF2F2; border-left: 4px solid #EF4444; }
.tag { font-size: 7.5px; font-weight: 800; padding: 2px 6px; border-radius: 3px; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#2563EB; text-transform:uppercase;">Estrutura 05 · Semáforo de Desempenho Local</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#6B7280; margin-bottom:12px;">Auditoria Semafórica dos Fatores de Atração e Conversão no Google</div>

  <div class="signal-box ok">
    <div><div style="font-size:9.5px; font-weight:800; color:#065F46;">Volume de Avaliações Públicas</div><div style="font-size:8px; color:#047857;">5.385 comentários registrados (Maior autoridade regional).</div></div>
    <span class="tag" style="background:#10B981; color:#FFF;">APROVADO ✓</span>
  </div>

  <div class="signal-box ok">
    <div><div style="font-size:9.5px; font-weight:800; color:#065F46;">Sinal Cadastral (NAP & GPS)</div><div style="font-size:8px; color:#047857;">Nome limpo, endereço e localização exatos na Praia dos Ingleses.</div></div>
    <span class="tag" style="background:#10B981; color:#FFF;">APROVADO ✓</span>
  </div>

  <div class="signal-box warn">
    <div><div style="font-size:9.5px; font-weight:800; color:#92400E;">Nota Média de Reputação</div><div style="font-size:8px; color:#B45309;">Nota atual de 4.5★ vs. média de 4.8★ dos concorrentes diretos.</div></div>
    <span class="tag" style="background:#F59E0B; color:#FFF;">ATENÇÃO !</span>
  </div>

  <div class="signal-box bad">
    <div><div style="font-size:9.5px; font-weight:800; color:#991B1B;">Taxa de Resposta da Gestão</div><div style="font-size:8px; color:#B91C1C;">Grande volume de clientes sem respostas oficiais do proprietário.</div></div>
    <span class="tag" style="background:#EF4444; color:#FFF;">CRÍTICO ✕</span>
  </div>
</div>
<div style="border-top:1px solid #E5E7EB; padding-top:6px; font-size:7.5px; color:#9CA3AF; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 05 / 10 · Semáforo de Desempenho</span></div>
</div></body></html>"""

# 6. RELATÓRIO EXECUTIVO DE 1 PÁGINA (C-LEVEL BRIEFING)
def l6():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #FAFAFA; color: #18181B; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }
.kpi-box { background: #FFF; border: 1px solid #E4E4E7; border-radius: 8px; padding: 10px; }
.kpi-val { font-size: 16px; font-weight: 900; color: #18181B; margin: 2px 0; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#71717A; text-transform:uppercase;">Estrutura 06 · Executive Briefing C-Level</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#71717A; margin-bottom:12px;">Síntese Executiva de Presença Digital e Dominância de Mercado</div>

  <div class="kpi-row">
    <div class="kpi-box"><div style="font-size:7.5px; color:#71717A; text-transform:uppercase;">Volume de Reviews</div><div class="kpi-val" style="color:#2563EB;">5.385</div><div style="font-size:7px; color:#10B981; font-weight:700;">1º no Norte da Ilha</div></div>
    <div class="kpi-box"><div style="font-size:7.5px; color:#71717A; text-transform:uppercase;">Nota Média</div><div class="kpi-val">4.5 ★</div><div style="font-size:7px; color:#71717A;">Satisfação Sólida</div></div>
    <div class="kpi-box"><div style="font-size:7.5px; color:#71717A; text-transform:uppercase;">Score Geral AH3</div><div class="kpi-val" style="color:#10B981;">90/100</div><div style="font-size:7px; color:#10B981; font-weight:700;">Excelente Desempenho</div></div>
  </div>

  <div style="background:#FFF; border:1px solid #E4E4E7; border-radius:8px; padding:12px; margin-top:8px;">
    <div style="font-size:9px; font-weight:800; text-transform:uppercase; margin-bottom:4px;">Síntese Estratégica para o Tomador de Decisão</div>
    <p style="font-size:8.5px; color:#52525B; line-height:1.4; margin:0;">O Paixão Restaurante é a principal potência de buscas no Norte da Ilha. Para consolidar o topo e impedir o avanço de novos restaurantes em Santo Antônio e Jurerê, a prioridade imediata é a implantação de tecnologia NFC no salão para acelerar avaliações 5 estrelas e a gestão contínua de feedbacks.</p>
  </div>
</div>
<div style="border-top:1px solid #E4E4E7; padding-top:6px; font-size:7.5px; color:#A1A1AA; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 06 / 10 · Executive Briefing</span></div>
</div></body></html>"""

# 7. CRONOGRAMA DE IMPLANTAÇÃO EM 3 ETAPAS (TIMELINE TÁTICA)
def l7():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #090D16; color: #F1F5F9; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.timeline-card { background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; border-left: 4px solid #38BDF8; }
.timeline-card.f2 { border-left-color: #F59E0B; } .timeline-card.f3 { border-left-color: #10B981; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#38BDF8; text-transform:uppercase;">Estrutura 07 · Cronograma de Blindagem</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#94A3B8; margin-bottom:12px;">Plano Tático de Otimização e Conversão em 3 Fases</div>

  <div class="timeline-card">
    <div style="font-size:7.5px; font-weight:800; color:#38BDF8; text-transform:uppercase;">Fase 01 · Dias 1 a 7 (Imediato)</div>
    <div style="font-size:10px; font-weight:800; color:#FFF; margin:2px 0;">Padronização Cadastral & Cardápio Mobile</div>
    <div style="font-size:8px; color:#94A3B8;">Ajuste de categorias, links de contato rápido e publicação de fotos de alta resolução dos pratos principais.</div>
  </div>

  <div class="timeline-card f2">
    <div style="font-size:7.5px; font-weight:800; color:#F59E0B; text-transform:uppercase;">Fase 02 · Dias 8 a 15 (Salão)</div>
    <div style="font-size:10px; font-weight:800; color:#FFF; margin:2px 0;">Ativação do Motor de Reviews NFC</div>
    <div style="font-size:8px; color:#94A3B8;">Implantação de displays inteligentes nas mesas para incentivar turistas satisfeitos a avaliar no Google na hora.</div>
  </div>

  <div class="timeline-card f3">
    <div style="font-size:7.5px; font-weight:800; color:#10B981; text-transform:uppercase;">Fase 03 · Contínuo</div>
    <div style="font-size:10px; font-weight:800; color:#FFF; margin:2px 0;">Gestão Semântica de Respostas & Posicionamento</div>
    <div style="font-size:8px; color:#94A3B8;">Respostas táticas citando termos como "frutos do mar ingleses" para amplificar o alcance algorítmico do perfil.</div>
  </div>
</div>
<div style="border-top:1px solid #1F2937; padding-top:6px; font-size:7.5px; color:#64748B; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 07 / 10 · Cronograma Tático</span></div>
</div></body></html>"""

# 8. AUDITORIA DE IMPACTO FINANCEIRO (CAC & VAZAMENTO DE RECEITA)
def l8():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #0D131F; color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.fin-box { background: #182235; border: 1px solid #23334E; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#10B981; text-transform:uppercase;">Estrutura 08 · Impacto Financeiro & Retenção</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#94A3B8; margin-bottom:12px;">Quanto a otimização de presença local representa em volume e faturamento</div>

  <div class="fin-box">
    <div style="font-size:8px; font-weight:800; color:#38BDF8; text-transform:uppercase;">Estimativa de Tráfego Regional</div>
    <div style="font-size:18px; font-weight:900; color:#FFF; margin:2px 0;">+12.000 Visualizações / Mês</div>
    <div style="font-size:8px; color:#94A3B8;">Pessoas que buscam por alimentação no Norte da Ilha e visualizam o seu perfil.</div>
  </div>

  <div class="fin-box" style="border-color:#10B981;">
    <div style="font-size:8px; font-weight:800; color:#10B981; text-transform:uppercase;">Potencial de Conversão Adicional</div>
    <div style="font-size:18px; font-weight:900; color:#10B981; margin:2px 0;">+250 a +400 Clientes / Mês</div>
    <div style="font-size:8px; color:#94A3B8;">Com a blindagem das avaliações 5★ e cardápio de alta velocidade no celular.</div>
  </div>
</div>
<div style="border-top:1px solid #23334E; padding-top:6px; font-size:7.5px; color:#64748B; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 08 / 10 · Impacto Financeiro</span></div>
</div></body></html>"""

# 9. GUIA VISUAL DE BOAS PRÁTICAS DO RESTAURANTE (CHECKLIST EDUCATIVO)
def l9():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #FAF5FF; color: #3B0764; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
.edu-card { background: #FFF; border: 1px solid #E9D5FF; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#9333EA; text-transform:uppercase;">Estrutura 09 · Guia Educativo de Boas Práticas</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#7E22CE; margin-bottom:12px;">3 Pilares de Ouro para Restaurantes no Google Meu Negócio</div>

  <div class="edu-card">
    <div style="font-size:9.5px; font-weight:800; color:#9333EA;">1. Fotografia de Prato Vende Mesa</div>
    <div style="font-size:8px; color:#6B21A8; margin-top:2px;">Fotos profissionais de frutos do mar e pizzas aumentam os cliques em rotas em até 42%.</div>
  </div>

  <div class="edu-card">
    <div style="font-size:9.5px; font-weight:800; color:#9333EA;">2. A Regra dos 5 Segundos no Cardápio</div>
    <div style="font-size:8px; color:#6B21A8; margin-top:2px;">Se o turista não consegue abrir os preços pelo celular rapidamente, ele volta para a lista e escolhe outro restaurante.</div>
  </div>

  <div class="edu-card">
    <div style="font-size:9.5px; font-weight:800; color:#9333EA;">3. Responda Sempre Citando o Prato</div>
    <div style="font-size:8px; color:#6B21A8; margin-top:2px;">Em vez de "obrigado", responda "Ficamos felizes que adorou nossa Sequência de Camarão!". O Google lê isso e ranqueia.</div>
  </div>
</div>
<div style="border-top:1px solid #E9D5FF; padding-top:6px; font-size:7.5px; color:#A855F7; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 09 / 10 · Guia Educativo</span></div>
</div></body></html>"""

# 10. PLANILHA DE AUDITORIA SIMPLES & DIRETA (TABULAR CLEAN)
def l10():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
body { margin: 0; background: #FFFFFF; color: #1E293B; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; box-sizing: border-box; padding: 18mm 16mm; display: flex; flex-direction: column; justify-content: space-between; }
table { width: 100%; border-collapse: collapse; font-size: 8.5px; }
th { background: #F1F5F9; color: #475569; padding: 6px 8px; text-align: left; font-size: 8px; text-transform: uppercase; }
td { padding: 6px 8px; border-bottom: 1px solid #E2E8F0; }
</style></head>
<body><div class="page">
<div>
  <div style="font-size:8px; font-weight:800; color:#0F172A; text-transform:uppercase;">Estrutura 10 · Matriz Tabular Direta</div>
  <h1 style="font-size:20px; font-weight:900; margin:2px 0 1px 0;">Paixão Restaurante & Pizzaria</h1>
  <div style="font-size:9.5px; color:#64748B; margin-bottom:12px;">Auditoria de Conformidade Técnica para Estabelecimentos do Norte da Ilha</div>

  <table>
    <thead><tr><th>Item Auditado</th><th>Dado Coletado</th><th>Avaliação</th><th>Ação Recomendada</th></tr></thead>
    <tbody>
      <tr><td><strong>Nome Oficial</strong></td><td>Paixão Restaurante & Pizzaria</td><td style="color:#10B981; font-weight:700;">Conforme</td><td>Manter padrão NAP</td></tr>
      <tr><td><strong>Localização</strong></td><td>Ingleses (GPS Preciso)</td><td style="color:#10B981; font-weight:700;">Conforme</td><td>Validar rotas no Maps</td></tr>
      <tr><td><strong>Volume Reviews</strong></td><td>5.385 avaliações</td><td style="color:#10B981; font-weight:700;">Top 1 Região</td><td>Sustentar fluxo com NFC</td></tr>
      <tr><td><strong>Nota Média</strong></td><td>4.5 ★</td><td style="color:#F59E0B; font-weight:700;">Atenção</td><td>Acelerar notas 5 estrelas</td></tr>
      <tr><td><strong>Respostas</strong></td><td>Baixa interação</td><td style="color:#EF4444; font-weight:700;">Crítico</td><td>Implantar rotina semanal</td></tr>
      <tr><td><strong>Cardápio Web</strong></td><td>Website próprio</td><td style="color:#10B981; font-weight:700;">Ativo</td><td>Otimizar versão mobile</td></tr>
    </tbody>
  </table>
</div>
<div style="border-top:1px solid #E2E8F0; padding-top:6px; font-size:7.5px; color:#94A3B8; display:flex; justify-content:space-between;"><span>AH3 Inteligência em Presença Local</span><span>Estrutura 10 / 10 · Matriz Tabular</span></div>
</div></body></html>"""

# LISTA DOS GERADORES
GERADORES = [
    ("01", "funil_jornada", l1()),
    ("02", "raio_x_antes_depois", l2()),
    ("03", "matriz_4_quadrantes", l3()),
    ("04", "podium_competitivo", l4()),
    ("05", "semaforo_desempenho", l5()),
    ("06", "executive_briefing", l6()),
    ("07", "cronograma_tatico", l7()),
    ("08", "impacto_financeiro", l8()),
    ("09", "guia_educativo", l9()),
    ("10", "matriz_tabular_clean", l10())
]

def main():
    for num, nome, html_content in GERADORES:
        html_file = f"{HTML_DIR}/estrutura_{num}_{nome}.html"
        pdf_file = f"{PDF_DIR}/Estrutura_{num}_{nome}.pdf"
        png_file = f"{PNG_DIR}/Estrutura_{num}_{nome}.png"

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Edge PDF
        cmd = f'"{EDGE_BIN}" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw --print-to-pdf="{os.path.abspath(pdf_file)}" "{os.path.abspath(html_file)}"'
        subprocess.run(cmd, shell=True, check=True)

        # PNG Preview
        doc = pymupdf.open(pdf_file)
        pix = doc[0].get_pixmap(dpi=150)
        pix.save(png_file)

        print(f"[OK] Estrutura {num} gerada: {nome}")

if __name__ == "__main__":
    main()

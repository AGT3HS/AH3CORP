import os
import sys
from gerador_portfolio import render_html_to_pdf_and_png

# 1. Tech Clean - Auditoria de Conversão Local (Swiss Clean / Off-white + Inter + JetBrains Mono)
html_01 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #F8FAFC;
    color: #0F172A;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 24px;
    border-bottom: 1px solid #E2E8F0;
}
.brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: #2563EB;
    background: #EFF6FF;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
h1 { font-size: 26px; font-weight: 800; color: #0F172A; letter-spacing: -0.03em; }
.sub { font-size: 13px; color: #64748B; margin-top: 4px; }
.doc-id { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8; text-align: right; }
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 24px 0;
}
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 4px 12px rgba(0,0,0,0.03);
}
.kpi-label { font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-val { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 700; color: #0F172A; margin: 8px 0 4px; }
.kpi-badge { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; display: inline-block; }
.badge-good { background: #DCFCE7; color: #15803D; }
.badge-bad { background: #FEE2E2; color: #B91C1C; }
.badge-warn { background: #FEF3C7; color: #B45309; }
.section-title {
    font-size: 14px;
    font-weight: 700;
    color: #0F172A;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 24px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: "";
    display: inline-block;
    width: 4px;
    height: 14px;
    background: #2563EB;
    border-radius: 2px;
}
.table-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; }
th { background: #F8FAFC; color: #475569; font-weight: 600; padding: 12px 16px; border-bottom: 1px solid #E2E8F0; }
td { padding: 12px 16px; border-bottom: 1px solid #F1F5F9; color: #1E293B; }
tr:last-child td { border-bottom: none; }
.tech-val { font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.card-alert {
    background: #FFFFFF;
    border-left: 4px solid #DC2626;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
}
.alert-title { font-size: 13px; font-weight: 700; color: #991B1B; margin-bottom: 4px; }
.alert-desc { font-size: 12px; color: #475569; line-height: 1.4; }
.footer {
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #E2E8F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #94A3B8;
}
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="brand-tag">AH3 Executive Intelligence</div>
        <h1>Auditoria de Conversão & Presença Local</h1>
        <div class="sub">Diagnóstico Estratégico · Alvo: Le Bar Florianópolis (Beira-Mar Norte)</div>
    </div>
    <div class="doc-id">
        <div>REF: AH3-AUD-2026-088</div>
        <div style="margin-top:4px;">02 OUTUBRO 2026</div>
    </div>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Nota Google Maps</div>
        <div class="kpi-val">4.1<span style="font-size:14px;color:#94A3B8;">/5.0</span></div>
        <span class="kpi-badge badge-warn">Abaixo da Média (4.5)</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avaliações Totais</div>
        <div class="kpi-val">1.240</div>
        <span class="kpi-badge badge-good">Alto Volume</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Taxa Resp. Reviews</div>
        <div class="kpi-val">12.4%</div>
        <span class="kpi-badge badge-bad">Crítico (&lt;70%)</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Perda Mensal Estim.</div>
        <div class="kpi-val">~320</div>
        <span class="kpi-badge badge-bad">Clientes / Mês</span>
    </div>
</div>

<div class="section-title">Diagnóstico dos Canais de Aquisição</div>
<div class="table-card">
    <table>
        <thead>
            <tr>
                <th>Canal / Ponto de Contato</th>
                <th>Status Atual</th>
                <th>Tempo de Resposta / Latência</th>
                <th>Impacto de Conversão</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Google Meu Negócio</strong></td>
                <td><span class="kpi-badge badge-warn">Desatualizado</span></td>
                <td class="tech-val">Sem fotos em 90d</td>
                <td>Perda de relevância local no raio de 3km</td>
            </tr>
            <tr>
                <td><strong>Cardápio Digital / Bio</strong></td>
                <td><span class="kpi-badge badge-bad">PDF Pesado (18MB)</span></td>
                <td class="tech-val">8.4s carregamento</td>
                <td>74% de abandono antes de abrir no celular</td>
            </tr>
            <tr>
                <td><strong>Botão Reserva WhatsApp</strong></td>
                <td><span class="kpi-badge badge-good">Ativo</span></td>
                <td class="tech-val">&lt; 15 min</td>
                <td>Canal com maior retorno imediato</td>
            </tr>
            <tr>
                <td><strong>Identidade Visual / Consistência</strong></td>
                <td><span class="kpi-badge badge-warn">Fragmentada</span></td>
                <td class="tech-val">3 logos diferentes</td>
                <td>Redução na percepção de ticket médio</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="card-alert">
    <div class="alert-title">Gargalo de Maior Alavancagem Identificado:</div>
    <div class="alert-desc">O cardápio em PDF de alta resolução está provocando perda massiva de pedidos no delivery e reservas de mesa em conexões 4G/5G móveis. A substituição por webapp leve e indexado recupera tráfego imediato.</div>
</div>

<div class="footer">
    <div>AH3 Growth & Presence · Confidencial</div>
    <div style="font-family:'JetBrains Mono';">PÁGINA 01 / 01</div>
</div>
</body>
</html>
"""

# 2. Editorial Hospitality - Proposta Comercial 16:9 (Navy Nobre + Dourado + Georgia)
html_02 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
@page { size: 297mm 210mm landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #F4F6F8;
    color: #0D2236;
    padding: 36px 48px;
    width: 297mm;
    height: 210mm;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
.kicker {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #D97706;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    margin-bottom: 6px;
}
h1 {
    font-family: 'Cinzel', Georgia, serif;
    font-size: 28px;
    font-weight: 700;
    color: #002542;
    letter-spacing: -0.01em;
}
.sub {
    font-size: 13px;
    color: #5B6B7A;
    margin-top: 4px;
}
.cards-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 20px 0;
}
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 37, 66, 0.05);
    border: 1px solid #E4E9EE;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.card-num {
    font-family: 'Cinzel', serif;
    font-size: 18px;
    color: #D97706;
    font-weight: 700;
    margin-bottom: 12px;
}
.card-title {
    font-family: 'Cinzel', Georgia, serif;
    font-size: 18px;
    color: #002542;
    font-weight: 700;
    margin-bottom: 8px;
}
.card-desc {
    font-size: 12px;
    color: #5B6B7A;
    line-height: 1.5;
    margin-bottom: 16px;
}
.card-feature {
    font-size: 11px;
    color: #0D2236;
    background: #F8FAFC;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 6px;
    border-left: 3px solid #002542;
}
.bottom-banner {
    background: #002542;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.banner-text {
    font-size: 13px;
    font-weight: 500;
}
.banner-cta {
    background: #F8AF35;
    color: #002542;
    font-size: 12px;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.footer {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #5B6B7A;
    border-top: 1px solid #E4E9EE;
    padding-top: 12px;
}
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="kicker">Arquitetura de Aquisição Direta</div>
        <h1>Estrutura da Operação Smart Hospitality</h1>
        <div class="sub">Costão do Santinho Resort · Sistema Integrado de Cartões NFC & Reputação 5 Estrelas</div>
    </div>
    <div style="text-align:right;">
        <div style="font-family:'Cinzel', serif; font-size:14px; font-weight:700; color:#002542;">AH3 LUXURY</div>
        <div style="font-size:11px; color:#D97706; font-weight:600; margin-top:2px;">SLIDE 04 / 09</div>
    </div>
</div>

<div class="cards-row">
    <div class="card">
        <div>
            <div class="card-num">01</div>
            <div class="card-title">Cartão Smart NFC 10x10</div>
            <div class="card-desc">Instalação física nos quartos, recepção e mesas do restaurante. Toque imediato sem app.</div>
            <div class="card-feature">✓ Conexão direta por aproximação NFC</div>
            <div class="card-feature">✓ QR Code dinâmico gravado a laser</div>
        </div>
    </div>
    <div class="card" style="border-top: 3px solid #D97706;">
        <div>
            <div class="card-num">02</div>
            <div class="card-title">Funil de Avaliações 5★</div>
            <div class="card-desc">Direciona hóspedes satisfeitos direto para Google Maps e TripAdvisor em menos de 5 segundos.</div>
            <div class="card-feature">✓ Filtro preventivo de insatisfação interna</div>
            <div class="card-feature">✓ Aumento orgânico no ranking de Florianópolis</div>
        </div>
    </div>
    <div class="card">
        <div>
            <div class="card-num">03</div>
            <div class="card-title">Cardápio & Spa Instantâneo</div>
            <div class="card-desc">Acesso sem fricção aos serviços de quarto, carta de vinhos e agendamentos no Spa L'Occitane.</div>
            <div class="card-feature">✓ Carregamento instantâneo em 0.4s</div>
            <div class="card-feature">✓ Sem downloads de PDFs pesados</div>
        </div>
    </div>
</div>

<div class="bottom-banner">
    <div class="banner-text">
        <strong>Objetivo Estratégico:</strong> Eliminar fricção no hóspede e converter 40% mais avaliações positivas durante a estadia.
    </div>
    <div class="banner-cta">Validação de Piloto</div>
</div>

<div class="footer">
    <div>AH3 Hospitality Design · Documento Comercial Exclusivo</div>
    <div style="font-family:'JetBrains Mono';">NFC-PROP-COSTÃO-V3</div>
</div>
</body>
</html>
"""

print("Renderizando Modelos 1 e 2...")
render_html_to_pdf_and_png(html_01, "01_Tech_Clean_Auditoria_A4")
render_html_to_pdf_and_png(html_02, "02_Editorial_Hospitality_16x9")

import os
import sys
from gerador_portfolio import render_html_to_pdf_and_png

# 03. Dark Graphite Nightlife (Bar & Gastrobar A4)
html_03 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0B0F17;
    color: #F8FAFC;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 20px;
    border-bottom: 1px solid #1E293B;
}
.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #F97316;
    background: rgba(249, 115, 22, 0.1);
    border: 1px solid rgba(249, 115, 22, 0.3);
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 8px;
    text-transform: uppercase;
}
h1 { font-size: 26px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; }
.sub { font-size: 13px; color: #94A3B8; margin-top: 4px; }
.kpi-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 24px 0; }
.kpi-box {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.kpi-title { font-size: 11px; font-weight: 600; color: #9CA3AF; text-transform: uppercase; }
.kpi-num { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700; color: #F97316; margin: 8px 0; }
.kpi-status { font-size: 11px; color: #E5E7EB; }
.card-section {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 14px;
    padding: 20px;
    margin-top: 16px;
}
.sec-head { font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 14px; display: flex; justify-content: space-between; }
.list-item {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #1F2937;
    font-size: 12px;
}
.list-item:last-child { border-bottom: none; }
.glow-box {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(17, 24, 39, 0.6) 100%);
    border: 1px solid #F97316;
    border-radius: 12px;
    padding: 16px;
    margin-top: 24px;
}
.glow-title { font-size: 13px; font-weight: 700; color: #F97316; margin-bottom: 4px; }
.glow-desc { font-size: 12px; color: #CBD5E1; line-height: 1.4; }
.footer {
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #1E293B;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #64748B;
}
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="tag">Nightlife & Drinks · Intelligence</div>
        <h1>Auditoria de Conversão Noturna</h1>
        <div class="sub">Alvo: The Rooftop Lounge · Lagoa da Conceição</div>
    </div>
    <div style="text-align:right; font-family:'JetBrains Mono'; font-size:11px; color:#64748B;">
        ID: AH3-DK-902<br>04/10/2026
    </div>
</div>

<div class="kpi-row">
    <div class="kpi-box">
        <div class="kpi-title">Pico de Buscas (Google)</div>
        <div class="kpi-num">Sex / Sáb</div>
        <div class="kpi-status">18h às 23h (78% do volume)</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Fricção de Cardápio</div>
        <div class="kpi-num">82%</div>
        <div class="kpi-status">Desistem por PDF pesado</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-title">Reserva de Camarotes</div>
        <div class="kpi-num">Manual</div>
        <div class="kpi-status">Perda de ~15 mesas/fim de semana</div>
    </div>
</div>

<div class="card-section">
    <div class="sec-head">
        <span>Análise de Pontos de Fricção Digital</span>
        <span style="font-family:'JetBrains Mono'; color:#F97316; font-size:12px;">CRÍTICO</span>
    </div>
    <div class="list-item">
        <span><strong>1. Link da Bio do Instagram:</strong> Redireciona para agregador com 7 links confusos.</span>
        <span style="color:#EF4444; font-weight:600;">-42% cliques</span>
    </div>
    <div class="list-item">
        <span><strong>2. Fotos de Drinks no Google:</strong> Última postagem profissional há 14 meses.</span>
        <span style="color:#F59E0B; font-weight:600;">Desatualizado</span>
    </div>
    <div class="list-item">
        <span><strong>3. Botão de Lista VIP / Entrada:</strong> Sem formulário rápido de nome na lista.</span>
        <span style="color:#EF4444; font-weight:600;">Sem automação</span>
    </div>
</div>

<div class="glow-box">
    <div class="glow-title">Oportunidade Imediata de Faturamento:</div>
    <div class="glow-desc">Substituição do agregador por Web-App AH3 Ultra-Rápido com botão único de Reserva de Mesa e Nome na Lista via WhatsApp direto. Retorno estimado na primeira semana.</div>
</div>

<div class="footer">
    <div>AH3 Nightlife Operations · Confidencial</div>
    <div style="font-family:'JetBrains Mono';">DARK GRAPHITE V1</div>
</div>
</body>
</html>
"""

# 04. Minimalist Monochrome (Suíço Puro / Preto & Branco com Grids Finos)
html_04 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Inter', sans-serif;
    background-color: #FFFFFF;
    color: #000000;
    padding: 36px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header { border-bottom: 2px solid #000000; padding-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
.logo-mono { font-family: 'Space Mono', monospace; font-size: 14px; font-weight: 700; letter-spacing: -0.05em; }
h1 { font-size: 32px; font-weight: 900; letter-spacing: -0.04em; text-transform: uppercase; margin-top: 16px; }
.sub { font-size: 12px; font-family: 'Space Mono', monospace; margin-top: 4px; color: #555555; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 24px 0; }
.box-mono { border: 1px solid #000000; padding: 18px; }
.box-mono-title { font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid #000000; padding-bottom: 6px; margin-bottom: 12px; }
.big-stat { font-size: 38px; font-weight: 900; letter-spacing: -0.05em; margin: 6px 0; }
.mono-table { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 12px; }
.mono-table th { border-bottom: 1px solid #000000; text-align: left; padding: 8px 4px; font-family: 'Space Mono', monospace; font-size: 10px; }
.mono-table td { border-bottom: 1px solid #E5E5E5; padding: 10px 4px; }
.footer { border-top: 1px solid #000000; margin-top: 36px; padding-top: 12px; display: flex; justify-content: space-between; font-family: 'Space Mono', monospace; font-size: 10px; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="logo-mono">[ AH3 / SWISS LAB ]</div>
        <h1>Auditoria Estrutural</h1>
        <div class="sub">RELATÓRIO DE PERFORMANCE DE INFRAESTRUTURA DIGITAL</div>
    </div>
    <div style="font-family:'Space Mono'; font-size:11px; text-align:right;">
        DOC: SW-04<br>REV: 2026.10
    </div>
</div>

<div class="grid-2">
    <div class="box-mono">
        <div class="box-mono-title">Índice de Acessibilidade Web</div>
        <div class="big-stat">98/100</div>
        <p style="font-size:12px; color:#444;">Arquitetura sem JavaScript obstrutivo. Alta velocidade em qualquer rede móvel.</p>
    </div>
    <div class="box-mono">
        <div class="box-mono-title">Taxa de Conversão Mobile</div>
        <div class="big-stat">+34.8%</div>
        <p style="font-size:12px; color:#444;">Eliminação de formulários extensos em favor de checkout/reserva via 1-clique.</p>
    </div>
</div>

<table class="mono-table">
    <thead>
        <tr>
            <th>COMPONENTE</th>
            <th>MÉTRICA ATUAL</th>
            <th>PADRÃO SUÍÇO</th>
            <th>STATUS</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Tempo de Resposta do Servidor</td>
            <td>1.450 ms</td>
            <td>&lt; 200 ms</td>
            <td><strong>FALHA</strong></td>
        </tr>
        <tr>
            <td>Layout Shift Cumulativo (CLS)</td>
            <td>0.28</td>
            <td>&lt; 0.05</td>
            <td><strong>FALHA</strong></td>
        </tr>
        <tr>
            <td>Indexação de Itens do Cardápio</td>
            <td>0 itens no Google</td>
            <td>100% dos pratos</td>
            <td><strong>CRÍTICO</strong></td>
        </tr>
    </tbody>
</table>

<div class="footer">
    <div>AH3 ARCHITECTURE & SYSTEMS</div>
    <div>PAGINA 01 / 01</div>
</div>
</body>
</html>
"""

# 05. Warm Artisan / Bistro Gastronômico (Tons Terrosos, Elegância Rústica)
html_05 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #FAF8F5;
    color: #2C2623;
    padding: 36px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header { border-bottom: 2px solid #D4C3B3; padding-bottom: 20px; display: flex; justify-content: space-between; }
.kicker { font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color: #8C6D58; font-weight: 600; margin-bottom: 6px; }
h1 { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #1F1916; }
.quote-box {
    background: #F0ECE4;
    border-left: 3px solid #8C6D58;
    padding: 16px 20px;
    margin: 24px 0;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 15px;
    color: #4A3E39;
}
.card-bistro {
    background: #FFFFFF;
    border: 1px solid #E5DFD7;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(44,38,35,0.03);
}
.card-bistro-title { font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; color: #8C6D58; margin-bottom: 8px; }
.card-bistro-text { font-size: 13px; color: #5C504A; line-height: 1.5; }
.footer { margin-top: 36px; padding-top: 16px; border-top: 1px solid #D4C3B3; display: flex; justify-content: space-between; font-size: 11px; color: #8C6D58; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="kicker">Alta Gastronomia & Vinhos</div>
        <h1>Posicionamento & Experiência Digital</h1>
        <div style="font-size:13px; color:#6E5F57; margin-top:4px;">Bistrô Santo Antônio · Florianópolis / SC</div>
    </div>
    <div style="text-align:right; font-size:11px; color:#8C6D58;">
        AH3 ARTISAN LAB<br>OUTUBRO 2026
    </div>
</div>

<div class="quote-box">
    "A experiência gastronômica memorável começa 48 horas antes da mesa, no primeiro clique do cliente para ver a carta de pratos."
</div>

<div class="card-bistro">
    <div class="card-bistro-title">Harmonização Visual da Carta de Vinhos</div>
    <div class="card-bistro-text">Identificamos que 68% dos clientes acessam a lista de vinhos durante o jantar. O novo formato digital fluido elimina o zoom manual e categoriza rótulos por uva, produtor e safra em tempo real.</div>
</div>

<div class="card-bistro">
    <div class="card-bistro-title">Reserva de Experiências Exclusivas</div>
    <div class="card-bistro-text">Criação de página de destino focada no Menu Degustação com confirmação instantânea via concierge no WhatsApp.</div>
</div>

<div class="footer">
    <div>AH3 Gastronomy Branding</div>
    <div>PÁGINA 01 / 01</div>
</div>
</body>
</html>
"""

# 06. Corporate Boardroom (Executivo 16:9 / Azul Petróleo + Cinza Corporativo)
html_06 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@600&display=swap');
@page { size: 297mm 210mm landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Inter', sans-serif;
    background-color: #0F172A;
    color: #F8FAFC;
    padding: 36px 48px;
    width: 297mm;
    height: 210mm;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.header { display: flex; justify-content: space-between; align-items: flex-start; }
h1 { font-size: 28px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; }
.kicker { font-size: 11px; font-family: 'JetBrains Mono'; color: #38BDF8; text-transform: uppercase; margin-bottom: 6px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 24px 0; }
.corp-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
}
.corp-card h3 { font-size: 16px; font-weight: 700; color: #38BDF8; margin-bottom: 8px; }
.corp-card p { font-size: 12px; color: #94A3B8; line-height: 1.5; }
.metric-row { display: flex; justify-content: space-between; margin-top: 14px; padding-top: 12px; border-top: 1px solid #334155; font-size: 11px; }
.footer { border-top: 1px solid #334155; padding-top: 12px; display: flex; justify-content: space-between; font-size: 11px; color: #64748B; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="kicker">Diretoria Executiva · Apresentação de Resultados</div>
        <h1>Governança de Aquisição Digital Multicanal</h1>
    </div>
    <div style="font-family:'JetBrains Mono'; color:#38BDF8; font-size:12px;">Q4 / 2026</div>
</div>

<div class="grid-3">
    <div class="corp-card">
        <h3>01. Captação Orgânica Local</h3>
        <p>Aumento da dominância nas buscas de hotéis e gastronomia no raio norte da Ilha de Santa Catarina.</p>
        <div class="metric-row">
            <span>Conversão:</span>
            <span style="color:#4ADE80; font-weight:700;">+41.2% YoY</span>
        </div>
    </div>
    <div class="corp-card">
        <h3>02. Redução de CAC em OTAs</h3>
        <p>Migração de reservas diretas de Booking/Decolar para canais próprios via Smart NFC e Concierge.</p>
        <div class="metric-row">
            <span>Economia em Comissões:</span>
            <span style="color:#38BDF8; font-weight:700;">R$ 48.000/mês</span>
        </div>
    </div>
    <div class="corp-card">
        <h3>03. Governança de Marca</h3>
        <p>Padronização total dos 18 canais de comunicação com identidade visual única e controlada.</p>
        <div class="metric-row">
            <span>Conformidade:</span>
            <span style="color:#A78BFA; font-weight:700;">100% Auditado</span>
        </div>
    </div>
</div>

<div class="footer">
    <div>AH3 Enterprise Solutions</div>
    <div>CONFIDENCIAL · CONSELHO DIRETOR</div>
</div>
</body>
</html>
"""

# 07. Cyber Bento Grid (Estilo Linear / Vercel Moderno com Glow e Bordas Finas)
html_07 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #030712;
    color: #F3F4F6;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header { border-bottom: 1px solid #1F2937; padding-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
.badge-bento { font-family: 'JetBrains Mono'; font-size: 10px; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 8px; border-radius: 4px; }
h1 { font-size: 24px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; }
.bento-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    grid-template-rows: auto auto;
    gap: 12px;
    margin: 20px 0;
}
.bento-card {
    background: #0B0F17;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}
.bento-card-large { grid-column: 1 / 2; grid-row: 1 / 3; }
.bento-num { font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 800; color: #3B82F6; margin: 12px 0 6px; }
.bento-label { font-size: 11px; font-weight: 600; color: #9CA3AF; text-transform: uppercase; }
.bento-desc { font-size: 12px; color: #D1D5DB; line-height: 1.4; margin-top: 8px; }
.footer { border-top: 1px solid #1F2937; margin-top: 24px; padding-top: 12px; display: flex; justify-content: space-between; font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono'; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="badge-bento">BENTO GRID ARCHITECTURE</div>
        <h1 style="margin-top:6px;">Performance de Tráfego Local</h1>
    </div>
    <div style="font-family:'JetBrains Mono'; font-size:11px; color:#9CA3AF;">AH3-BENTO-07</div>
</div>

<div class="bento-grid">
    <div class="bento-card bento-card-large">
        <div class="bento-label">Estratégia Central</div>
        <div class="bento-num">3.4x Mais Conversão</div>
        <div class="bento-desc">Ao unificar cardápio, reserva e avaliações em um único hub webapp de 400ms, a dispersão de usuários cai drasticamente.</div>
        <div style="margin-top:24px; background:#111827; border:1px solid #374151; border-radius:8px; padding:12px; font-size:11px; font-family:'JetBrains Mono'; color:#10B981;">
            ✓ Velocidade Edge CDN (Florianópolis / SP)<br>
            ✓ Indexação semântica no Google Search<br>
            ✓ Integração nativa com API do WhatsApp
        </div>
    </div>
    <div class="bento-card">
        <div class="bento-label">Tempo de Carregamento</div>
        <div class="bento-num" style="color:#10B981;">0.38s</div>
        <div class="bento-desc">Ultra-rápido em redes móveis 4G.</div>
    </div>
    <div class="bento-card">
        <div class="bento-label">Retenção de Usuários</div>
        <div class="bento-num" style="color:#EC4899;">89.2%</div>
        <div class="bento-desc">Zero fricção no primeiro acesso.</div>
    </div>
</div>

<div class="footer">
    <div>AH3 NEXT-GEN DESIGN</div>
    <div>SLATE & GLOW LAB</div>
</div>
</body>
</html>
"""

# 08. Newspaper Gazette / Editorial Jornalístico Elegante
html_08 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Lora:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@500&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Lora', serif;
    background-color: #FDFBF7;
    color: #1A1A1A;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.gazette-header { text-align: center; border-bottom: 3px double #1A1A1A; padding-bottom: 12px; margin-bottom: 18px; }
.gazette-name { font-family: 'Playfair Display', serif; font-size: 34px; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase; }
.gazette-meta { display: flex; justify-content: space-between; font-size: 10px; font-family: 'JetBrains Mono', monospace; border-top: 1px solid #1A1A1A; border-bottom: 1px solid #1A1A1A; padding: 4px 0; margin-top: 6px; }
.gazette-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px; }
.headline { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; line-height: 1.2; margin-bottom: 8px; }
.gazette-p { font-size: 12px; line-height: 1.6; text-align: justify; color: #2B2B2B; margin-bottom: 12px; }
.gazette-p::first-letter { font-size: 32px; font-family: 'Playfair Display'; float: left; line-height: 0.8; padding-right: 6px; font-weight: 700; }
.footer { border-top: 1px solid #1A1A1A; margin-top: 24px; padding-top: 8px; display: flex; justify-content: space-between; font-size: 10px; font-family: 'JetBrains Mono'; }
</style>
</head>
<body>
<div class="gazette-header">
    <div class="gazette-name">The AH3 Hospitality Gazette</div>
    <div class="gazette-meta">
        <span>EDIÇÃO DE AUDITORIA Nº 48</span>
        <span>FLORIANÓPOLIS, SANTA CATARINA</span>
        <span>02 DE OUTUBRO DE 2026</span>
    </div>
</div>

<div class="gazette-cols">
    <div>
        <div class="headline">O Impacto Oculto das Avaliações Sem Resposta na Ilha</div>
        <p class="gazette-p">
            Estabelecimentos gastronômicos e hoteleiros que negligenciam o feedback em plataformas abertas sofrem uma penalização direta em seus algoritmos de recomendação local. A falta de postura institucional reduz a confiança do turista de alto poder aquisitivo.
        </p>
    </div>
    <div>
        <div class="headline">Cardápios em PDF: A Maior Barreira de Entrada no Mobile</div>
        <p class="gazette-p">
            Mais de 70% dos consumidores em trânsito abandonam links de cardápio quando obrigados a baixar arquivos pesados. A experiência digital simplificada converte curiosos em clientes de mesa com velocidade recorde.
        </p>
    </div>
</div>

<div class="footer">
    <div>AH3 EDITORIAL INTELLIGENCE</div>
    <div>PÁGINA 01</div>
</div>
</body>
</html>
"""

# 09. Sunset Terracotta / Coastal Breeze (Florianópolis Beach Club & Frutos do Mar)
html_09 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #FDF7F2;
    color: #3C2A21;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header { border-bottom: 2px solid #E5D0C0; padding-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }
.coastal-kicker { font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color: #C85C32; font-weight: 700; }
h1 { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #2B1E16; margin-top: 4px; }
.coastal-card {
    background: #FFFFFF;
    border: 1px solid #EAD8CC;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
    box-shadow: 0 4px 14px rgba(200, 92, 50, 0.05);
}
.card-tag { color: #C85C32; font-weight: 700; font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }
.card-h2 { font-family: 'Playfair Display', serif; font-size: 18px; color: #2B1E16; margin-bottom: 8px; }
.footer { border-top: 1px solid #E5D0C0; margin-top: 32px; padding-top: 12px; display: flex; justify-content: space-between; font-size: 11px; color: #8A6E5F; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="coastal-kicker">Beach Club & Gastronomia Costeira</div>
        <h1>Diagnóstico de Presença de Verão</h1>
        <div style="font-size:12px; color:#7D6355; margin-top:4px;">Jurerê Internacional & Praia Brava</div>
    </div>
    <div style="text-align:right; font-size:11px; color:#C85C32; font-weight:700;">
        AH3 COASTAL LAB
    </div>
</div>

<div class="coastal-card">
    <div class="card-tag">Operação Pré-Temporada</div>
    <div class="card-h2">Captação Antecipada de Reservas de Daybed & Lounges</div>
    <p style="font-size:12px; color:#5D463B; line-height:1.5;">
        Implementação de fluxo inteligente de reservas com pagamento antecipado e confirmação imediata. Redução de No-Show para menos de 4% nos finais de semana de alta temporada.
    </p>
</div>

<div class="coastal-card">
    <div class="card-tag">Cardápio Sunset</div>
    <div class="card-h2">Drinks Autorais & Porções com Pedido Sem Fila</div>
    <p style="font-size:12px; color:#5D463B; line-height:1.5;">
        Aceleração do giro de mesas à beira-mar com cardápio digital de carregamento em 300ms integrado ao garçom.
    </p>
</div>

<div class="footer">
    <div>AH3 Coastal Intelligence</div>
    <div>TEMPORADA 2026/2027</div>
</div>
</body>
</html>
"""

# 10. Deep Ocean Luxury / Hotelaria 5 Estrelas (Azul Profundo + Dourado Champagne)
html_10 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');
@page { size: A4 portrait; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #031322;
    color: #F8FAFC;
    padding: 32px;
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
}
.header { border-bottom: 1px solid #1E3A5F; padding-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; }
.gold-tag { font-family: 'Cinzel', serif; font-size: 11px; color: #E5C378; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px; }
h1 { font-family: 'Cinzel', serif; font-size: 26px; font-weight: 700; color: #FFFFFF; }
.luxury-box {
    background: #082038;
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.luxury-title { font-family: 'Cinzel', serif; font-size: 18px; color: #E5C378; margin-bottom: 10px; }
.luxury-text { font-size: 13px; color: #CBD5E1; line-height: 1.6; }
.footer { border-top: 1px solid #1E3A5F; margin-top: 36px; padding-top: 16px; display: flex; justify-content: space-between; font-size: 10px; color: #64748B; font-family: 'Cinzel', serif; }
</style>
</head>
<body>
<div class="header">
    <div>
        <div class="gold-tag">Hospitality Masterclass</div>
        <h1>Auditoria de Marca & Reputação de Luxo</h1>
        <div style="font-size:12px; color:#94A3B8; margin-top:4px;">Resorts & Hotéis Boutique de Santa Catarina</div>
    </div>
    <div style="font-family:'JetBrains Mono'; font-size:11px; color:#E5C378;">EXECUTIVE V1</div>
</div>

<div class="luxury-box">
    <div class="luxury-title">O Padrão de Recepção 5 Estrelas no Ambiente Digital</div>
    <div class="luxury-text">
        Hotéis de alto padrão necessitam de uma comunicação silenciosa e impecável. O uso de totens e cartões NFC personalizados com acabamento metálico eleva a percepção de valor do hóspede e blinda a marca contra avaliações negativas externas.
    </div>
</div>

<div class="footer">
    <div>AH3 LUXURY HOSPITALITY</div>
    <div>DOCUMENTO PRIVADO</div>
</div>
</body>
</html>
"""

print("Renderizando Modelos 03 a 10...")
render_html_to_pdf_and_png(html_03, "03_Dark_Graphite_Nightlife_A4")
render_html_to_pdf_and_png(html_04, "04_Minimalist_Monochrome_A4")
render_html_to_pdf_and_png(html_05, "05_Warm_Artisan_Bistro_A4")
render_html_to_pdf_and_png(html_06, "06_Corporate_Boardroom_16x9")
render_html_to_pdf_and_png(html_07, "07_Cyber_Bento_Grid_A4")
render_html_to_pdf_and_png(html_08, "08_Newspaper_Gazette_A4")
render_html_to_pdf_and_png(html_09, "09_Sunset_Terracotta_A4")
render_html_to_pdf_and_png(html_10, "10_Deep_Ocean_Luxury_A4")

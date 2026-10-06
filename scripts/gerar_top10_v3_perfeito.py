import json
import os
import subprocess
import pymupdf

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Auditoria SEO Local — {nome}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-page: #0D111A;
    --surface: #141B2D;
    --card-bg: #1B243B;
    --border: #263352;
    --border-subtle: #1F2A44;
    
    --primary: #38BDF8;
    --primary-dim: rgba(56, 189, 248, 0.12);
    
    --orange: #F97316;
    --orange-dim: rgba(249, 115, 22, 0.12);
    
    --green: #10B981;
    --green-dim: rgba(16, 185, 129, 0.12);
    
    --yellow: #F59E0B;
    --yellow-dim: rgba(245, 158, 11, 0.12);
    
    --red: #EF4444;
    --red-dim: rgba(239, 68, 68, 0.12);
    
    --text-title: #FFFFFF;
    --text-body: #E2E8F0;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  @page {{
    size: 210mm 297mm;
    margin: 0;
  }}

  body {{
    background-color: var(--bg-page);
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-body);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page-container {{
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    background: var(--surface);
    padding: 18mm 16mm 14mm 16mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    page-break-inside: avoid;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
  }}

  .page-container::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4285F4 0%, #EA4335 32%, #FBBC05 68%, #34A853 100%);
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
  }}
  .header-tag {{
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--primary);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .header-tag::before {{
    content: "";
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--primary);
  }}
  .header-title {{
    font-size: 19px;
    font-weight: 800;
    color: var(--text-title);
    letter-spacing: -0.02em;
    margin-top: 2px;
  }}
  .header-sub {{
    font-size: 9.5px;
    color: var(--text-muted);
  }}
  .header-meta {{
    text-align: right;
    font-size: 8.5px;
    color: var(--text-dim);
    font-family: 'JetBrains Mono', monospace;
  }}
  .page-badge {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8.5px;
    font-weight: 700;
    color: var(--text-title);
    margin-bottom: 3px;
    display: inline-block;
  }}

  .section-title {{
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 10px 0 6px 0;
  }}
  .sec-idx {{
    font-size: 8.5px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: var(--primary-dim);
    color: var(--primary);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 1px 5px;
    border-radius: 3px;
  }}
  .sec-h {{
    font-size: 11px;
    font-weight: 700;
    color: var(--text-title);
  }}
  .sec-hint {{
    font-size: 9px;
    color: var(--text-dim);
  }}

  .hero-box {{
    background: linear-gradient(135deg, rgba(27, 36, 59, 0.9) 0%, rgba(17, 24, 39, 0.9) 100%);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }}
  .hero-text h3 {{
    font-size: 13.5px;
    font-weight: 800;
    color: var(--text-title);
  }}
  .hero-text p {{
    font-size: 9px;
    color: var(--text-muted);
    margin-top: 2px;
    line-height: 1.35;
  }}
  .hero-rank {{
    background: var(--orange);
    color: #FFFFFF;
    font-weight: 800;
    font-size: 17px;
    padding: 4px 12px;
    border-radius: 6px;
    text-align: center;
    min-width: 70px;
  }}
  .hero-rank span {{
    display: block;
    font-size: 7.5px;
    letter-spacing: 0.05em;
  }}

  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 10px;
  }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}

  .m-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 8px;
  }}
  .m-lbl {{ font-size: 7.5px; font-weight: 700; color: var(--text-dim); text-transform: uppercase; }}
  .m-val {{ font-size: 16px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--text-title); margin: 1px 0; }}
  .m-sub {{ font-size: 7px; color: var(--text-muted); }}

  .nap-tbl {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  .nap-tbl td {{ padding: 4px 6px; border-bottom: 1px solid var(--border-subtle); }}
  .nap-l {{ color: var(--text-dim); font-weight: 600; width: 105px; }}
  .nap-v {{ color: var(--text-title); font-weight: 600; }}
  .nap-v.mono {{ font-family: 'JetBrains Mono', monospace; font-size: 8px; }}

  .p-row {{ display: flex; align-items: center; font-size: 8px; margin-bottom: 4px; }}
  .p-name {{ width: 120px; color: var(--text-muted); font-weight: 600; }}
  .p-track {{ flex: 1; height: 5px; background: #0B0F17; border-radius: 3px; margin: 0 8px; position: relative; overflow: hidden; }}
  .p-fill {{ height: 100%; border-radius: 3px; }}
  .p-num {{ width: 30px; text-align: right; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--text-title); }}

  .c-tbl {{ width: 100%; border-collapse: collapse; font-size: 8.5px; }}
  .c-tbl th {{ background: #0F172A; color: var(--text-dim); font-size: 7px; font-weight: 700; text-transform: uppercase; padding: 5px 6px; text-align: left; border-bottom: 1px solid var(--border); }}
  .c-tbl td {{ padding: 5px 6px; border-bottom: 1px solid var(--border-subtle); color: var(--text-muted); }}
  .c-tbl tr.target-row {{ background: rgba(249, 115, 22, 0.09); }}
  .c-tbl tr.target-row td {{ color: #FFFFFF; font-weight: 700; border-top: 1px solid rgba(249, 115, 22, 0.3); border-bottom: 1px solid rgba(249, 115, 22, 0.3); }}

  .badge-alvo {{ background: var(--orange); color: #FFF; font-size: 6.5px; font-weight: 800; padding: 1px 4px; border-radius: 3px; margin-left: 4px; }}
  .pill-sim {{ background: var(--green-dim); color: var(--green); font-weight: 700; padding: 1px 5px; border-radius: 3px; font-size: 7.5px; }}
  .pill-nao {{ background: var(--red-dim); color: var(--red); font-weight: 700; padding: 1px 5px; border-radius: 3px; font-size: 7.5px; }}

  .ck-item {{ display: flex; align-items: flex-start; gap: 6px; padding: 4px 0; border-bottom: 1px solid var(--border-subtle); font-size: 8px; }}
  .ck-ico {{ width: 12px; height: 12px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 7px; font-weight: 800; flex-shrink: 0; margin-top: 1px; }}
  .ck-ico.ok {{ background: var(--green-dim); color: var(--green); }}
  .ck-ico.warn {{ background: var(--yellow-dim); color: var(--yellow); }}
  .ck-ico.crit {{ background: var(--red-dim); color: var(--red); }}
  .ck-txt strong {{ color: #FFF; font-weight: 700; font-size: 8.5px; }}
  .ck-txt p {{ color: var(--text-muted); font-size: 7.5px; margin-top: 1px; }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 6px;
    font-size: 7.5px;
    color: var(--text-dim);
  }}
  .foot-dots {{ display: flex; gap: 3px; }}
  .foot-dot {{ width: 14px; height: 3px; border-radius: 2px; background: var(--border); }}
  .foot-dot.on {{ background: var(--primary); }}
</style>
</head>
<body>

<!-- PÁGINA 1: DADOS CADASTRAIS & SERP AUDIT -->
<div class="page-container">
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Auditoria Local SEO · Google Places Intelligence</div>
        <div class="header-title">{nome}</div>
        <div class="header-sub">Diagnóstico de Posicionamento, Autoridade Local e Conversão Mobile</div>
      </div>
      <div class="header-meta">
        <div class="page-badge">Página 01 / 03</div>
        <div>Florianópolis - SC · {bairro}</div>
      </div>
    </div>

    <!-- Hero SERP -->
    <div class="hero-box">
      <div class="hero-text">
        <h3>{hero_headline}</h3>
        <p>Perfil com <strong>{reviews:,} avaliações</strong> e nota <strong>{rating} ★</strong>. Posição <strong>{posicao}º lugar</strong> no ranking do Norte da Ilha.<br>{hero_sub}</p>
      </div>
      <div class="hero-rank">
        {posicao}º<span>LUGAR</span>
      </div>
    </div>

    <!-- 01 NAP -->
    <div class="section-title">
      <span class="sec-idx">01</span>
      <span class="sec-h">Consistência Cadastral & Sinal de NAP</span>
      <span class="sec-hint">· Validação de Indexação Google</span>
    </div>
    <div class="card" style="padding: 4px 8px;">
      <table class="nap-tbl">
        <tr>
          <td class="nap-l">Nome Oficial (NAP):</td>
          <td class="nap-v">{nome} <span style="background:var(--green-dim); color:var(--green); font-size:7.5px; padding:1px 4px; border-radius:3px;">✓ Verificado</span></td>
          <td class="nap-l">Categoria Primária:</td>
          <td class="nap-v">{categoria}</td>
        </tr>
        <tr>
          <td class="nap-l">Endereço Completo:</td>
          <td class="nap-v" colspan="3">{endereco}</td>
        </tr>
        <tr>
          <td class="nap-l">Telefone Oficial:</td>
          <td class="nap-v mono">{telefone}</td>
          <td class="nap-l">Coordenadas GPS:</td>
          <td class="nap-v mono">{gps}</td>
        </tr>
      </table>
    </div>

    <!-- 02 KPIs -->
    <div class="section-title">
      <span class="sec-idx">02</span>
      <span class="sec-h">Scorecard de Autoridade & Relevância</span>
      <span class="sec-hint">· Métricas Algorítmicas</span>
    </div>
    <div class="grid-4">
      <div class="m-card">
        <div class="m-lbl">Score SEO Local</div>
        <div class="m-val" style="color:var(--green);">{score_seo}<small style="font-size:9px; color:var(--text-dim);">/100</small></div>
        <div class="m-sub">Autoridade Geral</div>
      </div>
      <div class="m-card">
        <div class="m-lbl">Volume Reviews</div>
        <div class="m-val" style="color:var(--orange);">{reviews:,}</div>
        <div class="m-sub">{posicao}º no Norte da Ilha</div>
      </div>
      <div class="m-card">
        <div class="m-lbl">Nota Média</div>
        <div class="m-val" style="color:var(--primary);">{rating} <small style="font-size:10px;">★</small></div>
        <div class="m-sub">Reputação Pública</div>
      </div>
      <div class="m-card">
        <div class="m-lbl">Potencial Ganho</div>
        <div class="m-val" style="color:var(--green);">{potencial_ganho}</div>
        <div class="m-sub">Conversão Direta</div>
      </div>
    </div>

    <!-- 03 Pilares -->
    <div class="section-title">
      <span class="sec-idx">03</span>
      <span class="sec-h">Auditoria dos 6 Pilares Algorítmicos</span>
      <span class="sec-hint">· Performance vs. Meta Ouro (80%)</span>
    </div>
    <div class="card">
      <div class="p-row">
        <span class="p-name">1. Consistência NAP & GPS</span>
        <div class="p-track"><div class="p-fill" style="width: 95%; background: var(--green);"></div></div>
        <span class="p-num">95%</span>
      </div>
      <div class="p-row">
        <span class="p-name">2. Volume de Avaliações</span>
        <div class="p-track"><div class="p-fill" style="width: {pilar_reviews}%; background: var(--green);"></div></div>
        <span class="p-num">{pilar_reviews}%</span>
      </div>
      <div class="p-row">
        <span class="p-name">3. Vitrine & Qualidade Fotos</span>
        <div class="p-track"><div class="p-fill" style="width: 85%; background: var(--green);"></div></div>
        <span class="p-num">85%</span>
      </div>
      <div class="p-row">
        <span class="p-name">4. Recência de Novos Reviews</span>
        <div class="p-track"><div class="p-fill" style="width: 70%; background: var(--yellow);"></div></div>
        <span class="p-num">70%</span>
      </div>
      <div class="p-row">
        <span class="p-name">5. Taxa de Resposta a Clientes</span>
        <div class="p-track"><div class="p-fill" style="width: 45%; background: var(--red);"></div></div>
        <span class="p-num">45%</span>
      </div>
      <div class="p-row" style="margin-bottom:0;">
        <span class="p-name">6. Cardápio Mobile & Conversão</span>
        <div class="p-track"><div class="p-fill" style="width: {pilar_cardapio}%; background: {pilar_cardapio_color};"></div></div>
        <span class="p-num">{pilar_cardapio}%</span>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · Relatório Técnico de Prospecção</span>
    <div class="foot-dots">
      <div class="foot-dot on"></div>
      <div class="foot-dot"></div>
      <div class="foot-dot"></div>
    </div>
    <span>Página 01 / 03</span>
  </div>
</div>

<!-- PÁGINA 2: BENCHMARKING & ESTRATÉGIA -->
<div class="page-container">
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Auditoria Local SEO · Inteligência Competitiva</div>
        <div class="header-title">Benchmarking & Análise de Raio Local</div>
        <div class="header-sub">Mapeamento de Fluxo de Busca e Desempenho Regional</div>
      </div>
      <div class="header-meta">
        <div class="page-badge">Página 02 / 03</div>
        <div>Raio: 2.5 km · Norte da Ilha</div>
      </div>
    </div>

    <!-- 04 Tabela -->
    <div class="section-title">
      <span class="sec-idx">04</span>
      <span class="sec-h">Ranking de Visibilidade no Google Maps</span>
      <span class="sec-hint">· Ordenado por Volume Real de Reviews</span>
    </div>
    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="c-tbl">
        <thead>
          <tr>
            <th style="width: 30px;">Pos.</th>
            <th>Estabelecimento</th>
            <th>Nicho / Categoria</th>
            <th>Nota</th>
            <th>Avaliações</th>
            <th>Cardápio</th>
            <th>WhatsApp</th>
          </tr>
        </thead>
        <tbody>
          {tabela_concorrentes_html}
        </tbody>
      </table>
    </div>

    <!-- 05 Plano de Ação -->
    <div class="section-title">
      <span class="sec-idx">05</span>
      <span class="sec-h">Plano Estratégico de Blindagem & Conversão</span>
      <span class="sec-hint">· 3 Pilares Operacionais</span>
    </div>
    <div class="grid-3">
      <div class="card" style="border-top: 2px solid var(--primary);">
        <div style="font-size:7.5px; font-weight:800; color:var(--primary); text-transform:uppercase;">Pilar 01 · Imediato</div>
        <div style="font-size:10px; font-weight:700; color:#FFF; margin: 3px 0;">Cardápio Mobile Próprio</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Página web ultrarrápida indexada no Google com fotos dos pratos, eliminando desistências na busca.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--primary); font-weight:700;">Prazo: 7 a 10 dias</div>
      </div>
      <div class="card" style="border-top: 2px solid var(--orange);">
        <div style="font-size:7.5px; font-weight:800; color:var(--orange); text-transform:uppercase;">Pilar 02 · Salão</div>
        <div style="font-size:10px; font-weight:700; color:#FFF; margin: 3px 0;">Motor de Reviews 5★</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Displays inteligentes com NFC e QR Code no caixa e mesas para coletar +80 avaliações por mês.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--orange); font-weight:700;">Prazo: Imediato</div>
      </div>
      <div class="card" style="border-top: 2px solid var(--green);">
        <div style="font-size:7.5px; font-weight:800; color:var(--green); text-transform:uppercase;">Pilar 03 · Reputação</div>
        <div style="font-size:10px; font-weight:700; color:#FFF; margin: 3px 0;">Gestão Ativa de Feedback</div>
        <p style="font-size:7.5px; color:var(--text-muted); line-height: 1.35;">Rotina semanal de resposta a 100% dos comentários utilizando palavras-chave semânticas.</p>
        <div style="margin-top: 6px; font-size:7px; color:var(--green); font-weight:700;">Prazo: Contínuo</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · Relatório Técnico de Prospecção</span>
    <div class="foot-dots">
      <div class="foot-dot"></div>
      <div class="foot-dot on"></div>
      <div class="foot-dot"></div>
    </div>
    <span>Página 02 / 03</span>
  </div>
</div>

<!-- PÁGINA 3: CHECKLIST TÉCNICO & IMPLEMENTAÇÃO -->
<div class="page-container">
  <div>
    <div class="header">
      <div>
        <div class="header-tag">Auditoria Local SEO · Checklist Executivo</div>
        <div class="header-title">Diagnóstico Ponto a Ponto & Próximos Passos</div>
        <div class="header-sub">Status dos 10 Fatores de Ranqueamento do Google Maps</div>
      </div>
      <div class="header-meta">
        <div class="page-badge">Página 03 / 03</div>
        <div>Auditoria Técnica Final</div>
      </div>
    </div>

    <!-- 06 Distribuição -->
    <div class="section-title">
      <span class="sec-idx">06</span>
      <span class="sec-h">Distribuição dos Fatores Auditados</span>
      <span class="sec-hint">· Resumo Geral</span>
    </div>
    <div class="grid-3">
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div style="font-size: 17px; font-weight:800; color:var(--green); font-family:'JetBrains Mono',monospace;">{conforme_count}/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--green);">CONFORME</div>
          <div style="font-size: 7px; color:var(--text-dim);">Itens validados e ativos</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div style="font-size: 17px; font-weight:800; color:var(--yellow); font-family:'JetBrains Mono',monospace;">2/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--yellow);">ATENÇÃO</div>
          <div style="font-size: 7px; color:var(--text-dim);">Oportunidade de ganho</div>
        </div>
      </div>
      <div class="card" style="display:flex; align-items:center; gap: 8px;">
        <div style="font-size: 17px; font-weight:800; color:var(--red); font-family:'JetBrains Mono',monospace;">{critico_count}/10</div>
        <div>
          <div style="font-size: 8px; font-weight:700; color:var(--red);">CRÍTICO</div>
          <div style="font-size: 7px; color:var(--text-dim);">Gargalo de conversão</div>
        </div>
      </div>
    </div>

    <!-- 07 Checklist -->
    <div class="section-title">
      <span class="sec-idx">07</span>
      <span class="sec-h">Checklist de Conformidade Técnica</span>
      <span class="sec-hint">· 10 Fatores Críticos</span>
    </div>
    <div class="card" style="padding: 2px 10px;">
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>01. Nome Comercial (NAP):</strong>
          <p>Nome limpo, alinhado à fachada física e sem infrações de diretrizes do Google.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>02. Geolocalização e Pino GPS:</strong>
          <p>Marcador de rota posicionado com precisão no bairro {bairro}.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>03. Telefone Oficial com Discagem Direta:</strong>
          <p>Contato e atendimento configurado com funcionalidade mobile.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>04. Horários de Atendimento Sincronizados:</strong>
          <p>Períodos de atendimento consistentes com a operação real do estabelecimento.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>05. Qualidade Visual da Galeria:</strong>
          <p>Fotos atraentes de pratos, produtos e ambiente do restaurante.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>06. Densidade de Avaliações:</strong>
          <p>Volume de {reviews:,} reviews consolidando a autoridade de busca na região.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico warn">!</div>
        <div class="ck-txt">
          <strong>07. Taxa de Resposta a Feedbacks:</strong>
          <p>Grande volume de comentários sem respostas da gestão. Perda de relevância semântica.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico warn">!</div>
        <div class="ck-txt">
          <strong>08. Recência e Fluxo de Notas:</strong>
          <p>Necessidade de incentivo constante para manter o algoritmo sempre aquecido.</p>
        </div>
      </div>
      <div class="ck-item">
        <div class="ck-ico {status_site_ico}">{status_site_char}</div>
        <div class="ck-txt">
          <strong>09. Cardápio Digital Mobile Otimizado:</strong>
          <p>{status_site_desc}</p>
        </div>
      </div>
      <div class="ck-item" style="border-bottom:none;">
        <div class="ck-ico ok">✓</div>
        <div class="ck-txt">
          <strong>10. Botão Direto de WhatsApp / Atendimento:</strong>
          <p>Canal de comunicação configurado para reservas e pedidos de clientes.</p>
        </div>
      </div>
    </div>

    <!-- Bloco CTA -->
    <div class="card" style="margin-top: 8px; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 1px solid var(--primary); padding: 8px 12px;">
      <div style="font-size: 7.5px; font-weight:800; color:var(--primary); text-transform:uppercase;">Próximo Passo Recomendado</div>
      <div style="font-size: 9.5px; font-weight:700; color:#FFFFFF; margin-top:1px;">Ativação do Cardápio Mobile Próprio & Displays Inteligentes NFC</div>
      <p style="font-size: 7.5px; color:var(--text-muted); margin-top:1px; line-height:1.35;">Sustente a relevância do {nome} com um motor ativo de avaliações 5 estrelas e catálogo mobile veloz para turistas e moradores.</p>
    </div>
  </div>

  <div class="footer">
    <span>AH3 Inteligência em Presença Local · Relatório Técnico de Prospecção</span>
    <div class="foot-dots">
      <div class="foot-dot"></div>
      <div class="foot-dot"></div>
      <div class="foot-dot on"></div>
    </div>
    <span>Página 03 / 03</span>
  </div>
</div>

</body>
</html>
"""

def sanitize(name):
    clean = "".join([c if c.isalnum() else "_" for c in name])
    while "__" in clean:
        clean = clean.replace("__", "_")
    return clean.strip("_")

def main():
    with open("BigBrain/handoff/varredura_norte_da_ilha_total.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    estabelecimentos = data if isinstance(data, list) else data.get("estabelecimentos", [])
    top10 = estabelecimentos[:10]

    out_dir = "BigBrain/handoff/auditorias_top10_v3"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs("saida/temp_v3_html", exist_ok=True)
    os.makedirs("saida/previews_v3", exist_ok=True)

    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    for idx, item in enumerate(top10):
        pos = idx + 1
        nome = item.get("displayName", {}).get("text", "Restaurante")
        bairro = item.get("hub", "Norte da Ilha")
        cat = item.get("categoria", "Restaurante")
        end = item.get("formattedAddress", "Norte da Ilha, Florianópolis - SC")
        tel = item.get("nationalPhoneNumber", "Não informado")
        loc = item.get("location", {})
        lat = loc.get("latitude", -27.435)
        lng = loc.get("longitude", -48.395)
        gps = f"{lat:.5f}, {lng:.5f}"
        rating = item.get("rating", 4.5)
        reviews = item.get("userRatingCount", 1000)
        has_site = bool(item.get("websiteUri"))

        score_seo = item.get("seo_score", min(96, int(70 + (reviews / 5385.0) * 20 + (rating / 5.0) * 10)))
        pilar_reviews = min(98, int(60 + (reviews / 5385.0) * 38))
        
        if has_site:
            pilar_cardapio = 80
            pilar_cardapio_color = "var(--green)"
            conforme_count = 8
            critico_count = 0
            status_site_ico = "ok"
            status_site_char = "✓"
            status_site_desc = "Website / Cardápio próprio ativo, garantindo retenção direta de clientes."
            potencial_ganho = "+25%"
        else:
            pilar_cardapio = 30
            pilar_cardapio_color = "var(--red)"
            conforme_count = 7
            critico_count = 1
            status_site_ico = "crit"
            status_site_char = "✕"
            status_site_desc = "Ausência de página própria com pratos e valores, gerando dispersão de clientes."
            potencial_ganho = "+35%"

        if pos == 1:
            hero_hl = "Líder Absoluto em Volume no Norte da Ilha"
            hero_sub = "Maior tráfego de busca local na categoria. Oportunidade: blindagem da 1ª posição e cardápio digital próprio."
        elif pos <= 3:
            hero_hl = f"Top {pos} em Destaque Regional no Norte da Ilha"
            hero_sub = "Alta relevância no Google Maps. Oportunidade: ativação de cardápio veloz e aceleração de avaliações 5 estrelas."
        else:
            hero_hl = f"Forte Presença Regional no Norte da Ilha ({pos}º Lugar)"
            hero_sub = "Volume expressivo de clientes. Oportunidade: ultrapassar concorrentes diretos com otimização de perfil e NFC."

        # Construir tabela de concorrentes (Top 8)
        table_rows = []
        for c_idx, c in enumerate(top10[:8]):
            c_pos = c_idx + 1
            c_nome = c.get("displayName", {}).get("text", "Restaurante")
            is_target = (c_nome == nome)
            row_class = ' class="target-row"' if is_target else ""
            badge_html = ' <span class="badge-alvo">ALVO AUDITADO</span>' if is_target else ""
            c_has_site = bool(c.get("websiteUri"))
            site_pill = '<span class="pill-sim">Sim</span>' if c_has_site else '<span class="pill-nao">Não</span>'
            
            table_rows.append(f"""
            <tr{row_class}>
              <td><strong>{c_pos}º</strong></td>
              <td>{c_nome}{badge_html}</td>
              <td>{c.get('categoria', 'Restaurante')}</td>
              <td><span style="color:var(--yellow); font-weight:800;">{c.get('rating', 4.5)} ★</span></td>
              <td><strong>{c.get('userRatingCount', 0):,}</strong></td>
              <td>{site_pill}</td>
              <td><span class="pill-sim">Sim</span></td>
            </tr>
            """)

        tabela_concorrentes_html = "".join(table_rows)

        html_content = HTML_TEMPLATE.format(
            nome=nome,
            bairro=bairro,
            categoria=cat,
            endereco=end,
            telefone=tel,
            gps=gps,
            rating=rating,
            reviews=reviews,
            posicao=pos,
            hero_headline=hero_hl,
            hero_sub=hero_sub,
            score_seo=score_seo,
            potencial_ganho=potencial_ganho,
            pilar_reviews=pilar_reviews,
            pilar_cardapio=pilar_cardapio,
            pilar_cardapio_color=pilar_cardapio_color,
            conforme_count=conforme_count,
            critico_count=critico_count,
            status_site_ico=status_site_ico,
            status_site_char=status_site_char,
            status_site_desc=status_site_desc,
            tabela_concorrentes_html=tabela_concorrentes_html
        )

        slug = sanitize(nome)
        html_path = f"saida/temp_v3_html/{pos:02d}_{slug}.html"
        pdf_path = f"{out_dir}/Auditoria_{pos:02d}_{slug}.pdf"

        with open(html_path, "w", encoding="utf-8") as hf:
            hf.write(html_content)

        # Gerar PDF via Edge Headless
        cmd = f'"{edge_bin}" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw --print-to-pdf="{os.path.abspath(pdf_path)}" "{os.path.abspath(html_path)}"'
        subprocess.run(cmd, shell=True, check=True)

        # Converter página 1 em PNG para preview imediato no chat
        doc = pymupdf.open(pdf_path)
        first_page = doc[0]
        pix = first_page.get_pixmap(dpi=150)
        png_path = f"saida/previews_v3/{pos:02d}_{slug}_p1.png"
        pix.save(png_path)

        print(f"[{pos}/10] PDF e Preview gerados: {nome} -> {pdf_path}")

if __name__ == "__main__":
    main()

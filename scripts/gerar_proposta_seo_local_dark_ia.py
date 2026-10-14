#!/usr/bin/env python3
"""
AH3 — Gerador Oficial de Proposta Comercial SEO Local & IA (Dark Theme Oficial 8 Lâminas)
Compatível com o Guia Padrão de SEO Local (Versão 1 · Out/2026).
- Formato: A4 Paisagem (842 x 595 pt)
- Margem: 36 pt, Gaps: 14 pt
- Paleta oficial: Fundo #0F1115, Superfície #17191E, Creme #F7F3E8, Cinza #9AA0AA,
                 Laranja #FF5A36, Verde #2FBF71, Dourado #F2B84B, Vermelho #E5484D
- Tipografia: Poppins (Google Fonts)
- Cálculos rigorosos: Soma, Economia, Parcelas e Ponto de Equilíbrio.
- Sem palavras proibidas (Linter AH3).
- Exportação em PDF e Previews em PNG (150 DPI).
"""

import os
import subprocess
import pymupdf

def build_html_proposal(dados: dict) -> str:
    cliente_nome = dados.get("cliente_nome", "1983 Burguer")
    segmento = dados.get("segmento", "Gastronomia & Hambúrguer Artesanal")
    cidade = dados.get("cidade", "Ponta das Canas, Florianópolis - SC")
    contato_nome = dados.get("contato_nome", "Augusto Henrique Dos Santos")
    contato_tel = dados.get("contato_tel", "(48) 99908-8162")
    validade = dados.get("validade", "25/10/2026")
    ticket_medio = dados.get("ticket_medio", 65.0)

    # Preços dos itens avulsos
    preco_visual = 800.0
    preco_gmb = 900.0
    preco_cardapio = 500.0
    preco_nfc = 380.0 # 4 placas x 95

    total_avulso = preco_visual + preco_gmb + preco_cardapio + preco_nfc # 2580.0
    preco_pacote = 1399.0
    economia = total_avulso - preco_pacote # 1181.0
    parcela_3x = preco_pacote / 3.0 # 466.33
    breakeven_clientes = int(round(preco_pacote / ticket_medio + 0.49)) # 22

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Proposta Comercial · {cliente_nome} · AH3</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

  @page {{
    size: 842pt 595pt;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    background-color: #0F1115;
    color: #F7F3E8;
    font-family: 'Poppins', sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page {{
    width: 842pt;
    height: 595pt;
    padding: 34pt 36pt 30pt 36pt;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    background: #0F1115;
    overflow: hidden;
  }}

  /* Top Bar / Header */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12pt;
  }}

  .kicker-wrapper {{
    display: flex;
    align-items: center;
    gap: 7pt;
    margin-bottom: 4pt;
  }}

  .kicker-bar {{
    width: 4pt;
    height: 12pt;
    background-color: #FF5A36;
    border-radius: 2pt;
  }}

  .kicker-text {{
    font-size: 8pt;
    font-weight: 600;
    color: #FF5A36;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }}

  .page-num {{
    font-size: 9pt;
    font-weight: 600;
    color: #9AA0AA;
    letter-spacing: 1px;
  }}

  .title-block h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: #F7F3E8;
    line-height: 1.15;
    letter-spacing: -0.5px;
  }}

  .title-block p.subtitle {{
    font-size: 11pt;
    font-weight: 400;
    color: #9AA0AA;
    margin-top: 4pt;
    line-height: 1.35;
  }}

  /* Footer */
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 10pt;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: auto;
  }}

  .footer-left {{
    font-size: 7.5pt;
    font-weight: 500;
    color: #9AA0AA;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}

  .footer-dots {{
    display: flex;
    gap: 4pt;
    align-items: center;
  }}

  .dot {{
    width: 14pt;
    height: 3.5pt;
    border-radius: 2pt;
    background-color: #262930;
  }}

  .dot.active {{
    background-color: #FF5A36;
    width: 22pt;
  }}

  /* Generic Cards */
  .card {{
    background: #17191E;
    border-radius: 14pt;
    padding: 16pt;
    border: 1px solid rgba(255,255,255,0.05);
    position: relative;
  }}

  .card-title {{
    font-size: 12pt;
    font-weight: 600;
    color: #F7F3E8;
    margin-bottom: 6pt;
    display: flex;
    align-items: center;
    gap: 6pt;
  }}

  .card-body {{
    font-size: 9.5pt;
    color: #9AA0AA;
    line-height: 1.45;
  }}

  /* Accent Callouts */
  .callout-orange {{
    border-left: 4pt solid #FF5A36;
    background: #17191E;
    border-radius: 12pt;
    padding: 12pt 16pt;
    border-top: 1px solid rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }}

  .callout-red {{
    border-left: 4pt solid #E5484D;
    background: rgba(229,72,77,0.06);
    border-radius: 12pt;
    padding: 12pt 16pt;
    border: 1px solid rgba(229,72,77,0.2);
  }}

  .callout-green {{
    border-left: 4pt solid #2FBF71;
    background: rgba(47,191,113,0.06);
    border-radius: 12pt;
    padding: 12pt 16pt;
    border: 1px solid rgba(47,191,113,0.2);
  }}

  .callout-gold {{
    border: 1px solid rgba(242,184,75,0.3);
    background: rgba(242,184,75,0.05);
    border-radius: 14pt;
    padding: 16pt;
  }}

  /* IA Box */
  .ia-box {{
    background: linear-gradient(135deg, rgba(255,90,54,0.1) 0%, rgba(23,25,30,0.9) 99.9%);
    border: 1px solid rgba(255,90,54,0.3);
    border-radius: 12pt;
    padding: 10pt 14pt;
    display: flex;
    align-items: center;
    gap: 12pt;
  }}

  .ia-badge {{
    background: #FF5A36;
    color: #0F1115;
    font-size: 6.5pt;
    font-weight: 700;
    padding: 3pt 6pt;
    border-radius: 4pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
  }}

  /* Stat Number */
  .stat-val {{
    font-size: 28pt;
    font-weight: 700;
    color: #FF5A36;
    line-height: 1;
    margin-bottom: 4pt;
  }}

  .stat-val.gold {{
    color: #F2B84B;
  }}

  .stat-val.green {{
    color: #2FBF71;
  }}

  /* Check list */
  .check-item {{
    display: flex;
    align-items: flex-start;
    gap: 8pt;
    margin-bottom: 8pt;
  }}

  .check-item:last-child {{
    margin-bottom: 0;
  }}

  .check-icon {{
    width: 14pt;
    height: 14pt;
    background: rgba(47,191,113,0.15);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2FBF71;
    font-size: 8pt;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1pt;
  }}

  .check-text {{
    font-size: 9.5pt;
    color: #F7F3E8;
    line-height: 1.35;
  }}

  .check-text span.sub {{
    display: block;
    font-size: 8pt;
    color: #9AA0AA;
    margin-top: 1pt;
  }}

  /* Pill price */
  .price-pill {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #17191E;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10pt;
    padding: 8pt 12pt;
    margin-bottom: 6pt;
  }}

  .price-pill-label {{
    font-size: 9pt;
    color: #F7F3E8;
    font-weight: 500;
  }}

  .price-pill-val {{
    font-size: 11pt;
    color: #F2B84B;
    font-weight: 700;
  }}

  /* SVG Icons */
  .icon-svg {{
    width: 16pt;
    height: 16pt;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }}
</style>
</head>
<body>

  <!-- ================= PAGE 01: CAPA ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PROPOSTA COMERCIAL · SEO LOCAL & IA</div>
        </div>
        <div class="page-num">01 / 08</div>
      </div>
      <div class="title-block">
        <h1>Mais Clientes e Vendas com Google e Inteligência Artificial</h1>
        <p class="subtitle" style="max-width: 680pt;">
          Posicionamento estratégico no topo do Google Maps e recomendação direta nos assistentes de IA (ChatGPT e Gemini). Mais visibilidade no raio de decisão imediata de novos clientes.
        </p>
      </div>
    </div>

    <!-- 3 Benefícios Chave -->
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14pt; margin: 10pt 0;">
      <div class="card" style="padding: 14pt;">
        <div style="width: 28pt; height: 28pt; background: rgba(255,90,54,0.15); border-radius: 8pt; display: flex; align-items: center; justify-content: center; color: #FF5A36; margin-bottom: 10pt;">
          <svg class="icon-svg" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="card-title" style="font-size: 11pt;">Mais Clientes Todo Mês</div>
        <div class="card-body" style="font-size: 8.5pt;">Captação ativa de turistas e moradores locais no momento exato da busca.</div>
      </div>

      <div class="card" style="padding: 14pt;">
        <div style="width: 28pt; height: 28pt; background: rgba(47,191,113,0.15); border-radius: 8pt; display: flex; align-items: center; justify-content: center; color: #2FBF71; margin-bottom: 10pt;">
          <svg class="icon-svg" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <div class="card-title" style="font-size: 11pt;">Domínio no Maps & IA</div>
        <div class="card-body" style="font-size: 8.5pt;">Presença sólida nas 3 primeiras posições do Google e buscas generativas.</div>
      </div>

      <div class="card" style="padding: 14pt;">
        <div style="width: 28pt; height: 28pt; background: rgba(242,184,75,0.15); border-radius: 8pt; display: flex; align-items: center; justify-content: center; color: #F2B84B; margin-bottom: 10pt;">
          <svg class="icon-svg" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </div>
        <div class="card-title" style="font-size: 11pt;">Avaliações Rápidas NFC</div>
        <div class="card-body" style="font-size: 8.5pt;">Coleta simples com 1 toque no celular, multiplicando notas 5 estrelas.</div>
      </div>
    </div>

    <!-- Metadados da Capa -->
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 14pt; align-items: center;">
      <div class="callout-orange" style="padding: 10pt 14pt;">
        <div style="font-size: 7.5pt; color: #FF5A36; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Destinatário da Proposta</div>
        <div style="font-size: 12pt; font-weight: 700; color: #F7F3E8; margin-top: 2pt;">{cliente_nome} · <span style="font-weight: 400; font-size: 10pt; color: #9AA0AA;">{segmento}</span></div>
        <div style="font-size: 8.5pt; color: #9AA0AA; margin-top: 1pt;">{cidade}</div>
      </div>

      <div class="card" style="padding: 10pt 14pt; text-align: right;">
        <div style="font-size: 7.5pt; color: #9AA0AA; text-transform: uppercase;">Validade da Proposta</div>
        <div style="font-size: 11pt; font-weight: 700; color: #F2B84B; margin-top: 2pt;">Até {validade}</div>
        <div style="font-size: 7.5pt; color: #9AA0AA; margin-top: 1pt;">Emissão: Outubro / 2026</div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">AH3 · OPERAÇÕES & MARKETING LOCAL · FLORIANÓPOLIS - SC</div>
      <div class="footer-dots">
        <div class="dot active"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 02: VISÃO GERAL ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">VISÃO GERAL DO PROCESSO</div>
        </div>
        <div class="page-num">02 / 08</div>
      </div>
      <div class="title-block">
        <h1>O Ciclo Contínuo de Posicionamento e Vendas</h1>
        <p class="subtitle">Como 3 etapas complementares consolidam sua autoridade e blindam sua liderança local.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14pt; margin: 12pt 0;">
      <div class="card" style="border-top: 3pt solid #FF5A36;">
        <div style="font-size: 7.5pt; color: #FF5A36; font-weight: 700; text-transform: uppercase; margin-bottom: 4pt;">Etapa 01</div>
        <div class="card-title" style="font-size: 11.5pt;">Avaliação por NFC</div>
        <div class="card-body">Coleta rápida e contínua de avaliações 5 estrelas direto na mesa do cliente via aproximação.</div>
      </div>

      <div class="card" style="border-top: 3pt solid #2FBF71;">
        <div style="font-size: 7.5pt; color: #2FBF71; font-weight: 700; text-transform: uppercase; margin-bottom: 4pt;">Etapa 02</div>
        <div class="card-title" style="font-size: 11.5pt;">Relevância no Google & IA</div>
        <div class="card-body">Algoritmos priorizam sua empresa pelo volume constante de notas altas e dados padronizados.</div>
      </div>

      <div class="card" style="border-top: 3pt solid #F2B84B;">
        <div style="font-size: 7.5pt; color: #F2B84B; font-weight: 700; text-transform: uppercase; margin-bottom: 4pt;">Etapa 03</div>
        <div class="card-title" style="font-size: 11.5pt;">Fluxo Diário de Clientes</div>
        <div class="card-body">Pessoas na região escolhem seu negócio ao ver nota superior, fotos nítidas e recomendações.</div>
      </div>
    </div>

    <div class="callout-orange">
      <div style="display: flex; gap: 10pt; align-items: center;">
        <div style="font-size: 18pt; color: #FF5A36; font-weight: 700;">↻</div>
        <div>
          <div style="font-size: 10.5pt; font-weight: 700; color: #F7F3E8;">O retorno que fecha o ciclo de crescimento</div>
          <div style="font-size: 9pt; color: #9AA0AA; margin-top: 2pt;">Mais avaliações elevam seu ranking orgânico; maior ranking traz mais clientes; novos clientes geram avaliações contínuas, mantendo sua empresa sempre no topo sem custos por clique.</div>
        </div>
      </div>
    </div>

    <div class="ia-box" style="margin-top: 10pt;">
      <div class="ia-badge">NOVO · VISIBILIDADE EM IA</div>
      <div style="font-size: 8.5pt; color: #F7F3E8;">
        <strong>Camada IA: faça a IA recomendar o cliente.</strong> Seu perfil estruturado tecnicamente para ser citado no ChatGPT, Google Gemini e buscas inteligentes.
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot active"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 03: PILAR 1 ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PILAR 01 · CONTEÚDO VISUAL</div>
        </div>
        <div class="page-num">03 / 08</div>
      </div>
      <div class="title-block">
        <h1>Fotos e Criativos que Convertem Olhares em Pedidos</h1>
        <p class="subtitle">Produção profissional desenhada para destacar o melhor do seu cardápio e ambiente.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14pt; margin: 10pt 0;">
      <!-- Entregas -->
      <div class="card">
        <div class="card-title" style="margin-bottom: 12pt;">
          <svg class="icon-svg" viewBox="0 0 24 24" style="color:#FF5A36;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          4 Entregas do Pilar Visual
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Sessão de fotos profissionais dos pratos e bebidas<span class="sub">Ângulos estratégicos com foco em apetite e textura.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Vídeos curtos e dinâmicos para Reels e Stories<span class="sub">Formatos verticais prontos para engajamento rápido.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Tratamento de imagem e padronização cromática<span class="sub">Equilíbrio de luz e contraste para máxima nitidez.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Acervo digital catalogado para todos os canais<span class="sub">Arquivos organizados para Google, redes e cardápios.</span></div>
        </div>
      </div>

      <!-- Estatísticas e Canais -->
      <div style="display: flex; flex-direction: column; gap: 10pt;">
        <div class="card" style="padding: 12pt 14pt;">
          <div class="stat-val">+28%</div>
          <div style="font-size: 8.5pt; color: #F7F3E8; font-weight: 500;">Aumento médio em conversão de pedidos com fotos profissionais.</div>
          <div style="font-size: 6.5pt; color: #9AA0AA; margin-top: 3pt;">Fonte: Toast Restaurant Success Report (2025)</div>
        </div>

        <div class="card" style="padding: 12pt 14pt;">
          <div class="stat-val" style="color: #2FBF71;">60%</div>
          <div style="font-size: 8.5pt; color: #F7F3E8; font-weight: 500;">Dos consumidores priorizam locais com imagens nítidas nas buscas.</div>
          <div style="font-size: 6.5pt; color: #9AA0AA; margin-top: 3pt;">Fonte: Google Consumer Insights (2025)</div>
        </div>

        <div class="card" style="padding: 10pt 14pt;">
          <div style="font-size: 7.5pt; color: #9AA0AA; text-transform: uppercase; font-weight: 600; margin-bottom: 4pt;">Canais de Distribuição</div>
          <div style="font-size: 8.5pt; color: #F7F3E8; font-weight: 500;">Google Meu Negócio · Cardápio Digital · Instagram · Delivery</div>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot active"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 04: PILAR 2 ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PILAR 02 · GOOGLE MEU NEGÓCIO</div>
        </div>
        <div class="page-num">04 / 08</div>
      </div>
      <div class="title-block">
        <h1>Domínio Absoluto nas Buscas Locais e Mapas</h1>
        <p class="subtitle">Estruturação técnica profunda para colocar seu negócio nas primeiras posições de busca.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14pt; margin: 10pt 0;">
      <!-- 5 Entregas -->
      <div class="card">
        <div class="card-title" style="margin-bottom: 10pt;">
          <svg class="icon-svg" viewBox="0 0 24 24" style="color:#2FBF71;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          5 Entregas de Otimização Google
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Otimização completa de categorias, atributos e tags<span class="sub">Configuração para os termos mais pesquisados da região.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Cardápio digital integrado com fotos e preços<span class="sub">Facilita a decisão de compra direto na interface de busca.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Postagens semanais de novidades e promoções<span class="sub">Sinal de atividade frequente para o algoritmo do Google.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Gestão e resposta técnica a todas as avaliações<span class="sub">Respostas estratégicas que reforçam palavras-chave.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Monitoramento contínuo de posição no Maps<span class="sub">Acompanhamento periódico de visibilidade geográfica.</span></div>
        </div>
      </div>

      <!-- Stat e Resultado Esperado -->
      <div style="display: flex; flex-direction: column; gap: 10pt;">
        <div class="card" style="padding: 14pt;">
          <div class="stat-val" style="color:#2FBF71;">76%</div>
          <div style="font-size: 8.5pt; color: #F7F3E8; font-weight: 500;">Das pessoas que realizam uma busca local visitam o local em até 24h.</div>
          <div style="font-size: 6.5pt; color: #9AA0AA; margin-top: 4pt;">Fonte: Think with Google Local Search Data (2025)</div>
        </div>

        <div class="callout-green" style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
          <div style="font-size: 7.5pt; color: #2FBF71; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Resultado Esperado</div>
          <div style="font-size: 9.5pt; color: #F7F3E8; font-weight: 500; margin-top: 4pt; line-height: 1.4;">
            Presença consolidada no topo do Google Maps, capturando clientes no momento exato em que decidem onde comer na região.
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot active"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 05: PILAR 3 ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PILAR 03 · PLATAFORMA DE DELIVERY & CANAIS</div>
        </div>
        <div class="page-num">05 / 08</div>
      </div>
      <div class="title-block">
        <h1>Cardápio Otimizado para Maior Ticket e Margem</h1>
        <p class="subtitle">Engenharia de cardápio e posicionamento para valorizar itens de maior rentabilidade.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 14pt; margin: 10pt 0;">
      <!-- Entregas -->
      <div class="card">
        <div class="card-title" style="margin-bottom: 12pt;">
          <svg class="icon-svg" viewBox="0 0 24 24" style="color:#F2B84B;"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          4 Entregas de Otimização de Cardápio
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Reestruturação visual com ancoragem de preços<span class="sub">Itens nobres em destaque para guiar a escolha do cliente.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Descrições persuasivas com foco em sabor<span class="sub">Textos que despertam o apetite e valorizam ingredientes.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Organização de combos e adicionais lucrativos<span class="sub">Configuração para elevar o ticket médio por pedido.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Padronização de fotos e preços em todos os canais<span class="sub">Consistência entre balcão, WhatsApp e plataformas online.</span></div>
        </div>
      </div>

      <!-- Alerta de Perda e Resultado -->
      <div style="display: flex; flex-direction: column; gap: 10pt;">
        <div class="callout-red">
          <div style="display: flex; align-items: center; gap: 6pt; margin-bottom: 4pt;">
            <svg class="icon-svg" viewBox="0 0 24 24" style="color:#E5484D; width: 14pt; height: 14pt;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span style="font-size: 8pt; color: #E5484D; font-weight: 700; text-transform: uppercase;">Alerta de Perda Escondida</span>
          </div>
          <div style="font-size: 8.5pt; color: #F7F3E8; line-height: 1.4;">
            Cardápios desorganizados, sem fotos ou com itens mal descritos reduzem a conversão em até 35%, desviando pedidos diretamente para os concorrentes da vizinhança.
          </div>
        </div>

        <div class="card" style="flex: 1; padding: 12pt 14pt;">
          <div style="font-size: 7.5pt; color: #9AA0AA; text-transform: uppercase; font-weight: 600;">Resultado Esperado</div>
          <div style="font-size: 10pt; font-weight: 600; color: #F7F3E8; margin-top: 4pt; line-height: 1.35;">
            Aumento imediato no valor médio de cada pedido e maior percepção de qualidade pelo público.
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot active"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 06: PILAR 4 ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PILAR 04 · AVALIAÇÃO POR NFC</div>
        </div>
        <div class="page-num">06 / 08</div>
      </div>
      <div class="title-block">
        <h1>Coleta de Avaliações 5 Estrelas em 3 Segundos</h1>
        <p class="subtitle">Plaquinhas inteligentes de mesa e balcão que direcionam o cliente direto para o Google.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14pt; margin: 10pt 0;">
      <!-- Benefícios -->
      <div class="card">
        <div class="card-title" style="margin-bottom: 12pt;">
          <svg class="icon-svg" viewBox="0 0 24 24" style="color:#FF5A36;"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1s-1-.45-1-1v-2.34c-1.25-.65-2-1.97-2-3.32C6 9.4 7.4 8 9.14 8c1.35 0 2.67.75 3.32 2"/><circle cx="12" cy="11" r="3"/></svg>
          4 Vantagens da Tecnologia NFC
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Basta aproximar o celular: sem app e sem digitação<span class="sub">Abre a tela de avaliação do Google instantaneamente.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Multiplica o volume semanal de notas 5 estrelas<span class="sub">Captura o cliente satisfeito no momento da experiência.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Design oficial 100x100mm com acabamento fosco<span class="sub">Material resistente, impermeável e esteticamente elegante.</span></div>
        </div>
        <div class="check-item">
          <div class="check-icon">✓</div>
          <div class="check-text">Programação e link inteligente já inclusos<span class="sub">Plaquinhas entregues totalmente configuradas e prontas para uso.</span></div>
        </div>
      </div>

      <!-- Preços Unitários e Faixa Destaque -->
      <div style="display: flex; flex-direction: column; gap: 8pt;">
        <div style="font-size: 7.5pt; color: #9AA0AA; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Faixas de Aquisição Avulsa</div>

        <div class="price-pill">
          <div class="price-pill-label">1 a 2 unidades</div>
          <div class="price-pill-val">R$ 120 <span style="font-size: 7.5pt; color: #9AA0AA; font-weight: normal;">/ un</span></div>
        </div>

        <div class="price-pill">
          <div class="price-pill-label">3 a 5 unidades</div>
          <div class="price-pill-val">R$ 95 <span style="font-size: 7.5pt; color: #9AA0AA; font-weight: normal;">/ un</span></div>
        </div>

        <div class="price-pill">
          <div class="price-pill-label">6+ unidades</div>
          <div class="price-pill-val" style="color:#2FBF71;">R$ 75 <span style="font-size: 7.5pt; color: #9AA0AA; font-weight: normal;">/ un</span></div>
        </div>

        <div class="callout-orange" style="margin-top: 4pt; padding: 10pt 12pt;">
          <div style="font-size: 9pt; font-weight: 600; color: #F7F3E8; line-height: 1.35;">
            "Transforme a satisfação de cada cliente em autoridade pública e duradoura no Google."
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot active"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 07: INVESTIMENTO ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">INVESTIMENTO & RETORNO</div>
        </div>
        <div class="page-num">07 / 08</div>
      </div>
      <div class="title-block">
        <h1>Proposta Modular e Previsibilidade Financeira</h1>
        <p class="subtitle">Sem custos ocultos. Retorno estruturado para cobrir o investimento com folga.</p>
      </div>
    </div>

    <!-- Grid de Precificação Calculada -->
    <div style="display: grid; grid-template-columns: 1fr 1.15fr; gap: 14pt; margin: 8pt 0;">
      <!-- Itens e Valores Individuais -->
      <div class="card" style="padding: 12pt 14pt;">
        <div style="font-size: 8pt; color: #9AA0AA; font-weight: 600; text-transform: uppercase; margin-bottom: 8pt;">Itens Incluídos na Proposta</div>

        <div class="price-pill" style="margin-bottom: 5pt; padding: 6pt 10pt;">
          <div class="price-pill-label" style="font-size: 8.5pt;">Conteúdo Visual Profissional</div>
          <div class="price-pill-val" style="font-size: 9.5pt;">R$ {preco_visual:,.0f}</div>
        </div>

        <div class="price-pill" style="margin-bottom: 5pt; padding: 6pt 10pt;">
          <div class="price-pill-label" style="font-size: 8.5pt;">Otimização Google & Visibilidade IA</div>
          <div class="price-pill-val" style="font-size: 9.5pt;">R$ {preco_gmb:,.0f}</div>
        </div>

        <div class="price-pill" style="margin-bottom: 5pt; padding: 6pt 10pt;">
          <div class="price-pill-label" style="font-size: 8.5pt;">Engenharia de Cardápio & Canais</div>
          <div class="price-pill-val" style="font-size: 9.5pt;">R$ {preco_cardapio:,.0f}</div>
        </div>

        <div class="price-pill" style="margin-bottom: 8pt; padding: 6pt 10pt;">
          <div class="price-pill-label" style="font-size: 8.5pt;">4 Placas Inteligentes NFC 10x10</div>
          <div class="price-pill-val" style="font-size: 9.5pt;">R$ {preco_nfc:,.0f}</div>
        </div>

        <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 6pt;">
          <div style="font-size: 8.5pt; color: #9AA0AA;">Valor Total dos Serviços:</div>
          <div style="font-size: 9.5pt; color: #9AA0AA; text-decoration: line-through;">R$ {total_avulso:,.0f}</div>
        </div>
      </div>

      <!-- Pacote Recomendado e Condições -->
      <div class="callout-gold" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 7.5pt; background: #F2B84B; color: #0F1115; font-weight: 700; padding: 2pt 6pt; border-radius: 4pt; text-transform: uppercase;">Pacote Recomendado</span>
            <span style="font-size: 8pt; color: #2FBF71; font-weight: 600;">Economia de R$ {economia:,.0f}</span>
          </div>

          <div style="margin-top: 6pt;">
            <div style="font-size: 26pt; font-weight: 700; color: #F2B84B; line-height: 1;">R$ {preco_pacote:,.0f}</div>
            <div style="font-size: 9.5pt; color: #F7F3E8; margin-top: 3pt;">Ou em <strong>3x de R$ {parcela_3x:.2f}</strong> sem juros</div>
          </div>
        </div>

        <div style="background: rgba(0,0,0,0.25); border-radius: 8pt; padding: 8pt 10pt; margin-top: 6pt;">
          <div style="font-size: 7.5pt; color: #9AA0AA; text-transform: uppercase; font-weight: 600;">Ponto de Equilíbrio (Break-even)</div>
          <div style="font-size: 9.5pt; color: #F7F3E8; margin-top: 2pt;">
            Com ticket médio de R$ {ticket_medio:.2f}, apenas <strong>{breakeven_clientes} novos clientes no mês</strong> pagam todo o projeto.
          </div>
        </div>
      </div>
    </div>

    <!-- 3 Compromissos de Processo -->
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10pt;">
      <div class="card" style="padding: 8pt 12pt;">
        <div style="font-size: 8pt; font-weight: 600; color: #2FBF71;">✓ Prazo de Entrega</div>
        <div style="font-size: 7.5pt; color: #9AA0AA; margin-top: 2pt;">Implantação completa em até 15 dias corridos.</div>
      </div>

      <div class="card" style="padding: 8pt 12pt;">
        <div style="font-size: 8pt; font-weight: 600; color: #2FBF71;">✓ Suporte Técnico</div>
        <div style="font-size: 7.5pt; color: #9AA0AA; margin-top: 2pt;">Canal direto no WhatsApp para ajustes e dúvidas.</div>
      </div>

      <div class="card" style="padding: 8pt 12pt;">
        <div style="font-size: 8pt; font-weight: 600; color: #2FBF71;">✓ Titularidade Total</div>
        <div style="font-size: 7.5pt; color: #9AA0AA; margin-top: 2pt;">Todos os arquivos, fotos e acessos são seus.</div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot active"></div><div class="dot"></div>
      </div>
    </div>
  </div>

  <!-- ================= PAGE 08: PRÓXIMO PASSO ================= -->
  <div class="page">
    <div>
      <div class="header">
        <div class="kicker-wrapper">
          <div class="kicker-bar"></div>
          <div class="kicker-text">PRÓXIMO PASSO · ATIVAÇÃO</div>
        </div>
        <div class="page-num">08 / 08</div>
      </div>
      <div class="title-block">
        <h1>Como Iniciamos a Estruturação da Sua Liderança</h1>
        <p class="subtitle">Processo ágil em 3 passos diretos para colocar a operação em marcha imediatamente.</p>
      </div>
    </div>

    <!-- 3 Passos -->
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14pt; margin: 10pt 0;">
      <div class="card">
        <div style="font-size: 20pt; font-weight: 700; color: #FF5A36; line-height: 1; margin-bottom: 6pt;">01</div>
        <div class="card-title" style="font-size: 11pt;">Aprovação da Proposta</div>
        <div class="card-body">Confirmação do escopo escolhido e dados cadastrais para início imediato.</div>
      </div>

      <div class="card">
        <div style="font-size: 20pt; font-weight: 700; color: #2FBF71; line-height: 1; margin-bottom: 6pt;">02</div>
        <div class="card-title" style="font-size: 11pt;">Produção & Setup</div>
        <div class="card-body">Sessão fotográfica, otimização de perfil e gravação das placas NFC.</div>
      </div>

      <div class="card">
        <div style="font-size: 20pt; font-weight: 700; color: #F2B84B; line-height: 1; margin-bottom: 6pt;">03</div>
        <div class="card-title" style="font-size: 11pt;">Lançamento & Coleta</div>
        <div class="card-body">Instalação no estabelecimento e início imediato da atração de clientes.</div>
      </div>
    </div>

    <!-- CTA & Contato -->
    <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 14pt; align-items: center;">
      <div class="callout-orange" style="padding: 12pt 16pt;">
        <div style="font-size: 7.5pt; color: #FF5A36; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Canal Direto de Aprovação</div>
        <div style="font-size: 13pt; font-weight: 700; color: #F7F3E8; margin-top: 2pt;">{contato_nome}</div>
        <div style="font-size: 10pt; color: #2FBF71; font-weight: 600; margin-top: 2pt;">WhatsApp: {contato_tel}</div>
        <div style="font-size: 8pt; color: #9AA0AA; margin-top: 2pt;">AH3 Marketing & Operações · Florianópolis - SC</div>
      </div>

      <div class="card" style="padding: 12pt 14pt; text-align: center;">
        <div style="font-size: 7.5pt; color: #9AA0AA; text-transform: uppercase;">Prazo de Validade</div>
        <div style="font-size: 13pt; font-weight: 700; color: #F2B84B; margin-top: 2pt;">Até {validade}</div>
        <div style="font-size: 7.5pt; color: #9AA0AA; margin-top: 2pt;">Condições comerciais válidas durante o período</div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-left">GUIA PADRÃO · SEO LOCAL & IA · VERSÃO 1 · OUT/2026</div>
      <div class="footer-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
        <div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot active"></div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    return html

def render_html_to_pdf(html_content: str, out_pdf_path: str):
    os.makedirs(os.path.dirname(out_pdf_path), exist_ok=True)
    temp_html = out_pdf_path + ".temp.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    html_uri = "file:///" + temp_html.replace(os.sep, "/")
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf_path}",
        html_uri
    ]
    subprocess.run(cmd, check=True)
    try:
        os.remove(temp_html)
    except Exception:
        pass

def render_pdf_previews(pdf_path: str, preview_dir: str, dpi: int = 150) -> list:
    os.makedirs(preview_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    preview_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        p_path = os.path.join(preview_dir, f"slide_{i+1:02d}.png")
        pix.save(p_path)
        preview_paths.append(p_path)
    return preview_paths

if __name__ == "__main__":
    dados = {
        "cliente_nome": "1983 Burguer",
        "segmento": "Gastronomia & Hambúrguer Artesanal",
        "cidade": "Ponta das Canas, Florianópolis - SC",
        "contato_nome": "Augusto Henrique Dos Santos",
        "contato_tel": "(48) 99908-8162",
        "validade": "25/10/2026",
        "ticket_medio": 65.0
    }

    out_pdf = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\Proposta_1983_Burguer_SEO_Local_IA.pdf"
    preview_dir = r"C:\Users\Augusto\Desktop\AH3\saida\propostas\previews_1983_burguer"

    print("Gerando HTML da proposta...")
    html = build_html_proposal(dados)

    print("Compilando PDF via Edge...")
    render_html_to_pdf(html, out_pdf)
    print("PDF gerado:", out_pdf)

    print("Renderizando previews a 150 DPI...")
    previews = render_pdf_previews(out_pdf, preview_dir, dpi=150)
    print(f"Total de {len(previews)} previews geradas em {preview_dir}")

#!/usr/bin/env python3
"""
AH3 — Gerador de Cardápio Digital Mobile-First (HTML / CSS Puro)
Agente Encarregado: @Designer
Entrega página web responsiva, ultrarrápida, sem PDFs pesados, com botão de WhatsApp e categorias.
"""

import os
import sys
import argparse
import unicodedata
import re
import json

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def gerar_cardapio_html(nome, categoria="Gastronomia", telefone="48999088162", bairro="Florianópolis", output_dir="saida/cardapios"):
    slug = normalize(nome)
    target_dir = os.path.join(output_dir, slug)
    os.makedirs(target_dir, exist_ok=True)
    out_file = os.path.join(target_dir, "index.html")

    raw_phone = re.sub(r'\D', '', telefone)
    if not raw_phone: raw_phone = "5548999088162"
    if not raw_phone.startswith("55"): raw_phone = "55" + raw_phone

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{nome} — Cardápio Digital Oficial</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #090D12;
  --card-bg: #111822;
  --card-border: #1E293B;
  --text: #F1F5F9;
  --muted: #94A3B8;
  --accent: #F97316;
  --gold: #EAB308;
  --success: #10B981;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', sans-serif;
  padding-bottom: 90px;
}}
.hero {{
  background: linear-gradient(180deg, #16202E 0%, var(--bg) 100%);
  padding: 32px 20px 20px;
  text-align: center;
  border-bottom: 1px solid var(--card-border);
}}
.badge-top {{
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  background: rgba(249, 115, 22, 0.12);
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 10px;
  border: 1px solid rgba(249, 115, 22, 0.3);
}}
h1 {{
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 700;
  color: #FFF;
  margin-bottom: 6px;
}}
.sub {{
  color: var(--muted);
  font-size: 13px;
}}
.nav-cats {{
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 16px 20px;
  position: sticky;
  top: 0;
  background: rgba(9, 13, 18, 0.95);
  backdrop-filter: blur(10px);
  z-index: 100;
  border-bottom: 1px solid var(--card-border);
}}
.cat-btn {{
  background: #111822;
  border: 1px solid var(--card-border);
  color: var(--muted);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  text-decoration: none;
}}
.cat-btn.active, .cat-btn:hover {{
  background: var(--accent);
  color: #FFF;
  border-color: var(--accent);
}}
.section-title {{
  font-size: 18px;
  font-weight: 700;
  color: #FFF;
  margin: 24px 20px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.section-title::before {{
  content: '';
  width: 4px;
  height: 18px;
  background: var(--accent);
  border-radius: 2px;
}}
.menu-grid {{
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 20px;
}}
.menu-item {{
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}}
.item-info {{ flex: 1; }}
.item-name {{ font-size: 15px; font-weight: 700; color: #FFF; margin-bottom: 4px; }}
.item-desc {{ font-size: 12px; color: var(--muted); line-height: 1.4; }}
.item-price {{ font-size: 15px; font-weight: 800; color: var(--gold); white-space: nowrap; }}
.footer-bar {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #0e1520;
  border-top: 1px solid var(--card-border);
  padding: 12px 20px;
  display: flex;
  gap: 10px;
  z-index: 200;
}}
.btn-action {{
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 13px;
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}}
.btn-wa {{ background: #059669; color: #FFF; }}
.btn-review {{ background: #2563EB; color: #FFF; }}
</style>
</head>
<body>

<div class="hero">
  <span class="badge-top">Ativação Inteligente NFC</span>
  <h1>{nome}</h1>
  <p class="sub">{bairro} • Florianópolis</p>
</div>

<div class="nav-cats">
  <a href="#destaques" class="cat-btn active">⭐ Destaques</a>
  <a href="#entradas" class="cat-btn">🍤 Petiscos</a>
  <a href="#principais" class="cat-btn">🍽️ Pratos Principais</a>
  <a href="#bebidas" class="cat-btn">🍹 Drinks &amp; Chopp</a>
</div>

<div id="destaques">
  <div class="section-title">Sugestões da Casa</div>
  <div class="menu-grid">
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Especial da Ilha (2 Pessoas)</div>
        <div class="item-desc">Frutos do mar selecionados, camarões grelhados, iscas de peixe nobre e guarnições artesanais.</div>
      </div>
      <div class="item-price">R$ 149,00</div>
    </div>
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Combo Experiência Premium</div>
        <div class="item-desc">Entrada especial com casquinha de siri + 2 chopes artesanais locais de Florianópolis.</div>
      </div>
      <div class="item-price">R$ 68,00</div>
    </div>
  </div>
</div>

<div id="entradas">
  <div class="section-title">Petiscos &amp; Entradas</div>
  <div class="menu-grid">
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Camarão à Milanesa Crocante</div>
        <div class="item-desc">Acompanha molho tártaro da casa e limão siciliano.</div>
      </div>
      <div class="item-price">R$ 89,00</div>
    </div>
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Iscas de Peixe com Molho Especial</div>
        <div class="item-desc">Porção generosa de peixe fresco empanado na farinha panko.</div>
      </div>
      <div class="item-price">R$ 62,00</div>
    </div>
  </div>
</div>

<div id="bebidas">
  <div class="section-title">Bebidas &amp; Coquetelaria</div>
  <div class="menu-grid">
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Chopp Artesanal IPA / Pilsen (500ml)</div>
        <div class="item-desc">Produzido localmente em Florianópolis, servido estupidamente gelado.</div>
      </div>
      <div class="item-price">R$ 18,00</div>
    </div>
    <div class="menu-item">
      <div class="item-info">
        <div class="item-name">Caipirinha Tropical de Frutas Vermelhas</div>
        <div class="item-desc">Cachaça nobre de alambique ou vodka premium com frutas frescas.</div>
      </div>
      <div class="item-price">R$ 32,00</div>
    </div>
  </div>
</div>

<div class="footer-bar">
  <a href="https://wa.me/{raw_phone}?text=Ol%C3%A1!%20Gostaria%20de%20fazer%20um%20pedido%20pelo%20card%C3%A1pio%20digital." target="_blank" class="btn-action btn-wa">💬 Pedir no WhatsApp</a>
  <a href="https://maps.google.com" target="_blank" class="btn-action btn-review">⭐ Avaliar no Google</a>
</div>

</body>
</html>
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"OK: Cardapio digital gerado com sucesso em {out_file}")
    return out_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gerador de Cardápio Digital Mobile-First AH3")
    parser.add_argument("--nome", type=str, required=True, help="Nome do estabelecimento")
    parser.add_argument("--telefone", type=str, default="48999088162", help="Telefone WhatsApp")
    parser.add_argument("--bairro", type=str, default="Florianópolis", help="Bairro / Região")
    parser.add_argument("--categoria", type=str, default="Gastronomia", help="Categoria")
    parser.add_argument("--output", type=str, default="saida/cardapios", help="Diretório de saída")
    
    args = parser.parse_args()
    gerar_cardapio_html(args.nome, args.categoria, args.telefone, args.bairro, args.output)

#!/usr/bin/env python3
"""
AH3 — Motor de Redirecionamento Dinâmico de Placas NFC (Smart Link Router)
Agente Encarregado: @Designer & @Marketing
Permite alterar remotamente o destino da placa NFC do cliente (Manhã -> Cardápio, Noite -> Google Reviews, etc.)
sem necessidade de regravar o chip físico.
"""

import os
import sys
import json
import argparse
import unicodedata
import re

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def criar_roteador_dinamico(nome, url_google="https://maps.google.com", url_cardapio=None, output_dir="saida/redirecionamento"):
    slug = normalize(nome)
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"router_{slug}.html")

    if not url_cardapio:
        url_cardapio = f"../cardapios/{slug}/index.html"

    # HTML Router dinâmico com auto-redirect inteligente
    router_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nome} — Smart NFC Router</title>
<script>
// Configuração Dinâmica dos Destinos
const CONFIG = {{
  nome: "{nome}",
  modo: "auto", // 'auto' (por horário), 'review', 'cardapio', 'whatsapp'
  destinos: {{
    review: "{url_google}",
    cardapio: "{url_cardapio}",
    whatsapp: "https://wa.me/5548999088162"
  }}
}};

function redirecionar() {{
  const hora = new Date().getHours();
  let destinoFinal = CONFIG.destinos.review;

  if (CONFIG.modo === 'auto') {{
    // Horário de Almoço / Jantar (11h às 15h e 19h às 22h) -> Direciona para Cardápio
    // Fora do pico -> Direciona para Avaliação Google
    if ((hora >= 11 && hora <= 15) || (hora >= 19 && hora <= 22)) {{
      destinoFinal = CONFIG.destinos.cardapio;
    }} else {{
      destinoFinal = CONFIG.destinos.review;
    }}
  }} else if (CONFIG.destinos[CONFIG.modo]) {{
    destinoFinal = CONFIG.destinos[CONFIG.modo];
  }}

  window.location.replace(destinoFinal);
}}

window.onload = redirecionar;
</script>
</head>
<body style="background: #0b0f17; color: #fff; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center;">
  <div>
    <div style="font-size: 32px; margin-bottom: 12px;">⚡</div>
    <h2>Conectando a {nome}...</h2>
    <p style="color: #94a3b8; font-size: 14px;">Redirecionando através da Placa Inteligente AH3</p>
  </div>
</body>
</html>
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(router_html)

    print(f"OK: Roteador dinamico NFC criado com sucesso em {out_file}")
    return out_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gerador de Roteador Dinâmico NFC AH3")
    parser.add_argument("--nome", type=str, required=True, help="Nome do estabelecimento")
    parser.add_argument("--url_google", type=str, default="https://maps.google.com", help="URL da ficha Google")
    parser.add_argument("--url_cardapio", type=str, default=None, help="URL do cardápio")
    parser.add_argument("--output", type=str, default="saida/redirecionamento", help="Diretório de saída")
    
    args = parser.parse_args()
    criar_roteador_dinamico(args.nome, args.url_google, args.url_cardapio, args.output)

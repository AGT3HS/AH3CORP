"""
Gerador de Posts Editoriais de Alto Nível (Estilo Menux.co / SaaS & Gastronomia Premium)
Formatos: 1080x1350 (4:5 Retrato Instagram)
Tipografia: Outfit (Títulos de Alto Impacto) + Inter (Subtextos e Métricas)
Integração: Fotografia Gastronômica Real + Micro-UI (Cards de Métricas, Chat e Badges)
"""

import os
import re
import base64
import argparse
import unicodedata
import pymupdf

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

def escape_xml(text: str) -> str:
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

def quebrar_linhas(texto: str, max_chars: int = 24) -> list:
    palavras = texto.split()
    linhas = []
    linha_atual = []
    tamanho_atual = 0
    
    for palavra in palavras:
        if tamanho_atual + len(palavra) + (1 if linha_atual else 0) <= max_chars:
            linha_atual.append(palavra)
            tamanho_atual += len(palavra) + (1 if len(linha_atual) > 1 else 0)
        else:
            if linha_atual:
                linhas.append(" ".join(linha_atual))
            linha_atual = [palavra]
            tamanho_atual = len(palavra)
    if linha_atual:
        linhas.append(" ".join(linha_atual))
    return linhas

def get_image_base64(image_path: str) -> str:
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

# ==============================================================================
# LAYOUT 1: SPLIT EDITORIAL LIGHT (Foto Real + UI Flutuante + Destaque 2 Cores)
# ==============================================================================
def gerar_post_split_editorial(
    nome: str,
    titulo_linha1: str = "Restaurante cheio de",
    titulo_linha2: str = "boas histórias.",
    subtexto: str = "A AH3 transforma mesas cheias em presença dominante no Google e clientes fiéis.",
    tag_topo: str = "01 / PRESENÇA LOCAL",
    badge_metrica_1: str = "+3.8× Mais Reviews",
    badge_metrica_2: str = "+42% Visitas no Maps",
    chat_pergunta: str = "Qual prato vocês recomendam?",
    chat_resposta: str = "Nosso polvo grelhado com azeite de ervas frescas da Ilha!",
    foto_path: str = "BigBrain/modelos/assets/foto_polvo.jpg",
    cor_destaque: str = "#6366F1", # Roxo elétrico da Menux
    output_dir: str = "saida/posts_instagram"
) -> tuple:
    slug = slugify(nome)
    os.makedirs(output_dir, exist_ok=True)
    foto_b64 = get_image_base64(foto_path)
    
    linhas_sub = quebrar_linhas(subtexto, max_chars=34)
    sub_svg = ""
    for idx, l in enumerate(linhas_sub):
        y_pos = 320 + (idx * 34)
        sub_svg += f'<text x="540" y="{y_pos}" font-family="Inter, sans-serif" font-size="22" font-weight="400" fill="#475569">{escape_xml(l)}</text>\n'

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <filter id="shadowHeavy" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="30" flood-color="#0f172a" flood-opacity="0.12" />
    </filter>
    <filter id="shadowFloat" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="18" flood-color="#0f172a" flood-opacity="0.10" />
    </filter>
    <clipPath id="fotoClip">
      <rect x="70" y="440" width="420" height="580" rx="32" />
    </clipPath>
  </defs>

  <!-- Fundo Limpo Editorial -->
  <rect width="1080" height="1350" fill="#F8FAFC" />

  <!-- Arcos e Curvas Vetoriais Sutis de Fundo -->
  <path d="M 0 350 Q 540 600 1080 300" fill="none" stroke="#E2E8F0" stroke-width="1.5" />
  <path d="M 300 1350 Q 700 900 1080 1100" fill="none" stroke="{cor_destaque}" stroke-opacity="0.2" stroke-width="2" />

  <!-- Topo: Marca e Tag -->
  <g transform="translate(70, 80)">
    <text x="0" y="24" font-family="Outfit, sans-serif" font-size="24" font-weight="800" fill="#0F172A" letter-spacing="1">{escape_xml(nome.upper())}</text>
  </g>
  <g transform="translate(1010, 80)">
    <text x="0" y="24" text-anchor="end" font-family="Inter, sans-serif" font-size="15" font-weight="600" fill="#64748B" letter-spacing="2">{escape_xml(tag_topo)}</text>
  </g>
  <line x1="70" y1="125" x2="1010" y2="125" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Título Principal em 2 Cores -->
  <g transform="translate(540, 200)">
    <text x="0" y="0" font-family="Outfit, sans-serif" font-size="52" font-weight="900" fill="#0F172A" letter-spacing="-1">{escape_xml(titulo_linha1)}</text>
    <text x="0" y="62" font-family="Outfit, sans-serif" font-size="52" font-weight="900" fill="{cor_destaque}" letter-spacing="-1">{escape_xml(titulo_linha2)}</text>
  </g>

  <!-- Subtexto -->
  {sub_svg}

  <!-- Foto Real Gastronômica à Esquerda com Moldura e Sombra -->
  <g filter="url(#shadowHeavy)">
    <rect x="70" y="440" width="420" height="580" rx="32" fill="#E2E8F0" />
    <image href="{foto_b64}" x="70" y="440" width="420" height="580" preserveAspectRatio="xMidYMid slice" clip-path="url(#fotoClip)" />
    <rect x="70" y="440" width="420" height="580" rx="32" fill="none" stroke="#FFFFFF" stroke-width="4" />
  </g>

  <!-- Elementos de UI Flutuantes à Direita -->
  
  <!-- Badges de Métricas no Topo da Direita -->
  <g transform="translate(540, 440)" filter="url(#shadowFloat)">
    <rect x="0" y="0" width="220" height="60" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
    <text x="110" y="38" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="800" fill="{cor_destaque}">{escape_xml(badge_metrica_1)}</text>
  </g>
  <g transform="translate(780, 440)" filter="url(#shadowFloat)">
    <rect x="0" y="0" width="230" height="60" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
    <text x="115" y="38" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="800" fill="#10B981">{escape_xml(badge_metrica_2)}</text>
  </g>

  <!-- Balão de Chat 1 (Pergunta do Cliente) -->
  <g transform="translate(540, 530)" filter="url(#shadowFloat)">
    <rect x="0" y="0" width="470" height="85" rx="20" fill="{cor_destaque}" />
    <text x="24" y="32" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#E0E7FF">CLIENTE NA MESA</text>
    <text x="24" y="60" font-family="Inter, sans-serif" font-size="18" font-weight="500" fill="#FFFFFF">{escape_xml(chat_pergunta)}</text>
  </g>

  <!-- Balão de Chat 2 (Resposta do Estabelecimento / IA) -->
  <g transform="translate(540, 640)" filter="url(#shadowFloat)">
    <rect x="0" y="0" width="470" height="110" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
    <text x="24" y="32" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="{cor_destaque}">MAESTRO AH3</text>
    <text x="24" y="60" font-family="Inter, sans-serif" font-size="17" font-weight="500" fill="#1E293B">“{escape_xml(chat_resposta)}”</text>
    <text x="24" y="88" font-family="Inter, sans-serif" font-size="13" font-weight="600" fill="#10B981">★ 4.9 no Google Maps • Sugestão do Chef</text>
  </g>

  <!-- Mini Card de Ação Rápida -->
  <g transform="translate(540, 780)" filter="url(#shadowFloat)">
    <rect x="0" y="0" width="470" height="90" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" />
    <circle cx="50" cy="45" r="24" fill="{cor_destaque}" opacity="0.15" />
    <text x="50" y="52" text-anchor="middle" font-family="Outfit, sans-serif" font-size="20" font-weight="800" fill="{cor_destaque}">➔</text>
    <text x="90" y="38" font-family="Outfit, sans-serif" font-size="20" font-weight="800" fill="#0F172A">Do pedido à avaliação</text>
    <text x="90" y="64" font-family="Inter, sans-serif" font-size="15" font-weight="500" fill="#64748B">Placa NFC de aproximação instantânea no balcão</text>
  </g>

  <!-- Botão Pill no Rodapé do Bloco -->
  <g transform="translate(540, 930)">
    <rect x="0" y="0" width="470" height="65" rx="32" fill="#0F172A" />
    <text x="235" y="40" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">EXPERIMENTE NA SUA MESA ➔</text>
  </g>

  <!-- Rodapé Global -->
  <line x1="70" y1="1240" x2="1010" y2="1240" stroke="#E2E8F0" stroke-width="1.5" />
  <text x="70" y="1285" font-family="Inter, sans-serif" font-size="16" font-weight="600" fill="#64748B">AH3 • Presença Local &amp; Hospitalidade</text>
  <text x="1010" y="1285" text-anchor="end" font-family="Inter, sans-serif" font-size="16" font-weight="600" fill="{cor_destaque}">Florianópolis, SC</text>
</svg>
"""
    svg_file = os.path.join(output_dir, f"post_menux_split_{slug}.svg")
    png_file = os.path.join(output_dir, f"post_menux_split_{slug}.png")
    
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    doc = pymupdf.open("pdf", pymupdf.open(stream=svg_content.encode("utf-8"), filetype="svg").convert_to_pdf())
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_file)
    
    print(f"OK: Post Split Editorial PNG gerado em {png_file}")
    return svg_file, png_file


# ==============================================================================
# LAYOUT 2: DARK MOODY (Ambiance Restaurante + Glassmorphism + Métricas)
# ==============================================================================
def gerar_post_dark_moody(
    nome: str,
    titulo_linha1: str = "Boa experiência também",
    titulo_linha2: str = "dá lucro.",
    subtexto: str = "A AH3 ajuda seu restaurante a atrair mais clientes locais com presença estratégica no Google Maps e placas inteligentes na mesa.",
    foto_fundo_path: str = "BigBrain/modelos/assets/foto_restaurante_moody.jpg",
    metrica_1: str = "+27% no Ticket Médio",
    metrica_2: str = "+40% de Avaliações 5★",
    metrica_3: str = "★ 4.9 Nota Média no Google",
    cor_destaque: str = "#818CF8", # Roxo brilhante para Dark Mode
    output_dir: str = "saida/posts_instagram"
) -> tuple:
    slug = slugify(nome)
    os.makedirs(output_dir, exist_ok=True)
    foto_b64 = get_image_base64(foto_fundo_path)
    
    linhas_sub = quebrar_linhas(subtexto, max_chars=32)
    sub_svg = ""
    for idx, l in enumerate(linhas_sub):
        y_pos = 580 + (idx * 36)
        sub_svg += f'<text x="80" y="{y_pos}" font-family="Inter, sans-serif" font-size="22" font-weight="400" fill="#CBD5E1">{escape_xml(l)}</text>\n'

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <linearGradient id="darkOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19" stop-opacity="0.92" />
      <stop offset="50%" stop-color="#0B0F19" stop-opacity="0.75" />
      <stop offset="100%" stop-color="#0B0F19" stop-opacity="0.95" />
    </linearGradient>
    <filter id="glassBlur">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.6" />
    </filter>
  </defs>

  <!-- Imagem Fotográfica de Fundo -->
  <image href="{foto_b64}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" />
  
  <!-- Overlay Gradiente Escuro -->
  <rect width="1080" height="1350" fill="url(#darkOverlay)" />

  <!-- Luzes de Destaque -->
  <circle cx="200" cy="300" r="250" fill="{cor_destaque}" opacity="0.15" filter="blur(60px)" />
  <circle cx="900" cy="800" r="300" fill="#38BDF8" opacity="0.10" filter="blur(70px)" />

  <!-- Topo: Marca e Tag -->
  <g transform="translate(80, 80)">
    <text x="0" y="24" font-family="Outfit, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">{escape_xml(nome.upper())}</text>
  </g>
  <g transform="translate(1000, 80)">
    <rect x="-170" y="-8" width="170" height="38" rx="19" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.15" />
    <text x="-85" y="16" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="{cor_destaque}">GESTÃO LOCAL</text>
  </g>

  <!-- Título Principal em 2 Cores -->
  <g transform="translate(80, 420)">
    <text x="0" y="0" font-family="Outfit, sans-serif" font-size="58" font-weight="900" fill="#FFFFFF" letter-spacing="-1">{escape_xml(titulo_linha1)}</text>
    <text x="0" y="70" font-family="Outfit, sans-serif" font-size="58" font-weight="900" fill="{cor_destaque}" letter-spacing="-1">{escape_xml(titulo_linha2)}</text>
  </g>

  <!-- Subtexto -->
  {sub_svg}

  <!-- Botão Pill de Destaque à Esquerda -->
  <g transform="translate(80, 740)">
    <rect x="0" y="0" width="360" height="56" rx="28" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.2" />
    <text x="180" y="35" text-anchor="middle" font-family="Outfit, sans-serif" font-size="17" font-weight="700" fill="#FFFFFF">Resultados que fazem sentido ➔</text>
  </g>

  <!-- Badges Flutuantes de Vidro (Glassmorphism) à Direita -->
  <g transform="translate(620, 400)" filter="url(#glassBlur)">
    <rect x="0" y="0" width="380" height="90" rx="24" fill="#1E293B" fill-opacity="0.6" stroke="#FFFFFF" stroke-opacity="0.2" stroke-width="1.5" />
    <circle cx="50" cy="45" r="22" fill="{cor_destaque}" fill-opacity="0.2" />
    <text x="50" y="52" text-anchor="middle" font-family="Outfit, sans-serif" font-size="20" font-weight="800" fill="{cor_destaque}">📈</text>
    <text x="90" y="52" font-family="Outfit, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF">{escape_xml(metrica_1)}</text>
  </g>

  <g transform="translate(620, 520)" filter="url(#glassBlur)">
    <rect x="0" y="0" width="380" height="90" rx="24" fill="#1E293B" fill-opacity="0.6" stroke="#FFFFFF" stroke-opacity="0.2" stroke-width="1.5" />
    <circle cx="50" cy="45" r="22" fill="#10B981" fill-opacity="0.2" />
    <text x="50" y="52" text-anchor="middle" font-family="Outfit, sans-serif" font-size="20" font-weight="800" fill="#10B981">⭐</text>
    <text x="90" y="52" font-family="Outfit, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF">{escape_xml(metrica_2)}</text>
  </g>

  <g transform="translate(620, 640)" filter="url(#glassBlur)">
    <rect x="0" y="0" width="380" height="90" rx="24" fill="#1E293B" fill-opacity="0.6" stroke="#FFFFFF" stroke-opacity="0.2" stroke-width="1.5" />
    <circle cx="50" cy="45" r="22" fill="#F59E0B" fill-opacity="0.2" />
    <text x="50" y="52" text-anchor="middle" font-family="Outfit, sans-serif" font-size="20" font-weight="800" fill="#F59E0B">🎯</text>
    <text x="90" y="52" font-family="Outfit, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF">{escape_xml(metrica_3)}</text>
  </g>

  <!-- Rodapé Global -->
  <line x1="80" y1="1240" x2="1000" y2="1240" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1" />
  <text x="80" y="1285" font-family="Inter, sans-serif" font-size="16" font-weight="500" fill="#94A3B8">AH3 Marketing &amp; Presença Local</text>
  <text x="1000" y="1285" text-anchor="end" font-family="Inter, sans-serif" font-size="16" font-weight="600" fill="{cor_destaque}">Florianópolis, SC</text>
</svg>
"""
    svg_file = os.path.join(output_dir, f"post_menux_dark_{slug}.svg")
    png_file = os.path.join(output_dir, f"post_menux_dark_{slug}.png")
    
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    doc = pymupdf.open("pdf", pymupdf.open(stream=svg_content.encode("utf-8"), filetype="svg").convert_to_pdf())
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_file)
    
    print(f"OK: Post Dark Moody PNG gerado em {png_file}")
    return svg_file, png_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Posts Estilo Editorial Menux.co")
    parser.add_argument("--estilo", type=str, choices=["split", "dark"], default="split", help="Estilo do post")
    parser.add_argument("--nome", type=str, default="Restaurante O Timoneiro", help="Nome do estabelecimento")
    parser.add_argument("--t1", type=str, default="Restaurante cheio de", help="Título Linha 1")
    parser.add_argument("--t2", type=str, default="boas histórias.", help="Título Linha 2 (destaque)")
    parser.add_argument("--sub", type=str, default="A AH3 transforma mesas cheias em presença dominante no Google e clientes fiéis.", help="Subtexto")
    parser.add_argument("--foto", type=str, default="BigBrain/modelos/assets/foto_polvo.jpg", help="Caminho da foto")
    parser.add_argument("--output", type=str, default="saida/posts_instagram", help="Diretório de saída")
    
    args = parser.parse_args()
    
    if args.estilo == "split":
        gerar_post_split_editorial(
            nome=args.nome,
            titulo_linha1=args.t1,
            titulo_linha2=args.t2,
            subtexto=args.sub,
            foto_path=args.foto,
            output_dir=args.output
        )
    elif args.estilo == "dark":
        gerar_post_dark_moody(
            nome=args.nome,
            titulo_linha1=args.t1,
            titulo_linha2=args.t2,
            subtexto=args.sub,
            foto_fundo_path="BigBrain/modelos/assets/foto_restaurante_moody.jpg",
            output_dir=args.output
        )

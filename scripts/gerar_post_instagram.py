"""
Gerador de Posts e Carrosséis para Instagram AH3 (Formato de Imagem PNG 300 DPI)
Formatos: 1080x1350 (4:5 Retrato) e 1080x1080 (1:1 Quadrado)
Tipografia: Outfit (Títulos) + Inter (Corpo/Subtextos)
Compatível com PyMuPDF para renderização de altíssima nitidez.
"""

import os
import re
import unicodedata
import argparse
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

def quebrar_linhas(texto: str, max_chars: int = 32) -> list:
    """Quebra texto em linhas respeitando palavras inteiras."""
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

def gerar_post_avaliacao(
    nome: str,
    texto_avaliacao: str,
    autor: str,
    nota: int = 5,
    bairro: str = "Florianópolis, SC",
    cor_primaria: str = "#1E3A8A", # Azul profundo / Turquesa
    cor_secundaria: str = "#0F172A", # Fundo nobre
    cor_destaque: str = "#F59E0B", # Dourado estrelas
    cor_texto: str = "#F8FAFC",
    logo_path: str = None,
    output_dir: str = "saida/posts_instagram"
) -> tuple:
    """Gera um post único de avaliação 5 estrelas do Google Maps em 1080x1350 px."""
    slug = slugify(nome)
    os.makedirs(output_dir, exist_ok=True)
    
    # 5 Estrelas SVG Path
    estrelas_svg = ""
    for i in range(nota):
        cx = 360 + (i * 72)
        estrelas_svg += f"""
        <g transform="translate({cx}, 730)">
            <path d="M 0 -22 L 6 -6 L 23 -6 L 9 4 L 14 20 L 0 10 L -14 20 L -9 4 L -23 -6 L -6 -6 Z" fill="{cor_destaque}" />
        </g>
        """
        
    linhas_review = quebrar_linhas(f'"{texto_avaliacao}"', max_chars=34)
    linhas_svg = ""
    y_start = 540 - (len(linhas_review) * 22)
    for idx, l in enumerate(linhas_review):
        y_pos = y_start + (idx * 48)
        linhas_svg += f'<text x="540" y="{y_pos}" text-anchor="middle" font-family="Inter, sans-serif" font-size="34" font-weight="500" font-style="italic" fill="{cor_texto}" opacity="0.95">{escape_xml(l)}</text>\n'

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cor_secundaria}" />
      <stop offset="40%" stop-color="#111827" />
      <stop offset="100%" stop-color="{cor_primaria}" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.02" />
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.5" />
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="1080" height="1350" fill="url(#bgGrad)" />

  <!-- Círculos de luz decorativos -->
  <circle cx="200" cy="200" r="300" fill="{cor_primaria}" opacity="0.25" filter="blur(60px)" />
  <circle cx="900" cy="1100" r="350" fill="{cor_destaque}" opacity="0.15" filter="blur(80px)" />

  <!-- Topo: Marca e Badge -->
  <g transform="translate(540, 140)">
    <rect x="-180" y="-30" width="360" height="60" rx="30" fill="{cor_primaria}" opacity="0.4" stroke="{cor_destaque}" stroke-width="1.5" />
    <text x="0" y="8" text-anchor="middle" font-family="Outfit, sans-serif" font-size="20" font-weight="700" fill="{cor_destaque}" letter-spacing="3">AVALIAÇÃO VERIFICADA</text>
  </g>

  <!-- Nome do Estabelecimento -->
  <text x="540" y="270" text-anchor="middle" font-family="Outfit, sans-serif" font-size="44" font-weight="800" fill="{cor_texto}" letter-spacing="1">{escape_xml(nome.upper())}</text>
  <text x="540" y="315" text-anchor="middle" font-family="Inter, sans-serif" font-size="20" font-weight="500" fill="{cor_destaque}" letter-spacing="2">{escape_xml(bairro.upper())}</text>

  <!-- Card Central de Depoimento -->
  <g filter="url(#cardShadow)">
    <rect x="80" y="380" width="920" height="680" rx="40" fill="url(#cardGrad)" stroke="#ffffff" stroke-opacity="0.15" stroke-width="1.5" />
  </g>

  <!-- Aspas Gigantes no Topo do Card -->
  <text x="540" y="470" text-anchor="middle" font-family="Outfit, sans-serif" font-size="90" font-weight="800" fill="{cor_destaque}" opacity="0.5">“</text>

  <!-- Texto da Avaliação -->
  {linhas_svg}

  <!-- Estrelas Douradas -->
  {estrelas_svg}

  <!-- Autor do Review -->
  <text x="540" y="830" text-anchor="middle" font-family="Outfit, sans-serif" font-size="28" font-weight="700" fill="{cor_texto}">{escape_xml(autor)}</text>
  
  <!-- Badge Google Maps -->
  <g transform="translate(540, 880)">
    <rect x="-130" y="-18" width="260" height="36" rx="18" fill="#1e293b" opacity="0.8" stroke="#334155" stroke-width="1" />
    <text x="0" y="6" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#94a3b8">Google Maps • 5.0 ⭐</text>
  </g>

  <!-- Rodapé / Convite -->
  <g transform="translate(540, 1180)">
    <rect x="-240" y="-35" width="480" height="70" rx="35" fill="{cor_destaque}" />
    <text x="0" y="8" text-anchor="middle" font-family="Outfit, sans-serif" font-size="22" font-weight="800" fill="#0f172a" letter-spacing="1">VENHA VIVER ESSA EXPERIÊNCIA</text>
  </g>
  <text x="540" y="1275" text-anchor="middle" font-family="Inter, sans-serif" font-size="16" font-weight="500" fill="#94a3b8">Link na bio para cardápio e reservas • Florianópolis</text>
</svg>
"""
    svg_file = os.path.join(output_dir, f"post_review_{slug}.svg")
    png_file = os.path.join(output_dir, f"post_review_{slug}.png")
    
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    doc = pymupdf.open("pdf", pymupdf.open(stream=svg_content.encode("utf-8"), filetype="svg").convert_to_pdf())
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    pix.save(png_file)
    
    print(f"OK: Post Review SVG gerado em {svg_file}")
    print(f"OK: Post Review PNG (300 DPI) renderizado em {png_file}")
    return svg_file, png_file


def gerar_carrossel_instagram(
    nome: str,
    tema: str,
    slides: list,
    bairro: str = "Florianópolis, SC",
    cor_primaria: str = "#0D3B66",
    cor_secundaria: str = "#0A1128",
    cor_destaque: str = "#EE964B",
    cor_texto: str = "#F8FAFC",
    output_dir: str = "saida/posts_instagram"
) -> list:
    """
    Gera um carrossel completo de N slides em 1080x1350 px (4:5 Retrato).
    Estrutura de cada slide no array `slides`:
    [
      {"tipo": "capa", "tag": "GUIA GASTRONÔMICO", "titulo": "3 Segredos do Polvo Grelhado Perfeito", "sub": "Como transformamos uma receita tradicional no prato mais pedido da Ilha."},
      {"tipo": "conteudo", "numero": "01", "titulo": "Ingredientes Frescos do Dia", "texto": "Nossos pescados são adquiridos diariamente de produtores artesanais locais de Florianópolis."},
      {"tipo": "conteudo", "numero": "02", "titulo": "Ponto da Brasa Controlado", "texto": "A selagem em brasa de eucalipto garante crocância externa e maciez extrema por dentro."},
      {"tipo": "cta", "tag": "EXPERIMENTE HOJE", "titulo": "Reserve Sua Mesa no Salão", "sub": "Atendimento de terça a domingo no almoço e jantar. Toque no link da bio para reservar."}
    ]
    """
    slug = slugify(nome)
    carrossel_dir = os.path.join(output_dir, f"carrossel_{slug}")
    os.makedirs(carrossel_dir, exist_ok=True)
    total_slides = len(slides)
    arquivos_gerados = []

    for idx, slide in enumerate(slides):
        slide_num = idx + 1
        tipo_slide = slide.get("tipo", "conteudo")
        tag = slide.get("tag", "AH3 HOSPITALIDADE")
        titulo = slide.get("titulo", "")
        texto = slide.get("texto", slide.get("sub", ""))
        
        # Indicador de slide no topo [ 1 / 4 ]
        indicador_slide = f"{slide_num:02d} / {total_slides:02d}"
        
        if tipo_slide == "capa":
            linhas_titulo = quebrar_linhas(titulo, max_chars=22)
            titulo_svg = ""
            for t_idx, tl in enumerate(linhas_titulo):
                y_pos = 580 + (t_idx * 75)
                titulo_svg += f'<text x="100" y="{y_pos}" font-family="Outfit, sans-serif" font-size="64" font-weight="900" fill="{cor_texto}" letter-spacing="-1">{escape_xml(tl)}</text>\n'
                
            linhas_sub = quebrar_linhas(texto, max_chars=38)
            sub_svg = ""
            y_sub_start = 580 + (len(linhas_titulo) * 75) + 30
            for s_idx, sl in enumerate(linhas_sub):
                y_pos = y_sub_start + (s_idx * 42)
                sub_svg += f'<text x="100" y="{y_pos}" font-family="Inter, sans-serif" font-size="28" font-weight="400" fill="#94a3b8">{escape_xml(sl)}</text>\n'

            corpo_slide = f"""
            <!-- Tag do Topo -->
            <rect x="100" y="420" width="300" height="50" rx="25" fill="{cor_destaque}" />
            <text x="250" y="453" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="800" fill="#0f172a" letter-spacing="2">{escape_xml(tag)}</text>
            
            <!-- Título Principal -->
            {titulo_svg}
            
            <!-- Subtítulo / Gancho -->
            {sub_svg}
            
            <!-- Indicador de Arraste -->
            <g transform="translate(980, 1200)">
              <circle cx="-50" cy="0" r="35" fill="{cor_primaria}" stroke="{cor_destaque}" stroke-width="2" />
              <text x="-50" y="8" text-anchor="middle" font-family="Outfit, sans-serif" font-size="24" font-weight="800" fill="{cor_destaque}">➔</text>
              <text x="-110" y="7" text-anchor="end" font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="{cor_destaque}">Deslize para ver</text>
            </g>
            """

        elif tipo_slide == "cta":
            linhas_titulo = quebrar_linhas(titulo, max_chars=24)
            titulo_svg = ""
            for t_idx, tl in enumerate(linhas_titulo):
                y_pos = 520 + (t_idx * 70)
                titulo_svg += f'<text x="540" y="{y_pos}" text-anchor="middle" font-family="Outfit, sans-serif" font-size="58" font-weight="900" fill="{cor_texto}">{escape_xml(tl)}</text>\n'

            linhas_sub = quebrar_linhas(texto, max_chars=36)
            sub_svg = ""
            y_sub_start = 520 + (len(linhas_titulo) * 70) + 20
            for s_idx, sl in enumerate(linhas_sub):
                y_pos = y_sub_start + (s_idx * 44)
                sub_svg += f'<text x="540" y="{y_pos}" text-anchor="middle" font-family="Inter, sans-serif" font-size="26" font-weight="400" fill="#cbd5e1">{escape_xml(sl)}</text>\n'

            corpo_slide = f"""
            <g transform="translate(540, 380)">
              <rect x="-160" y="-25" width="320" height="50" rx="25" fill="{cor_primaria}" stroke="{cor_destaque}" stroke-width="1.5" />
              <text x="0" y="8" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="800" fill="{cor_destaque}" letter-spacing="2">{escape_xml(tag)}</text>
            </g>

            {titulo_svg}
            {sub_svg}

            <!-- Botão de Ação CTA -->
            <g transform="translate(540, 940)">
              <rect x="-260" y="-40" width="520" height="80" rx="40" fill="{cor_destaque}" />
              <text x="0" y="10" text-anchor="middle" font-family="Outfit, sans-serif" font-size="24" font-weight="900" fill="#0f172a" letter-spacing="1">RESERVAR PELO WHATSAPP</text>
            </g>

            <text x="540" y="1080" text-anchor="middle" font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="#94a3b8">Link direto disponível na bio do nosso perfil</text>
            <text x="540" y="1120" text-anchor="middle" font-family="Inter, sans-serif" font-size="18" font-weight="500" fill="{cor_destaque}">📍 {escape_xml(bairro)}</text>
            """

        else: # Conteúdo / Dicas / Motivos
            numero_slide = slide.get("numero", f"{slide_num:02d}")
            linhas_titulo = quebrar_linhas(titulo, max_chars=24)
            titulo_svg = ""
            for t_idx, tl in enumerate(linhas_titulo):
                y_pos = 500 + (t_idx * 65)
                titulo_svg += f'<text x="100" y="{y_pos}" font-family="Outfit, sans-serif" font-size="52" font-weight="800" fill="{cor_texto}">{escape_xml(tl)}</text>\n'

            linhas_texto = quebrar_linhas(texto, max_chars=34)
            texto_svg = ""
            y_txt_start = 500 + (len(linhas_titulo) * 65) + 35
            for tx_idx, txl in enumerate(linhas_texto):
                y_pos = y_txt_start + (tx_idx * 48)
                texto_svg += f'<text x="100" y="{y_pos}" font-family="Inter, sans-serif" font-size="30" font-weight="400" fill="#e2e8f0">{escape_xml(txl)}</text>\n'

            corpo_slide = f"""
            <!-- Número Destacado -->
            <text x="100" y="420" font-family="Outfit, sans-serif" font-size="110" font-weight="900" fill="{cor_destaque}" opacity="0.9">{escape_xml(numero_slide)}</text>
            <line x1="260" y1="380" x2="980" y2="380" stroke="#ffffff" stroke-opacity="0.1" stroke-width="2" />

            {titulo_svg}
            {texto_svg}

            <!-- Indicador Próximo -->
            <g transform="translate(980, 1200)">
              <text x="-50" y="7" text-anchor="end" font-family="Inter, sans-serif" font-size="18" font-weight="600" fill="{cor_destaque}">Próximo ➔</text>
            </g>
            """

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
    <linearGradient id="bgGrad{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{cor_secundaria}" />
      <stop offset="60%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="{cor_primaria}" />
    </linearGradient>
  </defs>

  <!-- Fundo -->
  <rect width="1080" height="1350" fill="url(#bgGrad{idx})" />
  <circle cx="950" cy="150" r="300" fill="{cor_primaria}" opacity="0.3" filter="blur(70px)" />
  <circle cx="100" cy="1200" r="280" fill="{cor_destaque}" opacity="0.12" filter="blur(70px)" />

  <!-- Cabeçalho Global: Nome e Indicador de Slide -->
  <g transform="translate(100, 120)">
    <text x="0" y="30" font-family="Outfit, sans-serif" font-size="28" font-weight="800" fill="{cor_texto}" letter-spacing="1">{escape_xml(nome.upper())}</text>
    <text x="0" y="60" font-family="Inter, sans-serif" font-size="16" font-weight="500" fill="{cor_destaque}">{escape_xml(bairro.upper())}</text>
  </g>

  <!-- Badge de Numeração de Slide [ 01 / 04 ] -->
  <g transform="translate(980, 140)">
    <rect x="-110" y="-22" width="110" height="44" rx="22" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.15" />
    <text x="-55" y="8" text-anchor="middle" font-family="Outfit, sans-serif" font-size="18" font-weight="700" fill="{cor_texto}">{indicador_slide}</text>
  </g>

  <!-- Linha Divisória de Topo -->
  <line x1="100" y1="210" x2="980" y2="210" stroke="#ffffff" stroke-opacity="0.1" stroke-width="1.5" />

  <!-- Conteúdo Específico do Slide -->
  {corpo_slide}

  <!-- Rodapé Global -->
  <line x1="100" y1="1260" x2="980" y2="1260" stroke="#ffffff" stroke-opacity="0.1" stroke-width="1.5" />
  <text x="100" y="1295" font-family="Inter, sans-serif" font-size="14" font-weight="500" fill="#64748b">AH3 Marketing &amp; Presença Local</text>
  <text x="980" y="1295" text-anchor="end" font-family="Inter, sans-serif" font-size="14" font-weight="500" fill="#64748b">Florianópolis • SC</text>
</svg>
"""
        svg_file = os.path.join(carrossel_dir, f"slide_{slide_num:02d}.svg")
        png_file = os.path.join(carrossel_dir, f"slide_{slide_num:02d}.png")
        
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        doc = pymupdf.open("pdf", pymupdf.open(stream=svg_content.encode("utf-8"), filetype="svg").convert_to_pdf())
        page = doc[0]
        pix = page.get_pixmap(dpi=300)
        pix.save(png_file)
        
        arquivos_gerados.append(png_file)
        print(f"OK: Slide {slide_num} renderizado (300 DPI) em {png_file}")

    return arquivos_gerados

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Posts e Carrosséis Instagram AH3 (PNG 300 DPI)")
    parser.add_argument("--tipo", type=str, choices=["avaliacao", "carrossel"], default="avaliacao", help="Tipo de post")
    parser.add_argument("--nome", type=str, default="Jurerê Beach Village", help="Nome do estabelecimento")
    parser.add_argument("--bairro", type=str, default="Jurerê, Florianópolis", help="Bairro / Cidade")
    parser.add_argument("--texto", type=str, default="Experiência maravilhosa de frente para o mar! Café da manhã impecável.", help="Texto da avaliação ou gancho")
    parser.add_argument("--autor", type=str, default="Mariana Silva", help="Autor da avaliação")
    parser.add_argument("--nota", type=int, default=5, help="Nota da avaliação (1-5)")
    parser.add_argument("--tema", type=str, default="3 Motivos para se hospedar em Jurerê", help="Tema do carrossel")
    parser.add_argument("--cor_primaria", type=str, default="#0D3B66", help="Cor primária HEX")
    parser.add_argument("--cor_secundaria", type=str, default="#0A1128", help="Cor fundo HEX")
    parser.add_argument("--cor_destaque", type=str, default="#EE964B", help="Cor destaque HEX")
    parser.add_argument("--output", type=str, default="saida/posts_instagram", help="Diretório de saída")
    
    args = parser.parse_args()
    
    if args.tipo == "avaliacao":
        gerar_post_avaliacao(
            nome=args.nome,
            texto_avaliacao=args.texto,
            autor=args.autor,
            nota=args.nota,
            bairro=args.bairro,
            cor_primaria=args.cor_primaria,
            cor_secundaria=args.cor_secundaria,
            cor_destaque=args.cor_destaque,
            output_dir=args.output
        )
    elif args.tipo == "carrossel":
        slides_exemplo = [
            {
                "tipo": "capa",
                "tag": "HOSPEDAGEM EXCLUSIVA",
                "titulo": args.tema,
                "sub": f"Descubra por que o {args.nome} é a escolha perfeita para a sua próxima estadia na Ilha."
            },
            {
                "tipo": "conteudo",
                "numero": "01",
                "titulo": "Localização Beira-Mar Pé na Areia",
                "texto": "Acesso direto à praia mais charmosa de Floripa, com serviço de praia exclusivo e piscinas aquecidas."
            },
            {
                "tipo": "conteudo",
                "numero": "02",
                "titulo": "Gastronomia Internacional & Regional",
                "texto": "Restaurante próprio com café da manhã artesanal completo e cardápio refinado de frutos do mar frescos."
            },
            {
                "tipo": "cta",
                "tag": "RESERVE AGORA",
                "titulo": "Garanta a Sua Experiência Inesquecível",
                "sub": "Condições especiais para reservas diretas. Toque no botão e fale com nossa recepção pelo WhatsApp."
            }
        ]
        gerar_carrossel_instagram(
            nome=args.nome,
            tema=args.tema,
            slides=slides_exemplo,
            bairro=args.bairro,
            cor_primaria=args.cor_primaria,
            cor_secundaria=args.cor_secundaria,
            cor_destaque=args.cor_destaque,
            output_dir=args.output
        )

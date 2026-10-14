import json, os, re, ssl, urllib.request
from urllib.parse import urljoin, urlparse
from PIL import Image
import io

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

with open(r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_hotelaria_florianopolis.json', 'r', encoding='utf-8') as f:
    hotels = json.load(f)

top40 = hotels[:40]
base_assets_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual\logos_completos'
os.makedirs(base_assets_dir, exist_ok=True)

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text)
    return text.strip('_').lower()

consolidated_table = []

for h in top40:
    rank = h['ranking']
    nome = h['nome']
    site = h.get('site', '')
    quartos = h.get('quartos', 0)
    
    hotel_slug = f"{rank:02d}_{slugify(nome)[:30]}"
    hotel_dir = os.path.join(base_assets_dir, hotel_slug)
    os.makedirs(hotel_dir, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f"[{rank:02d}/40] Analisando: {nome} | {site}")
    print(f"=======================================================")
    
    if not site or not site.startswith('http'):
        print(f"-> Sem site cadastrado.")
        consolidated_table.append({
            'ranking': rank,
            'hotel': nome,
            'arquivo': '-',
            'tipo': 'Site Ausente',
            'formato': '-',
            'dimensoes': '-',
            'qualidade': 'Sem Site',
            'origem': '-'
        })
        continue

    pages_to_crawl = [site]
    # Páginas extras a checar se existirem
    for sub in ['/sobre', '/quem-somos', '/imprensa', '/hotel', '/pt/']:
        pages_to_crawl.append(urljoin(site, sub))

    found_assets = {} # url -> dict of info

    for page_url in pages_to_crawl[:2]:
        try:
            req = urllib.request.Request(page_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                
                # 1. SVGs inline
                svgs = re.findall(r'<svg[^>]*>.*?</svg>', html, re.DOTALL | re.I)
                for idx_svg, s in enumerate(svgs):
                    s_lower = s.lower()
                    if any(k in s_lower for k in ['logo', 'brand', 'marca', 'header', slugify(nome).split('_')[0]]) and len(s) > 300:
                        # Salvar svg inline
                        svg_name = f"{slugify(nome)}_logo_inline_{idx_svg+1}.svg"
                        svg_path = os.path.join(hotel_dir, svg_name)
                        with open(svg_path, 'w', encoding='utf-8') as sf:
                            sf.write(s)
                        found_assets[f"inline_svg_{idx_svg}"] = {
                            'file': svg_name,
                            'tipo': 'Logotipo Completo Oficial (SVG Inline)',
                            'formato': 'SVG',
                            'dimensoes': 'Escalável (Vetor Nativo)',
                            'tamanho': f"{len(s)/1024:.1f} KB",
                            'origem': page_url,
                            'score': 100
                        }

                # 2. Link tags (Favicon, Apple touch icon, manifest)
                links = re.findall(r'<link[^>]+rel=[\"\']([^\"\']+)[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', html, re.I)
                for rel, href in links:
                    rel_l = rel.lower()
                    if any(k in rel_l for k in ['icon', 'apple-touch-icon', 'shortcut icon']):
                        full_u = urljoin(page_url, href)
                        tipo = 'Ícone Apple Touch' if 'apple' in rel_l else 'Favicon / Ícone de Navegador'
                        score = 40 if 'apple' in rel_l else 20
                        if full_u not in found_assets:
                            found_assets[full_u] = {'tipo': tipo, 'score': score, 'origem': full_u}

                # 3. Meta og:image
                og_imgs = re.findall(r'<meta[^>]+property=[\"\']og:image[\"\'][^>]+content=[\"\']([^\"\']+)[\"\']', html, re.I)
                for og in og_imgs:
                    full_u = urljoin(page_url, og)
                    if full_u not in found_assets:
                        found_assets[full_u] = {'tipo': 'Imagem de Identidade / Social (OG:Image)', 'score': 50, 'origem': full_u}

                # 4. Imagens com tags <img> e <picture> <source srcset>
                img_srcs = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', html, re.I)
                srcsets = re.findall(r'srcset=[\"\']([^\"\']+)[\"\']', html, re.I)
                for sc in srcsets:
                    for part in sc.split(','):
                        u = part.strip().split(' ')[0]
                        if u: img_srcs.append(u)

                norm_first = slugify(nome).split('_')[0]
                for img in img_srcs:
                    img_l = img.lower()
                    if any(bad in img_l for bad in ['tripadvisor', 'booking', 'visa', 'mastercard', 'google', 'facebook', 'instagram', 'youtube', 'whatsapp', 'lang-', 'bandeira']):
                        continue
                    
                    score = 0
                    tipo = 'Ativo de Marca'
                    if 'logo' in img_l or 'brand' in img_l or 'marca' in img_l:
                        score = 90
                        tipo = 'Logotipo Completo Oficial'
                    elif norm_first in img_l:
                        score = 80
                        tipo = 'Logotipo / Marca do Empreendimento'
                    elif img_l.endswith('.svg'):
                        score = 70
                        tipo = 'Ativo Vetorial (SVG)'
                    elif any(img_l.endswith(ext) for ext in ['.png', '.webp']):
                        score = 30
                        tipo = 'Imagem Institucional'
                    
                    if score > 0:
                        full_u = urljoin(page_url, img)
                        if full_u not in found_assets or found_assets[full_u].get('score', 0) < score:
                            found_assets[full_u] = {'tipo': tipo, 'score': score, 'origem': full_u}

        except Exception as e:
            # print(f"Erro ao ler página {page_url}: {e}")
            pass

    # Processar downloads e validações
    saved_for_hotel = []
    # Ordenar por score decrescente
    sorted_candidates = sorted(found_assets.items(), key=lambda x: x[1].get('score', 0), reverse=True)

    for item_key, meta in sorted_candidates:
        if 'file' in meta: # Já foi salvo como svg inline
            saved_for_hotel.append(meta)
            continue
            
        img_url = meta['origem']
        try:
            req_dl = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req_dl, timeout=8, context=ctx) as r_dl:
                raw_data = r_dl.read()
                ct = r_dl.headers.get('content-type', '').lower()
                
                is_svg = img_url.endswith('.svg') or 'svg' in ct
                is_png = img_url.endswith('.png') or 'png' in ct
                is_webp = img_url.endswith('.webp') or 'webp' in ct
                is_ico = img_url.endswith('.ico') or 'ico' in ct
                is_jpg = img_url.endswith('.jpg') or img_url.endswith('.jpeg') or 'jpeg' in ct or 'jpg' in ct
                
                ext = '.svg' if is_svg else ('.png' if is_png else ('.webp' if is_webp else ('.ico' if is_ico else ('.jpg' if is_jpg else '.png'))))
                
                w, h_dim = 0, 0
                if not is_svg:
                    try:
                        im = Image.open(io.BytesIO(raw_data))
                        w, h_dim = im.size
                        # Descartar imagens minúsculas (rastreadores de 1x1)
                        if w < 24 and h_dim < 24:
                            continue
                    except:
                        continue
                
                dim_str = 'Escalável (Vetor Nativo)' if is_svg else f"{w}x{h_dim} px"
                var_suffix = "principal" if meta['score'] >= 80 else ("vetor" if is_svg else ("icone" if 'icone' in meta['tipo'].lower() or 'favicon' in meta['tipo'].lower() else "social"))
                
                fname = f"{slugify(nome)}_{var_suffix}_{len(saved_for_hotel)+1}{ext}"
                fpath = os.path.join(hotel_dir, fname)
                with open(fpath, 'wb') as f_out:
                    f_out.write(raw_data)
                
                saved_for_hotel.append({
                    'file': fname,
                    'tipo': meta['tipo'],
                    'formato': ext.replace('.', '').upper(),
                    'dimensoes': dim_str,
                    'tamanho': f"{len(raw_data)/1024:.1f} KB",
                    'origem': img_url,
                    'score': meta['score']
                })
                
                # Pegar até 3 melhores variações por hotel
                if len(saved_for_hotel) >= 3:
                    break
        except Exception as e:
            continue

    if saved_for_hotel:
        best = saved_for_hotel[0]
        print(f"-> SUCESSO: {len(saved_for_hotel)} variações capturadas. Principal: {best['file']} ({best['dimensoes']})")
        for asset_item in saved_for_hotel:
            consolidated_table.append({
                'ranking': rank,
                'hotel': nome,
                'arquivo': f"{hotel_slug}/{asset_item['file']}",
                'tipo': asset_item['tipo'],
                'formato': asset_item['formato'],
                'dimensoes': asset_item['dimensoes'],
                'tamanho': asset_item['tamanho'],
                'origem': asset_item['origem']
            })
    else:
        print(f"-> NÃO ENCONTRADO: nenhum logotipo público identificado no portal.")
        consolidated_table.append({
            'ranking': rank,
            'hotel': nome,
            'arquivo': '-',
            'tipo': 'Logotipo Não Encontrado',
            'formato': '-',
            'dimensoes': '-',
            'tamanho': '-',
            'origem': site
        })

with open(r'C:\Users\Augusto\Desktop\AH3\scripts\tabela_consolidada_logos_top40.json', 'w', encoding='utf-8') as f:
    json.dump(consolidated_table, f, ensure_ascii=False, indent=2)

print("\nPROCESSAMENTO DOS 40 HOTÉIS CONCLUÍDO COM SUCESSO!")

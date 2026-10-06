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

json_path = r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_hotelaria_florianopolis.json'
with open(json_path, 'r', encoding='utf-8') as f:
    hotels = json.load(f)

base_assets_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual\logos_completos'
logos_flat_dir = r'C:\Users\Augusto\Desktop\AH3\guias_identidade_visual\logos'
os.makedirs(base_assets_dir, exist_ok=True)
os.makedirs(logos_flat_dir, exist_ok=True)

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text)
    return text.strip('_').lower()

# Carregar mapa de logos existente se houver
logos_info_path = r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_150.json'
existing_logos = {}
if os.path.exists(logos_info_path):
    try:
        with open(logos_info_path, 'r', encoding='utf-8') as lf:
            existing_list = json.load(lf)
            existing_logos = {item['ranking']: item for item in existing_list}
    except Exception:
        pass

# Também checar se temos do top40
top40_logos_path = r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_top40.json'
if os.path.exists(top40_logos_path):
    try:
        with open(top40_logos_path, 'r', encoding='utf-8') as lf:
            for item in json.load(lf):
                if item['ranking'] not in existing_logos:
                    existing_logos[item['ranking']] = item
    except Exception:
        pass

consolidated_table = []

for h in hotels:
    rank = h.get('ranking') or hotels.index(h) + 1
    nome = h['nome']
    site = h.get('site', '')
    quartos = h.get('quartos', 0)
    
    # Se já foi auditado com sucesso e o arquivo existe, reutiliza
    if rank in existing_logos and existing_logos[rank].get('qualidade') in ['Vetor Oficial', 'Alta Resolução', 'Média Resolução']:
        cached = existing_logos[rank]
        target_file = cached.get('arquivo', '')
        if target_file and os.path.exists(os.path.join(logos_flat_dir, target_file)):
            print(f"[{rank:03d}/150] {nome} -> Já auditado ({cached.get('qualidade')})")
            consolidated_table.append(cached)
            continue

    hotel_slug = f"{rank:03d}_{slugify(nome)[:30]}"
    hotel_dir = os.path.join(base_assets_dir, hotel_slug)
    os.makedirs(hotel_dir, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f"[{rank:03d}/150] Analisando: {nome} | {site}")
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
    for sub in ['/sobre', '/quem-somos', '/hotel', '/pt/']:
        pages_to_crawl.append(urljoin(site, sub))

    found_assets = {} # url -> dict of info

    for page_url in pages_to_crawl[:2]:
        try:
            req = urllib.request.Request(page_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                
                # SVGs inline
                svg_matches = re.findall(r'(<svg[^>]*>.*?</svg>)', html, flags=re.DOTALL | re.IGNORECASE)
                for idx, svg_code in enumerate(svg_matches):
                    if any(k in svg_code.lower() for k in ['logo', 'brand', 'header', 'navbar', 'emblema', 'marca']):
                        w = 500
                        h_val = 200
                        found_assets[f"inline_svg_{idx}"] = {
                            'type': 'svg_inline',
                            'code': svg_code,
                            'width': w,
                            'height': h_val,
                            'area': w * h_val,
                            'is_vector': True,
                            'score': 100000 + (w * h_val)
                        }

                # Tags <img>
                img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html, flags=re.IGNORECASE)
                for src in img_matches:
                    full_img_url = urljoin(page_url, src)
                    low_src = src.lower()
                    if any(bad in low_src for bad in ['facebook', 'tripadvisor', 'booking', 'whatsapp', 'instagram', 'arrow', 'icon', 'pixel', 'banner']):
                        continue
                    if any(good in low_src for good in ['logo', 'brand', 'marca', 'header', 'topo']):
                        found_assets[full_img_url] = {'type': 'img_tag', 'url': full_img_url, 'score': 5000}
                    elif full_img_url.endswith('.svg'):
                        found_assets[full_img_url] = {'type': 'svg_img', 'url': full_img_url, 'score': 8000}

                # Links / Icons
                link_matches = re.findall(r'<link[^>]+(?:rel=["\'][^"\']*(?:icon|logo|apple-touch-icon)[^"\']*["\'])[^>]+href=["\']([^"\']+)["\'][^>]*>', html, flags=re.IGNORECASE)
                for href in link_matches:
                    full_link_url = urljoin(page_url, href)
                    if not any(bad in full_link_url.lower() for bad in ['facebook', 'instagram', 'tripadvisor']):
                        found_assets[full_link_url] = {'type': 'icon', 'url': full_link_url, 'score': 1000}

        except Exception as e:
            pass

    # Baixar e avaliar candidatos
    evaluated_assets = []
    
    for key, asset in found_assets.items():
        try:
            if asset['type'] == 'svg_inline':
                fname = f"{slugify(nome)[:25]}_logo_inline_{len(evaluated_assets)+1}.svg"
                local_path = os.path.join(hotel_dir, fname)
                with open(local_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(asset['code'])
                evaluated_assets.append({
                    'path': local_path,
                    'filename': fname,
                    'format': 'SVG',
                    'width': 0,
                    'height': 0,
                    'area': 9999999,
                    'is_vector': True,
                    'score': 150000,
                    'source': 'SVG Inline HTML'
                })
            else:
                img_url = asset['url']
                req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(req, timeout=5, context=ctx) as img_resp:
                    content_bytes = img_resp.read()
                    
                ext = '.png'
                if '.svg' in img_url.lower(): ext = '.svg'
                elif '.webp' in img_url.lower(): ext = '.webp'
                elif '.jpg' in img_url.lower() or '.jpeg' in img_url.lower(): ext = '.jpg'
                
                fname = f"{slugify(nome)[:25]}_asset_{len(evaluated_assets)+1}{ext}"
                local_path = os.path.join(hotel_dir, fname)
                with open(local_path, 'wb') as f_out:
                    f_out.write(content_bytes)
                    
                if ext == '.svg':
                    evaluated_assets.append({
                        'path': local_path,
                        'filename': fname,
                        'format': 'SVG',
                        'width': 0,
                        'height': 0,
                        'area': 9999999,
                        'is_vector': True,
                        'score': 140000,
                        'source': img_url
                    })
                else:
                    try:
                        im = Image.open(io.BytesIO(content_bytes))
                        w, h_dim = im.size
                        area = w * h_dim
                        score = area
                        if 'logo' in img_url.lower() or 'brand' in img_url.lower():
                            score += 20000
                        evaluated_assets.append({
                            'path': local_path,
                            'filename': fname,
                            'format': im.format,
                            'width': w,
                            'height': h_dim,
                            'area': area,
                            'is_vector': False,
                            'score': score,
                            'source': img_url
                        })
                    except Exception:
                        pass
        except Exception:
            pass

    if evaluated_assets:
        evaluated_assets.sort(key=lambda x: x['score'], reverse=True)
        best = evaluated_assets[0]
        
        flat_ext = os.path.splitext(best['filename'])[1]
        flat_name = f"{rank:03d}_{slugify(nome)[:30]}{flat_ext}"
        flat_dest = os.path.join(logos_flat_dir, flat_name)
        
        with open(best['path'], 'rb') as f_in, open(flat_dest, 'wb') as f_out:
            f_out.write(f_in.read())
            
        qualidade = 'Alta Resolução'
        if best['is_vector']:
            qualidade = 'Vetor Oficial'
            dims = 'Escalável (Vetor Nativo)'
        else:
            dims = f"{best['width']}x{best['height']} px"
            if best['width'] < 150 or best['height'] < 50:
                qualidade = 'Média/Baixa Resolução'
                
        print(f"-> SUCESSO: {flat_name} ({qualidade} - {dims})")
        consolidated_table.append({
            'ranking': rank,
            'hotel': nome,
            'arquivo': flat_name,
            'tipo': 'Logotipo Oficial',
            'formato': best['format'],
            'dimensoes': dims,
            'qualidade': qualidade,
            'origem': best['source']
        })
    else:
        print(f"-> NÃO ENCONTRADO: nenhum asset no portal.")
        consolidated_table.append({
            'ranking': rank,
            'hotel': nome,
            'arquivo': '-',
            'tipo': 'Não Encontrado',
            'formato': '-',
            'dimensoes': '-',
            'qualidade': 'Pendente Revisão',
            'origem': '-'
        })

with open(logos_info_path, 'w', encoding='utf-8') as f:
    json.dump(consolidated_table, f, ensure_ascii=False, indent=2)

print("\nAuditoria de logos dos 150 hotéis concluída com sucesso!")

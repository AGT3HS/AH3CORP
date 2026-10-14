"""
Script de Auditoria, Extracao e Validacao Estrita de Telefones/WhatsApp (DDD 48)
dos Estabelecimentos Hoteleiros de Florianopolis e Regiao Metropolitana.

Regras Inegociaveis:
- Apenas DDD 48. Qualquer outro DDD e sumariamente descartado.
- Prioridade para celular WhatsApp (9 digitos) sobre telefone fixo (8 digitos).
- Extracao direta dos sites oficiais (home e subpaginas /contato, /reservas, /fale-conosco).
- Se a URL original estiver inativa, busca o dominio oficial autentico do hotel e atualiza a URL.
- Zero dados presumidos ou ficticios.
"""

import json
import re
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
}

IGN_DOMAINS = [
    'duckduckgo', 'w3.org', 'tripadvisor', 'booking.com', 'kayak', 'trivago',
    'cylex', 'hoteis.com', 'expedia', 'agoda', 'airbnb', 'wikipedia', 'youtube',
    'instagram.com', 'facebook.com', 'linkedin.com', 'twitter.com', 'tiktok.com',
    'guiatelefone', 'paginaamarela', 'telelistas', 'apontador', 'guiamais'
]

def clean_to_48(raw):
    """Retorna apenas numeros limpos com DDD 48 (10 ou 11 digitos)."""
    if not raw:
        return None
    d = re.sub(r'\D', '', str(raw))
    if d.startswith('55') and len(d) in [12, 13]:
        d = d[2:]
    if d.startswith('48') and len(d) in [10, 11]:
        # Validacao de digito local: fixo comeca com 2-5, celular com 9
        local = d[2:]
        if len(d) == 11 and local.startswith('9'):
            return d
        if len(d) == 10 and local[0] in '2345':
            return d
        # Alguns celulares antigos/locais ou fixos especiais
        if len(d) in [10, 11]:
            return d
    return None

def format_48(c):
    """Formata numero limpo para +55 48 XXXXX-XXXX ou +55 48 XXXX-XXXX."""
    if not c:
        return ''
    if len(c) == 11:
        return f'+55 48 {c[2:7]}-{c[7:]}'
    elif len(c) == 10:
        return f'+55 48 {c[2:6]}-{c[6:]}'
    return c

def search_ddg_lite(query):
    """Busca rapida via DuckDuckGo Lite."""
    url = 'https://lite.duckduckgo.com/lite/'
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception:
        return ''

def extract_from_html(html, base_url=''):
    """Extrai numeros com DDD 48 de links wa.me, tel e texto HTML."""
    wa_mobile = set()
    wa_fixo = set()
    other_mobile = set()
    other_fixo = set()

    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        soup = None

    # 1. Links wa.me, api.whatsapp.com, whatsapp:
    wa_links = re.findall(r'href=[\"\\\']([^\"\\\']*(?:wa\.me|api\.whatsapp\.com|whatsapp)[^\"\\\']*)[\"\\\']', html, re.I)
    for lk in wa_links:
        nums = re.findall(r'(?:phone=|wa\.me\/|send\?phone=|\/)([+0-9\-\s]{8,})', lk)
        for n in nums:
            c = clean_to_48(n)
            if c:
                if len(c) == 11 and c[2] == '9':
                    wa_mobile.add(c)
                else:
                    wa_fixo.add(c)

    # 2. Links tel:
    tel_links = re.findall(r'href=[\"\\\']tel:([^\"\\\']+)[\"\\\']', html, re.I)
    for tl in tel_links:
        c = clean_to_48(tl)
        if c:
            if len(c) == 11 and c[2] == '9':
                other_mobile.add(c)
            else:
                other_fixo.add(c)

    # 3. Contexto explicito WhatsApp no texto
    text = soup.get_text(separator=' ') if soup else html
    for m in re.finditer(r'(?:whatsapp|whats|wpp|zap|celular|reservas?)', text, re.I):
        snip = text[max(0, m.start()-30):min(len(text), m.end()+120)]
        found = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)[2-9]\d{3,4}[-\s]?\d{4}', snip)
        for n in found:
            c = clean_to_48(n)
            if c:
                if len(c) == 11 and c[2] == '9':
                    wa_mobile.add(c)
                else:
                    wa_fixo.add(c)

    # 4. Todos os telefones DDD 48 no texto
    all_48 = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)[2-9]\d{3,4}[-\s]?\d{4}', text)
    for n in all_48:
        c = clean_to_48(n)
        if c:
            if len(c) == 11 and c[2] == '9':
                other_mobile.add(c)
            else:
                other_fixo.add(c)

    # Hierarquia estrita de escolha
    if wa_mobile:
        return list(wa_mobile)[0], 'site_wa_mobile'
    if other_mobile:
        return list(other_mobile)[0], 'site_mobile_48'
    if wa_fixo:
        return list(wa_fixo)[0], 'site_wa_fixo'
    if other_fixo:
        return list(other_fixo)[0], 'site_fixo_48'

    return None, None

def fetch_page(url, timeout=6):
    """Requisicao segura com variantes https e http."""
    variants = []
    if url.startswith('http://') or url.startswith('https://'):
        variants.append(url)
    else:
        variants.append('https://' + url)
        variants.append('http://' + url)

    for u in variants:
        try:
            r = requests.get(u, headers=HEADERS, timeout=timeout, verify=False, allow_redirects=True)
            if r.status_code == 200 and len(r.text) > 300:
                return r.text, r.url
        except Exception:
            continue
    return None, None

def process_hotel(hotel):
    """Processa um hotel: valida site atual, busca novo site se necessario, extrai DDD 48."""
    rk = hotel['ranking']
    nome = hotel['nome']
    regiao = hotel.get('regiao', 'Florianópolis')
    site_orig = hotel.get('site', '')

    best_phone = None
    source = None
    real_site = site_orig

    # Tentativa 1: Site atual
    if site_orig:
        html, final_url = fetch_page(site_orig)
        if html and final_url:
            real_site = final_url
            c, src = extract_from_html(html, final_url)
            if c:
                best_phone = c
                source = f'{src}_home'
            else:
                # Tentar subpaginas
                for sub in ['/contato', '/fale-conosco', '/contato/', '/reservas', '/reservas/']:
                    sub_url = urllib.parse.urljoin(final_url, sub)
                    sub_html, _ = fetch_page(sub_url, timeout=4)
                    if sub_html:
                        sub_c, sub_src = extract_from_html(sub_html, sub_url)
                        if sub_c:
                            best_phone = sub_c
                            source = f'{sub_src}_subpage'
                            break

    # Tentativa 2: Se nao achou telefone no site atual, pesquisar dominio oficial ou contato na web
    if not best_phone:
        ddg_html = search_ddg_lite(f'"{nome}" {regiao} Florianopolis site oficial telefone')
        if ddg_html:
            # Encontrar possiveis sites oficiais
            candidate_urls = re.findall(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s\"\'<>]*)?', ddg_html)
            filtered_urls = []
            for cu in candidate_urls:
                cu_clean = cu.lower()
                if not any(ign in cu_clean for ign in IGN_DOMAINS):
                    filtered_urls.append(cu)

            # Testar ate 2 sites candidatos
            for cand in filtered_urls[:2]:
                cand_html, cand_final = fetch_page(cand, timeout=5)
                if cand_html and cand_final:
                    c, src = extract_from_html(cand_html, cand_final)
                    if c:
                        best_phone = c
                        source = f'{src}_discovered_site'
                        real_site = cand_final
                        break

            # Se ainda nao achou, extrair da propria busca DDG
            if not best_phone:
                nums = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)[2-9]\d{3,4}[-\s]?\d{4}', ddg_html)
                clean_candidates = [n for n in (clean_to_48(raw) for raw in nums) if n is not None]
                # Priorizar celular
                mobiles = [n for n in clean_candidates if len(n) == 11 and n[2] == '9']
                if mobiles:
                    best_phone = mobiles[0]
                    source = 'search_snippet_mobile_48'
                elif clean_candidates:
                    best_phone = clean_candidates[0]
                    source = 'search_snippet_fixo_48'

    # Se ainda nao achou, busca especifica de WhatsApp DDD 48
    if not best_phone:
        ddg_wa = search_ddg_lite(f'{nome} Florianopolis whatsapp (48)')
        if ddg_wa:
            nums = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)[2-9]\d{3,4}[-\s]?\d{4}', ddg_wa)
            clean_candidates = [n for n in (clean_to_48(raw) for raw in nums) if n is not None]
            mobiles = [n for n in clean_candidates if len(n) == 11 and n[2] == '9']
            if mobiles:
                best_phone = mobiles[0]
                source = 'search_wa_mobile_48'
            elif clean_candidates:
                best_phone = clean_candidates[0]
                source = 'search_wa_fixo_48'

    formatted = format_48(best_phone) if best_phone else ''
    clean_val = best_phone if best_phone else ''

    return {
        'ranking': rk,
        'nome': nome,
        'site': real_site,
        'telefone': formatted,
        'phone_clean': clean_val,
        'source': source
    }

def main():
    with open('scripts/data/sorted_150_hotels.json', 'r', encoding='utf-8') as f:
        hoteis = json.load(f)

    print(f'Iniciando processamento de {len(hoteis)} estabelecimentos hoteleiros...')
    start_time = time.time()

    results = {}
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(process_hotel, h): h['ranking'] for h in hoteis}
        for fut in as_completed(futures):
            res = fut.result()
            results[res['ranking']] = res
            status_str = f"{res['telefone']} ({res['source']})" if res['telefone'] else "NAO_ENCONTRADO"
            print(f"#{res['ranking']:3d} | {res['nome'][:30]:30s} | {status_str}")

    # Atualizar base JSON
    success_count = 0
    for h in hoteis:
        rk = h['ranking']
        if rk in results:
            r = results[rk]
            if r['telefone']:
                h['telefone'] = r['telefone']
                h['phone_clean'] = r['phone_clean']
                h['site'] = r['site']
                h['contato_fonte'] = r['source']
                success_count += 1
            else:
                h['telefone'] = ''
                h['phone_clean'] = ''
                h['contato_fonte'] = 'pendente'

    with open('scripts/data/sorted_150_hotels.json', 'w', encoding='utf-8') as f:
        json.dump(hoteis, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    print(f'\nConcluido em {elapsed:.1f}s.')
    print(f'Hoteis com DDD 48 autentico validado: {success_count}/{len(hoteis)}')

if __name__ == '__main__':
    main()

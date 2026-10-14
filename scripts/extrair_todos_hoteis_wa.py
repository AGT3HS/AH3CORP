import json
import re
import time
import requests
import urllib3
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import concurrent.futures

urllib3.disable_warnings()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
}

def clean_to_48(raw):
    d = re.sub(r'\D', '', str(raw))
    if d.startswith('55'):
        d = d[2:]
    if d.startswith('48') and len(d) in [10, 11]:
        return d
    return None

def format_phone(c):
    if not c or not c.startswith('48'):
        return ''
    if len(c) == 11:
        return f"+55 48 {c[2:7]}-{c[7:]}"
    elif len(c) == 10:
        return f"+55 48 {c[2:6]}-{c[6:]}"
    return c

def extract_from_html(html, base_url):
    wa_mobile = []
    wa_fixo = []
    text_mobile = []
    text_fixo = []
    other_48 = []

    # 1. Links
    links = re.findall(r'href=[\"\\\']([^\"\\\']+)[\"\\\']', html)
    for l in links:
        l_low = l.lower()
        if any(k in l_low for k in ['wa.me', 'whatsapp.com', 'whatsapp://']):
            nums = re.findall(r'(?:phone=|wa\.me\/|send\?phone=|\/)([+0-9\-\s]{8,})', l)
            for raw in nums:
                c = clean_to_48(raw)
                if c:
                    if len(c) == 11 and c[2] == '9':
                        wa_mobile.append(c)
                    else:
                        wa_fixo.append(c)
        elif 'tel:' in l_low:
            raw = l_low.split('tel:')[-1]
            c = clean_to_48(raw)
            if c:
                if len(c) == 11 and c[2] == '9':
                    other_48.append(c)
                else:
                    other_48.append(c)

    # 2. BeautifulSoup text extraction
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ')

    # Near "whatsapp", "whats", "zap", "wpp"
    for m in re.finditer(r'(?:whatsapp|whats|wpp|zap)', text, re.I):
        snip = text[max(0, m.start() - 30):min(len(text), m.end() + 150)]
        found = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)?[2-9]\d{3,4}[-\s]?\d{4}', snip)
        for num in found:
            c = clean_to_48(num)
            if not c:
                clean_digits = re.sub(r'\D', '', num)
                c = clean_to_48('48' + clean_digits)
            if c:
                if len(c) == 11 and c[2] == '9':
                    text_mobile.append(c)
                else:
                    text_fixo.append(c)

    # All phones with 48 in text
    all_48 = re.findall(r'(?:\+?55\s*)?(?:\(?48\)?\s*)[2-9]\d{3,4}[-\s]?\d{4}', text)
    for num in all_48:
        c = clean_to_48(num)
        if c:
            other_48.append(c)

    return {
        'wa_mobile': list(dict.fromkeys(wa_mobile)),
        'wa_fixo': list(dict.fromkeys(wa_fixo)),
        'text_mobile': list(dict.fromkeys(text_mobile)),
        'text_fixo': list(dict.fromkeys(text_fixo)),
        'other_48': list(dict.fromkeys(other_48)),
    }

def find_subpages(soup, base_url):
    domain = urlparse(base_url).netloc.replace('www.', '')
    subpages = []
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        full = urljoin(base_url, href)
        p = urlparse(full)
        if domain in p.netloc:
            path_lower = p.path.lower()
            if any(k in path_lower for k in ['contat', 'fale', 'reserv', 'atend', 'unidade', 'sobre', 'local']):
                if full not in subpages and full != base_url:
                    subpages.append(full)
    return subpages[:3]

def scrape_hotel(hotel):
    site = hotel.get('site', '')
    nome = hotel.get('nome', '')
    ranking = hotel.get('ranking', 0)

    if not site:
        return ranking, None, None, "SEM_SITE"

    # Known domain fixups
    if 'inglesespraiahotel.com.br' in site:
        site = 'https://www.inglesespraia.com.br'
    elif 'sesc-sc.com.br/hotelsesccacupe' in site:
        site = 'https://www.sesc-sc.com.br/hotelsesccacupe/'

    collected = {
        'wa_mobile': [],
        'wa_fixo': [],
        'text_mobile': [],
        'text_fixo': [],
        'other_48': []
    }

    try:
        r = requests.get(site, headers=HEADERS, timeout=7, verify=False, allow_redirects=True)
        if r.status_code == 200:
            res = extract_from_html(r.text, r.url)
            for k in collected:
                collected[k].extend(res[k])

            soup = BeautifulSoup(r.text, 'html.parser')
            subs = find_subpages(soup, r.url)
            for sub in subs:
                try:
                    r_sub = requests.get(sub, headers=HEADERS, timeout=5, verify=False, allow_redirects=True)
                    if r_sub.status_code == 200:
                        res_sub = extract_from_html(r_sub.text, r_sub.url)
                        for k in collected:
                            collected[k].extend(res_sub[k])
                except:
                    pass
    except Exception as e:
        return ranking, None, None, f"ERRO_CONEXAO: {type(e).__name__}"

    # Deduplicate
    for k in collected:
        collected[k] = list(dict.fromkeys(collected[k]))

    # Selection hierarchy:
    # 1. wa_mobile (Direct wa.me mobile)
    # 2. text_mobile (Text labeled whats mobile)
    # 3. wa_fixo (Direct wa.me landline)
    # 4. text_fixo (Text labeled whats landline)
    # 5. other_48 mobile
    # 6. other_48 fixo
    chosen = None
    source = "NONE"

    if collected['wa_mobile']:
        chosen = collected['wa_mobile'][0]
        source = "wa_mobile_link"
    elif collected['text_mobile']:
        chosen = collected['text_mobile'][0]
        source = "text_mobile_whats"
    elif collected['wa_fixo']:
        chosen = collected['wa_fixo'][0]
        source = "wa_fixo_link"
    elif collected['text_fixo']:
        chosen = collected['text_fixo'][0]
        source = "text_fixo_whats"
    elif collected['other_48']:
        # prefer 11 digits
        mobs = [x for x in collected['other_48'] if len(x) == 11 and x[2] == '9']
        if mobs:
            chosen = mobs[0]
            source = "other_48_mobile"
        else:
            chosen = collected['other_48'][0]
            source = "other_48_fixo"

    if chosen:
        formatted = format_phone(chosen)
        phone_clean = '55' + chosen
        return ranking, formatted, phone_clean, source

    return ranking, None, None, "NAO_ENCONTRADO"

if __name__ == '__main__':
    with open('scripts/data/sorted_150_hotels.json', 'r', encoding='utf-8') as f:
        hoteis = json.load(f)

    print(f"Iniciando varredura em {len(hoteis)} hoteis...")
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as ex:
        futures = {ex.submit(scrape_hotel, h): h for h in hoteis}
        for fut in concurrent.futures.as_completed(futures):
            ranking, fmt, clean, src = fut.result()
            results[ranking] = (fmt, clean, src)

    encontrados = sum(1 for r in results.values() if r[0])
    print(f"\nFinalizado! Total de contatos com DDD 48 identificados: {encontrados}/{len(hoteis)}")

    # Mostra primeiros 20
    for rk in range(1, 21):
        if rk in results:
            h = next(x for x in hoteis if x['ranking'] == rk)
            print(f"#{rk:2d} | {h['nome'][:30]:30s} | {results[rk][0]} ({results[rk][2]})")

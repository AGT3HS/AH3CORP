import json
import re
import time
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

DATA_FILE = 'scripts/data/sorted_150_hotels.json'

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    hoteis = json.load(f)

def clean_phone(p):
    d = re.sub(r'\D', '', str(p))
    if d.startswith('55') and len(d) in [12, 13]:
        d = d[2:]
    return d

def get_whatsapp_from_website(hotel):
    site = hotel.get('site')
    if not site:
        return (hotel['ranking'], None)
    
    # Adicionando https se faltar
    if not site.startswith('http'):
        site = 'https://' + site

    try:
        r = requests.get(site, headers=headers, timeout=10, verify=False)
        html = r.text
        
        # Procura links diretos de WhatsApp (wa.me, api.whatsapp.com)
        match_wa = re.findall(r'href=[\'"](?:https?://)?(?:wa\.me/|api\.whatsapp\.com/send\?phone=|\+?\d*\?phone=|\/send\?phone=|\/\?phone=)[^0-9+]*([+0-9\-\s]+)', html)
        if match_wa:
            for num in match_wa:
                cleaned = clean_phone(num)
                # Aceitar se for um número válido (mínimo 10 dígitos)
                if len(cleaned) >= 10:
                    return (hotel['ranking'], cleaned)
                    
        # Se não encontrou link, busca regex de celular pelo menos
        cels = re.findall(r'(?:[wW]hats[aA]pp|WA).{0,20}\(?48\)?\s*9?\d{4}[-\s]?\d{4}', html)
        if cels:
            cleaned = clean_phone(cels[0])
            if len(cleaned) >= 10:
                return (hotel['ranking'], cleaned)
                
    except Exception as e:
        pass
        
    return (hotel['ranking'], None)

def main():
    print("Iniciando extração profunda nos sites dos hotéis...")
    resultados = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {executor.submit(get_whatsapp_from_website, h): h for h in hoteis}
        for idx, futuro in enumerate(as_completed(futuros)):
            r, num = futuro.result()
            if num:
                resultados[r] = num
            if (idx + 1) % 15 == 0:
                print(f"Buscados: {idx + 1}/{len(hoteis)}")
                
    print(f"Total de números de WhatsApp encontrados: {len(resultados)}")
    
    # Aplicar os achados
    for h in hoteis:
        r = h.get('ranking')
        if r in resultados:
            c = resultados[r]
            # formatar
            if len(c) == 11:
                h['telefone'] = f"({c[:2]}) {c[2:7]}-{c[7:]}"
            else:
                h['telefone'] = f"({c[:2]}) {c[2:6]}-{c[6:]}"
            h['phone_clean'] = f"55{c}"
        elif '3000' in h.get('telefone', ''):
            # Limpa telefone se não encontrou nada e era o genérico 3000
            h['telefone'] = ''
            h['phone_clean'] = ''
            
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hoteis, f, ensure_ascii=False, indent=2)
        
    print("Base JSON atualizada com os números extraídos diretamente dos sites.")

if __name__ == '__main__':
    main()

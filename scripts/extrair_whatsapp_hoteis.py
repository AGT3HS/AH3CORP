"""
Script de Auditoria e Extração de WhatsApp Oficial dos Hotéis da Grande Florianópolis.
Varre os sites dos estabelecimentos em busca de links diretos de WhatsApp (wa.me, api.whatsapp.com, etc.)
e números de celular/WhatsApp para prospecção.
"""

import os
import re
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3

urllib3.disable_warnings()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, 'scripts', 'data', 'sorted_150_hotels.json')
CLIENTES_DIR = os.path.join(ROOT_DIR, 'BigBrain', 'clientes')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def formatar_telefone_br(digitos):
    """Formata sequência de dígitos no padrão telefônico brasileiro."""
    d = re.sub(r'\D', '', str(digitos))
    if d.startswith('55') and len(d) in (12, 13):
        d = d[2:]
    if len(d) == 11:
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"
    elif len(d) == 10:
        return f"({d[:2]}) {d[2:6]}-{d[6:]}"
    return digitos

def limpar_para_wa(digitos):
    """Retorna o número limpo com DDI 55 para links de WhatsApp."""
    d = re.sub(r'\D', '', str(digitos))
    if not d:
        return ""
    if d.startswith('55') and len(d) >= 12:
        return d
    if len(d) in (10, 11):
        return f"55{d}"
    return d

def buscar_wa_em_html(html, base_url):
    """Extrai números e links de WhatsApp de um conteúdo HTML."""
    if not html:
        return []
    
    encontrados = []
    
    # 1. Links diretos para WhatsApp (wa.me, api.whatsapp.com, send?phone=, etc.)
    wa_hrefs = re.findall(r'href=[\"\']([^\"\']*(?:wa\.me|api\.whatsapp\.com|whatsapp\.com/send|web\.whatsapp\.com)[^\"\']*)[\"\']', html, re.I)
    for link in wa_hrefs:
        # Extrair parâmetro phone ou caminho wa.me/
        m = re.search(r'(?:phone=|wa\.me/|send\?phone=|\?p=|\/)([0-9+]+)', link)
        if m:
            raw_num = m.group(1)
            clean = re.sub(r'\D', '', raw_num)
            if len(clean) >= 10:
                encontrados.append(('link_wa', clean, link))

    # 2. Textos contendo 'whatsapp', 'whats', 'zap' seguido de número
    wa_texts = re.findall(r'(?:whatsapp|whats|zap|wpp)[^0-9\n<]{0,40}?(\+?55\s*\(?\d{2}\)?\s*9?\d{4}[-\s]?\d{4})', html, re.I)
    for num in wa_texts:
        clean = re.sub(r'\D', '', num)
        if len(clean) in (10, 11, 12, 13):
            encontrados.append(('texto_wa', clean, num))

    # 3. Links tel: com celular (9 dígitos)
    tel_hrefs = re.findall(r'href=[\"\']tel:([^\"\']+)[\"\']', html, re.I)
    for link in tel_hrefs:
        clean = re.sub(r'\D', '', link)
        if clean.startswith('55'):
            clean = clean[2:]
        if len(clean) == 11 and clean[2] == '9': # Celular
            encontrados.append(('tel_celular', clean, link))

    # 4. Celulares gerais DDD 48 ou 47 no padrão (48) 9XXXX-XXXX
    cels = re.findall(r'(?:(?:\+?55\s*)?\(?(?:48|47)\)?\s*(9\d{4})[-\s]?(\d{4}))', html)
    for c in cels:
        full_c = re.findall(r'(?:\+?55\s*)?\(?(?:48|47)\)?\s*9\d{4}[-\s]?\d{4}', html)
        for fc in full_c:
            clean = re.sub(r'\D', '', fc)
            if len(clean) in (10, 11, 12, 13):
                encontrados.append(('cel_geral', clean, fc))

    return encontrados

def raspar_hotel(hotel):
    """Executa a raspagem de WhatsApp no site do hotel e subpáginas."""
    ranking = hotel.get('ranking')
    nome = hotel.get('nome')
    site = hotel.get('site')
    tel_atual = hotel.get('telefone', '')
    
    res = {
        'ranking': ranking,
        'nome': nome,
        'site': site,
        'tel_original': tel_atual,
        'whatsapp_encontrado': None,
        'origem': None,
        'status': 'pendente'
    }
    
    if not site:
        res['status'] = 'sem_site'
        return res
        
    urls_para_testar = [site]
    
    # Gerar URLs de subpáginas comuns de contato
    base = site.rstrip('/')
    urls_para_testar.extend([
        f"{base}/contato",
        f"{base}/contato/",
        f"{base}/fale-conosco",
        f"{base}/fale-conosco/",
        f"{base}/reservas",
        f"{base}/reservas/",
        f"{base}/pt/contato"
    ])
    
    # Remover duplicatas mantendo ordem
    seen = set()
    urls_unicas = []
    for u in urls_para_testar:
        if u not in seen:
            seen.add(u)
            urls_unicas.append(u)
            
    session = requests.Session()
    session.headers.update(HEADERS)
    
    candidatos = []
    
    for u in urls_unicas:
        try:
            resp = session.get(u, timeout=7, verify=False, allow_redirects=True)
            if resp.status_code == 200:
                achados = buscar_wa_em_html(resp.text, u)
                if achados:
                    candidatos.extend(achados)
                    # Se encontrou link direto de WhatsApp, podemos parar
                    has_direct_wa = any(x[0] == 'link_wa' for x in achados)
                    if has_direct_wa:
                        break
        except Exception:
            continue
            
    if candidatos:
        # Priorizar: 1. link_wa com celular (9 digitos) ou DDD 48
        # 2. texto_wa com celular
        # 3. link_wa qualquer
        # 4. cel_geral
        melhor = None
        for tipo, clean, raw in candidatos:
            clean_digits = re.sub(r'\D', '', clean)
            if clean_digits.startswith('55') and len(clean_digits) >= 12:
                clean_digits = clean_digits[2:]
            
            # Checar se é número válido (10 ou 11 dígitos)
            if len(clean_digits) in (10, 11):
                # Se for celular DDD 48 ou 47, prioridade máxima
                if len(clean_digits) == 11 and clean_digits[:2] in ('48', '47') and clean_digits[2] == '9':
                    melhor = (tipo, clean_digits, raw)
                    break
                elif tipo == 'link_wa' and melhor is None:
                    melhor = (tipo, clean_digits, raw)
                elif melhor is None:
                    melhor = (tipo, clean_digits, raw)
                    
        if melhor:
            tipo, clean_digits, raw = melhor
            res['whatsapp_encontrado'] = formatar_telefone_br(clean_digits)
            res['phone_clean'] = limpar_para_wa(clean_digits)
            res['origem'] = tipo
            res['status'] = 'encontrado'
            return res
            
    res['status'] = 'nao_encontrado'
    return res

def main():
    print(f"Lendo dados de {DATA_FILE}...")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        hoteis = json.load(f)
        
    print(f"Iniciando varredura concorrente em {len(hoteis)} sites de hotéis...")
    
    resultados = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        futuros = {executor.submit(raspar_hotel, h): h for h in hoteis}
        for future in as_completed(futuros):
            try:
                res = future.result()
                resultados.append(res)
                if res['status'] == 'encontrado':
                    print(f"[{len(resultados)}/{len(hoteis)}] [OK] #{res['ranking']} {res['nome']} -> WA: {res['whatsapp_encontrado']} ({res['origem']})")
                else:
                    print(f"[{len(resultados)}/{len(hoteis)}] [Padrão] #{res['ranking']} {res['nome']} -> Mantém: {res['tel_original']}")
            except Exception as e:
                print(f"Erro ao processar: {e}")
                
    resultados.sort(key=lambda x: x['ranking'])
    
    total_encontrados = sum(1 for r in resultados if r['status'] == 'encontrado')
    print(f"\nVarredura concluída! WhatsApp oficial identificado em {total_encontrados} de {len(hoteis)} hotéis.")
    
    # Atualizar sorted_150_hotels.json
    atualizados = 0
    for h in hoteis:
        r = h.get('ranking')
        match_res = next((x for x in resultados if x['ranking'] == r), None)
        if match_res and match_res['status'] == 'encontrado':
            h['telefone_fixo'] = h.get('telefone')
            h['telefone'] = match_res['whatsapp_encontrado']
            h['phone_clean'] = match_res['phone_clean']
            h['origem_contato'] = 'whatsapp_site'
            atualizados += 1
            
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(hoteis, f, ensure_ascii=False, indent=2)
        
    print(f"Arquivo {DATA_FILE} atualizado com {atualizados} números diretos de WhatsApp!")
    
    # Atualizar os hotel_info.json individuais em BigBrain/clientes/
    for h in hoteis:
        r = h.get('ranking')
        # Localizar pasta do cliente
        prefix = f"{r:02d}_"
        subdirs = [d for d in os.listdir(CLIENTES_DIR) if d.startswith(prefix) and os.path.isdir(os.path.join(CLIENTES_DIR, d))]
        if subdirs:
            hotel_dir = os.path.join(CLIENTES_DIR, subdirs[0])
            info_file = os.path.join(hotel_dir, 'hotel_info.json')
            if os.path.exists(info_file):
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        info_data = json.load(f)
                    info_data['telefone'] = h.get('telefone')
                    if 'telefone_fixo' in h:
                        info_data['telefone_fixo'] = h.get('telefone_fixo')
                    info_data['phone_clean'] = h.get('phone_clean')
                    with open(info_file, 'w', encoding='utf-8') as f:
                        json.dump(info_data, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Erro ao atualizar {info_file}: {e}")

if __name__ == '__main__':
    main()

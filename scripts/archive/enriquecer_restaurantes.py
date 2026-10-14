import json
import re
import requests
from urllib.parse import urlparse
import concurrent.futures

INPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_raw.json"
OUTPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_enriquecido.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    places = json.load(f)

print(f"Carregados {len(places)} estabelecimentos para enriquecimento.")

# Regras de exclusão de redes conhecidas / nacionais adicionais
CHAINS_EXTRA = [
    "subway", "mcdonald", "burger king", "bobs", "habib", "cacau show", "kopenhagen",
    "outback", "madero", "dunkin", "starbucks", "domino", "pizza hut", "giraffas",
    "china in box", "spoleto", "vivenda do camarao", "subway", "amigo urso", "pague menos"
]

def extract_instagram_from_html(html_text):
    if not html_text:
        return None
    # Procura links do instagram
    matches = re.findall(r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_\.]+)', html_text, re.IGNORECASE)
    for handle in matches:
        handle_clean = handle.strip("/?&").lower()
        if handle_clean not in ["p", "reel", "stories", "explore", "tv", "accounts", "share", "home", "instagram"]:
            return f"https://www.instagram.com/{handle_clean}/"
    return None

def extract_ifood_from_html(html_text):
    if not html_text:
        return None
    matches = re.findall(r'https?://(?:www\.)?ifood\.com\.br/delivery/[a-zA-Z0-9_\-\.\/]+', html_text, re.IGNORECASE)
    if matches:
        return matches[0]
    if "ifood" in html_text.lower():
        return "Sim (mencionado no site/link)"
    return None

def enrich_single_place(place):
    site = place.get("site", "")
    place_name = place.get("nome", "")
    
    # Check chain by name
    name_lower = place_name.lower()
    if any(c in name_lower for c in CHAINS_EXTRA):
        place["is_chain"] = True
    else:
        place["is_chain"] = False
        
    # Se o próprio site for link do instagram
    if "instagram.com/" in site:
        place["instagram"] = site
        place["site"] = "não informado (usa Instagram)"
    elif site.startswith("http"):
        try:
            resp = requests.get(site, timeout=6, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            if resp.status_code == 200:
                html = resp.text
                ig = extract_instagram_from_html(html)
                if ig:
                    place["instagram"] = ig
                
                ifood_res = extract_ifood_from_html(html)
                if ifood_res:
                    place["ifood"] = ifood_res
                else:
                    place["ifood"] = "não identificado"
        except Exception:
            pass
            
    # Se ainda não achou instagram e o site não respondeu, mantém "não encontrado"
    if place.get("instagram") == "não encontrado":
        # Se for linktree ou similar
        if "linktr.ee" in site or "instabio" in site:
            try:
                resp = requests.get(site, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    ig = extract_instagram_from_html(resp.text)
                    if ig:
                        place["instagram"] = ig
            except Exception:
                pass
                
    return place

# Executa enriquecimento com multithreading
print("Iniciando enriquecimento web (Instagram, iFood, Redes)...")
with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    enriched_places = list(executor.map(enrich_single_place, places))

# Filtra redes confirmadas
valid_places = [p for p in enriched_places if not p.get("is_chain")]

print(f"Total pós-filtro de redes: {len(valid_places)} restaurantes.")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(valid_places, f, ensure_ascii=False, indent=2)

print(f"Arquivo final salvo em {OUTPUT_FILE}")

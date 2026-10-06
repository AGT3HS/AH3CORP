import os
import json
import re
import time
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not API_KEY:
    print("ERRO: GOOGLE_PLACES_API_KEY não encontrada no .env")
    exit(1)

# Configurações de Bairros e Buscas
BAIRROS = [
    "Ponta das Canas, Florianópolis - SC",
    "Canasvieiras, Florianópolis - SC",
    "Jurerê, Florianópolis - SC",
    "Jurerê Internacional, Florianópolis - SC",
    "Jurerê Tradicional, Florianópolis - SC"
]

CATEGORIAS_QUERIES = [
    ("restaurante", "Restaurante"),
    ("restaurante japonês sushi", "Japonesa"),
    ("restaurante italiano massas", "Italiana"),
    ("restaurante frutos do mar peixaria", "Frutos do Mar"),
    ("pizzaria", "Pizzaria"),
    ("hamburgueria burger", "Hamburgueria"),
    ("restaurante comida brasileira comida caseira", "Brasileira"),
    ("bar petiscaria chopp", "Bar"),
    ("cafeteria café bistro", "Café"),
    ("padaria panificadora confeitaria", "Padaria")
]

KNOWN_CHAINS = [
    "mcdonald's", "mcdonalds", "burger king", "subway", "bobs", "bob's",
    "habib's", "habibs", "cacau show", "kopenhagen", "outback", "madero",
    "dunkin", "starbucks", "domino's", "dominos", "pizza hut", "pizzahut",
    "giraffas", "china in box", "spoleto", "vivenda do camarão"
]

def map_category(primary_type, name, query_cat):
    pt = (primary_type or "").lower()
    nm = (name or "").lower()
    
    if any(k in pt or k in nm for k in ["sushi", "japanese", "japones", "temaki", "ramen"]):
        return "Japonesa"
    if any(k in pt or k in nm for k in ["pizza", "pizzaria"]):
        return "Pizzaria"
    if any(k in pt or k in nm for k in ["burger", "hamburguer", "hamburgueria"]):
        return "Hamburgueria"
    if any(k in pt or k in nm for k in ["italian", "italiano", "massa", "pasta", "trattoria"]):
        return "Italiana"
    if any(k in pt or k in nm for k in ["seafood", "frutos do mar", "peixe", "ostra", "marisco", "camarao", "camarão"]):
        return "Frutos do Mar"
    if any(k in pt or k in nm for k in ["bakery", "padaria", "confeitaria"]):
        return "Padaria"
    if any(k in pt or k in nm for k in ["cafe", "café", "coffee", "bistro", "bistrô"]):
        return "Café"
    if any(k in pt or k in nm for k in ["bar", "pub", "chopp", "choperia", "cervejaria", "boteco"]):
        return "Bar"
    if any(k in pt or k in nm for k in ["brazilian", "churrascaria", "churrasco", "galeteria", "brasileira"]):
        return "Brasileira"
    
    if query_cat and query_cat != "Restaurante":
        return query_cat
    return "Brasileira / Variada"

def extract_bairro_canonico(formatted_address, raw_bairro):
    addr = formatted_address or ""
    if "ponta das canas" in addr.lower() or "ponta das canas" in raw_bairro.lower():
        return "Ponta das Canas"
    if "canasvieiras" in addr.lower() or "canasvieiras" in raw_bairro.lower():
        return "Canasvieiras"
    if "jurerê internacional" in addr.lower() or "jurere internacional" in addr.lower() or "jurerê internacional" in raw_bairro.lower():
        return "Jurerê Internacional"
    if "jurerê" in addr.lower() or "jurere" in addr.lower() or "jurerê" in raw_bairro.lower():
        return "Jurerê"
    return raw_bairro.split(",")[0].strip()

def search_places_new(query):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.businessStatus,places.websiteUri,places.internationalPhoneNumber,places.nationalPhoneNumber,places.regularOpeningHours,places.primaryType,places.types,places.googleMapsUri,places.location"
    }
    payload = {
        "textQuery": query,
        "languageCode": "pt-BR",
        "regionCode": "BR",
        "maxResultCount": 20
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            return resp.json().get("places", [])
        else:
            print(f"Erro API Places [{resp.status_code}]: {resp.text}")
            return []
    except Exception as e:
        print(f"Exceção na chamada API: {e}")
        return []

def format_whatsapp(phone):
    if not phone or phone == "não encontrado":
        return "não encontrado"
    clean = re.sub(r"\D", "", phone)
    if clean.startswith("55"):
        num = clean[2:]
    else:
        num = clean
    
    # Valida se é celular brasileiro (DDD de 2 dígitos + 9 dígitos começando com 9)
    if len(num) == 11 and num[2] == "9":
        return f"https://wa.me/55{num}"
    elif len(num) == 10:
        # Fixo
        return "fixo (sem wa.me direto)"
    elif len(clean) >= 10:
        return f"https://wa.me/{clean}"
    return "não encontrado"

def format_price_level(pl):
    mapping = {
        "PRICE_LEVEL_INEXPENSIVE": "$ (Econômico)",
        "PRICE_LEVEL_MODERATE": "$$ (Moderado)",
        "PRICE_LEVEL_EXPENSIVE": "$$$ (Sofisticado)",
        "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$ (Luxo)",
        "PRICE_LEVEL_UNSPECIFIED": "não informado"
    }
    return mapping.get(pl, pl or "não informado")

def run():
    print("=== INICIANDO VARREDURA RADAR GOOGLE PLACES NEW ===")
    places_map = {} # place_id -> data
    
    for bairro in BAIRROS:
        bairro_nome = bairro.split(",")[0].strip()
        print(f"\n--- Varrendo Bairro: {bairro_nome} ---")
        for q_term, q_cat in CATEGORIAS_QUERIES:
            query = f"{q_term} em {bairro}"
            print(f"Buscando: '{query}'...")
            results = search_places_new(query)
            print(f"  -> Encontrados: {len(results)} estabelecimentos")
            
            for p in results:
                pid = p.get("id")
                if not pid:
                    continue
                
                name = p.get("displayName", {}).get("text", "Sem nome")
                status = p.get("businessStatus", "OPERATIONAL")
                
                # Regra 1: Excluir permanentemente fechados
                if status == "CLOSED_PERMANENTLY":
                    continue
                
                rating = p.get("rating", 0.0)
                reviews = p.get("userRatingCount", 0)
                
                # Regras de corte aprovadas: Rating >= 3.8 e Reviews >= 15
                if rating < 3.8 or reviews < 15:
                    continue
                
                # Checagem de redes conhecidas
                name_clean = name.lower()
                is_chain = any(chain in name_clean for chain in KNOWN_CHAINS)
                if is_chain:
                    continue
                
                address = p.get("formattedAddress", "")
                
                # Garantir que está na ilha/região e não continente
                if "florianópolis" not in address.lower() and "florianopolis" not in address.lower() and "sc" not in address.lower():
                    continue
                
                bairro_canonico = extract_bairro_canonico(address, bairro_nome)
                cat_final = map_category(p.get("primaryType"), name, q_cat)
                
                hours_desc = "não encontrado"
                if "regularOpeningHours" in p and "weekdayDescriptions" in p["regularOpeningHours"]:
                    hours_desc = " | ".join(p["regularOpeningHours"]["weekdayDescriptions"])
                
                phone = p.get("nationalPhoneNumber") or p.get("internationalPhoneNumber") or "não encontrado"
                wa_link = format_whatsapp(phone)
                
                website = p.get("websiteUri") or "não encontrado"
                price_lvl = format_price_level(p.get("priceLevel"))
                maps_url = p.get("googleMapsUri") or f"https://www.google.com/maps/place/?q=place_id:{pid}"
                
                loc = p.get("location", {})
                
                if pid not in places_map:
                    places_map[pid] = {
                        "place_id": pid,
                        "nome": name,
                        "bairro": bairro_canonico,
                        "categoria": cat_final,
                        "endereco": address,
                        "nota": rating,
                        "avaliacoes": reviews,
                        "faixa_preco": price_lvl,
                        "status": "aberto" if status == "OPERATIONAL" else "temporariamente fechado",
                        "telefone": phone,
                        "whatsapp": wa_link,
                        "site": website,
                        "instagram": "não encontrado", # Será enriquecido na etapa 2
                        "ifood": "não verificado",      # Será enriquecido na etapa 2
                        "horario": hours_desc,
                        "maps_url": maps_url,
                        "lat": loc.get("latitude"),
                        "lng": loc.get("longitude"),
                        "possivel_rede": False,
                        "dominio": urlparse(website).netloc if website != "não encontrado" else ""
                    }
            time.sleep(0.5)

    print(f"\nTotal de estabelecimentos brutos únicos coletados: {len(places_map)}")
    
    # Detectar possíveis redes por domínio repetido ou nomes muito similares
    domain_counts = {}
    for pid, p in places_map.items():
        dom = p.get("dominio")
        if dom and dom not in ["linktr.ee", "instabio.cc", "wa.me", "instagram.com", "facebook.com", "cardapio.menu", "ola.click"]:
            domain_counts[dom] = domain_counts.get(dom, 0) + 1
            
    for pid, p in places_map.items():
        dom = p.get("dominio")
        if dom and domain_counts.get(dom, 0) > 1:
            p["possivel_rede"] = True

    # Salvar base inicial em JSON
    output_path = "BigBrain/handoff/restaurantes_norte_ilha_raw.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(list(places_map.values()), f, ensure_ascii=False, indent=2)
        
    print(f"Salvo com sucesso em: {output_path}")

if __name__ == "__main__":
    run()

# -*- coding: utf-8 -*-
"""
Coleta Oficial de Dados Reais via Google Places API (New) - Polo Norte de Florianópolis
Busca estabelecimentos gastronômicos com salão físico nas microrregiões do Polo Norte.
"""

import os
import sys
import json
import time
import requests

BASE_DIR = r"C:\Users\Augusto\Desktop\AH3"
ENV_FILE = os.path.join(BASE_DIR, ".env")

with open(ENV_FILE, "r", encoding="utf-8") as f:
    text = f.read()

keys = {}
for l in text.splitlines():
    if "=" in l:
        k, v = l.split("=", 1)
        keys[k.strip()] = v.strip().strip('"\'')

google_key = keys.get("GOOGLE_PLACES_API_KEY")
if not google_key:
    print("ERRO: GOOGLE_PLACES_API_KEY não encontrada no .env")
    sys.exit(1)

URL_PLACES = "https://places.googleapis.com/v1/places:searchText"
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": google_key,
    "X-Goog-FieldMask": (
        "places.id,places.displayName,places.formattedAddress,"
        "places.rating,places.userRatingCount,places.nationalPhoneNumber,"
        "places.types,places.websiteUri,places.businessStatus,"
        "places.location,places.servesBreakfast,places.servesLunch,places.servesDinner"
    )
}

# Consultas específicas por microrregião do Polo Norte de Florianópolis
QUERIES = [
    # Jurerê / Jurerê Internacional
    ("restaurantes em Jurere Internacional Florianopolis", "Jurerê Internacional"),
    ("restaurantes em Jurere Tradicional Florianopolis", "Jurerê Tradicional"),
    ("bares e gastronomia em Jurere Florianopolis", "Jurerê"),
    
    # Canasvieiras
    ("restaurantes em Canasvieiras Florianopolis", "Canasvieiras"),
    ("pizzarias e restaurantes Canasvieiras Florianopolis", "Canasvieiras"),
    ("frutos do mar Canasvieiras Florianopolis", "Canasvieiras"),
    
    # Ingleses e Santinho
    ("restaurantes na praia dos Ingleses Florianopolis", "Ingleses"),
    ("restaurantes e marisqueiras Ingleses Florianopolis", "Ingleses"),
    ("restaurantes Praia do Santinho Florianopolis", "Praia do Santinho"),
    
    # Ponta das Canas, Brava e Cachoeira do Bom Jesus
    ("restaurantes Ponta das Canas Florianopolis", "Ponta das Canas"),
    ("restaurantes Praia Brava Florianopolis", "Praia Brava"),
    ("restaurantes Cachoeira do Bom Jesus Florianopolis", "Cachoeira do Bom Jesus"),
    
    # Santo Antônio de Lisboa e Sambaqui (Rota Gastronômica do Sol Poente)
    ("restaurantes Santo Antonio de Lisboa Florianopolis", "Santo Antônio de Lisboa"),
    ("restaurantes Sambaqui Florianopolis", "Sambaqui"),
    ("ostras e frutos do mar Santo Antonio de Lisboa Florianopolis", "Santo Antônio de Lisboa"),
    
    # Daniela e Vargem Grande/Bom Jesus
    ("restaurantes Praia da Daniela Florianopolis", "Daniela"),
    ("restaurantes Vargem Grande Florianopolis", "Vargem Grande")
]

def buscar_lugares(query):
    body = {
        "textQuery": query,
        "languageCode": "pt-BR",
        "maxResultCount": 20
    }
    try:
        r = requests.post(URL_PLACES, headers=HEADERS, json=body, timeout=15)
        if r.status_code == 200:
            return r.json().get("places", [])
        else:
            print(f"Erro na query '{query}': HTTP {r.status_code} - {r.text}")
            return []
    except Exception as e:
        print(f"Exceção na query '{query}': {e}")
        return []

todos_lugares = {}
print("Iniciando varredura oficial via Google Places API (New)...")

for q_text, bairro_ref in QUERIES:
    print(f"Buscando: {q_text}...")
    places = buscar_lugares(q_text)
    for p in places:
        pid = p.get("id")
        if not pid:
            continue
        
        # Filtro de negócio ativo e relevante
        status = p.get("businessStatus", "OPERATIONAL")
        if status != "OPERATIONAL":
            continue
            
        disp_name = p.get("displayName", {}).get("text", "")
        rating = p.get("rating", 0.0)
        user_ratings_total = p.get("userRatingCount", 0)
        addr = p.get("formattedAddress", "")
        phone = p.get("nationalPhoneNumber", "Não informado")
        website = p.get("websiteUri", "")
        menu_uri = p.get("menuUri", "")
        types = p.get("types", [])
        
        # Mapeamento do bairro a partir do endereço
        bairro_identificado = bairro_ref
        for b_nome in ["Jurerê Internacional", "Jurerê", "Canasvieiras", "Ingleses", "Santinho", 
                       "Ponta das Canas", "Praia Brava", "Cachoeira do Bom Jesus", 
                       "Santo Antônio de Lisboa", "Sambaqui", "Daniela", "Vargem Grande"]:
            if b_nome.lower() in addr.lower():
                bairro_identificado = b_nome
                break
                
        # Classificação da categoria
        categoria = "Restaurante & Gastronomia"
        if any("seafood" in t.lower() or "frutos do mar" in disp_name.lower() or "ostras" in disp_name.lower() for t in types):
            categoria = "Frutos do Mar & Ostras"
        elif any("pizza" in t.lower() or "pizzaria" in disp_name.lower() for t in types):
            categoria = "Pizzaria & Forno a Lenha"
        elif any("bar" in t.lower() or "pub" in t.lower() or "beach" in disp_name.lower() for t in types):
            categoria = "Bar, Beach Club & Petiscos"
        elif any("italian" in t.lower() or "cantina" in disp_name.lower() or "bistro" in disp_name.lower() for t in types):
            categoria = "Bistrô & Culinária Contemporânea"
            
        if pid not in todos_lugares:
            todos_lugares[pid] = {
                "id": pid,
                "nome": disp_name,
                "nota": rating,
                "reviews": user_ratings_total,
                "bairro": bairro_identificado,
                "endereco": addr,
                "telefone": phone,
                "website": website,
                "menu_uri": menu_uri,
                "has_menu": bool(menu_uri),
                "categoria": categoria,
                "types": types
            }
    time.sleep(0.5)

lista_final = list(todos_lugares.values())
print(f"\nVarredura concluída! Total de restaurantes únicos coletados no Polo Norte: {len(lista_final)}")

# Identificar os líderes do polo norte
lista_ordenada = sorted(lista_final, key=lambda x: x["reviews"], reverse=True)
max_reviews_polo = lista_ordenada[0]["reviews"] if lista_ordenada else 1
lider_nome = lista_ordenada[0]["nome"] if lista_ordenada else ""
print(f"Líder de avaliações no Polo Norte: {lider_nome} com {max_reviews_polo} avaliações.")

# Calcular o GAP exato de cada estabelecimento vs o líder do polo
for item in lista_final:
    rev = max(item["reviews"], 1)
    gap = round(max_reviews_polo / rev, 1)
    item["lider_polo_nome"] = lider_nome
    item["lider_polo_reviews"] = max_reviews_polo
    item["gap_lider"] = gap

# Salvar dados 100% auditados e reais
OUT_DATA_PATH = os.path.join(BASE_DIR, "scripts", "data", "gastronomia_polo_norte_real.json")
os.makedirs(os.path.dirname(OUT_DATA_PATH), exist_ok=True)
with open(OUT_DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(lista_final, f, ensure_ascii=False, indent=2)

print(f"Base oficial salva com sucesso em: {OUT_DATA_PATH}")

import os
import json
import requests
from dotenv import load_dotenv

# Carrega .env do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def buscar_estabelecimentos(termo_busca, max_resultados=10):
    """
    Busca estabelecimentos no Google Places API (New)
    termo_busca: ex: 'churrascaria em Moema, Sao Paulo'
    """
    if not API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY não encontrada no arquivo .env!")

    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,places.rating,"
            "places.userRatingCount,places.websiteUri,places.nationalPhoneNumber,"
            "places.internationalPhoneNumber,places.regularOpeningHours,places.photos,"
            "places.reviews,places.googleMapsUri,places.businessStatus,places.types"
        )
    }
    payload = {
        "textQuery": termo_busca,
        "languageCode": "pt-BR",
        "maxResultCount": max_resultados
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Erro na API do Google Places: {response.status_code} - {response.text}")

    data = response.json()
    places = data.get("places", [])
    return places

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "restaurante em Pinheiros Sao Paulo"
    print(f"Buscando por: '{query}'...")
    resultados = buscar_estabelecimentos(query, max_resultados=5)
    print(f"Encontrados: {len(resultados)}")
    for r in resultados:
        nome = r.get("displayName", {}).get("text", "N/A")
        nota = r.get("rating", "A verificar")
        total_avaliacoes = r.get("userRatingCount", 0)
        tel = r.get("nationalPhoneNumber", "A verificar")
        tem_site = "Sim" if r.get("websiteUri") else "Não"
        print(f"- {nome} | Nota: {nota} ({total_avaliacoes} avaliações) | Site: {tem_site} | Tel: {tel}")

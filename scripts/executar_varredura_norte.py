import urllib.request
import json
import os
import csv
import collections

with open('.env') as f:
    for line in f:
        if line.startswith('GOOGLE_PLACES_API_KEY='):
            api_key = line.split('=', 1)[1].strip().strip('"\'')

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': 'places.id,places.displayName,places.primaryType,places.types,places.rating,places.userRatingCount,places.businessStatus,places.formattedAddress,places.location,places.googleMapsUri,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours'
}

hubs = [
    {'name': 'Canasvieiras', 'lat': -27.4260, 'lng': -48.4550, 'radius': 2200.0},
    {'name': 'Jurerê / Jurerê Internacional', 'lat': -27.4380, 'lng': -48.5000, 'radius': 2500.0},
    {'name': 'Ingleses do Rio Vermelho', 'lat': -27.4350, 'lng': -48.3950, 'radius': 2500.0},
    {'name': 'Santinho', 'lat': -27.4650, 'lng': -48.3800, 'radius': 1800.0},
    {'name': 'Ponta das Canas / Cachoeira / Brava', 'lat': -27.4000, 'lng': -48.4250, 'radius': 2500.0},
    {'name': 'Santo Antônio de Lisboa / Sambaqui', 'lat': -27.5050, 'lng': -48.5200, 'radius': 2500.0},
    {'name': 'Vargem Grande / Ratones', 'lat': -27.4650, 'lng': -48.4750, 'radius': 3000.0},
    {'name': 'Rio Vermelho', 'lat': -27.4950, 'lng': -48.4150, 'radius': 2500.0}
]

types_list = [
    ['restaurant', 'seafood_restaurant', 'brazilian_restaurant'],
    ['pizza_restaurant', 'italian_restaurant', 'hamburger_restaurant'],
    ['bar', 'pub', 'japanese_restaurant', 'steak_house', 'barbecue_restaurant']
]

all_places = {}

for hub in hubs:
    for type_group in types_list:
        payload = {
            'includedTypes': type_group,
            'maxResultCount': 20,
            'locationRestriction': {
                'circle': {
                    'center': {'latitude': hub['lat'], 'longitude': hub['lng']},
                    'radius': hub['radius']
                }
            }
        }
        url = 'https://places.googleapis.com/v1/places:searchNearby'
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                for p in res.get('places', []):
                    pid = p.get('id')
                    if pid and pid not in all_places:
                        p['hub'] = hub['name']
                        all_places[pid] = p
        except Exception:
            pass

def categorize(p):
    types = p.get('types', [])
    name = p.get('displayName', {}).get('text', '').lower()
    
    if any(t in types for t in ['seafood_restaurant']) or any(w in name for w in ['frutos do mar', 'ostras', 'peixe', 'pescador', 'marisco']):
        return 'Frutos do Mar & Peixes'
    if any(t in types for t in ['pizza_restaurant', 'italian_restaurant']) or any(w in name for w in ['pizza', 'pizzaria', 'pasta', 'cantina', 'trattoria', 'massa']):
        return 'Pizzarias & Culinária Italiana'
    if any(t in types for t in ['steak_house', 'barbecue_restaurant']) or any(w in name for w in ['churrasco', 'churrascaria', 'costela', 'grill', 'carne', 'parrilla']):
        return 'Carnes, Churrasco & Parrilla'
    if any(t in types for t in ['hamburger_restaurant']) or any(w in name for w in ['burger', 'hamburgueria', 'hamburguer']):
        return 'Hamburguerias & Lanches'
    if any(t in types for t in ['japanese_restaurant', 'sushi_restaurant']) or any(w in name for w in ['sushi', 'japones', 'oriental', 'temaki']):
        return 'Culinária Japonesa & Asiática'
    if any(t in types for t in ['bar', 'pub']) or any(w in name for w in ['bar', 'pub', 'boteco', 'botequim', 'cervejaria', 'beer']):
        return 'Bares, Pubs & Cervejarias'
    return 'Culinária Brasileira & Contemporânea'

def audit_seo(p):
    score = 100
    gaps = []
    
    rating = p.get('rating', 0)
    reviews = p.get('userRatingCount', 0)
    website = p.get('websiteUri')
    phone = p.get('nationalPhoneNumber')
    hours = p.get('regularOpeningHours')
    
    if not website:
        score -= 25
        gaps.append('Sem Website/Link de Conversão')
    if not phone:
        score -= 15
        gaps.append('Sem Telefone Visível')
    if not hours:
        score -= 15
        gaps.append('Horários Ausentes/Incompletos')
    if reviews < 100:
        score -= 20
        gaps.append('Volume Crítico de Avaliações (<100)')
    elif reviews < 500:
        score -= 10
        gaps.append('Volume Intermediário (<500)')
    if rating < 4.3:
        score -= 20
        gaps.append(f'Nota Baixa ({rating})')
    elif rating < 4.6:
        score -= 10
        gaps.append(f'Nota Regular ({rating})')
        
    return score, gaps

# Exclusões de estabelecimentos não-restaurantes diretos (hotéis puros, shoppings, padarias puras, supermercados)
excluded_terms = ['hotel', 'pousada', 'resort', 'hostel', 'albergue', 'shopping', 'bakery', 'padaria', 'supermercado', 'supermarket', 'hipermercado', 'posto ', 'jurerê open', 'mcdonald']

valid_places = []
closed_count = 0

for p in all_places.values():
    status = p.get('businessStatus')
    if status == 'CLOSED_PERMANENTLY':
        closed_count += 1
        continue
    if status != 'OPERATIONAL':
        continue
        
    name = p.get('displayName', {}).get('text', '')
    name_lower = name.lower()
    types = p.get('types', [])
    
    if any(term in name_lower for term in excluded_terms):
        continue
    if 'lodging' in types and not any(t in types for t in ['restaurant', 'seafood_restaurant', 'bar', 'pizza_restaurant']):
        continue
        
    p['categoria'] = categorize(p)
    score, gaps = audit_seo(p)
    p['seo_score'] = score
    p['seo_gaps'] = gaps
    valid_places.append(p)

valid_places.sort(key=lambda x: x.get('userRatingCount', 0), reverse=True)

os.makedirs('BigBrain/handoff', exist_ok=True)
with open('BigBrain/handoff/varredura_norte_da_ilha_total.json', 'w', encoding='utf-8') as f:
    json.dump(valid_places, f, ensure_ascii=False, indent=2)

top10 = valid_places[:10]
csv_path = 'BigBrain/handoff/auditoria_seo_top10_norte_da_ilha.csv'
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([
        'Rank', 'Nome do Restaurante', 'Categoria', 'Região / Bairro', 
        'Nota Google', 'Qtd Avaliações', 'Score SEO (0-100)', 
        'Website / Link Direto', 'Telefone', 'Gargalos Críticos de SEO Local'
    ])
    for idx, p in enumerate(top10, 1):
        writer.writerow([
            f'{idx}º',
            p.get('displayName', {}).get('text'),
            p.get('categoria'),
            p.get('hub'),
            p.get('rating', 'N/D'),
            p.get('userRatingCount', 0),
            f"{p.get('seo_score')}/100",
            'Sim' if p.get('websiteUri') else 'Não',
            'Sim' if p.get('nationalPhoneNumber') else 'Não',
            ', '.join(p.get('seo_gaps')) if p.get('seo_gaps') else 'Perfil Robusto'
        ])

cat_counts = collections.Counter(p['categoria'] for p in valid_places)
print(f"TOTAL_VALIDOS: {len(valid_places)}")
print(f"CATEGORIAS: {json.dumps(cat_counts, ensure_ascii=False)}")
print("\nTOP 10:")
for idx, p in enumerate(top10, 1):
    print(f"{idx}. {p.get('displayName', {}).get('text')} | {p.get('categoria')} | {p.get('hub')} | Nota: {p.get('rating')} | Avaliações: {p.get('userRatingCount')} | Score: {p.get('seo_score')}/100")

import os
import math
import json
import requests
from dotenv import load_dotenv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_PLACES_API_KEY não encontrada no .env!")

def haversine(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return 999.0
    R = 6371.0 # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def buscar_places(query, max_res=20):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,places.rating,"
            "places.userRatingCount,places.websiteUri,places.nationalPhoneNumber,"
            "places.regularOpeningHours,places.businessStatus,places.types,"
            "places.location,places.primaryType,places.primaryTypeDisplayName"
        )
    }
    payload = {
        "textQuery": query,
        "languageCode": "pt-BR",
        "maxResultCount": max_res
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        print(f"Erro API: {resp.status_code} - {resp.text}")
        return []
    return resp.json().get("places", [])

def eh_estabelecimento_gastronomico(p):
    types = set(p.get("types", []))
    primary = p.get("primaryType", "")
    
    valid_types = {
        "restaurant", "food", "bar", "meal_takeaway", "cafe", "bakery",
        "seafood_restaurant", "pizza_restaurant", "hamburger_restaurant",
        "barbecue_restaurant", "steak_house", "sushi_restaurant",
        "japanese_restaurant", "italian_restaurant", "brazilian_restaurant",
        "buffet_restaurant", "fast_food_restaurant", "meal_delivery",
        "ice_cream_shop", "pub", "bistro", "diner"
    }
    
    invalid_types = {
        "natural_feature", "beach", "tourist_attraction", "park",
        "lodging", "hotel", "campground", "real_estate_agency"
    }
    
    if any(t in invalid_types for t in types) and not any(t in valid_types for t in types):
        return False
        
    if primary in invalid_types:
        return False
        
    return bool(types.intersection(valid_types))

def extrair_turno(opening_hours):
    if not opening_hours:
        return "Geral / Não informado"
    periods = opening_hours.get("periods", [])
    if not periods:
        return "Geral"
    tem_almoco = False
    tem_jantar = False
    for p in periods:
        open_time = p.get("open", {}).get("hour", 0)
        close_time = p.get("close", {}).get("hour", 0)
        if open_time < 16 or (close_time > 11 and close_time <= 17):
            tem_almoco = True
        if open_time >= 17 or close_time > 20 or close_time < 6:
            tem_jantar = True
    if tem_almoco and tem_jantar:
        return "Almoço e Jantar"
    elif tem_almoco:
        return "Almoço"
    elif tem_jantar:
        return "Jantar / Noturno"
    return "Geral"

def extrair_nicho(types, display_nicho, nome):
    # Tipos comuns para nicho
    mapa_nicho = {
        "seafood_restaurant": "Frutos do Mar",
        "pizza_restaurant": "Pizzaria",
        "pizzeria": "Pizzaria",
        "hamburger_restaurant": "Hamburgueria",
        "barbecue_restaurant": "Churrascaria / Carnes",
        "steak_house": "Churrascaria / Carnes",
        "sushi_restaurant": "Japonês / Sushi",
        "japanese_restaurant": "Japonês / Sushi",
        "italian_restaurant": "Italiano / Massas",
        "buffet_restaurant": "Buffet / Por Quilo",
        "bar_and_grill": "Bar & Petiscaria",
        "bar": "Bar / Petiscaria",
        "cafe": "Café / Padaria",
        "bakery": "Padaria / Café",
        "ice_cream_shop": "Sorveteria / Sobremesas"
    }
    if display_nicho and isinstance(display_nicho, dict):
        txt = display_nicho.get("text")
        if txt and txt.lower() not in ["restaurante", "restaurant"]:
            return txt
            
    for t in types or []:
        if t in mapa_nicho:
            return mapa_nicho[t]
            
    nome_lower = (nome or "").lower()
    if any(k in nome_lower for k in ["peixe", "mar", "pescador", "frutos do mar", "camarão", "lagoinha", "ostra"]):
        return "Frutos do Mar"
    if any(k in nome_lower for k in ["pizza", "pizzaria", "forno"]):
        return "Pizzaria"
    if any(k in nome_lower for k in ["burger", "burguer", "hamburguer", "lanche"]):
        return "Hamburgueria / Lanches"
    if any(k in nome_lower for k in ["grill", "churrasco", "churrascaria", "costela", "carne"]):
        return "Churrascaria / Carnes"
    if any(k in nome_lower for k in ["sushi", "japa", "oriental"]):
        return "Japonês / Sushi"
    if any(k in nome_lower for k in ["bar", "pub", "choperia", "petisc"]):
        return "Bar & Petiscaria"
        
    return "Restaurante Geral"

def main():
    print("[*] Coletando restaurantes em Ponta das Canas e arredores (Cachoeira, Brava, Canasvieiras)...")
    
    # 1. Buscar restaurantes alvo em Ponta das Canas
    alvos_raw = buscar_places("restaurante em Ponta das Canas Florianopolis", max_res=20)
    alvos_raw_2 = buscar_places("restaurante bar frutos do mar Ponta das Canas", max_res=20)
    
    # Pool de alvos únicos
    alvos_dict = {}
    for p in alvos_raw + alvos_raw_2:
        pid = p.get("id")
        status = p.get("businessStatus", "OPERATIONAL")
        # Regra 1: Ativo obrigatório + Estabelecimento gastronômico
        if pid and pid not in alvos_dict and status == "OPERATIONAL" and eh_estabelecimento_gastronomico(p):
            alvos_dict[pid] = p
            
    print(f"[✓] {len(alvos_dict)} estabelecimentos ativos encontrados em Ponta das Canas.")
    
    # 2. Buscar pool de estabelecimentos gastronômicos regionais (Ponta das Canas, Lagoinha do Norte, Praia Brava, Cachoeira)
    pool_raw = []
    buscas = [
        "restaurantes Ponta das Canas Florianopolis",
        "restaurante Praia da Lagoinha Florianopolis",
        "restaurante Lagoinha do Norte Florianopolis",
        "restaurantes Cachoeira do Bom Jesus Florianopolis",
        "restaurantes Praia Brava Florianopolis"
    ]
    for b in buscas:
        pool_raw.extend(buscar_places(b, max_res=20))
        
    pool_dict = {}
    for p in pool_raw:
        pid = p.get("id")
        status = p.get("businessStatus", "OPERATIONAL")
        if pid and pid not in pool_dict and status == "OPERATIONAL" and eh_estabelecimento_gastronomico(p):
            pool_dict[pid] = p
            
    print(f"[✓] Pool regional consolidado: {len(pool_dict)} estabelecimentos gastronômicos operacionais.")
    
    # Processar cada restaurante e achar seus 5 concorrentes mais próximos
    lista_final = []
    
    for pid, alvo in alvos_dict.items():
        nome_alvo = alvo.get("displayName", {}).get("text", "Sem Nome")
        loc_alvo = alvo.get("location", {})
        lat_a = loc_alvo.get("latitude")
        lon_a = loc_alvo.get("longitude")
        types_a = alvo.get("types", [])
        p_nicho = alvo.get("primaryTypeDisplayName")
        nicho_alvo = extrair_nicho(types_a, p_nicho, nome_alvo)
        turno_alvo = extrair_turno(alvo.get("regularOpeningHours"))
        nota_alvo = alvo.get("rating", 0)
        reviews_alvo = alvo.get("userRatingCount", 0)
        tel_alvo = alvo.get("nationalPhoneNumber", "Não informado")
        canal_alvo = "Sim" if alvo.get("websiteUri") else "Ausente"
        endereco_alvo = alvo.get("formattedAddress", "")
        
        # Filtrar e ranquear concorrentes por PROXIMIDADE GEOGRÁFICA
        candidatos = []
        for c_id, conc in pool_dict.items():
            if c_id == pid:
                continue # não concorre consigo mesmo
                
            nome_c = conc.get("displayName", {}).get("text", "Sem Nome")
            loc_c = conc.get("location", {})
            dist_km = haversine(lat_a, lon_a, loc_c.get("latitude"), loc_c.get("longitude"))
            
            types_c = conc.get("types", [])
            p_nicho_c = conc.get("primaryTypeDisplayName")
            nicho_c = extrair_nicho(types_c, p_nicho_c, nome_c)
            turno_c = extrair_turno(conc.get("regularOpeningHours"))
            nota_c = conc.get("rating", 0)
            reviews_c = conc.get("userRatingCount", 0)
            canal_c = "Sim" if conc.get("websiteUri") else "Ausente"
            endereco_c = conc.get("formattedAddress", "")
            
            candidatos.append({
                "id": c_id,
                "nome": nome_c,
                "nicho": nicho_c,
                "turno": turno_c,
                "dist_km": dist_km,
                "nota": nota_c,
                "reviews": reviews_c,
                "canal": canal_c,
                "endereco": endereco_c
            })
            
        # CRITÉRIO SOBERANO: Proximidade geográfica (menor distância em km). Desempate por reviews.
        candidatos.sort(key=lambda c: (c["dist_km"], -c["reviews"]))
        top5 = candidatos[:5]
        
        lista_final.append({
            "alvo": {
                "nome": nome_alvo,
                "nicho": nicho_alvo,
                "turno": turno_alvo,
                "nota": nota_alvo,
                "reviews": reviews_alvo,
                "canal": canal_alvo,
                "telefone": tel_alvo,
                "endereco": endereco_alvo
            },
            "concorrentes": top5
        })
        
    print(f"[✓] Processamento concluído para {len(lista_final)} restaurantes.")
    
    # 3. Gerar Excel elegante
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Benchmarking Ponta das Canas"
    ws.views.sheetView[0].showGridLines = True
    
    # Estilos
    f_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    f_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    f_alvo_title = Font(name="Segoe UI", size=11, bold=True, color="0F172A")
    f_alvo_data = Font(name="Segoe UI", size=10, bold=True, color="991B1B")
    f_conc_pos = Font(name="Segoe UI", size=9, bold=True, color="2563EB")
    f_regular = Font(name="Segoe UI", size=9, color="334155")
    f_bold = Font(name="Segoe UI", size=9, bold=True, color="1E293B")
    
    fill_dark = PatternFill(start_color="090D16", end_color="090D16", fill_type="solid")
    fill_blue_head = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_alvo_head = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    fill_alvo_row = PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid")
    fill_conc_row = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    fill_conc_alt = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )
    
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    
    # Título Geral
    ws.merge_cells("A1:G1")
    ws["A1"] = "MAPEAMENTO DE RESTAURANTES & TOP 5 CONCORRENTES LOCAIS • PONTA DAS CANAS / FLORIANÓPOLIS"
    ws["A1"].font = f_title
    ws["A1"].fill = fill_dark
    ws["A1"].alignment = align_center
    ws.row_dimensions[1].height = 35
    
    row_idx = 3
    
    for item in lista_final:
        alvo = item["alvo"]
        concs = item["concorrentes"]
        
        # Cabeçalho do Bloco do Alvo
        ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=7)
        ws.cell(row=row_idx, column=1, value=f"🎯 RESTAURANTE AUDITADO: {alvo['nome']}  |  Nicho: {alvo['nicho']}  |  Turno: {alvo['turno']}").font = f_alvo_title
        ws.cell(row=row_idx, column=1).fill = fill_alvo_head
        ws.cell(row=row_idx, column=1).alignment = align_left
        ws.row_dimensions[row_idx].height = 24
        row_idx += 1
        
        # Cabeçalho das Colunas
        headers = ["Tipo / Posição", "Nome do Estabelecimento", "Nicho Culinário", "Distância", "Nota Google", "Avaliações", "Canal Direto"]
        for col_idx, h in enumerate(headers, 1):
            c = ws.cell(row=row_idx, column=col_idx, value=h)
            c.font = f_header
            c.fill = fill_blue_head
            c.alignment = align_center if col_idx not in [2, 3] else align_left
            c.border = thin_border
        ws.row_dimensions[row_idx].height = 20
        row_idx += 1
        
        # Linha do ALVO
        alvo_row = [
            "• ALVO",
            alvo["nome"],
            alvo["nicho"],
            "Local",
            f"{alvo['nota']} ★",
            alvo["reviews"],
            alvo["canal"]
        ]
        for col_idx, val in enumerate(alvo_row, 1):
            c = ws.cell(row=row_idx, column=col_idx, value=val)
            c.font = f_alvo_data
            c.fill = fill_alvo_row
            c.alignment = align_center if col_idx not in [2, 3] else align_left
            c.border = thin_border
        ws.row_dimensions[row_idx].height = 19
        row_idx += 1
        
        # Linhas dos 5 Concorrentes
        for rank, c_item in enumerate(concs, 1):
            conc_row = [
                f"#{rank} Concorrente",
                c_item["nome"],
                c_item["nicho"],
                f"{c_item['dist_km']} km",
                f"{c_item['nota']} ★",
                c_item["reviews"],
                c_item["canal"]
            ]
            fill_curr = fill_conc_row if rank % 2 != 0 else fill_conc_alt
            for col_idx, val in enumerate(conc_row, 1):
                c = ws.cell(row=row_idx, column=col_idx, value=val)
                c.font = f_conc_pos if col_idx == 1 else (f_bold if col_idx in [2, 5] else f_regular)
                c.fill = fill_curr
                c.alignment = align_center if col_idx not in [2, 3] else align_left
                c.border = thin_border
            ws.row_dimensions[row_idx].height = 18
            row_idx += 1
            
        # Espaçamento entre restaurantes
        row_idx += 1
        
    # Ajuste de largura das colunas
    col_widths = {1: 18, 2: 38, 3: 25, 4: 14, 5: 14, 6: 15, 7: 16}
    for col_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = w
        
    caminho_xlsx = os.path.join(BASE_DIR, "saida", "Benchmarking_Ponta_das_Canas.xlsx")
    wb.save(caminho_xlsx)
    print(f"[✓] Arquivo Excel salvo com sucesso em: {caminho_xlsx}")

if __name__ == "__main__":
    main()

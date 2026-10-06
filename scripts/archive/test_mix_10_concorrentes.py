import os, math, requests, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from dotenv import load_dotenv

load_dotenv("C:/Users/Augusto/Desktop/AH3/.env")
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def haversine(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2): return 999.0
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)), 2)

def buscar_places(query, max_res=20):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.location,places.businessStatus,places.types,places.primaryTypeDisplayName,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours"
    }
    payload = {"textQuery": query, "languageCode": "pt-BR", "maxResultCount": max_res}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        return r.json().get("places", [])
    return []

def eh_restaurante_relevante(p):
    types = set(p.get("types", []))
    nome = p.get("displayName", {}).get("text", "")
    
    # Exclusão estrita de entidades geográficas e hotelaria sem restaurante
    if any(inv in types for inv in ["natural_feature", "beach", "lodging", "hotel", "tourist_attraction", "campground"]):
        if not any(t in types for t in ["restaurant", "bar", "seafood_restaurant"]):
            return False
        if any(b in nome for b in ["Praia Ponta das Canas", "Praia da Lagoinha", "Praia Brava"]):
            return False
            
    # Exclusão de padarias / cafés / confeitarias puras (não concorrem na refeição principal)
    if ("bakery" in types or "cafe" in types) and not any(t in types for t in ["restaurant", "bar", "seafood_restaurant"]):
        return False
        
    return bool(types.intersection({"restaurant", "food", "bar", "pub", "bistro", "seafood_restaurant"}))

def classificar_proposta(nome, types, primary_type):
    nome_lower = nome.lower()
    if any(k in nome_lower for k in ["peixe", "maré", "mare", "lula", "pescador", "garra", "canto", "rancho", "chico", "marquinho", "baleia", "marinheiro", "frutos do mar", "ocean", "ponta da praia"]) or "seafood_restaurant" in types:
        return "Direto (Frutos do Mar / Praia)"
    elif any(k in nome_lower for k in ["burger", "burguer", "hamburguer"]):
        return "Cross-Nicho (Hamburgueria)"
    elif any(k in nome_lower for k in ["pizza", "pizzaria", "cantina", "italiano"]):
        return "Cross-Nicho (Italiano / Pizza)"
    elif any(k in nome_lower for k in ["beer", "choperia", "bar", "pub", "toca", "boteco"]):
        return "Cross-Nicho (Bar / Choperia)"
    elif any(k in nome_lower for k in ["campeira", "assadão", "carne", "churrasco"]):
        return "Cross-Nicho (Carnes / Campeiro)"
    return "Cross-Nicho (Restaurante Geral)"

def main():
    print("[*] Iniciando teste de mix de 10 concorrentes (Diretos + Cross-Nicho)...")
    
    # 1. Alvos de Ponta das Canas
    alvos_raw = buscar_places("restaurantes Ponta das Canas Florianopolis", max_res=20)
    alvos = {}
    for p in alvos_raw:
        pid = p.get("id")
        if pid and pid not in alvos and p.get("businessStatus") == "OPERATIONAL" and eh_restaurante_relevante(p):
            alvos[pid] = p
            
    # 2. Pool Regional
    buscas = [
        "restaurantes Ponta das Canas Florianopolis",
        "restaurantes Praia da Lagoinha Florianopolis",
        "restaurantes Lagoinha do Norte Florianopolis",
        "restaurantes Cachoeira do Bom Jesus Florianopolis",
        "restaurantes Praia Brava Florianopolis"
    ]
    pool = {}
    for b in buscas:
        for p in buscar_places(b, max_res=20):
            pid = p.get("id")
            if pid and pid not in pool and p.get("businessStatus") == "OPERATIONAL" and eh_restaurante_relevante(p):
                pool[pid] = p
                
    print(f"[✓] {len(alvos)} alvos mapeados. Pool regional: {len(pool)} locais operacionais.")
    
    # Processar cada alvo para Top 10 (Mix Direto + Cross-Nicho)
    dados_processados = []
    
    for pid, alvo in alvos.items():
        nome_alvo = alvo.get("displayName", {}).get("text", "Sem Nome")
        lat_a = alvo.get("location", {}).get("latitude")
        lon_a = alvo.get("location", {}).get("longitude")
        tipo_alvo = classificar_proposta(nome_alvo, alvo.get("types", []), alvo.get("primaryTypeDisplayName"))
        
        candidatos = []
        for c_id, conc in pool.items():
            if c_id == pid: continue
            nome_c = conc.get("displayName", {}).get("text", "Sem Nome")
            lat_c = conc.get("location", {}).get("latitude")
            lon_c = conc.get("location", {}).get("longitude")
            dist = haversine(lat_a, lon_a, lat_c, lon_c)
            tipo_c = classificar_proposta(nome_c, conc.get("types", []), conc.get("primaryTypeDisplayName"))
            
            is_direto = "Direto" in tipo_c
            candidatos.append({
                "nome": nome_c,
                "tipo": tipo_c,
                "is_direto": is_direto,
                "dist": dist,
                "rating": conc.get("rating", 0),
                "reviews": conc.get("userRatingCount", 0),
                "canal": "Sim" if conc.get("websiteUri") else "Ausente",
                "endereco": conc.get("formattedAddress", "")
            })
            
        # Selecionar Top 6 Diretos (mais próximos) + Top 4 Cross-Nicho (líderes de atração da microrregião)
        diretos = [c for c in candidatos if c["is_direto"]]
        diretos.sort(key=lambda x: x["dist"])
        
        cross = [c for c in candidatos if not c["is_direto"]]
        cross.sort(key=lambda x: (x["dist"], -x["reviews"]))
        
        # Montar os 10 do Mix
        selecionados = diretos[:6] + cross[:4]
        # Ordenar por proximidade no resultado final
        selecionados.sort(key=lambda x: (x["dist"], -x["reviews"]))
        
        dados_processados.append({
            "alvo": {
                "nome": nome_alvo,
                "tipo": tipo_alvo,
                "rating": alvo.get("rating", 0),
                "reviews": alvo.get("userRatingCount", 0),
                "canal": "Sim" if alvo.get("websiteUri") else "Ausente",
                "telefone": alvo.get("nationalPhoneNumber", "Não informado")
            },
            "concorrentes": selecionados
        })
        
    # Gerar Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Mix 10 Concorrentes"
    ws.views.sheetView[0].showGridLines = True
    
    # Estilos
    f_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    f_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    f_sec = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    f_alvo = Font(name="Segoe UI", size=10, bold=True, color="7F1D1D")
    f_regular = Font(name="Segoe UI", size=10, color="1E293B")
    
    fill_title = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    fill_sec = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    fill_header = PatternFill(start_color="475569", end_color="475569", fill_type="solid")
    fill_alvo = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    fill_direto = PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid")
    fill_alt = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0")
    )
    
    # Título Principal
    ws.merge_cells("A1:G1")
    t_cell = ws["A1"]
    t_cell.value = "BENCHMARKING HIPERLOCAL: MIX DE 10 CONCORRENTES (DIRETOS + POLOS REGIONAIS)"
    t_cell.font = f_title
    t_cell.fill = fill_title
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 36
    
    curr = 3
    for bloco in dados_processados:
        alvo = bloco["alvo"]
        
        # Cabeçalho do Bloco Alvo
        ws.merge_cells(f"A{curr}:G{curr}")
        s_cell = ws[f"A{curr}"]
        s_cell.value = f"🎯 RESTAURANTE AUDITADO: {alvo['nome']}  |  Classificação: {alvo['tipo']}  |  Tel: {alvo['telefone']}"
        s_cell.font = f_sec
        s_cell.fill = fill_sec
        s_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[curr].height = 26
        curr += 1
        
        # Cabeçalhos da Tabela
        headers = ["Posição / Tipo", "Nome do Estabelecimento", "Proposta / Categoria", "Distância", "Nota Google", "Avaliações", "Canal Direto"]
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=curr, column=col_idx)
            cell.value = h
            cell.font = f_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
        ws.row_dimensions[curr].height = 22
        curr += 1
        
        # Linha do Alvo
        row_alvo = [
            "• ALVO",
            alvo["nome"],
            alvo["tipo"],
            "Local",
            f"{alvo['rating']:.1f} ★",
            alvo["reviews"],
            alvo["canal"]
        ]
        for col_idx, val in enumerate(row_alvo, 1):
            cell = ws.cell(row=curr, column=col_idx)
            cell.value = val
            cell.font = f_alvo
            cell.fill = fill_alvo
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if col_idx in [1,4,5,6,7] else "left", vertical="center")
        ws.row_dimensions[curr].height = 20
        curr += 1
        
        # Linhas dos 10 Concorrentes
        for idx, conc in enumerate(bloco["concorrentes"], 1):
            row_conc = [
                f"#{idx:02d} Concorrente",
                conc["nome"],
                conc["tipo"],
                f"{conc['dist']:.2f} km",
                f"{conc['rating']:.1f} ★",
                conc["reviews"],
                conc["canal"]
            ]
            fill_row = fill_direto if conc["is_direto"] else (fill_alt if idx % 2 == 0 else PatternFill(fill_type=None))
            for col_idx, val in enumerate(row_conc, 1):
                cell = ws.cell(row=curr, column=col_idx)
                cell.value = val
                cell.font = f_regular
                if fill_row.fill_type:
                    cell.fill = fill_row
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center" if col_idx in [1,4,5,6,7] else "left", vertical="center")
            ws.row_dimensions[curr].height = 18
            curr += 1
            
        curr += 2 # Espaçamento entre blocos
        
    # Ajuste de larguras
    larguras = {"A": 18, "B": 42, "C": 32, "D": 14, "E": 14, "F": 14, "G": 14}
    for col, w in larguras.items():
        ws.column_dimensions[col].width = w
        
    out_path = "C:/Users/Augusto/Desktop/AH3/saida/Benchmarking_Mix_10_Ponta_das_Canas.xlsx"
    wb.save(out_path)
    print(f"[✓] Arquivo salvo: {out_path}")

if __name__ == "__main__":
    main()

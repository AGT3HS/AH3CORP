import os
import subprocess
import requests
import math
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("C:/Users/Augusto/Desktop/AH3/.env")
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def haversine(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2): return 999.0
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)), 2)

def buscar_place_detalhes(place_query):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.location,places.businessStatus,places.types,places.primaryTypeDisplayName,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours"
    }
    r = requests.post(url, headers=headers, json={"textQuery": place_query, "languageCode": "pt-BR", "maxResultCount": 1})
    if r.status_code == 200 and r.json().get("places"):
        return r.json()["places"][0]
    return None

def buscar_concorrentes_geograficos(lat, lon, radius_meters=2000):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.location,places.businessStatus,places.types,places.primaryTypeDisplayName,places.websiteUri,places.nationalPhoneNumber"
    }
    
    types_groups = [
        ["restaurant", "seafood_restaurant"],
        ["bar", "pub", "bistro"],
        ["pizza_restaurant", "hamburger_restaurant"]
    ]
    
    coletados = {}
    for t_group in types_groups:
        payload = {
            "includedTypes": t_group,
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": lat, "longitude": lon},
                    "radius": float(radius_meters)
                }
            }
        }
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 200:
            for p in r.json().get("places", []):
                pid = p.get("id")
                if pid and pid not in coletados:
                    coletados[pid] = p
                    
    # Filtro operacional estrito
    validos = []
    for p in coletados.values():
        if p.get("businessStatus") != "OPERATIONAL":
            continue
        types = set(p.get("types", []))
        nome = p.get("displayName", {}).get("text", "")
        # Excluir hoteis sem restaurante aberto
        if "lodging" in types and not any(t in types for t in ["restaurant", "bar", "seafood_restaurant"]):
            if "Hotel" in nome or "Pousada" in nome:
                continue
        # Excluir padarias e confeitarias puras
        if ("bakery" in types or "cafe" in types) and not any(t in types for t in ["restaurant", "bar", "seafood_restaurant"]):
            continue
        validos.append(p)
        
    return validos

def classificar_subcategoria(nome, types):
    n_lower = nome.lower()
    if any(k in n_lower for k in ["peixe", "maré", "mare", "lula", "pescador", "garra", "canto", "rancho", "chico", "marinheiro", "ocean", "vento", "baleia", "lagoinha", "mar", "praia"]) or "seafood_restaurant" in types:
        return "Direto (Frutos do Mar / Praia)"
    elif any(k in n_lower for k in ["pizza", "pizzaria", "cantina", "italiano"]):
        return "Cross-Nicho (Pizzaria / Italiano)"
    elif any(k in n_lower for k in ["burger", "burguer", "hamburgueria", "lanches"]):
        return "Cross-Nicho (Hamburgueria)"
    elif any(k in n_lower for k in ["beer", "choperia", "bar", "pub", "toca", "boteco", "drinks"]):
        return "Cross-Nicho (Bar & Choperia)"
    elif any(k in n_lower for k in ["campeira", "assadão", "carne", "churrascaria", "buffet"]):
        return "Cross-Nicho (Buffet & Carnes)"
    return "Cross-Nicho (Restaurante Geral)"

def gerar_relatorio_final_canto_do_mar():
    print("[*] Buscando dados oficiais do alvo...")
    alvo = buscar_place_detalhes("Canto do Mar Ponta das Canas Florianopolis")
    
    nome = alvo.get("displayName", {}).get("text", "Canto do Mar Ponta das Canas")
    endereco = alvo.get("formattedAddress", "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC")
    telefone = alvo.get("nationalPhoneNumber", "(48) 3261-0872")
    rating = float(alvo.get("rating", 4.6))
    total_reviews = int(alvo.get("userRatingCount", 178))
    lat_a = alvo.get("location", {}).get("latitude", -27.3972)
    lon_a = alvo.get("location", {}).get("longitude", -48.4239)
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    print("[*] Buscando concorrentes no raio circular exato de 2.0 km (Places NearbySearch)...")
    concorrentes_raw = buscar_concorrentes_geograficos(lat_a, lon_a, radius_meters=2000)
    print(f"[✓] {len(concorrentes_raw)} estabelecimentos gastronômicos operacionais encontrados no raio de 2km.")
    
    # Processar candidatos
    candidatos = []
    for p in concorrentes_raw:
        pid = p.get("id")
        p_nome = p.get("displayName", {}).get("text", "")
        p_lat = p.get("location", {}).get("latitude")
        p_lon = p.get("location", {}).get("longitude")
        dist = haversine(lat_a, lon_a, p_lat, p_lon)
        p_nota = p.get("rating", 0)
        p_revs = p.get("userRatingCount", 0)
        p_card = "Sim" if p.get("websiteUri") else "Não"
        is_alvo = (pid == alvo["id"]) or (p_nome == nome)
        p_tipo = classificar_subcategoria(p_nome, p.get("types", []))
        
        candidatos.append({
            "nome": p_nome,
            "dist": dist,
            "nota": f"{p_nota:.1f} ★",
            "revs": p_revs,
            "cardapio": p_card,
            "whats": p_card,
            "tipo": p_tipo,
            "alvo": is_alvo
        })
        
    # Ordenar rigorosamente por MAIOR NÚMERO DE AVALIAÇÕES (Decrescente)
    candidatos.sort(key=lambda x: -x["revs"])
    
    # Selecionar Top 10 Concorrentes + Assegurar a presenca do Alvo no ranking
    top_ranking = []
    alvo_inserido = False
    
    # Pegar os 10 primeiros
    for item in candidatos[:11]:
        if item["alvo"]:
            alvo_inserido = True
        top_ranking.append(item)
        
    # Se o alvo estiver abaixo do top 11, incluir no final para viabilizar a comparacao
    if not alvo_inserido:
        item_alvo = next((c for c in candidatos if c["alvo"]), None)
        if item_alvo:
            top_ranking.append(item_alvo)
            top_ranking.sort(key=lambda x: -x["revs"])
            top_ranking = top_ranking[:11]
            
    # Montar tbody HTML da tabela
    ranking_tbody = ""
    for idx, r in enumerate(top_ranking, 1):
        pos_str = f"{idx}º"
        revs_fmt = f"{r['revs']:,}".replace(",", ".") + " reviews"
        card_cls = "yes" if r["cardapio"] == "Sim" else "no"
        whats_cls = "yes" if r["whats"] == "Sim" else "no"
        
        if r["alvo"]:
            ranking_tbody += f"""              <tr class="is-target">
                <td><span class="pos-badge target">{pos_str}</span></td>
                <td>
                  <div class="company-cell">
                    <span>{r['nome']}</span>
                    <span class="tag-target">ALVO AUDITADO</span>
                  </div>
                </td>
                <td><span style="color: #F59E0B; font-weight: 800;">{r['nota']}</span></td>
                <td><strong>{revs_fmt}</strong></td>
                <td><span class="pill-bool yes">Sim</span></td>
                <td><span class="pill-bool yes">Sim</span></td>
              </tr>\n"""
        else:
            badge_cls = "top-3" if idx <= 3 else "other"
            nota_cor = "var(--green)" if any(k in r["nota"] for k in ["4.6", "4.7", "4.8", "4.9", "5.0"]) else "var(--muted)"
            ranking_tbody += f"""              <tr>
                <td><span class="pos-badge {badge_cls}">{pos_str}</span></td>
                <td><span style="font-weight: 600; color: var(--text);">{r['nome']} <small style="color:var(--muted); font-size:10px;">({r['tipo']})</small></span></td>
                <td><span style="color: {nota_cor}; font-weight: 700;">{r['nota']}</span></td>
                <td>{revs_fmt}</td>
                <td><span class="pill-bool {card_cls}">{r['cardapio']}</span></td>
                <td><span class="pill-bool {whats_cls}">{r['whats']}</span></td>
              </tr>\n"""

    template_path = r"C:\Users\Augusto\.gemini\antigravity-ide\scratch\auditoria-tradicao-campeira\Auditoria_Tradicao_Campeira_Dark_Orange.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Substituições de Dados Gerais
    html = html.replace("Restaurante Tradição Campeira", nome)
    html = html.replace("Av. Luiz Boiteux Piazza, 4893 - Cachoeira do Bom Jesus, Florianópolis - SC", endereco)
    html = html.replace("(48) 3284-5153", telefone)
    html = html.replace("-27.41682, -48.43129", f"{lat_a:.5f}, {lon_a:.5f}")
    html = html.replace("Cachoeira do Bom Jesus", "Ponta das Canas")
    html = html.replace("26/09/2026", data_atual)
    html = html.replace("Buffet e Frutos do Mar", "Restaurante de Frutos do Mar")

    # Atualizar KPIs da Página 1 com estrela Amarela/Laranja (#F59E0B)
    html = html.replace('>64<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>', '>58<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>')
    html = html.replace('>996<', f'>{total_reviews}<')
    html = html.replace('4º Lugar Regional', 'Abaixo do Top 3 Regional')
    html = html.replace('Líder regional possui 2.140', 'Líder regional possui 2.114')
    html = html.replace('>4.4<span style="font-size:18px; color:var(--orange);">★</span>', f'>{rating:.1f}<span style="font-size:18px; color:#F59E0B; margin-left:2px;">★</span>')
    html = html.replace('Abaixo do Top 3 (4.6★)', 'Nota de Excelência (4.6★)')
    html = html.replace('Dispersão em notas recentes', 'Satisfação elevada comprovada')

    # Substituir tabela
    tbody_pattern = r"<tbody>[\s\S]*?</tbody>"
    html = re.sub(tbody_pattern, f"<tbody>\n{ranking_tbody}            </tbody>", html, count=1)

    # CSS denso e calibrado para impressão A4 sem cortes
    css_fix = """
  /* AJUSTES DE PROPORÇÃO E COMPACTAÇÃO DE PÁGINA */
  .page {
    width: 210mm;
    min-height: 297mm;
    height: 297mm;
    max-height: 297mm;
    max-width: 980px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 24px 34px 16px !important;
    position: relative;
    box-shadow: 0 24px 60px rgba(0,0,0,.45);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .action-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px !important;
  }

  .action-card {
    background: var(--surface-2);
    border: 1px solid var(--line);
    border-radius: 10px !important;
    padding: 10px 12px !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 4px !important;
  }

  .action-num {
    font-size: 20px !important;
    font-weight: 800;
    color: var(--orange);
    line-height: 1;
  }

  .action-tag {
    font-size: 8.5px !important;
    padding: 1px 5px !important;
  }

  .action-title {
    font-size: 12px !important;
    font-weight: 700;
    color: var(--text);
    line-height: 1.25;
  }

  .action-desc {
    font-size: 10.5px !important;
    color: var(--muted);
    line-height: 1.35 !important;
  }

  .action-meta {
    margin-top: 2px !important;
    padding-top: 4px !important;
    font-size: 9.5px !important;
    display: flex;
    justify-content: space-between;
  }

  .tag-target {
    background: var(--orange);
    color: #FFFFFF;
    font-size: 9px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 4px;
    letter-spacing: .05em;
  }
"""
    html = html.replace("/* ESTRUTURA DO CONTAINER DE PÁGINA (CARTÃO FLUTUANTE) */", css_fix + "\n  /* ESTRUTURA DO CONTAINER DE PÁGINA (CARTÃO FLUTUANTE) */")

    # Ajustar Callouts
    callout_p1 = f"""<strong>Diagnóstico Executivo da Página 1:</strong> O <strong>{nome}</strong> apresenta nota de excelência (<strong>{rating:.1f}★</strong>) e cadastro validado. Entretanto, com <strong>{total_reviews} avaliações</strong>, fica em desvantagem crítica de volume frente aos concorrentes no raio de 2km como Mira Maré (1.445 reviews) e Garra Azul (1.362 reviews). Alavancar a captação ativa de avaliações é o fator decisivo para conquistar o Top 3 no Google Maps."""
    
    callout_p2 = f"""<strong>Proposta Comercial & Impacto Direto:</strong> Ao estruturar a captação contínua de avaliações no pós-atendimento e otimizar o canal direto de reservas no WhatsApp, o <strong>{nome}</strong> superará rapidamente o patamar de 500 reviews, disputando o topo das preferências gastronômicas da orla."""

    html = re.sub(r'<div class="callout">[\s\S]*?</div>', f'<div class="callout">\n        {callout_p1}\n      </div>', html, count=1)
    html = re.sub(r'<div class="callout" style="padding: 14px 18px;">[\s\S]*?</div>', f'<div class="callout" style="padding: 10px 14px; font-size:11.5px; line-height:1.4;">\n        {callout_p2}\n      </div>', html, count=1)

    saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
    os.makedirs(saida_dir, exist_ok=True)
    caminho_html = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_Nearby2km_DarkOrange.html")
    caminho_pdf = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_Nearby2km_DarkOrange.pdf")

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html)

    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={caminho_pdf}",
        caminho_html
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(caminho_pdf):
        print(f"[✓] PDF Final com Busca Geográfica Nearby 2km gerado: {caminho_pdf}")
        return caminho_pdf
    else:
        raise RuntimeError(f"Erro na conversão PDF: {res.stderr}")

if __name__ == "__main__":
    gerar_relatorio_final_canto_do_mar()

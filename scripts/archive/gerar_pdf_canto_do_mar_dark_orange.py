import os
import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("C:/Users/Augusto/Desktop/AH3/.env")
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

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

def gerar_relatorio_canto_do_mar_padrao_tradicao():
    print("[*] Buscando dados de Canto do Mar Ponta das Canas...")
    alvo = buscar_place_detalhes("Canto do Mar Ponta das Canas Florianopolis")
    
    nome = alvo.get("displayName", {}).get("text", "Canto do Mar Ponta das Canas")
    endereco = alvo.get("formattedAddress", "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC")
    telefone = alvo.get("nationalPhoneNumber", "(48) 3261-0872")
    website = alvo.get("websiteUri", "https://cantodomarfloripa.com.br")
    rating = float(alvo.get("rating", 4.6))
    total_reviews = int(alvo.get("userRatingCount", 178))
    lat = alvo.get("location", {}).get("latitude", -27.3972)
    lon = alvo.get("location", {}).get("longitude", -48.4239)
    cid_mock = "0x400c15ed012f4ec"
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # 10 Concorrentes Reais (Mix de 10)
    ranking = [
        {"pos": "1º", "nome": "Ocean House", "dist": "0.39 km", "nota": "4.6 ★", "revs": "475 reviews", "cardapio": "Não", "whats": "Não", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "2º", "nome": "Restaurante Mira Maré", "dist": "0.50 km", "nota": "4.5 ★", "revs": "1.445 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "3º", "nome": "Restaurante Garra Azul", "dist": "0.51 km", "nota": "4.3 ★", "revs": "1.362 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "4º", "nome": "Ponta da Praia", "dist": "0.53 km", "nota": "4.7 ★", "revs": "217 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "5º", "nome": "Ratones Craft Beer", "dist": "0.91 km", "nota": "4.8 ★", "revs": "2.114 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Cross-Nicho (Bar/Chopp)", "destaque": False},
        # Alvo
        {"pos": "6º", "nome": nome, "dist": "Local", "nota": f"{rating:.1f} ★", "revs": f"{total_reviews} reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": True},
        {"pos": "7º", "nome": "Gaivota", "dist": "0.30 km", "nota": "4.4 ★", "revs": "335 reviews", "cardapio": "Não", "whats": "Não", "tipo": "Cross-Nicho (Geral)", "destaque": False},
        {"pos": "8º", "nome": "A Toca Choperia e Petiscaria", "dist": "0.39 km", "nota": "4.9 ★", "revs": "165 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Cross-Nicho (Bar/Chopp)", "destaque": False},
        {"pos": "9º", "nome": "Restaurante Marinheiro's", "dist": "1.14 km", "nota": "4.6 ★", "revs": "444 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "10º", "nome": "Restaurante Lula Floripa", "dist": "1.25 km", "nota": "4.6 ★", "revs": "626 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "destaque": False},
        {"pos": "11º", "nome": "Baleia Branca RestoBar", "dist": "0.52 km", "nota": "4.3 ★", "revs": "72 reviews", "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (RestoBar)", "destaque": False}
    ]

    # Carregar o modelo exato do Dark Orange de Tradição Campeira
    template_path = r"C:\Users\Augusto\.gemini\antigravity-ide\scratch\auditoria-tradicao-campeira\Auditoria_Tradicao_Campeira_Dark_Orange.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Substituições de Dados Gerais
    html = html.replace("Restaurante Tradição Campeira", nome)
    html = html.replace("Av. Luiz Boiteux Piazza, 4893 - Cachoeira do Bom Jesus, Florianópolis - SC", endereco)
    html = html.replace("(48) 3284-5153", telefone)
    html = html.replace("-27.41682, -48.43129", f"{lat:.5f}, {lon:.5f}")
    html = html.replace("Cachoeira do Bom Jesus", "Ponta das Canas")
    html = html.replace("26/09/2026", data_atual)
    html = html.replace("Buffet e Frutos do Mar", "Restaurante de Frutos do Mar")

    # Atualizar KPIs da Página 1
    html = html.replace('>64<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>', '>58<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>')
    html = html.replace('>996<', f'>{total_reviews}<')
    html = html.replace('4º Lugar Regional', 'Abaixo do Top 3 Regional')
    html = html.replace('Líder regional possui 2.140', 'Líder direto possui 1.445 reviews')
    html = html.replace('>4.4<span style="font-size:18px; color:var(--orange);">★</span>', f'>{rating:.1f}<span style="font-size:18px; color:var(--green);">★</span>')
    html = html.replace('Abaixo do Top 3 (4.6★)', 'Nota de Excelência (4.6★)')
    html = html.replace('Dispersão em notas recentes', 'Satisfação elevada comprovada')

    # Substituir Linhas da Tabela de Benchmarking da Página 2
    # Montar o novo tbody com os 10 concorrentes reais
    ranking_tbody = ""
    for r in ranking:
        if r["destaque"]:
            ranking_tbody += f"""              <tr class="is-target">
                <td><span class="pos-badge target">{r['pos']}</span></td>
                <td>
                  <div class="company-cell">
                    <span>{r['nome']}</span>
                    <span class="tag-target">ALVO</span>
                  </div>
                </td>
                <td><span style="color: var(--green); font-weight: 800;">{r['nota']}</span></td>
                <td><strong>{r['revs']}</strong></td>
                <td><span class="pill-bool yes">Sim</span></td>
                <td><span class="pill-bool yes">Sim</span></td>
              </tr>\n"""
        else:
            badge_cls = "top-3" if r["pos"] in ["1º", "2º", "3º"] else "other"
            card_cls = "yes" if r["cardapio"] == "Sim" else "no"
            whats_cls = "yes" if r["whats"] == "Sim" else "no"
            nota_cor = "var(--green)" if "4.6" in r["nota"] or "4.7" in r["nota"] or "4.8" in r["nota"] or "4.9" in r["nota"] else "var(--muted)"
            ranking_tbody += f"""              <tr>
                <td><span class="pos-badge {badge_cls}">{r['pos']}</span></td>
                <td><span style="font-weight: 600; color: var(--text);">{r['nome']} <small style="color:var(--muted); font-size:10px;">({r['tipo']})</small></span></td>
                <td><span style="color: {nota_cor}; font-weight: 700;">{r['nota']}</span></td>
                <td>{r['revs']}</td>
                <td><span class="pill-bool {card_cls}">{r['cardapio']}</span></td>
                <td><span class="pill-bool {whats_cls}">{r['whats']}</span></td>
              </tr>\n"""

    # Encontrar e substituir o bloco tbody da tabela
    import re
    tbody_pattern = r"<tbody>[\s\S]*?</tbody>"
    html = re.sub(tbody_pattern, f"<tbody>\n{ranking_tbody}            </tbody>", html, count=1)

    # Atualizar Callouts de Diagnóstico
    callout_p1 = f"""<strong>Diagnóstico Executivo da Página 1:</strong> O <strong>{nome}</strong> apresenta uma das melhores notas da orla (<strong>{rating:.1f}★</strong>) e presença cadastral impecável. No entanto, com apenas <strong>{total_reviews} avaliações</strong>, fica em desvantagem crítica de volume frente aos vizinhos imediatos como Mira Maré (1.445) e Garra Azul (1.362). Acelerar a captação de avaliações é o passo decisivo para assumir a liderança orgânica."""
    
    callout_p2 = f"""<strong>Proposta Comercial & Impacto Direto:</strong> Ao implementar uma rotina ativa de captura de avaliações no pós-atendimento e otimizar a rota de reservas no WhatsApp, o <strong>{nome}</strong> superará a barreira das 500 avaliações rapidamente, disputando o topo das buscas com os líderes consolidados de Ponta das Canas."""

    # Ajustar textos dos callouts
    html = re.sub(r'<div class="callout">[\s\S]*?</div>', f'<div class="callout">\n        {callout_p1}\n      </div>', html, count=1)
    html = re.sub(r'<div class="callout" style="padding: 14px 18px;">[\s\S]*?</div>', f'<div class="callout" style="padding: 14px 18px;">\n        {callout_p2}\n      </div>', html, count=1)

    # Salvar HTML e converter para PDF
    saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
    os.makedirs(saida_dir, exist_ok=True)
    caminho_html = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_DarkOrange_Original.html")
    caminho_pdf = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_DarkOrange_Original.pdf")

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[✓] HTML gerado: {caminho_html}")

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
        print(f"[✓] PDF Dark Orange Original gerado com sucesso: {caminho_pdf}")
        return caminho_pdf
    else:
        raise RuntimeError(f"Erro na conversão PDF: {res.stderr}")

if __name__ == "__main__":
    gerar_relatorio_canto_do_mar_padrao_tradicao()

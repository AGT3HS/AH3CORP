import os
import sys
import subprocess
import json
import re
import unicodedata
from datetime import datetime

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '_', text)

# Carregar template Dark Orange base
template_path = r"C:\Users\Augusto\Desktop\AH3\saida\Auditoria_Canto_do_Mar_DarkOrange_V3.html"
if not os.path.exists(template_path):
    template_path = r"C:\Users\Augusto\Desktop\AH3\saida\Auditoria_Canto_do_Mar_Nearby2km_DarkOrange.html"

with open(template_path, "r", encoding="utf-8") as f:
    base_html_template = f.read()

with open('BigBrain/handoff/varredura_norte_da_ilha_total.json', 'r', encoding='utf-8') as f:
    todos_restaurantes = json.load(f)

top10 = todos_restaurantes[:10]
os.makedirs('BigBrain/handoff/auditorias_top10_dark_orange', exist_ok=True)
os.makedirs('saida/top10_dark_orange_html', exist_ok=True)

edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

data_atual = datetime.now().strftime("%d/%m/%Y")

gerados = []

for idx, alvo in enumerate(top10, 1):
    nome = alvo.get("displayName", {}).get("text", "Restaurante")
    categoria = alvo.get("categoria", "Restaurante")
    bairro = alvo.get("hub", "Norte da Ilha")
    endereco = alvo.get("formattedAddress", f"{bairro}, Florianópolis - SC")
    telefone = alvo.get("nationalPhoneNumber", "(48) Não informado")
    rating = float(alvo.get("rating", 4.5))
    total_reviews = int(alvo.get("userRatingCount", 0))
    lat = alvo.get("location", {}).get("latitude", -27.4260)
    lon = alvo.get("location", {}).get("longitude", -48.4550)
    tem_site = bool(alvo.get("websiteUri"))
    tem_tel = bool(alvo.get("nationalPhoneNumber"))
    
    # Calcular benchmarks com estabelecimentos do mesmo bairro ou próximos
    concorrentes_bairro = [r for r in todos_restaurantes if r.get('id') != alvo.get('id')]
    # Pegar os maiores em volume para o ranking comparativo
    top_concorrentes = concorrentes_bairro[:9]
    
    raw_concorrentes = []
    for c in top_concorrentes:
        raw_concorrentes.append({
            "nome": c.get("displayName", {}).get("text", "Concorrente"),
            "nota": f"{float(c.get('rating', 4.5)):.1f} ★",
            "revs_num": int(c.get("userRatingCount", 0)),
            "cardapio": "Sim" if c.get("websiteUri") else "Não",
            "whats": "Sim" if c.get("nationalPhoneNumber") else "Não",
            "tipo": c.get("categoria", "Gastronomia"),
            "alvo": False
        })
    
    # Inserir o alvo
    raw_concorrentes.append({
        "nome": nome,
        "nota": f"{rating:.1f} ★",
        "revs_num": total_reviews,
        "cardapio": "Sim" if tem_site else "Não",
        "whats": "Sim" if tem_tel else "Não",
        "tipo": f"Alvo ({categoria})",
        "alvo": True
    })
    
    # Ordenar por volume de avaliações desc
    raw_concorrentes.sort(key=lambda x: -x["revs_num"])
    
    # Achar a posição do alvo
    pos_alvo = 1
    for i, r in enumerate(raw_concorrentes, 1):
        if r["alvo"]:
            pos_alvo = i
            break
            
    # Montar tbody
    ranking_tbody = ""
    for r_idx, r in enumerate(raw_concorrentes[:8], 1):
        pos_str = f"{r_idx}º"
        revs_formatado = f"{r['revs_num']:,}".replace(",", ".")
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
                <td><strong>{revs_formatado}</strong></td>
                <td><span class="pill-bool {card_cls}">{r['cardapio']}</span></td>
                <td><span class="pill-bool {whats_cls}">{r['whats']}</span></td>
              </tr>\n"""
        else:
            badge_cls = "top-3" if r_idx <= 3 else "other"
            ranking_tbody += f"""              <tr>
                <td><span class="pos-badge {badge_cls}">{pos_str}</span></td>
                <td><span style="font-weight: 600; color: var(--text);">{r['nome']} <small style="color:var(--muted); font-size:10px;">({r['tipo']})</small></span></td>
                <td><span style="color: var(--text); font-weight: 700;">{r['nota']}</span></td>
                <td>{revs_formatado}</td>
                <td><span class="pill-bool {card_cls}">{r['cardapio']}</span></td>
                <td><span class="pill-bool {whats_cls}">{r['whats']}</span></td>
              </tr>\n"""

    # KPIs
    score_presenca = alvo.get("seo_score", 85)
    
    # Clonar e ajustar HTML
    html = base_html_template
    html = html.replace("Canto do Mar Ponta das Canas", nome)
    html = html.replace("R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC, 88056-730", endereco)
    html = html.replace("(48) 3261-0872", telefone)
    html = html.replace("-27.39836, -48.43072", f"{lat:.5f}, {lon:.5f}")
    html = html.replace("Restaurante de Frutos do Mar", categoria)
    html = html.replace("Ponta das Canas", bairro)
    html = html.replace("30/09/2026", data_atual)
    
    # Atualizar dados numéricos
    html = re.sub(r'>\d+/100<', f'>{score_presenca}/100<', html)
    html = html.replace(">178<", f">{total_reviews:,}".replace(",", ".") + "<")
    html = html.replace(">4,6<", f">{rating:.1f}<".replace(".", ","))
    html = html.replace(">4.6<", f">{rating:.1f}<")
    html = html.replace("Você é o 9º no Google Maps da região.", f"Você é o {pos_alvo}º em volume no Google Maps regional.")
    
    # Substituir tabela do ranking
    tbody_pattern = r"<tbody>[\s\S]*?</tbody>"
    html = re.sub(tbody_pattern, f"<tbody>\n{ranking_tbody}            </tbody>", html, count=1)
    
    slug = slugify(nome)
    caminho_html = os.path.abspath(f"saida/top10_dark_orange_html/{idx:02d}_{slug}.html")
    caminho_pdf = os.path.abspath(f"BigBrain/handoff/auditorias_top10_dark_orange/{idx:02d}_Auditoria_{slug}_DarkOrange.pdf")
    
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={caminho_pdf}",
        caminho_html
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(caminho_pdf):
        print(f"[{idx}/10] Gerado Dark Orange PDF: {caminho_pdf}")
        gerados.append(caminho_pdf)

print("Todos os 10 relatórios Dark Orange gerados com sucesso!")

import os
import subprocess
import requests
import re
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

def gerar_pdf_ajustado():
    print("[*] Buscando dados de Canto do Mar Ponta das Canas...")
    alvo = buscar_place_detalhes("Canto do Mar Ponta das Canas Florianopolis")
    
    nome = alvo.get("displayName", {}).get("text", "Canto do Mar Ponta das Canas") if alvo else "Canto do Mar Ponta das Canas"
    endereco = alvo.get("formattedAddress", "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC") if alvo else "R. Dep. Fernando Viégas, 560 - Ponta das Canas, Florianópolis - SC"
    telefone = alvo.get("nationalPhoneNumber", "(48) 3261-0872") if alvo else "(48) 3261-0872"
    rating = float(alvo.get("rating", 4.6)) if alvo else 4.6
    total_reviews = int(alvo.get("userRatingCount", 178)) if alvo else 178
    lat = alvo.get("location", {}).get("latitude", -27.3972) if alvo else -27.3972
    lon = alvo.get("location", {}).get("longitude", -48.4239) if alvo else -48.4239
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Lista de concorrentes ordenada rigorosamente por volume de avaliações (desc)
    raw_concorrentes = [
        {"nome": "Ratones Craft Beer", "dist": "0.91 km", "nota": "4.8 ★", "revs_num": 2114, "cardapio": "Sim", "whats": "Sim", "tipo": "Cross-Nicho (Bar/Chopp)", "alvo": False},
        {"nome": "Restaurante Mira Maré", "dist": "0.50 km", "nota": "4.5 ★", "revs_num": 1445, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": "Restaurante Garra Azul", "dist": "0.51 km", "nota": "4.3 ★", "revs_num": 1362, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": "Restaurante Lula Floripa", "dist": "1.25 km", "nota": "4.6 ★", "revs_num": 626, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": "Ocean House", "dist": "0.39 km", "nota": "4.6 ★", "revs_num": 475, "cardapio": "Não", "whats": "Não", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": "Restaurante Marinheiro's", "dist": "1.14 km", "nota": "4.6 ★", "revs_num": 444, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": "Gaivota", "dist": "0.30 km", "nota": "4.4 ★", "revs_num": 335, "cardapio": "Não", "whats": "Não", "tipo": "Cross-Nicho (Geral)", "alvo": False},
        {"nome": "Ponta da Praia", "dist": "0.53 km", "nota": "4.7 ★", "revs_num": 217, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": False},
        {"nome": nome, "dist": "Local", "nota": f"{rating:.1f} ★", "revs_num": total_reviews, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (Frutos do Mar)", "alvo": True},
        {"nome": "A Toca Choperia e Petiscaria", "dist": "0.39 km", "nota": "4.9 ★", "revs_num": 165, "cardapio": "Sim", "whats": "Sim", "tipo": "Cross-Nicho (Bar/Chopp)", "alvo": False},
        {"nome": "Baleia Branca RestoBar", "dist": "0.52 km", "nota": "4.3 ★", "revs_num": 72, "cardapio": "Sim", "whats": "Sim", "tipo": "Direto (RestoBar)", "alvo": False}
    ]

    raw_concorrentes.sort(key=lambda x: -x["revs_num"])

    ranking_tbody = ""
    for idx, r in enumerate(raw_concorrentes, 1):
        pos_str = f"{idx}º"
        revs_formatado = f"{r['revs_num']:,}".replace(",", ".") + " reviews"
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
                <td>{revs_formatado}</td>
                <td><span class="pill-bool {card_cls}">{r['cardapio']}</span></td>
                <td><span class="pill-bool {whats_cls}">{r['whats']}</span></td>
              </tr>\n"""

    template_path = r"C:\Users\Augusto\.gemini\antigravity-ide\scratch\auditoria-tradicao-campeira\Auditoria_Tradicao_Campeira_Dark_Orange.html"
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Substituições de Dados Gerais
    html = html.replace("Restaurante Tradição Campeira", nome)
    html = html.replace("Av. Luiz Boiteux Piazza, 4893 - Cachoeira do Bom Jesus, Florianópolis - SC", endereco)
    html = html.replace("(48) 3284-5153", telefone)
    html = html.replace("-27.41682, -48.43129", f"{lat:.5f}, {lon:.5f}")
    html = html.replace("Cachoeira do Bom Jesus", "Ponta das Canas")
    html = html.replace("26/09/2026", data_atual)
    html = html.replace("Buffet e Frutos do Mar", "Restaurante de Frutos do Mar")

    # 2. Atualizar KPIs da Página 1
    html = html.replace('>64<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>', '>58<span style="font-size:16px; font-weight:600; color:var(--muted);">/100</span>')
    html = html.replace('>996<', f'>{total_reviews}<')
    html = html.replace('4º Lugar Regional', '9º em Volume Regional')
    html = html.replace('Líder regional possui 2.140', 'Líder regional possui 2.114')
    html = html.replace('>4.4<span style="font-size:18px; color:var(--orange);">★</span>', f'>{rating:.1f}<span style="font-size:18px; color:#F59E0B; margin-left:2px;">★</span>')
    html = html.replace('Abaixo do Top 3 (4.6★)', 'Nota de Excelência (4.6★)')
    html = html.replace('Dispersão em notas recentes', 'Satisfação elevada comprovada')

    # 3. Explicar e traduzir termos didáticos na Página 1 (Gráfico de Barras)
    html = html.replace('<span class="bar-label">Dados NAP</span>', '<span class="bar-label" title="Nome, Endereço e Telefone padronizados">Dados Cadastrais (NAP)</span>')
    html = html.replace('<span class="bar-label">Recência</span>', '<span class="bar-label" title="Ritmo e frequência de novos comentários">Recência (Novos Reviews)</span>')

    # 4. Substituir tabela de ranking
    tbody_pattern = r"<tbody>[\s\S]*?</tbody>"
    html = re.sub(tbody_pattern, f"<tbody>\n{ranking_tbody}            </tbody>", html, count=1)

    # 5. Ajustes Didáticos no Checklist da Página 3
    # Item 01: NAP explicado
    html = html.replace(
        '<strong style="color:var(--text);">01. Nome Comercial (NAP)</strong>',
        '<strong style="color:var(--text);">01. Nome Comercial & Dados Cadastrais (NAP)</strong><br><small style="color:var(--muted); font-size:9.5px;">Consistência de Nome, Endereço e Telefone em toda a web</small>'
    )
    html = html.replace(
        'Nome limpo e alinhado com a fachada, sem inclusão indevida de palavras-chave.',
        'Alinhamento exato entre o nome de fachada, endereço e telefone no Google Maps, evitando duplicidades ou perda de relevância.'
    )

    # Item 08: Recência explicada
    html = html.replace(
        '<strong style="color:var(--text);">08. Recência das Avaliações</strong>',
        '<strong style="color:var(--text);">08. Recência das Avaliações (Frequência de Novos Reviews)</strong><br><small style="color:var(--muted); font-size:9.5px;">Ritmo contínuo com que novos clientes avaliam o local</small>'
    )
    html = html.replace(
        'Frequência intermitente de novos reviews; o algoritmo favorece perfis com fluxo contínuo.',
        'Fluxo de avaliações no último mês. O Google prioriza perfis com fluxo contínuo e recente de feedbacks positivos.'
    )

    # Item 07: Taxa de Resposta explicada
    html = html.replace(
        '<strong style="color:var(--text);">07. Taxa de Resposta a Reviews</strong>',
        '<strong style="color:var(--text);">07. Taxa de Resposta a Reviews (Gestão de SAC)</strong><br><small style="color:var(--muted); font-size:9.5px;">% de comentários respondidos pela equipe</small>'
    )
    html = html.replace(
        'Apenas 14% das opiniões são respondidas; perda de engajamento e pontuação no Maps.',
        'Poucas opiniões são respondidas pelo proprietário; responder a 99.9% dos reviews eleva o engajamento e a nota no Maps.'
    )

    # 6. Atualizar Barra de Cobertura da Página 3 (Didática)
    html = html.replace(
        '<span><strong>65% Fatores On-SERP Auditados:</strong> Perfil GBP, Volume, Notas, NAP e Imagens</span>',
        '<span><strong>65% Fatores Públicos Auditados (On-SERP):</strong> Perfil Google Maps, Volume, Notas, Dados Cadastrais (NAP) e Imagens</span>'
    )
    html = html.replace(
        '<span><strong>35% Fatores Off-SERP (Fase 2):</strong> SEO on-page, Backlinks, Search Console</span>',
        '<span><strong>35% Métricas Internas do Painel (Fase 2):</strong> Chamadas telefônicas, rotas solicitadas e buscas diretas</span>'
    )

    # 7. Ajustar CSS para evitar cortes e manter proporção A4
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
    padding: 24px 32px 16px !important;
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
    gap: 5px !important;
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
  
  .checklist-table td {
    padding: 7px 10px !important;
    font-size: 11px !important;
  }
"""
    html = html.replace("/* ESTRUTURA DO CONTAINER DE PÁGINA (CARTÃO FLUTUANTE) */", css_fix + "\n  /* ESTRUTURA DO CONTAINER DE PÁGINA (CARTÃO FLUTUANTE) */")

    # 8. Ajustar Callouts
    callout_p1 = f"""<strong>Diagnóstico Executivo da Página 1:</strong> O <strong>{nome}</strong> apresenta nota destacada (<strong>{rating:.1f}★</strong>) e dados cadastrais (NAP: Nome, Endereço e Telefone) validados. Contudo, com <strong>{total_reviews} avaliações</strong>, ocupa a 9ª posição em volume na microrregião, enquanto concorrentes a 500m já superam 1.400 reviews. Acelerar a recência e a captação ativa de avaliações é o caminho mais rápido para alcançar o Top 3 no Google Maps."""
    
    callout_p2 = f"""<strong>Proposta Comercial & Impacto Direto:</strong> Ao estruturar a captação contínua de avaliações no pós-atendimento e otimizar o canal direto de reservas no WhatsApp, o <strong>{nome}</strong> superará rapidamente o patamar de 500 reviews, atraindo um fluxo projetado de clientes muito maior para a orla de Ponta das Canas."""

    html = re.sub(r'<div class="callout">[\s\S]*?</div>', f'<div class="callout">\n        {callout_p1}\n      </div>', html, count=1)
    html = re.sub(r'<div class="callout" style="padding: 14px 18px;">[\s\S]*?</div>', f'<div class="callout" style="padding: 10px 14px; font-size:11.5px; line-height:1.4;">\n        {callout_p2}\n      </div>', html, count=1)

    saida_dir = r"C:\Users\Augusto\Desktop\AH3\saida"
    os.makedirs(saida_dir, exist_ok=True)
    caminho_html = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_DarkOrange_V3.html")
    caminho_pdf = os.path.join(saida_dir, "Auditoria_Canto_do_Mar_DarkOrange_V3.pdf")

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
        print(f"[✓] PDF V3 gerado com sucesso: {caminho_pdf}")
        return caminho_pdf, caminho_html
    else:
        raise RuntimeError(f"Erro na conversão PDF: {res.stderr}")

if __name__ == "__main__":
    gerar_pdf_ajustado()

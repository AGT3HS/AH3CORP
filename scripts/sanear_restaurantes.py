import json
import csv
import re
import os

INPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_enriquecido.json"
OUTPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_enriquecido.json"
CSV_FILE = "BigBrain/handoff/restaurantes_norte_da_ilha.csv"
MD_FILE = "BigBrain/handoff/lista_restaurantes_norte.md"
HTML_FILE = "painel_controle.html"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    places = json.load(f)

print(f"Total antes do saneamento: {len(places)}")

# Bairros alvo válidos para esta etapa (Norte da Ilha específico solicitado)
# Ponta das Canas, Cachoeira do Bom Jesus (vizinho imediato/conexo), Canasvieiras, Jurerê, Jurerê Internacional, Jurerê Tradicional, Praia do Forte, Vargem do Bom Jesus, Vargem Grande.
VALID_NORTH_KEYWORDS = [
    "ponta das canas", "canasvieiras", "jurerê", "jurere", "praia do forte",
    "cachoeira do bom jesus", "lagoinha", "praia da lagoinha", "vargem grande",
    "vargem do bom jesus"
]

def determine_exact_bairro(address):
    addr = (address or "").lower()
    
    if "ponta das canas" in addr or "praia da lagoinha" in addr or "lagoinha" in addr:
        return "Ponta das Canas"
    if "cachoeira do bom jesus" in addr:
        return "Ponta das Canas / Cachoeira"
    if "canasvieiras" in addr or "vargem grande" in addr or "vargem do bom jesus" in addr:
        return "Canasvieiras"
    if "jurerê internacional" in addr or "jurere internacional" in addr:
        return "Jurerê Internacional"
    if "jurerê" in addr or "jurere" in addr or "praia do forte" in addr:
        return "Jurerê"
    
    # Se caiu em outros bairros fora do escopo desta rodada (Centro, Itacorubi, Trindade, Ingleses, Barra da Lagoa, Santo Antônio, etc.)
    return None

cleaned_places = []

for p in places:
    addr = p.get("endereco", "")
    exact_bairro = determine_exact_bairro(addr)
    
    if exact_bairro:
        p["bairro"] = exact_bairro
        cleaned_places.append(p)
    else:
        # Fora do escopo do Lote 1 (ex: Forneria Piedoro que fica no Itacorubi, Trattoria Carbone no Centro, etc.)
        # print(f"Removido (fora do lote): {p.get('nome')} | {addr}")
        pass

print(f"Total após saneamento geográfico estrito: {len(cleaned_places)} restaurantes.")

# Salvar JSON higienizado
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_places, f, ensure_ascii=False, indent=2)

# Ordenar
cleaned_places = sorted(cleaned_places, key=lambda x: (x.get("bairro", ""), -float(x.get("nota", 0)), -int(x.get("avaliacoes", 0))))

# Salvar CSV
fields = [
    "nome", "bairro", "categoria", "nota", "avaliacoes", "faixa_preco",
    "status", "endereco", "telefone", "whatsapp", "site", "instagram",
    "ifood", "maps_url", "possivel_rede"
]

with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in cleaned_places:
        writer.writerow(row)

# Gerar Markdown
bairros = {}
for r in cleaned_places:
    b = r.get("bairro", "Outro")
    bairros.setdefault(b, []).append(r)

lines = []
lines.append("# Lista Consolidada de Restaurantes · Norte da Ilha (Florianópolis)\n")
lines.append(f"**Total de Estabelecimentos Auditados:** {len(cleaned_places)}\n")
lines.append("> Base extraída via Google Places API (New) com filtro geográfico rigoroso por endereço real (Ponta das Canas/Cachoeira, Canasvieiras e Jurerê/Jurerê Internacional).\n")

for b, items in sorted(bairros.items()):
    lines.append(f"\n## 📍 {b.upper()} ({len(items)} restaurantes)\n")
    lines.append("| Restaurante | Categoria | Nota / Avaliações | Preço | WhatsApp | Instagram | Maps |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |")
    
    items_sorted = sorted(items, key=lambda x: (-float(x.get("nota", 0)), -int(x.get("avaliacoes", 0))))
    for r in items_sorted:
        nome = r["nome"].replace("|", "-")
        cat = r["categoria"]
        nota = f"⭐ {r['nota']} ({r['avaliacoes']})"
        preco = r["faixa_preco"].split(" ")[0] if r["faixa_preco"] else "-"
        
        wa = f"[WhatsApp]({r['whatsapp']})" if r["whatsapp"].startswith("http") else "—"
        ig = f"[Instagram]({r['instagram']})" if r["instagram"].startswith("http") else "—"
        maps = f"[Maps]({r['maps_url']})"
        
        lines.append(f"| **{nome}** | {cat} | {nota} | {preco} | {wa} | {ig} | {maps} |")

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"CSV e Markdown regerados com sucesso.")

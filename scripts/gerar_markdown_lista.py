import json

INPUT_FILE = "BigBrain/handoff/restaurantes_norte_ilha_enriquecido.json"
MD_FILE = "BigBrain/handoff/lista_restaurantes_norte.md"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Agrupamento
bairros = {}
for r in data:
    b = r.get("bairro", "Outro")
    bairros.setdefault(b, []).append(r)

lines = []
lines.append("# Lista Consolidada de Restaurantes · Norte da Ilha (Florianópolis)\n")
lines.append(f"**Total de Estabelecimentos Auditados:** {len(data)}\n")
lines.append("> Base extraída via Google Places API (New) e enriquecida com dados de Instagram, WhatsApp e Maps.\n")

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

print(f"Markdown completo gerado em: {MD_FILE}")

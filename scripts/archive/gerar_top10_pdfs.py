import json
import os
import re
import unicodedata
from gerar_relatorio import gerar_auditoria_pdf

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'[-\s]+', '_', text)

with open('BigBrain/handoff/varredura_norte_da_ilha_total.json', 'r', encoding='utf-8') as f:
    todos = json.load(f)

# Top 10
top10 = todos[:10]

os.makedirs('BigBrain/handoff/auditorias_top10', exist_ok=True)
os.makedirs('saida', exist_ok=True)

gerados = []

for idx, r in enumerate(top10, 1):
    nome = r.get('displayName', {}).get('text', 'Restaurante')
    slug = slugify(nome)
    pdf_path = os.path.abspath(f'BigBrain/handoff/auditorias_top10/{idx:02d}_Auditoria_{slug}.pdf')
    
    dados_formatados = {
        "displayName": {"text": nome},
        "formattedAddress": r.get('formattedAddress', 'Endereço em Florianópolis - SC'),
        "nationalPhoneNumber": r.get('nationalPhoneNumber'),
        "websiteUri": r.get('websiteUri'),
        "rating": r.get('rating', 4.5),
        "userRatingCount": r.get('userRatingCount', 0),
        "categoria": r.get('categoria', 'Restaurante'),
        "hub": r.get('hub', 'Norte da Ilha')
    }
    
    gerar_auditoria_pdf(dados_formatados, pdf_path)
    gerados.append({
        "rank": idx,
        "nome": nome,
        "categoria": r.get('categoria'),
        "bairro": r.get('hub'),
        "nota": r.get('rating'),
        "avaliacoes": r.get('userRatingCount'),
        "pdf": pdf_path
    })
    print(f"[{idx}/10] Gerado: {pdf_path}")

print("Concluído!")

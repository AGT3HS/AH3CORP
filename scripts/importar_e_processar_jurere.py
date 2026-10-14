import os
import csv
from datetime import datetime

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
VERIFIED_CSV = os.path.join(ROOT_DIR, "BigBrain/handoff/lista_completa_restaurantes_verificados_ah3.csv")
LEADS_CSV = os.path.join(ROOT_DIR, "BigBrain/funil/leads.csv")

def importar_jurere():
    if not os.path.exists(VERIFIED_CSV):
        print(f"Erro: {VERIFIED_CSV} não encontrado.")
        return

    # Ler leads existentes em leads.csv para pegar o maior ID
    max_id = 0
    existing_names = set()
    if os.path.exists(LEADS_CSV):
        with open(LEADS_CSV, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_names.add(row.get('nome', '').strip().lower())
                try:
                    max_id = max(max_id, int(row.get('id', 0)))
                except:
                    pass

    print(f"Maior ID atual em leads.csv: {max_id}. Leads já cadastrados: {len(existing_names)}")

    # Ler verificados e filtrar Jurerê / Daniela
    novos_leads = []
    with open(VERIFIED_CSV, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            bairro = row.get('bairro', '')
            nome = row.get('nome', '')
            if ('jurerê' in bairro.lower() or 'daniela' in bairro.lower()) and nome.strip().lower() not in existing_names:
                max_id += 1
                lead_entry = {
                    'id': str(max_id),
                    'nome': nome,
                    'bairro': f"{bairro}, Florianópolis",
                    'categoria': row.get('categoria', 'Restaurante/Bar'),
                    'nota_google': row.get('nota_google', '4.5'),
                    'total_avaliacoes': row.get('reviews_google', '100'),
                    'status': 'novo',
                    'telefone': row.get('telefone', '[SEM CONTATO]'),
                    'contato_nome': '',
                    'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'data_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'valor_fechado': '',
                    'observacoes': f"Importado automaticamente via varredura Jurerê/Daniela. Maps: {row.get('link_google_maps', '')}"
                }
                novos_leads.append(lead_entry)
                existing_names.add(nome.strip().lower())

    print(f"Total de novos leads de Jurerê/Daniela prontos para importação: {len(novos_leads)}")

    if not novos_leads:
        print("Nenhum lead novo encontrado para importar.")
        return

    # Escrever de volta em leads.csv (mantendo os existentes ou adicionando)
    # Primeiro lemos todas as linhas existentes
    fieldnames = ['id', 'nome', 'bairro', 'categoria', 'nota_google', 'total_avaliacoes', 'status', 'telefone', 'contato_nome', 'data_criacao', 'data_atualizacao', 'valor_fechado', 'observacoes']
    
    rows_existentes = []
    if os.path.exists(LEADS_CSV):
        with open(LEADS_CSV, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows_existentes.append(row)

    todas_linhas = rows_existentes + novos_leads

    with open(LEADS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todas_linhas)

    print(f"Sucesso! {len(novos_leads)} novos leads adicionados a {LEADS_CSV}. Total no funil: {len(todas_linhas)}")

if __name__ == '__main__':
    importar_jurere()

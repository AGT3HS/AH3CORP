#!/usr/bin/env python3
"""
AH3 — Gerador em Lote de Kits de Prospecção por Bairro (Batch Pipeline)
Agente Encarregado: @Maestro
Executa a esteira Lead-to-Proposal para múltiplos estabelecimentos de uma região em lote:
1. Geração de Placa NFC 100x100mm (SVG + PNG 300 DPI)
2. Validação Visual SVG Linter
3. Geração de Proposta Modular 9 Slides em PDF
4. Linter de Compliance Anti-Promessas
5. Sincronização do Painel de Controle e Registro no Ledger
"""

import os
import sys
import csv
import argparse
import subprocess
import unicodedata
import re

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
LEADS_CSV = os.path.join(ROOT_DIR, "BigBrain/funil/leads.csv")

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def processar_lote(bairro_filtro, max_leads=5):
    if not os.path.exists(LEADS_CSV):
        print(f"Erro: {LEADS_CSV} não encontrado.")
        return

    leads_alvo = []
    with open(LEADS_CSV, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bairro = row.get('bairro', '')
            if not bairro_filtro or normalize(bairro_filtro) in normalize(bairro):
                leads_alvo.append(row)

    print(f"\n========================================================")
    print(f" AH3 BATCH PIPELINE — Processando Lote: '{bairro_filtro or 'Geral'}'")
    print(f" Total de leads encontrados: {len(leads_alvo)} | Alvo deste lote: {min(len(leads_alvo), max_leads)}")
    print(f"========================================================\n")

    sucessos = 0
    for idx, lead in enumerate(leads_alvo[:max_leads], 1):
        nome = lead.get('nome')
        bairro = lead.get('bairro', 'Florianópolis')
        cat = lead.get('categoria', 'Gastronomia')
        nota = lead.get('nota_google', '4.6')
        reviews = lead.get('total_avaliacoes', '150')

        print(f"\n[{idx}/{min(len(leads_alvo), max_leads)}] Processando: {nome} ({bairro})...")
        cmd = [
            sys.executable, "scripts/pipeline_lead_to_proposal.py",
            "--nome", nome,
            "--bairro", bairro,
            "--categoria", cat
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [OK] Placa NFC, Proposta 9 Slides e Linter concluidos.")
            sucessos += 1
        else:
            print(f"  [ERRO] Falha no processamento: {res.stderr or res.stdout}")

    # Atualizar Painel de Controle
    print("\nAtualizando painel de controle operacional...")
    subprocess.run([sys.executable, "scripts/atualizar_painel_controle.py"], capture_output=True)

    # Registrar no Ledger
    subprocess.run([
        sys.executable, "scripts/ledger_append.py",
        "Eventos-chave",
        f"Batch Pipeline executado para {sucessos} estabelecimentos do bairro '{bairro_filtro or 'Geral'}'. Ativos sincronizados no Handoff e Painel."
    ], capture_output=True)

    print(f"\n========================================================")
    print(f" [CONCLUÍDO] {sucessos} estabelecimentos processados com sucesso.")
    print(f" Painel atualizado: Abra 'painel_controle.html' no seu navegador.")
    print(f"========================================================\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gerador em Lote de Prospecção por Bairro AH3")
    parser.add_argument("--bairro", type=str, default="Canasvieiras", help="Bairro / Região (ex: Canasvieiras, Ponta das Canas)")
    parser.add_argument("--quantidade", type=int, default=5, help="Quantidade de leads para processar")
    
    args = parser.parse_args()
    processar_lote(args.bairro, args.quantidade)

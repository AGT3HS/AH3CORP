#!/usr/bin/env python3
"""
AH3 — Pipeline Unificado "Lead-to-Proposal"
Agente Encarregado: @Maestro (Orquestração de Ponta a Ponta)
Executa a esteira completa: Ativo NFC -> Proposta -> Validação Linter -> Depósito em Handoff -> Ledger.
"""

import os
import sys
import argparse
import subprocess
import shutil
import glob
import unicodedata
import re

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def main():
    parser = argparse.ArgumentParser(description="Pipeline Lead-to-Proposal AH3")
    parser.add_argument("--nome", type=str, required=True, help="Nome do estabelecimento")
    parser.add_argument("--bairro", type=str, default="Florianópolis", help="Bairro / Região")
    parser.add_argument("--categoria", type=str, default="Hotelaria", help="Categoria")
    parser.add_argument("--output_handoff", type=str, default="BigBrain/handoff", help="Diretório de handoff")
    args = parser.parse_args()

    nome = args.nome
    slug = normalize(nome)
    os.makedirs(args.output_handoff, exist_ok=True)

    print(f"\n[1/5] Orquestrando ativos para: {nome} (@Maestro)...")
    
    # 1. Gerar Placa NFC
    print("[2/5] Gerando Placa Inteligente NFC 100x100mm (@Designer)...")
    placa_svg, placa_png = None, None
    res_placa = subprocess.run([
        sys.executable, "scripts/gerar_placa.py",
        "--nome", nome,
        "--output", "saida/placas_nfc"
    ], capture_output=True, text=True)
    print(res_placa.stdout)

    # 2. Validar SVG pelo Linter de Design
    svg_candidate = f"saida/placas_nfc/placa_nfc_{slug}.svg"
    if os.path.exists(svg_candidate):
        print("[3/5] Validando conformidade de design SVG (@Designer)...")
        res_linter_svg = subprocess.run([
            sys.executable, "scripts/verificar_design_svg.py", svg_candidate
        ], capture_output=True, text=True)
        print(res_linter_svg.stdout)
        
        # Copiar para handoff
        shutil.copy(svg_candidate, os.path.join(args.output_handoff, f"placa_{slug}.svg"))
        png_candidate = f"saida/placas_nfc/placa_nfc_{slug}.png"
        if os.path.exists(png_candidate):
            shutil.copy(png_candidate, os.path.join(args.output_handoff, f"placa_{slug}.png"))

    # 3. Gerar Proposta Modular Universal
    print("[4/6] Compilando Proposta Comercial Oficial (@Comercial)...")
    res_prop = subprocess.run([
        sys.executable, "scripts/gerar_proposta_hotelaria_base_oficial.py",
        "--nome", nome
    ], capture_output=True, text=True)
    print(res_prop.stdout)

    # 4. Gerar Relatório Executivo de Auditoria Local (Glass A4 Canônico)
    print("[5/6] Gerando Relatório Executivo de Auditoria Local Glass A4 (@Comercial)...")
    res_audit = subprocess.run([
        sys.executable, "scripts/gerar_auditoria_oficial_real.py",
        "--nome", nome,
        "--output", args.output_handoff
    ], capture_output=True, text=True)
    if res_audit.stdout:
        print(res_audit.stdout)

    # 5. Validar Textos de Handoff com Linter de Compliance
    print("[6/6] Executando linter anti-promessas (AGENTS.md)...")
    markdown_files = glob.glob(os.path.join(args.output_handoff, "*.md"))
    for mf in markdown_files:
        res_txt = subprocess.run([sys.executable, "scripts/verificar_texto.py", mf], capture_output=True, text=True)
        if res_txt.returncode != 0:
            print(f"[ALERTA DE COMPLIANCE] {mf}: {res_txt.stderr or res_txt.stdout}")

    # 5. Registro no Ledger
    subprocess.run([
        sys.executable, "scripts/ledger_append.py",
        "Eventos-chave",
        f"Pipeline Lead-to-Proposal executado para '{nome}'. Entregáveis depositados em BigBrain/handoff/."
    ], capture_output=True, text=True)

    print(f"\n==================================================================")
    print(f" [GATE DE DECISAO & GOVERNANCA — AGENTS.md]")
    print(f" Ativos depositados em: {args.output_handoff}/")
    print(f" • Placa NFC (SVG + PNG 300 DPI): placa_{slug}.svg / placa_{slug}.png")
    print(f" • Proposta Comercial 9 Slides: Proposta_Comercial_{slug}.pdf")
    print(f"\n Augusto, voce APROVA para manter ou REPROVA para exclusao?")
    print(f"==================================================================\n")

if __name__ == '__main__':
    main()

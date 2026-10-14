#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração em Lote de Apresentações Executivas Comerciais (7 Slides)
para todos os Hotéis da Base AH3.
Conforme AGENTS.md e diretrizes operacionais.
"""

import os
import sys
import json
import glob
import re
import time
import shutil
import pymupdf
from PIL import Image, ImageDraw

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

DATA_FILE = os.path.join(ROOT_DIR, "scripts", "data", "sorted_150_hotels.json")
CLIENTES_DIR = os.path.join(ROOT_DIR, "BigBrain", "clientes")
SAIDA_APRES_DIR = os.path.join(ROOT_DIR, "saida", "apresentacoes")
SAIDA_PREVIEWS_DIR = os.path.join(ROOT_DIR, "saida", "previews_apresentacoes")
PREVIEWS_CAPA_DIR = os.path.join(ROOT_DIR, "saida", "apresentacoes", "previews_capa")

from scripts.gerar_apresentacao_lead_base_oficial import (
    gerar_apresentacao_lead,
    render_svg_exact_transparent
)

def sanitizar_slug(nome):
    slug = nome.lower()
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    for orig, rep in replacements.items():
        slug = slug.replace(orig, rep)
    slug = re.sub(r'[^a-z0-9]+', '_', slug).strip('_')
    return slug

def extrair_cor_svg(svg_path):
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            c = f.read()
        m = re.findall(r'<path d=\"M0,0 L1000,0[^\"]*\" fill=\"(#[0-9a-fA-F]{6})\"', c)
        if m:
            return m[0]
        # Procura qualquer fill hex inicial
        m2 = re.findall(r'fill=\"(#[0-9a-fA-F]{6})\"', c)
        if m2:
            return m2[0]
    except Exception:
        pass
    return "#0D3B66"

def render_previews_pdf(pdf_path, out_dir, dpi=120):
    os.makedirs(out_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        img_p = os.path.join(out_dir, f"slide_{i+1:02d}.png")
        pix.save(img_p)

def processar_todos_hoteis(force=True):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        hoteis = json.load(f)

    os.makedirs(SAIDA_APRES_DIR, exist_ok=True)
    os.makedirs(SAIDA_PREVIEWS_DIR, exist_ok=True)
    os.makedirs(PREVIEWS_CAPA_DIR, exist_ok=True)

    total = len(hoteis)
    gerados = 0
    ja_existiam = 0

    print(f"Iniciando processamento de apresentações para {total} estabelecimentos (force={force})...")
    start_total = time.time()

    for idx, h in enumerate(hoteis, 1):
        ranking = h.get('ranking', idx)
        nome = h.get('nome', '')
        slug = sanitizar_slug(nome)

        # Localizar diretório do cliente
        dirs = glob.glob(os.path.join(CLIENTES_DIR, f"{ranking:02d}_*")) + \
               glob.glob(os.path.join(CLIENTES_DIR, f"{ranking}_*"))
        
        if not dirs:
            print(f"[{ranking:03d}/{total}] Pasta não encontrada para {nome}")
            continue

        h_dir = dirs[0]
        h_apres_dir = os.path.join(h_dir, "apresentacoes")
        os.makedirs(h_apres_dir, exist_ok=True)

        # Nome padrão de saída
        target_pdf_saida = os.path.join(SAIDA_APRES_DIR, f"Apresentacao_{slug}.pdf")
        target_pdf_cliente = os.path.join(h_apres_dir, f"Apresentacao_{slug}.pdf")

        if not force:
            existing_pdf = None
            pdf_candidates = glob.glob(os.path.join(h_apres_dir, "*.pdf"))
            if pdf_candidates:
                existing_pdf = pdf_candidates[0]
            elif os.path.exists(target_pdf_saida):
                existing_pdf = target_pdf_saida

            if existing_pdf and os.path.exists(existing_pdf):
                ja_existiam += 1
                if existing_pdf != target_pdf_saida and not os.path.exists(target_pdf_saida):
                    shutil.copy2(existing_pdf, target_pdf_saida)
                if existing_pdf != target_pdf_cliente and not os.path.exists(target_pdf_cliente):
                    shutil.copy2(existing_pdf, target_pdf_cliente)
                continue

        # Selecionar SVG da placa NFC
        placa_svg = None
        placas_dir = os.path.join(h_dir, "placas_nfc")
        
        # Ordem de preferência: monocromático autoridade se Costão/Majestic, senão clássico cor mãe
        pref_placas = [
            "04_modelo_monocromatico_autoridade.svg" if ranking in [1, 7] else "01_modelo_classico_cor_mae.svg",
            "01_modelo_classico_cor_mae.svg",
            "04_modelo_monocromatico_autoridade.svg",
            "02_modelo_noturno_luxo.svg",
            "03_modelo_secundario_acento.svg"
        ]
        for p_name in pref_placas:
            cand = os.path.join(placas_dir, p_name)
            if os.path.exists(cand):
                placa_svg = cand
                break
        
        if not placa_svg:
            svgs = glob.glob(os.path.join(placas_dir, "*.svg"))
            if svgs:
                placa_svg = svgs[0]

        if not placa_svg:
            print(f"[{ranking:03d}/{total}] AVISO: Sem SVG de placa para {nome}, pulando...")
            continue

        # Paleta de Cores Padrão Oficial AH3 (Fundo e Estrutura Fixos)
        cor_primaria = "#0D3B66"   # Azul Navy Clássico AH3 (Fundo Capa/Encerramento)
        cor_secundaria = "#EE964B" # Âmbar Acento AH3

        # Gerar apresentação
        resumo_p5 = f"4 serviços essenciais integrados no quarto: Wi-Fi Guest direto, Gastronomia & Room Service, Lazer & Conforto e Avaliação Google."
        
        try:
            gerar_apresentacao_lead(
                hotel_name=nome,
                svg_placa=placa_svg,
                telas_mobile=None,
                resumo_servicos_p5=resumo_p5,
                primary_hex=cor_primaria,
                accent_hex=cor_secundaria,
                autor="Augusto Henrique Dos Santos",
                tel="(48) 99908-8162",
                out_pdf=target_pdf_saida
            )

            # Sincronizar na pasta oficial do cliente
            shutil.copy2(target_pdf_saida, target_pdf_cliente)

            # Renderizar previews de slides (120 DPI)
            base_name = os.path.splitext(os.path.basename(target_pdf_saida))[0]
            preview_folder = os.path.join(SAIDA_PREVIEWS_DIR, base_name)
            render_previews_pdf(target_pdf_saida, preview_folder, dpi=120)

            # Renderizar capa (120 DPI)
            capa_png = os.path.join(PREVIEWS_CAPA_DIR, f"{ranking:02d}_capa_{slug}.png")
            doc = pymupdf.open(target_pdf_saida)
            pix = doc[0].get_pixmap(dpi=120)
            pix.save(capa_png)

            gerados += 1
            print(f"[{ranking:03d}/{total}] OK: {nome}")
        except Exception as e:
            print(f"[{ranking:03d}/{total}] ERRO ao gerar {nome}: {e}")

    elapsed = time.time() - start_total
    print("=" * 60)
    print(f"Processamento concluído em {elapsed:.2f} segundos!")
    print(f"Total de apresentações geradas: {gerados}")
    print("=" * 60)

if __name__ == "__main__":
    processar_todos_hoteis(force=True)

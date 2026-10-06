#!/usr/bin/env python3
"""Reprova texto com palavras proibidas. Uso: verificar_texto.py arquivo.md"""
import re, sys, pathlib

PROIBIDAS = [r"garantid[oa]s?", r"garantia[s]?", r"garant[ie]\w*", r"100\s?%", r"com certeza"]
if len(sys.argv) < 2:
    sys.exit("Uso: verificar_texto.py <arquivo>")
texto = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
achados = sorted({m.group().lower() for p in PROIBIDAS for m in re.finditer(p, texto, re.IGNORECASE)})
if achados:
    print("REPROVADO. Encontrado:", achados)
    sys.exit(1)
print("OK: nenhuma palavra proibida.")

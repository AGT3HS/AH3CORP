#!/usr/bin/env python3
"""Uso: ledger_append.py "<Seção>" "<texto>"  (seção padrão: Eventos-chave)"""
import sys, datetime, pathlib

SECOES = ["Eventos-chave", "Decisões tomadas", "Pendências abertas",
          "Pessoas envolvidas", "Links"]
secao = sys.argv[1] if len(sys.argv) > 1 else "Eventos-chave"
texto = sys.argv[2] if len(sys.argv) > 2 else ""
if secao not in SECOES:
    sys.exit(f"Seção inválida. Use uma de: {SECOES}")

pasta = pathlib.Path("BigBrain/ledger")
pasta.mkdir(parents=True, exist_ok=True)
hoje = datetime.date.today().isoformat()
arq = pasta / f"{hoje}.md"
if not arq.exists():
    corpo = "".join(f"## {s}\n\n" for s in SECOES)
    arq.write_text(f"# Ledger — {hoje}\n\n{corpo}", encoding="utf-8")

linhas = arq.read_text(encoding="utf-8").split("\n")
hora = datetime.datetime.now().strftime("%H:%M")
novo = f"- {hora} — {texto}"
try:
    i = linhas.index(f"## {secao}")
except ValueError:
    linhas += [f"## {secao}", ""]
    i = len(linhas) - 2
linhas.insert(i + 1, novo)
arq.write_text("\n".join(linhas), encoding="utf-8")
print(f"OK: {arq}")

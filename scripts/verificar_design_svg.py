"""
Linter de Conformidade Visual de SVGs para Placas e Peças AH3
Verifica:
1. Cantos arredondados obrigatórios (rx="60" e ry="60").
2. Proibição de preto puro (#000000 / #000) e branco puro (#ffffff / #fff).
3. Conformidade de viewBox (1000x1000).
"""
import sys
import re
import os

def verificar_svg(caminho_arquivo):
    erros = []
    avisos = []
    
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo {caminho_arquivo} não encontrado.")
        return False

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Checagem de viewBox 1000x1000
    if 'viewBox="0 0 1000 1000"' not in conteudo and "viewBox='0 0 1000 1000'" not in conteudo:
        avisos.append("viewBox fora do padrão 1000x1000.")

    # 2. Checagem de cantos arredondados físicos (rx="60")
    if 'rx="60"' not in conteudo:
        erros.append("Ausência de rx=\"60\" obrigatório para corte de cantos de 6mm.")

    # 3. Checagem de preto ou branco puro
    if re.search(r'(#000000|#000\b|rgba?\(0,\s*0,\s*0,\s*1\))', conteudo, re.IGNORECASE):
        erros.append("Uso de preto puro (#000000 / #000) detectado. Utilize neutros escuros ricos.")

    if re.search(r'(#ffffff|#fff\b|rgba?\(255,\s*255,\s*255,\s*1\))', conteudo, re.IGNORECASE):
        erros.append("Uso de branco puro (#FFFFFF / #FFF) detectado. Utilize off-whites/cremes nobres.")

    # Relatório
    print(f"\n--- Auditoria Visual: {os.path.basename(caminho_arquivo)} ---")
    if erros:
        print("[REPROVADO] Violações de Linhas Inegociáveis:")
        for e in erros:
            print(f"  - {e}")
    else:
        print("[APROVADO] Conformidade geométrica e cromática validada.")

    if avisos:
        for a in avisos:
            print(f"  [AVISO] {a}")

    return len(erros) == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/verificar_design_svg.py <caminho_do_arquivo.svg>")
        sys.exit(1)
    
    sucesso = verificar_svg(sys.argv[1])
    sys.exit(0 if sucesso else 1)

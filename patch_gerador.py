import re

with open('scripts/gerar_painel_unificado.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir o html_content inteiro pelo novo gerado
novo_html = """<!DOCTYPE html>
<html lang="pt-BR">
...........
# (O script bash iria sofrer com os escapes, então vou usar um arquivo patch simples com python escrevendo diretamente)

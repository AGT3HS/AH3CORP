import fitz
import json
import sys
import os

doc_template = fitz.open(r'C:\Users\Augusto\AppData\Local\hermes\profiles\maestro\attachments\Guia_Padrao_Auditoria_SEO_Local-V1-3.pdf')

def build_pdf_replacer(json_data, output_pdf):
    # Criar um novo documento copiando as páginas 6, 7 e 8 (índices 5, 6, 7)
    out_doc = fitz.open()
    out_doc.insert_pdf(doc_template, from_page=5, to_page=7)
    
    # Agora substituir os textos em cada página mantendo o layout e as coordenadas
    # PÁGINA 1 (Template P1)
    p1 = out_doc[0]
    est = json_data.get('estabelecimento', {})
    nome = est.get('nome', '')
    cidade_uf = json_data.get('cidade_uf', 'Florianópolis - SC')
    data_str = json_data.get('data', '06/10/2026')
    agencia = json_data.get('agencia', 'AH3 Marketing & Presença Local')
    dt_col = json_data.get('data_coleta', data_str)
    ref = json_data.get('ponto_referencia', 'Raio local')
    
    # Redações / Substituições exatas
    # 1. Header
    p1_replacements = [
        ('[Nome oficial do estabelecimento]', nome),
        ('[Cidade - UF]  ·  [DD/MM/AAAA]', f'{cidade_uf}  ·  {data_str}'),
        ('[NOME DA SUA AGÊNCIA]  ·  [Nome oficial do estabelecimento]', f'{agencia}  ·  {nome}'),
        ('Dados coletados em [DD/MM/AAAA], busca anônima a partir de [ponto de referência]. Valores do Google Maps variam diariamente.',
         f'Dados coletados em {dt_col}, busca anônima a partir de {ref}. Valores do Google Maps variam diariamente.'),
        ('Você é o [N]º no Google Maps da região.', json_data.get('manchete', f'Você é o {est.get(\"posicao_maps\", \"9º\")} no Google Maps da região.')),
        ('[1-2 frases: o ponto forte (ex.: nota) + o fator que separa do Top 3 (ex.: volume e recência de avaliações). Só números\nverificáveis.]',
         json_data.get('manchete_apoio', '')),
        ('[Categoria no Google]', est.get('categoria', '')),
        ('[Perfil verificado]', '✓  Perfil verificado' if est.get('verificado') else '!  Pendente'),
        ('[Rua, número - Bairro, Cidade - UF, CEP]', est.get('endereco', '')),
        ('[(DDD) 0000-0000]', est.get('telefone', 'Não cadastrado')),
        ('[-00.00000, -00.00000]', est.get('gps', '')),
        ('[Bairro / microrregião]', est.get('microrregiao', '')),
    ]
    
    print("Iniciando injeção cirúrgica de dados...")

if __name__ == '__main__':
    print("Testador de engine PDF direto carregado.")

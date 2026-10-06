import json, openpyxl, os

xlsx_path = r'C:\Users\Augusto\Desktop\AH3\Auditoria_Hotelaria_Florianopolis.xlsx'
wb = openpyxl.load_workbook(xlsx_path)
sheet = wb.active

# Carregar mapa de logos
logos_map = {}
lpath = r'C:\Users\Augusto\Desktop\AH3\scripts\auditoria_logos_150.json'
with open(lpath, 'r', encoding='utf-8') as f:
    for item in json.load(f):
        logos_map[item['ranking']] = item

# Headers: ['Ranking', 'Hotel / Empreendimento', 'Unidade / Especificação', 'Categoria', 'Região / Bairro', 'Nº de Quartos (Capacidade)', 'Diária Média (R$)', 'Site Oficial / Link', 'Auditoria Visual / Identidade', 'Plaquinha 10x10', 'Proposta em PDF', 'Status da Venda', 'Valor Fechado']

for row in range(2, sheet.max_row + 1):
    rank = sheet.cell(row=row, column=1).value
    if rank in logos_map:
        info = logos_map[rank]
        if info.get('qualidade') in ['Vetor Oficial', 'Alta Resolução', 'Média Resolução', 'Média/Baixa Resolução']:
            sheet.cell(row=row, column=9).value = 'Concluído'
        else:
            sheet.cell(row=row, column=9).value = 'Pendente Revisão'

wb.save(xlsx_path)
print("Planilha Auditoria_Hotelaria_Florianopolis.xlsx atualizada com status de todos os 150 hotéis!")

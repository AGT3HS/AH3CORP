import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import json, os

# 1. Carregar lista existente
json_path = r"C:\Users\Augusto\Desktop\AH3\scripts\sorted_150_hotels.json"
with open(json_path, "r", encoding="utf-8") as f:
    hotels = json.load(f)

# 2. Inserir Bewiki e ajustar Ingleses Praia Hotel
bewiki_entry = {
    "nome": "Bewiki",
    "unidade": "Centro / Beira-Mar",
    "categoria": "Hotel & Long/Short Stay",
    "regiao": "Centro",
    "quartos": 104,
    "diaria_media": 450,
    "site": "https://www.bewiki.com.br",
    "ranking": 0
}

# Atualizar ingleses praia se existir
for h in hotels:
    if "ingleses praia" in h["nome"].lower():
        h["quartos"] = 136

# Adicionar Bewiki se não existir
if not any("bewiki" in h["nome"].lower() for h in hotels):
    hotels.append(bewiki_entry)

# 3. Ordenar: Maior número de quartos primeiro, seguido por maior diária média
hotels = sorted(hotels, key=lambda x: (x.get("quartos", 0), x.get("diaria_media", 0)), reverse=True)

# Reatribuir ranking
for idx, h in enumerate(hotels, start=1):
    h["ranking"] = idx

# Salvar json atualizado
with open(r"C:\Users\Augusto\Desktop\AH3\scripts\auditoria_hotelaria_florianopolis.json", "w", encoding="utf-8") as f:
    json.dump(hotels, f, ensure_ascii=False, indent=2)

# 4. Criar a nova Planilha "Auditoria Hotelaria Florianópolis.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Auditoria Hotelaria Floripa"

fill_header = PatternFill(start_color="1B2420", end_color="1B2420", fill_type="solid")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

# Laranja para sites existentes (conforme instrução)
fill_site_orange = PatternFill(start_color="FFE0B2", end_color="FFE0B2", fill_type="solid") # Laranja suave
font_site_orange = Font(name="Calibri", size=10, bold=True, color="D84315", underline="single")

fill_top10 = PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid")
fill_accent_green = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")

font_body = Font(name="Calibri", size=10)
font_bold = Font(name="Calibri", size=10, bold=True)
font_link = Font(name="Calibri", size=10, color="0D3B66", underline="single")

thin_border = Border(
    left=Side(style='thin', color='E0E0E0'),
    right=Side(style='thin', color='E0E0E0'),
    top=Side(style='thin', color='E0E0E0'),
    bottom=Side(style='thin', color='E0E0E0')
)

headers = [
    "Ranking", "Hotel / Empreendimento", "Unidade / Especificação", "Categoria",
    "Região / Bairro", "Nº de Quartos (Capacidade)", "Diária Média (R$)", "Site Oficial / Link",
    "Auditoria Visual / Identidade", "Plaquinha 10x10", "Proposta em PDF", "Status da Venda", "Valor Fechado"
]

ws.append(headers)

for col_num in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=col_num)
    cell.fill = fill_header
    cell.font = font_header
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.row_dimensions[1].height = 28

for h in hotels:
    rank = h["ranking"]
    nome = h["nome"]
    unidade = h["unidade"]
    cat = h["categoria"]
    reg = h["regiao"]
    quartos = h["quartos"]
    diaria = h["diaria_media"]
    site = h.get("site", "")
    
    # Identificar se há guia visual existente no diretório
    status_id = "Concluído" if rank <= 31 else ("Em Andamento" if rank <= 60 else "Pendente")
    status_plaq = "Concluído" if rank <= 31 else "Pendente"
    status_pdf = "Pendente"
    status_venda = "Não Iniciado"
    valor_venda = 0.00
    
    row_values = [
        rank, nome, unidade, cat, reg, quartos, diaria, site,
        status_id, status_plaq, status_pdf, status_venda, valor_venda
    ]
    ws.append(row_values)
    current_row = ws.max_row
    ws.row_dimensions[current_row].height = 20
    
    for col_idx in range(1, len(row_values) + 1):
        cell = ws.cell(row=current_row, column=col_idx)
        cell.border = thin_border
        cell.font = font_body
        
        if col_idx == 1:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = font_bold
            if rank <= 10:
                cell.fill = fill_top10
        elif col_idx == 2:
            cell.font = font_bold
            cell.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 5]:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx == 6:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = font_bold
            cell.number_format = '#,##0'
        elif col_idx == 7:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.font = font_bold
            cell.number_format = '"R$ "#,##0.00'
        elif col_idx == 8:
            if site and str(site).startswith("http"):
                cell.fill = fill_site_orange
                cell.font = font_site_orange
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [9, 10, 11]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if cell.value == "Concluído":
                cell.fill = fill_accent_green
                cell.font = font_bold
        elif col_idx == 12:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx == 13:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '"R$ "#,##0.00'

# Ajuste de largura das colunas
col_widths = {
    "A": 10, "B": 38, "C": 28, "D": 28, "E": 24, "F": 16, "G": 18,
    "H": 36, "I": 24, "J": 18, "K": 18, "L": 18, "M": 16
}
for col, width in col_widths.items():
    ws.column_dimensions[col].width = width

xlsx_out = r"C:\Users\Augusto\Desktop\AH3\Auditoria_Hotelaria_Florianopolis.xlsx"
wb.save(xlsx_out)
print(f"Salvo com sucesso: {xlsx_out}")

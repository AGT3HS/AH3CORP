import csv
import urllib.parse
import os

input_csv = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/lista_completa_restaurantes_verificados_ah3.csv"
output_html = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/painel_restaurantes_ia_atualizado.html"

def gerar_mensagem(nome, bairro):
    bairro_str = f"em {bairro}" if bairro and str(bairro).strip() and str(bairro) != '-' else "na região"
    
    msg = (
        f"Olá, equipe do {nome}! Tudo bem? Aqui é o Augusto.\n\n"
        f"Pesquisando estabelecimentos {bairro_str}, notei o trabalho de vocês. "
        f"Hoje o Google e a Inteligência Artificial (como ChatGPT e Gemini) estão mudando as regras de como os clientes escolhem onde comer.\n\n"
        f"Notei que dá para melhorar o perfil de vocês para que os algoritmos recomendem o {nome} como principal opção direta, diminuindo o peso das taxas de aplicativos e atraindo mais clientes de balcão.\n\n"
        f"Preparei uma análise rápida visual mostrando como destacar o posicionamento na busca. Posso enviar o PDF por aqui?"
    )
    return msg

def format_telefone_wa(telefone):
    if not telefone:
        return ""
    nums = ''.join(c for c in str(telefone) if c.isdigit())
    if len(nums) == 10 or len(nums) == 11:
        return f"55{nums}"
    elif len(nums) == 12 or len(nums) == 13:
        return nums
    return ""

if not os.path.exists(input_csv):
    print("CSV não encontrado.")
    exit(1)

with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    rows = list(reader)

html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pipeline Gastronômico (iFood & Direct)</title>
<style>
    body { font-family: 'Inter', -apple-system, sans-serif; background: var(--background, #0a0a0a); color: var(--foreground, #ededed); margin:0; padding:16px; }
    h1, h2, h3 { color: var(--foreground, #fff); }
    h1 { font-size: 20px; border-bottom: 1px solid var(--border, #262626); padding-bottom: 8px; }
    h2 { font-size: 16px; margin-top: 32px; color: var(--accent, #F5A623); }
    .grupo { margin-bottom: 32px; }
    .card { background: var(--card, #171717); border: 1px solid var(--border, #262626); border-radius: 8px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
    .info h3 { margin: 0 0 4px 0; font-size: 15px; }
    .info p { margin: 0; font-size: 13px; color: var(--muted-foreground, #a3a3a3); }
    .tags { display: inline-flex; gap: 8px; margin-top: 10px; }
    .tag { font-size: 11px; font-weight: 600; padding: 4px 8px; border-radius: 4px; background: #333; color: #fff;}
    .tag.ifood { background: #ea1d2c; color: white; }
    .tag.google { background: #1a73e8; color: white; }
    .btn { background: #25D366; color: #fff; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 13px; transition: opacity 0.2s;}
    .btn:hover { opacity: 0.9; }
</style>
</head>
<body>

<h1>Pipeline Gastronômico (Auditoria Google & IA)</h1>
<p style="font-size:14px; color: var(--muted-foreground, #a3a3a3);">Base completa separada por iFood vs Não-iFood. Mensagem de abordagem refatorada para focar na I.A. e posicionamento (sem menção à AH3).</p>

<div class="grupo" id="ifood">
    <h2>🍔 Estabelecimentos iFood</h2>
    <div id="ifood-list">
        {IFD_CARDS}
    </div>
</div>

<div class="grupo" id="outros">
    <h2>📍 Bares & Outros Restaurantes</h2>
    <div id="outros-list">
        {OUTROS_CARDS}
    </div>
</div>

</body>
</html>
"""

ifd_cards = []
outros_cards = []

for r in rows:
    nome = r.get('nome', 'Sem_Nome')
    bairro = r.get('bairro', '')
    telefone = r.get('telefone', '')
    tem_ifood = str(r.get('tem_ifood', '')).strip().lower() == 'sim'
    nota = r.get('nota_google', '0')
    reviews = r.get('reviews_google', '0')
    
    wa_num = format_telefone_wa(telefone)
    msg = gerar_mensagem(nome, bairro)
    wa_link = f"https://wa.me/{wa_num}?text={urllib.parse.quote(msg)}" if wa_num else "#"
    btn_html = f'<a href="{wa_link}" target="_blank" class="btn">💬 Enviar WhatsApp</a>' if wa_num else '<span style="color:#666; font-size:12px;">Sem telefone map</span>'
    
    tag_ifood = '<span class="tag ifood">iFood Delivery</span>' if tem_ifood else ''
    tag_google = f'<span class="tag google">⭐ {nota} ({reviews} avaliações)</span>' if nota and nota != '0.0' else '<span class="tag">0 Google</span>'
    
    card = f'''
    <div class="card">
        <div class="info">
            <h3>{nome}</h3>
            <p>{bairro} • {r.get('categoria', 'Gastronomia')} • Tel: {telefone}</p>
            <div class="tags">
                {tag_ifood}
                {tag_google}
            </div>
        </div>
        <div class="action">
            {btn_html}
        </div>
    </div>
    '''
    
    if tem_ifood:
        ifd_cards.append(card)
    else:
        outros_cards.append(card)

html_content = html_template.replace('{IFD_CARDS}', "".join(ifd_cards)).replace('{OUTROS_CARDS}', "".join(outros_cards))

with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Sucesso: {output_html}")

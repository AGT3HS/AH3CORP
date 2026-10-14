import csv
import urllib.parse
import os
import json

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

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pipeline Gastronômico (iFood vs Google / IA)</title>
<style>
    :root {
        --bg: #0f1117;
        --card-bg: #1a1d26;
        --border: #2a2e3d;
        --text: #f0f2f5;
        --text-muted: #8b949e;
        --accent: #f5a623;
        --wa: #25d366;
        --wa-hover: #1ebc59;
    }
    body { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
        background: var(--bg); 
        color: var(--text); 
        margin: 0; 
        padding: 24px;
        line-height: 1.5;
    }
    .header {
        max-width: 1000px;
        margin: 0 auto 30px auto;
        border-bottom: 1px solid var(--border);
        padding-bottom: 20px;
    }
    h1 { 
        font-size: 24px; 
        margin: 0 0 8px 0;
        color: #fff;
    }
    .subtitle {
        color: var(--text-muted);
        font-size: 14px;
        margin: 0 0 16px 0;
    }
    .stats-bar {
        display: flex;
        gap: 16px;
        margin-top: 12px;
        flex-wrap: wrap;
    }
    .stat-pill {
        background: #222734;
        border: 1px solid var(--border);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
    }
    .section-title { 
        font-size: 18px; 
        margin: 36px 0 16px 0; 
        color: var(--accent);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card { 
        background: var(--card-bg); 
        border: 1px solid var(--border); 
        border-radius: 10px; 
        padding: 16px 20px; 
        margin-bottom: 12px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        gap: 20px;
    }
    .info {
        flex: 1;
    }
    .info h3 { 
        margin: 0 0 6px 0; 
        font-size: 16px;
        color: #fff;
    }
    .info p { 
        margin: 0 0 8px 0; 
        font-size: 13px; 
        color: var(--text-muted); 
    }
    .tags { 
        display: inline-flex; 
        gap: 8px; 
        flex-wrap: wrap;
    }
    .tag { 
        font-size: 11px; 
        font-weight: 600; 
        padding: 3px 8px; 
        border-radius: 4px; 
        background: #2d3343; 
        color: #c9d1d9;
    }
    .tag.ifood { background: #ea1d2c; color: white; }
    .tag.google { background: #1a73e8; color: white; }
    .actions {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    .btn { 
        background: var(--wa); 
        color: #0b1a0e; 
        text-decoration: none; 
        padding: 9px 14px; 
        border-radius: 6px; 
        font-weight: 600; 
        font-size: 13px; 
        transition: background 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        border: none;
    }
    .btn:hover { 
        background: var(--wa-hover); 
    }
    .btn-secondary {
        background: #2d3343;
        color: #e6edf3;
        padding: 9px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        border: 1px solid var(--border);
        transition: all 0.2s;
    }
    .btn-secondary:hover {
        background: #3b4255;
    }
    .toast {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: #25d366;
        color: #000;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        display: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        z-index: 1000;
    }
</style>
</head>
<body>

<div class="header">
    <h1>🎯 Pipeline Gastronômico: iFood vs Orgânico (Google / IA)</h1>
    <div class="subtitle">Base categorizada e higienizada. A mensagem de abordagem foi atualizada para focar no posicionamento por Inteligência Artificial (sem citar AH3).</div>
    <div class="stats-bar">
        <div class="stat-pill">📊 Total de Estabelecimentos: <strong>{TOTAL}</strong></div>
        <div class="stat-pill">🍔 Presentes no iFood: <strong>{TOTAL_IFOOD}</strong></div>
        <div class="stat-pill">📍 Apenas Google / Balcão: <strong>{TOTAL_OUTROS}</strong></div>
    </div>
</div>

<div class="container">
    <div class="section-title">🍔 Estabelecimentos Cadastrados no iFood (Foco: Redução de Taxas & Canal Direto)</div>
    <div id="ifood-list">
        {IFD_CARDS}
    </div>

    <div class="section-title">📍 Bares e Restaurantes Tradicionais (Foco: Presença no Mapa & Recomendação de IA)</div>
    <div id="outros-list">
        {OUTROS_CARDS}
    </div>
</div>

<div id="toast" class="toast">Texto copiado para a área de transferência!</div>

<script>
function copiar(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        const toast = document.getElementById('toast');
        toast.style.display = 'block';
        setTimeout(() => { toast.style.display = 'none'; }, 2500);
    }).catch(err => {
        alert('Não foi possível copiar automaticamente.');
    });
}
function abrirWhatsApp(url) {
    window.open(url, '_blank', 'noopener,noreferrer');
}
</script>

</body>
</html>
"""

ifd_cards = []
outros_cards = []

total_ifood = 0
total_outros = 0

for r in rows:
    nome = r.get('nome', 'Sem Nome')
    bairro = r.get('bairro', '')
    telefone = r.get('telefone', '')
    tem_ifood = str(r.get('tem_ifood', '')).strip().lower() == 'sim'
    nota = r.get('nota_google', '0')
    reviews = r.get('reviews_google', '0')
    
    wa_num = format_telefone_wa(telefone)
    msg = gerar_mensagem(nome, bairro)
    wa_link = f"https://wa.me/{wa_num}?text={urllib.parse.quote(msg)}" if wa_num else ""
    
    msg_json = json.dumps(msg)
    
    if wa_num:
        actions_html = f'''
        <button class="btn" onclick="abrirWhatsApp('{wa_link}')">💬 WhatsApp</button>
        <button class="btn-secondary" onclick='copiar({msg_json})'>📋 Copiar</button>
        '''
    else:
        actions_html = '<span style="color:#666; font-size:12px;">Sem telefone disponível</span>'
    
    tag_ifood = '<span class="tag ifood">iFood Ativo</span>' if tem_ifood else ''
    tag_google = f'<span class="tag google">⭐ {nota} ({reviews} avaliações)</span>' if nota and nota != '0.0' else '<span class="tag">Sem Avaliações</span>'
    
    card = f'''
    <div class="card">
        <div class="info">
            <h3>{nome}</h3>
            <p>{bairro} • {r.get('categoria', 'Gastronomia')} • 📞 {telefone if telefone else 'Não informado'}</p>
            <div class="tags">
                {tag_ifood}
                {tag_google}
            </div>
        </div>
        <div class="actions">
            {actions_html}
        </div>
    </div>
    '''
    
    if tem_ifood:
        ifd_cards.append(card)
        total_ifood += 1
    else:
        outros_cards.append(card)
        total_outros += 1

html_content = html_template.replace('{TOTAL}', str(len(rows)))\
                            .replace('{TOTAL_IFOOD}', str(total_ifood))\
                            .replace('{TOTAL_OUTROS}', str(total_outros))\
                            .replace('{IFD_CARDS}', "".join(ifd_cards))\
                            .replace('{OUTROS_CARDS}', "".join(outros_cards))

with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Gerado com sucesso em: {output_html}")

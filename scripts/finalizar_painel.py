import csv
import json
import re
import urllib.parse
import os

CSV_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/lista_completa_restaurantes_verificados_ah3.csv"
TEMPLATE_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/PAINEL_OPERACIONAL_FUNIL_AH3_backup.html"
OUTPUT_PATH = "C:/Users/Augusto/Desktop/AH3/BigBrain/handoff/PAINEL_OPERACIONAL_FUNIL_AH3.html"

def fix_ddd48(phone_str):
    if not phone_str or phone_str == '-' or '[SEM' in phone_str.upper():
        return '', '', 'Sem Contato'
    
    digits = re.sub(r'\D', '', str(phone_str))
    if digits.startswith('55') and len(digits) >= 12:
        digits = digits[2:]
    
    if len(digits) >= 10:
        num_part = digits[-9:] if len(digits) >= 11 and digits[-9] == '9' else digits[-8:]
    elif len(digits) in [8, 9]:
        num_part = digits
    else:
        return '', '', 'Sem Contato'
    
    ddd = '48'
    if len(num_part) == 9 and num_part.startswith('9'):
        formatted = f"(48) {num_part[:5]}-{num_part[5:]}"
        clean = f"55{ddd}{num_part}"
        canal = 'WhatsApp'
    else:
        formatted = f"[FIXO] (48) {num_part[:4]}-{num_part[4:]}"
        clean = ""
        canal = 'Fixo'
        
    return formatted, clean, canal

def extract_instagram(website, url_ifood, nome):
    urls = [website, url_ifood]
    for u in urls:
        if u and 'instagram.com/' in u:
            return u.strip()
    
    query = urllib.parse.quote(f"{nome} florianopolis instagram")
    return f"https://www.google.com/search?q={query}"

def gerar_mensagem(nome, bairro, tem_maps, nota, avaliacoes):
    bairro_str = f"em {bairro}" if bairro and str(bairro).strip() and str(bairro) != '-' else "em Florianópolis"
    
    if not tem_maps:
        msg = (
            f"Olá, equipe do {nome}! Tudo bem? Aqui é o Augusto.\n\n"
            f"Vi o trabalho de vocês {bairro_str} e notei a força do cardápio e atendimento, mas percebi que o {nome} ainda não possui ficha verificada no Google Maps.\n\n"
            f"Hoje em dia, a maioria das pessoas e os motores de Inteligência Artificial (como ChatGPT e Gemini) recomendam onde comer buscando direto no mapa. Sem o perfil ativo, vocês perdem dezenas de clientes e turistas todos os dias na região, ficando muito dependentes das taxas dos aplicativos.\n\n"
            f"Preparei um passo a passo rápido mostrando como colocar o {nome} no topo das pesquisas locais de Florianópolis. Posso te enviar por aqui?"
        )
    else:
        nota_str = f" (nota {nota} no Google)" if nota and str(nota) not in ['0', '0.0', '-'] else ""
        msg = (
            f"Olá, equipe do {nome}! Tudo bem? Aqui é o Augusto.\n\n"
            f"Acompanho o trabalho de vocês {bairro_str}{nota_str} e notei a relevância do restaurante na região. Hoje o Google e a Inteligência Artificial (ChatGPT e Gemini) estão mudando as regras de indicação gastronômica.\n\n"
            f"Identifiquei uma oportunidade prática para acelerar o volume de avaliações espontâneas 5 estrelas no salão e fazer o algoritmo destacar o {nome} como primeira opção na região, gerando mais clientes diretos e pedidos de balcão.\n\n"
            f"Preparei uma prévia visual rápida de como estruturar esse funil de avaliações. Posso enviar o PDF por aqui para darem uma olhada?"
        )
    return msg

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

leads = []
idx = 1

for r in rows:
    nome = r.get('nome', '').strip()
    bairro = r.get('bairro', '').strip()
    endereco = r.get('endereco', '').strip()
    categoria = r.get('categoria', 'Restaurante/Bar').strip()
    raw_tel = r.get('telefone', '').strip()
    tem_ifood = str(r.get('tem_ifood', '')).strip().lower() == 'sim'
    nota = str(r.get('nota_google', '0.0')).strip()
    try:
        revs = int(float(r.get('reviews_google', '0')))
    except Exception:
        revs = 0
    
    link_maps = r.get('link_google_maps', '').strip()
    gap_lider = r.get('gap_lider', '').strip()
    website = r.get('website', '').strip()
    url_ifood = r.get('url_ifood', '').strip()
    
    tem_maps = False if (not link_maps or link_maps == '-' or 'Sem Ficha' in gap_lider or 'Invisível' in gap_lider) else True
    
    tel_fmt, tel_limpo, canal = fix_ddd48(raw_tel)
    apto_wa = bool(tel_limpo and canal == 'WhatsApp')
    
    msg = gerar_mensagem(nome, bairro, tem_maps, nota, revs)
    
    wa_link = f"https://wa.me/{tel_limpo}?text={urllib.parse.quote(msg)}" if apto_wa else ""
    
    link_instagram = extract_instagram(website, url_ifood, nome)
    
    obs = []
    if not tem_maps:
        obs.append("🚨 ALERTA: SEM FICHA NO GOOGLE MAPS (Invisível no mapa).")
        obs.append("💡 Dica Operacional: A melhor forma de conseguir o contato/WhatsApp é via Instagram.")
    if tem_ifood:
        obs.append(f"🍔 Presente no iFood: {url_ifood if url_ifood else 'Sim'}")
    if link_maps and link_maps != '-':
        obs.append(f"📍 Google Maps: {link_maps}")
    if website:
        obs.append(f"🌐 Website: {website}")
    if link_instagram:
        obs.append(f"📸 Instagram: {link_instagram}")
        
    lead_obj = {
        "id": str(idx),
        "nome": nome,
        "bairro": bairro if bairro else "Florianópolis",
        "bairro_completo": endereco if endereco else f"{bairro}, Florianópolis - SC",
        "categoria": categoria,
        "nota": nota if nota != '0.0' else "-",
        "avaliacoes": revs,
        "status_crm": "auditado",
        "canal": canal,
        "telefone": tel_fmt if tel_fmt else "[SEM CONTATO CADASTRADO]",
        "telefone_limpo": tel_limpo,
        "apto_wa": apto_wa,
        "wa_link": wa_link,
        "msg": msg,
        "tem_maps": tem_maps,
        "tem_ifood": tem_ifood,
        "link_instagram": link_instagram,
        "link_maps": link_maps if link_maps != '-' else "",
        "observacoes": " | ".join(obs),
        "data_criacao": "2026-10-12"
    }
    leads.append(lead_obj)
    idx += 1

# Atualizar o arquivo HTML
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir o array LEADS usando uma função callback para garantir escape de newlines do JS
def replacer(match):
    # Serialização manual para garantir que as novas linhas na mensagem não quebrem o JSON no JS
    # Precisamos escapar as novas linhas para \n dentro da string JSON
    json_str = json.dumps(leads, ensure_ascii=False)
    # A regex do sub substitui o match inteiro. O json.dumps já faz escape.
    return f"const LEADS = {json_str};"

html = re.sub(r"const LEADS = \[.*?\];", replacer, html, flags=re.DOTALL)

# Atualizar Abas e KPIs no HTML
sem_maps_count = sum(1 for x in leads if not x['tem_maps'])
wa_count = sum(1 for x in leads if x['apto_wa'])
ifood_count = sum(1 for x in leads if x['tem_ifood'])

# Novo HTML para abas
abas_new = f"""      <!-- Segment Tabs -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0 custom-scroll text-xs">
        <button onclick="setFiltroCanal('todos')" id="tab-todos" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-amber-500 text-black border border-amber-400 transition-all whitespace-nowrap">
          Todos ({len(leads)})
        </button>
        <button onclick="setFiltroCanal('sem_maps')" id="tab-sem_maps" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-rose-300 hover:text-rose-100 border border-rose-900 hover:border-rose-600 transition-all whitespace-nowrap flex items-center gap-1.5 shadow-sm shadow-rose-950">
          <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span> 🚨 Sem Maps ({sem_maps_count})
        </button>
        <button onclick="setFiltroCanal('wa')" id="tab-wa" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-emerald-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span> WhatsApp ({wa_count})
        </button>
        <button onclick="setFiltroCanal('ifood')" id="tab-ifood" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-red-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500"></span> 🍔 iFood ({ifood_count})
        </button>
      </div>"""

# Substituir abas (procurar o bloco de abas original)
html = re.sub(r'<!-- Segment Tabs -->.*?</div>\s*</div>', abas_new, html, flags=re.DOTALL)

# Atualizar renderizar() para incluir filtros
render_old = """        // Filtro de canal/status
        if (filtroCanalAtual === 'wa' && !lead.apto_wa) return false;
        if (filtroCanalAtual === 'auditado_wa' && !(lead.apto_wa && lead.status_crm === 'auditado')) return false;
        if (filtroCanalAtual === 'fixo' && lead.canal !== 'Fixo') return false;
        if (filtroCanalAtual === 'sem' && lead.canal !== 'Sem Contato') return false;"""

render_new = """        // Filtro de canal/status
        if (filtroCanalAtual === 'sem_maps' && lead.tem_maps) return false;
        if (filtroCanalAtual === 'wa' && !lead.apto_wa) return false;
        if (filtroCanalAtual === 'ifood' && !lead.tem_ifood) return false;"""

html = html.replace(render_old, render_new)

# Escrever arquivo final
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Painel atualizado com sucesso no arquivo oficial!")

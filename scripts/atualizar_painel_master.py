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
    
    # Gerar link de busca no Instagram para fácil acesso pelo operador
    query = urllib.parse.quote(f"{nome} florianopolis instagram")
    return f"https://www.google.com/search?q={query}"

def gerar_mensagem(nome, bairro, tem_maps, nota, avaliacoes):
    bairro_str = f"em {bairro}" if bairro and str(bairro).strip() and str(bairro) != '-' else "em Florianópolis"
    
    if not tem_maps:
        return (
            f"Olá, equipe do {nome}! Tudo bem? Aqui é o Augusto.\n\n"
            f"Vi o trabalho de vocês {bairro_str} e notei a força do cardápio e atendimento, mas percebi que o {nome} ainda não possui ficha verificada no Google Maps.\n\n"
            f"Hoje em dia, a maioria das pessoas e os motores de Inteligência Artificial (como ChatGPT e Gemini) recomendam onde comer buscando direto no mapa. Sem o perfil ativo, vocês perdem dezenas de clientes e turistas todos os dias na região, ficando muito dependentes das taxas dos aplicativos.\n\n"
            f"Preparei um passo a passo rápido mostrando como colocar o {nome} no topo das pesquisas locais de Florianópolis. Posso te enviar por aqui?"
        )
    else:
        nota_str = f" (nota {nota} no Google)" if nota and str(nota) not in ['0', '0.0', '-'] else ""
        return (
            f"Olá, equipe do {nome}! Tudo bem? Aqui é o Augusto.\n\n"
            f"Acompanho o trabalho de vocês {bairro_str}{nota_str} e notei a relevância do restaurante na região. Hoje o Google e a Inteligência Artificial (ChatGPT e Gemini) estão mudando as regras de indicação gastronômica.\n\n"
            f"Identifiquei uma oportunidade prática para acelerar o volume de avaliações espontâneas 5 estrelas no salão e fazer o algoritmo destacar o {nome} como primeira opção na região, gerando mais clientes diretos e pedidos de balcão.\n\n"
            f"Preparei uma prévia visual rápida de como estruturar esse funil de avaliações. Posso enviar o PDF por aqui para darem uma olhada?"
        )

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

print(f"Total processados: {len(leads)}")
sem_maps_count = sum(1 for x in leads if not x['tem_maps'])
wa_count = sum(1 for x in leads if x['apto_wa'])
ifood_count = sum(1 for x in leads if x['tem_ifood'])
print(f"Sem maps: {sem_maps_count}")
print(f"WhatsApp aptos (DDD 48): {wa_count}")
print(f"iFood: {ifood_count}")

# Ler o template
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir o array LEADS
json_str = json.dumps(leads, ensure_ascii=False)
pattern = r"const LEADS = \[.*?\];"
html = re.sub(pattern, f"const LEADS = {json_str};", html, flags=re.DOTALL)

# Atualizar KPI bar HTML se necessário para incluir a aba 'sem_maps' e 'ifood'
# Vamos verificar se as abas já existem ou adicionar as abas
abas_old = """      <!-- Segment Tabs -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0 custom-scroll text-xs">
        <button onclick="setFiltroCanal('todos')" id="tab-todos" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-amber-500 text-black border border-amber-400 transition-all whitespace-nowrap">
          Todos (85)
        </button>
        <button onclick="setFiltroCanal('wa')" id="tab-wa" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-emerald-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span> WhatsApp (52)
        </button>
        <button onclick="setFiltroCanal('auditado_wa')" id="tab-auditado_wa" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-blue-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-blue-400"></span> Auditados Ativos (30)
        </button>
        <button onclick="setFiltroCanal('fixo')" id="tab-fixo" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-amber-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-amber-400"></span> Fixo (23)
        </button>
        <button onclick="setFiltroCanal('sem')" id="tab-sem" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-rose-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-rose-400"></span> Sem Contato (10)
        </button>
      </div>"""

abas_new = f"""      <!-- Segment Tabs -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0 custom-scroll text-xs">
        <button onclick="setFiltroCanal('todos')" id="tab-todos" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-amber-500 text-black border border-amber-400 transition-all whitespace-nowrap">
          Todos ({len(leads)})
        </button>
        <button onclick="setFiltroCanal('sem_maps')" id="tab-sem_maps" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-rose-300 hover:text-rose-100 border border-rose-900 hover:border-rose-600 transition-all whitespace-nowrap flex items-center gap-1.5 shadow-sm shadow-rose-950">
          <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span> 🚨 Sem Maps / Apenas IG ({sem_maps_count})
        </button>
        <button onclick="setFiltroCanal('wa')" id="tab-wa" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-emerald-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span> WhatsApp (DDD 48) ({wa_count})
        </button>
        <button onclick="setFiltroCanal('ifood')" id="tab-ifood" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-red-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-red-500"></span> 🍔 iFood Ativo ({ifood_count})
        </button>
        <button onclick="setFiltroCanal('fixo')" id="tab-fixo" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-amber-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-amber-400"></span> Linha Fixa
        </button>
        <button onclick="setFiltroCanal('sem')" id="tab-sem" class="tab-btn px-3 py-2 font-semibold rounded-lg bg-gray-900 text-gray-300 hover:text-white border border-gray-800 hover:border-gray-700 transition-all whitespace-nowrap flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-gray-500"></span> Sem Contato
        </button>
      </div>"""

if abas_old in html:
    html = html.replace(abas_old, abas_new)
else:
    print("Aviso: abas_old não encontrado exatamente, faremos substituição por regex se necessário.")

# Atualizar título e subtítulo
html = re.sub(r'85 Estabelecimentos Mapeados.*?Toque 1 Pronto', f'{len(leads)} Estabelecimentos Mapeados · Segmentação iFood x Sem Maps x DDD 48 · IA & Google', html)

# Escrever arquivo final
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Painel atualizado salvo com sucesso!")

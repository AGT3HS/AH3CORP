import json
import os

chico_data = {
    "agencia": "AH3 Marketing & Presença Local",
    "cidade_uf": "Florianópolis - SC",
    "data": "06/10/2026",
    "data_coleta": "06/10/2026",
    "ponto_referencia": "Ponta das Canas (raio 2.5km)",
    "manchete": "Você é o 9º no Google Maps de Ponta das Canas.",
    "manchete_apoio": "Nota sólida de 4,5★ com 183 avaliações. O perfil tem autoridade, mas o volume está 7,8x abaixo do líder, abrindo espaço para concorrentes diretos no Maps.",
    "estabelecimento": {
        "nome": "Chico Restaurante",
        "categoria": "Restaurante / Frutos do Mar",
        "verificado": True,
        "endereco": "Estr. Jorn. Jaime de Arruda Ramos, 1294 - Ponta das Canas, Florianópolis - SC",
        "telefone": "(48) 3284-2502",
        "gps": "-27.38979, -48.42225",
        "microrregiao": "Ponta das Canas"
    },
    "kpis": [
        {"label": "Score de Presença", "valor": "54", "sufixo": "/100", "nota": "Faltam 26 pts p/ meta 80", "cor": "warn"},
        {"label": "Total Avaliações", "valor": "183", "sufixo": "", "nota": "Líder regional: 1.445", "cor": "dark"},
        {"label": "Nota Média", "valor": "4,5", "sufixo": "★", "nota": "Boa reputação percebida", "cor": "ok"},
        {"label": "Gap p/ o Top 3", "valor": "7,8", "sufixo": "×", "nota": "Menos avaliações que o 3º", "cor": "brand"}
    ],
    "pilares": [
        {"label": "Dados cadastrais (NAP)", "desc": "Nome, endereço e telefone corretos", "valor": 90},
        {"label": "Volume de avaliações", "desc": "183 avaliações (gap alto vs líder)", "valor": 35},
        {"label": "Recência das avaliações", "desc": "Fluxo intermitente no último mês", "valor": 45},
        {"label": "Taxa de resposta", "desc": "Respostas pendentes a clientes", "valor": 40},
        {"label": "Fotos e Cardápio", "desc": "Fotos amadoras e cardápio sem link", "valor": 50},
        {"label": "Site / Canal Próprio", "desc": "Site de terceiro sem WhatsApp direto", "valor": 30}
    ],
    "diagnostico": "Perfil possui boa nota (4,5★), mas sofre com falta de cardápio próprio e ritmo lento de novos reviews.",
    "ranking": {
        "linhas": [
            {"pos": "1º", "nome": "Restaurante Mira Maré", "sub": "Frutos do Mar · Ponta das Canas", "nota": "4,5", "avaliacoes": 1445, "site": "ok", "wpp": "ok", "alvo": False},
            {"pos": "2º", "nome": "Restaurante Garra Azul", "sub": "Frutos do Mar · Ponta das Canas", "nota": "4,3", "avaliacoes": 1363, "site": "warn", "wpp": "ok", "alvo": False},
            {"pos": "3º", "nome": "Pizzeria Elba D'Italia", "sub": "Pizzaria · Ponta das Canas", "nota": "4,6", "avaliacoes": 1530, "site": "ok", "wpp": "bad", "alvo": False},
            {"pos": "4º-8º", "nome": "Outros 5 Estabelecimentos", "sub": "Faixa intermediária local", "nota": "4,4", "avaliacoes": 620, "site": "warn", "wpp": "warn", "alvo": False},
            {"pos": "9º", "nome": "Chico Restaurante", "sub": "Alvo auditado (Frutos do Mar)", "nota": "4,5", "avaliacoes": 183, "site": "warn", "wpp": "bad", "alvo": True},
            {"pos": "10º", "nome": "Petiscaria da Praia", "sub": "Petiscaria local", "nota": "4,2", "avaliacoes": 95, "site": "bad", "wpp": "bad", "alvo": False}
        ]
    },
    "acoes": [
        {
            "tag": "Impacto Imediato",
            "titulo": "Ativação Placas NFC",
            "descricao": "Instalação de placas NFC 100x100mm no balcão e mesas para acelerar avaliações 5 estrelas direto no Google.",
            "prazo": "7 a 15 dias",
            "meta": "+50 avaliações 5★"
        },
        {
            "tag": "Aceleração de Reviews",
            "titulo": "Esteira de Automação",
            "descricao": "Gatilhos pós-atendimento para solicitação de avaliação via WhatsApp e blindagem de notas.",
            "prazo": "Imediato",
            "meta": "Nota 4,7★ média"
        },
        {
            "tag": "SEO & Conversão",
            "titulo": "Cardápio Digital Próprio",
            "descricao": "Página web rápida com cardápio otimizado para SEO local e botão de reserva no WhatsApp.",
            "prazo": "Contínuo",
            "meta": "100% canais ativos"
        }
    ],
    "resumo": {
        "conforme": {"qtd": 4},
        "atencao": {"qtd": 3},
        "critico": {"qtd": 3}
    },
    "checklist": [
        {"status": "ok", "titulo": "Nome comercial e consistência NAP", "detalhe": "Nome oficial alinhado com o registro de fachada e buscas."},
        {"status": "ok", "titulo": "Marcador GPS e Endereço", "detalhe": "Ponto no mapa correto na Av. Jorn. Jaime de Arruda Ramos."},
        {"status": "ok", "titulo": "Telefone com DDD local", "detalhe": "Telefone fixo ativo e funcional no perfil."},
        {"status": "ok", "titulo": "Horários de funcionamento", "detalhe": "Horários semanais preenchidos."},
        {"status": "warn", "titulo": "Fotos e Cardápio no perfil", "detalhe": "Fotos sem padrão profissional e ausência de cardápio em PDF/link."},
        {"status": "warn", "titulo": "Taxa de resposta a comentários", "detalhe": "Abaixo de 50% dos comentários respondidos formalmente."},
        {"status": "warn", "titulo": "Recência das avaliações", "detalhe": "Volume mensal estagnado fora da alta temporada."},
        {"status": "bad", "titulo": "Volume total de avaliações", "detalhe": "183 avaliações vs 1.445 do líder regional."},
        {"status": "bad", "titulo": "Site ou página de conversão própria", "detalhe": "Perfil direciona para portal de terceiro sem captura."},
        {"status": "bad", "titulo": "Botão de WhatsApp direto", "detalhe": "Ausência de link encurtado para atendimento no WhatsApp."}
    ],
    "proximo_passo": {
        "texto": "Implantar as placas inteligentes NFC de mesa e criar a página de cardápio direto para converter buscas em clientes.",
        "contato": "Fale com Augusto (AH3): (48) 99908-8162 · contato@ah3.com.br"
    }
}

corpo_data = {
    "agencia": "AH3 Marketing & Presença Local",
    "cidade_uf": "Florianópolis - SC",
    "data": "06/10/2026",
    "data_coleta": "06/10/2026",
    "ponto_referencia": "Ponta das Canas / Cachoeira (raio 3km)",
    "manchete": "Você é a 3ª Academia no Google Maps da região.",
    "manchete_apoio": "Nota 4,4★ com 45 avaliações. Ocupa posição no Top 3, mas está vulnerável à Fox Academia (176) e Shape Fitness (364) pela falta de novos reviews.",
    "estabelecimento": {
        "nome": "Academia Corpo em Ação",
        "categoria": "Academia / Centro de Treinamento",
        "verificado": True,
        "endereco": "Av. Luiz Boiteux Piazza, 6192 - Ponta das Canas, Florianópolis - SC",
        "telefone": "(48) 98878-1837",
        "gps": "-27.39691, -48.42704",
        "microrregiao": "Ponta das Canas"
    },
    "kpis": [
        {"label": "Score de Presença", "valor": "48", "sufixo": "/100", "nota": "Faltam 32 pts p/ meta 80", "cor": "bad"},
        {"label": "Total Avaliações", "valor": "45", "sufixo": "", "nota": "Líder regional: 364", "cor": "dark"},
        {"label": "Nota Média", "valor": "4,4", "sufixo": "★", "nota": "Reputação positiva", "cor": "warn"},
        {"label": "Gap p/ o Líder", "valor": "8,1", "sufixo": "×", "nota": "Menos avaliações que o líder", "cor": "brand"}
    ],
    "pilares": [
        {"label": "Dados cadastrais (NAP)", "desc": "Endereço e celular corretos", "valor": 85},
        {"label": "Volume de avaliações", "desc": "45 avaliações (muito abaixo do polo)", "valor": 25},
        {"label": "Recência das avaliações", "desc": "Poucas notas nos últimos 60 dias", "valor": 35},
        {"label": "Taxa de resposta", "desc": "Comentários sem resposta oficial", "valor": 30},
        {"label": "Fotos da Estrutura", "desc": "Poucas fotos de aparelhos e aulas", "valor": 45},
        {"label": "Site / Página de Planos", "desc": "Sem site próprio nem link de matrícula", "valor": 20}
    ],
    "diagnostico": "Excelente localização e boa nota, mas perfil vulnerável no Google por falta de reviews recentes e site próprio.",
    "ranking": {
        "linhas": [
            {"pos": "1º", "nome": "Shape Fitness Academy", "sub": "Academia · Cachoeira do Bom Jesus", "nota": "4,1", "avaliacoes": 364, "site": "ok", "wpp": "ok", "alvo": False},
            {"pos": "2º", "nome": "Fox Academia", "sub": "Academia · Ponta das Canas", "nota": "4,7", "avaliacoes": 176, "site": "warn", "wpp": "ok", "alvo": False},
            {"pos": "3º", "nome": "Academia Corpo em Ação", "sub": "Alvo auditado (Academia)", "nota": "4,4", "avaliacoes": 45, "site": "bad", "wpp": "ok", "alvo": True},
            {"pos": "4º", "nome": "Espaço Saúde & Treino", "sub": "Estúdio Funcional", "nota": "4,8", "avaliacoes": 32, "site": "bad", "wpp": "warn", "alvo": False},
            {"pos": "5º", "nome": "Academia Cross Floripa", "sub": "Centro de Treinamento", "nota": "4,6", "avaliacoes": 28, "site": "bad", "wpp": "bad", "alvo": False}
        ]
    },
    "acoes": [
        {
            "tag": "Impacto Imediato",
            "titulo": "Totem NFC na Recepção",
            "descricao": "Instalação de display NFC na catraca/balcão para coleta de avaliações diárias dos alunos ativos.",
            "prazo": "7 dias",
            "meta": "+40 avaliações no mês"
        },
        {
            "tag": "Aceleração de Reviews",
            "titulo": "Campanha de Matrículas",
            "descricao": "Automação pós-treino experimental para solicitar avaliação com 5 estrelas no Maps.",
            "prazo": "Imediato",
            "meta": "Alcançar 100 avaliações"
        },
        {
            "tag": "Presença Digital",
            "titulo": "Página de Planos & Grade",
            "descricao": "Site de alta conversão integrado com WhatsApp para fechar planos e matrículas online.",
            "prazo": "Contínuo",
            "meta": "Canal 100% ativo"
        }
    ],
    "resumo": {
        "conforme": {"qtd": 3},
        "atencao": {"qtd": 4},
        "critico": {"qtd": 3}
    },
    "checklist": [
        {"status": "ok", "titulo": "Nome comercial consistente", "detalhe": "Identificação clara como Academia Corpo em Ação."},
        {"status": "ok", "titulo": "Localização e Marcador GPS", "detalhe": "Endereço exato na Av. Luiz Boiteux Piazza."},
        {"status": "ok", "titulo": "Telefone com WhatsApp", "detalhe": "Celular comercial vinculado."},
        {"status": "warn", "titulo": "Horários de atendimento", "detalhe": "Horários de feriados não especificados."},
        {"status": "warn", "titulo": "Fotos das instalações e modalidades", "detalhe": "Faltam fotos de vestiários, esteiras e musculação."},
        {"status": "warn", "titulo": "Recência de avaliações", "detalhe": "Sem avaliações novas nas últimas semanas."},
        {"status": "warn", "titulo": "Taxa de resposta", "detalhe": "Avaliações de alunos sem interação da gerência."},
        {"status": "bad", "titulo": "Volume de avaliações", "detalhe": "Apenas 45 avaliações vs 364 da concorrente líder."},
        {"status": "bad", "titulo": "Site ou página de matrícula", "detalhe": "Sem página própria para exibição de grade e preços."},
        {"status": "bad", "titulo": "Ativação de palavras-chave locais", "detalhe": "Perfil não indexa para termos como musculação e pilates."}
    ],
    "proximo_passo": {
        "texto": "Instalar display NFC na recepção e criar página de conversão para captar matrículas de novos moradores da região.",
        "contato": "Fale com Augusto (AH3): (48) 99908-8162 · contato@ah3.com.br"
    }
}

os.makedirs('BigBrain/handoff/testes_auditoria', exist_ok=True)
with open('BigBrain/handoff/testes_auditoria/dados_chico_restaurante.json', 'w', encoding='utf-8') as f:
    json.dump(chico_data, f, indent=2, ensure_ascii=False)

with open('BigBrain/handoff/testes_auditoria/dados_academia_corpo_em_acao.json', 'w', encoding='utf-8') as f:
    json.dump(corpo_data, f, indent=2, ensure_ascii=False)

print('JSONs criados com sucesso!')

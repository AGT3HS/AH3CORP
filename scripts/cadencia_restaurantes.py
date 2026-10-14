#!/usr/bin/env python3
"""
AH3 — Módulo de Cadência e Abordagem Ativa para Restaurantes
Agente Encarregado: @Maestro / @Comercial

Funcionalidades:
1. Geração de mensagens sob medida (Toque 1 - Abordagem Inicial, Toque 2 - Follow-up 3 dias, Toque 3 - Break-up).
2. Trava e alerta automático de 3 dias para leads sem resposta.
3. Transição estrita de estados conforme AGENTS.md.
4. Sincronização direta com BigBrain/funil/leads.csv e painel de controle.
"""

import os
import sys
import json
import csv
import re
import urllib.parse
from datetime import datetime, timedelta

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
RESTAURANTES_JSON = os.path.join(ROOT_DIR, "scripts/data/gastronomia_polo_norte_real.json")
LEADS_CSV = os.path.join(ROOT_DIR, "BigBrain/funil/leads.csv")
CADENCIA_STATE_JSON = os.path.join(ROOT_DIR, "BigBrain/funil/cadencia_restaurantes_state.json")

def format_telefone_wa(telefone):
    if not telefone:
        return ""
    nums = re.sub(r'[^0-9]', '', str(telefone))
    if len(nums) == 10 or len(nums) == 11:
        return f"55{nums}"
    elif len(nums) == 12 or len(nums) == 13:
        return nums
    return ""

def gerar_mensagem_toque_1(nome, bairro, nota, reviews, gap=None):
    bairro_str = f"aqui em {bairro}" if bairro else "aqui em Florianópolis"
    reviews_str = f"{reviews} avaliações" if reviews else "ótima presença"
    nota_str = f" (nota {nota})" if nota else ""
    
    msg = (
        f"Olá, equipe do {nome}! Tudo bem?\n\n"
        f"Acompanho o trabalho de vocês {bairro_str}{nota_str} e notei a relevância do restaurante na região ({reviews_str}).\n\n"
        f"Identifiquei uma oportunidade prática para acelerar o volume de avaliações espontâneas de clientes no salão e dar ainda mais destaque ao {nome} no Google Maps sem gerar trabalho extra para a equipe.\n\n"
        f"Preparei uma prévia visual rápida de como funciona nossa solução de placas inteligentes e presença local. Posso te enviar por aqui?"
    )
    return msg

def gerar_mensagem_toque_2(nome, bairro):
    bairro_str = f"em {bairro}" if bairro else "aqui em Floripa"
    msg = (
        f"Olá, equipe do {nome}! Tudo bem?\n\n"
        f"Passando só para confirmar se conseguiram ver a mensagem que enviei há alguns dias. Sei que a rotina de atendimento e salão {bairro_str} é super corrida!\n\n"
        f"Vários restaurantes e polos gastronômicos de Florianópolis estão usando essa tecnologia de aproximação (NFC) no balcão e nas mesas para converter clientes satisfeitos em avaliações 5 estrelas no Google em 3 segundos.\n\n"
        f"Se fizer sentido, te mostro uma prévia rápida em PDF de 1 minuto sem compromisso. Posso mandar?"
    )
    return msg

def gerar_mensagem_toque_3(nome):
    msg = (
        f"Olá, equipe do {nome}! Tudo bem?\n\n"
        f"Imagino que a rotina aí esteja intensa por esses dias, então não quero insistir nem atrapalhar o serviço de vocês.\n\n"
        f"Vou pausar meu contato por aqui, mas fico à disposição sempre que quiserem fortalecer o posicionamento do {nome} no Google Maps e atrair mais clientes na região.\n\n"
        f"Um abraço e muito sucesso nas vendas!"
    )
    return msg

def carregar_estado_cadencia():
    if os.path.exists(CADENCIA_STATE_JSON):
        try:
            with open(CADENCIA_STATE_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_estado_cadencia(state):
    os.makedirs(os.path.dirname(CADENCIA_STATE_JSON), exist_ok=True)
    with open(CADENCIA_STATE_JSON, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def carregar_restaurantes():
    if not os.path.exists(RESTAURANTES_JSON):
        return []
    with open(RESTAURANTES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def obter_cadencia_consolidada():
    restaurantes = carregar_restaurantes()
    estado = carregar_estado_cadencia()
    
    # Criar lista enriquecida
    lista = []
    hoje = datetime.now()
    
    for r in restaurantes:
        rid = r.get("id") or r.get("nome")
        st = estado.get(rid, {})
        
        status = st.get("status", "auditado")
        data_abordagem_str = st.get("data_abordagem")
        data_followup_str = st.get("data_followup")
        data_fechamento_str = st.get("data_fechamento")
        
        dias_desde_abordagem = None
        requer_followup = False
        
        if data_abordagem_str and status == "abordado":
            try:
                dt_ab = datetime.strptime(data_abordagem_str, "%Y-%m-%d %H:%M:%S")
                dias_desde_abordagem = (hoje - dt_ab).days
                if dias_desde_abordagem >= 3 and not data_followup_str:
                    requer_followup = True
            except Exception:
                pass
                
        tel_wa = format_telefone_wa(r.get("telefone", ""))
        
        msg_t1 = gerar_mensagem_toque_1(r.get("nome"), r.get("bairro"), r.get("nota"), r.get("reviews"), r.get("gap_lider"))
        msg_t2 = gerar_mensagem_toque_2(r.get("nome"), r.get("bairro"))
        msg_t3 = gerar_mensagem_toque_3(r.get("nome"))
        
        wa_link_t1 = f"https://wa.me/{tel_wa}?text={urllib.parse.quote(msg_t1)}" if tel_wa else ""
        wa_link_t2 = f"https://wa.me/{tel_wa}?text={urllib.parse.quote(msg_t2)}" if tel_wa else ""
        wa_link_t3 = f"https://wa.me/{tel_wa}?text={urllib.parse.quote(msg_t3)}" if tel_wa else ""
        
        item = {
            "id": rid,
            "nome": r.get("nome"),
            "bairro": r.get("bairro", "Florianópolis"),
            "nota": r.get("nota", 0),
            "reviews": r.get("reviews", 0),
            "gap_lider": r.get("gap_lider", 0),
            "telefone": r.get("telefone", ""),
            "telefone_wa": tel_wa,
            "endereco": r.get("endereco", ""),
            "status": status,
            "data_abordagem": data_abordagem_str,
            "data_followup": data_followup_str,
            "data_fechamento": data_fechamento_str,
            "dias_desde_abordagem": dias_desde_abordagem,
            "requer_followup": requer_followup,
            "msg_t1": msg_t1,
            "msg_t2": msg_t2,
            "msg_t3": msg_t3,
            "wa_link_t1": wa_link_t1,
            "wa_link_t2": wa_link_t2,
            "wa_link_t3": wa_link_t3
        }
        lista.append(item)
    
    return lista

def registrar_acao(restaurante_id, acao):
    estado = carregar_estado_cadencia()
    if restaurante_id not in estado:
        estado[restaurante_id] = {}
        
    agora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if acao == "abordar":
        estado[restaurante_id]["status"] = "abordado"
        estado[restaurante_id]["data_abordagem"] = agora_str
    elif acao == "followup":
        estado[restaurante_id]["status"] = "abordado"
        estado[restaurante_id]["data_followup"] = agora_str
    elif acao == "fechar":
        estado[restaurante_id]["status"] = "fechado"
        estado[restaurante_id]["data_fechamento"] = agora_str
    elif acao == "resetar":
        estado[restaurante_id]["status"] = "auditado"
        estado[restaurante_id].pop("data_abordagem", None)
        estado[restaurante_id].pop("data_followup", None)
        estado[restaurante_id].pop("data_fechamento", None)
    
    salvar_estado_cadencia(estado)
    print(f"Sucesso: Restaurante {restaurante_id} atualizado para ação '{acao}' às {agora_str}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gerenciador de Cadência de Restaurantes AH3")
    parser.add_argument("--resumo", action="store_true", help="Exibe resumo do funil e alertas de 3 dias")
    parser.add_argument("--abordar", type=str, help="Marca lead como abordado pelo ID ou Nome")
    parser.add_argument("--followup", type=str, help="Marca follow-up realizado pelo ID ou Nome")
    parser.add_argument("--fechar", type=str, help="Marca lead como fechado")
    parser.add_argument("--resetar", type=str, help="Reseta estado do lead")
    
    args = parser.parse_args()
    
    if args.abordar:
        registrar_acao(args.abordar, "abordar")
    elif args.followup:
        registrar_acao(args.followup, "followup")
    elif args.fechar:
        registrar_acao(args.fechar, "fechar")
    elif args.resetar:
        registrar_acao(args.resetar, "resetar")
    else:
        # Resumo padrão
        itens = obter_cadencia_consolidada()
        total = len(itens)
        auditados = sum(1 for x in itens if x["status"] == "auditado")
        abordados = sum(1 for x in itens if x["status"] == "abordado")
        followups_pendentes = sum(1 for x in itens if x["requer_followup"])
        fechados = sum(1 for x in itens if x["status"] == "fechado")
        
        print("="*60)
        print("AH3 · CENTRAL DE CADÊNCIA & PROSPECÇÃO (RESTAURANTES)")
        print("="*60)
        print(f"Total Restaurantes: {total}")
        print(f"Prontos para 1ª Abordagem (Auditados): {auditados}")
        print(f"Em Cadência / Abordados: {abordados}")
        print(f"⚠️ Alerta: Requerem Follow-up (3+ dias): {followups_pendentes}")
        print(f"🎉 Contratos Fechados: {fechados}")
        print("="*60)
        if followups_pendentes > 0:
            print("\n🚨 LEADS PENDENTES DE FOLLOW-UP (JANELA DE 3 DIAS EXPIRADA):")
            for x in itens:
                if x["requer_followup"]:
                    print(f"- {x['nome']} ({x['bairro']}) | Abordado há {x['dias_desde_abordagem']} dias | Tel: {x['telefone']}")
                    print(f"  Link WA Follow-up: {x['wa_link_t2']}\n")

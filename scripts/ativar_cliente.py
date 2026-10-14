#!/usr/bin/env python3
"""
AH3 — Robô de Ativação de Cliente Fechado (Onboarding em 48h)
Agente Encarregado: @Maestro
Quando um lead fecha contrato, cria a estrutura privada em BigBrain/clientes/<slug>/,
preenche a minuta de contrato, gera o checklist de ativação de 48h e a pauta de conteúdo.
"""

import os
import sys
import argparse
import csv
from datetime import datetime
import unicodedata
import re

ROOT_DIR = "C:/Users/Augusto/Desktop/AH3"
CLIENTES_DIR = os.path.join(ROOT_DIR, "BigBrain/clientes")
LEADS_CSV = os.path.join(ROOT_DIR, "BigBrain/funil/leads.csv")
CONTRATO_BASE = os.path.join(ROOT_DIR, "BigBrain/modelos/contrato_base.md")

def normalize(txt):
    if not txt: return ''
    txt = unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9]', '', txt)

def ativar_cliente(nome, plano="Crescimento", valor="3200", cnpj="A preencher", endereco="Florianópolis - SC", telefone=""):
    slug = normalize(nome)
    pasta_cliente = os.path.join(CLIENTES_DIR, slug)
    
    # Criar subpastas isoladas (LGPD)
    subpastas = ["acessos", "conteudo", "contrato", "identidade_visual", "relatorios", "placas_nfc"]
    for sp in subpastas:
        os.makedirs(os.path.join(pasta_cliente, sp), exist_ok=True)

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    hoje_iso = datetime.now().strftime("%Y-%m-%d")

    # 1. Gerar Contrato Preenchido
    contrato_texto = f"""# CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE MARKETING E PRESENÇA LOCAL

**CONTRATANTE:** {nome.upper()}, pessoa jurídica com sede em {endereco}, inscrita no CNPJ sob o nº {cnpj}.
**CONTRATADA:** AGÊNCIA AH3 (Augusto Henrique Dos Santos), Florianópolis - SC.

---

## CLÁUSULA 1ª — DO OBJETO E ESCOPO
O presente instrumento tem por objeto a prestação de serviços de gestão de presença local, ativação de Placas Inteligentes NFC e reputação no Google Maps, conforme o **Plano {plano.upper()}**:
- Gestão e otimização contínua do perfil Google Meu Negócio;
- Fornecimento e codificação de Placas Inteligentes NFC 100x100mm;
- Funil de Avaliações no Google com retenção de feedbacks críticos;
- Gestão de Cardápio Digital e Experiência de Consumo;
- Relatório mensal de performance e notas locais.

## CLÁUSULA 2ª — DO VALOR E CONDIÇÕES DE PAGAMENTO
Pela prestação dos serviços contratados, a CONTRATANTE pagará à CONTRATADA o valor mensal de **R$ {valor},00 (reais)**, com vencimento todo dia 10 de cada mês.

## CLÁUSULA 3ª — DO PRAZO E RESCISÃO
O presente contrato possui vigência de 6 (seis) meses a contar da data de assinatura, renovável automaticamente por iguais períodos, podendo ser rescindido mediante aviso prévio de 30 (trinta) dias sem multa após o período inicial.

## CLÁUSULA 4ª — DO FORO
Para dirimir quaisquer controvérsias oriundas deste instrumento, as partes elegem o Foro da Comarca da Capital — Florianópolis / SC.

Florianópolis, {data_hoje}.

_______________________________
**{nome.upper()}** (Contratante)

_______________________________
**AGÊNCIA AH3** (Contratada)
"""
    with open(os.path.join(pasta_cliente, "contrato", f"contrato_{slug}.md"), "w", encoding="utf-8") as f:
        f.write(contrato_texto)

    # 2. Gerar Checklist de Ativação 48h
    checklist_texto = f"""# Checklist de Ativação 48h — {nome}
Data de Ativação: {data_hoje}
Plano: {plano} (R$ {valor}/mês)

- [ ] **Passo 1 (D+0):** Enviar link do contrato para assinatura digital via WhatsApp.
- [ ] **Passo 2 (D+1):** Solicitar acesso de 'Gerente' ao perfil do Google Meu Negócio.
- [ ] **Passo 3 (D+1):** Confirmar logos e aprovação final da arte da Placa NFC 100x100mm.
- [ ] **Passo 4 (D+2):** Enviar artes finais para corte a laser na gráfica parceira.
- [ ] **Passo 5 (D+3):** Gravar chips NFC NTAG213 com o link oficial de avaliações/cardápio.
- [ ] **Passo 6 (D+5):** Entrega presencial e instalação das placas nas mesas/balcão.
"""
    with open(os.path.join(pasta_cliente, "checklist_ativacao_48h.md"), "w", encoding="utf-8") as f:
        f.write(checklist_texto)

    # 3. Gerar Pauta Editorial do 1º Mês
    pauta_texto = f"""# Pauta Editorial e Presença Local (Mês 1) — {nome}

## Semana 1: Ativação & Boas-Vindas
- Foto de alta qualidade do prato/acomodação principal com geotag em {endereco}.
- Post Google Meu Negócio: "Novidade: Chegaram nossas Placas NFC de atendimento rápido."

## Semana 2: Autoridade & Prova Social
- Destaque da avaliação 5 estrelas mais recente de um cliente satisfeito.
- Atualização dos horários especiais de atendimento e fotos do ambiente.

## Semana 3: Experiência Gastronômica / Hospedagem
- Vídeo curto mostrando o preparo de um prato assinatura ou o café da manhã.
- Chamada para rota no Google Maps e reservas diretas no WhatsApp.

## Semana 4: Relatório Mensal & Fechamento
- Emissão do PDF de Auditoria de Crescimento de Avaliações e Visualizações no Maps.
"""
    with open(os.path.join(pasta_cliente, "conteudo", "pauta_mes_1.md"), "w", encoding="utf-8") as f:
        f.write(pauta_texto)

    # 4. Atualizar Status no leads.csv para 'fechado'
    if os.path.exists(LEADS_CSV):
        linhas = []
        with open(LEADS_CSV, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if normalize(row.get('nome', '')) == slug:
                    row['status'] = 'fechado'
                    row['valor_fechado'] = valor
                    row['data_atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                linhas.append(row)

        with open(LEADS_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(linhas)

    print(f"\n[SUCESSO] Cliente '{nome}' ativado com sucesso!")
    print(f"Pasta privada criada em: BigBrain/clientes/{slug}/")
    print(f"Contrato, Checklist 48h e Pauta Editorial gerados.")
    return pasta_cliente

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Robô de Ativação de Cliente AH3")
    parser.add_argument("--nome", type=str, required=True, help="Nome do cliente")
    parser.add_argument("--plano", type=str, default="Crescimento", help="Plano contratado")
    parser.add_argument("--valor", type=str, default="3200", help="Valor mensal")
    parser.add_argument("--cnpj", type=str, default="A preencher", help="CNPJ")
    parser.add_argument("--endereco", type=str, default="Florianópolis - SC", help="Endereço")
    
    args = parser.parse_args()
    ativar_cliente(args.nome, args.plano, args.valor, args.cnpj, args.endereco)

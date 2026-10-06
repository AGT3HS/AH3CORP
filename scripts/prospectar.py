import os
import json
import glob
from datetime import datetime
from buscar_locais import buscar_estabelecimentos
from gerar_relatorio import gerar_auditoria_pdf

BASE_DIR = r"C:\Users\Augusto\Desktop\AH3"
HANDOFF_DIR = os.path.join(BASE_DIR, "BigBrain", "handoff")
SAIDA_DIR = os.path.join(BASE_DIR, "saida")

def contar_abordagens_hoje():
    hoje = datetime.now().strftime("%Y-%m-%d")
    arquivos = glob.glob(os.path.join(HANDOFF_DIR, f"rascunho_*_{hoje}*.json"))
    return len(arquivos)

def criar_rascunho_whatsapp(dados_local, caminho_pdf):
    nome = dados_local.get("displayName", {}).get("text", "Estabelecimento")
    rating = dados_local.get("rating", "A verificar")
    total_reviews = dados_local.get("userRatingCount", "A verificar")
    website = dados_local.get("websiteUri")
    telefone = dados_local.get("nationalPhoneNumber", "A verificar")
    endereco = dados_local.get("formattedAddress", "A verificar")
    
    pontos = []
    if website:
        pontos.append(f"identificamos que o site está vinculado, mas há potencial projetado de otimização para captação direta de clientes")
    else:
        pontos.append(f"o perfil atual não possui link de website cadastrado, o que representa uma oportunidade esperada de direcionar clientes para cardápio/reservas")
        
    if rating != "A verificar" and total_reviews != "A verificar":
        pontos.append(f"a nota atual está em {rating} com {total_reviews} avaliações registradas")
    else:
        pontos.append(f"o volume de avaliações medido na região indica potencial de crescimento de autoridade local")
        
    texto_whatsapp = (
        f"Olá! Tudo bem? Meu nome é [Nome], da Agência AH3.\n\n"
        f"Estávamos analisando a presença digital de estabelecimentos na sua região e fizemos um diagnóstico preliminar do perfil da *{nome}* no Google Maps.\n\n"
        f"Notamos alguns pontos de destaque:\n"
        f"• {pontos[0].capitalize()};\n"
        f"• {pontos[1].capitalize()};\n"
        f"• Há um potencial esperado de aumento na visibilidade e atração de novos clientes aplicando ajustes de SEO local.\n\n"
        f"Preparamos um relatório em PDF com o diagnóstico completo medido pelo Google. Se fizer sentido, posso te encaminhar por aqui sem compromisso para você dar uma olhada?"
    )
    
    return {
        "estabelecimento": nome,
        "telefone": telefone,
        "endereco": endereco,
        "dados_medidos": {
            "nota": rating,
            "total_avaliacoes": total_reviews,
            "website": website if website else "A verificar",
            "telefone": telefone
        },
        "pdf_auditoria": caminho_pdf,
        "status": "Rascunho - Aguardando aprovação humana",
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem_whatsapp": texto_whatsapp
    }

def executar_prospeccao(termo_busca, max_estabelecimentos=3):
    os.makedirs(HANDOFF_DIR, exist_ok=True)
    os.makedirs(SAIDA_DIR, exist_ok=True)
    
    print(f"[*] Iniciando prospecção para: '{termo_busca}'")
    estabelecimentos = buscar_estabelecimentos(termo_busca, max_resultados=max_estabelecimentos)
    
    resultados = []
    for est in estabelecimentos:
        nome = est.get("displayName", {}).get("text", "Sem_Nome")
        nome_arquivo = "".join([c if c.isalnum() else "_" for c in nome])[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hoje = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Gerar PDF
        caminho_pdf = os.path.join(SAIDA_DIR, f"Auditoria_{nome_arquivo}_{timestamp}.pdf")
        gerar_auditoria_pdf(est, caminho_pdf)
        
        # 2. Criar rascunho de abordagem
        rascunho = criar_rascunho_whatsapp(est, caminho_pdf)
        
        # 3. Salvar no Handoff do BigBrain
        caminho_handoff = os.path.join(HANDOFF_DIR, f"rascunho_{nome_arquivo}_{hoje}_{timestamp}.json")
        with open(caminho_handoff, "w", encoding="utf-8") as f:
            json.dump(rascunho, f, ensure_ascii=False, indent=2)
            
        resultados.append({
            "nome": nome,
            "pdf": caminho_pdf,
            "handoff": caminho_handoff
        })
        print(f"[+] Processado: {nome} -> PDF e Handoff gerados.")
        
    total_hoje = contar_abordagens_hoje()
    print(f"\n[✓] Total de abordagens registradas hoje: {total_hoje}")
    return resultados

if __name__ == "__main__":
    import sys
    termo = sys.argv[1] if len(sys.argv) > 1 else "churrascaria em Moema sao paulo"
    executar_prospeccao(termo, max_estabelecimentos=2)

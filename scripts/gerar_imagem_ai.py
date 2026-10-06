"""
Módulo de Geração e Renderização Visual AI (Google GenAI / Imagen / Gemini)
AH3 - Direção de Arte e Design
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from PIL import Image
import io

load_dotenv()

def obter_cliente():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada no .env")
    return genai.Client(api_key=api_key)

def gerar_imagem_mockup(prompt: str, caminho_saida: str, modelo: str = "gemini-3-pro-image"):
    """
    Gera uma imagem / mockup de alta definição e salva no caminho de saída especificado.
    """
    client = obter_cliente()
    saida = Path(caminho_saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[AH3 Design] Gerando visual com modelo {modelo}...")
    print(f"[Prompt]: {prompt}")
    
    # Executa a geração
    try:
        response = client.models.generate_images(
            model=modelo,
            prompt=prompt,
            config=dict(
                number_of_images=1,
                aspect_ratio="1:1"
            )
        )
        if response.generated_images:
            img_bytes = response.generated_images[0].image.image_bytes
            img = Image.open(io.BytesIO(img_bytes))
            img.save(saida)
            print(f"[AH3 Design] Imagem salva com sucesso em: {saida.absolute()}")
            return str(saida.absolute())
    except Exception as e:
        print(f"[Aviso] Tentativa direta de generate_images falhou ({e}). Tentando fallback multimodal...")
        # Fallback via generate_content se o endpoint for unificado
        response = client.models.generate_content(
            model=modelo,
            contents=prompt
        )
        print(f"Resultado do modelo: {response.text}")
        return None

if __name__ == "__main__":
    import sys
    prompt_teste = sys.argv[1] if len(sys.argv) > 1 else "Mockup fotográfico de luxo de uma placa de acrílico preta fosca com detalhes dourados em uma mesa de mármore de restaurante sofisticado."
    gerar_imagem_mockup(prompt_teste, "BigBrain/handoff/teste_mockup_ai.png")

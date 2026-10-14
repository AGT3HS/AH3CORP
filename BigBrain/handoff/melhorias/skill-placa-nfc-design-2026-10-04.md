# Proposta de Skill: placa-nfc-design.md
Data: 2026-10-04
Autor: Diretor de Arte / Designer

## Objetivo
Padronizar a geração autônoma de placas táteis NFC (100x100mm) em formato vetorial puro (SVG) e renderização em PNG de alta definição para apresentação e aprovação do Augusto.

## Especificação Técnica Inviolável
1. **Formato & Geometria:**
   - `viewBox="0 0 1000 1000"` (escala 10 unid = 1 mm).
   - Cantos arredondados de corte físico: `rx="60"` e `ry="60"`.
   - Margem de respiro e segurança sagrada: 90 unidades (9 mm) em todos os lados.
   - Divisão de onda de contato: Y=530 nas bordas e Y=480 no centro.

2. **Tipografia e Corpos Fixos:**
   - Marca / Logo: 15 mm (150 unid.)
   - Produto: 6.4 mm (64 unid.)
   - NFC Badge: 3.0 mm (30 unid.)
   - Aproxime o celular: 2.8 mm (28 unid.)
   - Um toque libera: 2.9 mm (29 unid.)
   - Itens 2x2: 4.4 mm (44 unid.)
   - Rodapé: 3.0 mm (30 unid.)

3. **Tokens e Harmonia (60-30-10):**
   - 60% Fundo neutro nobre (ex: `#FAF8F2`, `#F8F6F0`). Nunca `#FFFFFF` ou `#000000` puros.
   - 30% Cor-mãe institucional do cliente no bloco superior.
   - 10% Ponto focal do sensor NFC.

4. **Entregáveis Obrigatórios:**
   - 4 variações canônicas de layout/cor.
   - Mockup PNG de palco neutro com sombra suave para validação visual.

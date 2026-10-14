# SKILL: placa-nfc-design  (Fase 1 · dono: Designer)
Leia antes: `BigBrain/travas.md` e `scripts/verificar_design_svg.py`.

## Quando usar
Geração de arte física de Placas e Cartões Inteligentes NFC (100x100mm) para hospitalidade e gastronomia.

## Entradas
- Nome do estabelecimento
- Cores institucionais (cor primária, topo degradê, fundo nobre, cor do sensor NFC)
- Arquivo de logo oficial (em `BigBrain/handoff/guias_identidade_visual/logos/` ou similar)

## Passos de Execução
1. Executar o gerador parametrizado:
   ```bash
   python scripts/gerar_placa.py --nome "Nome do Hotel" --cor_primaria "#..." --output "saida/placas_nfc"
   ```
2. Validar conformidade geométrica e visual com o linter:
   ```bash
   python scripts/verificar_design_svg.py "saida/placas_nfc/placa_nfc_<slug>.svg"
   ```
3. Garantir regras inegociáveis:
   - `viewBox="0 0 1000 1000"` (escala 10 unid = 1 mm)
   - Cantos arredondados para corte físico: `rx="60"` e `ry="60"`
   - Margem de respiro: 90 unidades (9 mm) em todos os lados
   - Proibição estrita de preto puro (#000000) e branco puro (#FFFFFF)
   - Divisão de onda de contato canônica: Y=530 nas bordas e Y=480 no centro
4. Copiar os arquivos gerados (SVG e PNG 300 DPI) para `BigBrain/handoff/placa_<slug>.svg` e `placa_<slug>.png`.

## Saída
- `saida/placas_nfc/placa_nfc_<slug>.svg`
- `saida/placas_nfc/placa_nfc_<slug>.png`
- Cópia homologada em `BigBrain/handoff/`

## Ao final
Registrar no ledger com `python scripts/ledger_append.py "Eventos-chave" "Placa NFC gerada para <nome>"`. Se houver melhorias na skill, registrar em `BigBrain/handoff/melhorias/`.

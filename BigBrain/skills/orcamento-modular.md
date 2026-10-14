---
name: orcamento-modular
description: Geração de apresentação executiva de 9 slides com 3 pacotes comerciais ancorados e narrativa bifurcada (Hotelaria vs Gastronomia).
owner: "@Comercial"
phase: 2
triggers:
  - "Lead respondeu com interesse e solicitou valores ou proposta comercial"
  - "Augusto pede geração de proposta modular para um cliente"
inputs:
  - nome: "Nome do estabelecimento"
  - vertical: "hotelaria ou gastronomia"
  - cores: "Cores da marca para identidade visual"
outputs:
  - proposta_pdf: "saida/propostas/proposta_<slug>.pdf (9 slides landscape)"
  - proposta_md: "BigBrain/handoff/proposta_<slug>.md"
governance_rules:
  - "Bloqueio absoluto se o pacote Essencial estiver abaixo do piso (R$ 1.850/mês)."
  - "Usar termos probabilísticos ('esperado', 'projetado', 'potencial')."
---

# SKILL: orcamento-modular (Fase 2 · Dono: @Comercial)

## Quando Usar
Quando o lead responder à abordagem inicial manifestando interesse em conhecer os pacotes da AH3.

## Entradas
- Nome e vertical do cliente (`--vertical hotelaria` ou `--vertical gastronomia`).
- Cores da marca (ou paleta regional de Florianópolis).

## Procedimento de Execução
1. **Executar o Gerador de Propostas Parametrizado Oficial:**
   ```bash
   python scripts/gerar_proposta_hotelaria_base_oficial.py --nome "Nome do Hotel"
   # ou para leads frios/apresentações executivas:
   python scripts/gerar_apresentacao_lead_base_oficial.py --nome "Nome do Lead"
   ```

2. **Matriz Canônica de Pacotes Ancorados:**
   - **Plano 1 — Essencial (R$ 1.850,00 / mês):**
     - Otimização completa do Google Meu Negócio.
     - 2 Placas Inteligentes NFC 100x100mm de alta durabilidade.
     - Relatório mensal de performance e monitoramento de avaliações.
   - **Plano 2 — Crescimento (R$ 3.200,00 / mês):**
     - Todos os itens do plano Essencial.
     - Gestão ativa e resposta estratégica a todas as avaliações no Google.
     - Cardápio Digital Mobile-First ou Landing Page de Reservas.
     - 4 Placas NFC para salão/mesas/recepção.
     - Calendário editorial semanal para Instagram.
   - **Plano 3 — Domínio Local (R$ 5.400,00 / mês):**
     - Todos os itens do plano Crescimento.
     - Planejamento e gestão de Tráfego Hiperlocal (Meta Ads / Google Maps).
     - 8 Placas NFC personalizadas.
     - Criação de posts e carrosséis visuais semanais em imagem de alta resolução.
     - Suporte prioritário via WhatsApp direto.

3. **Validação da Proposta:**
   - Submeter o PDF e o markdown para a skill `critica-proposta` do `@Maestro`.

## Ao Final
Registrar a geração da proposta no ledger:
```bash
python scripts/ledger_append.py "Propostas" "Proposta modular de 9 slides gerada para <nome>."
```

---
name: delegacao-souls
description: Roteamento de comandos e delegação contextual do Maestro para os 3 Agentes Especialistas da AH3.
owner: "@Maestro"
phase: 1
triggers:
  - "Augusto faz um pedido operacional fora da alçada de governança do Maestro"
  - "Necessidade de acionar Comercial, Marketing ou Designer"
inputs:
  - comando_usuario: "Texto da instrução enviada pelo Augusto"
  - mapa_skills: "BigBrain/skills/_map.md"
outputs:
  - handoff: "Arquivo gerado pelo agente especialista em BigBrain/handoff/"
governance_rules:
  - "Isolamento absoluto de contexto (LGPD): nunca injetar dados de um cliente no contexto de outro."
  - "Qualquer entrega deve ser salva em BigBrain/handoff/ para aprovação final do Augusto."
---

# SKILL: delegacao-souls (Fase 1 · Dono: @Maestro)

## Quando Usar
Sempre que uma tarefa exigir produção comercial, criativa, técnica de design ou gestão de tráfego/conteúdo.

## Matriz de Roteamento de Intenções (Intent Routing)

| Palavras-Chave no Pedido do Augusto | Agente Responsável | Soul | Skills Relacionadas |
|---|---|---|---|
| Varredura, auditar, lead, proposta, orçamento, contrato, fechamento | **@Comercial** | `souls/comercial.md` | `varredura-bairro`, `auditoria-google-meu-negocio`, `orcamento-modular`, `preenchimento-contrato` |
| Post, carrossel, instagram, review, resposta, tráfego, anúncio, calendário, relatório mensal | **@Marketing** | `souls/marketing.md` | `post-semanal`, `resposta-avaliacao`, `roteiro-instagram`, `calendario-editorial`, `planejamento-trafego`, `relatorio-mensal` |
| Placa NFC, SVG, logo, cardápio digital, landing page, identidade visual | **@Designer** | `souls/designer.md` | `placa-nfc-design`, `cardapio-digital`, `landing-page` |
| Governança, auditoria de travas, linter de textos, resumo diário, follow-up | **@Maestro** | `souls/maestro.md` | `resumo-funil-diario`, `follow-up-3-dias`, `critica-proposta`, `auditoria-skills-map`, `bootstrap-agencia` |

## Procedimento de Execução
1. **Identificação da Especialidade:** O Maestro analisa o pedido e localiza o Agente Canônico correspondente.
2. **Injeção Mínima de Contexto:** Fornecer apenas as variáveis essenciais para a execução da tarefa (nome do cliente, paleta, nicho).
3. **Execução Técnica:** Invocar a skill e os scripts associados.
4. **Validação de Conformidade:**
   - Rodar linter contra palavras proibidas (`python scripts/verificar_texto.py <arquivo>`).
   - Conferir respeito às travas invioláveis do [`AGENTS.md`](file:///c:/Users/Augusto/Desktop/AH3/AGENTS.md).
5. **Entrega em Handoff:** Salvar o entregável em `BigBrain/handoff/` e notificar o Augusto com resumo de decisão.

## Ao Final
Registrar a delegação no ledger:
```bash
python scripts/ledger_append.py "Delegação" "Tarefa delegada para @<Agente>: <resumo>."
```

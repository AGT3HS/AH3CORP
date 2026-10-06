# MAPA — Cérebro AH3

## O que é
Operação da Agência AH3. Cérebro privado e isolado. Dados de clientes nunca se cruzam (LGPD).

## Estrutura
- `travas.md` — regras invioláveis, status de lead, valor mínimo
- `augusto.md` — quem é o Augusto e como ele decide
- `funil/leads.csv` — pipeline
- `clientes/<slug>/` — 1 pasta por cliente
- `handoff/` — rascunhos aguardando aprovação
- `handoff/melhorias/` — sugestões de mudança em skills (Augusto aprova)
- `modelos/` — DESIGN.md, contrato_base.md
- `conteudo/` — calendário editorial
- `skills/_map.md` — mapa de skills
- `souls/` — personalidades invocadas via @
- `ledger/` — registro diário

## Quem escreve onde
| Agente | Pode escrever em |
|---|---|
| Maestro | funil, handoff, ledger, clientes |
| Radar | funil (só novo→auditado), handoff, ledger |
| Souls | handoff (via Maestro) |
| Skills e souls | NUNCA editadas por agente. Só o Augusto. |

## Regras
1. Nada sai de `handoff/` sem aprovação do Augusto.
2. Antes de agir: ler `travas.md` e `skills/_map.md`.
3. Skill fora do `_map.md` não existe.
4. Agente sugere melhoria em `handoff/melhorias/`. Não edita skill.
5. Credenciais só em `.env`.
6. Ledger: 1 registro ao final de cada tarefa. Só registra o que passou pelo sistema.

## Rotinas (quem dispara)
Disparo: agendador do Hermes. Se não tiver, Agendador de Tarefas do Windows chamando o Maestro.
| Fase | Rotina | Quando |
|---|---|---|
| 1 | `resumo-funil-diario` + `follow-up-3-dias` | 08h |
| 2 (com clientes) | `resumo-funil-diario` | 08h e 18h |
| 2 | `auditoria-skills-map` | segunda 09h |
| 3 | `post-semanal`, `relatorio-mensal` | por cliente fechado |

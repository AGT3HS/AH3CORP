---
name: auditoria-skills-map
description: Verificação de consistência e conformidade entre o catálogo de skills (_map.md) e os arquivos em disco.
owner: "@Maestro"
phase: 2
triggers:
  - "Rotina semanal de segunda-feira às 09:00"
  - "Após criação ou exclusão de procedimentos técnicos"
inputs:
  - catalogo: "BigBrain/skills/_map.md"
  - arquivos: "BigBrain/skills/*.md"
outputs:
  - relatorio: "Auditoria de integridade no terminal e registro no ledger"
governance_rules:
  - "PROIBIDO editar arquivos de skill diretamente sem aprovação formal do Augusto."
  - "Alertar se houver skills órfãs ou sem dono canônico atribuído."
---

# SKILL: auditoria-skills-map (Fase 2 · Dono: @Maestro)

## Quando Usar
Toda segunda-feira às 09:00 para auditar a governança do ecossistema de habilidades da AH3.

## Entradas
- Mapa de Habilidades: [`BigBrain/skills/_map.md`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/skills/_map.md)
- Diretório de Habilidades: [`BigBrain/skills/`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/skills)

## Procedimento de Execução
1. **Auditoria de Conformidade:**
   - Conferir se todas as skills possuem cabeçalho YAML Frontmatter válido (`name`, `description`, `owner`, `phase`, `triggers`).
   - Validar se o `owner` pertence aos 4 Agentes Canônicos (`@Maestro`, `@Comercial`, `@Marketing`, `@Designer`).
   - Identificar arquivos sem entrada no `_map.md` (fantasmas) ou entradas no `_map.md` sem arquivo correspondente (órfãos).

2. **Relatório de Governança:**
   - Gerar tabela de integridade listando o status de cada skill.

## Golden Sample (Exemplo Padrão-Ouro de Saída)
```text
🛡️ *Auditoria Semanal de Skills AH3 — 100% Conforme*

• Total de skills ativas: 19
• Donos alinhados: 19/19
• Frontmatter YAML válido: 19/19
• Divergências no _map.md: 0

✅ Todas as habilidades operam sob governança estrita e respeitam as 8 travas invioláveis.
```

## Ao Final
Registrar no diário de bordo com:
```bash
python scripts/ledger_append.py "Auditoria" "Auditoria do mapa de skills executada: 100% conforme."
```

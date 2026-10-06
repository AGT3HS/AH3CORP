# Proposta de Melhoria / Nova Skill: auditoria-redes-agent-reach

- **Data:** 2026-10-02
- **Autor/Proponente:** Maestro
- **Agente Alvo:** `@Radar` (e suporte ao `@Conteudo`)
- **Origem:** Integração com a biblioteca Agent Reach (`Panniantong/Agent-Reach`)

---

## 1. Contexto e Objetivo
Habilitar o agente `@Radar` a realizar varreduras e diagnósticos aprofundados da presença digital de estabelecimentos gastronômicos (Instagram, Facebook, YouTube, avaliações públicas e links web) em Florianópolis sem custo de API adicional, gerando dados ricos para prospecção no funil (`BigBrain/funil/leads.csv`).

---

## 2. Especificação Técnica da Operação

### Executável / Ambiente
- **Interpretador:** `C:/Users/Augusto/AppData/Local/Programs/Python/Python312/python.exe`
- **Módulo:** `agent_reach.cli`

### Comandos de Diagnóstico e Auditoria
1. **Diagnóstico geral dos canais ativos:**
   ```bash
   "C:/Users/Augusto/AppData/Local/Programs/Python/Python312/python.exe" -m agent_reach.cli doctor
   ```

2. **Leitura/Extração de conteúdo de página web/cardápio/artigo do lead:**
   ```bash
   "C:/Users/Augusto/AppData/Local/Programs/Python/Python312/python.exe" -m agent_reach.cli read "<URL_DO_LEAD>"
   ```

3. **Busca e monitoramento de menções e canais (quando configurados):**
   ```bash
   "C:/Users/Augusto/AppData/Local/Programs/Python/Python312/python.exe" -m agent_reach.cli search "<TERMO_OU_NOME_DO_RESTAURANTE>"
   ```

---

## 3. Travas de Segurança e Governança (AGENTS.md)
1. **Nenhum dado é publicado:** O Agent Reach é utilizado estritamente em modo de leitura (`read` / `search`).
2. **Isolamento de Credenciais:** Sessões ou cookies adicionais (ex: Instagram/Facebook via Chrome local) nunca são expostos em texto de propostas ou relatórios compartilhados.
3. **Fluxo do Funil:** Apenas leads com dados validados transitam de `novo` para `auditado`.

---

## 4. Próximos Passos
- Aprovação do Augusto para mover esta definição para `BigBrain/skills/auditoria-redes-agent-reach.md` e catalogar no `BigBrain/skills_map.md`.

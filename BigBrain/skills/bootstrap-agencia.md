---
name: bootstrap-agencia
description: Inicialização, verificação de sanidade e checagem de diretórios canônicos da AH3.
owner: "@Maestro"
phase: 1
triggers:
  - "Augusto pede bootstrap"
  - "Inicialização do sistema ou verificação de integridade"
  - "Estrutura de pastas ou arquivos corrompida"
inputs:
  - config: "BigBrain/travas.md, AGENTS.md, .env"
outputs:
  - relatorio: "Registro no ledger com status de sanidade"
governance_rules:
  - "Nunca sobrescrever dados de clientes ou funil existentes."
  - "Se faltar credencial em .env, alertar o Augusto imediatamente sem expor valores."
---

# SKILL: bootstrap-agencia (Fase 1 · Dono: @Maestro)

## Quando Usar
Quando o Augusto pedir para "iniciar o sistema", "verificar a estrutura" ou quando houver suspeita de pastas ou arquivos ausentes.

## Entradas
- Arquivos de governança: [`AGENTS.md`](file:///c:/Users/Augusto/Desktop/AH3/AGENTS.md) e [`BigBrain/travas.md`](file:///c:/Users/Augusto/Desktop/AH3/BigBrain/travas.md).
- Arquivo de credenciais: `.env`.

## Procedimento de Execução
1. **Verificação de Diretórios Obrigatórios:**
   Garantir a existência das seguintes pastas sem recriar se já existirem:
   - `BigBrain/funil/`
   - `BigBrain/clientes/`
   - `BigBrain/handoff/`
   - `BigBrain/handoff/melhorias/`
   - `BigBrain/ledger/`
   - `BigBrain/modelos/`
   - `BigBrain/conteudo/`
   - `BigBrain/skills/`
   - `BigBrain/souls/`
   - `saida/`

2. **Verificação de Arquivos Canônicos:**
   - `BigBrain/funil/leads.csv` (com cabeçalho correto se inexistente).
   - `BigBrain/travas.md` (validar se o piso financeiro está configurado).
   - `AGENTS.md` (manual de governança carregado).

3. **Verificação de Credenciais:**
   - Conferir se `.env` existe e possui `GOOGLE_PLACES_API_KEY` (não imprimir o valor).

## Saída Esperada
Relatório objetivo no terminal informando itens íntegros, itens criados e pendências de configuração.

## Ao Final
Registrar a execução no ledger operacional:
```bash
python scripts/ledger_append.py "Governança" "Auditoria de sanidade e bootstrap do sistema concluídos."
```

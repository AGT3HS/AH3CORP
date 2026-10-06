# GUIA DEFINITIVO DE ENGENHARIA E ORQUESTRAÇÃO COM AGENT SKILLS
**Edição Canônica · Arquitetura Integrada para Sistemas Autônomos de Alta Performance**
*Baseado no ecossistema Addy Osmani (`addyosmani/agent-skills`), Claude Code, Hermes Agent e Antigravity*

---

## 1. VISÃO GERAL & ARQUITETURA EM 3 CAMADAS

A engenharia orientada a agentes não opera com instruções genéricas. Ela se apoia em uma separação estrita de responsabilidades:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           COMMANDS / USER                               │
│  "O QUANDO" — Entry points, orquestração e gates de ciclo de vida       │
│  (/spec, /plan, /build, /test, /review, /ship, /webperf)                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Invoca / Mapeia
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              PERSONAS                                   │
│  "O QUEM" — Especialistas de perspectiva única e formato de saída fixo  │
│  (code-reviewer, security-auditor, test-engineer, web-perf-auditor)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Executa
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                               SKILLS                                    │
│  "O COMO" — Workflows determinísticos com regras e critérios de saída   │
│  (spec-driven-dev, test-driven-dev, code-simplification, etc.)          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Regras Cardeais de Composição:
1. **O Usuário (ou Command) é o Orquestrador:** Personas **nunca** chamam outras personas. Isso elimina *routers* intermediários que consomem tokens e perdem contexto.
2. **Subagents em Isolamento:** Subagentes rodam em janelas de contexto limpas e reportam apenas seu relatório estruturado para a sessão principal.
3. **Anti-Racionalização Obrigatória:** O agente é proibido de ignorar skills com pensamentos como *"Esta alteração é simples demais"* ou *"Vou codificar direto e testar depois"*.

---

## 2. NÚCLEO OPERACIONAL PRAGMÁTICO (V1 - CICLO DE VIDA PADRÃO)

Todo desenvolvimento de novas funcionalidades ou alterações estruturais segue o pipeline de 4 gates obrigatórios:

```
 [ 1. SPEC ] ───────► [ 2. PLAN ] ───────► [ 3. BUILD ] ───────► [ 4. VERIFY ]
spec-driven-dev     planning-breakdown    incremental-impl       shipping-and-launch
context-engineering  constraint-driven     test-driven-dev        code-review-and-quality
```

### Protocolo de Execução por Fase:

### Fase 1: SPEC (Definição de Contratos)
- **Skill:** `spec-driven-development` + `api-and-interface-design`
- **Ação:** Criação de arquivo `.spec.md` definindo inputs, outputs, payloads e tratamento de erros de borda.
- **Gate de Saída:** Nenhuma linha de código é alterada antes da especificação estar formalizada e aprovada.

### Fase 2: PLAN (Fatiamento Atômico)
- **Skill:** `planning-and-task-breakdown` + `constraint-driven-development`
- **Ação:** Decomposição da especificação em passos incrementais com escopo limitado (idealmente 1 arquivo por passo).
- **Gate de Saída:** Lista de tarefas em ordem estrita de dependência e matriz de restrições (latência, memória, segurança).

### Fase 3: BUILD (Implementação Incremental)
- **Skill:** `incremental-implementation` + `test-driven-development`
- **Ação:** Codificação em passos curtos. A cada arquivo modificado, validação com build e testes unitários.
- **Gate de Saída:** Compilação verde (`exit code 0`) e linter limpo a cada etapa.

### Fase 4: VERIFY (Validação Pré-Merge)
- **Skill:** `code-review-and-quality` + `code-simplification`
- **Ação:** Execução de revisão estrita em 5 eixos (arquitetura, segurança, robustez, performance e manutenibilidade).

---

## 3. ORQUESTRAÇÃO PARALELA NO /SHIP (V2 - MULTI-AGENT FAN-OUT)

O comando `/ship` é o padrão canônico para preparação de PRs e releases críticas. Ele executa uma divisão paralela (*fan-out*) com 3 subagentes especialistas, seguido de uma síntese determinística (*merge phase*).

```
                                  [ /SHIP ]
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼ (Contexto Isolado)        ▼ (Contexto Isolado)        ▼ (Contexto Isolado)
┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐
│       code-reviewer       │ │     security-auditor      │ │       test-engineer       │
│ - Design & Boas Práticas  │ │ - OWASP Top 10 & CWEs     │ │ - Prove-It Pattern        │
│ - Dívida Técnica & Clones │ │ - Vazamento de Segredos   │ │ - Cobertura de Caminhos   │
│ - Complexidade Ciclomática│ │ - Sanitização de Inputs   │ │ - Casos de Borda Críticos │
└─────────────┬─────────────┘ └─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │                             │
              └─────────────────────────────┼─────────────────────────────┘
                                            ▼
                                   [ FASE DE SÍNTESE ]
                          Matriz de Decisão Go / No-Go + Rollback
```

### Critérios de Veto do /SHIP:
- **No-Go Imediato:** Qualquer vulnerabilidade classificada como *High* ou *Critical* pelo `security-auditor`.
- **No-Go Imediato:** Falha de teste ou regressão apontada pelo `test-engineer`.
- **No-Go Imediato:** Bloqueio arquitetural pelo `code-reviewer`.
- **Go Autorizado:** 3 relatórios com sinal verde + plano de rollback documentado.

---

## 4. PROTOCOLO "PROVE-IT" PARA BUGS & CÓDIGO CRÍTICO (V3 - TDD EXTREMO)

Para qualquer correção de bug, regressão ou alteração em código crítico (autenticação, transações financeiras, persistência), aplica-se o ciclo **RED-GREEN-REFACTOR** com o padrão **Prove-It**:

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. REPRODUZIR (RED)                                                         │
 │ Escrever teste unitário reproduzindo o erro. O teste DEVE FALHAR.           │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 2. CORREÇÃO MÍNIMA (GREEN)                                                  │
 │ Alterar apenas o código estritamente necessário para o teste passar.        │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 3. SIMPLIFICAÇÃO & BLINDAGEM (REFACTOR)                                     │
 │ Executar 'code-simplification' e validar ausência de efeitos colaterais.    │
 └─────────────────────────────────────────────────────────────────────────────┘
```

### Regras do Padrão Prove-It:
1. **Proibido "Conserto Cego":** É terminantemente proibido propor um patch sem antes demonstrar o teste falhando no terminal real.
2. **Isolamento de Causa Raiz:** O agente deve investigar a classe do erro nos caminhos irmãos (`systematic-debugging`), e não apenas o ponto relatado.
3. **Zero Mocks Fictícios em Contratos Críticos:** Testes de integração devem bater contra o schema real da base ou do endpoint.

---

## 5. ENGENHARIA GUIADA POR RESTRIÇÕES NÃO-FUNCIONAIS (V4 - CONSTRAINT MATRIX)

Antes do início da implementação, o arquiteto fixa os limites máximos aceitáveis de consumo de recursos (*Floor-Guard Matrix*):

| Dimensão | Métrica / Restrição | Ferramenta / Skill de Auditoria | Ação em Caso de Violação |
| :--- | :--- | :--- | :--- |
| **Performance Web** | INP < 200ms · LCP < 2.5s · CLS < 0.1 | `web-performance-auditor` + DevTools | Rejeição automática de PR |
| **Bundle & Payload** | Limite máximo de acréscimo de +15KB gzip | `constraint-driven-development` | Tree-shaking / Code-splitting |
| **Memória & Backend** | TTFB < 150ms · Zero Memory Leaks em loop | `observability-and-instrumentation` | Profiling via script nativo |
| **Segurança** | Zero dependências vulneráveis (`audit 0`) | `security-and-hardening` | Upgrade ou troca de lib |

---

## 6. MANUAL DE INTEGRAÇÃO & TABELA CANÔNICA DE SKILLS (V5)

### Mapeamento Automático de Intenções (Intent Engine):

| Intenção do Usuário | Skill Primária | Skills de Suporte | Output Obrigatório |
| :--- | :--- | :--- | :--- |
| Criar funcionalidade / feature nova | `spec-driven-development` | `planning-breakdown`, `api-interface-design` | `SPEC.md` + Tarefas no checklist |
| Resolver bug ou falha inesperada | `debugging-and-error-recovery` | `test-driven-development` (Prove-It) | Teste falhando ➔ Teste passando |
| Refatorar ou limpar código | `code-simplification` | `test-driven-development` | Redução de LOC sem regressão |
| Revisar PR ou código pronto | `code-review-and-quality` | `security-and-hardening` | Relatório de 5 eixos |
| Otimizar Core Web Vitals / UI | `performance-optimization` | `browser-testing-with-devtools` | Trace de performance + métricas |
| Preparar release / deploy | `shipping-and-launch` | Fan-out `/ship` (3 personas) | Parecer Go/No-Go + Rollback |

---

## 7. CHECKLIST DE CONFORMIDADE PRÉ-COMMITT

- [ ] A especificação foi documentada antes do código?
- [ ] O teste unitário falhou antes da correção ser aplicada?
- [ ] Todos os testes unitários e de integração estão passando (`exit code 0`)?
- [ ] O linter/typecheck rodou sem novos avisos ou erros?
- [ ] O fan-out do `/ship` aprovou arquitetura, segurança e testes?
- [ ] As restrições de performance e payload foram respeitadas?
- [ ] A mensagem de commit segue o padrão Conventional Commits (`feat:`, `fix:`, `refactor:`)?

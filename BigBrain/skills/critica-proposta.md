---
name: critica-proposta
description: Auditoria heurística e verificação de conformidade em 5 eixos antes do envio de propostas comerciais ao cliente.
owner: "@Maestro"
phase: 2
triggers:
  - "Toda proposta comercial gerada antes de ser apresentada ao Augusto"
  - "Revisão de conformidade de PDF ou documento de vendas"
inputs:
  - proposta: "BigBrain/handoff/proposta-<slug>.pdf ou .md"
outputs:
  - parecer: "Veredito (APROVADO / REVISAR / REPROVADO) com relatório de apontamentos"
governance_rules:
  - "Reprovação imediata se contiver palavras proibidas ('garantido', 'garantia', '100%', 'com certeza')."
  - "Reprovação imediata se os valores estiverem abaixo do piso financeiro (R$ 1.850/mês)."
---

# SKILL: critica-proposta (Fase 2 · Dono: @Maestro)

## Quando Usar
Obrigatório para toda proposta comercial antes de ser liberada para o Augusto enviar ao cliente.

## Entradas
- Arquivo de proposta: `BigBrain/handoff/proposta-<slug>.pdf` (ou `.md`).

## Procedimento de Execução (Checklist Heurístico em 5 Eixos)

1. **Eixo 1 — Travas Invioláveis e Linter Anti-Promessa:**
   - Executar o linter oficial:
     ```bash
     python scripts/verificar_texto.py "BigBrain/handoff/proposta-<slug>.md"
     ```
   - Garantir que foram usados termos probabilísticos como *"potencial estimado"*, *"projeção de alcance"* ou *"capacidade esperada"*.

2. **Eixo 2 — Travas Financeiras e Ancoragem:**
   - Conferir se o pacote de entrada respeita o piso financeiro mínimo de **R$ 1.850,00/mês**.
   - Validar a presença dos 3 pacotes ancorados (Essencial, Crescimento, Domínio).

3. **Eixo 3 — Coerência de Nicho:**
   - Se Hotelaria: Foco em check-in, ADR (diária média), desintermediação de OTAs (Booking/Airbnb) e hóspedes.
   - Se Gastronomia: Foco em giro de salão, cardápio digital, tempo de mesa e fidelização.

4. **Eixo 4 — Identidade Visual & Design:**
   - Verificar padrão tipográfico canônico (**Outfit** para títulos e **Inter** para corpo).
   - Validar ausência de preto puro (#000000) e branco puro (#FFFFFF).

5. **Eixo 5 — Clareza de Decisão:**
   - Validar a presença de chamada para ação direta e sem fricção pelo WhatsApp.

## Saída Esperada
Parecer objetivo emitido pelo Maestro:
- **APROVADO:** Proposta 100% em conformidade com as regras de governança e pronta para o Augusto enviar.
- **REVISAR:** Pequenos ajustes solicitados ao `@Comercial`.
- **REPROVADO:** Violação de travas de segurança (bloqueio imediato).

## Ao Final
Registrar no diário de bordo com `python scripts/ledger_append.py "Auditoria" "Crítica de proposta emitida para <slug>: APROVADO."`.

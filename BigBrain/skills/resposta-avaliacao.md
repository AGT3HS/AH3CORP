---
name: resposta-avaliacao
description: Gestão ativa de reputação e elaboração de respostas estratégicas a avaliações no Google Maps com injeção de SEO Local.
owner: "@Marketing"
phase: 3
triggers:
  - "Nova avaliação postada no Google Maps de um cliente ativo"
  - "Auditoria periódica de reviews sem resposta"
inputs:
  - review: "Texto da avaliação, nota em estrelas e nome do cliente"
  - cliente: "Dados do cliente em BigBrain/clientes/<slug>/"
outputs:
  - resposta: "BigBrain/handoff/resposta_<slug>_<data>.md"
governance_rules:
  - "PROIBIDO responder com tom defensivo, agressivo ou irônico a reviews negativos."
  - "Nunca prometer cortesias financeiras, refeições grátis ou estadias sem prévia autorização por escrito do proprietário."
---

# SKILL: resposta-avaliacao (Fase 3 · Dono: @Marketing)

## Quando Usar
Sempre que o cliente receber uma nova avaliação no Google Meu Negócio ou durante a rotina semanal de monitoramento de reputação.

## Matriz Estratégica em 4 Quadrantes

| Nota | Objetivo Estratégico | Estrutura da Resposta |
|---|---|---|
| ⭐⭐⭐⭐⭐ **5 Estrelas** | Fidelização e SEO Local | Agradecer nominalmente, ecoar o prato/suíte elogiado e convidar para o próximo evento ou visita. |
| ⭐⭐⭐⭐ **4 Estrelas** | Reforço Positivo | Valorizar o que funcionou perfeitamente e acolher com humildade qualquer observação construtiva. |
| ⭐⭐⭐ **3 Estrelas** | Esclarecimento Neutro | Reconhecer a experiência mediana, agradecer o feedback e informar que a equipe de salão/governança foi comunicada. |
| ⭐/⭐⭐ **1-2 Estrelas** | **Desarme e Resgate** | Empatia genuína, pedido sincero de desculpas pelo transtorno e convite para conversa privada no WhatsApp do gerente (sem bater boca no público). |

## Injeção de Palavras-Chave de SEO Local
Em respostas 5 estrelas, incluir termos naturais que auxiliam o ranqueamento do Google:
- *"Ficamos muito felizes que você apreciou nossos frutos do mar frescos no Centro de Florianópolis!"*
- *"Esperamos te receber novamente para outro café da manhã inesquecível em Canasvieiras."*

## Golden Sample (Exemplo de Desarme — 1 Estrela)
> *"Olá, [Nome do Cliente]. Sentimos muito que o tempo de espera do seu pedido tenha ficado acima do nosso padrão no último sábado. Valorizamos muito o seu tempo e queremos entender o que houve para corrigir de imediato. Por favor, envie uma mensagem direta para a nossa gerência no WhatsApp [(48) 9XXXX-XXXX] para podermos conversar e cuidar pessoalmente da sua experiência. Agradecemos sua sinceridade e feedback."*

## Ao Final
Validar o texto e registrar no ledger:
```bash
python scripts/verificar_texto.py "BigBrain/handoff/resposta_<slug>_<data>.md"
python scripts/ledger_append.py "Reputação" "Resposta estratégica rascunhada para avaliação de <slug>."
```

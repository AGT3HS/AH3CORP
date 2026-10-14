# Auditoria e Saneamento de Telefones e WhatsApp — Base Canasvieiras e Polo Norte

**Data:** 11/10/2026  
**Responsável Operacional:** Maestro (Orquestrador AH3)  
**Artefato Gerado:** `BigBrain/handoff/auditoria_whatsapp_conferencia.csv`  
**Base Saneada:** `BigBrain/funil/leads.csv`

---

## 1. Causa Raiz do Erro Operacional

A varredura original do Google Maps importou telefones genéricos cadastrados nos perfis das empresas. No setor gastronômico de Florianópolis, esse procedimento gerou duas falhas críticas:
1. **Linhas Fixas Tradicionais (23 estabelecimentos):** Números com prefixo 3XXX-XXXX foram tratados como celulares. Ao tentar enviar mensagens via WhatsApp, o aplicativo acusa "número não registrado" ou atinge linhas sem suporte a mensagens.
2. **Números Pessoais e Reciclados:** Cadastros desatualizados do Google Maps frequentemente mantêm celulares de antigos sócios, contadores ou números cancelados reatribuídos a terceiros sem relação com o estabelecimento.

---

## 2. Ações de Correção Aplicadas

1. **Separação Rígida em `leads.csv`:**
   - Todas as 23 linhas fixas receberam o prefixo `[FIXO]` e observação de bloqueio para envio de WhatsApp.
   - Celulares com canais digitais verificados foram validados.
   - Casos com formatação atípica (ex: número da Argentina `+54`) foram marcados como internacionais.
2. **Criação da Planilha de Conferência:**
   - Criado `BigBrain/handoff/auditoria_whatsapp_conferencia.csv` contendo a classificação técnica, a fonte de validação e o link oficial de cada contato.
3. **Mapeamento de Origens Digitais:**
   - Extração dos links diretos de WhatsApp (wa.me/api.whatsapp), Instagram oficial, plataformas de cardápio digital (Anota.ai, Cardapioweb) e websites próprios.

---

## 3. Resumo Quantitativo da Base (85 Leads)

| Categoria | Quantidade | Ação Operacional |
|---|:---:|---|
| **Canais Digitais e Celulares Auditados** | 23 | Prontos para validação e abordagem direta via canal verificado |
| **Linhas Fixas (Não são WhatsApp)** | 23 | Bloqueados para WhatsApp; apenas ligação direta ou visita |
| **Celulares Cadastrados a Confirmar** | 28 | Exigem conferência prévia da bio/linktree antes do disparo |
| **Sem Telefone no Cadastro Inicial** | 10 | Necessitam busca ativa via Instagram |
| **Internacional (Argentina)** | 1 | Contato preferencial via Instagram Direct |

---

## 4. Top Estabelecimentos com Canais Digitais e Celulares Auditados

| ID | Estabelecimento | Telefone / Canal | Origem / Evidência |
|:---:|---|---|---|
| **52** | Camarão do Rafa | (48) 99865-6566 | Website oficial (`camaraodorafa.com.br`) |
| **53** | Jacks London Floripa | (48) 99642-2246 | Link oficial WhatsApp (`api.whatsapp.com`) |
| **36** | Restaurante Trilegal | (48) 99825-9338 | Instagram oficial (`restaurantetrilegal_oficial`) |
| **41** | Gigantes da Pizza | (48) 98837-3041 | Instagram oficial (`gigantesdapizza__`) |
| **42** | BARONG BURGUER | (48) 99129-9096 | Instagram oficial (`__barong_`) |
| **44** | Direto do Mar | (48) 99934-3505 | Instagram oficial (`diretodomar_canas`) |
| **56** | Milton Pizzaria | (48) 99646-5044 | Instagram oficial (`milton_pizzaria`) |
| **58** | Renascer Drinks | (48) 99990-1507 | Instagram oficial (`renascerdrinks.br`) |
| **63** | Pizzaria Firenze | (48) 99916-4173 | Cardápio Anota.ai (`firenzepizzaria`) |
| **67** | FLATY Burger | (48) 99122-1194 | Cardápio Web (`flaty_burger`) |
| **71** | Cafezim Floripa | (48) 99680-1477 | Instagram oficial (`cafezimfloripa`) |
| **77** | SEU BODEGA Gastrobar | (48) 98817-7469 | Instagram oficial (`seubodegagastrobar`) |
| **81** | Brazão Burguer | (48) 99183-5708 | Cardápio Anota.ai (`brazao-burguer`) |
| **6** | Brava Del Mar | (48) 98880-4141 | Website oficial (`bravadelmar.com`) |

---

## 5. Próximos Passos Recomendados

1. **Abordagem Piloto:** Iniciar contato exclusivamente com o grupo dos 14 estabelecimentos acima, cujos canais foram comprovados por presença digital ativa.
2. **Higienização Completa dos 28 Celulares Restantes:** Cruzar os nomes no Instagram antes de qualquer mensagem direta para confirmar se o número ativo no WhatsApp coincide com a bio atualizada.
3. **Protocolo para Linhas Fixas:** Caso haja interesse comercial em estabelecimentos de alto volume com linha fixa (ex: Galpão Gaúcho, Ecco Trattoria, Pizzaria Silvestre), realizar prospecção por ligação telefônica institucional ou visita presencial.

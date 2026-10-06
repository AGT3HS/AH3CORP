# Proposta de Nova Skill: auditoria-presenca-web (Fase 1 · dono: Radar)

**Data da Proposta:** 2026-10-02  
**Origem:** Inspiração em `VoltAgent/awesome-agent-skills` (módulo Firecrawl/Scraping avançado)  
**Status:** Aguardando validação do Augusto

---

## 1. Problema Identificado
A skill atual `auditoria-google-meu-negocio` extrai dados cadastrais e avaliações do Google Places, mas é cega para a conversão real fora do mapa:
- Não audita sites próprios, cardápios online ou motores de reserva.
- Falha quando sites bloqueiam raspagem simples (Cloudflare / SPAs em React).
- Deixa de capturar falhas técnicas graves (botão de WhatsApp quebrado, PDF ilegível no celular, carregamento lento).

---

## 2. Minuta da Nova Skill

```markdown
# SKILL: auditoria-presenca-web (Fase 1 · dono: Radar)
Leia antes: `BigBrain/travas.md`.

## Quando usar
Augusto diz "audita o site de [estabelecimento]" ou lead possui site/link de bio identificado na varredura.

## Entradas
URL do estabelecimento, nome, chave de API / engine de scraping em `.env`.

## Passos
1. Executar extração da página principal e subpáginas-chave (cardápio, reservas, contato).
2. Diagnosticar 4 pontos críticos de conversão:
   - **WhatsApp/Contato Direto:** Botão visível e clicável no mobile?
   - **Motor de Reservas / Cardápio:** Abre rápido ou depende de PDF pesado?
   - **Velocidade e Responsividade:** Bloqueios de renderização ou layout quebrado.
   - **Consistência de Marca:** Links para redes sociais ativos e atualizados.
3. Consolidar os 3 principais gargalos de perda de clientes em `handoff/auditoria-web-<slug>.md`.
4. Rascunhar abordagem consultiva e objetiva (máx 4 linhas, sem prometer ROI) destacando os gargalos encontrados.
5. Rodar `python scripts/verificar_texto.py` na abordagem.
6. Atualizar observações no `leads.csv`.
7. Registrar no ledger.

## Saída
`handoff/auditoria-web-<slug>.md` e abordagem em `handoff/abordagem-<slug>.md`.

## Ao final
Registre no ledger (`scripts/ledger_append.py`). Se algo falhou ou pode melhorar, escreva a SUGESTÃO em `handoff/melhorias/auditoria-presenca-web-<data>.md`. NÃO edite esta skill: o Augusto aprova e aplica.
```

---

## 3. Impacto Operacional
- **Sem conflito:** Complementa a varredura do `@Radar` sem sobrepor a skill de Google Meu Negócio.
- **Maior conversão na abordagem:** Fornece ao Augusto argumentos técnicos concretos e irrefutáveis para contato direto com o proprietário.

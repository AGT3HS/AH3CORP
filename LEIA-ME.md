# Pacote AH3 — como usar

## Instalação (uma vez)
1. Descompacte esta pasta em `C:\Users\Augusto\Desktop\AH3`.
2. Copie `.env.exemplo` para `.env` e preencha `GOOGLE_PLACES_API_KEY`.
3. No terminal: `pip install reportlab`.
4. No Hermes, crie os bots **Maestro** e **Radar**. Cole o conteúdo de `BigBrain/souls/maestro.md` e `radar.md` em cada campo SOUL.
   (Se o campo tiver limite de caracteres, mantenha só "Identidade", "Faz", "Não faz" e "Para se", e deixe o resto no arquivo.)
5. Mande o `BOOTSTRAP.md` para o Maestro.
6. Teste: "audita o [restaurante teste]".

## Fases
| Fase | Quando | O que liga |
|---|---|---|
| 1 | Agora | Maestro, Radar, 3 skills de prospecção + 4 de sistema |
| 2 | Ao fechar o 1º cliente | @Propostas, @Critical, contrato (revisado por advogado) |
| 3 | Sob demanda | @GestãoLocal, @Conteúdo, @Sites, @Mídia |

## Antes do primeiro cliente
- Definir o **valor mínimo** em `BigBrain/travas.md`.
- Revisar `modelos/contrato_base.md` com um advogado.
- Preencher CNPJ, endereço e foro no contrato.

## Regras de ouro
- Agentes NÃO editam skills nem souls. Sugerem em `handoff/melhorias/`; você decide.
- Palavras proibidas são conferidas por `scripts/verificar_texto.py`, não só por instrução.
- Rotinas (resumo das 08h) precisam de um disparador: agendador do Hermes ou Agendador de Tarefas do Windows.

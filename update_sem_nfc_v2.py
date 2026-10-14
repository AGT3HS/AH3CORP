import re

file_path = "scripts/gerar_proposta_aceleracao_sem_nfc.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update save paths
code = code.replace("Proposta_Aceleracao_Gastronomica_Oficial.pdf", "Proposta_Aceleracao_Gastronomica_Sem_NFC.pdf")
code = code.replace("previews_aceleracao_oficial", "previews_aceleracao_sem_nfc")

# 2. Slide 1 (Capa): Remove NFC item and layout as 3 grid items
s1_grid_old = """    <div class="s1-grid">
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">30 fotos profissionais</div>
          <div class="s1-card-desc">Pratos que dão água na boca</div>
        </div>
      </div>
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">Google Meu Negócio</div>
          <div class="s1-card-desc">Apareça quando a fome bater</div>
        </div>
      </div>
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        </div>
        <div>
          <div class="s1-card-title">Otimização do iFood</div>
          <div class="s1-card-desc">Venda mais e lucre mais por pedido</div>
        </div>
      </div>
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path></svg>
        </div>
        <div>
          <div class="s1-card-title">Plaquinhas NFC</div>
          <div class="s1-card-desc">Avaliação no Google em 1 toque</div>
        </div>
      </div>
    </div>"""

s1_grid_new = """    <div class="s1-grid" style="grid-template-columns: 1fr 1fr; grid-template-rows: auto auto;">
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">30 fotos profissionais</div>
          <div class="s1-card-desc">Pratos que dão água na boca</div>
        </div>
      </div>
      <div class="s1-card" style="grid-row: span 2;">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        </div>
        <div>
          <div class="s1-card-title">Estratégia Anti-Taxa iFood</div>
          <div class="s1-card-desc" style="line-height:1.4; margin-top:6px;">Uso da plataforma como isca para atrair clientes para o WhatsApp.</div>
        </div>
      </div>
      <div class="s1-card">
        <div class="s1-card-icon">
          <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        </div>
        <div>
          <div class="s1-card-title">Google Meu Negócio</div>
          <div class="s1-card-desc">Apareça quando a fome bater</div>
        </div>
      </div>
    </div>"""
code = code.replace(s1_grid_old, s1_grid_new)

# 3. Slide 5 (iFood): Change text without using regex that could match across slides
s5_target = """      <div class="right-cards-stack">
        <div class="alert-card-red">
          <div class="alert-text-top"><strong>Você pode estar pagando o iFood duas vezes:</strong> na comissão e no prejuízo escondido de um preço mal calculado.</div>
          <div class="alert-punchline">Encontramos esse vazamento e fechamos.</div>
        </div>
        <div class="result-card-green">
          <div class="result-tag">↑ RESULTADO ESPERADO</div>
          <div class="result-text">Mais pedidos por dia, mais lucro por pedido, mais recompra.</div>
        </div>
      </div>"""

s5_new = """      <div class="right-cards-stack">
        <div class="alert-card-red" style="padding: 16pt 22pt;">
          <div class="alert-text-top" style="font-size: 11.5pt;"><strong>O iFood é a maior vitrine de delivery do Brasil,</strong> mas deixar 20% a 27% de comissão em toda venda mata o seu lucro.</div>
          <div class="alert-text-top" style="font-size: 11.5pt; margin-bottom: 0;">A nossa estratégia usa o iFood apenas como isca para atrair novos clientes. Assim que o cliente faz o primeiro pedido, nós entregamos uma experiência que o faz pedir sempre direto pelo seu WhatsApp, <strong>revertendo todo o lucro da compra para você.</strong></div>
        </div>
        <div class="result-card-green">
          <div class="result-tag">↑ RESULTADO ESPERADO</div>
          <div class="result-text">Conquiste o cliente no iFood, mas lucre através do WhatsApp.</div>
        </div>
      </div>"""
code = code.replace(s5_target, s5_new)

# 4. Remove Slide 6 (NFC) completely!
# Slide 6 block is from:
# <!-- SLIDE 6: PILAR 4 PLAQUINHAS NFC -->
# up to just before:
# <!-- SLIDE 7: INVESTIMENTO -->

idx_start = code.find("<!-- SLIDE 6: PILAR 4 PLAQUINHAS NFC -->")
idx_end = code.find("<!-- SLIDE 7: INVESTIMENTO -->")
if idx_start != -1 and idx_end != -1:
    code = code[:idx_start] + code[idx_end:]

# Replace HTML page labels in footer:
code = code.replace("<!-- SLIDE 7: INVESTIMENTO -->", "<!-- SLIDE 6: INVESTIMENTO -->")
code = code.replace("<!-- SLIDE 8: PRÓXIMO PASSO -->", "<!-- SLIDE 7: PRÓXIMO PASSO -->")

code = code.replace('<div class="footer-page">07</div>', '<div class="footer-page">06</div>')
code = code.replace('<div class="footer-page">08</div>', '<div class="footer-page">07</div>')

# 6. Slide 7 (Now Slide 6) Investimento changes
bonus_text = """        <div class="s7-item-row bonus">
          <div>
            <div class="s7-item-info-title">Bônus · Plaquinhas NFC</div>
            <div class="s7-item-info-desc">2 de avaliação + 1 de cardápio</div>
          </div>
          <div>
            <div class="s7-item-price">Cortesia</div>
            <div class="s7-bonus-sub">valor R$ 135</div>
          </div>
        </div>"""
code = code.replace(bonus_text, "")

eco_old = """<div class="s7-pack-savings">Você leva R$ 1.935 em serviços · <strong>Economia de R$ 536</strong></div>"""
eco_new = """<div class="s7-pack-savings">Você leva R$ 1.800 em serviços · <strong>Economia de R$ 401</strong></div>"""
code = code.replace(eco_old, eco_new)

# Check if there are other economy bits
# Change Bônus from "Cortesia" to disappear, wait, we already removed it.

# Slide 8 (Now Slide 7) Próximo Passo changes
pas_old = """<div class="s8-step-desc">Fotos, Google, iFood e plaquinhas</div>"""
pas_new = """<div class="s8-step-desc">Fotos, Google e Otimização do iFood</div>"""
code = code.replace(pas_old, pas_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated OK, safe replacement.")

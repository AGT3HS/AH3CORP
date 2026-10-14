#!/usr/bin/env python3
"""
Gerador da Proposta Comercial Oficial - Costão do Santinho Resort
Seguindo rigorosamente o padrão canônico aprovado do Jurerê Beach Village:
- 11 slides em PDF paisagem
- Placa NFC 100% transparente com cantos arredondados (rx=60) e sem moldura branca
- Orçamento dinâmico com base no número de quartos do hotel (650 quartos x R$ 45 = R$ 29.250)
- Exibição de unidades totais sem preço unitário exposto
"""

import argparse, math, os, pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor, Color

ap = argparse.ArgumentParser()
ap.add_argument('--primary', default='#1B3A6B')
ap.add_argument('--accent', default='#C9A24B')
ap.add_argument('--hotel', default='Costão do Santinho Resort')
ap.add_argument('--quartos', type=int, default=650)
ap.add_argument('--autor', default='Augusto Henrique Dos Santos')
ap.add_argument('--tel', default='(48) 99908-8162')
ap.add_argument('--out', default='BigBrain/clientes/01_costao_do_santinho_resort/propostas/Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf')
a = ap.parse_args()

os.makedirs(os.path.dirname(a.out), exist_ok=True)
PLACA_IMG = 'BigBrain/clientes/01_costao_do_santinho_resort/propostas/placa_costao_transparente.png'

# Cálculo do investimento dinâmico (R$ 45 por plaquinha)
total_unidades = a.quartos
investimento_total = total_unidades * 45
investimento_fmt = f"R$ {investimento_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# ---------- paleta ----------
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
def tup(c): return (c.red, c.green, c.blue) if isinstance(c, Color) else c
def mix(c1, c2, t): return Color(*[x*(1-t) + y*t for x, y in zip(tup(c1), tup(c2))])

WH = (1, 1, 1); BK = (0, 0, 0); P = hx(a.primary); A = hx(a.accent)
lum = lambda c: 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
PRIMARY = Color(*P); PRIMARY_DARK = mix(P, BK, 0.25); PRIMARY_LIGHT = mix(P, WH, 0.10); PRIMARY_SOFT = mix(P, WH, 0.9)
ACCENT = Color(*A); GOLD_DARK = mix(A, BK, 0.32)
BG = Color(*hx('#FAF6EE')); CARD = Color(1, 1, 1); LINE = mix(A, WH, 0.62); SHADOW = Color(*hx('#E9E2D2'))
INK = mix(P, BK, 0.8); BODY = mix((0.35, 0.37, 0.37), P, 0.12); MUTED = mix((0.55, 0.57, 0.57), P, 0.1)
ON_P = Color(1, 1, 1) if lum(P) < 0.6 else INK
ON_P_SOFT = mix(WH, P, 0.12) if lum(P) < 0.6 else INK

W, H = 1308, 924
c = canvas.Canvas(a.out, pagesize=(842, 595))
c.setTitle('Proposta Comercial - Cartões NFC')
c.setAuthor(a.autor)
c.scale(842/W, 595/H)
Y = lambda y: H - y

def newpage(): c.showPage(); c.scale(842/W, 595/H)
def bg(col): c.setFillColor(col); c.rect(0, 0, W, H, stroke=0, fill=1)
def txt(s, x, y, font='Helvetica', size=16, col=INK, anchor='l', cs=0):
    t = c.beginText(); w = c.stringWidth(s, font, size) + cs*len(s)
    t.setTextOrigin(x - (w if anchor=='r' else w/2 if anchor=='c' else 0), Y(y))
    t.setFont(font, size); t.setCharSpace(cs); t.setFillColor(col); t.textOut(s); c.drawText(t)

def eyebrow(s, x, y, col=None):
    c.setFillColor(ACCENT); c.rect(x, Y(y-4), 34, 3, stroke=0, fill=1)
    txt(s.upper(), x+48, y, 'Helvetica-Bold', 13, col or GOLD_DARK, cs=4)

def para(s, x, y, w, font='Helvetica', size=17, col=BODY, lead=None):
    lead = lead or size*1.45
    for ln in simpleSplit(s, font, size, w):
        txt(ln, x, y, font, size, col); y += lead
    return y

def head(lines, x, y, size, col=INK, lead=None):
    for ln in lines: txt(ln, x, y, 'Times-Bold', size, col); y += lead or size*1.22
    return y

def footer(n):
    c.setFillColor(ACCENT); c.rect(75, Y(877), 34, 2, stroke=0, fill=1)
    txt('Proposta · Cartões NFC', 121, 881, 'Helvetica', 12, MUTED)
    txt(str(n), 1233, 881, 'Helvetica', 12, MUTED, anchor='r')

def card(x, y, w, h, fill=CARD, r=22):
    c.setFillColor(SHADOW); c.roundRect(x+5, Y(y+h)-5, w, h, r, stroke=0, fill=1)
    c.setFillColor(fill); c.roundRect(x, Y(y+h), w, h, r, stroke=0, fill=1)

def dot(x, y, col=None, r=6):
    c.setFillColor(col or ACCENT); c.circle(x, Y(y), r, stroke=0, fill=1)

def callout(x, y, w, h, s, size=17):
    card(x, y, w, h, r=14); c.setFillColor(ACCENT); c.roundRect(x, Y(y+h), 9, h, 4, stroke=0, fill=1)
    txt(s, x+32, y+h/2+6, 'Helvetica-Bold', size, PRIMARY)

def numdot(x, y, n, r=28, size=26):
    dot(x, y, PRIMARY, r); c.setStrokeColor(ACCENT); c.setLineWidth(2.5); c.circle(x, Y(y), r+4, stroke=1, fill=0)
    txt(str(n), x, y+size*0.35, 'Helvetica-Bold', size, ACCENT, anchor='c')

def bar(x, y):
    c.setFillColor(ACCENT); c.roundRect(x, Y(y+6), 50, 6, 3, stroke=0, fill=1)

def google_g(cx, cy, R, w):
    r = R - w/2; y0 = Y(cy); c.setLineWidth(w); c.setLineCap(0)
    for col, st, ex in [('#EA4335', 40, 110), ('#FBBC05', 150, 65), ('#34A853', 215, 105), ('#4285F4', 320, 40)]:
        c.setStrokeColor(HexColor(col)); c.arc(cx-r, y0-r, cx+r, y0+r, st, ex)
    c.setStrokeColor(HexColor('#4285F4')); c.line(cx, y0, cx+R-1, y0)

# ==========================================
# 1 CAPA
# ==========================================
bg(PRIMARY)
c.setFillColor(PRIMARY_LIGHT); c.circle(1250, Y(-40), 380, stroke=0, fill=1)
c.setFillColor(PRIMARY_DARK); c.circle(-20, Y(1000), 330, stroke=0, fill=1)

c.setStrokeColor(ACCENT); c.setLineCap(1); cx0, cy0 = 930, Y(470); c.setLineWidth(20)
for rr in (80, 150, 220): c.arc(cx0-rr, cy0-rr, cx0+rr, cy0+rr, -38, 76)
c.setFillColor(ACCENT); c.circle(cx0, cy0, 24, stroke=0, fill=1); c.setLineCap(0)

eyebrow('Proposta comercial', 87, 108, ACCENT)
y = head(['Cartões NFC', 'para a experiência', 'dos hóspedes.'], 87, 225, 76, ON_P, 92)
c.setFillColor(ACCENT); c.rect(90, Y(y+8), 90, 4, stroke=0, fill=1)
para('Informação do resort e cardápio gastronômico a um toque do celular — sempre atualizados.', 90, y+52, 700, size=22, col=ON_P_SOFT, lead=34)
txt('Preparada para: ' + a.hotel, 90, 780, 'Helvetica-Bold', 19, ACCENT)
txt('Por: %s  ·  %s' % (a.autor, a.tel), 90, 812, 'Helvetica', 17, ON_P_SOFT)
newpage()

# ==========================================
# 2 PONTO DE PARTIDA
# ==========================================
bg(BG); eyebrow('O ponto de partida', 87, 118)
head(['Mais tempo para o que importa.'], 87, 185, 52)
para('O hóspede chega com perguntas simples: qual é a senha do Wi-Fi? Até que horas vai o café da manhã? A piscina térmica está aberta? O que o restaurante serve hoje?', 87, 250, 900, size=21, lead=32)
for i, (t, d) in enumerate([
    ('Hoje', 'Informação espalhada entre recepção, placas e papéis impressos que envelhecem rápido.'),
    ('O custo', 'Equipe respondendo as mesmas perguntas e hóspede sem achar o que precisa.'),
    ('A proposta', 'Um cartão NFC no quarto e outro nos restaurantes: um toque abre tudo, atualizado.')
]):
    x = 87 + i*385; hi = (i == 2)
    card(x, 440, 350, 320, PRIMARY if hi else CARD); bar(x+28, 480)
    txt(t, x+28, 550, 'Times-Bold', 32, ACCENT if hi else PRIMARY)
    para(d, x+28, 595, 296, size=19, lead=29, col=ON_P_SOFT if hi else BODY)
footer(2); newpage()

# ==========================================
# 3 COMO FUNCIONA
# ==========================================
bg(BG); eyebrow('Como funciona', 87, 118)
head(['Três passos, nenhum aplicativo para baixar.'], 87, 185, 52)
for i, (t, d) in enumerate([
    ('Aproxime', 'O hóspede encosta o celular no cartão. O NFC funciona na maioria dos smartphones atuais.'),
    ('Abra', 'A página do resort abre direto no navegador: Wi-Fi, horários, serviços, eventos e mapa.'),
    ('Sempre atual', 'O hotel muda uma informação uma única vez e todos os cartões já mostram a versão nova.')
]):
    x = 87 + i*385; card(x, 270, 350, 340); numdot(x+62, 345, i+1)
    txt(t, x+28, 450, 'Times-Bold', 32, INK); para(d, x+28, 495, 296, size=19, lead=29)
callout(87, 680, 1133, 100, 'O segredo: o cartão guarda só um link. O conteúdo vive na página — por isso nunca fica desatualizado.', 19)
footer(3); newpage()

# ==========================================
# 4-6 PÁGINAS COM A PLACA TRANSPARENTE
# ==========================================
def side_page(n, eb, title, intro, items, note, x0, box=None, placa_x=None, placa_y=None):
    bg(BG); eyebrow(eb, x0, 123); head([title], x0, 188, 38)
    y = 236
    for ln in intro: txt(ln, x0, y, 'Helvetica', 16, BODY); y += 24
    y = 333
    for t, d in items:
        dot(x0+10, y-6, r=7); txt(t, x0+31, y, 'Helvetica-Bold', 20, PRIMARY); txt(d, x0+31, y+26, 'Helvetica', 16, BODY); y += 87
    if note and box: callout(box[0], box[1], box[2], box[3], note, 16)
    
    # Inserção da Placa 100% transparente com sombra suave projetada
    if placa_x and placa_y and os.path.exists(PLACA_IMG):
        c.saveState()
        # Sombra suave sob a placa transparente
        c.setFillColor(SHADOW); c.roundRect(placa_x+8, Y(placa_y+508)-8, 500, 500, 30, stroke=0, fill=1)
        c.drawImage(PLACA_IMG, placa_x, Y(placa_y+500), width=500, height=500, mask='auto', preserveAspectRatio=True)
        c.restoreState()
        
    footer(n); newpage()

side_page(4, 'Cartão 1 · Hóspedes', 'Para quem está hospedado.',
    ['Colocado no quarto e na recepção, libera', 'num toque o que o hóspede mais procura:'],
    [('Wi-Fi', 'Rede e senha, sem precisar pedir.'), ('Serviços', 'Café da manhã, piscinas, spa, academia.'),
     ('Programação', 'Atividades e entretenimento do resort.'), ('Horários', 'Funcionamento de cada espaço do complexo.')],
    None, 745, placa_x=87, placa_y=160)

side_page(5, 'Cartão 2 · Gastronomia', 'Para os restaurantes e bares.',
    ['Nas mesas e no balcão, um toque abre', 'o cardápio completo, sem papel:'],
    [('Pratos', 'Cardápio sempre na versão do dia.'), ('Bebidas', 'Drinks, vinhos, chopps e sucos.'),
     ('Sobremesas', 'Destaque para o que sai da confeitaria agora.'), ('Horários', 'Funcionamento e reservas dos restaurantes.')],
    'Prato esgotou? Atualiza na hora.', 87, (87, 700, 497, 80), placa_x=670, placa_y=160)

side_page(6, 'Cartão 3 · Lazer & Spa', 'Para quem busca bem-estar.',
    ['Nas recepções do Spa e Lazer, um toque leva', 'o hóspede direto ao que precisa:'],
    [('Agendar Spa', 'Massagens e rituais direto pelo WhatsApp.'), ('Complexo Esportivo', 'Quadras, golfe e trilhas com mapa interativo.'),
     ('Espaço Kids', 'Programação infantil e monitores.'), ('Atendimento', 'Canal direto de cada recepção temática.')],
    'Mudou a programação? Atualiza na hora.', 745, (745, 677, 476, 74), placa_x=87, placa_y=160)

# ==========================================
# 7 O QUE O HÓSPEDE VÊ
# ==========================================
bg(BG); eyebrow('O que o hóspede vê', 87, 118)
head(['Uma página que conecta', 'todos os serviços.'], 87, 190, 58)
para('Além do quarto, a mesma página apresenta os 6 restaurantes, o spa, a programação de lazer e o complexo esportivo; lista os próximos shows e eventos.', 87, 330, 880, size=21, lead=32)
chips = ['Informações do resort', 'Restaurantes & Bares', 'Spa & Bem-estar', 'Complexo Esportivo', 'Programação Infantil', 'Shows & Eventos']
for i, t in enumerate(chips):
    x = 87 + (i%3)*385; y = 440 + (i//3)*90
    card(x, y, 350, 70, r=16); c.setFillColor(PRIMARY_SOFT); c.circle(x+38, Y(y+35), 20, stroke=0, fill=1); dot(x+38, y+35, r=7)
    txt(t, x+72, y+42, 'Helvetica-Bold', 18, PRIMARY)
card(87, 640, 1133, 130, r=16); c.setFillColor(ACCENT); c.roundRect(87, Y(770), 9, 130, 4, stroke=0, fill=1)
txt('Novo: convite para avaliar no Google', 125, 688, 'Helvetica-Bold', 22, PRIMARY)
para('Ao fim da página, o hóspede satisfeito toca em "Avaliar no Google" e deixa sua nota em menos de 1 minuto — mais avaliações, mais visibilidade para o resort.', 125, 723, 1050, size=18, lead=27)
txt('Um canal único para divulgar o que o resort quiser, quando quiser.', 87, 826, 'Helvetica', 19, BODY)
footer(7); newpage()

# ==========================================
# 8 FOCO NO GOOGLE
# ==========================================
bg(BG); eyebrow('O foco do nosso serviço', 87, 118)
head(['Estadia melhor,', 'mais avaliações,', 'mais visibilidade.'], 87, 195, 58, lead=70)
para('Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito a avaliar o resort no Google. Mais avaliações recentes e boas notas mantêm o Costão no topo das buscas.', 87, 430, 520, size=18, lead=28)
card(735, 91, 490, 355)
for i, cl in enumerate(['#4285F4', '#EA4335', '#FBBC05', '#34A853']):
    c.setFillColor(HexColor(cl)); c.rect(735+i*122.5, Y(97), 122.5, 6, stroke=0, fill=1)
google_g(930, 140, 18, 7); txt('Avaliação', 958, 147, 'Helvetica-Bold', 19, HexColor('#5F6368'))
txt('Gostou da sua estadia?', 980, 208, 'Helvetica-Bold', 30, HexColor('#202124'), anchor='c')
txt('Avalie o Costão no Google. Leva menos de 1 minuto e', 980, 246, 'Helvetica', 16, HexColor('#5F6368'), anchor='c')
txt('ajuda outros viajantes a escolher nosso resort.', 980, 268, 'Helvetica', 16, HexColor('#5F6368'), anchor='c')

def star(cx, cy, r):
    p = c.beginPath()
    for k in range(10):
        ang = math.pi/2 + k*math.pi/5; rr = r if k%2==0 else r*0.42
        (p.moveTo if k==0 else p.lineTo)(cx + rr*math.cos(ang), cy + rr*math.sin(ang))
    p.close(); c.setFillColor(HexColor('#FBBC05')); c.drawPath(p, stroke=0, fill=1)

for k in range(5): star(980 - 124 + k*62, Y(312), 28)
c.setFillColor(HexColor('#4285F4')); c.roundRect(838, Y(424), 284, 58, 29, stroke=0, fill=1)
c.setFillColor(Color(1, 1, 1)); c.circle(871, Y(395), 20, stroke=0, fill=1); google_g(871, 395, 13, 5.5)
txt('Avaliar no Google', 1000, 402, 'Helvetica-Bold', 20, Color(1, 1, 1), anchor='c')

for i, (t, d) in enumerate([
    ('Estadia melhor', 'Wi-Fi, mapa e serviços a um toque: zero atrito para o hóspede.'),
    ('Convite certo', 'A página do cartão traz o botão "Avaliar no Google" no ponto alto da estadia.'),
    ('Mais avaliações', 'Hóspedes satisfeitos avaliam em menos de 1 minuto, direto do celular.'),
    ('Mais ranking', 'Volume e nota das avaliações consolidam a liderança do resort no Google.')
]):
    x = 87 + i*289; card(x, 640, 268, 190, r=18); numdot(x+38, 684, i+1, r=17, size=16)
    txt(t, x+72, 690, 'Helvetica-Bold', 18, INK); para(d, x+22, 730, 226, size=14, lead=21)
footer(8); newpage()

# ==========================================
# 9 POR QUE VALE
# ==========================================
bg(BG); eyebrow('Por que vale para o resort', 87, 118)
head(['Menos atrito, mais experiência.'], 87, 190, 56)
for i, (t, d) in enumerate([
    ('Informação sempre correta', 'Mudou o horário do restaurante? A programação infantil? Edita uma vez, todos os cartões refletem.'),
    ('Recepção mais ágil', 'Perguntas repetidas sobre Wi-Fi e horários são resolvidas instantaneamente pelo próprio cartão.'),
    ('Percepção de modernidade', 'Um gesto simples e sofisticado que encanta o hóspede e reforça o padrão 5 estrelas.'),
    ('Consumo nos restaurantes', 'Gastronomia, spa e passeios ganham visibilidade máxima para quem já está no complexo.')
]):
    x = 87 + (i%2)*575; y = 270 + (i//2)*270; card(x, y, 545, 235); bar(x+34, y+38)
    txt(t, x+34, y+100, 'Times-Bold', 30, INK); para(d, x+34, y+145, 475, size=19, lead=29)
footer(9); newpage()

# ==========================================
# 10 PRÓXIMOS PASSOS & INVESTIMENTO DINÂMICO
# ==========================================
bg(BG); eyebrow('Próximos passos', 87, 118)
head(['Vamos implantar juntos?'], 87, 190, 56)

# Card da Esquerda: Entregáveis e Quantidades
card(87, 260, 640, 520)
txt('Proposta de implantação', 117, 312, 'Helvetica-Bold', 22, PRIMARY)

y = 360
entregaveis = [
    ('Cartões para apartamentos e suítes', f'{total_unidades} unidades'),
    ('Cartões para recepções e lounges', 'Incluso no lote'),
    ('Página digital e atualizações em nuvem', 'Incluso'),
    ('Prazo estimado de entrega', '7 a 10 dias úteis')
]

for tit, val in entregaveis:
    txt(tit, 117, y, 'Helvetica-Bold', 18, INK)
    txt(val, 690, y, 'Helvetica', 17, PRIMARY, anchor='r')
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(117, Y(y+22), 690, Y(y+22))
    y += 75

para('Expansão para restaurantes, bares e spa: veja a próxima página.', 117, y+5, 580, 'Helvetica', 15, MUTED)
txt('1  Reunião de alinhamento para validar conteúdo e artes', 117, 725, 'Helvetica', 16, BODY)
txt('2  Produção física, configuração de links e entrega técnica', 117, 752, 'Helvetica', 16, BODY)

# Card da Direita: Investimento Total
c.setFillColor(PRIMARY); c.roundRect(760, Y(780), 460, 520, 22, stroke=0, fill=1)
eyebrow('Investimento total', 795, 312, ACCENT)

txt(f'{total_unidades} cartões inteligentes', 795, 360, 'Helvetica', 18, ON_P_SOFT)
txt(investimento_fmt, 795, 430, 'Times-Bold', 44, ON_P)

c.setStrokeColor(ON_P_SOFT); c.setLineWidth(1.5); c.line(795, Y(465), 1180, Y(465))
txt('Forma de pagamento', 795, 510, 'Helvetica-Bold', 18, ACCENT)
txt('50% na aprovação do projeto', 795, 545, 'Helvetica', 17, ON_P_SOFT)
txt('50% na entrega e ativação dos cartões', 795, 580, 'Helvetica', 17, ON_P_SOFT)

c.setStrokeColor(ON_P_SOFT); c.setLineWidth(1.5); c.line(795, Y(620), 1180, Y(620))
txt('Vamos conversar?', 795, 680, 'Times-Bold', 28, ON_P)
txt(a.autor, 795, 715, 'Helvetica', 16, ON_P_SOFT)
txt(a.tel, 795, 740, 'Helvetica', 16, ON_P_SOFT)

footer(10); newpage()

# ==========================================
# 11 EXPANSÃO
# ==========================================
bg(BG); eyebrow('Proposta de expansão', 87, 100)
head(['O próximo passo: o toque chega a mais complexos.'], 87, 160, 46)
txt('Mesma tecnologia NFC: atualiza uma vez, todos os cartões refletem.', 87, 195, 'Helvetica', 17, BODY)

for x, eb, t, d, bl in [
    (87, 'Cartão · Gastronomia', 'Restaurantes & Bares', 'Nas mesas e no balcão, um toque abre o cardápio completo, sem papel.',
     ['Cardápios de todos os restaurantes na versão do dia', 'Prato esgotou ou mudou safra? Atualiza na hora', 'Horários, reservas e eventos gastronômicos']),
    (670, 'Cartão · Spa & Bem-estar', 'Costão Spa & Lazer', 'Um toque libera agendamento de massagens, tratamentos e quadras.',
     ['Agendamento de massagens e rituais pelo WhatsApp', 'Mapa interativo de trilhas e complexo esportivo', 'Atendimento e recepção do centro de bem-estar'])
]:
    card(x, 250, 550, 400); eyebrow(eb, x+30, 300); txt(t, x+30, 348, 'Helvetica-Bold', 30, PRIMARY)
    para(d, x+30, 385, 490, size=17, lead=25); y = 470
    for b in bl: dot(x+36, y-6, r=6); y = para(b, x+56, y, 470, size=17, lead=25) + 12
    c.setStrokeColor(LINE); c.setLineWidth(1.5); c.line(x+30, Y(580), x+520, Y(580))
    eyebrow('Investimento', x+30, 616); txt('Sob consulta de volume adicional.', x+30, 642, 'Helvetica-Bold', 20, INK)

c.setFillColor(PRIMARY); c.roundRect(87, Y(840), 1133, 110, 20, stroke=0, fill=1)
c.setFillColor(ACCENT); c.roundRect(87, Y(840), 9, 110, 4, stroke=0, fill=1)
txt('Vamos conversar?', 125, 775, 'Times-Bold', 28, ON_P)
txt('%s  ·  %s' % (a.autor, a.tel), 125, 810, 'Helvetica', 17, ON_P_SOFT)
footer(11); c.save()
print("PDF da proposta do Costão gerado com sucesso:", a.out)

# Renderização PNG dos slides para conferência
doc = pymupdf.open(a.out)
out_dir = os.path.join(os.path.dirname(a.out), 'slides_preview')
os.makedirs(out_dir, exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    p_png = os.path.join(out_dir, f"slide_{i+1:02d}.png")
    pix.save(p_png)
print("Slides renderizados em:", out_dir)

import argparse
#!/usr/bin/env python3
"""
AH3 — Gerador Oficial de Proposta Comercial de Hotelaria (8 Lâminas / Padrão Editorial Fiel Costão & Noturno Luxo)
Base canônica: Proposta_Comercial_Cartoes_NFC_Costao_do_Santinho.pdf
- Plaquinha NFC: sem cantos brancos (transparência real nos cantos rx=60), modelo 02_modelo_noturno_luxo oficial.
- Página 5: Fiel ao padrão Costão (layout editorial com 3 colunas de telas mobile personalizadas para o Oceania Park Hotel + card Google Reviews à esquerda).
- Página 6: Fiel ao padrão Costão (Foco do nosso serviço + Mockup Google Reviews com 5 estrelas e botão 'Avaliar no Google' + grid de 4 etapas numeradas).
- Previews estritamente em 150 DPI.
"""

import math

import re

def extrair_dados_svg_itens(svg_path, hotel_nome):
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
        texts = re.findall(r'<text[^>]*>(.*?)</text>', content)
        texts = [t.replace('&amp;', '&').strip() for t in texts]
        
        try:
            idx_utl = texts.index('UM TOQUE LIBERA')
        except ValueError:
            idx_utl = 2
            
        itens = []
        i = idx_utl + 1
        while i + 1 < len(texts) and len(itens) < 4:
            titulo = texts[i]
            sub = texts[i+1]
            if 'Florianópolis' in titulo or '.com' in titulo or 'EXPERIÊNCIA' in titulo:
                break
            itens.append((titulo, sub))
            i += 2
        return itens
    except Exception:
        return []
import os
import subprocess
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor, Color
import pymupdf

def render_svg_exact_transparent(svg_path, out_png_path, size=1000, radius=60):
    os.makedirs(os.path.dirname(out_png_path), exist_ok=True)
    png_cand = svg_path.replace('.svg', '.png')
    if os.path.exists(png_cand):
        im = Image.open(png_cand).convert('RGBA')
        w, h = im.size
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
        im.putalpha(mask)
        im.save(out_png_path, 'PNG')
        return out_png_path

    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ background: transparent; width: {size}px; height: {size}px; overflow: hidden; }}
  svg {{ width: {size}px; height: {size}px; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

    html_file = out_png_path + ".html"
    raw_png = out_png_path + ".raw.png"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--window-size={size},{size}",
        f"--screenshot={os.path.abspath(raw_png)}",
        f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)
    try: os.remove(html_file)
    except: pass

    # Aplicação de máscara alpha nos cantos para eliminar qualquer fundo branco residual
    im = Image.open(raw_png).convert('RGBA')
    w, h = im.size
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    im.putalpha(mask)
    im.save(out_png_path, 'PNG')
    try: os.remove(raw_png)
    except: pass
    return out_png_path

def gerar_apresentacao_lead(
    hotel_name: str,
    svg_placa: str,
    telas_mobile: list,
    resumo_servicos_p5: str,
    primary_hex: str = "#0D3B66",
    accent_hex: str = "#EE964B",
    autor: str = "Augusto Henrique Dos Santos",
    tel: str = "(48) 99908-8162",
    out_pdf: str = None
):
    if not out_pdf:
        slug = hotel_name.lower().replace(" ", "_").replace("&", "e")
        out_pdf = f"saida/propostas/Proposta_Comercial_{slug}.pdf"
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    
    # 1. Renderização exata da placa oficial sem fundo branco nos cantos
    placa_png = os.path.join(os.path.dirname(out_pdf), "placa_02_noturno_luxo_transparente.png")
    render_svg_exact_transparent(svg_placa, placa_png, size=1000, radius=60)
    
    # 2. Setup de Cores e Canvas
    def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
    def tup(c): return (c.red,c.green,c.blue) if isinstance(c,Color) else c
    def mix(c1,c2,t): return Color(*[x*(1-t)+y*t for x,y in zip(tup(c1),tup(c2))])
    
    WH=(1,1,1); BK=(0,0,0); P=hx(primary_hex); A=hx(accent_hex)
    lum=lambda c:0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
    PRIMARY=Color(*P); PRIMARY_DARK=mix(P,BK,0.25); PRIMARY_LIGHT=mix(P,WH,0.10); PRIMARY_SOFT=mix(P,WH,0.9)
    ACCENT=Color(*A); GOLD_DARK=mix(A,BK,0.32)
    BG=Color(*hx('#FAF6EE')); CARD=Color(1,1,1); LINE=mix(A,WH,0.62); SHADOW=Color(*hx('#E9E2D2'))
    INK=mix(P,BK,0.8); BODY=mix((0.35,0.37,0.37),P,0.12); MUTED=mix((0.55,0.57,0.57),P,0.1)
    ON_P=Color(1,1,1) if lum(P)<0.6 else INK
    ON_P_SOFT=mix(WH,P,0.12) if lum(P)<0.6 else INK
    
    W, H = 1308, 924
    c = canvas.Canvas(out_pdf, pagesize=(842, 595))
    c.setTitle(f'Apresentação Executiva - Cartões NFC {hotel_name}')
    c.setAuthor(autor)
    c.scale(842/W, 595/H)
    Y = lambda y: H - y
    
    def newpage(): c.showPage(); c.scale(842/W, 595/H)
    def bg(col): c.setFillColor(col); c.rect(0,0,W,H,stroke=0,fill=1)
    def txt(s,x,y,font='Helvetica',size=16,col=INK,anchor='l',cs=0):
        t=c.beginText(); w=c.stringWidth(s,font,size)+cs*len(s)
        t.setTextOrigin(x-(w if anchor=='r' else w/2 if anchor=='c' else 0),Y(y)); t.setFont(font,size); t.setCharSpace(cs); t.setFillColor(col); t.textOut(s); c.drawText(t)
    def eyebrow(s,x,y,col=None):
        c.setFillColor(ACCENT); c.rect(x,Y(y-4),34,3,stroke=0,fill=1)
        txt(s.upper(),x+48,y,'Helvetica-Bold',13,col or GOLD_DARK,cs=4)
    def para(s,x,y,w,font='Helvetica',size=17,col=BODY,lead=None):
        lead=lead or size*1.45
        for ln in simpleSplit(s,font,size,w): txt(ln,x,y,font,size,col); y+=lead
        return y
    def head(lines,x,y,size,col=INK,lead=None):
        for ln in lines: txt(ln,x,y,'Times-Bold',size,col); y+=lead or size*1.22
        return y
    def footer(n):
        c.setFillColor(ACCENT); c.rect(75,Y(877),34,2,stroke=0,fill=1)
        txt(f'Apresentação · Cartões NFC {hotel_name}',121,881,'Helvetica',12,MUTED); txt(str(n),1233,881,'Helvetica',12,MUTED,anchor='r')
    def card(x,y,w,h,fill=CARD,r=22):
        c.setFillColor(SHADOW); c.roundRect(x+5,Y(y+h)-5,w,h,r,stroke=0,fill=1)
        c.setFillColor(fill); c.roundRect(x,Y(y+h),w,h,r,stroke=0,fill=1)
    def dot(x,y,col=None,r=6): c.setFillColor(col or ACCENT); c.circle(x,Y(y),r,stroke=0,fill=1)
    def callout(x,y,w,h,s,size=17):
        card(x,y,w,h,r=14); c.setFillColor(ACCENT); c.roundRect(x,Y(y+h),9,h,4,stroke=0,fill=1)
        txt(s,x+32,y+h/2+6,'Helvetica-Bold',size,PRIMARY)
    def numdot(x,y,n,r=28,size=26):
        dot(x,y,PRIMARY,r); c.setStrokeColor(ACCENT); c.setLineWidth(2.5); c.circle(x,Y(y),r+4,stroke=1,fill=0)
        txt(str(n),x,y+size*0.35,'Helvetica-Bold',size,ACCENT,anchor='c')
    def bar(x,y): c.setFillColor(ACCENT); c.roundRect(x,Y(y+6),50,6,3,stroke=0,fill=1)
    def google_g(cx,cy,R,w):
        r=R-w/2; y0=Y(cy); c.setLineWidth(w); c.setLineCap(0)
        for col,st,ex in [('#EA4335',40,110),('#FBBC05',150,65),('#34A853',215,105),('#4285F4',320,40)]:
            c.setStrokeColor(HexColor(col)); c.arc(cx-r,y0-r,cx+r,y0+r,st,ex)
        c.setStrokeColor(HexColor('#4285F4')); c.line(cx,y0,cx+R-1,y0)

    # ==========================================
    # SLIDE 1: CAPA
    # ==========================================
    bg(PRIMARY)
    c.setFillColor(PRIMARY_LIGHT); c.circle(1250,Y(-40),380,stroke=0,fill=1)
    c.setFillColor(PRIMARY_DARK); c.circle(-20,Y(1000),330,stroke=0,fill=1)
    
    # Placa Original Modelo Noturno Luxo com cantos total transparentes
    c.saveState()
    c.drawImage(placa_png, 750, Y(710), width=450, height=450, preserveAspectRatio=True, mask='auto')
    c.restoreState()
    
    eyebrow('Apresentação',87,108,ACCENT)
    y=head(['Cartões NFC','para a experiência','dos hóspedes.'],87,225,74,ON_P,90)
    c.setFillColor(ACCENT); c.rect(90,Y(y+8),90,4,stroke=0,fill=1)
    para(f'Toda a infraestrutura, serviços e gastronomia do {hotel_name} acessíveis em um toque. Sempre atualizados.',90,y+52,620,size=21,col=ON_P_SOFT,lead=32)
    txt(f'Preparada para: {hotel_name}',90,780,'Helvetica-Bold',19,ACCENT)
    txt(f'Por: {autor}  ·  {tel}',90,812,'Helvetica',17,ON_P_SOFT)
    newpage()

    # ==========================================
    # SLIDE 2: O DIA A DIA DO HOTEL
    # ==========================================
    bg(BG); eyebrow('O dia a dia do hotel', 87, 118)
    head(['As mesmas perguntas, todos os dias.'], 87, 185, 52)
    
    duvidas = [
        ('Qual é a senha do Wi-Fi?', '#0D3B66'),
        ('Até que horas vai o café da manhã?', '#EE964B'),
        ('As piscinas e SPA estão abertos?', '#FBBC05'),
        ('O que a gastronomia serve hoje?', '#2E7D32')
    ]
    
    for i, (q, col) in enumerate(duvidas):
        x = 87 + (i % 2) * 575
        y = 265 + (i // 2) * 110
        card(x, y, 550, 92, r=16)
        c.setFillColor(HexColor(col))
        c.circle(x + 46, Y(y + 46), 22, stroke=0, fill=1)
        num_col = INK if col == '#FBBC05' else Color(1,1,1)
        txt('?', x + 46, y + 54, 'Times-Bold', 22, num_col, anchor='c')
        txt(q, x + 85, y + 53, 'Times-Bold', 22, INK)
        
    card(87, 515, 1125, 230, r=18)
    c.setFillColor(ACCENT); c.roundRect(87, Y(745), 9, 230, 4, stroke=0, fill=1)
    txt('O custo de não ter um lugar único', 125, 565, 'Helvetica-Bold', 24, PRIMARY)
    para('A informação fica espalhada entre recepção, placas e papéis impressos que envelhecem rápido. A equipe repete as mesmas respostas dezenas de vezes por dia, e o hóspede nem sempre encontra o que precisa no momento ideal.', 125, 608, 1040, size=18, col=BODY, lead=28)
    footer(2); newpage()

    # ==========================================
    # SLIDE 3: COMO FUNCIONA
    # ==========================================
    bg(BG); eyebrow('Como funciona',87,118)
    head(['Três passos, nenhum aplicativo para baixar.'],87,185,52)
    for i,(t,d) in enumerate([
        ('Aproxime','O hóspede encosta o celular no cartão. O chip NFC integrado abre a página instantaneamente.'),
        ('Abra','A página oficial do hotel abre direto no navegador: Wi-Fi, horários, SPA, gastronomia e lazer.'),
        ('Sempre atual','A equipe do hotel atualiza o conteúdo uma única vez e todos os cartões já mostram a versão nova.')
    ]):
        x=87+i*385; card(x,270,350,350); numdot(x+62,345,i+1)
        txt(t,x+28,450,'Times-Bold',32,INK); para(d,x+28,495,296,size=18,lead=27)
    callout(87,680,1133,100,'O segredo: o cartão guarda apenas o link inteligente. O conteúdo vive na nuvem — por isso nunca desatualiza.',19)
    footer(3); newpage()

    # ==========================================
    # SLIDE 4: O CARTÃO NFC INTELIGENTE (Modelo Noturno Luxo Oficial)
    # ==========================================
    bg(BG); eyebrow('Cartão Inteligente · Hóspedes', 745, 123); head(['Para quem está hospedado.'], 745, 188, 38)
    y = 236
    intro_lines = ['Instalado nos quartos e na recepção, libera','em um toque tudo o que o hóspede procura:']
    for ln in intro_lines: txt(ln, 745, y, 'Helvetica', 16, BODY); y += 24
    y = 333
    itens_card = [
        ('Wi-Fi & Acesso', 'Rede guest e instruções na tela, sem filas.'),
        ('Serviços & Lazer', 'Piscinas, recreação, academia e horários.'),
        ('Gastronomia', 'Restaurantes, cardápios e room service.'),
        ('Eventos & Suporte', 'Programação do dia e contato direto.')
    ]
    for t, d in itens_card:
        dot(745 + 10, y - 6, r=7)
        txt(t, 745 + 31, y, 'Helvetica-Bold', 20, PRIMARY)
        txt(d, 745 + 31, y + 26, 'Helvetica', 16, BODY)
        y += 87
    callout(745, 680, 480, 80, 'Mudou o horário? Atualiza na hora na nuvem.', 16)
    
    # Plaquinha NFC Modelo Noturno Luxo com cantos total transparentes
    c.saveState()
    c.drawImage(placa_png, 100, Y(660), width=480, height=480, preserveAspectRatio=True, mask='auto')
    c.restoreState()
    footer(4); newpage()

        # ==========================================
    # SLIDE 5: O QUE O HÓSPEDE VÊ (Dinâmico e Personalizado com dados reais do SVG)
    # ==========================================
    bg(BG); eyebrow('O que o hóspede vê', 75, 105)
    head(['Uma página que conecta','todo o hotel.'], 75, 155, 42, lead=48)
    para(resumo_servicos_p5, 75, 275, 460, size=17, lead=25)
    
    # Card de Destaque Google Reviews à esquerda
    card(75, 410, 460, 220, r=16)
    c.setFillColor(ACCENT); c.roundRect(75, Y(630), 8, 220, 4, stroke=0, fill=1)
    txt('Novo: convite para avaliar no Google', 105, 445, 'Helvetica-Bold', 18, PRIMARY)
    para("Ao fim da página, o hóspede satisfeito toca em 'Avaliar no Google' e deixa sua nota em menos de 1 minuto — mais avaliações e maior nota média para o posicionamento do hotel.", 105, 480, 410, size=15, col=BODY, lead=22)
    
    txt('Um canal único para divulgar o que o hotel quiser,', 75, 680, 'Helvetica-Bold', 17, PRIMARY)
    txt('quando quiser. Sem limites de atualização.', 75, 705, 'Helvetica-Bold', 17, PRIMARY)

    # Extração dinâmica dos 4 serviços do SVG
    itens_svg = extrair_dados_svg_itens(svg_placa, hotel_name)
    it1 = itens_svg[0] if len(itens_svg) > 0 else ("GASTRONOMIA", "Restaurante e café da manhã")
    it2 = itens_svg[1] if len(itens_svg) > 1 else ("LAZER & PISCINA", "Área de lazer e descanso")
    it3 = itens_svg[2] if len(itens_svg) > 2 else ("BEM-ESTAR & SPA", "Massagens e relaxamento")
    it4 = itens_svg[3] if len(itens_svg) > 3 else ("SERVIÇOS & EVENTOS", "Recepção 24h e estrutura")

    # Primeiro nome ou sigla do hotel para rede Wi-Fi
    primeiro_nome = hotel_name.replace('Hotel', '').replace('Resort', '').strip().split()[0] if len(hotel_name.split()) > 1 else hotel_name

    telas_dinamicas = [
        {
            "kicker": "HOSPEDE-SE NO HOTEL",
            "header": hotel_name.upper()[:22],
            "bg": PRIMARY,
            "cards": [
                ("WI-FI GUEST", f"Rede: {primeiro_nome} Guest\nInstruções na tela"),
                ("CHECK-IN / OUT", "Check-in: 14h · Check-out: 11h\nRecepção 24h"),
                ("CAFÉ DA MANHÃ", "06h30 às 10h00\nRestaurante Principal"),
                ("ESTACIONAMENTO", "Serviço com manobrista")
            ]
        },
        {
            "kicker": "SABOREIE & RELAXE",
            "header": "GASTRONOMIA & LAZER",
            "bg": Color(0.08, 0.20, 0.32),
            "cards": [
                (it1[0].upper()[:20], f"{it1[1][:32]}\nConsulte horários e menu"),
                (it2[0].upper()[:20], f"{it2[1][:32]}\nDisponível aos hóspedes"),
                ("ROOM SERVICE", "Cardápio digital 24h\nDireto no quarto")
            ]
        },
        {
            "kicker": "HOJE NO HOTEL",
            "header": "SERVIÇOS & AVALIAÇÃO",
            "bg": PRIMARY,
            "cards": [
                (it3[0].upper()[:20], f"{it3[1][:32]}"),
                (it4[0].upper()[:20], f"{it4[1][:32]}"),
                ("FITNESS CENTER", "Academia climatizada"),
                ("★ ★ ★ ★ ★", "Avaliar no Google\nAjude outros hóspedes!")
            ]
        }
    ]

    mockup_w = 215
    mockup_h = 580
    start_mx = 575
    gap_m = 25
    my = 120

    for col_idx, t in enumerate(telas_dinamicas):
        tx = start_mx + col_idx * (mockup_w + gap_m)
        card(tx, my, mockup_w, mockup_h, r=22)

        # Header da tela mobile
        c.setFillColor(t["bg"])
        c.roundRect(tx + 6, Y(my + 80), mockup_w - 12, 74, 16, stroke=0, fill=1)
        txt(t["kicker"], tx + 16, my + 30, 'Helvetica-Bold', 9, ACCENT, cs=1)
        txt(t["header"], tx + 16, my + 54, 'Times-Bold', 12, Color(1,1,1))

        cy = my + 95
        for ctitle, cdesc in t["cards"]:
            is_stars = "★" in ctitle
            card_box_h = 88 if "\n" in cdesc else 72
            box_bg = Color(*hx('#FFF8E7')) if is_stars else Color(*hx('#F5F3EF'))

            c.setFillColor(box_bg)
            c.roundRect(tx + 12, Y(cy + card_box_h), mockup_w - 24, card_box_h, 10, stroke=0, fill=1)

            if is_stars:
                txt(ctitle, tx + 22, cy + 24, 'Helvetica-Bold', 15, ACCENT)
                txt(cdesc.split("\n")[0], tx + 22, cy + 48, 'Helvetica-Bold', 11, PRIMARY)
                if len(cdesc.split("\n")) > 1:
                    txt(cdesc.split("\n")[1], tx + 22, cy + 66, 'Helvetica', 10, MUTED)
            else:
                txt(ctitle, tx + 22, cy + 22, 'Helvetica-Bold', 11, PRIMARY)
                lines = cdesc.split("\n")
                ly = cy + 42
                for l in lines:
                    txt(l, tx + 22, ly, 'Helvetica', 10, BODY)
                    ly += 16

            cy += card_box_h + 10

    footer(5); newpage()

    # ==========================================
    # SLIDE 6: O FOCO DO NOSSO SERVIÇO (Padrão Oficial com Card Google Vertical Centralizado)
    # ==========================================
    bg(BG); eyebrow('Um bônus que aparece sozinho', 75, 105)
    head(['Estadia melhor,','mais avaliações,','mais visibilidade.'], 75, 160, 48, lead=56)
    para(f'Além de melhorar a experiência durante a estadia, o cartão leva o hóspede satisfeito a avaliar o hotel no Google no momento de pico de satisfação. Mais avaliações recentes e boas notas consolidam a liderança do {hotel_name} no Google Maps.', 75, 360, 560, size=16, lead=25)
    
    # Mockup Google Review no canto superior direito (Formato Vertical e total Centralizado - Fiel à Referência)
    card_gw = 480
    card_gh = 380
    card_gx = 740
    card_gy = 85
    card_gcx = card_gx + card_gw / 2
    
    card(card_gx, card_gy, card_gw, card_gh, r=22)
    
    # Faixa superior de 4 cores Google
    stripe_w = card_gw / 4
    for i, cl in enumerate(['#4285F4', '#EA4335', '#FBBC05', '#34A853']):
        c.setFillColor(HexColor(cl))
        c.rect(card_gx + i * stripe_w, Y(card_gy + 6), stripe_w, 6, stroke=0, fill=1)
    
    # Cabeçalho: 'G' + 'Avaliação' centralizado
    google_g(card_gcx - 46, card_gy + 42, 12, 4.5)
    txt('Avaliação', card_gcx - 24, card_gy + 46, 'Helvetica-Bold', 17, HexColor('#5F6368'))
    
    # Título: 'Gostou da sua estadia?' centralizado
    txt('Gostou da sua estadia?', card_gcx, card_gy + 96, 'Times-Bold', 26, HexColor('#202124'), anchor='c')
    
    # Texto descritivo centralizado
    sub_lines = [
        f'Avalie o {hotel_name} no Google. Leva menos',
        f'de 1 minuto e ajuda outros hóspedes a nos encontrar.'
    ]
    for idx_sl, sl in enumerate(sub_lines):
        txt(sl, card_gcx, card_gy + 138 + idx_sl * 22, 'Helvetica', 14, HexColor('#5F6368'), anchor='c')
    
    # 5 Estrelas Douradas Centralizadas
    def star_p6(cx, cy, r):
        p = c.beginPath()
        for k in range(10):
            ang = math.pi/2 + k * math.pi/5
            rr = r if k % 2 == 0 else r * 0.42
            (p.moveTo if k == 0 else p.lineTo)(cx + rr * math.cos(ang), cy + rr * math.sin(ang))
        p.close()
        c.setFillColor(HexColor('#FBBC05'))
        c.drawPath(p, stroke=0, fill=1)

    star_spacing = 38
    start_star_x = card_gcx - (2 * star_spacing)
    for k in range(5):
        star_p6(start_star_x + k * star_spacing, Y(card_gy + 225), 16)

    # Botão de Ação Google Centralizado na base com ícone G
    btn_w = 360
    btn_h = 52
    btn_x = card_gcx - btn_w / 2
    btn_y = card_gy + 285
    c.setFillColor(HexColor('#4285F4'))
    c.roundRect(btn_x, Y(btn_y + btn_h), btn_w, btn_h, btn_h / 2, stroke=0, fill=1)
    
    # Ícone G dentro do botão
    c.setFillColor(Color(1,1,1))
    c.circle(btn_x + 36, Y(btn_y + btn_h / 2), 14, stroke=0, fill=1)
    google_g(btn_x + 36, btn_y + btn_h / 2, 9, 3.5)
    
    # Texto do Botão
    txt('Avaliar no Google', card_gcx + 12, btn_y + btn_h / 2 + 6, 'Helvetica-Bold', 17, Color(1,1,1), anchor='c')
    
    # 4 Cards Inferiores (Grid Linear de 4 Etapas)
    grid_w = 270
    grid_h = 240
    start_gx = 75
    gap_g = 22
    gy = 510
    
    workflow_steps = [
        ("Estadia\nmelhor", "Wi-Fi, horários e serviços\na um toque: menos atrito\npara o hóspede.", '#4285F4'),
        ("Convite\ncerto", "A página do cartão traz\no botão 'Avaliar no Google'\nno fim da visita.", '#EE964B'),
        ("Mais\navaliações", "Hóspedes satisfeitos avaliam\nem menos de 1 minuto, direto\ndo celular.", '#FBBC05'),
        ("Mais\nranking", "Volume e nota das avaliações\npesam na posição do hotel\nno Google.", '#0D3B66')
    ]
    
    for idx, (titulo, desc, cor_hex) in enumerate(workflow_steps):
        bx = start_gx + idx * (grid_w + gap_g)
        card(bx, gy, grid_w, grid_h, r=18)
        
        # Círculo numerado colorido
        c.setFillColor(HexColor(cor_hex))
        c.circle(bx + 45, Y(gy + 45), 20, stroke=0, fill=1)
        num_col = INK if cor_hex == '#FBBC05' else Color(1,1,1)
        txt(str(idx + 1), bx + 45, gy + 52, 'Helvetica-Bold', 17, num_col, anchor='c')
        
        # Título
        lines_t = titulo.split("\n")
        ty = gy + 110
        for lt in lines_t:
            txt(lt, bx + 28, ty, 'Times-Bold', 24, INK)
            ty += 28
            
        # Descrição
        ty += 12
        lines_d = desc.split("\n")
        for ld in lines_d:
            txt(ld, bx + 28, ty, 'Helvetica', 14, MUTED)
            ty += 20
            
    footer(6); newpage()

    # ==========================================
    # SLIDE 7: O QUE MUDA PARA O HOTEL & PRÓXIMO PASSO (Pitch Lead Frio sem Preço)
    # ==========================================
    bg(BG); eyebrow('O que muda para o hotel', 75, 105)
    head(['Menos atrito, mais experiência.'], 75, 155, 42)
    
    pilares = [
        ('Informação sempre correta', 'Mudou o café ou o Wi-Fi? Edita uma vez na nuvem e todos os cartões refletem na hora.', '#2E7D32'),
        ('Recepção mais leve', 'Dúvidas repetitivas passam a ser resolvidas no próprio quarto pelo celular.', '#EE964B'),
        ('Percepção de modernidade', 'Um toque inteligente e elegante que o hóspede nota, elogia e compartilha.', '#FBBC05'),
        ('Venda cruzada & Consumo', 'Restaurantes, spa, eventos e lazer ganham visibilidade máxima durante a estadia.', '#0D3B66')
    ]
    
    grid_pw = 280
    grid_ph = 230
    for i, (t, d, col_p) in enumerate(pilares):
        px = 75 + (i % 2) * (grid_pw + 20)
        py = 230 + (i // 2) * (grid_ph + 20)
        card(px, py, grid_pw, grid_ph, r=18)
        c.setFillColor(HexColor(col_p))
        c.roundRect(px + 20, Y(py + 26), 40, 5, 2, stroke=0, fill=1)
        txt(t, px + 20, py + 65, 'Times-Bold', 20, INK)
        para(d, px + 20, py + 95, grid_pw - 40, size=15, lead=22, col=BODY)
        
    cx_r = 695
    card(cx_r, 230, 535, 480, fill=PRIMARY, r=22)
    
    eyebrow('Próximo passo', cx_r + 35, 275, ACCENT)
    txt('Vamos testar juntos?', cx_r + 35, 335, 'Times-Bold', 34, ON_P)
    
    para('Se fizer sentido para o seu hotel, o próximo passo é uma conversa rápida de alinhamento. Em seguida, desenhamos a proposta sob medida.', cx_r + 35, 380, 465, size=17, col=ON_P_SOFT, lead=26)
    
    c.setStrokeColor(mix(WH,P,0.3)); c.setLineWidth(1); c.line(cx_r + 35, Y(460), cx_r + 500, Y(460))
    
    passos_teste = [
        ('1', 'Reunião rápida para validar conteúdo e identidade visual das telas'),
        ('2', 'Apresentação da proposta de implantação sob medida e prazos')
    ]
    
    sy = 495
    for n_p, d_p in passos_teste:
        numdot(cx_r + 55, sy + 15, n_p, r=18, size=16)
        para(d_p, cx_r + 90, sy + 5, 400, font='Helvetica-Bold', size=15, col=ON_P, lead=20)
        sy += 65
        
    c.setStrokeColor(mix(WH,P,0.3)); c.setLineWidth(1); c.line(cx_r + 35, Y(620), cx_r + 500, Y(620))
    
    txt('Vamos conversar?', cx_r + 35, 655, 'Times-Bold', 22, ACCENT)
    txt(f'{autor}  ·  {tel}', cx_r + 35, 685, 'Helvetica', 16, ON_P)
    footer(7)
    
    c.save()
    print(f"PDF 8 Slides gerado com sucesso em: {out_pdf}")

    # 3. Exportar todas as 8 Lâminas em PNG de 150 DPI (estritamente 150 DPI)
    preview_dir = os.path.join(os.path.dirname(out_pdf), "slides_preview")
    if os.path.exists(preview_dir):
        for f in os.listdir(preview_dir):
            if f.endswith('.png'):
                try: os.remove(os.path.join(preview_dir, f))
                except: pass
    os.makedirs(preview_dir, exist_ok=True)
    doc_out = pymupdf.open(out_pdf)
    for i in range(len(doc_out)):
        page = doc_out[i]
        pix = page.get_pixmap(dpi=150)
        img_p = os.path.join(preview_dir, f"slide_{i+1:02d}.png")
        pix.save(img_p)
        print(f"Preview Slide {i+1}: {img_p}")

def main():
    parser = argparse.ArgumentParser(description="Gerador Canônico Oficial de Apresentação Comercial para Leads Frios (7 Slides)")
    parser.add_argument("--hotel", required=True, help="Nome do hotel")
    parser.add_argument("--svg-placa", required=True, help="Caminho do SVG da placa")
    parser.add_argument("--resumo-p5", required=True, help="Resumo dos servicos para a pagina 5")
    parser.add_argument("--primary", default="#0D3B66", help="Cor primaria em hex")
    parser.add_argument("--accent", default="#EE964B", help="Cor de acento em hex")
    parser.add_argument("--autor", default="Augusto Henrique Dos Santos", help="Nome do autor")
    parser.add_argument("--tel", default="(48) 99908-8162", help="Telefone de contato")
    parser.add_argument("--output", default=None, help="Caminho do PDF de saida")
    args = parser.parse_args()

    primeira_palavra = args.hotel.split()[0]
    telas = [
        {
            "kicker": "HOSPEDE-SE NO HOTEL",
            "header": args.hotel.upper(),
            "bg": HexColor(args.primary),
            "cards": [
                ("WI-FI GUEST", "Rede: " + primeira_palavra + " Guest - Instrucoes na tela"),
                ("CHECK-IN / OUT", "Check-in: 14h - Check-out: 11h - Recepcao 24h"),
                ("CAFE DA MANHA", "06h30 as 10h00 - Restaurante Principal"),
                ("ESTACIONAMENTO", "Servico disponivel no local")
            ]
        },
        {
            "kicker": "SABOREIE & RELAXE",
            "header": "GASTRONOMIA & LAZER",
            "bg": HexColor(args.primary),
            "cards": [
                ("RESTAURANTE", "Gastronomia selecionada - Almoco e jantar a la carte"),
                ("SPA & BEM-ESTAR", "Massagens e terapias - Agende na recepcao"),
                ("ROOM SERVICE", "Cardapio digital 24h - Direto no quarto")
            ]
        },
        {
            "kicker": "HOJE NO HOTEL",
            "header": "EXPERIENCIA & AVALIACAO",
            "bg": HexColor(args.primary),
            "cards": [
                ("PISCINAS & LAZER", "Complexo aberto aos hospedes"),
                ("EVENTOS & SALAS", "Infraestrutura corporativa"),
                ("FITNESS CENTER", "Academia climatizada"),
                ("* * * * *", "Avaliar no Google - Ajude outros hospedes!")
            ]
        }
    ]

    gerar_apresentacao_lead(
        hotel_name=args.hotel,
        svg_placa=args.svg_placa,
        telas_mobile=telas,
        resumo_servicos_p5=args.resumo_p5,
        primary_hex=args.primary,
        accent_hex=args.accent,
        autor=args.autor,
        tel=args.tel,
        out_pdf=args.output
    )

if __name__ == '__main__':
    main()

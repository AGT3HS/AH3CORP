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

def gerar_proposta_hotelaria(
    hotel_name: str,
    quartos: int,
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
    c.setTitle(f'Proposta Comercial - Cartões NFC {hotel_name}')
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
        txt(f'Proposta · Cartões NFC {hotel_name}',121,881,'Helvetica',12,MUTED); txt(str(n),1233,881,'Helvetica',12,MUTED,anchor='r')
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
    
    eyebrow('Proposta comercial',87,108,ACCENT)
    y=head(['Cartões NFC','para a experiência','dos hóspedes.'],87,225,74,ON_P,90)
    c.setFillColor(ACCENT); c.rect(90,Y(y+8),90,4,stroke=0,fill=1)
    para(f'Toda a infraestrutura, serviços e gastronomia do {hotel_name} acessíveis em um toque. Sempre atualizados.',90,y+52,620,size=21,col=ON_P_SOFT,lead=32)
    txt(f'Preparada para: {hotel_name}',90,780,'Helvetica-Bold',19,ACCENT)
    txt(f'Por: {autor}  ·  {tel}',90,812,'Helvetica',17,ON_P_SOFT)
    newpage()

    # ==========================================
    # SLIDE 2: O PONTO DE PARTIDA
    # ==========================================
    bg(BG); eyebrow('O ponto de partida',87,118)
    head(['Mais tempo para o que importa.'],87,185,52)
    para(f'O hóspede chega com dúvidas simples: qual é a senha do Wi-Fi? Até que horas vai o café da manhã? Onde agendo o SPA? Quais os horários das piscinas e eventos?',87,250,900,size=21,lead=32)
    for i,(t,d) in enumerate([
        ('Hoje','Informação espalhada entre recepção, placas e impressos que envelhecem rápido e geram atrito.'),
        ('O custo','Equipe da recepção sobrecarregada respondendo as mesmas perguntas repetitivas.'),
        ('A proposta','Um cartão NFC no quarto e nos pontos de contato: um toque abre tudo no celular, sempre atualizado.')
    ]):
        x=87+i*385; hi=(i==2)
        card(x,440,350,320,PRIMARY if hi else CARD); bar(x+28,480)
        txt(t,x+28,550,'Times-Bold',32,ACCENT if hi else PRIMARY)
        para(d,x+28,595,296,size=19,lead=29,col=ON_P_SOFT if hi else BODY)
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
    bg(BG); eyebrow('O foco do nosso serviço', 75, 105)
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
        f'Avalie o Oceania Park Hotel no Google. Leva menos',
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
    # SLIDE 7: POR QUE VALE PARA O HOTEL
    # ==========================================
    bg(BG); eyebrow('Por que vale para o hotel', 87, 118)
    head(['Menos atrito operacional,','mais valor percebido.'], 87, 190, 56)
    for i,(t,d) in enumerate([
        ('Informação sempre correta','Mudou o horário do café? A senha do Wi-Fi? Edita na nuvem uma vez e todos os cartões refletem na hora.'),
        ('Recepção mais ágil','Perguntas repetitivas passam a ser respondidas instantaneamente pelo próprio cartão nos quartos.'),
        ('Percepção de modernidade','Um toque inteligente e elegante que o hóspede nota, elogia e compartilha.'),
        ('Consumo e Venda Cruzada','Restaurantes, spa, bar da piscina e convenções ganham visibilidade máxima para quem já está hospedado.')
    ]):
        x=87+(i%2)*575; y=270+(i//2)*270; card(x,y,545,235); bar(x+34,y+38)
        txt(t,x+34,y+100,'Times-Bold',30,INK); para(d,x+34,y+145,475,size=19,lead=29)
    footer(7); newpage()

    # ==========================================
    # SLIDE 8: PRÓXIMOS PASSOS & INVESTIMENTO DINÂMICO
    # ==========================================
    total_invest = quartos * 45
    parcela = total_invest / 2
    
    bg(BG); eyebrow('Próximos passos', 87, 118)
    head(['Vamos testar juntos?'], 87, 190, 56)
    
    card(87, 260, 640, 520)
    txt('Proposta de Implantação', 117, 305, 'Helvetica-Bold', 22, PRIMARY)
    txt(f'{hotel_name}', 117, 330, 'Helvetica-Bold', 18, INK)
    
    itens_impl = [
        (f'Cartões Inteligentes NFC', f'{quartos} unidades (1 por acomodação). Placas em acrílico resinado nobre com chip NFC de alta durabilidade e QR Code de contingência.'),
        ('Suporte de Tecnologia', '2 anos de cobertura técnica e integridade total dos chips NFC em todas as placas.'),
        ('Plataforma Web & Atualizações', 'Hospedagem em nuvem de alta velocidade. 1º mês incluso na implantação.'),
        ('Prazo de Entrega', '15 dias úteis a partir da aprovação final das artes e direcionamentos.')
    ]
    
    y = 370
    for tit, dsc in itens_impl:
        txt(tit, 117, y, 'Helvetica-Bold', 17, INK)
        para(dsc, 117, y + 24, 560, font='Helvetica', size=14, col=MUTED, lead=20)
        c.setStrokeColor(LINE); c.setLineWidth(1); c.line(117, Y(y + 75), 680, Y(y + 75))
        y += 88
        
    txt('1  Validação do conteúdo e identidade visual das placas', 117, 725, 'Helvetica', 15, BODY)
    txt('2  Produção física, codificação técnica e entrega presencial', 117, 752, 'Helvetica', 15, BODY)
    
    # Bloco de Investimento
    c.setFillColor(PRIMARY); c.roundRect(760, Y(780), 460, 520, 22, stroke=0, fill=1)
    eyebrow('Investimento total', 795, 312, ACCENT)
    txt(f'R$ {total_invest:,.2f}'.replace(',','X').replace('.',',').replace('X','.'), 795, 375, 'Times-Bold', 46, ON_P)
    txt(f'Implantação completa de {quartos} cartões inteligentes.', 795, 420, 'Helvetica', 15, ON_P_SOFT)
    
    c.setStrokeColor(ON_P_SOFT); c.setLineWidth(1.5); c.line(795, Y(450), 1180, Y(450))
    
    txt('Condições de pagamento:', 795, 490, 'Helvetica-Bold', 18, ACCENT)
    txt(f'• 50% na aprovação do pedido: R$ {parcela:,.2f}'.replace(',','X').replace('.',',').replace('X','.'), 795, 530, 'Helvetica', 16, ON_P)
    txt(f'• 50% na entrega e ativação técnica: R$ {parcela:,.2f}'.replace(',','X').replace('.',',').replace('X','.'), 795, 565, 'Helvetica', 16, ON_P)
    
    c.line(795, Y(610), 1180, Y(610))
    txt('Vamos conversar?', 795, 665, 'Times-Bold', 28, ON_P)
    txt(autor, 795, 705, 'Helvetica-Bold', 17, ON_P)
    txt(tel, 795, 735, 'Helvetica', 17, ACCENT)
    footer(8)
    
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
    parser = argparse.ArgumentParser(description="Gerador Canonico Oficial de Propostas Comerciais de Hotelaria AH3 (8 Slides)")
    parser.add_argument("--hotel", required=True, help="Nome do hotel")
    parser.add_argument("--quartos", type=int, required=True, help="Numero de quartos")
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

    gerar_proposta_hotelaria(
        hotel_name=args.hotel,
        quartos=args.quartos,
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

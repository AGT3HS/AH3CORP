import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

W, H = A4

themes = [
    {
        'id': '01_v2_warm_orange',
        'title': '01. V2 Warm Light & Hero Dark',
        'sub': 'Frutos do Mar e Litoral',
        'bg': colors.HexColor('#FAFAF5'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#1F2430'),
        'accent': colors.HexColor('#F26A21'),
        'text': colors.HexColor('#1F2430'),
        'muted': colors.HexColor('#6B7280'),
        'border': colors.HexColor('#E5E1DA')
    },
    {
        'id': '02_dark_obsidian',
        'title': '02. Dark Obsidian & Neon Orange',
        'sub': 'Choperias, Pubs & Burgers',
        'bg': colors.HexColor('#0E0E0E'),
        'card': colors.HexColor('#181818'),
        'hero': colors.HexColor('#222222'),
        'accent': colors.HexColor('#F26522'),
        'text': colors.HexColor('#F4F4F4'),
        'muted': colors.HexColor('#7C7C7C'),
        'border': colors.HexColor('#2C2C2C')
    },
    {
        'id': '03_slate_executive',
        'title': '03. Slate Executive Minimalist',
        'sub': 'Restaurantes Executivos & Redes',
        'bg': colors.HexColor('#F8FAFC'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#0F172A'),
        'accent': colors.HexColor('#2563EB'),
        'text': colors.HexColor('#0F172A'),
        'muted': colors.HexColor('#64748B'),
        'border': colors.HexColor('#E2E8F0')
    },
    {
        'id': '04_tuscan_terracotta',
        'title': '04. Tuscan Terracotta & Sage',
        'sub': 'Pizzarias & Trattorias',
        'bg': colors.HexColor('#FBF8F3'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#2C221E'),
        'accent': colors.HexColor('#C85A32'),
        'text': colors.HexColor('#2C221E'),
        'muted': colors.HexColor('#786A63'),
        'border': colors.HexColor('#E8DEC8')
    },
    {
        'id': '05_nordic_roast',
        'title': '05. Nordic Roast & Amber Wood',
        'sub': 'Parrillas & Churrascarias',
        'bg': colors.HexColor('#F5F3EF'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#1E1B18'),
        'accent': colors.HexColor('#D97706'),
        'text': colors.HexColor('#1E1B18'),
        'muted': colors.HexColor('#736C64'),
        'border': colors.HexColor('#E4DFD7')
    },
    {
        'id': '06_atlantic_navy',
        'title': '06. Atlantic Deep Navy & Seafoam',
        'sub': 'Petiscarias & Beach Points',
        'bg': colors.HexColor('#F0F4F8'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#0C1E36'),
        'accent': colors.HexColor('#0284C7'),
        'text': colors.HexColor('#0C1E36'),
        'muted': colors.HexColor('#5E718D'),
        'border': colors.HexColor('#CBD5E1')
    },
    {
        'id': '07_cyber_midnight',
        'title': '07. Cyber Midnight & Electric Lime',
        'sub': 'Dark Kitchens & Delivery',
        'bg': colors.HexColor('#121316'),
        'card': colors.HexColor('#1C1E24'),
        'hero': colors.HexColor('#252830'),
        'accent': colors.HexColor('#84CC16'),
        'text': colors.HexColor('#F3F4F6'),
        'muted': colors.HexColor('#9CA3AF'),
        'border': colors.HexColor('#2E323D')
    },
    {
        'id': '08_bordeaux_luxury',
        'title': '08. Bordeaux Editorial & Rose Gold',
        'sub': 'Bistrôs & Fine Dining',
        'bg': colors.HexColor('#FAF8F7'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#2A0E18'),
        'accent': colors.HexColor('#8B1E3F'),
        'text': colors.HexColor('#2A0E18'),
        'muted': colors.HexColor('#79636A'),
        'border': colors.HexColor('#EDE4E6')
    },
    {
        'id': '09_kyoto_zen',
        'title': '09. Kyoto Zen & Wasabi Leaf',
        'sub': 'Sushi & Culinária Oriental',
        'bg': colors.HexColor('#F7F8F5'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#1A1D20'),
        'accent': colors.HexColor('#4D7C0F'),
        'text': colors.HexColor('#1A1D20'),
        'muted': colors.HexColor('#626A5D'),
        'border': colors.HexColor('#E2E6DF')
    },
    {
        'id': '10_sunset_coral',
        'title': '10. Sunset Island Coral & Gold',
        'sub': 'Beach Clubs & Sunset Bars',
        'bg': colors.HexColor('#FCF9F5'),
        'card': colors.HexColor('#FFFFFF'),
        'hero': colors.HexColor('#211815'),
        'accent': colors.HexColor('#F95738'),
        'text': colors.HexColor('#211815'),
        'muted': colors.HexColor('#7E6A63'),
        'border': colors.HexColor('#EBE3DA')
    }
]

os.makedirs('BigBrain/handoff/catalogo_10_designs', exist_ok=True)

for t in themes:
    out_pdf = f"BigBrain/handoff/catalogo_10_designs/{t['id']}.pdf"
    c = canvas.Canvas(out_pdf, pagesize=A4)
    
    for page_num in range(1, 4):
        # Fundo
        c.setFillColor(t['bg'])
        c.rect(0, 0, W, H, fill=True, stroke=False)
        
        # Barra de topo
        c.setFillColor(t['accent'])
        c.rect(0, H - 6, W, 6, fill=True, stroke=False)
        
        # Header
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(t['accent'])
        c.drawString(40, H - 32, f"AUDITORIA DE PRESENÇA DIGITAL · {t['sub'].upper()}")
        
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(t['text'])
        c.drawString(40, H - 56, 'Paixão Restaurante & Pizzaria')
        
        c.setFont('Helvetica', 9)
        c.setFillColor(t['muted'])
        c.drawString(40, H - 72, f"Design System: {t['title']}")
        
        c.setFont('Helvetica-Bold', 9.5)
        c.setFillColor(t['text'])
        c.drawRightString(W - 40, H - 32, f"Página 0{page_num} / 03")
        
        c.setStrokeColor(t['border'])
        c.setLineWidth(1.0)
        c.line(40, H - 84, W - 40, H - 84)
        c.line(40, 38, W - 40, 38)
        
        # Footer
        c.setFont('Helvetica', 8)
        c.setFillColor(t['muted'])
        c.drawString(40, 24, f"AH3 Intelligence · {t['title']}")
        c.drawRightString(W - 40, 24, f"Página 0{page_num} / 03")
        
        cx = W / 2.0 - 28
        for i in range(1, 4):
            c.setFillColor(t['accent'] if i == page_num else t['border'])
            c.rect(cx + (i - 1) * 20, 22, 16, 4, fill=True, stroke=False)
            
        if page_num == 1:
            # Hero Box
            c.setFillColor(t['hero'])
            c.rect(40, H - 180, W - 80, 86, fill=True, stroke=False)
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 110, 'O QUE A AUDITORIA MOSTRA')
            c.setFont('Helvetica-Bold', 16)
            c.setFillColor(colors.white)
            c.drawString(56, H - 132, 'Você é o 1º em Volume no Norte da Ilha.')
            c.setFont('Helvetica', 8.5)
            c.setFillColor(colors.HexColor('#D1D5DB') if t['hero'] != colors.white else t['muted'])
            c.drawString(56, H - 150, 'Perfil líder com 5.385 avaliações e nota 4.5★ nos Ingleses.')
            c.drawString(56, H - 162, 'Oportunidade de blindagem de autoridade e cardápio mobile de conversão direta.')
            
            # Cards NAP
            c.setFillColor(t['card'])
            c.setStrokeColor(t['border'])
            c.setLineWidth(0.8)
            c.rect(40, H - 286, W - 80, 92, fill=True, stroke=True)
            c.setFont('Helvetica-Bold', 7)
            c.setFillColor(t['muted'])
            c.drawString(56, H - 204, 'NOME OFICIAL')
            c.drawString(250, H - 204, 'CATEGORIA')
            c.drawString(430, H - 204, 'STATUS')
            c.setFont('Helvetica-Bold', 9)
            c.setFillColor(t['text'])
            c.drawString(56, H - 218, 'Paixão Restaurante & Pizzaria')
            c.drawString(250, H - 218, 'Frutos do Mar & Pizzaria')
            c.drawString(430, H - 218, '✓ Perfil Verificado')
            
            # 4 KPIs
            w_kpi = (W - 80 - 24) / 4.0
            kpis = [('SCORE PRESENÇA', '90/100', t['text']), ('TOTAL AVALIAÇÕES', '5.385', t['accent']), ('NOTA MÉDIA', '4.5 ★', t['text']), ('POTENCIAL', '+40%', colors.HexColor('#1E9E5A'))]
            for ki, (kt, kv, kc) in enumerate(kpis):
                kx = 40 + ki * (w_kpi + 8)
                c.setFillColor(t['card'])
                c.setStrokeColor(t['border'])
                c.rect(kx, H - 380, w_kpi, 76, fill=True, stroke=True)
                c.setFont('Helvetica-Bold', 6.5)
                c.setFillColor(t['muted'])
                c.drawString(kx + 10, H - 310, kt)
                c.setFont('Helvetica-Bold', 15)
                c.setFillColor(kc)
                c.drawString(kx + 10, H - 338, kv)
                c.setFont('Helvetica', 7.5)
                c.setFillColor(t['muted'])
                c.drawString(kx + 10, H - 360, 'Métrica consolidada')
                
            # Pilares
            c.setFillColor(t['card'])
            c.setStrokeColor(t['border'])
            c.rect(40, H - 520, W - 80, 126, fill=True, stroke=True)
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 410, '03. PILARES DE PERFORMANCE LOCAL')
            pilares = [('Dados NAP', 0.95), ('Volume de Reviews', 0.92), ('Fotos & Mídia', 0.85), ('Recência', 0.70), ('Taxa de Resposta', 0.40), ('Cardápio Mobile', 0.25)]
            for pi, (pn, pv) in enumerate(pilares):
                py = H - 430 - pi * 14
                c.setFont('Helvetica-Bold', 7.5)
                c.setFillColor(t['text'])
                c.drawString(56, py, pn)
                c.setFillColor(colors.HexColor('#E5E7EB'))
                c.rect(180, py - 2, 280, 7, fill=True, stroke=False)
                c.setFillColor(t['accent'])
                c.rect(180, py - 2, 280 * pv, 7, fill=True, stroke=False)
                
            # Callout
            c.setFillColor(t['card'])
            c.setStrokeColor(t['accent'])
            c.rect(40, H - 590, W - 80, 56, fill=True, stroke=True)
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 544, 'DIAGNÓSTICO EXECUTIVO')
            c.setFont('Helvetica', 8)
            c.setFillColor(t['text'])
            c.drawString(56, H - 560, 'Líder consolidado de volume nos Ingleses. Acelerar respostas e implementar cardápio web.')
            c.drawString(56, H - 572, 'Placas inteligentes no salão garantem a sustentação do 1º lugar frente a concorrentes.')
            
        elif page_num == 2:
            # Tabela Ranking
            c.setFillColor(t['card'])
            c.setStrokeColor(t['border'])
            c.rect(40, H - 380, W - 80, 270, fill=True, stroke=True)
            c.setFont('Helvetica-Bold', 9)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 110, '04. RANKING COMPETITIVO REGIONAL')
            
            concorrentes = [
                ('1º', 'Paixão Restaurante & Pizzaria', '4.5 ★', '5.385', 'ALVO AUDITADO', True),
                ('2º', 'Don Zarichta Pizzaria', '4.9 ★', '5.230', 'Direto', False),
                ('3º', 'Costillas Grill', '4.3 ★', '4.791', 'Cross-Nicho', False),
                ('4º', 'Freguesia Bar', '4.4 ★', '4.377', 'Direto', False),
                ('5º', 'Villa do Porto', '4.6 ★', '3.983', 'Direto', False),
                ('6º', "Antonio's Restaurante", '4.7 ★', '3.918', 'Direto', False),
                ('7º', 'Camarão Chef Seghetto', '4.6 ★', '3.857', 'Direto', False),
                ('8º', 'Pizzaria Happy', '4.6 ★', '3.771', 'Direto', False)
            ]
            for ri, (rpos, rnom, rnot, rrev, rtag, is_alvo) in enumerate(concorrentes):
                ry = H - 136 - ri * 28
                if is_alvo:
                    c.setFillColor(t['accent'])
                    c.rect(42, ry - 6, W - 84, 24, fill=True, stroke=False)
                    c.setFillColor(colors.white)
                else:
                    c.setFillColor(t['text'])
                c.setFont('Helvetica-Bold', 8)
                c.drawString(56, ry + 2, rpos)
                c.drawString(90, ry + 2, rnom)
                c.drawString(280, ry + 2, rnot)
                c.drawString(340, ry + 2, rrev)
                c.drawString(420, ry + 2, rtag)
                
            # 3 Pilares Ação
            w_ac = (W - 80 - 16) / 3.0
            planos = [('01', 'IMPACTO IMEDIATO', 'Cardápio Mobile Próprio'), ('02', 'MOTOR DE REVIEWS', 'Placas NFC & QR Code'), ('03', 'BLINDAGEM SEO', 'Gestão Ativa de Feedback')]
            for pi, (pnum, ptag, ptit) in enumerate(planos):
                px = 40 + pi * (w_ac + 8)
                c.setFillColor(t['card'])
                c.setStrokeColor(t['border'])
                c.rect(px, H - 560, w_ac, 160, fill=True, stroke=True)
                c.setFont('Helvetica-Bold', 18)
                c.setFillColor(t['accent'])
                c.drawString(px + 12, H - 420, pnum)
                c.setFont('Helvetica-Bold', 7)
                c.setFillColor(t['muted'])
                c.drawString(px + 12, H - 438, ptag)
                c.setFont('Helvetica-Bold', 8.5)
                c.setFillColor(t['text'])
                c.drawString(px + 12, H - 458, ptit)
                c.setFont('Helvetica', 7.5)
                c.setFillColor(t['muted'])
                c.drawString(px + 12, H - 480, 'Execução técnica em até')
                c.drawString(px + 12, H - 492, '7 a 10 dias com foco em')
                c.drawString(px + 12, H - 504, 'conversão de clientes.')
                
        elif page_num == 3:
            # Resumo Status
            w_st = (W - 80 - 16) / 3.0
            stats = [('CONFORME', '7 / 10', colors.HexColor('#1E9E5A')), ('ATENÇÃO', '2 / 10', colors.HexColor('#E8A317')), ('CRÍTICO', '1 / 10', colors.HexColor('#D6403A'))]
            for si, (st, sv, sc) in enumerate(stats):
                sx = 40 + si * (w_st + 8)
                c.setFillColor(t['card'])
                c.setStrokeColor(t['border'])
                c.rect(sx, H - 170, w_st, 64, fill=True, stroke=True)
                c.setFont('Helvetica-Bold', 7)
                c.setFillColor(sc)
                c.drawString(sx + 10, H - 120, st)
                c.setFont('Helvetica-Bold', 16)
                c.setFillColor(sc)
                c.drawString(sx + 10, H - 144, sv)
                
            # Checklist
            c.setFillColor(t['card'])
            c.setStrokeColor(t['border'])
            c.rect(40, H - 480, W - 80, 296, fill=True, stroke=True)
            c.setFont('Helvetica-Bold', 8.5)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 196, '07. CHECKLIST AUDITADO ITEM A ITEM')
            
            chk = [
                '01. Nome Comercial (NAP) padronizado no Google',
                '02. Marcador de GPS geolocalizado com precisão',
                '03. Telefone oficial com DDD local ativo',
                '04. Horários de funcionamento atualizados',
                '05. Galeria de fotos profissionais do salão',
                '06. Volume de avaliações acima de 5.000 reviews',
                '07. Taxa de resposta ativa a novos clientes',
                '08. Recência e fluxo contínuo de avaliações',
                '09. Cardápio digital mobile indexado no Google',
                '10. Botão direto para reservas no WhatsApp'
            ]
            for ci, ct in enumerate(chk):
                cy = H - 222 - ci * 25
                c.setFillColor(t['accent'])
                c.circle(52, cy + 3, 3.5, fill=True, stroke=False)
                c.setFont('Helvetica', 8)
                c.setFillColor(t['text'])
                c.drawString(64, cy + 1, ct)
                c.setStrokeColor(t['border'])
                c.setLineWidth(0.4)
                c.line(46, cy - 6, W - 46, cy - 6)
                
            # CTA Final
            c.setFillColor(t['hero'])
            c.rect(40, H - 560, W - 80, 68, fill=True, stroke=False)
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(t['accent'])
            c.drawString(56, H - 510, 'PRÓXIMO PASSO RECOMENDADO')
            c.setFont('Helvetica', 8)
            c.setFillColor(colors.white)
            c.drawString(56, H - 528, 'Ativar a blindagem da liderança através do cardápio mobile próprio e displays NFC.')
            c.drawString(56, H - 540, 'Entre em contato para iniciar a implementação técnica sem complicações.')
            
        c.showPage()
        
    c.save()
    print(f"[✓] Gerado PDF: {out_pdf}")

print("Catálogo com 10 designs gerado com sucesso!")

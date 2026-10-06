import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

# PALETA & SOBRETONS EXECUTIVOS
BG_DARK = (10, 25, 45)          # #0A192D (Azul Petróleo Profundo)
BG_DARK_MID = (20, 42, 70)      # #142A46
BG_CREAM = (248, 246, 240)      # #F8F6F0 (Creme Editorial Nobre)
BG_LIGHT_TINT = (240, 243, 246) # #F0F3F6 (Cinza Nobre Suave)

CARD_WHITE = (255, 255, 255)
CARD_WARM = (252, 250, 246)
BORDER_SUBTLE = (226, 230, 235)
BORDER_WARM = (235, 230, 220)

NAVY = (13, 34, 54)             # #0D2236
NAVY_ACCENT = (26, 75, 120)     # #1A4B78
GOLD = (248, 175, 53)           # #F8AF35
GOLD_MUTED = (212, 145, 30)     # #D4911E
RED_ALERT = (217, 48, 37)       # #D93025 (Segurança / Falha)
GREEN_SUCCESS = (30, 130, 76)   # #1E824C (Verde Sucesso / Go)
BLUE_ACCENT = (26, 115, 232)    # #1A73E8

TEXT_DARK = (13, 34, 54)
TEXT_BODY = (40, 55, 70)
TEXT_MUTED = (95, 110, 125)
TEXT_LIGHT = (255, 255, 255)
TEXT_LIGHT_MUTED = (195, 212, 230)

FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"

OUTPUT_PDF = "C:/Users/Augusto/Desktop/AH3/BigBrain/guias/Guia_Definitivo_Agent_Skills.pdf"
SCRATCH_DIR = "C:/Users/Augusto/Desktop/AH3/cartoes_hoteis_10x10"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_shadow_card(draw_base, img_base, bbox, radius=20, bg_color=CARD_WHITE, border_color=BORDER_SUBTLE, shadow_alpha=35, shadow_blur=22, shadow_offset=(0, 10)):
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    pad = shadow_blur * 2
    
    s_img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    
    ox, oy = shadow_offset
    sx1 = pad + ox
    sy1 = pad + oy
    sx2 = sx1 + w
    sy2 = sy1 + h
    
    s_draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=radius, fill=(0, 20, 40, shadow_alpha))
    s_img = s_img.filter(ImageFilter.GaussianBlur(shadow_blur))
    img_base.paste(s_img, (x1 - pad, y1 - pad), s_img)
    draw_base.rounded_rectangle(bbox, radius=radius, fill=bg_color, outline=border_color, width=1)

def draw_header(draw, kicker, title, subtitle=None, is_dark=False, kicker_color=None):
    k_color = kicker_color if kicker_color else (GOLD if is_dark else NAVY_ACCENT)
    t_color = TEXT_LIGHT if is_dark else TEXT_DARK
    s_color = TEXT_LIGHT_MUTED if is_dark else TEXT_MUTED

    y = 70
    draw.text((100, y), kicker.upper(), font=get_font(FONT_SANS_BOLD, 18), fill=k_color)
    y += 38
    
    t_lines = title.split("\n")
    for tl in t_lines:
        draw.text((100, y), tl, font=get_font(FONT_SERIF_BOLD, 44), fill=t_color)
        y += 54
        
    y += 18
    if subtitle:
        lines = subtitle.split("\n")
        for line in lines:
            draw.text((100, y), line, font=get_font(FONT_SANS, 20), fill=s_color)
            y += 30

def draw_footer(draw, page_num, total_pages=6, is_dark=False):
    f_color = (130, 165, 195) if is_dark else TEXT_MUTED
    line_col = (25, 65, 100) if is_dark else BORDER_SUBTLE
    
    draw.line([(100, H - 70), (W - 100, H - 70)], fill=line_col, width=1)
    draw.text((100, H - 54), "Guia Definitivo de Engenharia e Orquestração com Agent Skills · AH3 BigBrain", font=get_font(FONT_SANS, 16), fill=f_color)
    draw.text((W - 140, H - 54), f"Lâmina {page_num}/{total_pages}", font=get_font(FONT_SANS_BOLD, 16), fill=f_color)

# ==============================================================================
# LÂMINA 1: CAPA
# ==============================================================================
def build_slide_1():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 800, -300), (W + 500, 1000)], fill=BG_DARK_MID)

    draw.text((120, H//2 - 220), "MANUAL CANÔNICO DE ENGENHARIA DE AGENTES", font=get_font(FONT_SANS_BOLD, 20), fill=GOLD)
    draw.text((120, H//2 - 160), "Guia Definitivo de", font=get_font(FONT_SERIF_BOLD, 68), fill=TEXT_LIGHT)
    draw.text((120, H//2 - 75), "Agent Skills &", font=get_font(FONT_SERIF_BOLD, 68), fill=GOLD)
    draw.text((120, H//2 + 10), "Orquestração Autônoma", font=get_font(FONT_SERIF_BOLD, 68), fill=TEXT_LIGHT)

    draw.text((120, H//2 + 125), "A síntese definitiva integrando o framework de 3 camadas,", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)
    draw.text((120, H//2 + 160), "fan-out concorrente no /ship, padrão Prove-It e matriz de restrições.", font=get_font(FONT_SANS, 24), fill=TEXT_LIGHT_MUTED)

    draw.text((120, H - 120), "Base de Conhecimento: addyosmani/agent-skills · Claude Code · Hermes Agent · Antigravity", font=get_font(FONT_SANS_BOLD, 18), fill=GOLD)
    draw.text((120, H - 85), "Arquitetura & Engenharia: Augusto Henrique (AH3 BigBrain)", font=get_font(FONT_SANS, 17), fill=TEXT_LIGHT_MUTED)

    # Card direito demonstrativo
    c_box = [W - 700, 240, W - 120, 840]
    draw_shadow_card(draw, img, c_box, radius=24, bg_color=CARD_WARM, border_color=BORDER_WARM, shadow_alpha=90)
    
    draw.text((c_box[0] + 40, c_box[1] + 45), "ARQUITETURA EM 3 CAMADAS", font=get_font(FONT_SANS_BOLD, 16), fill=NAVY_ACCENT)
    
    blocos = [
        ("1. Commands / User", "O QUANDO — Gatilhos de ciclo de vida e orquestração (/spec, /plan, /ship).", NAVY),
        ("2. Personas Especializadas", "O QUEM — Especialistas independentes de perspectiva única (reviewer, security, QA).", GOLD_MUTED),
        ("3. Skills Determinísticas", "O COMO — Protocolos práticos com regras inegociáveis e saída formal.", BLUE_ACCENT),
        ("Regra de Ouro", "Personas NUNCA chamam outras personas. O usuário/command faz a orquestração.", RED_ALERT)
    ]
    
    by = c_box[1] + 110
    for tit, dsc, cor in blocos:
        draw.rounded_rectangle([c_box[0] + 40, by, c_box[0] + 48, by + 85], radius=4, fill=cor)
        draw.text((c_box[0] + 65, by + 5), tit, font=get_font(FONT_SERIF_BOLD, 22), fill=TEXT_DARK)
        lines = dsc.split("\n")
        dy = by + 35
        for l in lines:
            draw.text((c_box[0] + 65, dy), l, font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
            dy += 22
        by += 115

    return img

# ==============================================================================
# LÂMINA 2: V1 - NÚCLEO PRAGMÁTICO (4 GATES)
# ==============================================================================
def build_slide_2():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "FASE 1: FLUXO OPERACIONAL PADRÃO (V1)", "Os 4 Gates Inegociáveis do Ciclo de Vida",
                "Nenhum código é escrito sem especificação prévia. O agente avança estritamente através de gates formais.")
    draw_footer(draw, 2)

    card_w = (W - 200 - 90) // 4
    card_h = 580
    card_y = 260
    cx = 100

    fases = [
        ("1. SPEC", "Definição de Contratos",
         "Skill: spec-driven-development\n+ api-and-interface-design\n\n• Formalizar .spec.md\n• Definir inputs, outputs e payloads\n• Mapear casos de erro de borda\n\nNenhuma linha de código é criada antes da aprovação do spec.",
         NAVY),
        ("2. PLAN", "Fatiamento Atômico",
         "Skill: planning-and-task-breakdown\n+ constraint-driven-dev\n\n• Decompor em passos curtos\n• Escopo limitado a 1 arquivo/etapa\n• Definir ordem de dependência\n\nEvita regressões e perda de contexto durante a implementação.",
         GOLD_MUTED),
        ("3. BUILD", "Implementação com TDD",
         "Skill: incremental-implementation\n+ test-driven-development\n\n• Codificação incremental\n• Testes a cada novo bloco\n• Validação com terminal real\n\nCompilação verde e linter limpo são obrigatórios a cada etapa.",
         GOLD),
        ("4. VERIFY", "Revisão & Qualidade",
         "Skill: code-review-and-quality\n+ code-simplification\n\n• Análise em 5 eixos de qualidade\n• Remoção de código redundante\n• Verificação de regressões\n\nCódigo só avança para merge após validação de todos os critérios.",
         NAVY_ACCENT)
    ]

    for idx, (f_num, f_sub, f_desc, f_cor) in enumerate(fases):
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=18, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 12], radius=6, fill=f_cor)
        draw.text((cx + 30, card_y + 45), f_num, font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_DARK)
        draw.text((cx + 30, card_y + 90), f_sub, font=get_font(FONT_SANS_BOLD, 17), fill=f_cor)

        lines = f_desc.split("\n")
        ly = card_y + 150
        for l in lines:
            if l.startswith("Skill:"):
                draw.text((cx + 30, ly), l, font=get_font(FONT_SANS_BOLD, 16), fill=NAVY)
            elif l.startswith("•"):
                draw.text((cx + 30, ly), l, font=get_font(FONT_SANS, 16), fill=TEXT_BODY)
            else:
                draw.text((cx + 30, ly), l, font=get_font(FONT_SANS, 15), fill=TEXT_MUTED)
            ly += 26

        cx += card_w + 30

    return img

# ==============================================================================
# LÂMINA 3: V2 - ORQUESTRAÇÃO PARALELA NO /SHIP
# ==============================================================================
def build_slide_3():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "FASE 2: PREPARAÇÃO DE RELEASE (V2)", "Comando /ship: Multi-Agent Fan-Out Concorrente",
                "Divisão paralela para 3 especialistas com contexto isolado, culminando em uma decisão binária de Go / No-Go.")
    draw_footer(draw, 3)

    card_w = (W - 200 - 60) // 3
    card_h = 360
    card_y = 260
    gap = 30

    personas = [
        ("code-reviewer", "Senior Staff Engineer",
         "• Análise de complexidade ciclomática\n• Identificação de código duplicado\n• Manutenibilidade e contratos de API\n• Conformidade com design patterns",
         NAVY_ACCENT),
        ("security-auditor", "Security Engineer",
         "• Varredura de OWASP Top 10 e CWEs\n• Prevenção contra injeção e XSS\n• Auditoria de credenciais e segredos\n• Sanitização estrita de entradas",
         RED_ALERT),
        ("test-engineer", "QA Engineer",
         "• Aplicação do padrão Prove-It\n• Cobertura de caminhos críticos\n• Validação de casos de borda reais\n• Verificação de regressões ocultas",
         GREEN_SUCCESS)
    ]

    for i, (p_nome, p_cargo, p_itens, p_cor) in enumerate(personas):
        cx = 100 + i * (card_w + gap)
        bbox = [cx, card_y, cx + card_w, card_y + card_h]
        draw_shadow_card(draw, img, bbox, radius=18, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx + 30, card_y + 35, cx + 42, card_y + 85], radius=4, fill=p_cor)
        draw.text((cx + 55, card_y + 35), p_nome, font=get_font(FONT_SERIF_BOLD, 28), fill=TEXT_DARK)
        draw.text((cx + 55, card_y + 70), p_cargo, font=get_font(FONT_SANS_BOLD, 16), fill=p_cor)

        lines = p_itens.split("\n")
        ly = card_y + 130
        for l in lines:
            draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 18), fill=TEXT_BODY)
            ly += 34

    # Bloco inferior: Merge Phase
    m_box = [100, 660, W - 100, 870]
    draw_shadow_card(draw, img, m_box, radius=20, bg_color=CARD_WARM, border_color=BORDER_WARM)
    
    draw.text((140, 690), "FASE DE SÍNTESE (MERGE PHASE) & CRITÉRIOS DE VETO", font=get_font(FONT_SANS_BOLD, 18), fill=NAVY)
    
    vetos = [
        ("VETO AUTOMÁTICO (NO-GO):", "Qualquer falha de segurança 'High/Critical', teste quebrado ou objeção arquitetural bloqueia o PR imediatamente.", RED_ALERT),
        ("APROVAÇÃO (GO):", "3 pareceres favoráveis emitidos de forma independente + plano de rollback documentado para a release.", GREEN_SUCCESS)
    ]
    
    vy = 740
    for v_tit, v_desc, v_cor in vetos:
        draw.text((140, vy), v_tit, font=get_font(FONT_SANS_BOLD, 16), fill=v_cor)
        draw.text((430, vy), v_desc, font=get_font(FONT_SANS, 17), fill=TEXT_BODY)
        vy += 45

    return img

# ==============================================================================
# LÂMINA 4: V3 & V4 - PROVE-IT & CONSTRAINT MATRIX
# ==============================================================================
def build_slide_4():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "FASE 3 & 4: ROBUSTEZ EXTREMA (V3 & V4)", "Padrão 'Prove-It' para Bugs e Matriz de Restrições",
                "Verificação empírica obrigatória para código crítico e travas rígidas de performance e segurança.")
    draw_footer(draw, 4)

    # Lado Esquerdo: Padrão Prove-It (V3)
    b_left = [100, 260, 940, 870]
    draw_shadow_card(draw, img, b_left, radius=20, bg_color=CARD_WHITE)

    draw.rounded_rectangle([100, 260, 940, 272], radius=6, fill=RED_ALERT)
    draw.text((140, 295), "PADRÃO 'PROVE-IT' (BUGS & CRITICAL)", font=get_font(FONT_SANS_BOLD, 16), fill=RED_ALERT)
    draw.text((140, 330), "Ciclo RED-GREEN-REFACTOR", font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_DARK)

    etapas_prove = [
        ("1. PROVA DE FALHA (RED):", "Escrever teste unitário reproduzindo o bug. O teste DEVE FALHAR no terminal antes de qualquer patch.", RED_ALERT),
        ("2. CORREÇÃO MÍNIMA (GREEN):", "Alterar estritamente as linhas necessárias para fazer o teste passar (exit code 0).", GREEN_SUCCESS),
        ("3. SIMPLIFICAÇÃO (REFACTOR):", "Executar 'code-simplification' para eliminar código redundante sem introduzir regressões.", NAVY_ACCENT)
    ]

    py = 410
    for tit, dsc, cor in etapas_prove:
        draw.text((140, py), tit, font=get_font(FONT_SANS_BOLD, 17), fill=cor)
        lines = dsc.split("\n")
        dy = py + 26
        for l in lines:
            draw.text((140, dy), l, font=get_font(FONT_SANS, 16), fill=TEXT_BODY)
            dy += 22
        py += 105

    draw.rounded_rectangle([140, 750, 900, 830], radius=12, fill=BG_LIGHT_TINT)
    draw.text((160, 775), "Regra: Zero consertos 'no escuro'. Prova empírica via terminal.", font=get_font(FONT_SANS_BOLD, 16), fill=NAVY)

    # Lado Direito: Matriz de Restrições (V4)
    b_right = [980, 260, W - 100, 870]
    draw_shadow_card(draw, img, b_right, radius=20, bg_color=CARD_WHITE)

    draw.rounded_rectangle([980, 260, W - 100, 272], radius=6, fill=NAVY_ACCENT)
    draw.text((1020, 295), "MATRIZ DE RESTRIÇÕES (V4)", font=get_font(FONT_SANS_BOLD, 16), fill=NAVY_ACCENT)
    draw.text((1020, 330), "Floor-Guard & Não-Funcionais", font=get_font(FONT_SERIF_BOLD, 32), fill=TEXT_DARK)

    constraints = [
        ("Performance Web:", "INP < 200ms · LCP < 2.5s · CLS < 0.1\nAuditado via 'web-performance-auditor' e DevTools.", GOLD_MUTED),
        ("Bundle & Payload:", "Limite máximo de acréscimo de +15KB gzip.\nTree-shaking e code-splitting obrigatórios.", BLUE_ACCENT),
        ("Segurança de Dependências:", "Zero vulnerabilidades conhecidas (npm audit 0).\nAuditoria contínua com 'security-and-hardening'.", RED_ALERT),
        ("Backend & Latência:", "TTFB < 150ms · Zero Memory Leaks em loop.\nMonitoramento via 'observability-and-instrumentation'.", GREEN_SUCCESS)
    ]

    cy = 410
    for tit, dsc, cor in constraints:
        draw.text((1020, cy), tit, font=get_font(FONT_SANS_BOLD, 17), fill=cor)
        lines = dsc.split("\n")
        dy = cy + 26
        for l in lines:
            draw.text((1020, dy), l, font=get_font(FONT_SANS, 16), fill=TEXT_BODY)
            dy += 22
        cy += 95

    return img

# ==============================================================================
# LÂMINA 5: V5 - INTENT ENGINE & CATÁLOGO
# ==============================================================================
def build_slide_5():
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    draw_header(draw, "FASE 5: MANUAL DE INTEGRAÇÃO (V5)", "Intent Engine: Mapeamento Automático de Habilidades",
                "O agente identifica o gatilho da mensagem do usuário e seleciona a rota metodológica ótima.")
    draw_footer(draw, 5)

    card_w = (W - 200 - 40) // 2
    card_h = 260
    start_y = 260

    rotas = [
        ("Criar Nova Funcionalidade", "Skill Primária: spec-driven-development\nSuporte: planning-and-task-breakdown, api-interface-design\n\nOutput Obrigatório: SPEC.md aprovado e checklist atômico de tarefas antes de codificar.", NAVY),
        ("Corrigir Bug ou Falha", "Skill Primária: debugging-and-error-recovery\nSuporte: test-driven-development (Padrão Prove-It)\n\nOutput Obrigatório: Teste reproduzindo o erro no terminal antes da correção mínima.", RED_ALERT),
        ("Refatorar ou Limpar Código", "Skill Primária: code-simplification\nSuporte: test-driven-development, codebase-inspection\n\nOutput Obrigatório: Redução de linhas e complexidade com 100% de aprovação na suite de testes.", GOLD_MUTED),
        ("Auditar Performance ou UI", "Skill Primária: performance-optimization\nSuporte: browser-testing-with-devtools, frontend-ui-engineering\n\nOutput Obrigatório: Relatório com Core Web Vitals (INP, LCP, CLS) e visual traces de render.", BLUE_ACCENT)
    ]

    for idx, (tit, desc, cor) in enumerate(rotas):
        row = idx // 2
        col = idx % 2
        cx = 100 + col * (card_w + 40)
        cy = start_y + row * (card_h + 30)

        bbox = [cx, cy, cx + card_w, cy + card_h]
        draw_shadow_card(draw, img, bbox, radius=18, bg_color=CARD_WHITE)

        draw.rounded_rectangle([cx, cy + 25, cx + 8, cy + card_h - 25], radius=4, fill=cor)
        draw.text((cx + 35, cy + 30), tit, font=get_font(FONT_SERIF_BOLD, 26), fill=TEXT_DARK)

        lines = desc.split("\n")
        ly = cy + 75
        for l in lines:
            if "Skill Primária:" in l or "Output Obrigatório:" in l:
                draw.text((cx + 35, ly), l, font=get_font(FONT_SANS_BOLD, 16), fill=NAVY)
            else:
                draw.text((cx + 35, ly), l, font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
            ly += 24

    draw.rounded_rectangle([100, 810, W - 100, 870], radius=14, fill=BG_DARK)
    draw.text((140, 832), "Princípio Operacional: Se uma skill especializada existe para a tarefa, ela DEVE ser invocada.", font=get_font(FONT_SANS_BOLD, 18), fill=GOLD)

    return img

# ==============================================================================
# LÂMINA 6: PROTOCOLO DE CONFORMIDADE & CONCLUSÃO
# ==============================================================================
def build_slide_6():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw.ellipse([(W - 750, -250), (W + 550, 1050)], fill=BG_DARK_MID)

    draw_header(draw, "CONCLUSÃO & AUDITORIA", "Checklist de Conformidade Pré-Merge",
                "Critérios absolutos para entrega de software com garantia de qualidade e estabilidade operacional.", is_dark=True)
    draw_footer(draw, 6, is_dark=True)

    b_main = [100, 260, W - 100, 850]
    draw_shadow_card(draw, img, b_main, radius=24, bg_color=CARD_WARM, border_color=BORDER_WARM, shadow_alpha=120)

    draw.text((150, 310), "CHECKLIST DE SAÍDA DO ENGENHEIRO SÊNIOR", font=get_font(FONT_SERIF_BOLD, 32), fill=NAVY)

    itens = [
        ("1. Contrato & Especificação Formal", "A funcionalidade foi especificada em .spec.md antes da criação do código?"),
        ("2. Prova de Falha Anterior (Prove-It)", "O teste unitário reproduziu a falha no terminal real antes da correção?"),
        ("3. Cobertura & Suíte Verde", "Todos os testes unitários e de integração passaram com exit code 0?"),
        ("4. Fan-Out Aprovado no /ship", "As 3 personas especializadas (Reviewer, Security, QA) emitiram parecer favorável?"),
        ("5. Matriz de Restrições Atendida", "Os limites de Core Web Vitals, memória, latência e bundle size foram mantidos?"),
        ("6. Código Enxuto & Convencional", "A skill code-simplification foi executada e os commits seguem Conventional Commits?")
    ]

    iy = 380
    for tit, dsc in itens:
        draw.ellipse([150, iy + 4, 172, iy + 26], fill=GREEN_SUCCESS)
        draw.text((156, iy + 4), "✓", font=get_font(FONT_SANS_BOLD, 15), fill=TEXT_LIGHT)
        draw.text((190, iy), tit, font=get_font(FONT_SANS_BOLD, 20), fill=NAVY)
        draw.text((190, iy + 28), dsc, font=get_font(FONT_SANS, 16), fill=TEXT_MUTED)
        iy += 72

    return img

# ==============================================================================
# COMPILADOR DO PDF FINAL
# ==============================================================================
def gerar_guia_definitivo_pdf():
    print("Iniciando compilação do Guia Definitivo de Agent Skills em PDF...")
    
    slides = [
        (1, build_slide_1),
        (2, build_slide_2),
        (3, build_slide_3),
        (4, build_slide_4),
        (5, build_slide_5),
        (6, build_slide_6)
    ]

    pdf = pymupdf.open()
    
    for num, builder_fn in slides:
        print(f"-> Renderizando Lâmina {num}...")
        img = builder_fn()
        png_path = os.path.join(SCRATCH_DIR, f"guia_skills_slide_{num}.png")
        img.save(png_path, quality=95)
        
        img_doc = pymupdf.open(png_path)
        pdfbytes = img_doc.convert_to_pdf()
        pdf_img = pymupdf.open("pdf", pdfbytes)
        pdf.insert_pdf(pdf_img)
        img_doc.close()
        pdf_img.close()

    pdf.save(OUTPUT_PDF)
    pdf.close()
    print(f"=== SUCESSO: Guia Definitivo gerado em {OUTPUT_PDF} ===")

if __name__ == "__main__":
    gerar_guia_definitivo_pdf()

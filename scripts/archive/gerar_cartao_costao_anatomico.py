from PIL import Image
import base64, io, os

webp_path = r'C:\Users\Augusto\Downloads\b04782b1-4797-4dc1-9ea2-6066d87397b7.webp'
img = Image.open(webp_path)
buf = io.BytesIO()
img.save(buf, format='PNG')
b64_logo = base64.b64encode(buf.getvalue()).decode('ascii')

# Construção exata seguindo as especificações do Guia Bewiki (PDF):
# - Formato: 100x100mm (1000x1000px na escala vetorial)
# - Cantos: Raio 6mm (60px)
# - Margem de segurança: 9mm (90px)
# - Divisão: Curva suave escuro/claro
# - Topo: Logo oficial à esquerda + NFC à direita (pílula âmbar #F09C24 + ondas + "Aproxime o celular")
# - Base clara: Chamada "UM TOQUE LIBERA" + Grade 2x2 com ícones circulares 8mm com 12% da cor da marca
# - Rodapé: Filete com frase de efeito à esquerda e domínio à direita

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <clipPath id="cardClip">
      <rect width="1000" height="1000" rx="60" ry="60"/>
    </clipPath>
    <linearGradient id="darkBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141815"/>
      <stop offset="100%" stop-color="#080B09"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#cardClip)">
    <!-- Base Clara Inferior -->
    <rect width="1000" height="1000" fill="#F8F9FA"/>

    <!-- Divisão Superior Escura com Curva Suave -->
    <path d="M0,0 L1000,0 L1000,430 Q500,485 0,430 Z" fill="url(#darkBg)"/>

    <!-- A) LOGO OFICIAL (Topo Esquerdo / Centralizado na área escura) -->
    <g transform="translate(90, 110)">
      <image href="data:image/png;base64,{b64_logo}" x="0" y="0" width="460" height="160" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- B) SÍMBOLO NFC COM ETIQUETA PÍLULA ÂMBAR (Topo Direito) -->
    <g transform="translate(820, 160)">
      <!-- Pílula NFC Âmbar (#F09C24) -->
      <rect x="-45" y="-60" width="90" height="34" rx="17" fill="#F09C24"/>
      <text x="0" y="-38" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#080B09" text-anchor="middle" letter-spacing="1.5">NFC</text>

      <!-- Símbolo de Ondas NFC -->
      <g stroke="#F09C24" stroke-width="6" stroke-linecap="round" fill="none" transform="translate(0, 12)">
        <circle cx="-25" cy="0" r="3.5" fill="#F09C24" stroke="none"/>
        <path d="M-12,-18 C-3,-9 -3,9 -12,18"/>
        <path d="M3,-30 C18,-15 18,15 3,30"/>
        <path d="M18,-42 C38,-21 38,21 18,42"/>
      </g>
      
      <!-- Chamada de Ação -->
      <text x="0" y="85" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="600" fill="#E5E7EB" text-anchor="middle" letter-spacing="0.5">Aproxime o celular</text>
    </g>

    <!-- C) CHAMADA: UM TOQUE LIBERA -->
    <g transform="translate(90, 520)">
      <text x="0" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#6B7280" letter-spacing="3" text-transform="uppercase">UM TOQUE LIBERA</text>
    </g>

    <!-- D) ITENS EM GRADE 2x2 (Os 4 Pilares Reais do Costão do Santinho) -->
    
    <!-- Item 1: Spa & Terapias -->
    <g transform="translate(90, 565)">
      <circle cx="40" cy="40" r="40" fill="#0E2B24" fill-opacity="0.10"/>
      <g stroke="#0E2B24" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M16 26 C16 12 6 8 2 18 C2 24 10 26 16 26 Z"/>
        <path d="M16 26 C16 12 26 8 30 18 C30 24 22 26 16 26 Z"/>
        <path d="M16 26 C11 16 13 6 16 3 C19 6 21 16 16 26 Z"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Costão SPA &amp; Relax</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Massagens, hidro e rituais</text>
    </g>

    <!-- Item 2: Eventos & Shows Diários -->
    <g transform="translate(520, 565)">
      <circle cx="40" cy="40" r="40" fill="#0E2B24" fill-opacity="0.10"/>
      <g stroke="#0E2B24" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <rect x="3" y="6" width="26" height="23" rx="4"/>
        <line x1="3" y1="13" x2="29" y2="13"/>
        <line x1="9" y1="2" x2="9" y2="7"/>
        <line x1="23" y1="2" x2="23" y2="7"/>
        <circle cx="10" cy="19" r="1.5" fill="#0E2B24"/>
        <circle cx="16" cy="19" r="1.5" fill="#0E2B24"/>
        <circle cx="22" cy="19" r="1.5" fill="#0E2B24"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Shows &amp; Programação</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Agenda diária e atrações</text>
    </g>

    <!-- Item 3: Gastronomia All-Inclusive -->
    <g transform="translate(90, 715)">
      <circle cx="40" cy="40" r="40" fill="#0E2B24" fill-opacity="0.10"/>
      <g stroke="#0E2B24" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <path d="M5 3 L5 12 C5 15 8 17 11 17 L11 29"/>
        <line x1="11" y1="3" x2="11" y2="12"/>
        <path d="M17 3 L17 12 C17 15 14 17 11 17"/>
        <path d="M23 3 C27 8 27 15 24 18 L24 29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Restaurantes &amp; Bares</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Cardápios, reservas e horários</text>
    </g>

    <!-- Item 4: Mapa & Experiência Resort -->
    <g transform="translate(520, 715)">
      <circle cx="40" cy="40" r="40" fill="#0E2B24" fill-opacity="0.10"/>
      <g stroke="#0E2B24" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(24, 24)">
        <polygon points="3 7 11 3 21 7 29 3 29 25 21 29 11 25 3 29"/>
        <line x1="11" y1="3" x2="11" y2="25"/>
        <line x1="21" y1="7" x2="21" y2="29"/>
      </g>
      <text x="100" y="36" font-family="'Plus Jakarta Sans', sans-serif" font-size="22" font-weight="700" fill="#111827">Mapa &amp; Guia Resort</text>
      <text x="100" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="15" font-weight="500" fill="#4B5563">Wi-Fi, trilhas e arqueologia</text>
    </g>

    <!-- E) RODAPÉ ANATÔMICO COM FILETE -->
    <g transform="translate(90, 890)">
      <line x1="0" y1="0" x2="820" y2="0" stroke="#E5E7EB" stroke-width="1.5"/>
      <text x="0" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="600" fill="#6B7280">Experiência All-Inclusive na Praia do Santinho.</text>
      <text x="820" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="700" fill="#111827" text-anchor="end">costao.com.br</text>
    </g>
  </g>
</svg>'''

svg_path = r'C:\Users\Augusto\Desktop\AH3\cartoes_hoteis_10x10\01_costao_do_santinho_card_10x10.svg'
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(svg)

print('SVG regerado com sucesso.')

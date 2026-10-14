import os

WEB_DIR = r"C:\Users\Augusto\Desktop\AH3\BigBrain\portfolioreferencias\paginas_web"
os.makedirs(WEB_DIR, exist_ok=True)

# 1. Trattoria Italiana (Clean / Warm Typography)
web_01 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nonna Mia Trattoria · Florianópolis</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: #FAF8F5; color: #2D2421; }
nav { display: flex; justify-content: space-between; align-items: center; padding: 24px 48px; border-bottom: 1px solid #EBE4DD; background: #FFFFFF; }
.logo { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 700; color: #7A2E1E; }
.btn-reserva { background: #7A2E1E; color: #FFF; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 14px; }
.hero { text-align: center; padding: 80px 24px 60px; max-width: 800px; margin: 0 auto; }
.hero-tag { font-size: 12px; text-transform: uppercase; letter-spacing: 0.2em; color: #C06B3E; font-weight: 700; margin-bottom: 12px; }
.hero h1 { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 700; color: #1E1614; line-height: 1.15; margin-bottom: 20px; }
.hero p { font-size: 18px; color: #6E5F5A; line-height: 1.6; margin-bottom: 32px; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; max-width: 1100px; margin: 0 auto 80px; padding: 0 24px; }
.dish-card { background: #FFFFFF; border: 1px solid #EBE4DD; border-radius: 12px; padding: 24px; }
.dish-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.dish-name { font-family: 'Playfair Display', serif; font-size: 18px; font-weight: 700; color: #1E1614; }
.dish-price { font-weight: 700; color: #7A2E1E; }
.dish-desc { font-size: 14px; color: #6E5F5A; line-height: 1.5; }
</style>
</head>
<body>
<nav>
    <div class="logo">Nonna Mia · Trattoria</div>
    <a href="#reservar" class="btn-reserva">Reservar Mesa</a>
</nav>
<div class="hero">
    <div class="hero-tag">Massas Frescas & Forno a Lenha</div>
    <h1>A verdadeira tradição italiana na Beira-Mar.</h1>
    <p>Massas artesanais produzidas diariamente com ingredientes importados e carta de vinhos selecionada.</p>
</div>
<div class="menu-grid">
    <div class="dish-card">
        <div class="dish-head">
            <div class="dish-name">Tagliolini al Tartufo</div>
            <div class="dish-price">R$ 88</div>
        </div>
        <div class="dish-desc">Massa fresca artesanal com emulsão de manteiga de trufas negras e queijo Parmigiano Reggiano 24 meses.</div>
    </div>
    <div class="dish-card">
        <div class="dish-head">
            <div class="dish-name">Ossobuco Tradizionale</div>
            <div class="dish-price">R$ 112</div>
        </div>
        <div class="dish-desc">Cozimento lento por 8 horas ao molho de vinho tinto, acompanhado de polenta cremosa bramata.</div>
    </div>
    <div class="dish-card">
        <div class="dish-head">
            <div class="dish-name">Tiramisù della Nonna</div>
            <div class="dish-price">R$ 38</div>
        </div>
        <div class="dish-desc">Biscoitos savoiardi embebidos em café espresso, creme de mascarpone e cacau amargo 100%.</div>
    </div>
</div>
</body>
</html>
"""

# 2. Modern Burger & Beer (Dark / Streetwear)
web_02 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IRON BURGER LAB · Craft & Fire</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0A0D14; color: #F3F4F6; }
header { padding: 32px 24px; text-align: center; border-bottom: 1px solid #1F2937; }
.badge { font-family: 'JetBrains Mono'; font-size: 11px; background: #F97316; color: #000; padding: 4px 12px; border-radius: 4px; font-weight: 700; display: inline-block; }
h1 { font-size: 44px; font-weight: 900; letter-spacing: -0.04em; text-transform: uppercase; margin: 16px 0 8px; }
.sub { font-size: 15px; color: #9CA3AF; }
.grid { max-width: 900px; margin: 40px auto; padding: 0 24px; display: grid; gap: 16px; }
.card { background: #111827; border: 1px solid #1F2937; border-radius: 12px; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
.card h3 { font-size: 18px; font-weight: 800; color: #FFF; }
.card p { font-size: 13px; color: #9CA3AF; margin-top: 4px; }
.btn-pedir { background: #F97316; color: #000; padding: 10px 18px; border-radius: 6px; font-weight: 800; text-decoration: none; font-size: 12px; text-transform: uppercase; }
</style>
</head>
<body>
<header>
    <div class="badge">SMASH & CRAFT BEER</div>
    <h1>IRON BURGER LAB</h1>
    <div class="sub">Carne 100% Angus prensada na chapa de ferro ultra-quente.</div>
</header>
<div class="grid">
    <div class="card">
        <div>
            <h3>DOUBLE SMASH TRIPLE CHEESE</h3>
            <p>2x blend 90g Angus, queijo cheddar inglês derretido, cebola caramelizada e maionese defumada.</p>
        </div>
        <a href="#" class="btn-pedir">R$ 44 · Pedir</a>
    </div>
    <div class="card">
        <div>
            <h3>TRUFFLE & BACON CRISPY</h3>
            <p>Blend 160g, bacon artesanal crocante, fondue de queijo gouda e azeite trufado.</p>
        </div>
        <a href="#" class="btn-pedir">R$ 52 · Pedir</a>
    </div>
</div>
</body>
</html>
"""

# 3. Seafood & Oyster Bar (Coastal / Fresh)
web_03 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Maré Alta · Ostras & Frutos do Mar</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: #F0F7FA; color: #0E3446; }
header { background: #002B3D; color: #FFF; padding: 48px 24px; text-align: center; }
h1 { font-size: 38px; font-weight: 700; margin-bottom: 8px; }
p { font-size: 16px; color: #A4D2E6; }
.container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
.box { background: #FFF; border-radius: 12px; padding: 24px; margin-bottom: 16px; border: 1px solid #D1E5EE; box-shadow: 0 4px 12px rgba(0,43,61,0.04); }
.box-title { font-size: 18px; font-weight: 700; color: #002B3D; margin-bottom: 6px; }
.box-desc { font-size: 14px; color: #4A6E7E; }
</style>
</head>
<body>
<header>
    <h1>Maré Alta Oyster Bar</h1>
    <p>Ostras frescas de Ribeirão da Ilha servidas à beira-mar.</p>
</header>
<div class="container">
    <div class="box">
        <div class="box-title">Dúzia de Ostras Vivas ao Vinagrete de Caju</div>
        <div class="box-desc">Colhidas nas primeiras horas da manhã, servidas no gelo com limão cravo e pimenta da casa.</div>
    </div>
    <div class="box">
        <div class="box-title">Polvo Grelhado na Brasa com Batatas ao Murro</div>
        <div class="box-desc">Tentáculo crocante por fora e macio por dentro, azeite de ervas e alho confitado.</div>
    </div>
</div>
</body>
</html>
"""

# 4. Japanese Izakaya & Sushi (Minimalist / Tokyo Night)
web_04 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kuro Sushi & Izakaya · Omakase</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0D0D0D; color: #E5E5E5; }
.nav { display: flex; justify-content: space-between; padding: 24px 32px; border-bottom: 1px solid #222; }
.logo { font-size: 18px; font-weight: 700; letter-spacing: 0.15em; color: #FFF; }
.hero { text-align: center; padding: 80px 24px; }
h1 { font-size: 36px; font-weight: 300; letter-spacing: 0.08em; text-transform: uppercase; color: #FFF; margin-bottom: 16px; }
.omakase-box { max-width: 600px; margin: 0 auto; background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 32px; text-align: center; }
.btn-reserve { display: inline-block; background: #FFF; color: #000; padding: 12px 28px; border-radius: 4px; font-weight: 700; text-decoration: none; font-size: 13px; text-transform: uppercase; margin-top: 20px; }
</style>
</head>
<body>
<div class="nav">
    <div class="logo">KURO · 黒</div>
    <div style="font-size:12px; color:#888;">BALCÃO DE OMAKASE EXCLUSIVO</div>
</div>
<div class="hero">
    <h1>Experiência Omakase em 12 Etapas</h1>
    <div class="omakase-box">
        <p style="font-size:14px; color:#AAA; line-height:1.6;">Peixes frescos da costa de Santa Catarina selecionados diariamente pelo chef. Apenas 10 assentos por turno.</p>
        <a href="#" class="btn-reserve">Solicitar Reserva</a>
    </div>
</div>
</body>
</html>
"""

# 5. Specialty Coffee & Bakery (Nordic Clean)
web_05 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nordic Roast & Bakery</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; background: #F8F9FA; color: #212529; }
header { padding: 40px 24px; text-align: center; border-bottom: 1px solid #E9ECEF; background: #FFF; }
h1 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }
.tag { font-family: 'JetBrains Mono'; font-size: 11px; color: #0D6EFD; margin-bottom: 8px; display: inline-block; }
.cards { max-width: 800px; margin: 40px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card { background: #FFF; border: 1px solid #E9ECEF; border-radius: 8px; padding: 20px; }
.card-h { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.card-p { font-size: 13px; color: #6C757D; }
</style>
</head>
<body>
<header>
    <div class="tag">CAFÉS ESPECIAIS & FERMENTAÇÃO NATURAL</div>
    <h1>NORDIC COFFEE ROASTERS</h1>
</header>
<div class="cards">
    <div class="card">
        <div class="card-h">Espresso Single Origin (Cerrado Mineiro)</div>
        <div class="card-p">Notas de chocolate amargo, caramelo e finalização sedosa.</div>
    </div>
    <div class="card">
        <div class="card-h">Croissant Tradicional de Manteiga</div>
        <div class="card-p">Fermentação de 72 horas com manteiga francesa folhada.</div>
    </div>
</div>
</body>
</html>
"""

pages = [
    ("web_01_trattoria_italiana.html", web_01),
    ("web_02_iron_burger_lab.html", web_02),
    ("web_03_mare_alta_seafood.html", web_03),
    ("web_04_kuro_sushi_izakaya.html", web_04),
    ("web_05_nordic_coffee_bakery.html", web_05),
]

for fname, content in pages:
    fpath = os.path.join(WEB_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] Página web gerada: {fpath}")

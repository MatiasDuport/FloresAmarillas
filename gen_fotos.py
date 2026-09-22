"""Fotos v3: rosa macro, campo atardecer, cierre ramo atado + carta. Reusa blooms de gen_ramo."""
import pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random, math

random.seed(11)
HLP = {}
exec(compile(pathlib.Path("gen_ramo.py").read_text(encoding="utf-8").split(
    "# ---------- composición ----------")[0], "helpers", "exec"), HLP)
petal_r, petal_punta = HLP["petal_r"], HLP["petal_punta"]
hoja, eucalipto, nube = HLP["hoja"], HLP["eucalipto"], HLP["nubecilla"]
girasol, rosa, ranunculo, boton, anillo = (HLP["girasol"], HLP["rosa"], HLP["ranunculo"],
                                           HLP["boton"], HLP["anillo"])

def fondo_lino(w, h, c1=(250, 243, 228), c2=(230, 208, 172)):
    im = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)))
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x in range(0, w, 4):
        od.line([(x, 0), (x, h)], fill=(120, 95, 60, 10))
    for y in range(0, h, 4):
        od.line([(0, y), (w, y)], fill=(255, 252, 240, 12))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    return im

def bokeh(img, n, rmax=60, alpha=44):
    w, h = img.size
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    db = ImageDraw.Draw(cap)
    for _ in range(n):
        x, y = random.randint(0, w), random.randint(0, h)
        rr = random.randint(18, rmax)
        db.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 250, 235, alpha))
    img.alpha_composite(cap.filter(ImageFilter.GaussianBlur(16)))

def vineta(img, fuerza=120):
    w, h = img.size
    m = Image.new("L", (w, h), 90)
    ImageDraw.Draw(m).ellipse([w * 0.08, h * 0.06, w * 0.92, h * 0.94], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    osc = Image.new("RGBA", (w, h), (52, 34, 12, fuerza))
    return Image.alpha_composite(img, Image.composite(osc, Image.new("RGBA", (w, h), (0, 0, 0, 0)), m))

def grano(img, amt=10):
    w, h = img.size
    g = Image.effect_noise((w, h), 10).convert("L").point(lambda v: v * amt // 100)
    return Image.alpha_composite(img, Image.merge("RGBA", (g, g, g, g)))

def sombra(img, x, y, rx, ry, alpha=80, blur=18):
    w, h = img.size
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(cap).ellipse([x - rx, y - ry, x + rx, y + ry], fill=(74, 52, 33, alpha))
    img.alpha_composite(cap.filter(ImageFilter.GaussianBlur(blur)))

# ===== 1. ROSA MACRO 900x620 =====
w, h = 900, 620
img = fondo_lino(w, h)
bokeh(img, 14)
d = ImageDraw.Draw(img)
sombra(img, 450, 330, 260, 120)
for i, a in enumerate((-150, -110, -70, -30, 30, 70, 110, 150)):
    hoja(img, 450, 330, 250, 170, 60, a,
         fill=random.choice([(86, 116, 62), (74, 102, 56), (98, 128, 70)]))
rosa(img, 450, 300, 185)
boton(img, 220, 200, 26); boton(img, 690, 220, 24)
nube(img, 250, 420); nube(img, 670, 430)
d = ImageDraw.Draw(img)
for _ in range(14):  # rocío
    x, y = random.randint(300, 600), random.randint(160, 430)
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 200))
    d.ellipse([x - 5, y - 5, x - 1, y - 1], fill=(255, 255, 255, 255))
img = ImageEnhance.Color(vineta(img)).enhance(1.08)
grano(img).convert("RGB").save("img/rosa.jpg", quality=88)
print("rosa ok")

# ===== 2. CAMPO ATARDECER 900x560 =====
w, h = 900, 560
cielo = [(247, 217, 138), (238, 165, 80), (200, 110, 50)]
img = Image.new("RGB", (w, h))
d = ImageDraw.Draw(img)
for y in range(h):
    t = y / h
    c = cielo[0] if t < 0.45 else cielo[1] if t < 0.7 else cielo[2]
    d.line([(0, y), (w, y)], fill=c)
img = img.convert("RGBA")
d = ImageDraw.Draw(img)
respl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(respl).ellipse([w * 0.30 - 95, 185, w * 0.30 + 95, 375], fill=(255, 220, 150, 110))
img.alpha_composite(respl.filter(ImageFilter.GaussianBlur(24)))
d = ImageDraw.Draw(img)
d.ellipse([w * 0.30 - 62, 218, w * 0.30 + 62, 342], fill=(250, 183, 95, 255))  # sol
d.rectangle([0, 360, w, h], fill=(62, 70, 34, 255))  # tierra
d.rectangle([0, 360, w, 372], fill=(240, 180, 90, 255))  # filo luz horizonte
for i in range(7):  # hilera contraluz
    x = 70 + i * 130 + random.randint(-14, 14)
    top = 300 + random.randint(-24, 24)
    d.line([(x, 430), (x, top + 40)], fill=(40, 46, 22, 255), width=7)
    for a in range(0, 360, 30):
        petal_punta(img, x, top, 34, 62, 24, a + 8, (150, 100, 20, 255))
    d.ellipse([x - 26, top - 26, x + 26, top + 26], fill=(48, 32, 12, 255))
    d.arc([x - 26, top - 26, x + 26, top + 26], 200, 340, fill=(250, 200, 110, 255), width=3)
girasol(img, 150, 480, 66, giro=-10)
girasol(img, 760, 490, 72, giro=14)
ranunculo(img, 640, 520, 44)
img = ImageEnhance.Color(vineta(img, 100)).enhance(1.1)
grano(img).convert("RGB").save("img/campo.jpg", quality=88)
print("campo ok")

# ===== 3. CIERRE: ramo atado + carta lacrada 900x1200 =====
w, h = 900, 1200
img = fondo_lino(w, h, (251, 245, 232), (232, 211, 176))
bokeh(img, 12)
d = ImageDraw.Draw(img)
CX, CY = 400, 520
sombra(img, CX, CY + 260, 260, 90)
for dx, wd in ((-70, 8), (-25, 9), (20, 8), (65, 9)):
    d.line([(CX + dx * 0.6, CY + 120), (CX + dx * 0.9, 900)], fill=(101, 124, 66, 255), width=wd)
for i in range(12):
    a = -150 + i * 26 + random.randint(-6, 6)
    hoja(img, CX, CY + 60, 210, 150, 52, a,
         fill=random.choice([(86, 116, 62), (74, 102, 56)]))
d = ImageDraw.Draw(img)
d.line([(CX - 120, 640), (CX + 120, 640)], fill=(150, 110, 60, 255), width=7)  # cordel
anillo(img, CX - 62, 622, 52, 30, -22, (150, 110, 60, 255))
anillo(img, CX + 62, 622, 52, 30, 22, (150, 110, 60, 255))
d.ellipse([CX - 26, 616, CX + 26, 668], fill=(165, 118, 20, 255))
d.ellipse([CX - 16, 624, CX + 16, 660], fill=(205, 155, 48, 255))
girasol(img, CX - 130, CY - 60, 108, giro=-6)
rosa(img, CX + 90, CY - 20, 104)
ranunculo(img, CX + 10, CY - 150, 72)
boton(img, CX - 210, CY + 40, 22); nube(img, CX + 190, CY - 120)
# carta lacrada apoyada
carta = [540, 730, 860, 1030]
d.rounded_rectangle(carta, radius=10, fill=(253, 250, 240, 255), outline=(185, 138, 31, 255), width=3)
for i, y in enumerate((780, 812, 844, 876)):
    d.line([(570, y), (830 - i * 40, y)], fill=(210, 190, 155, 255), width=4)
d.ellipse([672, 898, 728, 954], fill=(165, 118, 20, 255))
d.ellipse([680, 906, 720, 946], fill=(205, 155, 48, 255))
img = ImageEnhance.Color(vineta(img)).enhance(1.07)
grano(img).convert("RGB").save("img/sobre.jpg", quality=88)
print("cierre ok")

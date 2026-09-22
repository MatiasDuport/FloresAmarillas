"""Ramo editorial v2 — girasoles, rosas, ranúnculos sobre lino. Solo Pillow."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random, math

random.seed(7)
W, H = 1080, 1440
CX, CY = 540, 560  # corazón del ramo

# ---------- base lino ----------
def linen():
    top, bot = (250, 243, 228), (228, 205, 168)
    im = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x in range(0, W, 4):  # trama vertical
        od.line([(x, 0), (x, H)], fill=(120, 95, 60, 10))
    for y in range(0, H, 4):  # trama horizontal
        od.line([(0, y), (W, y)], fill=(255, 252, 240, 12))
    for _ in range(2600):  # fibra
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        od.point((x, y), fill=(110, 85, 50, 22))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    # luz cálida cenital
    luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(luz)
    ld.ellipse([-320, -420, W + 320, 900], fill=(255, 250, 232, 70))
    im = Image.alpha_composite(im, luz)
    return im

# ---------- pétalos rotados ----------
def petal_r(base, cx, cy, dist, L, Wd, ang, fill, outline=None):
    L, Wd = max(4, int(L)), max(4, int(Wd))
    tmp = Image.new("RGBA", (L * 2, Wd * 2), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse([2, 2, L * 2 - 3, Wd * 2 - 3], fill=fill, outline=outline)
    tmp = tmp.rotate(-ang, expand=True, resample=Image.BICUBIC)
    r = math.radians(ang)
    px, py = cx + math.cos(r) * dist, cy + math.sin(r) * dist
    base.alpha_composite(tmp, (int(px - tmp.width / 2), int(py - tmp.height / 2)))

def petal_punta(base, cx, cy, dist, L, Wd, ang, fill, vein=None, contorno=None):
    L, Wd = max(6, int(L)), max(4, int(Wd))
    tmp = Image.new("RGBA", (L, Wd), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.polygon([(1, Wd / 2), (L * 0.52, 1), (L - 1, Wd / 2), (L * 0.52, Wd - 2)],
              fill=fill, outline=contorno)
    if vein:
        d.line([(L * 0.2, Wd / 2), (L - 3, Wd / 2)], fill=vein, width=2)
    tmp = tmp.rotate(-ang, expand=True, resample=Image.BICUBIC)
    r = math.radians(ang)
    px, py = cx + math.cos(r) * dist, cy + math.sin(r) * dist
    base.alpha_composite(tmp, (int(px - tmp.width / 2), int(py - tmp.height / 2)))

def hoja(base, cx, cy, dist, L, Wd, ang, fill=(86, 116, 62), vein=(58, 82, 44)):
    # Hoja curva orgánica: dos bordes cuadráticos, envés más oscuro, nervadura.
    L, Wd = int(L), int(Wd)
    tmp = Image.new("RGBA", (L, Wd), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    pts_sup, pts_inf, N = [], [], 14
    for i in range(N + 1):
        t = i / N
        x = 2 + t * (L - 4)
        curva = math.sin(t * math.pi)
        pts_sup.append((x, Wd / 2 - Wd * 0.46 * curva - Wd * 0.06 * math.sin(t * 2.2)))
        pts_inf.append((x, Wd / 2 + Wd * 0.34 * curva))
    d.polygon(pts_sup + pts_inf[::-1], fill=fill)
    d.polygon([(x, Wd / 2 + (y - Wd / 2) * 0.9) for x, y in pts_inf][::-1] + pts_inf,
              fill=tuple(max(0, c - 26) for c in fill))
    d.line([(3, Wd / 2), (L - 4, Wd / 2)], fill=vein, width=2)
    for i in range(2, 9, 2):  # nervaduras laterales
        x = L * i / 10
        d.line([(x, Wd / 2), (x + L * 0.12, Wd / 2 - Wd * 0.22)], fill=vein, width=1)
        d.line([(x, Wd / 2), (x + L * 0.12, Wd / 2 + Wd * 0.18)], fill=vein, width=1)
    tmp = tmp.rotate(-ang, expand=True, resample=Image.BICUBIC)
    r = math.radians(ang)
    base.alpha_composite(tmp, (int(cx + math.cos(r) * dist - tmp.width / 2),
                               int(cy + math.sin(r) * dist - tmp.height / 2)))

def anillo(base, cx, cy, L, Wd, ang, color, width=7):
    tmp = Image.new("RGBA", (int(L * 2), int(Wd * 2)), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse([width, width, int(L * 2) - width, int(Wd * 2) - width],
                                outline=color, width=width)
    tmp = tmp.rotate(-ang, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)))

def halo_fondo(img):
    cap = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cap)
    dc.ellipse([CX - 430, CY - 430, CX + 430, CY + 430], fill=(255, 252, 238, 60))
    dc.ellipse([CX - 300, CY - 300, CX + 300, CY + 300], fill=(255, 250, 230, 55))
    img.alpha_composite(cap.filter(ImageFilter.GaussianBlur(60)))
    bk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(bk)
    for _ in range(12):  # bokeh crema desenfocado
        x, y = random.randint(60, W - 60), random.randint(60, H - 60)
        rr = random.randint(26, 70)
        db.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 250, 235, 42))
    img.alpha_composite(bk.filter(ImageFilter.GaussianBlur(18)))

def eucalipto(base, x, y, largo, ang, verde=(122, 148, 118)):
    r = math.radians(ang)
    dx, dy = math.cos(r), math.sin(r)
    d = ImageDraw.Draw(base)
    d.line([(x, y), (x + dx * largo, y + dy * largo)], fill=(96, 120, 92, 255), width=5)
    for i in range(1, 7):
        px, py = x + dx * largo * i / 7, y + dy * largo * i / 7
        rr = 13 - i
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=verde + (255,))
        d.ellipse([px - rr, py - rr, px - rr + 8, py - rr + 8], fill=(200, 214, 198, 255))

def nubecilla(base, x, y):  # gypsophila
    d = ImageDraw.Draw(base)
    for _ in range(14):
        px, py = x + random.randint(-34, 34), y + random.randint(-30, 30)
        d.line([(x, y + 20), (px, py)], fill=(170, 150, 120, 255), width=1)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(253, 248, 232, 255))

# ---------- flores ----------
def girasol(base, cx, cy, R, giro=0):
    tonos = [(214, 142, 10), (242, 183, 5), (248, 200, 40)]
    for anillo, n, esc in ((0, 20, 1.0), (1, 20, 0.84)):
        for i in range(n):
            a = giro + anillo * 9 + i * (360 / n) + random.uniform(-2.5, 2.5)
            L = int(R * esc * random.uniform(0.9, 1.06))
            petal_punta(base, cx, cy, L * 0.52, L, int(R * 0.38), a,
                        tonos[(i + anillo) % 3], vein=(185, 120, 12), contorno=(170, 108, 8))
    d = ImageDraw.Draw(base)
    rc = int(R * 0.40)
    d.ellipse([cx - rc - 4, cy - rc - 4, cx + rc + 4, cy + rc + 4], fill=(196, 148, 52, 255))
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], fill=(70, 44, 12, 255))
    for gy in range(-rc + 6, rc - 4, 7):
        for gx in range(-rc + 6, rc - 4, 7):
            if gx * gx + gy * gy < (rc - 8) ** 2 and random.random() < 0.8:
                c = (42, 26, 8, 255) if random.random() < 0.7 else (150, 108, 40, 255)
                d.ellipse([cx + gx - 2, cy + gy - 2, cx + gx + 2, cy + gy + 2], fill=c)

def rosa(base, cx, cy, R):
    ext, med, luz, cor = (176, 122, 18), (233, 169, 31), (247, 207, 90), (138, 90, 12)
    d = ImageDraw.Draw(base)
    d.ellipse([cx - R - 8, cy - R + 4, cx + R + 8, cy + R + 12], fill=(110, 72, 10, 110))
    for k in range(5):  # pétalos exteriores abiertos, radiales, punta clara
        a = k * 72 + random.randint(-6, 6)
        petal_r(base, cx, cy, R * 0.78, R * 0.52, R * 0.40, a, med + (255,), ext + (255,))
        r = math.radians(a)
        bx, by = cx + math.cos(r) * R * 0.78, cy + math.sin(r) * R * 0.78
        d.arc([bx - R * 0.45, by - R * 0.45, bx + R * 0.45, by + R * 0.45],
              a - 50, a + 90, fill=(253, 233, 168, 255), width=max(2, R // 22))
    d.ellipse([cx - R * 0.72, cy - R * 0.72, cx + R * 0.72, cy + R * 0.72], fill=med + (255,))
    w = max(4, R // 8)
    for k in range(7):
        a = k * (360 / 7) + 24
        d.arc([cx - R * 0.72, cy - R * 0.72, cx + R * 0.72, cy + R * 0.72],
              a, a + 84, fill=luz + (255,), width=w)
    r3 = int(R * 0.38)
    d.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=luz + (255,))
    d.arc([cx - r3, cy - r3, cx + r3, cy + r3], 8, 205, fill=cor + (255,), width=max(3, r3 // 4))
    d.arc([cx - r3 // 2, cy - r3 // 2, cx + r3 // 2, cy + r3 // 2], 195, 375, fill=cor + (255,), width=max(2, r3 // 5))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=cor + (255,))
    d.arc([cx - R * 0.8, cy - R * 0.8, cx + R * 0.2, cy + R * 0.2], 90, 220, fill=(253, 233, 168, 255), width=4)

def ranunculo(base, cx, cy, R):
    capas = [((232, 160, 22), 12, R * 0.95, 0.62), ((246, 190, 52), 10, R * 0.70, 0.55), ((252, 220, 130), 8, R * 0.45, 0.5)]
    for col, n, dist, prop in capas:
        for i in range(n):
            a = i * (360 / n) + dist
            petal_r(base, cx, cy, dist * 0.55, int(dist * 0.62), int(dist * 0.62 * prop), a, col + (255,), (200, 130, 15, 255))
    d = ImageDraw.Draw(base)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(170, 105, 12, 255))

def boton(base, cx, cy, R):
    d = ImageDraw.Draw(base)
    d.line([(cx, cy), (cx - 12, cy + R * 2)], fill=(86, 110, 60, 255), width=4)
    for i, (dx, col) in enumerate(((-8, (240, 180, 40)), (8, (250, 205, 90)))):
        d.ellipse([cx + dx - R // 2, cy - R // 2 - i * 4, cx + dx + R // 2, cy + R // 2 - i * 4], fill=col + (255,))

# ---------- composición ----------
img = linen()
halo_fondo(img)
d = ImageDraw.Draw(img)

# sombra del ramo
sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sombra).ellipse([CX - 330, 880, CX + 330, 1080], fill=(74, 52, 33, 90))
img = Image.alpha_composite(img, sombra.filter(ImageFilter.GaussianBlur(30)))
d = ImageDraw.Draw(img)

# tallos
for dx, w in ((-90, 9), (-40, 11), (10, 9), (60, 10), (110, 8)):
    d.line([(CX + dx * 0.5, 700), (CX + dx * 0.35, 1250)], fill=(101, 124, 66, 255), width=w)

# papel envoltorio con pliegues, borde enrollado, moño y lacre
papel = [(CX - 350, 830), (CX + 350, 830), (CX + 210, 1380), (CX - 210, 1380)]
d.polygon(papel, fill=(253, 250, 240, 255))
pliegues = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dp = ImageDraw.Draw(pliegues)
for fx, fw, col in ((CX - 190, 56, (190, 160, 115, 60)), (CX - 30, 40, (255, 255, 252, 70)),
                    (CX + 130, 62, (190, 160, 115, 60)), (CX + 40, 26, (255, 255, 252, 55))):
    dp.polygon([(fx - fw, 830), (fx + fw, 830), (fx + fw * 0.6, 1380), (fx - fw * 0.6, 1380)], fill=col)
img.alpha_composite(pliegues.filter(ImageFilter.GaussianBlur(9)))
d = ImageDraw.Draw(img)
d.polygon(papel, outline=(185, 138, 31, 255))
d.rounded_rectangle([CX - 352, 812, CX + 352, 852], radius=20, fill=(244, 232, 203, 255),
                    outline=(185, 138, 31, 255), width=3)  # borde enrollado
d.line([(CX - 250, 1010), (CX + 250, 1010)], fill=(150, 110, 60, 255), width=6)
anillo(img, CX - 78, 992, 62, 34, -24, (150, 110, 60, 255))  # lazadas inclinadas
anillo(img, CX + 78, 992, 62, 34, 24, (150, 110, 60, 255))
d.line([(CX - 40, 1030), (CX - 90, 1110)], fill=(150, 110, 60, 255), width=7)
d.line([(CX + 40, 1030), (CX + 90, 1110)], fill=(150, 110, 60, 255), width=7)
d.ellipse([CX - 30, 982, CX + 30, 1042], fill=(165, 118, 20, 255))
d.ellipse([CX - 19, 990, CX + 19, 1034], fill=(205, 155, 48, 255))
d.ellipse([CX - 19, 990, CX - 6, 1003], fill=(235, 195, 110, 255))  # brillo lacre

# follaje posterior
for i in range(16):
    a = -160 + i * 20 + random.randint(-6, 6)
    hoja(img, CX, CY + 40, 300, 190, 62, a,
         fill=(random.choice([(86, 116, 62), (74, 102, 56), (98, 128, 70)])))
for x, y, a, l in ((250, 480, -50, 220), (830, 470, 50, 230), (200, 660, -80, 200), (880, 660, 80, 200)):
    eucalipto(img, x, y, l, a)
nubecilla(img, 300, 380); nubecilla(img, 790, 400); nubecilla(img, 850, 720); nubecilla(img, 230, 730)

# flores (atrás → adelante) con sombra suave bajo cada corola
def sombra_bloom(x, y, R):
    cap = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(cap).ellipse([x - R * 0.9, y + R * 0.15, x + R * 0.9, y + R * 1.05],
                                fill=(74, 52, 33, 80))
    img.alpha_composite(cap.filter(ImageFilter.GaussianBlur(16)))

for _x, _y, _r in ((700, 360, 118), (350, 470, 108), (560, 400, 88), (400, 560, 150),
                   (600, 590, 132), (750, 620, 92), (480, 720, 96), (690, 740, 92)):
    sombra_bloom(_x, _y, _r)
girasol(img, 700, 360, 118, giro=12)
rosa(img, 350, 470, 108)
ranunculo(img, 560, 400, 88)
girasol(img, 400, 560, 150, giro=-8)
rosa(img, 600, 590, 132)
ranunculo(img, 750, 620, 92)
rosa(img, 480, 720, 96)
girasol(img, 690, 740, 92, giro=25)
boton(img, 300, 640, 26); boton(img, 800, 540, 24); boton(img, 620, 330, 22)
nubecilla(img, 470, 470); nubecilla(img, 660, 500)

# pétalos sueltos sobre papel, con nervadura central
d = ImageDraw.Draw(img)
colocados = 0
while colocados < 6:
    x, y = random.randint(280, 800), random.randint(880, 1280)
    if abs(x - CX) < 150 and 940 < y < 1080:
        continue  # no tapar el moño
    a = random.randint(0, 359)
    petal_r(img, x, y, 0, random.randint(26, 44), random.randint(16, 24),
            a, random.choice([(246, 190, 40), (250, 210, 90), (240, 175, 30)]) + (255,))
    r = math.radians(a)
    d.line([(x - math.cos(r) * 16, y - math.sin(r) * 16),
            (x + math.cos(r) * 16, y + math.sin(r) * 16)], fill=(190, 135, 20, 255), width=2)
    colocados += 1

# viñeta + grano + calidez
vin = Image.new("L", (W, H), 95)
ImageDraw.Draw(vin).ellipse([90, 60, W - 90, H - 60], fill=0)
vin = vin.filter(ImageFilter.GaussianBlur(160))
oscuro = Image.new("RGBA", (W, H), (52, 34, 12, 130))
img = Image.alpha_composite(img, Image.composite(oscuro, Image.new("RGBA", (W, H), (0, 0, 0, 0)), vin))
img = ImageEnhance.Color(img.convert("RGB")).enhance(1.08).convert("RGBA")
grano = Image.effect_noise((W, H), 10).convert("L").point(lambda v: v * 12 // 100)
img = Image.alpha_composite(img, Image.merge("RGBA", (grano, grano, grano, grano)))

img.convert("RGB").save("img/ramo.jpg", quality=90)
print("ramo v2 ok")

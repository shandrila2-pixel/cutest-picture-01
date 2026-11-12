# cutest-picture-01 entry v2: kawaii kitten, beanie, big glossy eyes
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

SS = 2
W = H = 1024 * SS
random.seed(9)

def layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def heart(dr, cx, cy, s, col):
    r = s * 0.30
    dr.ellipse([cx - s * 0.5, cy - s * 0.35, cx, cy + s * 0.15], fill=col)
    dr.ellipse([cx, cy - s * 0.35, cx + s * 0.5, cy + s * 0.15], fill=col)
    dr.polygon([(cx - s * 0.48, cy + s * 0.02), (cx + s * 0.48, cy + s * 0.02),
                (cx, cy + s * 0.55)], fill=col)

# ---------- background: soft pastel gradient, gentle blobs, sparkles ----------
bg = Image.new('RGB', (W, H), (255, 243, 240))
bd = ImageDraw.Draw(bg)
top, bot = (255, 243, 248), (255, 232, 216)
for y in range(H):
    f = y / H
    col = tuple(int(top[i] + (bot[i] - top[i]) * f) for i in range(3))
    bd.line([(0, y), (W, y)], fill=col)

blobs = layer()
bld = ImageDraw.Draw(blobs)
for _ in range(14):
    x, y = random.randint(0, W), random.randint(0, H)
    r = random.randint(160, 400)
    col = random.choice([(255, 214, 232, 36), (255, 224, 200, 34), (222, 240, 255, 34)])
    bld.ellipse([x - r, y - r, x + r, y + r], fill=col)
blobs = blobs.filter(ImageFilter.GaussianBlur(90))
bg = Image.alpha_composite(bg.convert('RGBA'), blobs)

spark = layer()
sd = ImageDraw.Draw(spark)
for _ in range(60):
    x, y = random.randint(0, W), random.randint(0, H)
    r = random.randint(4, 10) * SS // 2
    a = random.randint(80, 170)
    c = (255, 255, 255, a)
    sd.line([x - r, y, x + r, y], fill=c, width=3)
    sd.line([x, y - r, x, y + r], fill=c, width=3)
spark = spark.filter(ImageFilter.GaussianBlur(1))
bg = Image.alpha_composite(bg, spark)

img = bg

# ---------- ground shadow ----------
sh = layer()
shd = ImageDraw.Draw(sh)
shd.ellipse([512 * SS - 240 * SS, 885 * SS, 512 * SS + 240 * SS, 948 * SS], fill=(225, 175, 185, 90))
sh = sh.filter(ImageFilter.GaussianBlur(16 * SS // 2))
img = Image.alpha_composite(img, sh)

hx, hy, hr = 512 * SS, 545 * SS, 205 * SS

# ---------- body (small, below big head) with outline ----------
body = layer()
bod = ImageDraw.Draw(body)
bod.ellipse([hx - 218 * SS, 700 * SS, hx + 218 * SS, 930 * SS], fill=(249, 224, 199, 255))
# lighter belly patch
bod.ellipse([hx - 140 * SS, 760 * SS, hx + 140 * SS, 925 * SS], fill=(255, 238, 218, 255))
# one soft outline around body
bod.ellipse([hx - 218 * SS, 700 * SS, hx + 218 * SS, 930 * SS],
            outline=(235, 198, 170, 110), width=4)
body = body.filter(ImageFilter.GaussianBlur(1))
img = Image.alpha_composite(img, body)

# ---------- head: big circle, slightly warmer than body, soft rim ----------
head = layer()
hd = ImageDraw.Draw(head)
hd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 240, 222, 255))
for k in range(16):
    f = k / 16
    a = int(26 * f)
    r2 = hr * (1 - f * 0.16)
    hd.ellipse([hx - r2, hy - r2, hx + r2, hy + r2], outline=(240, 198, 160, a), width=5)
# fluffy cheek bumps on lower sides — very subtle, tucked at the jaw
for sx in (-1, 1):
    fx = hx + sx * (hr * 0.66)
    fy = hy + hr * 0.76
    r = 20 * SS
    hd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 240, 222, 255))
head = head.filter(ImageFilter.GaussianBlur(1.2))
img = Image.alpha_composite(img, head)

# ---------- beanie: dome + ribbed band + pompom ----------
beanie = layer()
b2 = ImageDraw.Draw(beanie)
band_top = hy - hr * 0.28
band_h = 64 * SS
dome_cy = hy - 30 * SS
dome_r = hr * 1.04
# dome
b2.pieslice([hx - dome_r, dome_cy - dome_r, hx + dome_r, dome_cy + dome_r], 180, 360,
            fill=(127, 216, 208, 255))
# knit chevrons, clipped to dome
for i in range(-11, 12):
    x0 = hx + i * 36 * SS
    if abs(x0 - hx) > dome_r - 26 * SS:
        continue
    for yy in range(int(dome_cy - dome_r), int(band_top), 24 * SS):
        half = math.sqrt(max(0.0, dome_r ** 2 - (dome_cy - yy) ** 2))
        if abs(x0 - hx) > half - 24 * SS:
            continue
        b2.line([x0 - 15 * SS, yy + 12 * SS, x0, yy], fill=(98, 192, 186, 110), width=4)
        b2.line([x0, yy, x0 + 15 * SS, yy + 12 * SS], fill=(98, 192, 186, 110), width=4)
# rim shading
for k in range(8):
    f = k / 8
    a = int(34 * (1 - f))
    b2.arc([hx - dome_r * (1 + f * 0.006), dome_cy - dome_r * (1 + f * 0.006),
            hx + dome_r * (1 + f * 0.006), dome_cy + dome_r * (1 + f * 0.006)],
           180, 360, fill=(70, 158, 152, a), width=6)
# ribbed band (slightly wider than dome = classic beanie)
band_w = dome_r + 14 * SS
b2.rounded_rectangle([hx - band_w, band_top, hx + band_w, band_top + band_h],
                     radius=30 * SS, fill=(109, 199, 192, 255))
for i in range(-13, 14):
    x0 = hx + i * 30 * SS
    if abs(x0 - hx) < band_w - 16 * SS:
        b2.line([x0, band_top + 10 * SS, x0, band_top + band_h - 10 * SS],
                fill=(88, 178, 172, 130), width=5)
# pompom: fluffy off-white ball
pom_r = 50 * SS
py = dome_cy - dome_r + 10 * SS
for k in range(5):
    f = k / 5
    r = pom_r * (1 - f * 0.5)
    b2.ellipse([hx - r, py - r, hx + r, py + r], fill=(252 - int(20 * f), 248 - int(26 * f), 250 - int(18 * f), 255))
for _ in range(22):
    ang = random.uniform(0, math.tau)
    rr = random.uniform(30, 54) * SS
    b2.line([hx + math.cos(ang) * 26 * SS, py + math.sin(ang) * 26 * SS,
             hx + math.cos(ang) * rr, py + math.sin(ang) * rr],
            fill=(252, 250, 253, 90), width=3)
beanie = beanie.filter(ImageFilter.GaussianBlur(0.7))
img = Image.alpha_composite(img, beanie)

# ---------- face ----------
face = layer()
fd = ImageDraw.Draw(face)
# eyes
ey = hy + 45 * SS
for sx in (-1, 1):
    ex = hx + sx * 84 * SS
    erx, ery = 47 * SS, 53 * SS
    fd.ellipse([ex - erx - 3 * SS, ey - ery - 3 * SS, ex + erx + 3 * SS, ey + ery + 3 * SS],
               fill=(118, 84, 80, 255))
    fd.ellipse([ex - erx, ey - ery, ex + erx, ey + ery], fill=(52, 36, 34, 255))
    fd.ellipse([ex - erx * 0.48, ey - ery * 0.64, ex - erx * 0.06, ey - ery * 0.20],
               fill=(255, 255, 255, 240))
    fd.ellipse([ex + erx * 0.10, ey + ery * 0.16, ex + erx * 0.44, ey + ery * 0.48],
               fill=(255, 255, 255, 165))
    fd.ellipse([ex - erx * 0.78, ey + ery * 0.28, ex - erx * 0.56, ey + ery * 0.52],
               fill=(255, 215, 222, 130))
# blush (soft, on own blurred layer)
face2 = layer()
f2 = ImageDraw.Draw(face2)
for sx in (-1, 1):
    bx = hx + sx * 148 * SS
    by = ey + 52 * SS
    f2.ellipse([bx - 36 * SS, by - 20 * SS, bx + 36 * SS, by + 20 * SS], fill=(255, 160, 188, 105))
face2 = face2.filter(ImageFilter.GaussianBlur(9))

# nose + mouth on a SHARP layer (never blurred)
sharpl = layer()
s2 = ImageDraw.Draw(sharpl)
# nose: rounded triangle, clearly visible
nx, ny = hx, ey + 66 * SS
s2.polygon([(nx - 17 * SS, ny - 9 * SS), (nx + 17 * SS, ny - 9 * SS), (nx, ny + 15 * SS)],
           fill=(240, 138, 160, 255))
s2.ellipse([nx - 6 * SS, ny - 5 * SS, nx + 6 * SS, ny + 2 * SS], fill=(255, 190, 205, 160))
# mouth: cat ω, bolder
mw = 32 * SS
s2.arc([nx - mw, ny + 8 * SS, nx, ny + 8 * SS + mw], 10, 170, fill=(176, 112, 108, 235), width=5)
s2.arc([nx, ny + 8 * SS, nx + mw, ny + 8 * SS + mw], 10, 170, fill=(176, 112, 108, 235), width=5)

img = Image.alpha_composite(img, face)
img = Image.alpha_composite(img, face2)
img = Image.alpha_composite(img, sharpl)

# ---------- paws ----------
paws = layer()
pd = ImageDraw.Draw(paws)
for sx in (-1, 1):
    px = hx + sx * 64 * SS
    py2 = 898 * SS
    pd.ellipse([px - 44 * SS, py2 - 30 * SS, px + 44 * SS, py2 + 30 * SS], fill=(255, 242, 224, 255))
    for i in (-1, 1):
        pd.line([px + i * 15 * SS, py2 - 15 * SS, px + i * 15 * SS, py2 + 8 * SS],
                fill=(232, 196, 172, 200), width=4)
paws = paws.filter(ImageFilter.GaussianBlur(0.8))
img = Image.alpha_composite(img, paws)

# ---------- floating hearts ----------
hh = layer()
hhd = ImageDraw.Draw(hh)
for cx, cy, s, col in [(190, 300, 72, (255, 125, 162, 215)),
                       (840, 260, 56, (255, 148, 178, 205)),
                       (866, 560, 40, (255, 168, 193, 195)),
                       (160, 640, 44, (255, 158, 188, 195)),
                       (742, 148, 30, (255, 183, 203, 175)),
                       (298, 148, 34, (255, 173, 198, 180)),
                       (560, 210, 26, (255, 195, 212, 160))]:
    heart(hhd, cx * SS, cy * SS, s * SS, col)
hh = hh.filter(ImageFilter.GaussianBlur(1.5))
img = Image.alpha_composite(img, hh)

out = img.convert('RGB').resize((1024, 1024), Image.LANCZOS)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
out.save(p)
print('saved cute v2', p)

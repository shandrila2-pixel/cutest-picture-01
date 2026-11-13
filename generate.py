# cutest-picture-01 entry — "cream kitten in a strawberry beanie hugging a plush bunny"
# Soft-shaded "fuzzy plush" look: numpy soft-ball shading + fur strokes + glossy eyes.
# Deterministic (fixed seeds), runs offline, writes entry.png next to this file.
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 2
W = H = 1024 * S
rs = np.random.RandomState(9)

img = np.zeros((H, W, 3), dtype=np.float64)

def lerp(a, b, t):
    return a + (b - a) * t

def paste_mask(c, color, m):
    for i in range(3):
        c[:, :, i] = c[:, :, i] * (1 - m) + color[i] * m
    return c

def ball(c, cx, cy, rx, ry, base, lx=0.0, ly=-0.9, feather=0.035, rot=0.0, edge=0.5):
    """Soft-shaded ball: warm shadow, bright lit side, subtle top highlight."""
    ys, xs = np.mgrid[0:H, 0:W]
    x = xs - cx; y = ys - cy
    if rot:
        t = math.radians(rot)
        x, y = x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t)
    q = (x / rx) ** 2 + (y / ry) ** 2
    m = np.clip(1.0 - (q - (1 - feather)) / feather, 0, 1)
    nx = x / rx; ny = y / ry
    d = np.sqrt(nx ** 2 + ny ** 2)
    # lit color and warm shadow color
    lit = np.clip(np.array(base, dtype=np.float64) * 1.05, 0, 255)
    shd = np.clip(np.array(base, dtype=np.float64) * np.array([0.80, 0.71, 0.66]), 0, 255)
    t2 = np.clip(d, 0, 1) ** 1.7
    light = np.clip((nx * lx + ny * ly) * 0.5 + 0.5, 0, 1)
    t2 = np.clip(t2 * (0.75 + 0.5 * (1 - light)), 0, 1)
    hi = np.clip(1 - ((nx - lx * 0.45) ** 2 + (ny - ly * 0.45) ** 2) / 0.22, 0, 1) ** 2 * edge * 0.3
    for i in range(3):
        col = lerp(lit[i], shd[i], t2) + hi * 255
        c[:, :, i] = c[:, :, i] * (1 - m) + col * m
    return c

def to_np(im):
    return np.asarray(im, dtype=np.float64)

def to_im(c):
    return Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))

# ---------- background: warm apricot glow ----------
ys, xs = np.mgrid[0:H, 0:W]
d = np.sqrt((xs - 0.5 * W) ** 2 + (ys - 0.40 * H) ** 2) / (0.72 * W)
for i, (a, b) in enumerate([(255, 251), (238, 216), (206, 172)]):
    img[:, :, i] = lerp(a, b, np.clip(d, 0, 1) ** 1.35)
halo = np.clip(1 - d / 0.55, 0, 1) ** 2 * 0.30
img += halo[:, :, None] * np.array([30, 20, 6])

# ---------- fluffy floor ----------
wav = 0.012 * H * (np.sin(xs / (0.055 * H)) * 0.5 + np.sin(xs / (0.019 * H) + 2.1) * 0.35)
floorm = np.clip((ys - (0.885 * H + wav)) / (0.12 * H), 0, 1) ** 1.4
img = paste_mask(img, (255, 246, 228), floorm * 0.92)

hx, hy = 0.5 * W, 0.40 * H
hr = 0.235 * W

FUR   = (252, 236, 208)   # main cream
FUR_L = (255, 246, 228)
FUR_D = (238, 208, 172)

# ---------- tail ----------
img = ball(img, 0.265 * W, 0.83 * H, 0.048 * W, 0.115 * H, FUR, lx=0.7, ly=-0.3, rot=-14)
img = ball(img, 0.225 * W, 0.715 * H, 0.068 * W, 0.082 * H, FUR, lx=0.6, ly=-0.5, rot=18)

# ---------- body ----------
img = ball(img, hx, 0.775 * H, 0.240 * W, 0.190 * H, FUR, lx=-0.15, ly=-0.85)
img = ball(img, hx + 0.015 * W, 0.805 * H, 0.150 * W, 0.120 * H, FUR_L, lx=-0.1, ly=-0.9, edge=0.3)

# ---------- head ----------
img = ball(img, hx, hy, hr, 0.94 * hr, FUR, lx=-0.2, ly=-0.85, edge=0.4)

# ---------- fur (subtle) ----------
fur = to_im(img)
fd = ImageDraw.Draw(fur, 'RGBA')
def fluff(cx, cy, rx, ry, n, lcol, dcol, lmin=8, lmax=20):
    for _ in range(n):
        a = rs.uniform(0, math.tau)
        px = cx + math.cos(a) * rx * rs2_pos(n)
        py = cy + math.sin(a) * ry * rs2_pos(n)
        out = rs.rand() < 0.35
        ln = rs.uniform(lmin, lmax) * S * (1.6 if out else 1.0)
        w = rs.uniform(1.4, 2.6) * S
        dxn, dyn = math.cos(a), math.sin(a)
        jx = rs.uniform(-0.5, 0.5); jy = rs.uniform(-0.3, 0.5)
        x1 = px - dxn * ln * 0.3 + jx * S; y1 = py - dyn * ln * 0.3 + jy * S
        x2 = px + dxn * ln + jx * S; y2 = py + dyn * ln + jy * S
        col = lcol if rs.rand() < 0.55 else dcol
        alpha = int(rs.uniform(16, 42))
        fd.line([x1, y1, x2, y2], fill=col + (alpha,), width=int(w))
def rs2_pos(n):
    return math.sqrt(rs.rand())
fluff(hx, hy, hr, 0.94 * hr, 1400, (255, 248, 231), FUR_D)
fluff(hx, 0.775 * H, 0.240 * W, 0.190 * H, 500, (255, 246, 226), FUR_D)
fur = fur.filter(ImageFilter.GaussianBlur(0.5 * S))
img = to_np(fur)

# ---------- strawberry beanie ----------
dome_cx, dome_cy = hx, hy - 0.50 * hr
dom_rx, dom_ry = 0.92 * hr, 0.55 * hr
band_cy = hy - 0.265 * hr
img = ball(img, dome_cx, dome_cy, dom_rx, dom_ry, (218, 64, 68), lx=-0.12, ly=-0.85)
bean = to_im(img)
bd = ImageDraw.Draw(bean, 'RGBA')
for row in range(-4, 5):
    yy = dome_cy + row * 0.100 * hr
    for i in range(-10, 11):
        xx = dome_cx + i * 0.100 * hr + row * 0.045 * hr
        q = ((xx - dome_cx) / dom_rx) ** 2 + ((yy - dome_cy) / dom_ry) ** 2
        if q > 0.70:
            continue
        s2 = 0.062 * hr
        bd.line([xx - s2, yy + s2 * 0.9, xx, yy - s2 * 0.55], fill=(255, 255, 255, 30), width=int(2.2 * S))
        bd.line([xx, yy - s2 * 0.55, xx + s2, yy + s2 * 0.9], fill=(148, 26, 30, 70), width=int(2.2 * S))
rs2 = np.random.RandomState(3)
for _ in range(9):
    a = rs2.uniform(-2.9, -0.25)
    rr = 0.35 + rs2.rand() * 0.38
    xx = dome_cx + math.cos(a) * rr * dom_rx
    yy = dome_cy + math.sin(a) * rr * dom_ry
    r = 0.024 * hr
    bd.ellipse([xx - r, yy - r * 1.3, xx + r, yy + r * 1.3], fill=(255, 242, 218, 235))
    bd.ellipse([xx - r * 0.35, yy - r * 0.95, xx + r * 0.3, yy - r * 0.3], fill=(255, 255, 255, 120))
# leafy calyx
leaf_c = (114, 164, 80)
tip_y = dome_cy - dom_ry
for ang, sc in [(-0.75, 0.9), (-0.35, 1.0), (0.0, 1.1), (0.35, 1.0), (0.75, 0.9)]:
    L = 0.30 * hr * sc
    bx0 = dome_cx + math.sin(ang) * 0.15 * hr
    by0 = tip_y + 0.10 * hr
    a0 = math.pi / 2 - ang
    pts = []
    for t in range(9):
        tt = t / 8
        px = bx0 + math.cos(a0) * L * tt
        py = by0 - math.sin(a0) * L * tt
        wid = math.sin(tt * math.pi) * 0.085 * hr
        perp = a0 + math.pi / 2
        pts.append((px + math.cos(perp) * wid, py + math.sin(perp) * wid))
    for t in range(8, -1, -1):
        tt = t / 8
        px = bx0 + math.cos(a0) * L * tt
        py = by0 - math.sin(a0) * L * tt
        wid = math.sin(tt * math.pi) * 0.085 * hr
        perp = a0 + math.pi / 2
        pts.append((px - math.cos(perp) * wid, py - math.sin(perp) * wid))
    bd.polygon(pts, fill=leaf_c + (255,))
# stem
bd.line([dome_cx, tip_y + 0.06 * hr, dome_cx + 0.025 * hr, tip_y - 0.10 * hr],
        fill=(92, 138, 62, 255), width=int(0.04 * hr))
img = to_np(bean)
# rolled brim
img = ball(img, dome_cx, band_cy, 0.96 * hr, 0.115 * hr, (206, 56, 60), lx=-0.08, ly=-0.6, edge=0.3)
band = to_im(img)
bd2 = ImageDraw.Draw(band, 'RGBA')
for i in range(-14, 15):
    xx = dome_cx + i * 0.068 * hr
    if abs(i) < 13:
        bd2.line([xx, band_cy - 0.075 * hr, xx + 0.018 * hr, band_cy + 0.075 * hr],
                 fill=(255, 255, 255, 34), width=int(2.4 * S))
img = to_np(band)

# ---------- eyes ----------
def eye(cx, cy, r):
    global img
    img = ball(img, cx, cy, r * 1.08, r * 1.08, (242, 212, 178), lx=0, ly=-0.4, edge=0.25)
    img = ball(img, cx, cy, r, r, (40, 24, 22), lx=0, ly=0, edge=0.0)
    ys2, xs2 = np.mgrid[0:H, 0:W]
    q = ((xs2 - cx) / (r * 0.90)) ** 2 + ((ys2 - cy) / (r * 0.90)) ** 2
    m = np.clip(1 - (q - 0.88) / 0.12, 0, 1)
    dd = np.sqrt(((xs2 - cx) / r) ** 2 + ((ys2 - cy) / r) ** 2)
    ir_hi = np.array([255, 202, 98], dtype=np.float64)
    ir_lo = np.array([116, 52, 22], dtype=np.float64)
    t = np.clip((dd - 0.10) / 0.78, 0, 1)
    ircol = np.zeros((H, W, 3))
    for i in range(3):
        ircol[:, :, i] = lerp(ir_hi[i], ir_lo[i], t ** 0.9)
    for i in range(3):
        img[:, :, i] = img[:, :, i] * (1 - m) + ircol[:, :, i] * m
    iris = to_im(img)
    idr = ImageDraw.Draw(iris, 'RGBA')
    for k in range(30):
        a = rs2.uniform(0, math.tau)
        r1, r2 = r * rs2.uniform(0.40, 0.55), r * rs2.uniform(0.78, 0.86)
        idr.line([cx + math.cos(a) * r1, cy + math.sin(a) * r1,
                  cx + math.cos(a) * r2, cy + math.sin(a) * r2],
                 fill=(255, 226, 150, 42), width=int(1.6 * S))
    img = to_np(iris)
    img = ball(img, cx, cy + r * 0.10, r * 0.50, r * 0.60, (24, 13, 11), edge=0.0)
    im2 = to_im(img)
    d2 = ImageDraw.Draw(im2, 'RGBA')
    d2.ellipse([cx - r * 0.60, cy - r * 0.74, cx - r * 0.12, cy - r * 0.34], fill=(255, 255, 255, 240))
    d2.ellipse([cx + r * 0.20, cy + r * 0.26, cx + r * 0.42, cy + r * 0.46], fill=(255, 255, 255, 140))
    sx2, sy2 = cx + r * 0.36, cy - r * 0.46
    sl = r * 0.20
    for a2 in (0, math.pi / 2):
        d2.line([sx2 - math.cos(a2) * sl, sy2 - math.sin(a2) * sl,
                 sx2 + math.cos(a2) * sl, sy2 + math.sin(a2) * sl],
                fill=(255, 255, 255, 185), width=int(1.8 * S))
    d2.ellipse([sx2 - sl * 0.28, sy2 - sl * 0.28, sx2 + sl * 0.28, sy2 + sl * 0.28], fill=(255, 255, 255, 220))
    img = to_np(im2)

ey = hy + 0.03 * hr
for sx in (-1, 1):
    eye(hx + sx * 0.40 * hr, ey, 0.24 * hr)

# ---------- nose, mouth, blep ----------
nose_y = hy + 0.46 * hr
im3 = to_im(img)
d3 = ImageDraw.Draw(im3, 'RGBA')
nw = 0.048 * hr
d3.polygon([(hx - nw, nose_y - nw * 0.5), (hx + nw, nose_y - nw * 0.5), (hx, nose_y + nw * 0.8)],
           fill=(245, 134, 144, 255))
d3.ellipse([hx - nw * 0.5, nose_y - nw * 0.35, hx + nw * 0.1, nose_y + nw * 0.1], fill=(255, 192, 202, 150))
mw = 0.13 * hr
m_top = nose_y + nw * 0.35
d3.arc([hx - mw, m_top, hx, m_top + mw], 20, 160, fill=(154, 92, 88, 235), width=int(2.6 * S))
d3.arc([hx, m_top, hx + mw, m_top + mw], 20, 160, fill=(154, 92, 88, 235), width=int(2.6 * S))
tw, th = 0.09 * hr, 0.145 * hr
ty = m_top + mw * 0.62
d3.rounded_rectangle([hx - tw, ty, hx + tw, ty + th], radius=int(tw), fill=(249, 140, 146, 255))
d3.ellipse([hx - tw * 0.55, ty + th * 0.5, hx + tw * 0.55, ty + th * 1.08], fill=(231, 106, 118, 150))
img = to_np(im3)
for sx in (-1, 1):
    q = ((xs - (hx + sx * 0.84 * hr)) / (0.20 * hr)) ** 2 + ((ys - (hy + 0.42 * hr)) / (0.12 * hr)) ** 2
    bl = np.clip(1 - q, 0, 1) ** 1.2
    img = paste_mask(img, (255, 138, 152), bl * 0.45)
im4 = to_im(img)
d4 = ImageDraw.Draw(im4, 'RGBA')
for sx in (-1, 1):
    for dy, ln in [(0.0, 0.75), (0.05, 0.65), (-0.04, 0.62)]:
        x0 = hx + sx * 0.64 * hr
        y0 = hy + 0.47 * hr + dy * hr
        x1 = hx + sx * (0.64 + ln) * hr
        y1 = y0 + dy * 0.55 * hr + rs2.uniform(-0.04, 0.04) * hr
        d4.line([x0, y0, x1, y1], fill=(255, 250, 240, 120), width=int(2.2 * S))
img = to_np(im4)

# ---------- plush bunny (held low, face fully visible) ----------
bx, by = 0.525 * W, 0.805 * H
img = ball(img, bx, by, 0.115 * W, 0.092 * H, (252, 240, 218), lx=-0.15, ly=-0.75)
img = ball(img, bx + 0.055 * W, by - 0.060 * H, 0.098 * W, 0.088 * H, (253, 243, 222), lx=-0.15, ly=-0.75)
# ears: one up, one floppy
img = ball(img, bx + 0.010 * W, by - 0.155 * H, 0.030 * W, 0.068 * H, (250, 237, 216), lx=0.2, ly=-0.85, rot=-6)
img = ball(img, bx + 0.010 * W, by - 0.155 * H, 0.016 * W, 0.045 * H, (255, 194, 196), lx=0.2, ly=-0.85, edge=0.2, rot=-6)
img = ball(img, bx + 0.130 * W, by - 0.060 * H, 0.024 * W, 0.055 * H, (248, 232, 208), lx=0.5, ly=-0.4, rot=58)
img = ball(img, bx + 0.127 * W, by - 0.054 * H, 0.013 * W, 0.038 * H, (255, 200, 202), lx=0.5, ly=-0.4, edge=0.2, rot=58)
im5 = to_im(img)
d5 = ImageDraw.Draw(im5, 'RGBA')
fx, fy = bx + 0.058 * W, by - 0.060 * H
for exs in (-1, 1):
    er = 0.012 * W
    d5.ellipse([fx + exs * 0.030 * W - er, fy - er, fx + exs * 0.030 * W + er, fy + er], fill=(74, 52, 48, 255))
    d5.ellipse([fx + exs * 0.030 * W - er * 0.4, fy - er * 0.6, fx + exs * 0.030 * W + er * 0.1, fy - er * 0.1],
               fill=(255, 255, 255, 210))
d5.arc([fx - 0.013 * W, fy + 0.014 * H, fx, fy + 0.028 * H], 15, 155, fill=(194, 124, 114, 220), width=int(2.0 * S))
d5.arc([fx, fy + 0.014 * H, fx + 0.013 * W, fy + 0.028 * H], 15, 155, fill=(194, 124, 114, 220), width=int(2.0 * S))
d5.ellipse([fx - 0.006 * W, fy + 0.005 * H, fx + 0.006 * W, fy + 0.014 * H], fill=(243, 134, 144, 230))
img = to_np(im5)
for exs in (-1, 1):
    q = ((xs - (fx + exs * 0.045 * W)) / (0.020 * W)) ** 2 + ((ys - (fy + 0.011 * H)) / (0.013 * H)) ** 2
    bl = np.clip(1 - q, 0, 1) ** 1.2
    img = paste_mask(img, (255, 152, 162), bl * 0.40)
im6 = to_im(img)
d6 = ImageDraw.Draw(im6, 'RGBA')
cx0, cy0 = bx + 0.058 * W, by + 0.010 * H
for dxs in (-1, 1):
    d6.ellipse([cx0 + dxs * 0.010 * W - 0.018 * W, cy0 - 0.012 * H, cx0 + dxs * 0.010 * W + 0.018 * W, cy0 + 0.012 * H],
               fill=(255, 154, 170, 255))
d6.ellipse([cx0 - 0.006 * W, cy0 - 0.006 * H, cx0 + 0.006 * W, cy0 + 0.006 * H], fill=(238, 114, 134, 255))
img = to_np(im6)

# ---------- front paws on bunny ----------
img = ball(img, bx - 0.150 * W, by - 0.030 * H, 0.062 * W, 0.062 * H, FUR, lx=-0.3, ly=-0.75)
img = ball(img, bx + 0.180 * W, by + 0.000 * H, 0.066 * W, 0.066 * H, FUR, lx=0.3, ly=-0.75)
im8 = to_im(img)
d8 = ImageDraw.Draw(im8, 'RGBA')
for px, py in [(bx - 0.150 * W, by - 0.030 * H), (bx + 0.180 * W, by + 0.000 * H)]:
    for k in (-1, 0, 1):
        d8.line([px + k * 0.013 * W, py - 0.026 * H, px + k * 0.015 * W, py + 0.007 * H],
                fill=(230, 196, 158, 120), width=int(2.2 * S))
img = to_np(im8)

# ---------- hind feet with toe beans ----------
for sx in (-1, 1):
    fx = hx + sx * 0.155 * W
    fy2 = 0.925 * H
    img = ball(img, fx, fy2, 0.110 * W, 0.068 * H, FUR, lx=sx * 0.2, ly=-0.85, edge=0.35)
im7 = to_im(img)
d7 = ImageDraw.Draw(im7, 'RGBA')
for sx in (-1, 1):
    fx = hx + sx * 0.155 * W
    fy2 = 0.925 * H
    bm = (255, 182, 180, 215)
    bm2 = (255, 162, 166, 175)
    r_b = 0.022 * W
    d7.ellipse([fx - r_b, fy2 - r_b * 0.55, fx + r_b, fy2 + r_b * 0.85], fill=bm)
    for k in (-1, 0, 1):
        bxk = fx + k * r_b * 0.92
        byk = fy2 - r_b * 1.10
        d7.ellipse([bxk - r_b * 0.42, byk - r_b * 0.40, bxk + r_b * 0.42, byk + r_b * 0.40], fill=bm2)
img = to_np(im7)

# ---------- contact shadow ----------
shadow = np.clip((ys - 0.972 * H) / (0.05 * H), 0, 1)
img = paste_mask(img, (198, 148, 116), shadow * 0.09)

# ---------- vignette ----------
v = np.sqrt(((xs - 0.5 * W) / (0.60 * W)) ** 2 + ((ys - 0.45 * H) / (0.60 * H)) ** 2)
vig = np.clip(1 - np.clip(v - 0.75, 0, 1) * 0.50, 0, 1)
img *= vig[:, :, None]

out = to_im(img).resize((1024, 1024), Image.LANCZOS)
outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
out.save(outp)
print('saved', outp)

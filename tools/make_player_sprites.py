#!/usr/bin/env python3
"""
Set sprite pemain final — The End Has Come
==========================================

Kontrak §17.3: kanvas 16x24, pivot (8,23), 30 frame x 5 arah = 150 frame digambar.
Layout atlas mengikuti `SpriteFactory._build()`:
  kolom : idle 2, walk 6, attack_melee 4, attack_ranged 3, hurt 2, death 6, dodge 4, interact 3
  baris : S, SE, E, NE, N   (SW, W, NW = mirror flip_h di runtime)

KEPUTUSAN SENI
--------------
1. Kepala/badan/tas digambar TANGAN per piksel (ASCII berpalet) — di 16x24 detail
   sekecil itu tidak boleh dihasilkan rumus, hasilnya selalu terlihat "generator".
2. Hanya lengan & kaki yang prosedural, karena bentuknya tabung.
3. Cahaya dari ATAS, bukan kiri-atas. Alasannya teknis: baris E/SE di-flip_h untuk
   jadi W/SW; kalau cahaya datang dari kiri, hasil mirror-nya jadi salah arah dan
   terlihat seperti sprite yang berbeda karakter. Rim atas + bayangan bawah aman
   di-mirror.
4. Palet 24 warna, 3 langkah per material, tanpa anti-aliasing (§17.1 #4).
5. Desain simetris (tanpa tas selempang / tempelan asimetris) supaya mirror sah.

Jalankan: python3 tools/make_player_sprites.py
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ palet ----
# huruf -> RGB. Huruf besar = versi gelap, kecil = dasar, kapital akhir = terang.
PAL = {
    "s": (164, 112, 74), "S": (121, 79, 50), "h": (200, 148, 102),  # kulit
    "a": (62, 52, 45),  "A": (42, 35, 30),  "H": (86, 73, 62),     # rambut
    "j": (38, 104, 98), "J": (25, 71, 68),  "k": (60, 148, 134),   # jaket teal
    "p": (68, 74, 58),  "P": (47, 52, 41),  "q": (88, 96, 74),     # celana
    "b": (98, 71, 52),  "B": (62, 45, 34),  "c": (126, 96, 70),    # sepatu
    "n": (88, 85, 60),  "N": (62, 60, 42),  "m": (112, 108, 78),   # tas kanvas
    "t": (58, 50, 38),  "T": (38, 32, 24),                         # tali tas
    "w": (92, 68, 46),  "W": (58, 42, 28),                         # ikat pinggang kulit
    "v": (172, 152, 88),                                            # gesper kuningan
    "u": (128, 134, 142),                                           # logam
    "e": (24, 21, 20),                                              # mata
    "y": (124, 76, 54),                                              # mulut
    "g": (30, 33, 28),                                              # kotoran
    ".": None,
}
OUTLINE = (21, 24, 28, 255)

W, H = 16, 24
WALK_COLS = None  # diisi saat build


def rgba(c):
    return (c[0], c[1], c[2], 255)


# ------------------------------------------------------------------ art ------
# Setiap baris HARUS 16 karakter. y1..y15 (baris 0 sengaja kosong).

BASE = {}

# Kepala 6 px (x5..x10): wajah butuh 2 px di antara kedua mata.
# Badan 6 px dengan tepi gelap di KEDUA sisi (silinder, bukan papan) — tepi dua
# sisi aman untuk mirror; tepi kiri-terang saja tidak.
# Tali tas 'T' dari bahu sampai pinggang, simetris di x6 dan x9.

BASE["s"] = [
    "......AAAA......",  # 1
    ".....AaaaaA.....",  # 2
    ".....AssssA.....",  # 3 dahi
    ".....AesseA.....",  # 4 mata x6 & x9
    ".....sssSss.....",  # 5 hidung
    "......SssS......",  # 6 dagu
    ".......SS.......",  # 7 leher
    "....kkkkkkkk....",  # 8 bahu
    ".....JtjjtJ.....",  # 9 jaket + tali tas
    ".....JtjjtJ.....",  # 10
    ".....JtjjtJ.....",  # 11
    ".....JjjjJJ.....",  # 12 ujung jaket
    ".....wwwwww.....",  # 13 ikat pinggang kulit
    ".....wwvvww.....",  # 14 gesper
]

BASE["se"] = [
    "......AAAA......",
    ".....AaaaaA.....",
    ".....AssssA.....",
    ".....AesseA.....",
    ".....sssSss.....",
    "......SssS......",
    ".......SS.......",
    "....kkkkkkkk....",
    ".....JtjjtJ.....",
    ".....JtjjtJ.....",
    ".....JtjjtJ.....",
    ".....JjjjJJ.....",
    ".....wwwwww.....",
    ".....wwvvww.....",
]

BASE["e"] = [
    "......AAAA......",
    ".....AaaaaA.....",
    ".....Aaaahh.....",
    ".....Aaaehs.....",
    ".....Asshhh.....",
    ".....ASsys......",
    ".......SS.......",
    "...kkkkkkk......",
    "..NmmJtjjJ......",
    "..NmmJtjjJ......",
    "..NmmJtjjJ......",
    "..NnnJjjjJ......",
    "..NNNwwwww......",
    "..NNNwwvvw......",
]

BASE["ne"] = [
    "......AAAA......",
    ".....AaaaaA.....",
    ".....AaaaaA.....",
    ".....AaaaaA.....",
    ".....AAaaAA.....",
    "......AaaA......",
    ".......SS.......",
    "...kkkkkkk......",
    "..jJNmmmmmN.....",
    "..jJNmtmmtN.....",
    "..jJNmtmmtN.....",
    "..jJNmmmmmN.....",
    "..NNNNnnnnN.....",
    "..NNNNwwwww.....",
]

BASE["n"] = [
    "......AAAA......",
    ".....AaaaaA.....",
    ".....AaaaaA.....",
    ".....AaaaaA.....",
    ".....AaaaaA.....",
    "......AaaA......",
    ".......SS.......",
    "....kkkkkkkk....",
    "....NmmmmmmN....",
    "....NmtmmtmN....",
    "....NmtmmtmN....",
    "....NmmmmmmN....",
    "....NNnnnnNN....",
    "....wwwwwwww....",
]

# --- tubuh tergeletak (death frame 4-5) --------------------------------------
# Bukan badan 90° (tidak muat di kanvas 16 px), tapi "tumpukan" yang terbaca:
# kepala di kiri, punggung di tengah, kaki di kanan, semua menyentuh tanah.
PRONE = {
    "s": [
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................",
        "....AAA.........",   # 19 rambut
        "...AaaaA........",   # 20
        "....AasssAjjjjj.",   # 21 wajah + punggung
        "...jjjjjjjjjjjpp",   # 22 jaket + pinggul
        "..jjjjjjjjjjjjpp",   # 23 badan di tanah
    ],
    "n": [
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................",
        "....AAA.........",
        "...AaaaaA.......",
        "....AaaaAjjjjjj.",
        "...jjjjjjjjjjjpp",
        "..NNNNNNNNNNNpp.",
    ],
}

# --- posisi meringkuk (dodge frame 1-2): bola guling, bukan jongkok ----------
TUCK = [
    "................", "................", "................", "................",
    "................", "................", "................", "................",
    "................", "................", "................", "................",
    "................", "................", "................",
    ".....AAA........",   # 15 kepala menunduk
    "....AaaaA.......",
    "...AjjjjjA......",   # 17 punggung membulat
    "..jjjjjjjjp.....",
    "..jjjjjjjjpp....",
    "..jjjjjjjjppb...",
    "...wwwwpppb.....",   # 21 kaki terlipat
    "....bbbb........",
    "................",
]


# ------------------------------------------------------------- komposisi ----

def blank():
    return {}


def put(mat, x, y, ch):
    if ch in (".", None):
        return
    if 0 <= x < W and 0 <= y < H:
        mat[(x, y)] = ch


def stamp(mat, rows, y0, x0=0):
    for i, row in enumerate(rows):
        assert len(row) == W, f"baris harus {W} char: {row!r} ({len(row)})"
        for x, ch in enumerate(row):
            put(mat, x0 + x, y0 + i, ch)


def leg(mat, x_hip, y_top, dx, lift, w=3, toe=0, inner=1):
    """Kaki 3 px: paha, betis, sepatu. lift = px telapak terangkat.

    inner = sisi yang menghadap kaki satunya (diberi nada gelap sebagai selout
    supaya kedua kaki terbaca terpisah, bukan satu blok).
    """
    foot_y = 23 - lift
    ankle_y = foot_y - 1
    knee_y = min(ankle_y - 1, y_top + 5)

    for y in range(y_top, ankle_y + 1):
        if y <= knee_y:
            t = (y - y_top) / max(1, knee_y - y_top)
            xc = x_hip + dx * 0.35 * t
        else:
            t = (y - knee_y) / max(1, ankle_y - knee_y)
            xc = x_hip + dx * (0.35 + 0.65 * t)
        for k in range(w):
            edge_in = (inner > 0 and k == w - 1) or (inner < 0 and k == 0)
            put(mat, int(round(xc)) + k, y, "P" if edge_in else "p")

    bx = int(round(x_hip + dx))
    for y in range(ankle_y, foot_y + 1):
        ch = "B" if y == foot_y else "b"
        for k in range(w - 1):
            put(mat, bx - 1 + k, y, ch)
        if toe:
            put(mat, bx - 1 + (w - 1) if toe > 0 else bx - 2, y, ch)


def arm(mat, shoulder, dx, dy, ext=0, w=2, length=6, back=False, inner=1, tone="j"):
    """Lengan 2 px: lengan jaket + tangan 1 px. inner = sisi menghadap badan."""
    sx, sy = shoulder
    hx = sx + dx + ext
    hy = sy + dy + length
    for y in range(sy, hy):
        t = (y - sy) / max(1, hy - sy)
        xc = int(round(sx + (hx - sx) * t))
        for k in range(w):
            edge_in = (inner > 0 and k == w - 1) or (inner < 0 and k == 0)
            ch = "J" if (y == hy - 1 or edge_in) else tone
            put(mat, xc + k, y, ch)
    for k in range(w):
        put(mat, int(round(hx)) + k, hy, "s")
    return hx, hy


def shade(mat):
    """Dimatikan: shading ditulis tangan lewat huruf palet.

    Versi otomatis (rim atas + gelap bawah per KOLOM) membuat setiap kolom punya
    titik terang sendiri, sehingga permukaan terlihat bergelombang dan seperti
    hasil generator. Shading sekarang eksplisit: terang di baris atas tiap bentuk,
    gelap di baris bawah, dan tepi dalam (selout) untuk memisahkan bagian.
    """
    return mat


def _unused_shade(mat):
    if not mat:
        return
    cols = {}
    rows = {}
    for (x, y) in mat:
        cols.setdefault(x, []).append(y)
        rows.setdefault(y, []).append(x)
    top = {x: min(v) for x, v in cols.items()}
    bot = {x: max(v) for x, v in cols.items()}

    def key(ch, want):
        # naik/turun satu langkah dalam ramp material
        ramp = {
            "s": "S", "h": "s", "a": "A", "H": "a", "j": "J", "k": "j",
            "p": "P", "q": "p", "b": "B", "c": "b", "n": "N", "m": "n",
        }
        rev = {
            "S": "s", "s": "h", "A": "a", "a": "H", "J": "j", "j": "k",
            "P": "p", "p": "q", "B": "b", "b": "c", "N": "n", "n": "m",
        }
        table = ramp if want == "light" else rev
        return table.get(ch, ch)

    out = dict(mat)
    for (x, y), ch in mat.items():
        if y == top[x]:
            lit = key(ch, "light")
            # jangan mencerahkan garis luar material gelap yang disengaja
            if ch not in "TyNBeu":
                out[(x, y)] = lit
        elif y == bot[x]:
            dark = key(ch, "dark")
            out[(x, y)] = dark
    return out


def render(mat):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for (x, y), ch in mat.items():
        c = PAL.get(ch)
        if c:
            px[x, y] = rgba(c)
    # outline 1 px
    filled = set(mat.keys())
    for (x, y) in filled:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in filled:
                px[nx, ny] = OUTLINE
    return img


# ------------------------------------------------------------------ pose ----

def pose_for(anim, f):
    p = dict(bob=0, crouch=0, lean=0, legL=(0, 0), legR=(0, 0),
             armL=(0, 0), armR=(0, 0), ext=0, prone=False, roll=False, head=0)
    if anim == "idle":
        p["bob"] = [0, -1][f]
        p["armL"] = (0, [0, -1][f]); p["armR"] = (0, [0, -1][f])
    elif anim == "walk":
        p.update([
            dict(legL=(2, 0), legR=(-2, 1), armL=(-1, 0), armR=(1, 0), bob=-1),
            dict(legL=(1, 0), legR=(-1, 2), armL=(-1, 1), armR=(0, 0), bob=0),
            dict(legL=(0, 0), legR=(1, 2), armL=(0, 1), armR=(-1, 0), bob=-1),
            dict(legL=(-2, 1), legR=(2, 0), armL=(1, 0), armR=(-1, 0), bob=-1),
            dict(legL=(-1, 2), legR=(1, 0), armL=(1, 1), armR=(0, 0), bob=0),
            dict(legL=(1, 2), legR=(0, 0), armL=(0, 1), armR=(0, 0), bob=-1),
        ][f])
    elif anim == "attack_melee":
        p.update([
            dict(armR=(-2, -2), lean=-1, ext=-2),
            dict(armR=(1, -3), lean=1, ext=4, legR=(1, 0)),
            dict(armR=(1, -1), lean=1, ext=3),
            dict(armR=(0, 0), lean=0, ext=0),
        ][f])
    elif anim == "attack_ranged":
        p.update([
            dict(armR=(2, -3), ext=2),
            dict(armR=(0, -3), lean=-1, ext=1, bob=-1),
            dict(armR=(2, -3), ext=2),
        ][f])
    elif anim == "hurt":
        p.update([dict(lean=-2, head=1, armL=(-1, 1)), dict(lean=-1, head=1)][f])
    elif anim == "death":
        p.update([
            dict(lean=-1, head=1),
            dict(lean=-2, head=1, crouch=2),
            dict(crouch=4, head=1),
            dict(crouch=6, lean=-1),
            dict(prone=True),
            dict(prone=True),
        ][f])
    elif anim == "dodge":
        p.update([
            dict(crouch=2),
            dict(crouch=5, lean=1, head=1, roll=True),
            dict(crouch=5, lean=1, head=1, roll=True),
            dict(crouch=1, bob=-1),
        ][f])
    elif anim == "interact":
        p.update([
            dict(armR=(1, 2), ext=1),
            dict(armR=(2, 3), ext=2, lean=1),
            dict(armR=(1, 2), ext=1),
        ][f])
    return p


# ------------------------------------------------------------------ arah ----

def shoulders(d):
    return {"s": ((3, 8), (12, 8)),
            "se": ((3, 8), (12, 8)),
            "e": ((5, 8), (5, 8)),
            "ne": ((3, 8), (12, 8)),
            "n": ((2, 8), (13, 8))}[d]


def hips(d):
    return {"s": (4, 9), "se": (4, 9), "e": (5, 7),
            "ne": (4, 9), "n": (4, 9)}[d]


def build(d, anim, f):
    p = pose_for(anim, f)
    mat = {}

    if p["prone"]:
        stamp(mat, PRONE["n" if d in ("n", "ne") else "s"], 0)
        return render(shade(mat))

    if p["roll"]:
        stamp(mat, TUCK, 0)
        return render(shade(mat))

    yb = 1 + p["bob"] + p["crouch"]
    lt = 15 + p["crouch"]

    hx_l, hx_r = hips(d)

    if d == "e":
        leg(mat, 6, lt, p["legR"][0], p["legR"][1], toe=1, inner=1)
        leg(mat, 7, lt, p["legL"][0], p["legL"][1], toe=1, inner=-1)
    else:
        leg(mat, hx_l, lt, p["legR"][0], p["legR"][1], toe=-1, inner=1)
        leg(mat, hx_l + 4, lt, p["legL"][0], p["legL"][1], toe=1, inner=-1)

    sh_l, sh_r = shoulders(d)
    if d in ("e", "ne", "n"):
        arm(mat, (sh_l[0], sh_l[1] + yb - 1), p["armL"][0], p["armL"][1], back=True, inner=1)

    stamp(mat, BASE[d], yb)

    if d == "e":
        arm(mat, (9, 8 + yb - 1), p["armR"][0], p["armR"][1], ext=p["ext"], inner=1)
    elif d == "n":
        arm(mat, (2, 8 + yb - 1), p["armL"][0], p["armL"][1], inner=-1)
        arm(mat, (12, 8 + yb - 1), p["armR"][0], p["armR"][1], ext=p["ext"], inner=1)
    else:
        arm(mat, (3, 8 + yb - 1), p["armL"][0], p["armL"][1], inner=-1)
        arm(mat, (11, 8 + yb - 1), p["armR"][0], p["armR"][1], ext=p["ext"], inner=1)

    return render(shade(mat))


DIRS5 = ["s", "se", "e", "ne", "n"]
ANIMS = [
    ("idle", 2, 3.0),
    ("walk", 6, 8.0),
    ("attack_melee", 4, 12.0),
    ("attack_ranged", 3, 12.0),
    ("hurt", 2, 10.0),
    ("death", 6, 10.0),
    ("dodge", 4, 14.0),
    ("interact", 3, 8.0),
]


def build_atlas():
    cols = sum(a[1] for a in ANIMS)
    atlas = Image.new("RGBA", (cols * W, len(DIRS5) * H), (0, 0, 0, 0))
    c = 0
    for (name, count, fps) in ANIMS:
        for r, d in enumerate(DIRS5):
            for i in range(count):
                atlas.alpha_composite(build(d, name, i), ((c + i) * W, r * H))
        c += count
    return atlas


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    atlas = build_atlas()
    out = os.path.join(root, "game", "assets", "sprites", "player.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    atlas.save(out)
    print(f"atlas {atlas.width}x{atlas.height} -> {out}")

    # zoom inspeksi: idle + walk S dan E
    zoom = Image.new("RGBA", (8 * 16 * 4 + 40, 24 * 16 + 20), (26, 28, 32, 255))
    cells = [(0, 0), (2, 0), (3, 0), (4, 0)]  # idle0, walk0, walk1, walk2 (kolom)
    for i, (col, row) in enumerate(cells):
        c = atlas.crop((col * W, row * H, col * W + W, row * H + H))
        zoom.alpha_composite(c.resize((W * 16, H * 16), Image.NEAREST), (10 + i * (W * 16 + 10), 10))
    zoom.save("/tmp/zoom_player.png")

    make_sheet(root, atlas)
    make_gif(root, atlas)
    make_character_sheet(root, atlas)


def make_sheet(root, atlas):
    S = 6
    cw, ch = W * S, H * S
    cols = sum(a[1] for a in ANIMS)
    pad_l, pad_t = 96, 44
    prev = Image.new("RGBA", (pad_l + cols * cw + 16, pad_t + 5 * ch + 40), (22, 24, 28, 255))
    d = ImageDraw.Draw(prev)
    try:
        bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        bold = small = ImageFont.load_default()
    d.text((12, 12), "PLAYER — 150 frame digambar · 16x24 · pivot (8,23) · 5 arah + 3 mirror",
           font=bold, fill=(232, 234, 238, 255))
    c = 0
    for (name, count, fps) in ANIMS:
        d.text((pad_l + c * cw + 2, 29), f"{name} {count}f @{int(fps)}",
               font=small, fill=(96, 200, 176, 255))
        c += count
    for r, dn in enumerate(DIRS5):
        y = pad_t + r * ch
        d.text((16, y + ch // 2 - 9), dn.upper(), font=bold, fill=(198, 208, 218, 255))
        c = 0
        for (name, count, fps) in ANIMS:
            for i in range(count):
                cell = atlas.crop(((c + i) * W, r * H, (c + i) * W + W, r * H + H))
                prev.alpha_composite(cell.resize((cw, ch), Image.NEAREST),
                                     (pad_l + (c + i) * cw, y))
                d.rectangle([pad_l + (c + i) * cw, y, pad_l + (c + i) * cw + cw - 1, y + ch - 1],
                            outline=(44, 48, 56, 255))
            c += count
    path = os.path.join(root, "docs", "art", "player-sheet-final.png")
    prev.save(path)
    print(f"sheet -> {path}")


def make_gif(root, atlas):
    start = ANIMS[0][1]          # walk mulai setelah idle
    gw, gh = W * 8, H * 8
    frames = []
    for i in range(6):
        sheet = Image.new("RGBA", (gw * 5 + 50, gh + 24), (22, 24, 28, 255))
        for r in range(5):
            cell = atlas.crop(((start + i) * W, r * H, (start + i) * W + W, r * H + H))
            sheet.alpha_composite(cell.resize((gw, gh), Image.NEAREST), (10 + r * (gw + 6), 10))
        frames.append(sheet)
    path = os.path.join(root, "docs", "art", "player-walk-preview.gif")
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=120, loop=0)
    print(f"gif -> {path}")


def make_character_sheet(root, atlas):
    """Lembar karakter: turnaround 5 arah + palet + catatan produksi."""
    S = 12
    gw, gh = W * S, H * S
    cols = 13
    pal_rows = (len([c for c in PAL.values() if c]) + cols - 1) // cols
    notes = [
        "Cahaya dari ATAS, bukan kiri-atas: baris E/SE dipakai juga sebagai W/SW lewat flip_h.",
        "Kalau cahaya dari kiri, hasil mirror berlawanan arah dan terbaca sebagai karakter lain.",
        "Siluet: bahu 8 px, kepala 6 px (rasio 0,75), pinggang 6 px, kaki 3 px + celah 1 px.",
        "Detail asimetris (tas selempang, tambalan satu sisi) DILARANG — membatalkan baris mirror.",
        "Wajah 6 px: 5 px menyisakan 1 px di antara mata, dan itu terbaca seperti topeng.",
        "Tangan & sepatu memakai nada lebih terang dari lengan/kaki: penanda ujung anggota badan.",
    ]
    pw = 40 + 5 * (gw + 20)
    y_pal = 92 + gh + 44
    y_notes = y_pal + 34 + pal_rows * 54 + 16
    ph = y_notes + len(notes) * 20 + 28

    img = Image.new("RGBA", (pw, ph), (20, 22, 26, 255))
    d = ImageDraw.Draw(img)
    try:
        bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
        mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        bold = mid = small = ImageFont.load_default()

    d.text((24, 18), "THE END HAS COME — SET SPRITE PEMAIN v1", font=bold, fill=(236, 238, 242, 255))
    d.text((24, 48), "150 frame digambar / 240 di atlas · kanvas 16x24 · pivot (8,23) · kaki di baseline",
           font=small, fill=(150, 158, 168, 255))

    labels = [("S", "depan"), ("SE", "3/4 depan"), ("E", "profil"),
              ("NE", "3/4 belakang"), ("N", "punggung")]
    for i, (dn, note) in enumerate(labels):
        x = 24 + i * (gw + 20)
        cell = atlas.crop((0, i * H, W, i * H + H))
        img.alpha_composite(cell.resize((gw, gh), Image.NEAREST), (x, 88))
        d.text((x, 88 + gh + 6), dn, font=mid, fill=(120, 216, 192, 255))
        d.text((x + 32, 88 + gh + 8), note, font=small, fill=(140, 148, 158, 255))

    d.text((24, y_pal), "PALET — 26 warna · 3 langkah per material · tanpa anti-aliasing",
           font=mid, fill=(230, 232, 236, 255))
    i = 0
    for k, c in PAL.items():
        if c is None:
            continue
        bx = 24 + (i % cols) * 60
        by = y_pal + 26 + (i // cols) * 54
        d.rectangle([bx, by, bx + 50, by + 30], fill=(c[0], c[1], c[2], 255))
        d.text((bx, by + 33), f"{k} {c[0]:02x}{c[1]:02x}{c[2]:02x}", font=small,
               fill=(126, 134, 144, 255))
        i += 1

    for j, t in enumerate(notes):
        d.text((24, y_notes + j * 20), "· " + t, font=small, fill=(170, 178, 188, 255))

    path = os.path.join(root, "docs", "art", "player-character-sheet.png")
    img.save(path)
    print(f"character sheet -> {path}")


if __name__ == "__main__":
    main()

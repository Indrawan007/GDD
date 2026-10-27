#!/usr/bin/env python3
"""
Set sprite pemain — The End Has Come  (v2: proporsi manusia)
=============================================================

Kontrak §17.3: kanvas 16x24, pivot (8,23), 30 frame x 5 arah = 150 frame digambar.

PROPORSI — diambil dari foto model berdiri, bukan selera
--------------------------------------------------------
Diukur dari referensi full-body (lihat docs/art/README.md):
    tinggi figur            1063 px
    tinggi kepala            ~144 px   -> 7,4 kepala
    lebar bahu              240 px
    lebar kepala             96 px    -> bahu = 2,5 x kepala
    panjang kaki (crotch)   ~430 px   -> 40-45% tinggi

Kanvas kita 24 px. Kepala 3 px (24/7,4) mustahil diberi wajah, jadi kepala
dipaksa 5 px = 4,8 kepala. Sisa tinggi dibagi mengikuti rasio asli:

    kepala   5 px  (21%)   [asli 13% — ini satu-satunya penyimpangan besar]
    leher    1 px  ( 4%)
    badan    7 px  (29%)   [asli 33%]
    kaki    10 px  (42%)   [asli 42-45%]  <- yang sebelumnya cuma 8 px

Sebelumnya: kepala 6, kaki 8 = 1:3,8 kepala. Itu chibi. Sekarang 1:4,8 dengan
kaki 42% tinggi — mendekati manusia, dan wajah masih terbaca.

ATURAN TEKNIS
-------------
1. Cahaya dari ATAS (bukan kiri-atas) supaya baris E/SE aman saat di-flip_h.
2. Bob hanya ke BAWAH (0 / +1). Kalau ke atas, kepala menyentuh baris 0.
3. Kepala 6 px: wajah 5 px hanya menyisakan 1 px antar mata -> terbaca topeng.
4. Selout 1 px memisahkan lengan/badan dan kaki/kaki.
5. Simetris wajib; detail asimetris membatalkan baris mirror.

Jalankan: python3 tools/make_player_sprites.py
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ palet ----
PAL = {
    "s": (170, 118, 78), "S": (126, 82, 52), "h": (206, 154, 108),  # kulit
    "a": (62, 52, 45),  "A": (40, 33, 28),  "H": (88, 74, 62),     # rambut
    "j": (38, 104, 98), "J": (24, 68, 66),  "k": (56, 140, 128),   # jaket teal
    "p": (70, 76, 60),  "P": (46, 51, 40),  "q": (90, 98, 76),     # celana
    "b": (96, 70, 52),  "B": (58, 42, 32),  "c": (124, 94, 68),    # sepatu
    "n": (90, 86, 62),  "N": (62, 59, 41),  "m": (114, 110, 80),   # tas kanvas
    "t": (60, 52, 40),  "T": (38, 32, 24),                         # tali tas
    "w": (92, 68, 46),  "W": (58, 42, 28),                         # ikat pinggang
    "v": (172, 152, 88),                                           # gesper
    "u": (128, 134, 142),                                          # logam
    "e": (26, 22, 20),                                             # mata
    "y": (120, 74, 54),                                            # mulut
    "g": (34, 37, 31),                                             # kotoran
    ".": None,
}
OUTLINE = (21, 24, 28, 255)

W, H = 16, 24


def rgba(c):
    return (c[0], c[1], c[2], 255)


# ------------------------------------------------------------------- art -----
# 13 baris = y1..y13. Kaki (y14..y23) dibuat prosedural oleh leg().
# Skema: terang di baris atas tiap bentuk, gelap di baris bawah, selout di tepi dalam.

BASE = {}

# Kepala 6 baris (1-6). Baris 3 = DAHI, wajib ada: tanpa dahi, mata menempel
# langsung di bawah rambut dan keduanya menyatu jadi satu blok gelap.
# Sisi mata memakai kulit (bukan rambut) supaya mata tidak menyatu dengan rambut.

BASE["s"] = [
    "......HHHH......",  # 1  atap rambut
    ".....HaaaaH.....",  # 2  rambut
    ".....SssSss.....",  # 3  dahi
    ".....sesseS.....",  # 4  mata x6 & x9
    ".....sshsss.....",  # 5  hidung terang 2 px
    "......syys......",  # 6  mulut + dagu
    "..kkkkkkkkkkkk..",  # 7  bahu menyambung ke lengan (bukan kaus tanpa lengan)
    "....JtjjjjtJ....",  # 8  dada + tali tas
    "....JtjjjjtJ....",  # 9
    "....JjjjjjjJ....",  # 10 pinggang
    "....JjjjjjjJ....",  # 11
    ".....JjjjjJ.....",  # 12 pinggang menyempit
    ".....wwvvww.....",  # 13 ikat pinggang + gesper
]

BASE["se"] = [
    "......HHHH......",
    ".....HaaaaH.....",
    ".....SssSss.....",
    ".....sesseS.....",
    ".....sshsss.....",
    "......syys......",
    "..kkkkkkkkkkkk..",
    "....JtjjjjtJ....",
    "....JtjjjjtJ....",
    "....JjjjjjjJ....",
    "....JjjjjjjJ....",
    ".....JjjjjJ.....",
    ".....wwvvww.....",
]

# Profil: mata tunggal di x7, hidung menonjol ke kanan di x9-x10.
BASE["e"] = [
    "......HHHH......",
    ".....HaaaaH.....",
    ".....Asssss.....",
    ".....Aseshs.....",
    ".....sshhss.....",
    "......syys......",
    ".....kkkkkk.....",
    "..nmmjjjjjj.....",
    "..nmmjjjjjj.....",
    "..nmmjjjjjJ.....",
    "..NNNjjjjjJ.....",
    "..NNNJJjjJJ.....",
    "..NNNwwvvww.....",
]

BASE["ne"] = [
    "......HHHH......",
    ".....HaaaaH.....",
    ".....HaaaaH.....",
    ".....AaaaaA.....",
    "......AaaA......",
    ".......SS.......",
    "...kkkkkkkkkk...",
    "...jmNNNNNNmj...",
    "...jmNttttNmj...",
    "...jmNNNNNNmj...",
    "....JmNNNNmJ....",
    ".....JmNNmJ.....",
    ".....wwvvww.....",
]

BASE["n"] = [
    "......HHHH......",
    ".....HaaaaH.....",
    ".....HaaaaH.....",
    ".....AaaaaA.....",
    "......AaaA......",
    ".......SS.......",
    "..kkkkkkkkkkkk..",
    "....jmNNNNmj....",
    "....jmNttNmj....",
    "....jmNNNNmj....",
    "....jmNNNNmj....",
    ".....JmNNmJ.....",
    ".....wwvvww.....",
]

# --- tubuh tergeletak (death frame 4-5) --------------------------------------
PRONE = {
    "s": [
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................",
        "....HHHH........",
        "...HaaaaH.......",
        "....HasssHjjjjj.",
        "...jjjjjjjjjpp..",
        "..jjjjjjjjjjpp..",
    ],
    "n": [
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................", "................", "................",
        "................", "................",
        "....HHHH........",
        "...HaaaaH.......",
        "....HaaaaHjjjjj.",
        "...jjjjjjjjjpp..",
        "..NNNNNNNNNNpp..",
    ],
}

# --- posisi meringkuk (dodge frame 1-2) --------------------------------------
TUCK = [
    "................", "................", "................", "................",
    "................", "................", "................", "................",
    "................", "................", "................", "................",
    "................",
    "......HHHH......",
    ".....HaaaaH.....",
    "....AjjjjjA.....",
    "...jjjjjjjjp....",
    "...jjjjjjjjpp...",
    "...jjjjjjjjppb..",
    "....wwwwpppb....",
    ".....bbbb.......",
    "................",
    "................",
]

# ------------------------------------------------------------- komposisi ----

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


def leg(mat, x_hip, y_top, dx, lift, inner=1, toe=0):
    """Kaki 10 baris: paha, lutut, betis, pergelangan, sepatu.

    Lebar 3 -> 2 (betis menyempit), sepatu 3 px + ujung menjulur ke arah luar.
    inner = sisi menghadap kaki satunya, diberi nada gelap (selout).
    """
    foot_y = 23 - lift
    ankle_y = foot_y - 2
    knee_y = min(max(y_top + 4, y_top + 1), ankle_y - 2)

    def px_row(y, xc, width):
        for k in range(width):
            edge_in = (inner > 0 and k == width - 1) or (inner < 0 and k == 0)
            put(mat, min(max(int(round(xc)) + k, 1), 14), y, "P" if edge_in else "p")

    # paha
    for y in range(y_top, knee_y + 1):
        t = (y - y_top) / max(1, knee_y - y_top)
        px_row(y, x_hip + dx * 0.25 * t, 3)
    # betis menyempit ke pergelangan
    for y in range(knee_y + 1, ankle_y):
        t = (y - knee_y) / max(1, ankle_y - knee_y)
        px_row(y, x_hip + dx * (0.25 + 0.55 * t), 3 if t < 0.5 else 2)
    # pergelangan
    px_row(ankle_y, x_hip + dx * 0.8, 2)

    bx = int(round(x_hip + dx))
    # sepatu: 3 px + tumit 1 px di belakang, ujung menjulur ke arah hadap
    for y in range(ankle_y + 1, foot_y):
        for k in range(3):
            put(mat, min(max(bx - 1 + k, 1), 14), y, "c" if y == ankle_y + 1 else "b")
    for k in range(3):
        put(mat, min(max(bx - 1 + k, 1), 14), foot_y, "B")
    if toe:
        tx = bx + 2 if toe > 0 else bx - 2
        put(mat, min(max(tx, 1), 14), foot_y, "B")
        put(mat, min(max(tx, 1), 14), foot_y - 1, "b")
        # tumit
        hx2 = bx - 2 if toe > 0 else bx + 2
        put(mat, min(max(hx2, 1), 14), foot_y, "B")


def arm(mat, shoulder, dx, dy, ext=0, length=9, inner=-1, tone="j"):
    """Lengan 2 px dengan siku: bahu -> siku -> pergelangan -> tangan."""
    sx, sy = shoulder
    hx = min(max(sx + dx + ext, 2), 13)
    hy = min(max(sy + dy + length, 9), 20)
    elbow_x = (sx + hx) / 2.0
    elbow_y = sy + (hy - sy) * 0.55

    for y in range(sy, hy + 1):
        if y <= elbow_y:
            t = (y - sy) / max(1, elbow_y - sy)
            xc = sx + (elbow_x - sx) * t
        else:
            t = (y - elbow_y) / max(1, hy - elbow_y)
            xc = elbow_x + (hx - elbow_x) * t
        xc = int(round(xc))
        if y == sy:                       # kemiringan bahu: 1 px lebih ke dalam
            xc += 1 if sx < 8 else -1
        for k in range(2):
            ch = "J" if y >= hy - 1 else tone
            put(mat, min(max(xc + k, 1), 14), y, ch)
    # tangan 2 px
    for k in range(2):
        put(mat, min(max(int(round(hx)) + k, 1), 14), hy, "s")


def shade(mat):
    """Shading ditulis tangan lewat huruf palet (lihat catatan di kepala berkas)."""
    return mat


def render(mat):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for (x, y), ch in mat.items():
        c = PAL.get(ch)
        if c:
            px[x, y] = rgba(c)
    filled = set(mat.keys())
    for (x, y) in filled:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in filled:
                px[nx, ny] = OUTLINE
    return img


# ------------------------------------------------------------------ pose ----
# CATATAN: bob hanya 0 atau +1 (turun). Bob negatif membuat kepala menyentuh
# baris 0 dan siluet terpotong.

def pose_for(anim, f):
    p = dict(bob=0, crouch=0, lean=0, legL=(0, 0), legR=(0, 0),
             armL=(0, 0), armR=(0, 0), ext=0, prone=False, roll=False, head=0,
             extL=0)
    if anim == "idle":
        p["bob"] = [0, 1][f]
        p["armL"] = (0, [0, 1][f]); p["armR"] = (0, [0, 1][f])
    elif anim == "walk":
        p.update([
            dict(legL=(2, 0), legR=(-2, 1), armL=(-1, 0), armR=(1, 0), bob=1),
            dict(legL=(1, 0), legR=(-1, 2), armL=(-1, 1), armR=(0, 0), bob=0),
            dict(legL=(0, 0), legR=(1, 2), armL=(0, 1), armR=(-1, 0), bob=1),
            dict(legL=(-2, 1), legR=(2, 0), armL=(1, 0), armR=(-1, 0), bob=1),
            dict(legL=(-2, 2), legR=(1, 0), armL=(1, 1), armR=(0, 0), bob=0),
            dict(legL=(1, 2), legR=(0, 0), armL=(0, 1), armR=(0, 0), bob=1),
        ][f])
    elif anim == "attack_melee":
        p.update([
            dict(armR=(-2, -1), lean=-1, ext=-3),
            dict(armR=(1, -2), lean=1, ext=5, legR=(1, 0), bob=1),
            dict(armR=(1, -1), lean=1, ext=4),
            dict(armR=(0, 0), lean=0, ext=0),
        ][f])
    elif anim == "attack_ranged":
        p.update([
            dict(armR=(2, -2), ext=3),
            dict(armR=(0, -2), lean=-1, ext=2, bob=1),
            dict(armR=(2, -2), ext=3),
        ][f])
    elif anim == "hurt":
        p.update([dict(lean=-2, head=1, armL=(-1, 1)), dict(lean=-1, head=1)][f])
    elif anim == "death":
        p.update([
            dict(lean=-1, head=1),
            dict(lean=-2, head=1, crouch=2, bob=1),
            dict(crouch=4, head=1),
            dict(crouch=7, lean=-1),
            dict(prone=True),
            dict(prone=True),
        ][f])
    elif anim == "dodge":
        p.update([
            dict(crouch=2),
            dict(crouch=7, lean=1, head=1, roll=True),
            dict(crouch=7, lean=1, head=1, roll=True),
            dict(crouch=1),
        ][f])
    elif anim == "interact":
        p.update([
            dict(armR=(1, 2), ext=1),
            dict(armR=(2, 3), ext=2, lean=1),
            dict(armR=(1, 2), ext=1),
        ][f])
    return p


# ------------------------------------------------------------------ arah ----

SHOULDER = {"s": (2, 12), "se": (2, 12), "e": (7, 7), "ne": (3, 11), "n": (2, 12)}
HIP_X = {"s": 4, "se": 4, "e": 5, "ne": 4, "n": 4}


def build(d, anim, f):
    p = pose_for(anim, f)
    mat = {}

    if p["prone"]:
        stamp(mat, PRONE["n" if d in ("n", "ne") else "s"], 0)
        return render(shade(mat))

    if p["roll"]:
        stamp(mat, TUCK, 0)
        return render(shade(mat))

    yb = 1 + p["bob"] + p["crouch"]          # baris pertama art (y1 saat diam)
    lt = 14 + p["bob"] + p["crouch"]         # paha mulai; telapak tetap di y23

    hx = HIP_X[d]

    if d == "e":
        leg(mat, 5, lt, p["legR"][0], p["legR"][1], inner=1, toe=1)
        leg(mat, 7, lt, p["legL"][0], p["legL"][1], inner=-1, toe=1)
    else:
        leg(mat, hx, lt, p["legR"][0], p["legR"][1], inner=1, toe=-1)
        leg(mat, hx + 4, lt, p["legL"][0], p["legL"][1], inner=-1, toe=1)

    sl, sr = SHOULDER[d]
    if d in ("e", "ne", "n"):
        arm(mat, (sl, 7 + p["bob"] + p["crouch"]), p["armL"][0], p["armL"][1],
            inner=1, tone="j")

    stamp(mat, BASE[d], yb)

    if d == "e":
        arm(mat, (7, 7 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
            ext=p["ext"], inner=-1)
    elif d == "n":
        arm(mat, (1, 7 + p["bob"] + p["crouch"]), p["armL"][0], p["armL"][1], inner=1)
        arm(mat, (13, 7 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
            ext=p["ext"], inner=-1)
    else:
        arm(mat, (1, 7 + p["bob"] + p["crouch"]), p["armL"][0], p["armL"][1], inner=1)
        arm(mat, (13, 7 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
            ext=p["ext"], inner=-1)

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


def validate(atlas):
    cells = sum(a[1] for a in ANIMS) * len(DIRS5)
    col = 0
    bad_edges, bad_top, empty = [], [], []
    for (name, count, fps) in ANIMS:
        for r, d in enumerate(DIRS5):
            for i in range(count):
                cell = atlas.crop(((col + i) * W, r * H, (col + i) * W + W, r * H + H))
                px = cell.load()
                filled = [(x, y) for y in range(H) for x in range(W) if px[x, y][3] > 0]
                if not filled:
                    empty.append(f"{name}/{d}/{i}")
                content = [(x, y) for (x, y) in filled if px[x, y][:3] != OUTLINE[:3]]
                if any(x in (0, W - 1) for x, _ in content):
                    bad_edges.append(f"{name}/{d}/{i}")
                if any(y == 0 for _, y in content):
                    bad_top.append(f"{name}/{d}/{i}")
        col += count

    print(f"  sel diperiksa      : {cells}")
    print(f"  sel kosong         : {len(empty)}")
    print(f"  isi menyentuh tepi : {len(bad_edges)}")
    print(f"  isi di baris 0     : {len(bad_top)}")
    ok = not (empty or bad_edges or bad_top)
    print(f"  HASIL              : {'LULUS' if ok else 'GAGAL'}")
    return ok


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    atlas = build_atlas()
    out = os.path.join(root, "game", "assets", "sprites", "player.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    atlas.save(out)
    print(f"atlas {atlas.width}x{atlas.height} -> {out}")
    validate(atlas)
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
    start = ANIMS[0][1]
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
    S = 12
    gw, gh = W * S, H * S
    cols = 13
    pal_items = [(k, c) for k, c in PAL.items() if c]
    pal_rows = (len(pal_items) + cols - 1) // cols
    notes = [
        "Proporsi diukur dari foto: 7,4 kepala; bahu = 2,5 x lebar kepala; kaki 41,5% tinggi.",
        "Di 24 px kepala 3 px mustahil, jadi kepala 5 px (4,8 kepala) dan kaki 10 px (42%).",
        "Kaki 41,7% hampir sama dengan foto (41,5%); selisih tinggi diserap kepala, bukan kaki.",
        "v1 lama: kepala 6 px, kaki 8 px = 1:3,8 kepala — chibi. v2: 1:4,8 dengan kaki 10 px.",
        "Cahaya dari ATAS: baris E/SE dipakai juga sebagai W/SW lewat flip_h.",
        "Bob hanya ke bawah (0/+1); bob ke atas membuat kepala menyentuh baris 0.",
        "Detail asimetris (tas selempang) DILARANG — membatalkan baris mirror.",
        "WAJAH butuh 3 baris: rambut / DAHI / mata. Tanpa baris dahi, mata menempel",
        "  di bawah rambut dan keduanya menyatu jadi satu blok gelap (diuji 4 varian).",
        "Sisi baris mata harus KULIT, bukan rambut — kalau rambut, kedua mata menyatu",
        "  dengan massa rambut. Ini juga alasan kepala tidak boleh < 6 baris.",
    ]
    pw = 40 + 5 * (gw + 20)
    y_pal = 92 + gh + 44
    y_notes = y_pal + 34 + pal_rows * 54 + 16 + 12 + 4 * 34 + 12
    ph = y_notes + len(notes) * 20 + 28

    img = Image.new("RGBA", (pw, ph), (20, 22, 26, 255))
    d = ImageDraw.Draw(img)
    try:
        bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
        mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        bold = mid = small = ImageFont.load_default()

    d.text((24, 18), "THE END HAS COME — SET SPRITE PEMAIN v2 (proporsi manusia)",
           font=bold, fill=(236, 238, 242, 255))
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
    for i, (k, c) in enumerate(pal_items):
        bx = 24 + (i % cols) * 60
        by = y_pal + 26 + (i // cols) * 54
        d.rectangle([bx, by, bx + 50, by + 30], fill=(c[0], c[1], c[2], 255))
        d.text((bx, by + 33), f"{k} {c[0]:02x}{c[1]:02x}{c[2]:02x}", font=small,
               fill=(126, 134, 144, 255))

    prop = [("kepala", 13.5, 5 / 24 * 100), ("leher", 4.7, 1 / 24 * 100),
            ("badan", 40.3, 7 / 24 * 100), ("kaki", 41.5, 10 / 24 * 100)]
    bar_top = y_pal + 34 + pal_rows * 54 + 16
    d.text((24, bar_top), "PROPORSI — foto vs sprite (persen tinggi total)",
           font=mid, fill=(230, 232, 236, 255))
    for i, (label, ref, spr) in enumerate(prop):
        by = bar_top + 26 + i * 34
        d.text((24, by + 1), label, font=small, fill=(150, 158, 168, 255))
        d.rectangle([110, by, 110 + int(ref * 8), by + 10], fill=(92, 110, 130, 255))
        d.rectangle([110, by + 13, 110 + int(spr * 8), by + 23], fill=(72, 176, 152, 255))
        d.text((110 + int(ref * 8) + 8, by - 1), f"foto {ref:.1f}%", font=small, fill=(120, 130, 142, 255))
        d.text((110 + int(spr * 8) + 8, by + 12), f"sprite {spr:.1f}%", font=small, fill=(110, 200, 178, 255))
    for j, t in enumerate(notes):
        d.text((24, y_notes + j * 20), "· " + t, font=small, fill=(170, 178, 188, 255))

    path = os.path.join(root, "docs", "art", "player-character-sheet.png")
    img.save(path)
    print(f"character sheet -> {path}")


if __name__ == "__main__":
    main()

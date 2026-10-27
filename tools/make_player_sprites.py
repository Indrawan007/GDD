#!/usr/bin/env python3
"""
Set sprite pemain — The End Has Come  (v3: kanvas 24x32)
========================================================

KENAPA NAIK DARI 16x24
----------------------
Referensi yang diberikan (288x52, karakter ~51 px tinggi) punya proporsi 1:4 —
sama seperti versi kita — tetapi **2x resolusi**. Itu sumber seluruh selisihnya:
di 16x24, wajah hanya dapat 3 baris; di 24x32 dapat 5-6 baris, dan itu perbedaan
antara "wajah terbaca" dan "wajah tidak ada".

Kanvas 24x32 = 1,5 tile x 2 tile @ tile 16. Aturan grid tetap; hanya sel yang
membesar 2x luasnya (768 px vs 384 px).

PROPORSI (24x32)
----------------
    kepala  8 baris  (25%)   wajah 6 baris: rambut x2, dahi, mata, hidung, mulut
    leher   1 baris  ( 3%)
    badan   9 baris  (28%)
    ikat    1 baris
    kaki   13 baris  (41%)   <- sama dengan manusia (41,5%)

ATURAN GAMBAR
-------------
1. Cahaya dari ATAS (baris E/SE juga dipakai sebagai W/SW lewat flip_h).
2. Ramp 4 langkah per material, tanpa anti-aliasing.
3. Outline 1 px di sekeliling siluet; tepi dalam memakai selout (ramp tergelap).
4. Simetris; detail asimetris membatalkan baris mirror.
5. Baris ditulis lewat R() (run-length) supaya jumlah 24 px tidak pernah salah hitung.

Jalankan: python3 tools/make_player_sprites.py
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ palet ----
PAL = {
    # rambut (4 langkah)
    "a0": (26, 21, 18), "a1": (40, 32, 27), "a2": (58, 46, 38), "a3": (80, 65, 52),
    # kulit
    "s0": (116, 72, 45), "s1": (152, 98, 63), "s2": (185, 129, 88), "s3": (212, 162, 118),
    # jaket teal (aksen pemain, dilarang dipakai di lingkungan)
    "j0": (14, 48, 47), "j1": (23, 72, 69), "j2": (35, 101, 93), "j3": (55, 139, 125),
    "j4": (88, 178, 156),
    # celana
    "p0": (31, 34, 26), "p1": (45, 50, 38), "p2": (62, 68, 51), "p3": (82, 90, 68),
    # sepatu
    "b0": (34, 25, 19), "b1": (56, 41, 30), "b2": (84, 62, 44),
    # tas kanvas
    "n0": (48, 45, 30), "n1": (72, 66, 45), "n2": (96, 88, 60), "n3": (120, 110, 78),
    # ikat pinggang / logam
    "w0": (38, 27, 18), "w1": (66, 47, 31), "v": (170, 150, 90), "u": (130, 136, 144),
    # wajah
    "e": (18, 16, 15), "m": (104, 60, 44),
}
OUTLINE = (19, 22, 26, 255)

W, H = 24, 32
FEET_Y = 31


PAD_LOG = []


def R(*pairs) -> list:
    """Bangun satu baris dari (token, jumlah), lalu pusatkan ke lebar kanvas.

    Kalau jumlah token < W, sisa piksel diisi '.' secara simetris (kiri/kanan).
    Kalau lebih, itu bug dan harus diperbaiki — bukan dipotong diam-diam.
    """
    out = []
    for ch, n in pairs:
        out += [ch] * n
    if len(out) < W:
        PAD_LOG.append(len(out))
        gap = W - len(out)
        left = gap // 2
        out = ["."] * left + out + ["."] * (gap - left)
    assert len(out) == W, f"baris = {len(out)} px, harus {W}: {out}"
    return out


# ------------------------------------------------------------------- art -----
# Baris 1..19 ditulis tangan. Kaki (20..31) prosedural.

BASE = {}

# ============================== S (depan) ===================================
BASE["s"] = [
    # --- kepala: 8 baris
    R((".", 9), ("a2", 6), (".", 9)),                             # 1 atap rambut
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),       # 2
    R((".", 8), ("a1", 1), ("a3", 1), ("s2", 4), ("a3", 1), ("a1", 1), (".", 8)),  # 3 poni
    R((".", 8), ("s1", 1), ("s3", 6), ("s1", 1), (".", 8)),       # 4 dahi
    R((".", 8), ("s1", 1), ("s2", 1), ("e", 1), ("s2", 2), ("e", 1), ("s2", 1),
      ("s1", 1), (".", 8)),                                       # 5 mata
    R((".", 8), ("s1", 1), ("s2", 2), ("s3", 2), ("s2", 2), ("s1", 1), (".", 8)),  # 6 hidung
    R((".", 8), ("s1", 1), ("s2", 1), ("s1", 1), ("m", 2), ("s1", 1), ("s2", 1),
      ("s1", 1), (".", 8)),                                       # 7 mulut
    R((".", 9), ("s1", 1), ("s2", 4), ("s1", 1), (".", 9)),       # 8 dagu
    # --- leher
    R((".", 10), ("s1", 4), (".", 10)),                           # 9
    # --- badan: bahu 14 px (x5..x18)
    R((".", 4), ("j3", 16), (".", 4)),                            # 10 bahu 16 px
    R((".", 4), ("j1", 1), ("j2", 1), ("j3", 2), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 2), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 11 dada + tali
    R((".", 4), ("j1", 1), ("j2", 1), ("j3", 2), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 2), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 12
    R((".", 4), ("n0", 1), ("j2", 1), ("j3", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 1), ("j2", 1),
      ("n0", 1), (".", 4)),                                       # 13 rusuk ransel
    R((".", 4), ("n0", 1), ("j2", 1), ("j3", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 1), ("j2", 1),
      ("n0", 1), (".", 4)),                                       # 14
    R((".", 4), ("j1", 1), ("j2", 1), ("j2", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j2", 1), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 15
    R((".", 5), ("j1", 1), ("j2", 12), ("j1", 1), (".", 5)),      # 16 pinggang
    R((".", 5), ("j0", 1), ("j1", 12), ("j0", 1), (".", 5)),      # 17 ujung jaket
    R((".", 5), ("w1", 14), (".", 5)),                            # 18 ikat pinggang
    R((".", 5), ("w0", 5), ("v", 4), ("w0", 5), (".", 5)),        # 19 gesper
]

# ============================== SE (3/4 depan) ==============================
BASE["se"] = [
    R((".", 9), ("a2", 6), (".", 9)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 1), ("a3", 1), ("s2", 4), ("a3", 1), ("a1", 1), (".", 8)),
    R((".", 8), ("s1", 1), ("s3", 6), ("s1", 1), (".", 8)),
    R((".", 8), ("s1", 1), ("s2", 1), ("e", 1), ("s2", 2), ("e", 1), ("s2", 1),
      ("s1", 1), (".", 8)),
    R((".", 8), ("s1", 1), ("s2", 2), ("s3", 2), ("s2", 2), ("s1", 1), (".", 8)),
    R((".", 8), ("s1", 1), ("s2", 1), ("s1", 1), ("m", 2), ("s1", 1), ("s2", 1),
      ("s1", 1), (".", 8)),
    R((".", 9), ("s1", 1), ("s2", 4), ("s1", 1), (".", 9)),
    R((".", 10), ("s1", 4), (".", 10)),
    R((".", 4), ("j3", 16), (".", 4)),                            # 10 bahu 16 px
    R((".", 4), ("j1", 1), ("j2", 1), ("j3", 2), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 2), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 11 dada + tali
    R((".", 4), ("j1", 1), ("j2", 1), ("j3", 2), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 2), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 12
    R((".", 4), ("n0", 1), ("j2", 1), ("j3", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 1), ("j2", 1),
      ("n0", 1), (".", 4)),                                       # 13 rusuk ransel
    R((".", 4), ("n0", 1), ("j2", 1), ("j3", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j3", 1), ("j2", 1),
      ("n0", 1), (".", 4)),                                       # 14
    R((".", 4), ("j1", 1), ("j2", 1), ("j2", 1), ("j2", 1), ("n1", 1), ("j2", 1),
      ("j0", 2), ("j2", 1), ("n1", 1), ("j2", 1), ("j2", 1), ("j2", 1),
      ("j1", 1), (".", 4)),                                       # 15
    R((".", 5), ("j1", 1), ("j2", 12), ("j1", 1), (".", 5)),      # 16 pinggang
    R((".", 5), ("j0", 1), ("j1", 12), ("j0", 1), (".", 5)),      # 17 ujung jaket
    R((".", 5), ("w1", 14), (".", 5)),                            # 18 ikat pinggang
    R((".", 5), ("w0", 5), ("v", 4), ("w0", 5), (".", 5)),        # 19 gesper
]

# ============================== E (profil kanan) ============================
# Kepala bergeser 1 px ke kanan; hidung menonjol di x16; tas terlihat di kiri.
BASE["e"] = [
    R((".", 10), ("a2", 6), (".", 8)),
    R((".", 9), ("a1", 1), ("a2", 6), ("a1", 1), (".", 7)),
    R((".", 9), ("a1", 1), ("a3", 1), ("s2", 4), ("a3", 1), (".", 8)),
    R((".", 9), ("s1", 1), ("s3", 6), (".", 8)),
    R((".", 9), ("s1", 1), ("s2", 1), ("e", 1), ("s2", 3), (".", 9)),
    R((".", 9), ("s1", 1), ("s2", 2), ("s3", 3), (".", 9)),        # hidung menonjol
    R((".", 9), ("s1", 1), ("s1", 1), ("m", 2), ("s1", 1), (".", 10)),
    R((".", 10), ("s1", 1), ("s2", 3), ("s1", 1), (".", 9)),
    R((".", 11), ("s1", 3), (".", 10)),
    R((".", 7), ("j3", 11), (".", 6)),                             # bahu (lebih sempit di profil)
    R((".", 5), ("n2", 3), ("j2", 1), ("j3", 8), ("j1", 1), (".", 6)),
    R((".", 5), ("n1", 3), ("j2", 1), ("j3", 7), ("j2", 1), (".", 7)),
    R((".", 5), ("n1", 3), ("j2", 1), ("j3", 6), ("j2", 2), (".", 7)),
    R((".", 5), ("n0", 3), ("j1", 1), ("j2", 6), ("j1", 2), (".", 7)),
    R((".", 5), ("n0", 3), ("j1", 1), ("j2", 5), ("j1", 2), (".", 8)),
    R((".", 5), ("n0", 3), ("j1", 1), ("j2", 5), ("j1", 1), (".", 8)),
    R((".", 6), ("w1", 7), (".", 11)),
    R((".", 6), ("w0", 3), ("v", 2), ("w0", 2), (".", 11)),
    R((".", 6), ("w0", 7), (".", 11)),
]

# ============================== NE (3/4 belakang) ===========================
BASE["ne"] = [
    R((".", 9), ("a2", 6), (".", 9)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 2), ("a2", 4), ("a1", 2), (".", 8)),
    R((".", 9), ("a1", 1), ("a2", 4), ("a1", 1), (".", 9)),
    R((".", 10), ("a1", 4), (".", 10)),
    R((".", 10), ("s0", 4), (".", 10)),                           # leher (belakang)
    R((".", 4), ("j3", 16), (".", 4)),                            # 10 bahu
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 4), ("u", 4), ("n3", 4), ("n1", 1),
      ("j1", 1), (".", 4)),                                       # 13 gesper tas
    R((".", 4), ("j1", 1), ("n1", 1), ("n2", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n2", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 5), ("j1", 1), ("n0", 12), ("j1", 1), (".", 5)),
    R((".", 5), ("j0", 1), ("j1", 12), ("j0", 1), (".", 5)),
    R((".", 5), ("w1", 14), (".", 5)),
    R((".", 5), ("w0", 5), ("v", 4), ("w0", 5), (".", 5)),
]

# ============================== N (punggung) ================================
BASE["n"] = [
    R((".", 9), ("a2", 6), (".", 9)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 1), ("a2", 6), ("a1", 1), (".", 8)),
    R((".", 8), ("a1", 2), ("a2", 4), ("a1", 2), (".", 8)),
    R((".", 9), ("a1", 1), ("a2", 4), ("a1", 1), (".", 9)),
    R((".", 10), ("a1", 4), (".", 10)),
    R((".", 10), ("s0", 4), (".", 10)),
    R((".", 4), ("j3", 16), (".", 4)),                            # 10 bahu
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n3", 4), ("u", 4), ("n3", 4), ("n1", 1),
      ("j1", 1), (".", 4)),                                       # 13 gesper tas
    R((".", 4), ("j1", 1), ("n1", 1), ("n2", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 4), ("j1", 1), ("n1", 1), ("n2", 12), ("n1", 1), ("j1", 1), (".", 4)),
    R((".", 5), ("j1", 1), ("n0", 12), ("j1", 1), (".", 5)),
    R((".", 5), ("j0", 1), ("j1", 12), ("j0", 1), (".", 5)),
    R((".", 5), ("w1", 14), (".", 5)),
    R((".", 5), ("w0", 5), ("v", 4), ("w0", 5), (".", 5)),
]

# --- tubuh tergeletak (death 4-5) -------------------------------------------
PRONE = [
    R((".", 24)),
] * 19 + [
    R((".", 3), ("a2", 5), (".", 16)),
    R((".", 2), ("a1", 1), ("a3", 4), ("a1", 1), (".", 16)),
    R((".", 3), ("s2", 4), ("j1", 1), ("j3", 6), ("j2", 4), (".", 6)),
    R((".", 2), ("j1", 2), ("j3", 6), ("j2", 4), ("p2", 4), ("p1", 2), (".", 4)),
    R((".", 2), ("p1", 4), ("p2", 3), ("b1", 4), (".", 11)),
]


def legs(mat, hip_left, y_top, dx_l, lift_l, dx_r, lift_r, toe_l, toe_r):
    """Dua kaki 13 baris: paha 3 px, betis 2 px, sepatu 3 px.

    Jarak antar-hip 7 px dan lebar 3 px membuat pasangan kaki simetris tepat pada
    sumbu x=11,5 — sumbu cermin kanvas 24 px. Kalau tidak simetris, flip_h ke arah
    W/SW akan menggeser karakter 1 px dan jalannya terlihat pincang.

    Celah itu wajib: tanpa celah, dua kaki 3 px yang bersebelahan terbaca sebagai
    satu balok selebar 8 px, dan seluruh siluet kehilangan bentuk manusia.
    """
    for (hip, dx, lift, toe, inner) in ((hip_left, dx_l, lift_l, toe_l, 1),
                                        (hip_left + 7, dx_r, lift_r, toe_r, -1)):
        foot_y = FEET_Y - lift
        ankle_y = foot_y - 2
        knee_y = y_top + 5
        for y in range(y_top, ankle_y):
            if y <= knee_y:
                t = (y - y_top) / max(1, knee_y - y_top)
                xc = hip + dx * 0.3 * t
                w = 3
            else:
                t = (y - knee_y) / max(1, ankle_y - knee_y)
                xc = hip + dx * (0.3 + 0.7 * t)
                w = 2
            xc = int(round(xc))
            for k in range(w):
                edge = (inner > 0 and k == w - 1) or (inner < 0 and k == 0)
                tone = "p1" if edge else "p2"
                if k == 1 and w == 3:
                    tone = "p3"                      # highlight paha depan
                mat[(min(max(xc + k, 1), W - 2), y)] = tone
        # sepatu chunky: 4 px, sol 2 baris
        bx = int(round(hip + dx))
        for y in range(ankle_y, foot_y + 1):
            for k in range(4):
                x = min(max(bx - 1 + k, 1), W - 2)
                if y >= foot_y - 1:
                    mat[(x, y)] = "b0"
                elif y == ankle_y:
                    mat[(x, y)] = "b2"
                else:
                    mat[(x, y)] = "b1"
        if toe:
            tx = bx + 3 if toe > 0 else bx - 2
            mat[(min(max(tx, 1), W - 2), foot_y)] = "b0"
            mat[(min(max(tx, 1), W - 2), foot_y - 1)] = "b0"


def arms(mat, shoulder, dx, dy, ext, length, tone_edge, hand_row=None):
    """Lengan 3 px dengan siku; bahu -> siku -> pergelangan -> tangan."""
    sx, sy = shoulder
    hx = min(max(sx + dx + ext, 2), W - 3)
    hy = hand_row if hand_row else min(sy + dy + length, 26)
    ex, ey = (sx + hx) / 2.0, sy + (hy - sy) * 0.55
    for y in range(sy, hy + 1):
        if y <= ey:
            t = (y - sy) / max(1, ey - sy)
            xc = sx + (ex - sx) * t
        else:
            t = (y - ey) / max(1, hy - ey)
            xc = ex + (hx - ex) * t
        xc = int(round(xc))
        for k in range(3):
            ch = tone_edge if k == 0 else ("j3" if k == 1 and y < sy + 4 else "j2")
            if y >= hy:
                ch = "s1" if k == 1 else "s0"
            mat[(min(max(xc + k, 1), W - 2), y)] = ch


def build(d, anim, f):
    p = pose_state(anim, f)
    mat = {}
    if p["prone"]:
        for i, row in enumerate(PRONE):
            for x, ch in enumerate(row):
                if ch != ".":
                    mat[(x, i)] = ch
        return finish(mat)

    yb = 1 + p["bob"] + p["crouch"]
    lt = 20 + p["bob"] + p["crouch"]

    hip = 8 if d == "e" else 7
    legs(mat, hip, lt, p["legL"][0], p["legL"][1], p["legR"][0], p["legR"][1],
         1, 1 if d == "e" else 0)

    # lengan jauh (di belakang badan) untuk arah punggung/profil
    if d in ("e", "ne", "n"):
        arms(mat, (16 if d != "n" else 17, 10 + p["bob"] + p["crouch"]),
             p["armL"][0], p["armL"][1], 0, 11, "j0")

    for i, row in enumerate(BASE[d]):
        y = i + yb
        for x, ch in enumerate(row):
            if ch != ".":
                mat[(x, y)] = ch

    if d == "e":
        arms(mat, (15, 10 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
             p["ext"], 11, "j0")
    elif d == "n":
        arms(mat, (5, 10 + p["bob"] + p["crouch"]), p["armL"][0], p["armL"][1], 0, 11, "j0")
        arms(mat, (16, 10 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
             p["ext"], 11, "j0")
    else:
        arms(mat, (3, 10 + p["bob"] + p["crouch"]), p["armL"][0], p["armL"][1], 0, 11, "j0")
        arms(mat, (18, 10 + p["bob"] + p["crouch"]), p["armR"][0], p["armR"][1],
             p["ext"], 11, "j1")

    return finish(mat)


def finish(mat):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for (x, y), ch in mat.items():
        c = PAL.get(ch)
        if c:
            px[x, y] = (c[0], c[1], c[2], 255)
    filled = set(mat.keys())
    for (x, y) in filled:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in filled:
                px[nx, ny] = OUTLINE
    return img


# ------------------------------------------------------------------ pose ----

def pose_state(anim, f):
    p = dict(bob=0, crouch=0, legL=(0, 0), legR=(0, 0),
             armL=(0, 0), armR=(0, 0), ext=0, prone=False)
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
            dict(armR=(-2, -1), ext=-3),
            dict(armR=(1, -2), ext=6, bob=1),
            dict(armR=(1, -1), ext=5),
            dict(armR=(0, 0), ext=0),
        ][f])
    elif anim == "attack_ranged":
        p.update([
            dict(armR=(2, -2), ext=3),
            dict(armR=(0, -2), ext=2, bob=1),
            dict(armR=(2, -2), ext=3),
        ][f])
    elif anim == "hurt":
        p.update([dict(legL=(1, 0)), dict(legL=(1, 1))][f])
    elif anim == "death":
        p.update([
            dict(bob=1), dict(crouch=3), dict(crouch=6), dict(crouch=10),
            dict(prone=True), dict(prone=True),
        ][f])
    elif anim == "dodge":
        p.update([
            dict(crouch=2), dict(crouch=9), dict(crouch=9), dict(crouch=1),
        ][f])
    elif anim == "interact":
        p.update([
            dict(armR=(1, 2), ext=2),
            dict(armR=(2, 3), ext=3),
            dict(armR=(1, 2), ext=2),
        ][f])
    return p


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
    col, empty, edges, top = 0, 0, 0, 0
    for (name, count, fps) in ANIMS:
        for r in range(len(DIRS5)):
            for i in range(count):
                px = atlas.crop(((col + i) * W, r * H, (col + i) * W + W,
                                 r * H + H)).load()
                filled = [(x, y) for y in range(H) for x in range(W) if px[x, y][3]]
                if not filled:
                    empty += 1
                content = [(x, y) for (x, y) in filled if px[x, y][:3] != OUTLINE[:3]]
                if any(x in (0, W - 1) for x, _ in content):
                    edges += 1
                if any(y == 0 for _, y in content):
                    top += 1
        col += count
    print(f"  sel {W}x{H}          : {sum(a[1] for a in ANIMS) * 5}")
    print(f"  sel kosong         : {empty}")
    print(f"  isi menyentuh tepi : {edges}")
    print(f"  isi di baris 0     : {top}")
    print(f"  HASIL              : {'LULUS' if not (empty or edges or top) else 'GAGAL'}")


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    atlas = build_atlas()
    out = os.path.join(root, "game", "assets", "sprites", "player.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    atlas.save(out)
    print(f"atlas {atlas.width}x{atlas.height} -> {out}")
    validate(atlas)
    sheet(root, atlas)


def sheet(root, atlas):
    S = 8
    cw, ch = W * S, H * S
    cols = sum(a[1] for a in ANIMS)
    pad_l, pad_t = 80, 40
    prev = Image.new("RGBA", (pad_l + cols * cw + 16, pad_t + 5 * ch + 40), (22, 24, 28, 255))
    d = ImageDraw.Draw(prev)
    try:
        bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except Exception:
        bold = small = ImageFont.load_default()
    d.text((12, 10), "PLAYER v3 — 24x32 · 150 frame digambar · pivot (12,31)",
           font=bold, fill=(232, 234, 238, 255))
    c = 0
    for (name, count, fps) in ANIMS:
        d.text((pad_l + c * cw + 2, 26), f"{name} {count}f", font=small,
               fill=(96, 200, 176, 255))
        c += count
    for r, dn in enumerate(DIRS5):
        y = pad_t + r * ch
        d.text((12, y + ch // 2 - 8), dn.upper(), font=bold, fill=(198, 208, 218, 255))
        c = 0
        for (name, count, fps) in ANIMS:
            for i in range(count):
                cell = atlas.crop(((c + i) * W, r * H, (c + i) * W + W, r * H + H))
                prev.alpha_composite(cell.resize((cw, ch), Image.NEAREST),
                                     (pad_l + (c + i) * cw, y))
                d.rectangle([pad_l + (c + i) * cw, y,
                             pad_l + (c + i) * cw + cw - 1, y + ch - 1],
                            outline=(44, 48, 56, 255))
            c += count
    path = os.path.join(root, "docs", "art", "player-sheet-final.png")
    prev.save(path)
    print(f"sheet -> {path}")


if __name__ == "__main__":
    main()

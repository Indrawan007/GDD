#!/usr/bin/env python3
"""Generator aset greybox untuk prototipe Godot (The End Has Come).

Mengikuti kontrak proyeksi §17.12:
  tile 16×16 · muka dinding 10 px · shadow 32×14 alpha 45% · karakter 16×24 pivot (8,23)

Jalankan: python3 tools/make_greybox_assets.py
Output:   game/assets/generated/
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "game", "assets", "generated")

# Palet 32 warna (subset) — sengaja "greybox", bukan seni final
FLOOR_A = (58, 62, 66)
FLOOR_B = (52, 56, 60)
FLOOR_LINE = (44, 47, 50)
WALL_TOP = (96, 88, 78)
WALL_FACE = (74, 66, 58)
WALL_EDGE = (34, 31, 28)
PLAYER_BODY = (78, 160, 150)
PLAYER_DARK = (46, 104, 98)
PLAYER_ACCENT = (240, 210, 120)
CRATE = (128, 100, 60)
CRATE_EDGE = (72, 56, 32)
BAG = (150, 120, 70)


def ensure_out() -> None:
    os.makedirs(OUT, exist_ok=True)


# --------------------------------------------------------------------------
# Tile
# --------------------------------------------------------------------------
def make_floor(variant: int) -> Image.Image:
    img = Image.new("RGBA", (16, 16), FLOOR_A if variant == 0 else FLOOR_B)
    d = ImageDraw.Draw(img)
    d.line([0, 0, 15, 0], fill=FLOOR_LINE)
    d.line([0, 0, 0, 15], fill=FLOOR_LINE)
    if variant == 1:
        d.point([(4, 5), (9, 11), (12, 3), (6, 13)], fill=(70, 74, 78))
    return img


def make_wall() -> Image.Image:
    """Satu tile dinding: 0–6 px permukaan atas, 6–16 px muka (10 px)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 5], fill=WALL_TOP)      # top surface 6 px
    d.rectangle([0, 6, 15, 15], fill=WALL_FACE)    # face 10 px
    d.line([0, 5, 15, 5], fill=WALL_EDGE)          # batas top/face
    d.line([0, 15, 15, 15], fill=WALL_EDGE)        # dasar
    # GOAL 3/4: setiap kotak punya kontur vertikal tipis pada kedua tepi samping
    d.line([0, 6, 0, 15], fill=WALL_EDGE)
    d.line([15, 6, 15, 15], fill=WALL_EDGE)
    # bata: garis horizontal tipis di muka dinding
    d.line([1, 10, 14, 10], fill=(66, 58, 51))
    return img


def make_roof() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (36, 38, 42, 255))
    d = ImageDraw.Draw(img)
    for x in range(0, 16, 4):
        d.line([x, 0, x, 15], fill=(32, 34, 38, 255))
    return img


def make_shadow() -> Image.Image:
    """32×14 ellipse, alpha 45% (kontrak §17.12). Satu lapis + halo tipis."""
    img = Image.new("RGBA", (32, 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1, 1, 30, 12], fill=(0, 0, 0, 40))        # halo
    d.ellipse([4, 3, 27, 10], fill=(0, 0, 0, 115))       # inti = alpha 45%
    return img


def make_crate() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([1, 3, 14, 15], fill=CRATE, outline=CRATE_EDGE)
    d.line([1, 7, 14, 7], fill=CRATE_EDGE)
    d.line([7, 3, 7, 15], fill=CRATE_EDGE)
    return img


def make_bag() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([3, 7, 12, 14], fill=BAG, outline=(80, 62, 34))
    d.ellipse([6, 4, 9, 7], fill=(80, 62, 34))
    return img


# --------------------------------------------------------------------------
# Player: 30 kolom × 8 baris, 16×24 per sel (§17.3)
# --------------------------------------------------------------------------
COLS = 30
ROWS = 8
DIRS = ["S", "SE", "E", "NE", "N"]          # baris 0–4 digambar
ANIM = [("idle", 2), ("walk", 6), ("attack_melee", 4), ("attack_ranged", 3),
        ("hurt", 2), ("death", 6), ("dodge", 4), ("interact", 3)]


def frame_index(anim: str, local: int) -> int:
    i = 0
    for name, count in ANIM:
        if name == anim:
            return i + local
        i += count
    return 0


def draw_player_cell(img: Image.Image, cell: tuple[int, int], row: int,
                     anim: str, local: int) -> None:
    x0, y0 = cell[0] * 16, cell[1] * 24
    d = ImageDraw.Draw(img)

    # pose
    bob = 0
    fall = 0
    leg_spread = 0
    if anim == "walk":
        bob = [0, -1, 0, 1, 0, -1][local % 6]
        leg_spread = [2, 3, 2, 0, 1, 2][local % 6]
    elif anim == "dodge":
        fall = local * 2
    elif anim == "death":
        fall = min(local * 3, 14)
    elif anim == "hurt":
        bob = 1

    # shadow (bagian dari sprite? tidak — shadow node terpisah. di sini tidak digambar)
    body_top = y0 + 4 + bob + fall
    body_bottom = y0 + 21
    if fall:
        # jatuh: badan jadi horizontal
        d.rectangle([x0 + 3, y0 + 17 - fall // 2, x0 + 13, y0 + 21 - fall // 2],
                    fill=PLAYER_BODY, outline=PLAYER_DARK)
    else:
        d.rounded_rectangle([x0 + 4, body_top, x0 + 11, body_bottom],
                            radius=2, fill=PLAYER_BODY, outline=PLAYER_DARK)
        # kaki
        d.line([x0 + 6, body_bottom, x0 + 6 - leg_spread, y0 + 23],
               fill=PLAYER_DARK, width=2)
        d.line([x0 + 9, body_bottom, x0 + 9 + leg_spread, y0 + 23],
               fill=PLAYER_DARK, width=2)

    # penanda arah hadap (biar 8 arah terbaca di greybox)
    cx, cy = x0 + 8, y0 + 6 + bob
    if not fall:
        if row == 0:      # S
            d.point([(cx, cy + 4), (cx - 1, cy + 5), (cx + 1, cy + 5)], fill=PLAYER_ACCENT)
        elif row == 1:    # SE
            d.point([(cx + 3, cy + 3), (cx + 4, cy + 4), (cx + 3, cy + 5)], fill=PLAYER_ACCENT)
        elif row == 2:    # E
            d.rectangle([cx + 3, cy + 3, cx + 4, cy + 5], fill=PLAYER_ACCENT)
        elif row == 3:    # NE
            d.point([(cx + 3, cy - 1), (cx + 4, cy), (cx + 3, cy + 1)], fill=PLAYER_ACCENT)
        else:             # N
            d.point([(cx, cy - 2), (cx - 1, cy - 3), (cx + 1, cy - 3)], fill=PLAYER_ACCENT)


def make_player_sheet() -> Image.Image:
    img = Image.new("RGBA", (COLS * 16, ROWS * 24), (0, 0, 0, 0))
    for row in range(len(DIRS)):
        for anim, count in ANIM:
            for local in range(count):
                col = frame_index(anim, local)
                draw_player_cell(img, (col, row), row, anim, local)
    # baris 5–7 (NW, W, SW) dibiarkan transparan: MIRROR di runtime
    return img



# --------------------------------------------------------------------------
# Walker: 16 kolom × 8 baris (idle2, walk4, attack4, hurt1, death5)
# --------------------------------------------------------------------------
WALKER_COLS = 16
WALKER_ANIM = [("idle", 2), ("walk", 4), ("attack", 4), ("hurt", 1), ("death", 5)]
Z_BODY = (120, 132, 96)
Z_DARK = (74, 84, 58)
Z_ACCENT = (170, 60, 60)


def walker_frame_index(anim: str, local: int) -> int:
    i = 0
    for name, count in WALKER_ANIM:
        if name == anim:
            return i + local
        i += count
    return 0


def draw_walker_cell(img: Image.Image, col: int, row: int, anim: str, local: int) -> None:
    x0, y0 = col * 16, row * 24
    d = ImageDraw.Draw(img)
    hunch = 3 if row in (0, 1, 2) else 1          # bungkuk lebih terlihat dari depan
    sway = 1 if (anim == "walk" and local % 2 == 1) else 0
    fall = 0
    if anim == "death":
        fall = min(local * 3, 14)
    if anim == "attack":
        sway = 2 if local % 2 == 0 else -1

    if fall:
        d.rectangle([x0 + 2, y0 + 18 - fall // 2, x0 + 13, y0 + 22 - fall // 2],
                    fill=Z_BODY, outline=Z_DARK)
        return

    top = y0 + 6 + hunch
    bottom = y0 + 21
    d.rounded_rectangle([x0 + 4 + sway, top, x0 + 11 + sway, bottom],
                        radius=3, fill=Z_BODY, outline=Z_DARK)
    # kepala lebih rendah & kecil = siluet zombie
    d.rectangle([x0 + 5 + sway, top - 3, x0 + 10 + sway, top + 2], fill=Z_DARK)
    # tangan menjuntai
    d.line([x0 + 4 + sway, top + 4, x0 + 1 + sway, top + 10], fill=Z_DARK, width=2)
    d.line([x0 + 11 + sway, top + 4, x0 + 14 - sway, top + 10], fill=Z_DARK, width=2)
    # kaki
    d.line([x0 + 6, bottom, x0 + 5, y0 + 23], fill=Z_DARK, width=2)
    d.line([x0 + 9, bottom, x0 + 10, y0 + 23], fill=Z_DARK, width=2)
    # mata (telegraph arah sedikit)
    d.point([(x0 + 7 + sway, top - 1), (x0 + 9 + sway, top - 1)], fill=Z_ACCENT)


def make_walker_sheet() -> Image.Image:
    img = Image.new("RGBA", (WALKER_COLS * 16, ROWS * 24), (0, 0, 0, 0))
    for row in range(len(DIRS)):
        for anim, count in WALKER_ANIM:
            for local in range(count):
                draw_walker_cell(img, walker_frame_index(anim, local), row, anim, local)
    return img


# --------------------------------------------------------------------------
def main() -> None:
    ensure_out()
    make_floor(0).save(os.path.join(OUT, "floor_a.png"))
    make_floor(1).save(os.path.join(OUT, "floor_b.png"))
    make_wall().save(os.path.join(OUT, "wall.png"))
    make_roof().save(os.path.join(OUT, "roof.png"))
    make_shadow().save(os.path.join(OUT, "shadow.png"))
    make_crate().save(os.path.join(OUT, "crate.png"))
    make_bag().save(os.path.join(OUT, "bag.png"))
    make_player_sheet().save(os.path.join(OUT, "player.png"))
    make_walker_sheet().save(os.path.join(OUT, "walker.png"))

    for f in sorted(os.listdir(OUT)):
        if f.endswith(".png"):
            with Image.open(os.path.join(OUT, f)) as im:
                print(f"  {f:16s} {im.size[0]:>4}×{im.size[1]:<4} {im.mode}")


if __name__ == "__main__":
    main()

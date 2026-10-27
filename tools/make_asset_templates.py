#!/usr/bin/env python3
"""Generator lembar template sprite untuk "The End Has Come".

Menghasilkan dua jenis berkas untuk tiap lembar:
  *-guide.png  : lembar berlabel (untuk dibaca manusia / brief ke artist)
  *-1x.png     : kanvas bersih ukuran final (untuk digambar di Aseprite)

Jalankan:  python3 tools/make_asset_templates.py
Output:    docs/art/
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "art")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = (30, 30, 30)
CELL = (42, 42, 42)
GRID = (62, 62, 62)
TEXT = (232, 232, 232)
DIM = (150, 150, 150)
ACCENT = (232, 176, 75)
PIVOT = (78, 201, 176)
GROUP = (92, 132, 168)
WARN = (214, 107, 107)
MIRROR_BG = (46, 40, 34)
MIRROR_LINE = (110, 84, 56)


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


@dataclass
class Group:
    name: str
    frames: int
    fps: str
    note: str = ""


def draw_sheet(
    path: str,
    title: str,
    subtitle: str,
    cell_w: int,
    cell_h: int,
    groups: list[Group],
    rows: list[tuple[str, str, str | None]],
    pivot: tuple[int, int] | None,
    footers: list[str],
    scale: int = 4,
) -> None:
    cols = sum(g.frames for g in groups)
    cw, ch = cell_w * scale, cell_h * scale

    margin = 48
    title_h = 108
    head_h = 92
    label_w = 150
    footer_h = 40 * len(footers) + 28

    grid_w = label_w + cols * cw
    height = margin * 2 + title_h + head_h + len(rows) * ch + footer_h

    # lebar harus mengakomodasi teks terpanjang (judul/subjudul/footer)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    text_w = max(
        probe.textlength(title, font=font(34, True)),
        probe.textlength(subtitle, font=font(19)),
        probe.textlength(
            f"sel {cell_w}×{cell_h} px  ·  {cols} kolom  ·  {len(rows)} baris  ·  "
            f"kanvas bersih: {cols * cell_w}×{len(rows) * cell_h} px",
            font=font(18),
        ),
        *[probe.textlength(f.lstrip("!"), font=font(17)) for f in footers],
    )
    width = int(max(margin * 2 + grid_w, margin * 2 + text_w))

    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)

    # --- judul -------------------------------------------------------------
    d.text((margin, margin), title, font=font(34, True), fill=TEXT)
    d.text((margin, margin + 46), subtitle, font=font(19), fill=DIM)
    d.text(
        (margin, margin + 72),
        f"sel {cell_w}×{cell_h} px  ·  {cols} kolom  ·  {len(rows)} baris  ·  "
        f"kanvas bersih: {cols * cell_w}×{len(rows) * cell_h} px",
        font=font(18),
        fill=ACCENT,
    )

    grid_top = margin + title_h + head_h

    # --- header grup animasi ----------------------------------------------
    def fit(text: str, max_w: int, size: int, bold: bool = False) -> str:
        f = font(size, bold)
        while text and d.textlength(text, font=f) > max_w:
            text = text[:-1]
        return text

    x = margin + label_w
    for g in groups:
        w = g.frames * cw
        top_h = grid_top - head_h
        d.rectangle([x + 2, top_h + 8, x + w - 4, grid_top - 8], outline=GROUP, width=2)
        inner = w - 20
        d.text((x + 10, top_h + 16), fit(g.name, inner, 19, True), font=font(19, True), fill=TEXT)
        d.text((x + 10, top_h + 42), fit(f"{g.frames}f · {g.fps}", inner, 15), font=font(15), fill=ACCENT)
        if g.note:
            d.text((x + 10, top_h + 62), fit(g.note, inner, 13), font=font(13), fill=DIM)
        d.line([x, top_h + 8, x, grid_top + len(rows) * ch], fill=GROUP, width=2)
        x += w
    d.line([x, grid_top - head_h + 8, x, grid_top + len(rows) * ch], fill=GROUP, width=2)

    # --- pola untuk baris mirror (dibuat sekali) ---------------------------
    hatch = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hatch)
    for k in range(-ch, cw, 22):
        hd.line([k, ch, k + ch, 0], fill=(*MIRROR_LINE, 90), width=2)

    # --- baris ------------------------------------------------------------
    for r, (row_name, row_note, mirror_src) in enumerate(rows):
        y = grid_top + r * ch

        d.text((margin, y + ch // 2 - 26), row_name, font=font(26, True), fill=TEXT)
        if row_note:
            d.text((margin, y + ch // 2 + 2), fit(row_note, label_w - 22, 13), font=font(13), fill=DIM)

        x = margin + label_w
        idx = 0
        for g in groups:
            for _ in range(g.frames):
                if mirror_src:
                    d.rectangle([x, y, x + cw - 2, y + ch - 2], fill=MIRROR_BG, outline=GRID)
                    img.paste(hatch, (x, y), hatch)   # pola diagonal "jangan digambar"
                    if idx % 4 == 0:
                        d.text((x + 6, y + ch // 2 - 8), "MIRROR", font=font(13, True),
                               fill=(126, 96, 62))
                else:
                    d.rectangle([x, y, x + cw - 2, y + ch - 2], fill=CELL, outline=GRID)
                    d.text((x + 5, y + 3), str(idx), font=font(12), fill=(110, 110, 110))
                    if pivot is not None:
                        px, py = x + pivot[0] * scale, y + pivot[1] * scale
                        d.line([px - 6, py, px + 6, py], fill=PIVOT, width=2)
                        d.line([px, py - 6, px, py - 2], fill=PIVOT, width=2)
                x += cw
                idx += 1
            # pemisah grup
            d.line([x - 1, y, x - 1, y + ch - 2], fill=GROUP, width=3)

    # garis bawah baris terakhir
    d.line([margin + label_w, grid_top + len(rows) * ch, margin + label_w + cols * cw,
            grid_top + len(rows) * ch], fill=GRID, width=2)

    # --- footer -----------------------------------------------------------
    fy = grid_top + len(rows) * ch + 24
    for line in footers:
        color = WARN if line.startswith("!") else DIM
        d.text((margin, fy), line.lstrip("!"), font=font(17), fill=color)
        fy += 40

    os.makedirs(OUT, exist_ok=True)
    img.save(path)


def save_clean_1x(path: str, cols: int, rows: int, cell_w: int, cell_h: int) -> None:
    """Kanvas transparan ukuran final, tanpa grid — untuk digambar."""
    img = Image.new("RGBA", (cols * cell_w, rows * cell_h), (0, 0, 0, 0))
    os.makedirs(OUT, exist_ok=True)
    img.save(path)


def draw_tileset(path: str, scale: int = 3) -> None:
    """Peta atlas tileset 32×32 sel (512×512 px)."""
    cells = 32
    cell = 16 * scale
    margin = 48
    title_h = 150
    w = margin * 2 + cells * cell
    h = margin * 2 + title_h + cells * cell + 280

    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)

    d.text((margin, margin), "THE END HAS COME — PETA ATLAS TILESET", font=font(32, True), fill=TEXT)
    d.text((margin, margin + 44), "1 atlas 512×512 px = 32×32 sel tile 16×16 (1024 tile)",
           font=font(19), fill=DIM)
    d.text((margin, margin + 72), "Proyeksi: TOP-DOWN 3/4 — dinding punya muka 10px. Prop di atlas bersama.",
           font=font(17), fill=ACCENT)
    d.text((margin, margin + 100), "Isi per distrik ±285 tile (termasuk wall face 3/4); sisa sel = reserve",
           font=font(17), fill=DIM)

    top = margin + title_h

    regions = [
        # nama, col, row, cols, rows, warna, catatan
        ("GROUND BLOB A (47)", 0, 0, 24, 2, (58, 92, 62), "rumput/material utama"),
        ("GROUND BLOB B (47)", 0, 2, 24, 2, (56, 78, 96), "material kedua"),
        ("GROUND BLOB C (47)", 0, 4, 24, 2, (92, 74, 52), "material ketiga"),
        ("SIDEWALK (16)", 0, 6, 16, 1, (86, 86, 92), "Match Sides"),
        ("WALL TOP EXTERIOR (47)", 0, 7, 24, 2, (104, 74, 58), "permukaan atas dinding"),
        ("WALL FACE (24)", 0, 9, 24, 1, (128, 92, 66), "muka 10px: depan, sudut, ujung"),
        ("WALL TOP INTERIOR (47)", 0, 10, 24, 1, (74, 84, 104), "permukaan atas dinding dalam"),
        ("LOW WALL / RAIL (16)", 0, 11, 16, 1, (88, 96, 110), "muka 6px, bisa dilewati peluru"),
        ("ROOF (15)", 0, 12, 15, 1, (108, 96, 72), "di-fade saat pemain masuk"),
        ("DOOR (12)", 16, 12, 12, 1, (140, 96, 48), "3 material × 4 state"),
        ("WINDOW (8)", 0, 13, 8, 1, (72, 112, 140), "2 material × 4 state"),
        ("STAIRS (4)", 8, 13, 4, 1, (100, 100, 100), "naik/turun × 2 arah"),
        ("DECO FLOOR (20)", 12, 13, 20, 1, (84, 68, 84), "karpet, retak, darah kering"),
        ("RESERVE", 0, 14, 32, 18, (46, 46, 46), "jangan dipakai sebelum 5 distrik selesai"),
    ]

    for name, cx, cy, cw_, ch_, color, note in regions:
        x0, y0 = margin + cx * cell, top + cy * cell
        x1, y1 = x0 + cw_ * cell, y0 + ch_ * cell
        d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=color, outline=(20, 20, 20), width=2)
        d.text((x0 + 8, y0 + 6), name, font=font(16, True), fill=(250, 250, 250))
        d.text((x0 + 8, y0 + 28), note, font=font(13), fill=(228, 228, 228))

    # grid sel
    for i in range(cells + 1):
        x = margin + i * cell
        d.line([x, top, x, top + cells * cell], fill=(255, 255, 255, 40), width=1)
        y = top + i * cell
        d.line([margin, y, margin + cells * cell, y], fill=(255, 255, 255, 40), width=1)

    # legend
    ly = top + cells * cell + 24
    legend = [
        "ATURAN: 1 atlas = 1 texture = 1 draw call per distrik. Jangan pecah jadi banyak PNG kecil.",
        "!JANGAN menaruh detail penting di 1 piksel tile — hilang saat di-scale ke 1280×720.",
        "!Collision HANYA di layer wall; ground tidak punya collision.",
        "Pintu & jendela = objek berstate (4 state), bukan tile statis.",
        "Layer TileMapLayer terpisah: ground / wall / roof / deco / props.",
        "Import Godot: Filter OFF · Mipmap OFF · Compress Lossless · Fix Alpha Border ON.",
    ]
    for line in legend:
        color = WARN if line.startswith("!") else DIM
        d.text((margin, ly), line.lstrip("!"), font=font(17), fill=color)
        ly += 36

    os.makedirs(OUT, exist_ok=True)
    img.save(path)



def draw_projection_sheet(path: str) -> None:
    """Lembar spesifikasi proyeksi Top-Down 3/4 (dikunci)."""
    scale = 10
    W, H = 1680, 1500
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((56, 40), "PROYEKSI — TOP-DOWN 3/4 (DIKUNCI)", font=font(34, True), fill=TEXT)
    d.text((56, 84), "The End Has Come · tile 16×16 · tanpa rotasi kamera · tanpa perspective scaling",
           font=font(19), fill=DIM)
    d.text((56, 112), "Setiap aset & tile HARUS mengikuti angka di halaman ini.",
           font=font(18), fill=ACCENT)

    # ---------- A: anatomi tile dinding ----------
    ax, ay = 56, 190
    d.text((ax, ay), "A. SATU TILE DINDING (16×16 px)", font=font(20, True), fill=TEXT)
    tile = 16 * scale
    tx, ty = ax, ay + 40
    d.rectangle([tx, ty, tx + tile, ty + tile], fill=(104, 74, 58), outline=(20, 20, 20), width=2)
    d.rectangle([tx, ty + 6 * scale, tx + tile, ty + tile], fill=(128, 92, 66), outline=(20, 20, 20), width=1)
    d.line([tx, ty + 6 * scale, tx + tile, ty + 6 * scale], fill=(240, 200, 120), width=3)
    lx = tx + tile + 20
    d.text((lx, ty + 2), "0–6 px — permukaan atas", font=font(16, True), fill=ACCENT)
    d.text((lx, ty + 24), "(top surface, terlihat dari atas)", font=font(14), fill=DIM)
    d.text((lx, ty + 6 * scale + 2), "6–16 px — muka dinding", font=font(16, True), fill=ACCENT)
    d.text((lx, ty + 6 * scale + 24), "(face, 10 px: inilah yang memberi rasa tinggi)", font=font(14), fill=DIM)

    # ---------- B: penampang ----------
    bx, by = 760, 190
    d.text((bx, by), "B. PENAMPANG BANGUNAN (potongan samping)", font=font(20, True), fill=TEXT)
    cx, cy = bx + 10, by + 46
    bw = 340
    d.rectangle([cx, cy, cx + bw, cy + 26], fill=(108, 96, 72), outline=(20, 20, 20), width=2)
    d.rectangle([cx, cy + 26, cx + bw, cy + 96], fill=(128, 92, 66), outline=(20, 20, 20), width=2)
    d.rectangle([cx, cy + 96, cx + bw, cy + 170], fill=(70, 70, 74), outline=(20, 20, 20), width=2)
    # karakter + shadow berdiri di lantai
    px, py = cx + 250, cy + 170
    d.ellipse([px - 16, py - 7, px + 16, py + 7], fill=(30, 30, 30))
    d.rectangle([px - 7, py - 34, px + 7, py - 2], fill=(78, 160, 150), outline=(10, 10, 10))
    # keterangan di bawah gambar
    ly = cy + 190
    for label, color in [
        ("ATAP — alpha 0,25–0,35 saat pemain di dalam bangunan", (240, 232, 200)),
        ("MUKA DINDING — 10 px eksterior / 6 px low wall interior", (250, 240, 220)),
        ("LANTAI — ground tile, tanpa collision", (215, 215, 215)),
        ("KARAKTER — kaki di baseline, shadow ellipse 32×14, offset (0, −2)", (160, 220, 210)),
    ]:
        d.text((bx, ly), label, font=font(15), fill=color)
        ly += 26

    # ---------- C: boleh vs jangan ----------
    gx, gy = 56, 560
    d.text((gx, gy), "C. BOLEH  vs  JANGAN", font=font(20, True), fill=TEXT)
    cell_w, cell_h = 600, 196
    gap_x, gap_y = 44, 22
    items = [
        ("BOLEH · karakter & prop punya shadow",
         "JANGAN · karakter mengambang tanpa shadow", "shadow"),
        ("BOLEH · dinding punya muka 10 px",
         "JANGAN · dinding digambar sebagai garis tipis", "face"),
        ("BOLEH · atap di-fade saat pemain masuk",
         "JANGAN · atap menutupi pemain (oklusi)", "roof"),
    ]
    for i, (ok_label, bad_label, kind) in enumerate(items):
        for j, good in enumerate((True, False)):
            x = gx + j * (cell_w + gap_x)
            y = gy + 40 + i * (cell_h + gap_y)
            border = (86, 150, 110) if good else (170, 86, 86)
            d.rectangle([x, y, x + cell_w, y + cell_h], fill=(36, 36, 36), outline=border, width=3)
            d.text((x + 12, y + 8), (ok_label if good else bad_label), font=font(15, True),
                   fill=(160, 220, 175) if good else (240, 170, 170))
            mx, my = x + 150, y + 70
            d.rectangle([mx, my, mx + 300, my + 100], fill=(52, 52, 56))
            if kind == "shadow":
                if good:
                    d.ellipse([mx + 132, my + 78, mx + 172, my + 92], fill=(24, 24, 24))
                d.rectangle([mx + 144, my + 40, mx + 160, my + 84], fill=(78, 160, 150), outline=(10, 10, 10))
            elif kind == "face":
                if good:
                    d.rectangle([mx + 40, my + 34, mx + 260, my + 50], fill=(104, 74, 58), outline=(10, 10, 10))
                    d.rectangle([mx + 40, my + 50, mx + 260, my + 84], fill=(128, 92, 66), outline=(10, 10, 10))
                else:
                    d.line([mx + 40, my + 62, mx + 260, my + 62], fill=(104, 74, 58), width=4)
            else:  # roof
                d.rectangle([mx + 40, my + 30, mx + 260, my + 96], fill=(70, 66, 60))
                d.rectangle([mx + 144, my + 44, mx + 160, my + 88], fill=(78, 160, 150))
                d.ellipse([mx + 132, my + 84, mx + 172, my + 96], fill=(24, 24, 24))
                if good:
                    overlay = Image.new("RGBA", (220, 66), (70, 66, 60, 170))
                    img.paste(overlay, (mx + 40, my + 30), overlay)

    # ---------- footer ----------
    fy = 560 + 40 + 3 * (cell_h + gap_y) + 26
    for line in [
        "DIKUNCI: tile 16×16 · tanpa rotasi kamera · tanpa perspective scaling (objek di atas TIDAK mengecil)",
        "Wall face 10 px (eksterior) / 6 px (low wall interior) · roof fade alpha 0,25–0,35 saat pemain di dalam",
        "Shadow ellipse 32×14, offset (0,−2), alpha 45% · y-sort key = kaki karakter (bukan tengah sprite)",
        "!Membuka kembali keputusan ini butuh greybox 2 hari + 5 tester + data — bukan opini atau screenshot.",
    ]:
        color = WARN if line.startswith("!") else DIM
        d.text((56, fy), line.lstrip("!"), font=font(16), fill=color)
        fy += 32

    os.makedirs(OUT, exist_ok=True)
    img.save(path)


def main() -> None:
    # ---------------- PLAYER ------------------------------------------------
    player_groups = [
        Group("IDLE", 2, "3 fps", "napas"),
        Group("WALK", 6, "8 fps", "12 = sprint"),
        Group("ATK MELEE", 4, "12 fps", "f2 hitbox"),
        Group("ATK RANGED", 3, "12 fps", "recoil"),
        Group("HURT", 2, "10 fps", "≤0,2s"),
        Group("DEATH", 6, "10 fps", "hold last"),
        Group("DODGE", 4, "14 fps", "roll"),
        Group("INTERACT", 3, "8 fps", "loot/pintu"),
    ]
    player_rows = [
        ("S", "depan", None),
        ("SE", "depan-kanan", None),
        ("E", "kanan", None),
        ("NE", "belakang-kanan", None),
        ("N", "belakang", None),
        ("NW", "mirror NE", "NE"),
        ("W", "mirror E", "E"),
        ("SW", "mirror SE", "SE"),
    ]
    draw_sheet(
        os.path.join(OUT, "player-sheet-guide.png"),
        "PLAYER — SPRITE SHEET TEMPLATE (8 ARAH)",
        "The End Has Come · 16×24 px per sel · 8 arah · 30 frame/arah = 240 frame di atlas · 150 frame digambar",
        cell_w=16,
        cell_h=24,
        groups=player_groups,
        rows=player_rows,
        pivot=(8, 23),
        footers=[
            "8 ARAH: gambar 5 baris saja (S, SE, E, NE, N). Baris NW/W/SW bertanda M = hasil MIRROR, JANGAN digambar.",
            "Pemetaan mirror: SE→SW · E→W · NE→NW. Runtime pakai flip_h + tabel arah, hemat 90 frame (37,5%).",
            "Pivot (8,23) = kaki di baseline (tanda + hijau). Collision 10×10 di kaki, BUKAN seluruh sprite.",
            "!Body menghadap arah GERAK (8 arah); senjata tetap berputar bebas ke arah kursor.",
            "!Nama animasi: walk_s, walk_se, walk_e, walk_ne, walk_n (+ flip). Arah di akhir nama.",
            "!Walk 6 frame dipakai juga untuk sprint (FPS 12). Jangan gambar animasi run terpisah.",
            "Varian survivor (3 warna) lewat palette swap ShaderMaterial — 0 frame tambahan.",
        ],
    )
    save_clean_1x(os.path.join(OUT, "player-sheet-1x.png"), cols=30, rows=8, cell_w=16, cell_h=24)

    # ---------------- ZOMBIE ------------------------------------------------
    zombie_groups = [
        Group("IDLE", 2, "3 fps", "kebingungan"),
        Group("WALK", 4, "6 fps", "pincang"),
        Group("ATTACK", 4, "10 fps", "f2 hitbox"),
        Group("HURT", 1, "—", "flinch"),
        Group("DEATH", 5, "8 fps", "hold last"),
    ]
    draw_sheet(
        os.path.join(OUT, "zombie-sheet-guide.png"),
        "ZOMBIE HUMANOID — SPRITE SHEET TEMPLATE (8 ARAH)",
        "Walker sebagai base body · 16×24 px · 8 arah · 16 frame/arah = 128 di atlas · 80 digambar",
        cell_w=16,
        cell_h=24,
        groups=zombie_groups,
        rows=[
            ("S", "depan", None),
            ("SE", "depan-kanan", None),
            ("E", "kanan", None),
            ("NE", "belakang-kanan", None),
            ("N", "belakang", None),
            ("NW", "mirror NE", "NE"),
            ("W", "mirror E", "E"),
            ("SW", "mirror SE", "SE"),
        ],
        pivot=(8, 23),
        footers=[
            "8 ARAH: gambar 5 baris (S, SE, E, NE, N); NW/W/SW = MIRROR (M). Pemetaan: SE→SW, E→W, NE→NW.",
            "BASE BODY + VARIAN: gambar 1 rig (walker), lalu varian hanya kepala/torso/aksesori.",
            "Runner · Spitter · Screamer · Exploder · Stalker memakai rig yang sama (± hemat 35%).",
            "Tank: canvas 24×32, animasi sama. The Hive: 48×48, 30 frame, bukan humanoid.",
            "!Bedakan tipe lewat SILUET (postur, tinggi, lebar), BUKAN warna — syarat buta warna.",
            "!Spitter +3 frame spit · Stalker +4 frame leap · Exploder 2 frame pulsing (telegraph).",
            "!Walk 4 frame, bukan 6. Jalan pincang justru lebih terbaca dengan 4 frame.",
        ],
    )
    save_clean_1x(os.path.join(OUT, "zombie-sheet-1x.png"), cols=16, rows=8, cell_w=16, cell_h=24)

    # ---------------- NPC ---------------------------------------------------
    npc_groups = [
        Group("IDLE", 2, "3 fps", "bernapas"),
        Group("TALK", 4, "8 fps", "saat buka dagangan"),
        Group("GESTURE", 2, "6 fps", "menunjuk"),
    ]
    draw_sheet(
        os.path.join(OUT, "npc-trader-sheet-guide.png"),
        "NPC TRADER — SPRITE SHEET TEMPLATE",
        "2 trader (Police Checkpoint & Commercial Market) · 16×24 px · 8 frame · menghadap S",
        cell_w=16,
        cell_h=24,
        groups=npc_groups,
        rows=[("S", "menghadap", None), ("E/W", "opsional", None)],
        pivot=(8, 23),
        footers=[
            "Trader statis di balik meja — TIDAK ada pathfinding, jadwal, atau dialog berjalan.",
            "Butuh 2 varian: pakaian & palet beda (petugas vs pedagang). Frame sama.",
            "Props trader (meja, tenda, kotak, papan harga) 16×32 — masuk atlas prop, bukan sheet ini.",
            "!NPC rasa (sosok statis di landmark) = 1 frame per sosok, ditunda ke pasca-launch (Q11).",
            "Menambah NPC yang bergerak = +4–6 minggu sistem baru. Belum di scope.",
        ],
    )
    save_clean_1x(os.path.join(OUT, "npc-trader-sheet-1x.png"), cols=8, rows=2, cell_w=16, cell_h=24)

    # ---------------- TILESET ----------------------------------------------
    draw_tileset(os.path.join(OUT, "tileset-atlas-map.png"))
    draw_projection_sheet(os.path.join(OUT, "projection-3q-spec.png"))

    print("selesai →", OUT)
    for f in sorted(os.listdir(OUT)):
        if not f.endswith(".png"):
            continue
        p = os.path.join(OUT, f)
        with Image.open(p) as im:
            print(f"  {f:34s} {im.size[0]:>5}×{im.size[1]:<5} {os.path.getsize(p) // 1024:>4} KB")


if __name__ == "__main__":
    main()

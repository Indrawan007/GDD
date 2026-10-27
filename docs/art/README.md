# Template Aset — The End Has Come

Lembar kerja sprite & tileset sesuai spesifikasi §17 GDD (v3.5).

## Berkas

| Berkas | Isi | Untuk siapa |
|--------|-----|-------------|
| `player-sheet-guide.png` | Lembar berlabel: 30 kolom × 4 baris, pivot, nama animasi, FPS | Brief ke artist / referensi |
| `player-sheet-1x.png` | Kanvas transparan 480×96 px, ukuran final | Digambar di Aseprite |
| `zombie-sheet-guide.png` | Base body walker: 16 kolom × 4 baris | Brief ke artist |
| `zombie-sheet-1x.png` | Kanvas transparan 256×96 px | Digambar di Aseprite |
| `npc-trader-sheet-guide.png` | Trader: 8 kolom × 2 baris | Brief ke artist |
| `npc-trader-sheet-1x.png` | Kanvas transparan 128×48 px | Digambar di Aseprite |
| `tileset-atlas-map.png` | Peta atlas 32×32 sel (512×512 px) + pembagian region | Brief ke artist |

## Aturan pakai

1. **Sel = 16×24 px** untuk semua karakter. Jangan mengubah ukuran sel; semua kode animasi mengasumsikan grid ini.
2. **Pivot `(8, 23)`** — 1 px di atas tepi bawah sel. Tanda `+` hijau di lembar guide menunjuk titik ini. Kaki karakter menyentuh baseline.
3. **Baris `W` (barat) boleh dikosongkan.** Prototipe memakai `flip_h` pada baris `E`. Hemat 25–30 frame per karakter.
4. **Nama animasi di `SpriteFrames`:** `walk_s`, `walk_n`, `walk_e`, `attack_melee_s`, `death_e` — arah di **akhir** nama.
5. **Satu atlas PNG per karakter**, bukan satu file per frame.
6. Grid di lembar `guide` hanya penanda. Yang digambar adalah `*-1x.png` (tanpa grid, transparan).

## Urutan kolom (jangan diubah)

Agar region bisa dihitung dengan rumus, urutan frame per baris adalah:

```text
PLAYER  (30 kolom): idle 0-1 · walk 2-7 · attack_melee 8-11 · attack_ranged 12-14
                    hurt 15-16 · death 17-22 · dodge 23-26 · interact 27-29

ZOMBIE  (16 kolom): idle 0-1 · walk 2-5 · attack 6-9 · hurt 10 · death 11-15
                    (Spitter +3 spit, Stalker +4 leap → sheet terpisah 20 kolom)

NPC     ( 8 kolom): idle 0-1 · talk 2-5 · gesture 6-7
```

Rumus region di Godot: `Rect2(kolom × 16, baris × 24, 16, 24)`.

## Import Godot 4.4

```
Filter: OFF · Mipmap: OFF · Compress: Lossless · Fix Alpha Border: ON
AnimatedSprite2D → SpriteFrames → tambah frame dari atlas
  Horizontal: jumlah frame per animasi   Vertical: 1
```

## Regenerate

Semua lembar dibuat oleh script — ubah angka di satu tempat, jangan gambar ulang manual:

```bash
python3 tools/make_asset_templates.py
```

Butuh `pillow` (`pip install pillow`). Font: DejaVu Sans Mono.

# Template Aset — The End Has Come

Lembar kerja sprite & tileset sesuai spesifikasi §17 GDD (v3.8) — **proyeksi Top-Down 3/4 (dikunci)** dan **8 arah** (5 baris digambar + 3 mirror).

## Berkas

| Berkas | Isi | Untuk siapa |
|--------|-----|-------------|
| `player-sheet-guide.png` | Lembar berlabel: 30 kolom × 8 baris, pivot, nama animasi, FPS | Brief ke artist / referensi |
| `player-sheet-1x.png` | Kanvas transparan **480×192 px**, ukuran final | Digambar di Aseprite |
| `zombie-sheet-guide.png` | Base body walker: 16 kolom × 8 baris | Brief ke artist |
| `zombie-sheet-1x.png` | Kanvas transparan **256×192 px** | Digambar di Aseprite |
| `npc-trader-sheet-guide.png` | Trader: 8 kolom × 2 baris | Brief ke artist |
| `npc-trader-sheet-1x.png` | Kanvas transparan 128×48 px | Digambar di Aseprite |
| `tileset-atlas-map.png` | Peta atlas 32×32 sel (512×512 px) + pembagian region, termasuk wall face | Brief ke artist |
| `projection-3q-spec.png` | **Kontrak proyeksi**: anatomi tile dinding, penampang, BOLEH vs JANGAN | Wajib dibaca sebelum menggambar apa pun |
| **`player-character-sheet.png`** | **SET FINAL v1**: turnaround 5 arah, palet 26 warna, catatan produksi | Acuan gaya untuk semua karakter lain |
| **`player-sheet-final.png`** | **SET FINAL v1**: 150 frame berlabel, 6× zoom | Review animasi per frame |
| **`player-walk-preview.gif`** | Walk cycle 5 arah, 8× zoom | Cek ritme jalan |
| **`ingame-scale-check.png`** | Karakter di layar 320×180 (4×): shadow 32×14 vs 14×7 | Bukti koreksi shadow §17.12 |
| **`game/assets/sprites/player.png`** | Atlas final 480×120 (30 kolom × 5 baris), dipakai engine | File yang dibaca `SpriteFactory` |

## Set final v1 — sudah ada, bukan template lagi

Pemain sudah punya set lengkap: **150 frame digambar** (30 frame × 5 arah), digenerate oleh `tools/make_player_sprites.py`, dan engine memakainya (`SpriteFactory.player_frames()`).

| Keputusan | Nilai | Alasan |
|---|---|---|
| Arah cahaya | **dari atas**, bukan kiri-atas | Baris E/SE dipakai juga sebagai W/SW lewat `flip_h`. Cahaya dari kiri akan terbalik saat mirror dan terbaca sebagai karakter lain. |
| Kepala | 6 px (bahu 8 px, rasio 0,75) | Wajah 5 px hanya menyisakan 1 px di antara mata → terbaca seperti topeng. |
| Tangan & sepatu | nada lebih terang dari lengan/kaki | Menandai ujung anggota badan tanpa perlu outline tambahan. |
| Pemisah bagian | **selout** 1 px (nada gelap di tepi dalam) | Tanpa ini lengan menyatu dengan badan jadi satu balok. |
| Simetri | wajib | Detail asimetris membatalkan baris mirror (§17.3). |
| Palet | 26 warna, 3 langkah per material | Batas §17.1: 32 global, tanpa anti-aliasing. |
| **Proporsi** | kaki **10 px (42%)**, kepala **5 px** = 1:4,8 kepala | Diukur dari foto model: 7,4 kepala, kaki 41,5%. Kepala dipaksa 5 px karena 3 px mustahil diberi wajah; seluruh selisih diserap kepala, bukan kaki. |
| **Shadow** | ellipse **14×7**, offset **(0,−1)**, alpha 45% | 32×14 (nilai lama) = selebar 2× karakter dan terbaca sebagai genangan. Bukti: `ingame-scale-check.png`. |

**Yang belum ada di set v1 (jujur):** transisi death/dodge masih pose tunggal (belum di-keyframe tangan per frame), belum ada varian hurt per arah senjata, belum ada palette swap oranye/abu (tinggal ganti huruf `j/J/k`).

## Aturan pakai

0. **Baca `projection-3q-spec.png` lebih dulu.** Proyeksi dikunci top-down 3/4: tile 16×16, muka dinding 10 px, atap di-fade, shadow 32×14, **tanpa** perspective scaling. Aset yang melanggar tes penerimaan §17.12 dikembalikan, bukan ditambal di engine.

1. **Sel = 16×24 px** untuk semua karakter. Jangan mengubah ukuran sel; semua kode animasi mengasumsikan grid ini.
2. **Pivot `(8, 23)`** — 1 px di atas tepi bawah sel. Tanda `+` hijau di lembar guide menunjuk titik ini. Kaki karakter menyentuh baseline.
3. **8 arah, digambar 5 baris.** Baris `S, SE, E, NE, N` digambar; `NW, W, SW` diberi pola garis miring bertanda `MIRROR` — **jangan digambar**, dibuat otomatis oleh `flip_h` di runtime. Pemetaan: `SE→SW`, `E→W`, `NE→NW`. Hemat 37,5% frame.
4. **Nama animasi di `SpriteFrames`:** `walk_s`, `walk_se`, `walk_e`, `walk_ne`, `walk_n`, `attack_melee_s`, `death_e` — arah di **akhir** nama. Saat runtime, tiga arah mirror memakai nama arah sumbernya + `flip_h`.
5. **Satu atlas PNG per karakter**, bukan satu file per frame.
6. Grid di lembar `guide` hanya penanda. Yang digambar adalah `*-1x.png` (tanpa grid, transparan).

## Urutan kolom (jangan diubah)

Agar region bisa dihitung dengan rumus, urutan frame per baris adalah:

```text
PLAYER  (30 kolom):
  idle 0-1 · walk 2-7 · attack_melee 8-11 · attack_ranged 12-14
  hurt 15-16 · death 17-22 · dodge 23-26 · interact 27-29

ZOMBIE  (16 kolom):
  idle 0-1 · walk 2-5 · attack 6-9 · hurt 10 · death 11-15
  (Spitter +3 spit, Stalker +4 leap → sheet 20 kolom, tambahan di akhir)

NPC     ( 8 kolom):
  idle 0-1 · talk 2-5 · gesture 6-7

BARIS (semua karakter):
  0 S · 1 SE · 2 E · 3 NE · 4 N   → digambar
  5 NW · 6 W · 7 SW               → MIRROR (flip_h), jangan digambar
```

Rumus region di Godot: `Rect2(kolom × 16, baris × 24, 16, 24)` — berlaku untuk semua canvas 16×24 (Tank 24×32 punya sheet sendiri).

## Import Godot 4.7.2

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

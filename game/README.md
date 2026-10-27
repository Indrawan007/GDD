# Greybox — The End Has Come

Prototipe **1 ruangan** untuk memvalidasi kontrak desain sebelum satu pixel seni final digambar.

> **Status:** versi ini sudah melewati **satu putaran tes nyata di Godot 4.7.2** (lihat bagian *Perbaikan setelah tes pertama*). Error parser yang dilaporkan sudah diperbaiki, dan lint lokal ditambah dua aturan baru supaya kesalahan sejenis tidak terulang.
>
> Masih ada kemungkinan error di tempat yang belum tersentuh tes (mis. urutan `_ready` saat pertama kali memuat aset). Laporkan pesan error persisnya — pengerjaan jadi jauh lebih cepat kalau ada nomor baris.

## Kompatibilitas Godot 4.7.2

Engine kamu 4.7.2 (rilis 18 Agustus 2026). Proyek ini **awalnya ditulis untuk 4.4**, jadi ada tiga hal yang disesuaikan:

| Perubahan | Alasan |
|---|---|
| `config/features` → `("4.7", "GL Compatibility")` | Tanpa ini Godot menampilkan dialog *"project was last edited in 4.4"* dan menawarkan konversi. `config_version` tetap **5** di 4.7.2 (sudah dicek di `core/config/project_settings.h`), jadi tidak ada migrasi format file. |
| `window/stretch/scale_mode="integer"` **ditambahkan** | 4.7 mengubah default proyek baru ke `canvas_items`+`expand`; kita tetap `viewport`+`keep` secara eksplisit. `integer` mencegah piksel tidak rata saat jendela di-resize ke skala bukan kelipatan 4. |
| `snap_2d_transforms_to_pixel` + `snap_2d_vertices_to_pixel` **ditambahkan** | **Ini bug nyata, bukan kosmetik.** GDD §17 butir 5 mewajibkan "gerakan sprite di-snap ke piksel", tapi `project.godot` hanya menyetel filter Nearest — snap-nya tidak pernah aktif. Header lama bahkan mengklaim "pixel snap". Greybox jadi melanggar kontrak proyeksinya sendiri. |

Semua nama setting di atas sudah diverifikasi ada di `doc/classes/ProjectSettings.xml` 4.7.2, dan tidak ada satu pun API yang kita pakai masuk daftar *breaking changes* atau *known incompatibilities* 4.7.x.

Kalau Godot tetap menampilkan dialog versi saat membuka: pilih **buka tanpa konversi** (data kita tidak butuh migrasi), atau konversi — hasilnya sama.

## Perbaikan setelah tes pertama (Godot 4.7.2)

Empat error dilaporkan. Akarnya **dua kebiasaan Python yang tidak ada di GDScript**:

| Gejala di engine | Penyebab | Perbaikan |
|------------------|----------|-----------|
| `Expected closing ")" after grouping expression` (window_node.gd:79, 86) | `state in (State.BROKEN, State.INTACT)` — GDScript tidak punya `in (A, B)` | Diganti `state == State.BROKEN or state == State.INTACT` |
| `Could not resolve class "WindowNode"` (main.gd:87) | Error parser di atas membuat file gagal di-parse, jadi `class_name` tidak terdaftar | Ikut hilang setelah di atas diperbaiki |
| `Cannot infer the type of "w"` | Cascade dari `WindowNode` yang tak terdaftar | Ikut hilang |
| `Cannot infer the type of "inside"` dan `"lit"` (main.gd:199, 209) | `:=` dipakai pada ekspresi yang menyentuh variabel **untyped** (`_player`) → tipenya Variant, tidak bisa diinfer | Diganti `var inside: bool = ...` dan `var lit: bool = ...` |

Saat memeriksa ulang, ditemukan **5 masalah sejenis di `zombie.gd`** yang belum sempat muncul karena file itu berhenti di error parser lebih dulu (`var x := p.global_position` dengan `p` untyped). Semua sudah diberi tipe eksplisit.

Dua aturan baru di `tools/lint_gdscript.py`:

1. `in (A, B)` → error (bukan GDScript).
2. `:=` yang menyentuh variabel untyped → error "tidak bisa menginfer tipe Variant".

## Set sprite pemain (v1, final pass pertama)

Greybox sekarang memakai atlas pemain sungguhan, bukan placeholder: `game/assets/sprites/player.png` (480×120, 30 kolom × 5 baris), dibaca oleh `SpriteFactory.player_frames()`.

- 150 frame digambar; 3 arah sisanya (`SW`, `W`, `NW`) dibuat lewat `flip_h`
- Regenerasi: `python3 tools/make_player_sprites.py` (sekaligus menjalankan validasi 150 sel)
- Lembar review: `docs/art/player-character-sheet.png` dan `docs/art/player-sheet-final.png`
- Walk cycle: `docs/art/player-walk-preview.gif`

Zombie masih memakai placeholder `assets/generated/walker.png` — itu disengaja, karena set zombie baru masuk setelah gaya pemain dikunci.

## Cara menjalankan

1. Godot **4.7.2** (GL Compatibility), buka folder `game/` → *Import* → pilih `project.godot`.
2. Tekan **F5**. Scene utama: `scenes/main.tscn`.

Tidak ada file `.tscn` untuk pemain/zombie/kontainer — semuanya dibangun di
`scripts/main.gd` memakai `SpriteFrames` yang dibuat runtime oleh
`scripts/entities/sprite_factory.gd`. Alasannya: file `.tscn` yang ditulis tangan
sangat mudah salah format; membangun node di kode jauh lebih mudah diverifikasi.

## Kontrol

| Tombol | Aksi |
|--------|------|
| WASD / panah / stick kiri | Gerak (8 arah) |
| Mouse | Bidik (senjata berputar mengikuti kursor) |
| Shift | Sprint (pakai stamina) |
| SPASI | Dodge roll (i-frame 0.25 s) |
| F | Lampu senter on/off (menghabiskan baterai, menaikkan heat) |
| E | **Vault lewat jendela PECAH** (0,45 s) — ditolak kalau berat Kelebihan; kalau tidak ada jendela: ambil kayu dari kontainer (+2 kg) |
| B | Papan/barikade jendela terdekat (PECAH → papan 60 HP → barikade 120 HP) |
| G | **Drop & Run** — buang tas, kecepatan langsung normal |
| R | Isi ulang baterai (hanya siang, dianggap "di shelter") |
| F5 | Lompat ke fase berikutnya (siang → senja → malam → subuh) |
| F3 | Spawn 1 walker |
| F2 | Revive / god mode |
| F1 | Sembunyikan/tampilkan atap |

## Yang sudah jalan (kalau tidak ada error)

- Siklus **siang → senja → malam → subuh**, malam memanjang +5 s/hari.
- **Berat → kecepatan**: 4 ambang (Ringan / Bermuatan / Berat / Kelebihan), plus
  tidak bisa sprint saat kelebihan muatan. HUD menampilkan kg + status berwarna.
- **Drop & Run**: tas jatuh sebagai objek, bisa diambil lagi (ada delay 1.2 s).
- **Lampu + baterai + heat**: lampu menyala menaikkan heat 0.4/detik, mati menurunkannya.
- **Serangan malam**: heat ≥ 25 memicu spawn walker dari tepi ruangan, cap 10.
- **Walker**: chase + attack + mati, LOS raycast ke layer dinding, deteksi 5×/detik.
- **Atap di-fade** (alpha 0.30) saat pemain di dalam ruangan.
- **Jendela 4 state** (§4.2B): utuh bisa dilihat tapi tidak dilewati; **pecah** bisa di-vault pemain
  (0,45 s) dan dipanjat walker (1,2 s); papan & barikade memblokir pandangan. Tekan **B** untuk memapan.
- **Sprite 8 arah**: 5 baris digambar, 3 arah mirror lewat `flip_h`.
- HUD: HP, stamina, baterai, berat, hari + jam, fase + hitung mundur, heat.

## Yang sengaja BELUM ada

| Belum | Alasan / kapan |
|-------|----------------|
| Menembak & damage ke zombie | Phase 1. Greybox hanya menguji gerak, berat, waktu, dan tekanan |
| `NavigationAgent2D` | Zombie masih steering langsung. Navmesh per chunk masuk Phase 3 |
| `TileMapLayer` + autotile | Greybox pakai `Sprite2D` per tile (nol risiko API). Produksi pakai TileMapLayer |
| Inventory grid, crafting, hunger/thirst | Phase 2 (§8.1, §9) |
| Input map penuh + gamepad | Phase 1 (§6.2) |
| Barricade, shelter tier, trader | Phase 2–3 |

## Angka produksi vs greybox

Semua angka ada di `scripts/autoload/tuning.gd`. Yang **dipendekkan** hanya durasi:

| Parameter | Greybox | Produksi (§5.1) |
|-----------|---------|-----------------|
| Siang | 120 s | 600 s |
| Malam | 30 s (+5/hari) | 180 s (+15/hari, cap 300) |

Sisanya (kecepatan, stamina, berat, HP, damage, deteksi) **sama dengan GDD §20**.
Jangan menaikkan angka produksi hanya karena greybox terasa enak — catat dulu di §20.

## Regenerasi aset placeholder

```bash
python3 tools/make_greybox_assets.py     # butuh pillow
```

Aset ditulis ke `game/assets/generated/` (aman untuk di-commit; ukurannya kecil).
Sheet 8 arah, pivot, dan wall face mengikuti §17.3, §17.4, dan §17.12.

## Lint

```bash
python3 tools/lint_gdscript.py
```

Memeriksa: kurung seimbang, indentasi tab, path `load()/preload()` yang tidak ada,
signal `EventBus` yang tidak dideklarasikan, konstanta `Tuning` yang tidak ada,
fungsi ganda, dan `$Node` yang tidak pernah dibuat.

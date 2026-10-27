# Greybox — The End Has Come

Prototipe **1 ruangan** untuk memvalidasi kontrak desain sebelum satu pixel seni final digambar.

> **Status jujur:** kode ini ditulis tanpa bisa menjalankan Godot (sandbox agent tidak punya engine dan unduhan binary diblokir). Sudah lolos `tools/lint_gdscript.py` (kurung, indentasi, path aset, nama signal, nama konstanta, fungsi ganda), tapi **belum pernah dijalankan di engine**. Kalau ada error saat pertama dibuka, kemungkinan besar di baris yang ditandai `# GREYBOX-TODO` atau pada pemanggilan API editor. Laporkan, saya perbaiki.

## Cara menjalankan

1. Godot **4.4** (GL Compatibility), buka folder `game/` → *Import* → pilih `project.godot`.
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
| E | Ambil kayu dari kontainer terdekat (+2 kg) |
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

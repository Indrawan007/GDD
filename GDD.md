# The End Has Come

## Game Design Document v3.14 — Canonical

### Survival Open World · Shelter · Singleplayer · Godot 4.7.2

> **Dokumen ini menggantikan v1, v2, v3.0, v3.1, dan v3.2.**
> Arah resmi: **Survival Open World + Shelter**, bukan roguelite per-floor. Yang masih berlaku dari v3.1: Night Director (event, bukan wave), Battery, angka zombie, angka combat, arsitektur Godot, dan disiplin scope. Yang dipensiunkan: struktur 5 floor, Signal, meta tree antar-run.

---

## 0. Changelog — Pivot v3.2 & penyesuaian v3.3

### 0.1 Ringkasan pivot

| # | Aspek | v3.1 (roguelite) | **v3.2 (berlaku sekarang)** |
|---|-------|------------------|------------------------------|
| 1 | Struktur | 5 floor, 1 siklus per floor, run 30–40 menit | **1 kota persisten, seed, dimainkan berhari-hari** |
| 2 | Kamis | Pemain tidak punya rumah | **Shelter: kamu klaim, bangun, dan pertahankan** |
| 3 | Waktu | Timer per fase, di-reset tiap floor | **Jam dunia berjalan terus; hari demi hari, malam makin panjang** |
| 4 | Kematian | Permadeath (run hilang) | **Respawn di shelter + corpse bag** (mode Ironman tersedia) |
| 5 | Progresi | Meta tree antar-run (Signal) | **Progresi di dalam save: skill tree, shelter tier, blueprint** |
| 6 | Kemenangan | Boss floor 5 | **Pancarkan sinyal dari radio tower, bertahan 3 malam, evakuasi** |
| 7 | Skor | Signal per run | **Hari bertahan (days survived)** |
| 8 | Malam | Loot run berisiko | **Pertahanan shelter + opsi night raid** (keduanya dipertahankan) |
| 9 | Hunger | Dihapus (diganti Battery) | **Kembali: Hunger + Thirst + Battery** (alasan di §8.1) |
| 10 | Scope | 24 minggu, launch penuh | **28 minggu ke Early Access, ±44 minggu ke 1.0** (§21) |

### 0.2 v3.3 — hasil diskusi (berat, night raid, shelter)

| # | Keputusan | Perubahan |
|---|-----------|-----------|
| 11 | **Shelter pindah pakai cooldown 3 hari** (Q1) | §6.1 |
| 12 | **Auto-resolve saat night raid boleh**, plus sistem hadiah night raid (Q2) | §7.5 |
| 13 | **8 distrik dipertahankan untuk 1.0** (Q5) | §4.2, §21 |
| 14 | **The Hive opsional** untuk ending (Q3) | §14.1, §24.1 |
| 15 | **Semua item punya berat; berat memengaruhi kecepatan gerak** | §8.1, §8.3, §8.5, §15.1, §20, §22 |
| 16 | **Kereta dorong opsional** (Q7) | §8.5 aturan 4 & 7, cut list §21 |
| 17 | **Berat senjata & armor dihitung, termasuk di hotbar** (Q8) | §8.5 aturan 6 |
| 18 | **Fatigue = −15% stamina saja** (Q9) | §7.5, §20 |
| 19 | **Spesifikasi tileset & sprite** (player, zombie, NPC, prop, UI, import Godot) | §17 (ditulis ulang) |
| 20 | **Seni = jalur kritis**: 5 distrik butuh ±26 minggu kerja 1 artist | §17.8, §21 |
| 21 | **Sumber seni: 1 artist kontrak**, karakter wajib custom (Q10) | §17.9 |
| 22 | **NPC rasa disimpan untuk pasca-1.0** (Q11) | §17.5, §17.9 |
| 23 | **Template sprite & tileset siap pakai** di `docs/art/` | §17.10 |
| 24 | **8 arah sprite** (bukan 4), digambar 5 baris + 3 mirror | §17.1, §17.3, §17.4, §17.8 |
| 25 | **Proyeksi: Top-Down 3/4 dengan tinggi, bukan isometrik** | §17.11 |
| 26 | **Kontrak proyeksi dikunci sebagai angka** + tes penerimaan aset | §17.12, `docs/art/projection-3q-spec.png` |
| 27 | **Prototipe greybox 1 ruangan** ada di repo (`game/`) | §21B, `game/README.md` |
| 28 | **Jendela: 4 state, bisa dilihat & dilewati lewat state pecah** | §4.2B, `docs/art/window-states-spec.png` |
| 29 | **Tes pertama di engine:** 4 error parser diperbaiki + lint diperkuat | §21B, `game/README.md` |
| 30 | **Target engine 4.7.2:** features bump, `scale_mode=integer`, pixel snap yang sebelumnya hilang | §17, §21B, `game/project.godot` |
| 31 | **Set sprite pemain v1: 150 frame digambar, atlas 480×120, dipakai engine** | §17.3B, `docs/art/player-character-sheet.png` |
| 32 | **Sprite pemain v2: proporsi diukur dari foto (kaki 42%, 1:4,8 kepala) + koreksi shadow 32×14 → 14×7** | §17.3B, §17.12, `docs/art/ingame-scale-check.png` |
| 33 | **Wajah: aturan 3 baris (rambut/dahi/mata) + sisi kulit + bahu menyambung lengan**, diuji 6 varian | §17.3B |
| 34 | **Kanvas pemain 16×24 → 24×32**: wajah dapat 6 baris, pivot (12,31), collider 12×10, shadow 16×7 | §17.3C, §17.12 |

### 0.3 Yang sengaja dipertahankan dari v3.1

| Sistem | Alasan tetap dipakai |
|--------|----------------------|
| Night Director + 12 event (**bukan wave terjadwal**) | Tetap benar: event terpicu keadaan lebih bermakna daripada jadwal |
| Night Pressure (satu angka untuk speed/detect/spawn) | Skalanya cuma ganti sumber: hari, bukan floor |
| Battery sebagai bahan bakar cahaya | Di open world lampu bahkan lebih penting (malam 3–5 menit) |
| Angka combat & zombie (Walker 30 HP, dst) | Sudah divalidasi terhadap layar 320×180 — jangan diutak-atik tanpa data |
| Object pooling, LOD, bake sekali, input gamepad wajib | Alasan teknisnya tidak berubah |
| Disiplin "cut list diputuskan sekarang" | Justru makin penting: open world 3× lebih besar dari roguelite |

### 0.4 Kenapa Hunger kembali (reversal sadar)

Di v3.1 saya menghapus Hunger karena **run cuma 30–40 menit**: meter yang turun karena jam tidak sempat mengajari apa pun. Di open world ini penalaran itu tidak berlaku. Save berjalan 10–30 jam; makanan dan air menjadi **alasan ekspedisi** dan **isi gudang shelter**, dan itu justru inti dari game yang kamu inginkan. Jadi: Hunger + Thirst kembali, tapi tetap dengan aturan "tidak boleh jadi pekerjaan rumah" (§8.1).

---

## 1. Overview

| Item | Detail |
|------|--------|
| **Judul** | The End Has Come |
| **Genre** | Top-Down Survival Open World + Shelter Base Building |
| **Perspektif** | Top-down, aim mouse/gamepad, **8 arah sprite** + rotasi senjata bebas |
| **Struktur** | Satu kota persisten, seed, save/continue, hari ke hari |
| **Multiplayer** | Singleplayer only |
| **Map** | 1 kota prosedural (384×384 tile) + interior bangunan prosedural dari template |
| **Engine** | Godot 4.7.2 (GDScript, Forward+) |
| **Art** | Pixel art 16×16, native 320×180 |
| **Platform** | PC (Steam), keyboard+mouse **dan** gamepad |
| **Target sesi** | 45–90 menit per duduk (bisa disimpan kapan saja di shelter) |
| **Panjang save** | 10–30 jam untuk mencapai ending |
| **Skor** | Hari bertahan, shelter tier, bangunan terjelajah |
| **Referensi rasa** | Project Zomboid (tema & ketegangan), Dysmantle/Dysplaced (loop open world kecil), State of Decay (shelter), Brotato (skala angka) |
| **Yang dijual** | "Rumahmu akan diserang malam ini. Apakah kamu sudah cukup?" |

---

## 2. Core Concept

### 2.1 Elevator Pitch

> Kota sudah mati, tapi kamu belum. Klaim satu bangunan, tutup jendelanya, cari generator. Siang kamu keluar untuk kayu, kaleng, dan obat — malam kamu pulang, menyalakan lampu, dan berharap tidak ada yang mengetuk pintu. Setiap malam lebih panjang dari malam sebelumnya. Kalau kamu bisa bertahan cukup lama, kamu bisa memancarkan sinyal dan keluar dari kota ini.

### 2.2 Design Pillars

| # | Pilar | Konsekuensi desain |
|---|-------|--------------------|
| 1 | **Siang milikmu, malam milik mereka** | Siang tidak pernah membunuh; malam selalu datang. Semua persiapan siang diukur dari "apakah cukup untuk malam ini". |
| 2 | **Shelter adalah karakter kedua** | Shelter punya HP, punya daftar struktur, punya rasa sakit saat rusak. Base bukan menu — base adalah bangunan yang bisa dihancurkan. |
| 3 | **Ekspedisi harus punya titik pulang** | Setiap perjalanan punya jam kembali. Pemain selalu tahu "kalau sekarang balik, masih aman". |
| 4 | **Keserakahan = keputusan, bukan jebakan** | Loot terbaik ada di tempat jauh/berbahaya, dan pemain selalu bisa memilih cukup. |
| 5 | **Bahaya terbaca** | Setiap ancaman punya telegraph audio + visual. Tidak ada kematian dari off-screen tanpa tanda. |
| 6 | **Kegagalan terasa seperti keputusan sendiri** | Kematian datang dari "satu gedung lagi", bukan dari angka yang tidak terlihat. |
| 7 | **Dunia tidak menunggu, tapi tidak menghukum omong kosong** | Waktu berjalan saat kamu tidur dan saat kamu pergi, tapi tidak ada penalti karena menutup game. |

### 2.3 Anti-Pilar

- **Bukan** tower defense. Shelter bertahan karena persiapan, bukan karena kamu berdiri di balik dinding 3 jam.
- **Bukan** horde shooter 100 zombie. Layar 20×11 tile; 18 zombie sudah banjir.
- **Bukan** open world raksasa. 1 kota, 8 distrik, 60–120 bangunan enterable. Bukan peta 20 km².
- **Bukan** game crafting 200 resep. 24 resep, semuanya punya alasan.
- **Bukan** permadeath sebagai default (kecuali mode Ironman).

---

## 3. Dua Loop

Game ini punya dua loop yang saling mengisi. Kalau salah satunya lemah, game-nya lemah.

### 3.1 Loop Ekspedisi (siang)

```text
        ┌──────────────────────────────────────────────┐
        │  PAGI: cek stok (makanan, air, obat, amunisi) │
        │  pilih target: dekat & aman  /  jauh & berharga│
        └──────────────────┬───────────────────────────┘
                           ▼
        ┌──────────────────────────────────────────────┐
        │  JELAJAH: bangunan → loot → craft di tempat  │
        │  (crafting portable, terbatas)               │
        │  konflik: muatan penuh / HP menipis /         │
        │           jam 16:00 lewat                    │
        └──────────────────┬───────────────────────────┘
                           ▼
        ┌──────────────────────────────────────────────┐
        │  PULANG ke shelter → simpan stok → pasang    │
        │  perbaikan, barricade, lampu, jebakan        │
        └──────────────────┬───────────────────────────┘
                           ▼
                     🌙 MALAM (loop 2)
```

**Tekanan loop 1** bukan jam (meski jam ada) tapi **muatan**: berapa kg yang bisa kamu bawa pulang tanpa jadi lambat (§8.5) vs berapa risiko yang kamu ambil untuk mengambilnya. Jam menentukan kapan pulang; berat menentukan apakah kamu **sampai** rumah.

### 3.2 Loop Pertahanan (malam)

```text
        ┌──────────────────────────────────────────────┐
        │  SENJA: lampu dinyalakan, pintu ditutup,     │
        │  generator dinyalakan / dimatikan (HEAT!)    │
        └──────────────────┬───────────────────────────┘
                           ▼
        ┌──────────────────────────────────────────────┐
        │  MALAM:                                     │
        │  · bertahan di shelter (pilihan aman)       │
        │  · night raid ke luar (pilihan serakah)     │
        │  · tidur untuk skip (pilihan bertaruh)      │
        └──────────────────┬───────────────────────────┘
                           ▼
              ┌────────────┴─────────────┐
              ▼                          ▼
       ✅ SUBUH (hidup)           💀 MATI / shelter jebol
       hitung hasil malam         corpse bag / kehilangan
```

### 3.3 Interlock (aturan yang bikin dua loop ini saling mengunci)

1. **Amunisi adalah penghubung.** Siang cari amunisi/materials → malam pakai.
2. **Lampu adalah penghubung.** Shelter butuh lampu untuk aman saat tidur; lampu butuh daya; daya butuh baterai/fuel; baterai diisi di shelter. Semua jalan kembali ke base.
3. **Heat adalah penghubung.** Kegiatan yang memudahkan siang (generator nyala, menembak) menaikkan risiko malam. Pemain mengelola trade-off ini tiap hari.
4. **Night raid adalah penghubung terbalik.** Kalau pemain butuh loot tier tinggi untuk naik tier shelter, ia harus keluar saat malam — dan itu berarti meninggalkan shelter saat shelter sedang diserang. Ini keputusan terbaik di game, jadi jangan pernah disederhanakan.

---

## 4. World

### 4.1 Skala & Bentuk

| Item | Nilai |
|------|-------|
| Ukuran kota | **384 × 384 tile** (16px) = 6.144 × 6.144 px |
| Chunk | 32 × 32 tile → **12 × 12 = 144 chunk** |
| Distrik | **8** (5 saat EA) |
| Bangunan enterable | **60–120** (target 80 saat EA) |
| Landmark tetap | 7 set-piece (hand-authored) |
| Batas dunia | Tembok karantina militer + reruntuhan (bukan invisible wall) |

### 4.2 Distrik

| Distrik | Isi | Bahaya | Loot kunci |
|---------|-----|--------|-----------|
| **Suburban** | Rumah, pagar, jalan kecil. Cocok shelter awal | Rendah | Food, cloth, wood, baterai |
| **Commercial** | Toko, kafe, minimarket | Sedang | Food, electronics, medicine |
| **Industrial** | Gudang, pabrik, derek | Tinggi | Scrap, fuel, tools |
| **Residential Tower** | Apartemen vertikal, banyak pintu | Sedang | Cloth, medicine, personal items |
| **Hospital** | Lorong sempit, banyak ruang | Tinggi | Medicine, chemical |
| **Mall** | Atrium luas, loot padat, zombie padat | Sangat tinggi | Rare gear, electronics |
| **Police / Fire** | Gudang senjata, kendaraan | Sangat tinggi | Senjata, amunisi, armor |
| **Quarantine Wall** *(endgame)* | Pos militer, bunker, radio | Ekstrem | **Radio tower parts**, blueprint akhir |

Aturan spacing: distrik aman (Suburban) selalu bersebelahan dengan spawn; distrik berbahaya minimal 2 distrik jauhnya. Pemain harus **melewati** distrik berbahaya untuk mencapai loot terbaik — itu satu-satunya alasan open world ini ada.

### 4.2B Jendela: Melihat, Masuk, dan Ditembus (top-down 3/4)

Di 3/4, jendela **tidak** menghadap kamera seperti di isometrik — ia **dipotong dari dinding**. Justru itu yang membuatnya bekerja: setiap tile dinding punya muka 10 px (§17.12), dan jendela menggantikan bagian muka itu dengan kaca, lubang, papan, atau barikade. Jadi tidak perlu sprite jendela menghadap 4 arah; satu tile, empat state.

**Yang bisa dan tidak bisa (dikunci):**

| State | Melihat ke dalam | Dilewati pemain | Dilewati zombie | Tembus peluru | HP |
|-------|------------------|-----------------|-----------------|---------------|-----|
| **Utuh** | **YA** (tembus pandang) | Tidak | Tidak | Kaca pecah dulu | 20 |
| **Pecah** | YA | **YA** — vault 0,45 s | YA — panjat 1,2 s | **YA** | — |
| **Papan** | **TIDAK** | Tidak | Tidak | Tidak | 60 |
| **Barikade** | TIDAK | Tidak | Tidak | Tidak | 120 (→ papan saat rusak) |

**Tiga aturan yang mengikat sistem lain:**

1. **Visibilitas memakai layer `vision blocker` (layer 5) yang terpisah dari collision.** Kaca utuh **tidak** memblokir pandangan; papan & barikade memblokir. Tanpa pemisahan ini, fog of war dan LOS akan salah di semua bangunan — dan "melihat lewat jendela" jadi tidak mungkin.
2. **Jendela adalah `Node2D`, bukan tile.** Alasannya: ia harus bisa jadi titik `NavigationLink2D` untuk zombie di masa depan, punya HP, dan menyimpan state di diff chunk (§4.4). Kalau dijadikan tile, semua itu harus diakali.
3. **Vault pemain ditolak saat berat "Kelebihan"** (§8.5). Konsisten dengan larangan sprint & dodge: kalau kamu serakah, jendela bukan jalan keluar. Pesannya muncul di HUD: *"Kelebihan muatan — buang tas dulu (G)"*.

**Untuk zombie (Navmesh):** jangan rebake navigation tiap kali jendela pecah — terlalu mahal. Pakai **`NavigationLink2D` per jendela** yang di-`enabled` saat state = PECAH. Rencana ini masuk Phase 3 (§21) dan **belum** ada di greybox (greybox memakai steering + raycast sederhana).

**Konsekuensi desain yang bagus:** jendela jadi alat tawar-menawar malam hari. Memapan semua jendela = aman tapi buta; membiarkan satu pecah = bisa melihat & kabur, tapi walker bisa memanjat lewat situ. Itu keputusan yang lebih menarik daripada pintu yang cuma bisa dibuka/ditutup.

### 4.3 Bangunan & Interior

- Eksterior: dari tileset per distrik, disusun prosedural per blok (grid 3×3 blok per distrik, tiap blok 3–6 bangunan).
- Interior: **template** per archetype (rumah kecil, rumah 2 lantai, toko, gudang, kantor, apartemen, klinik). Masing-masing 5–9 varian layout + 3 tingkat kekacauan (rapi, rusak, terbakar).
- Lantai: **maksimal 2 lantai**, naik lewat tangga. Lantai 2 memberi vantage point + loot lebih baik + jalur keluar.
- Pintu & jendela adalah objek state: terbuka/tertutup/dibarricade/dirusak. Ini yang membuat shelter dan looting terasa fisik. Detail jendela (lihat/masuk/tembus) di §4.2B.
- **Tidak ada loading screen** saat masuk bangunan — interior adalah bagian dari tilemap yang sama.
- **Dinding punya muka 10 px** (wall face tile) + drop shadow di bawah karakter/prop, supaya bangunan terlihat punya tinggi tanpa proyeksi isometrik. Angka pastinya di §17.12.

### 4.4 Streaming & Simulasi

```text
Chunk aktif        3×3 di sekitar pemain  → tilemap + entity penuh (60 tick)
Chunk dekat        radius 6              → entity simulasi 5 tick/detik
Chunk jauh         sisanya               → disimpan sebagai diff state; tidak di-tick

Isi diff state per chunk:
  pintu/jendela (state), kontainer (isi/terbuka), barricade, mayat yang bisa di-loot,
  populasi zombie (jumlah + tipe, bukan posisi presisi), hari terakhir dikunjungi
```

Aturan: **zombie di luar radius 6 tidak disimulasikan per-individu.** Mereka disimpan sebagai angka populasi per chunk dan "dituangkan" kembali saat chunk dimuat. Ini bukan penghematan opsional — tanpa ini, 384×384 tile dengan ratusan zombie tidak mungkin.

### 4.5 Populasi Zombie Dunia

| Parameter | Nilai |
|-----------|-------|
| Populasi dasar per chunk | 0–3 (distrik aman) sampai 4–8 (distrik ekstrem) |
| Populasi skala hari | `dasar × (1 + 0.04 × hari)` cap **×2.5** |
| Wandering horde | 1–4 grup, 8–20 zombie, berpindah antar chunk tiap 30–90s (disimulasikan kasar) |
| Horde tertarik suara | Tembakan menambah "noise pool" chunk, horde bergerak ke sana |
| Respawn chunk | Chunk yang dibersihkan kembali terisi setelah **7 hari** |
| Bangunan di-loot | Kontainer kosong tidak refill (kecuali event supply drop) |

**Kenapa respawn 7 hari:** tanpa respawn, pemain bisa "menghabiskan" kota dalam 3 hari. Dengan respawn instan, looting tidak bermakna. 7 hari membuat pemain harus **berpindah area** — dan itulah yang memaksa ekspedisi jauh.

### 4.6 Landmark (set-piece hand-authored)

1. **Radio Station** — lokasi blueprint radio tower (endgame)
2. **Quarantine Checkpoint** — gerbang, kendaraan militer, armor
3. **Hospital Wing** — sumber medicine terbesar, banyak zombie
4. **Mall Atrium** — loot padat, horde padat
5. **Water Treatment** — sumber air bersih berlimpah (mengubah ekonomi thirst)
6. **The Hive Nest** — sarang, menghasilkan horde terus; menghancurkannya menurunkan heat global
7. **The Bridge Out** — jalur evakuasi (fiktif), jadi motivasi cerita

Landmark adalah satu-satunya tempat yang tidak prosedural. Tujuannya: pemain punya **peta mental** dan cerita, bukan cuma kota acak yang homogen.

---

## 5. Waktu

### 5.1 Jam Dunia

| Fase | Durasi default | Fungsi |
|------|----------------|--------|
| **Siang** | 600s (10 menit) | Ekspedisi, looting, crafting |
| **Senja** | 90s | Kembali, tutup pintu, nyalakan lampu, putuskan heat |
| **Malam** | 180s → naik +15s/malam → cap **300s** | Pertahanan / night raid / tidur |
| **Subuh** | 30s | Jeda, hitung hasil, perbaikan cepat |

Satu hari penuh = **900s (15 menit)** di hari 1, dan **±1.170s (19,5 menit)** di hari 9+.

**Validasi angka siang 600s:** kecepatan jalan 80 px/s → ±48.000 px perjalanan per hari. Menyeberangi kota (6.144 px) ±77s. Jadi satu hari cukup untuk: pergi ke distrik tetangga, loot 3–4 bangunan, pulang — atau pergi jauh dan **tidak** sempat pulang. Itu pilihan yang diinginkan.

### 5.2 Aturan Waktu

1. **Jam tidak pernah berhenti di dalam game** (kecuali pause menu). Waktu juga berjalan saat di inventory/crafting.
2. **Menutup game tidak menghukum.** Saat load, jam melanjutkan dari titik terakhir save (save hanya di shelter atau saat quit, lihat §13.5).
3. **Tidak ada fast-forward** selain tidur (§5.4).
4. **Malam memanjang** tiap hari sampai batas. Ini kurva kesulitan utama, bukan angka zombie.
5. **Cuaca** (hujan, kabut, badai) mengubah visibilitas & suara; hujan menutupi bunyi tembakan (−40% noise) tapi mematikan lampu luar sementara.

### 5.3 Skala Hari → Kesulitan

```text
night_length   = min(180 + 15 × (hari - 1), 300)
night_pressure = 1.00 + 0.05 × (hari - 1)            cap 2.00
populasi       = dasar_chunk × min(1 + 0.04 × (hari-1), 2.5)
horde_night    = setiap hari ke-5 (5, 10, 15, ...)    selalu, apa pun heat-nya
```

Hari 1 malam 180s pressure 1.0. Hari 12 malam 300s pressure 1.55, populasi ×1.44. Pemain merasakan **perlambatan yang mencekik**, bukan lompatan angka.

### 5.4 Tidur

Tidur adalah cara utama melewati malam **tanpa** menghadapi serangan. Ia sengaja punya taruhan.

| Syarat | Nilai |
|--------|-------|
| Lokasi | Harus di shelter, di kasur, lampu menyala **atau** ada sentry |
| Musuh | Tidak ada zombie di dalam shelter |
| Efek | Jam dipercepat ×10 sampai subuh; +20 HP, stamina penuh, "Rested" (+15% regen stamina selama 1 hari) |
| Taruhan | **Serangan malam tetap bisa terjadi saat tidur** — diselesaikan lewat auto-resolve (§6.5) |
| Interupsi | Kalau shelter jebol saat tidur, pemain **terbangun di tengah serangan** dengan kondisi seperti saat tidur, bukan dengan HP penuh |
| Biaya | Melewatkan loot malam + trader restock (kalau malam itu) |
| Tidak bisa | Saat horde night (hari ke-5, 10, 15…) — horde **membangunkan** kamu, tanpa pilihan |

**Kenapa tidur tetap ada:** tanpa tidur, pemain yang sudah siap terjebak berdiri 3 menit. Dengan tidur, pemain memilih "saya percaya pertahanan saya" dan itu justru momen paling menegangkan — kamu melihat lampu mati satu per satu dari dalam kamar.

---

## 6. Shelter

### 6.1 Klaim Shelter

| Item | Aturan |
|------|--------|
| Cara | `Claim Kit` (10 wood + 5 scrap) pada pintu bangunan |
| Jumlah aktif | **1** shelter pada satu waktu |
| Pindah | Bisa melepas klaim (struktur hilang 50% materialnya) lalu klaim bangunan lain — **cooldown 3 hari** sejak klaim terakhir (keputusan v3.3) |
| Syarat bangunan | Punya minimal 1 pintu, 2 jendela, atap utuh, bukan bangunan landmark |
| Zona aman | Shelter tidak spawn zombie **di dalam** selama tertutup; di luar tetap berbahaya |

Pemain pemula akan mengklaim rumah Suburban kecil. Pemain berpengalaman akan mengejar gudang Industrial 2 lantai dengan satu pintu masuk. **Pemilihan shelter adalah keputusan strategis pertama dan terbesar** — jadi harus terasa.

**Kenapa cooldown 3 hari (Q1):** tanpa biaya, strategi optimal adalah "kemah di distrik aman saat lemah, pindah ke distrik ekstrem saat kuat" — pemain berpindah setiap kali situasi berubah, dan pilar "shelter adalah karakter kedua" hilang. Dengan cooldown, memilih shelter berarti **berkomitmen** untuk 3 hari, termasuk saat malamnya memburuk. Boleh pindah, tapi bukan sebagai refleks.

**Kalau shelter hancur total:** pemain boleh klaim bangunan baru **segera**, cooldown tidak berlaku. Ini bukan celah — kehilangan seluruh infrastruktur sudah jauh lebih mahal daripada menunggu 3 hari (§13.4).

### 6.2 Struktur Shelter

| Struktur | Tier | Material | Fungsi |
|----------|------|----------|--------|
| Door Reinforcement | 1–3 | wood 4/8/12 + scrap 2/4/8 | HP pintu 120/240/400, tahan Tank |
| Window Barricade | 1–3 | wood 6 / +scrap 4 / +metal 8 | Tutup jalur masuk, bisa diintip |
| Wall Reinforcement | 2 | wood 10 + scrap 6 | +100 HP dinding ruangan |
| Spike Strip | 1 | scrap 4 + wood 2 | 30 DMG, 1× pakai, lambatkan |
| **Generator** | 2 | scrap 20 + electronics 8 + fuel 4 | Daya untuk lampu, turret, freezer, radio. **+0.5 heat/menit** |
| Floodlight | 2 | electronics 4 + scrap 6 | Radius 200px, +0.2 heat/menit, menerangi halaman |
| Turret | 3 | scrap 25 + electronics 12 + turret parts | 12 DMG, 200px, butuh daya, amunisi 60 |
| Water Collector | 1 | cloth 6 + scrap 4 | +20 air/hari (hujan: +40) |
| Garden Plot | 2 | wood 8 + water 10 | +1 food/hari setelah 2 hari |
| Storage Crate | 1–3 | wood 8/12/16 + scrap 2/4/6 | 1/2/3 halaman stok = **60/120/180 kg** |
| Workbench | 1–3 | wood 10 / +scrap 15 / +electrical 8 | Membuka resep tier 2/3 |
| Bed | 1 | cloth 8 + wood 6 | Tidur (§5.4) |
| Infirmary | 2 | cloth 10 + medicine 5 + scrap 8 | +1 heal/hari, mempercepat pemulihan luka |
| Radio | 3 | electronics 10 + scrap 12 | Info cuaca/horde, kontak trader, **syarat menara akhir** |
| Noisemaker (decoy) | 2 | scrap 6 + electronics 2 | Mengalihkan serangan 1 malam (§7.4) |

### 6.3 Shelter Tier

| Tier | Syarat | Membuka |
|------|--------|---------|
| **1 — Shelter** | Claim + bed + barricade 2 jendela | Craft tier 1, storage 1, tidur |
| **2 — Stronghold** | Generator + workbench 2 + storage 2 + dinding diperkuat | Craft tier 2, garden, turret, noisemaker |
| **3 — Beacon** | Radio + workbench 3 + turret 2 + generator 2 | Craft tier 3, **radio tower (endgame)** |

Naik tier **tidak** otomatis: butuh material dan minimal 2 hari. Ini pacing utama.

### 6.4 Integritas Shelter

- Shelter punya **total HP struktural** = jumlah HP semua struktur + struktur bangunan dasar.
- Kerusakan dari serangan malam mengurangi HP struktur spesifik (pintu yang diserang rusak duluan).
- Struktur rusak tetap berfungsi sampai 0 HP, lalu berhenti (pintu 0 HP = terbuka).
- **Pemain tidak bisa membangun saat zombie ada di dalam shelter.** Urutannya harus: bersihkan → perbaiki → tutup.
- Kalau semua struktur hancur dan pemain mati: shelter tetap ada tapi **kosong dan tidak terlindungi** — pemain bisa klaim ulang, tapi isinya hilang (loot dicuri).

### 6.5 Auto-Resolve Serangan (saat tidur / saat pergi)

Kalau pemain tidur atau tidak berada di shelter saat serangan:

```text
resolve_attack(day, heat, structures, defender_present):
    attack_strength = f(day, heat)                 # §7.2
    defense_strength = Σ hp_efektif(struktur) × (1.15 jika ada turret) 
                       × (1.20 jika semua penerangan menyala)
                       × (0.70 jika tidak ada penerangan sama sekali)
    if defense_strength >= attack_strength:
        kerusakan = 0.15 × attack_strength          # baret, beberapa struktur −HP
    else:
        kerusakan = attack_strength - defense_strength
        pilih struktur dengan HP terendah secara berurutan → hancurkan/rusak
    catat laporan: "Pintu belakang rusak (HP 40/240). Dua walker masuk, mengacak 1 storage."
```

**Aturan kritis:** laporan hasil auto-resolve **wajib** ditampilkan sebagai ringkasan yang bisa dibaca (bukan angka acak). Pemain harus bisa belajar: "dinding kayu tidak cukup untuk hari 8". Kalau auto-resolve terasa tidak adil, pemain akan berhenti tidur dan berhenti keluar — dua-duanya mematikan game.

---

## 7. Heat & Night Attacks

### 7.1 Prinsip

Zombie tidak menyerang shelter karena "sudah malam ke-6". Mereka menyerang karena **kamu terdengar**. Sistem Heat adalah satu angka 0–100 per shelter yang membuat seluruh kegiatan pemain punya harga.

```text
Heat naik:
  Generator menyala        +0.5 / menit
  Floodlight               +0.2 / menit
  Turret menembak          +2.0 / ledakan 3 detik
  Tembakan pemain          +4.0 / tembakan
  Ledakan (molotov, barel) +8.0
  Crafting di workbench    +0.3 / menit
  Zombie memukul pintu     +1.0 / hit

Heat turun:
  Gelap & sunyi            −0.4 / menit
  Hujan                    −0.6 / menit
  Noisemaker aktif         −0.0 (tapi mengalihkan serangan)

Heat dibagi 4 saat pindah shelter (bukan nol — jejak tetap ada).
```

### 7.2 Serangan Malam: Pemicu

| Heat | Kemungkinan serangan | Kekuatan |
|------|---------------------|----------|
| 0–24 | 0% (kecuali horde night) | — |
| 25–49 | 25% | 2–4 walker, 1 pintu |
| 50–74 | 60% | 5–9 campuran, 2 arah |
| 75–100 | 90% | 11–16 + 1 tank/screamer, 3 arah |
| Horde night (hari 5, 10, 15…) | **100%**, apa pun heat | 16–24, gelombang 2–3 |

Night Director (dari v3.1) tetap dipakai **sebagai penambah**, bukan pengganti: event acak (`Echo Migration`, `Grid Collapse`, `Hunter Pack`, `Breach`, `The Quiet`, `Structural Collapse`, `Acid Rain`) terjadi **di dalam** malam, dengan aturan keadilan yang sama (maks 1 Event Tier 3/malam, pity saat HP<35%, telegraph wajib).

**Perbedaan penting dari v3.1:** jumlah zombie serangan dihitung dari **heat + hari**, bukan dari timer malam. Serangan punya awal yang jelas (bunyi, panah arah) dan akhir yang jelas (fajar atau zombie habis).

### 7.3 Bentuk Serangan

1. **Probe** — 2–4 zombie mendekati pintu, mencoba masuk, pergi kalau gagal 20s. Mengajarkan sistem.
2. **Breach** — 5–9 zombie, menyebar ke 2 arah, satu grup memecah jendela. Pemain harus memilih pintu mana yang dipertahankan.
3. **Siege** — 11–16 zombie + spesialis. Berlangsung 90–150s. Barricade yang hancur tidak bisa dibangun ulang selama ada zombie di dalam.
4. **Horde** — 16–24 dalam 2–3 gelombang, ada jeda 20s antar gelombang (jeda = waktu perbaiki, sengaja diberi).

### 7.4 Counterplay (yang membuat sistem ini bukan keputusasaan)

| Alat | Efek |
|------|------|
| Matikan generator sebelum gelap | Heat −0.5/menit; shelter gelap = zombie lebih sulit menemukan pintu (−30% attack strength) |
| Noisemaker / radio lure | Memindahkan serangan malam ini ke lokasi lain (tetap ada suara, tapi untuk kamu) |
| Perbaiki siang, bukan malam | Perbaikan di malam hari butuh 2× waktu dan menaikkan heat |
| Tidur di ruang dalam | Menghindari serangan frontal; auto-resolve memakai kekuatan struktur |
| Night raid | Keluar saat malam = shelter diserang tanpa kamu (auto-resolve 0,85×), tapi loot tier tinggi **dan hadiah apresiasi bila selamat** (§7.5) |
| Bunuh The Hive | Menurunkan heat global −25 (sekali) dan mengurangi horde night |

### 7.5 Night Raid: Aturan, Hadiah, Konsekuensi (keputusan v3.3)

Night raid adalah pilihan keluar shelter saat malam. Ini satu-satunya cara mendapat loot tier tertinggi, dan harganya adalah rumahmu menghadapi malam tanpa kamu.

**Definisi berhasil (harus dihitung dengan jelas, bukan feeling):**

```text
night_raid_valid  = pemain di luar shelter ≥50% durasi malam
                    DAN malam berakhir (subuh)                   
night_raid_sukses = night_raid_valid AND masih hidup saat subuh
night_raid_gagal  = mati di luar   → corpse bag, hadiah hangus
                    balik ke shelter sebelum subuh → bukan raid,
                    tapi tetap dihitung "pulang awal" (tidak ada hadiah, tidak ada Fatigue)
```

Selama raid, shelter **selalu** di-auto-resolve dengan pertahanan **×0,85** (penjaga tidak lengkap): turret tetap menembak, tapi pintu tidak bisa diperbaiki manual dan pemain tidak bisa memadamkan kebakaran.

**Hadiah apresiasi saat berhasil** (semua diberikan saat subuh, di lokasi pemain berada):

| Hadiah | Nilai | Kenapa ada |
|--------|-------|-----------|
| **Night loot** | Kontainer gelap yang dibuka saat malam: 1 tier di atas siang | Insentif utama; sudah ada sejak v3.1 |
| **Nightfall Cache** | 1 peti jatuh di lokasi pemain saat subuh | Imbalan konkret "kamu bertahan di luar" |
| Isi cache — Bronze | 1 resource bundle (scrap/electronics) + 1 medkit | Raid singkat tetap dihargai |
| Isi cache — Silver | + 1 senjata/blueprint umum | Raid menengah |
| Isi cache — Gold | + 1 rare (blueprint langka / turret part / radio part) | Raid penuh malam |
| **XP malam** | Kill saat malam ×1.5, +40 XP saat berhasil | Progresi terasa |
| **Trader favor** | 1 slot dagangan ekstra di kunjungan berikutnya | Hadiah non-material yang membangun cerita |
| **"Dawn Runner"** | +10% loot speed & +10% stamina regen selama 1 hari | Sedikit rasa kuat setelah malam berat |

```text
night_raid_score = menit_di_luar + 0.2 × zombie_dibunuh_saat_malam
  < 6   → tidak ada cache (raid terlalu singkat)
  6–9   → Bronze
  10–15 → Silver
  ≥ 16  → Gold
```

**Konsekuensi (juga wajib, kalau tidak ini jadi hadiah gratis):**

| Konsekuensi | Detail |
|-------------|--------|
| Shelter tanpa kamu | Auto-resolve ×0,85; kalau breached, **25% isi storage hilang** (dicuri/dihancurkan) |
| **Fatigue** | 1 hari setelah raid: **stamina maks −15% saja** (keputusan Q9). Tidak ada penalti hunger/thirst — dua penalti sekaligus terasa menghukum |
| Tidak bisa memperbaiki | Tidak ada perbaikan struktur selama malam; kamu pulang ke kerusakan |
| Kembalinya berat | Perjalanan pulang saat subuh tetap harus ditempuh dengan berat bawaan (§8.5); muatan penuh = lambat |
| Risiko mati | Mati di luar = corpse bag (semua loot raid ada di situ), hadiah hangus, respawn subuh |

**Aturan anti-eksploit:**

1. Raid harus benar-benar di luar shelter — berdiri di halaman shelter tidak dihitung.
2. Kalau shelter hancur saat raid, pemain **tetap** dapat cache (usaha dihargai) tapi kehilangan infrastruktur. Jangan pernah membuat pemain merasa "lebih baik mati".
3. Cache tidak bisa di-farm dengan masuk-keluar: satu cache per malam, dan hanya kalau `night_raid_valid`.
4. Night raid di **horde night** memberi cache satu tier lebih tinggi (Gold minimum), karena malam itu memang paling berbahaya.

**Kenapa hadiah ini perlu:** tanpanya, night raid hanya penalti (shelter diserang + Fatigue) tanpa imbalan terukur. Pemain rasional akan selalu tidur, dan seluruh sistem loot malam mati. Hadiah ini yang membuat "keluar malam ini?" jadi keputusan, bukan kesalahan.

---

## 8. Player

### 8.1 Stats

| Stat | Awal | Aturan |
|------|------|--------|
| **HP** | 100 | Tidak regen alami. Item, tidur, infirmary |
| **Stamina** | 100 | Sprint −18/s, regen 22/s setelah 0.8s jeda. Dodge −25 |
| **Hunger** | 100 | −1 per 20s (±30/hari). Di 0 → −1 HP / 4s. Food +40 |
| **Thirst** | 100 | −1 per 12s (±50/hari). Di 0 → −1 HP / 3s. Water +50 |
| **Battery** | 100 | Flashlight 1.0/s, torch 0.6/s. Recharge di generator (30/menit) |
| **Armor** | 0 | 2 slot, reduksi 15–40%, rusak saat kena |
| **Muatan** | 30 kg / 20 slot | **Dua batas**: berat (kg) yang menentukan kecepatan, dan slot yang menentukan jumlah tumpukan. Rincian §8.5 |
| **i-frame** | 0.6s saat kena | 0.25s saat dodge |
| **Walk / Sprint** | 80 / 128 px/s | Sprint sambil tidak menembak |

**Kenapa Hunger/Thirst tidak jadi pekerjaan rumah:** butuh ±1,5 makan dan 2 minum per hari (15 menit). Air tersedia dari Water Collector dan Water Treatment; makanan dari garden + loot. Artinya pemain bisa **mengamankan** kebutuhan ini dalam beberapa hari pertama, lalu fokus ke hal lain. Kalau playtest menunjukkan pemain menghabiskan >2 menit/hari untuk makan-minum, angkanya dilonggarkan.

### 8.2 Kontrol

```text
KEYBOARD + MOUSE                     GAMEPAD
WASD            gerak 8 arah         Left stick
Mouse           bidik                Right stick
Left click      serang               RT
Right click     aim (akurasi naik)   LT
R               reload               X
E               interact / loot      A
Q               lempar item          LB
1–4             hotbar               D-pad
F               flashlight on/off    RB (hold) / toggle di opsi
G               drop bag (§8.5)      R3 (click stick kanan)
Shift           sprint               L3
Space           dodge                B
Tab             inventory            Start
C               crafting             Select
M               map                  View
T               tidur (di kasur)     Y
```

### 8.3 Inventory

- **20 slot** (bisa naik +6 lewat skill Survival) — batas jumlah tumpukan.
- **Kapasitas berat 30 kg** (bisa naik lewat tas & skill, §8.5) — batas fisik, **inilah yang menentukan kecepatan**.
- Hotbar 4 slot.
- Stok shelter **tidak** memakai slot maupun berat — gudang shelter punya halaman sendiri (§6.2).
- Memindahkan stok di shelter instan. Memindahkan di luar shelter butuh 0.4s (tidak bisa sambil lari).
- **Slot penuh atau berat penuh = tidak bisa mengambil item**, bukan "mengambil lalu melambat". Pemain harus memilih: buang, simpan, atau jangan ambil.

### 8.4 Dodge Roll

Stamina 25 · durasi 0.30s · jarak 48px · i-frame 0.25s · cooldown 0.8s · 8 arah.

Dodge adalah satu-satunya jawaban untuk Runner dan Exploder. Kalau di minggu 4 dodge belum terasa enak, **hentikan fitur lain** sampai enak.

### 8.5 Berat / Encumbrance (keputusan v3.3)

Semua item punya berat. Berat bawaan memperlambat gerak, menaikkan suara, dan mengurangi kemampuan sprint/dodge. Tujuannya bukan realisme demi realisme — tujuannya **memaksa pemain memilih apa yang layak dibawa pulang**, karena itulah inti survival.

**Kapasitas dasar & upgrade:**

| Sumber | Kapasitas |
|--------|-----------|
| Dasar (Survivor) | **30 kg** |
| Tas Kecil (craft: cloth 10 + scrap 6) | 40 kg |
| Tas Besar (craft tier 3: cloth 16 + scrap 12 + electronics 4) | 50 kg |
| Skill Survival "Back Strength" ×2 node | +5 kg / node |
| Maksimum realistis | **60 kg** |

**Berat item (kg per unit):**

| Material | kg | Material | kg |
|----------|----|----------|----|
| Wood | 2.0 | Food | 0.5 |
| Scrap | 2.5 | Water | 1.0 |
| Electronics | 0.4 | Medicine | 0.2 |
| Chemical | 0.6 | Battery | 0.6 |
| Cloth | 0.3 | Bandage / Medkit | 0.2 / 0.6 |
| Fuel (kaleng) | 3.0 | Molotov | 0.7 |
| Amunisi (per 12) | 0.4 | Barricade kit | 6.0 |

| Senjata & armor | kg | Senjata & armor | kg |
|---------|----|---------|----|
| Machete | 1.1 | Pistol | 1.2 |
| Wrench | 2.2 | Nailgun | 3.0 |
| Spear | 2.0 | Sawed-off | 3.2 |
| Axe | 3.5 | Rifle | 3.8 |
| Armor vest | 4.0 | Helm | 1.5 |

**Ambang & efek:**

| Status | % kapasitas | Kecepatan | Sprint | Dodge | Regen stamina | Suara |
|--------|-------------|-----------|--------|-------|---------------|-------|
| **Ringan** | ≤50% | ×1.00 | penuh | normal | ×1.00 | ×1.00 |
| **Bermuatan** | 50–80% | ×0.95 | normal | normal | ×0.95 | ×1.05 |
| **Berat** | 80–100% | ×0.85 | biaya +15% | normal | ×0.80 | ×1.15 |
| **Kelebihan** | >100% | ×0.65 | **tidak bisa** | **tidak bisa** | ×0.50 | ×1.35 |

Contoh konkret: 40 kg dari 30 kg kapasitas → kecepatan jalan 80 × 0.65 = **52 px/s**. Runner bergerak 96 px/s. Artinya kelebihan muatan = **tidak mungkin lari dari Runner**. Ini bukan hukuman; ini peringatan bahwa kamu serakah.

**Efek lain:**

- Suara berat menambah **noise pool chunk** → heat naik +0.2/menit saat bergerak cepat dengan muatan Berat/Kelebihan.
- Menembak saat Berat: spread +10%. Saat Kelebihan: +25% dan recoil pulih lambat.
- Memanjat tangga saat Kelebihan butuh 2× waktu (loot lantai 2 jadi mahal).
- Fall damage tidak berubah — jangan menambah sistem yang tidak bisa dibaca pemain.

**Mekanik "Drop & Run" (fitur, bukan tambalan):**

Pemain bisa menekan `G` untuk **menjatuhkan tas** (seluruh isi inventory non-hotbar) di tanah:

```text
Efek:  berat langsung turun ke berat hotbar + armor
       kecepatan & dodge kembali normal seketika
Biaya: tas jadi objek di dunia (bisa diambil lagi, 0.6s)
       Zombie tidak mengambilnya, tapi bertahan hanya 2 hari
       Isi tas terlihat (bisa dipastikan tidak hilang)
```

Ini jawaban untuk "kenapa pemain tidak boleh sekadar memaksa berat": saat dikejar Runner dengan 38 kg di punggung, pilihan yang benar adalah **membuang tas dan hidup** — bukan melambat sampai mati. Itu momen yang bagus, dan pemain akan menceritakannya.

**Aturan desain yang mengikat:**

1. **Selalu tampilkan kg dan status** di HUD (bukan hanya saat buka inventory). Pemain harus tahu ia melambat **sebelum** dikejar.
2. **Tidak ada berat tersembunyi.** Semua item menampilkan kg di tooltip.
3. Barang misi (radio part, blueprint) **tidak** dihitung berat — jangan pernah membuat progresi cerita gagal karena tas penuh.
4. Loot besar (generator part, turret) tidak bisa dibawa: harus dipasang di tempat atau diangkut lewat **dua kali perjalanan**. Alat bantu opsional: kereta dorong (craft: scrap 8 + wood 4, 20 kg, muatan 40 kg, tidak bisa masuk bangunan sempit, tidak bisa didorong saat sprint).
5. Kalau playtest menunjukkan pemain menghabiskan >20% waktu untuk mengatur berat, naikkan kapasitas dasar — jangan hapus sistemnya.
6. **Senjata dan armor dihitung beratnya, termasuk yang terpasang di hotbar** (keputusan Q8). Ini disengaja: senjata memang barang paling berat (rifle 3,8 kg, axe 3,5 kg, vest 4,0 kg). Pemain yang membawa 4 senjata + vest + helm sudah menghabiskan 17 kg sebelum mengambil loot — itu keputusan, bukan bug. Tidak ada pengecualian untuk slot hotbar.
7. **Alat bantu angkut bersifat opsional** (keputusan Q7): kereta dorong boleh dipotong kalau Phase 2 mepet, tanpa merusak sistem berat — karena Drop & Run dan perjalanan ganda sudah cukup untuk menopang loop.

**Validasi angka (supaya berat tidak jadi pekerjaan rumah):**

```text
Contoh 1: membangun Generator
  scrap 20 (50,0 kg) + electronics 8 (3,2 kg) + fuel 4 (12,0 kg) = 65,2 kg
  → 3 perjalanan dengan kapasitas 30 kg
  → 2 perjalanan dengan Tas Kecil (40 kg)
  → 1 perjalanan kereta (muatan 40 kg) + 1 perjalanan punggung

Contoh 2: ekspedisi loot standar (kapasitas 30 kg, sisa setelah gear ±24 kg)
  6 wood (12 kg) + 12 scrap (30 kg) = 42 kg → TERLALU BERAT
  realistis: 6 wood (12 kg) + 4 scrap (10 kg) = 22 kg → status Bermuatan
  → pemain harus memilih: kayu untuk barricade, atau scrap untuk amunisi

Contoh 3: bertahan hidup 1 hari (yang harus selalu bisa dibawa)
  food 2 (1 kg) + water 2 (2 kg) + bandage 3 (0,6 kg) + amunisi 24 (0,8 kg) = 4,4 kg
  → kebutuhan hidup hanya 15% kapasitas. Sisa 85% untuk loot. Ini disengaja:
    berat bukan soal makan, tapi soal berapa banyak barang berharga yang berani kamu bawa.
```

---

## 9. Combat

### 9.1 Prinsip

- Proyektil punya travel time (bukan hitscan) → bisa meleset, bisa di-dodge.
- Spread naik saat bergerak; aim memperlambat tapi menaikkan akurasi.
- Melee arc 90°, hitbox aktif 0.18s, selalu memberi knockback.
- Setiap musuh punya telegraph ≥0.35s.
- **Tembakan menaikkan heat.** Ini yang membuat senjata api punya harga, bukan cuma amunisi.

### 9.2 Senjata (10 saat 1.0; 6 saat EA)

| Senjata | Tipe | DMG | Rate | Jangkauan | Ammo | Catatan |
|---------|------|-----|------|-----------|------|---------|
| Pipe Wrench | Melee | 22 | 1.6/s | 26px | ∞ | Knockback 80, stamina 8 |
| Machete | Melee | 15 | 2.6/s | 24px | ∞ | Bleed 2/s selama 4s |
| Fire Axe | Melee | 40 | 0.85/s | 30px | ∞ | Bisa merusak pintu/barricade, stamina 20 |
| Spear (craft) | Melee | 30 | 1.0/s | 44px | ∞ | Jarak aman dari Exploder |
| Pipe Pistol | Ranged | 12 | 3.0/s | 220px | 8 | Ammo paling umum |
| Sawed-off | Ranged | 6×6 | 1.1/s | 90px | 2 | Mematikan <60px |
| Bolt Rifle | Ranged | 45 | 0.8/s | 300px | 5 | Pierce 1, reload 2.2s |
| Nailgun (craft) | Ranged | 7 | 8.0/s | 150px | 30 | Spread 8°, murah |
| Molotov (craft) | Throw | 8/s api | — | radius 48px | 1 | 4s, area denial |
| Crossbow (craft) | Ranged | 60 | 0.6/s | 260px | 1 | **Silent** (heat 0) — senjata malam |

**TTK target** (jangan diubah tanpa mengukur ulang): Walker 30 HP → pistol 3 tembakan / wrench 2 pukulan; Runner 18 HP → 2 tembakan; Tank 150 HP → rifle 4; Spitter 26 HP → 2. Boss/nest: 900 HP.

### 9.3 Combat Feel

```text
□ Screen shake 2–4px (slider di aksesibilitas)
□ Hit-stop 2–3 frame saat kill/crit
□ Blood decal yang bertahan sampai hujan berikutnya
□ Muzzle flash + light 1 frame
□ Knockback konsisten
□ Audio 3 lapis (impact, tail, ducking)
□ Angka damage OPSIONAL (default mati)
```

---

## 10. Zombie

### 10.1 Statistik

| Zombie | HP | Speed | DMG | Atk range | Detect | Muncul | Peran |
|--------|----|-------|-----|-----------|--------|--------|-------|
| **Walker** | 30 | 36 | 8 | 22px | 120px | Hari 1 | Massa, mengajarkan ritme |
| **Runner** | 18 | 96 | 6 | 20px | 140px | Hari 3 | Memaksa dodge |
| **Spitter** | 26 | 44 | 10 + poison 3/s | 90–150px | 130px | Hari 5 | Area denial |
| **Screamer** | 40 | 40 | 5 | 20px | 150px | Hari 6 | Pemanggil; prioritas tertinggi |
| **Tank** | 150 | 30 | 22 | 26px | 110px | Hari 8 | Penghancur pintu |
| **Exploder** | 22 | 64 | 55 (radius 56px) | self | 130px | Hari 9 | Berkedip merah 2s sebelum meledak |
| **Stalker** *(baru, open world)* | 24 | 110 | 12 | 20px | 90px | Hari 12 | Hanya menyerang saat pemain tidak melihat; kabur bila terlihat. Menghukum looting sambil menoleh |
| **The Hive** (nest, landmark) | 900 | 34 | 18/25 | — | — | Hari 10 | 3 fase, spawn add, sumber horde |

Detect maksimum 150px untuk semua tipe. Di atas 160px zombie mendeteksi dari luar layar = tidak adil di resolusi 320×180.

### 10.2 State Machine

```text
   IDLE ◄───────────────────────────────┐
    │                                    │
    │ dengar noise (chunk noise pool)     │ selesai investigasi
    ▼                                    │
 INVESTIGATE ──► lihat pemain ──► CHASE ─┘
                     │              │
                     │ masuk range  │ keluar range
                     ▼              ▼
                  ATTACK ───────► CHASE
                     │ HP ≤ 0
                     ▼
                    DEAD
```

**INVESTIGATE wajib ada.** Tanpa state ini, sistem noise (§7) dan horde yang tertarik suara tidak punya arti.

### 10.3 Implementasi (gaya valid, bukan pseudocode)

```gdscript
# entities/zombie_ai.gd — potongan inti
extends CharacterBody2D

enum State { IDLE, WANDER, INVESTIGATE, CHASE, ATTACK, DEAD }

@export var data: ZombieData
@onready var agent: NavigationAgent2D = $NavigationAgent2D
@onready var body_sprite: AnimatedSprite2D = $AnimatedSprite2D

var state: State = State.IDLE
var target: Node2D = null
var _sight_timer := 0.0
var _repath_timer := 0.0
var _attack_timer := 0.0
var _noise_target := Vector2.ZERO

const SIGHT_INTERVAL := 0.2
const REPATH_INTERVAL := 0.25
const REPATH_MIN_DIST := 32.0

func _physics_process(delta: float) -> void:
    if state == State.DEAD or data == null:
        return
    _sight_timer -= delta
    _repath_timer -= delta
    _attack_timer = maxf(_attack_timer - delta, 0.0)

    match state:
        State.IDLE, State.WANDER:
            _wander()
            if _sight_timer <= 0.0:
                _sight_timer = SIGHT_INTERVAL
                _try_acquire_target()
        State.INVESTIGATE:
            _investigate()
        State.CHASE:
            _chase()
        State.ATTACK:
            _attack()

func _try_acquire_target() -> void:
    var p: Node2D = GameManager.player
    if p == null or not is_instance_valid(p) or GameManager.player_is_dead:
        return
    var detect := minf(data.detection_range * WorldClock.pressure, 150.0)
    if global_position.distance_to(p.global_position) > detect:
        return
    if not _has_line_of_sight(p):
        return
    target = p
    state = State.CHASE

func _chase() -> void:
    if target == null or not is_instance_valid(target):
        target = null
        state = State.IDLE
        return
    if global_position.distance_to(target.global_position) <= data.attack_range:
        velocity = Vector2.ZERO
        state = State.ATTACK
        return
    if _repath_timer <= 0.0:
        _repath_timer = REPATH_INTERVAL
        if agent.target_position.distance_squared_to(target.global_position) > REPATH_MIN_DIST * REPATH_MIN_DIST:
            agent.target_position = target.global_position
    var dir := (agent.get_next_path_position() - global_position).normalized()
    velocity = dir * data.speed * WorldClock.speed_mult
    move_and_slide()
    body_sprite.flip_h = dir.x < 0.0

func _has_line_of_sight(p: Node2D) -> bool:
    var q := PhysicsRayQueryParameters2D.create(global_position, p.global_position, 1)
    return get_world_2d().direct_space_state.intersect_ray(q).is_empty()
```

### 10.4 Performa

- Distance check dulu, raycast kemudian. Deteksi maks 5×/detik per zombie.
- `NavigationAgent2D.target_position` maks 4×/detik.
- Chunk non-aktif: **tidak ada** instance zombie (hanya angka populasi).
- Object pool untuk zombie & proyektil. Jangan `queue_free` + `instantiate` terus-menerus.

---

## 11. Crafting, Resource & Ekonomi

### 11.1 Resource

| Resource | Sumber | Kegunaan |
|----------|--------|----------|
| 🪵 Wood | Furnitur, pintu, pohon, pagar | Barricade, struktur, senjata dasar, bahan bakar |
| 🔩 Scrap | Mobil, mesin, perkakas | Senjata, amunisi, perbaikan, struktur |
| 🔌 Electronics | Toko, panel, komputer | Lampu, generator, turret, radio |
| 🧪 Chemical | Apotek, dapur, spitter | Obat, molotov, amunisi khusus |
| 🧵 Cloth | Rumah, zombie, kasur | Bandage, armor, water collector |
| ⛽ Fuel | Mobil, gudang, generator | Generator, molotov |
| 🍖 Food | Dapur, kaleng, garden | Hunger |
| 💧 Water | Botol, keran, water collector, Water Treatment | Thirst |
| 💊 Medicine | Klinik, hospital, apotek | Heal, infirmary |
| 🔋 Battery | Elektronik, toko | Daya lampu (item, bisa diisi di generator) |

### 11.2 Resep (24 saat 1.0; 16 saat EA)

```text
TIER 1 (tanpa workbench / workbench 1)
  Wood 4 + Scrap 1                       → Bandage (heal 20)
  Chemical 3 + Cloth 2                   → Medkit (heal 50)
  Scrap 5                                → Pistol ammo ×12
  Wood 3 + Scrap 2                       → Torch (radius 80, 90s)
  Wood 6 + Scrap 2                       → Barricade (1 tile, 120 HP)
  Wood 6 + Cloth 8                       → Bed
  Scrap 4 + Wood 2                       → Spike strip
  Scrap 3 + Chemical 1                   → Battery +30 daya

TIER 2 (workbench 2)
  Scrap 20 + Electronics 8 + Fuel 4      → Generator
  Scrap 6 + Electronics 4                → Floodlight
  Cloth 6 + Scrap 4                      → Water collector
  Wood 8 + Water 10                      → Garden plot
  Electronics 4 + Scrap 6 + Cloth 2      → Radio (tier 3 syarat)
  Scrap 10 + Electronics 4               → Nailgun
  Chemical 2 + Cloth 1 + Scrap 1 + Fuel 1→ Molotov
  Wood 2 + Cloth 2 + Scrap 1             → Spear
  Scrap 6 + Electronics 2                → Noisemaker

TIER 3 (workbench 3)
  Scrap 25 + Electronics 12 + Turret part→ Turret
  Scrap 12 + Electronics 10              → Radio tower part
  Scrap 15 + Electronics 5 + Chemical 3  → Crossbow
  Scrap 20 + Electronics 12 + Wood 10    → Wall reinforcement
  Scrap 30 + Electronics 20 + Radio tower part ×3 → Radio Tower
```

**Aturan resep:** tidak ada resep yang isinya cuma "menambah angka kecil". Semua resep harus mengubah cara main atau membuka opsi baru.

### 11.3 Trader

- Lokasi: 2 landmark tetap (Police Checkpoint & Commercial Market). Buka siang saja.
- Restock tiap **3 hari**; barang hilang kalau tidak dibeli.
- Barter: material ↔ material, bukan uang. Rasio dinamis berdasarkan kelangkaan.
- Bisa menjual loot curian (barang berharga) untuk material langka.
- Trader **tidak** ikut diserang (netral, tidak bisa dibunuh, tidak bisa di-rob).

Trader adalah satu-satunya tempat pemain bisa menukar kelebihan kayu menjadi obat. Ini mengubah surplus jadi strategi.

### 11.4 Ekonomi & Inflasi

| Masalah | Solusi |
|---------|--------|
| Pemain menimbun 400 wood | Storage dibatasi per tier (1/2/3 halaman); kelebihan harus dipakai atau dibuang |
| Loot habis | Respawn chunk 7 hari; supply drop event; trader restock |
| Material langka terlalu langka | Electronics & medicine selalu di distrik tetap; pemain belajar peta |
| Uang tidak ada artinya | **Tidak ada uang.** Semua barter → tidak ada inflasi mata uang |

---

## 12. Progresi

Progresi di open world harus **di dalam save**, bukan antar-run. Tiga jalur, semuanya terasa berbeda:

### 12.1 XP & Level

| Sumber XP | Nilai |
|-----------|-------|
| Zombie dibunuh | Walker 1, Runner 2, Spitter 3, Screamer 4, Tank 8, Exploder 3, Stalker 5 |
| Bangunan pertama kali dijelajah | 5 |
| Landmark ditemukan | 25 |
| Hari bertahan | 10 × hari |
| Resep baru dibuat pertama kali | 5 |
| Malam tanpa kerusakan shelter | 15 |

Level butuh `100 × level^1.35` XP (level 2 = 100, level 5 = 800, level 10 = 2.200). Target: level 10–14 saat ending.

### 12.2 Skill Tree (3 cabang, 30 node)

| Cabang | Contoh node | Rasa |
|--------|-------------|------|
| **Combat** | +8% damage, reload −15%, dodge i-frame +0.05s, melee stamina −20%, headshot +crit | Terasa langsung di malam |
| **Survival** | Hunger drain −20%, **+5 kg ×2 node**, +4 slot, loot speed −30%, noise −25%, heal +20% | Terasa di ekspedisi |
| **Engineering** | Craft cost −10%, struktur HP +20%, turret damage +25%, generator heat −30%, battery drain −20%, **drop bag recovery instan** | Terasa di shelter |

Aturan: **tidak ada respec gratis** (biaya: 1 rare item), supaya pilihan terasa. Tapi semua node harus berguna — tidak ada "trap node".

### 12.3 Blueprint

Ditemukan di landmark, kontainer gelap, dan hadiah trader. Blueprint membuka resep yang tidak bisa ditebak. Total 12 blueprint saat 1.0 (6 saat EA).

### 12.4 Hari Bertahan

Metrik utama dan satu-satunya "skor" yang ditampilkan di menu: **Hari bertahan**. Ditambah pencapaian kecil (bangunan terjelajah, landmark, shelter tier).

---

## 13. Kematian, Respawn & Mode

### 13.1 Mengapa Bukan Permadeath Default

Open world berjalan 10–30 jam. Kalau mati sekali = save hilang, pemain berhenti bereksperimen, berhenti keluar saat malam, dan berhenti memainkan game yang kita desain. Jadi default: **mati itu mahal, tapi bukan akhir.**

### 13.2 Kematian (mode Survivor — default)

Saat HP 0:

| Yang terjadi | Detail |
|--------------|--------|
| **Corpse bag** | Semua isi inventory jatuh di lokasi mati sebagai kantong yang bisa diambil kembali. Bertahan **3 hari**, lalu hilang |
| **Respawn** | Di shelter, saat **subuh berikutnya** (kamu kehilangan sisa hari itu) |
| **Yang tetap** | Senjata di hotbar, armor terpakai, semua XP & skill, blueprint yang sudah dipelajari, isi storage shelter |
| **Yang hilang** | Isi inventory (ada di corpse bag), 20% material di storage shelter (dalam kekacauan) |
| **Shelter** | Kalau mati di luar saat malam, shelter terkena auto-resolve serangan malam itu (§6.5) |
| **Debuff** | "Shaken": stamina maks −15% selama 1 hari |

Pengambilan corpse bag adalah **ekspedisi kedua yang wajib** — pemain harus kembali ke tempat ia mati, dan tempat itu sekarang lebih berbahaya (zombie berkumpul di mayat). Ini loop yang bagus; jangan dihapus.

### 13.3 Mode

| Mode | Mati | Save | Untuk siapa |
|------|------|------|-------------|
| **Survivor** | Corpse bag + respawn subuh | Bebas | Default, semua pemain |
| **Hardened** | Kehilangan **100%** inventory, tanpa corpse bag, respawn subuh | Bebas | Pemain yang mau tekanan |
| **Ironman** | **Permadeath, save terhapus** | 1 slot, autosave | Pencari tantangan, streamer |
| **Sandbox** | Seperti Survivor | Bebas + cheat menu | Belajar & bikin konten |

Mode dipilih saat mulai save dan **tidak bisa diubah**.

### 13.4 "Homeless" (bukan game over)

Kalau shelter hancur total dan pemain tidak punya klaim:

1. Pemain tetap hidup dengan isi inventory.
2. Harus klaim shelter baru sebelum malam (**Claim Kit** bisa dibuat dengan 10 wood + 5 scrap — selalu mungkin).
3. Semua isi storage lama hilang.
4. Heat reset ke 0 (jejak hilang bersama rumah).
5. Horde night berikutnya tetap datang.

Ini hukuman terberat yang tidak mematikan save: kamu kehilangan **infrastruktur**, bukan karakter. Cocok dengan tema.

### 13.5 Save

```text
user://save_slot_N/
  meta.json        (versi, mode, hari, seed, hari terakhir save, playtime)
  player.json      (stat, skill, inventory, posisi)
  shelter.json     (lokasi, struktur + HP, storage, heat)
  world_diff.bin   (per-chunk diff: pintu, kontainer, populasi, barricade, corpse bag)
  screenshot.png   (untuk menu save)
```

**Aturan save:**

- Autosave saat: tidur, subuh, masuk/keluar shelter, keluar game.
- Manual save hanya di shelter (bukan di tengah lapangan) — supaya keputusan tidak bisa di-undo.
- Save size target < 8 MB. Diff per chunk disimpan sparse (hanya chunk yang berubah).
- Anti-cheat tidak diprioritaskan (singleplayer), tapi dicegah save-scum di tengah ekspedisi: kalau load dari autosave terakhir, dunia memakai state autosave (tidak ada rollback pilihan).

---

## 14. Kemenangan & Ending

### 14.1 Jalan Menuju Ending

```text
1. Temukan Radio Station (landmark)          → blueprint radio tower
2. Bangun Radio (shelter tier 3)
3. Kumpulkan 3× Radio Tower Part            → Police / Quarantine / Hospital
4. Bangun Radio Tower di shelter tier 3
5. Pancarkan sinyal → SEMUA zombie di kota tertarik ke sheltermu
6. Bertahan 3 malam berturut-turut (heat 100, horde penuh, tanpa tidur)
7. Evakuasi → ENDING
```

Langkah 5–6 adalah puncak game: pemain yang selama ini menghindari heat, sekarang **sengaja** menarik seluruh kota. Durasi ±20 menit gameplay terkonsentrasi.

**The Hive opsional (Q3):** menyerang sarang tidak diperlukan untuk ending. Tapi menghancurkannya memberi **heat global −25** dan mengurangi frekuensi horde — jadi pemain yang memilih jalan sulit mendapat keuntungan nyata, tanpa dipaksa. Ini juga memberi dua profil ending: "cepat dan berisiko" vs "bersihkan dulu, baru pergi".

### 14.2 Ending

| Ending | Syarat | Isi |
|--------|--------|-----|
| **Extraction** | Sinyal + 3 malam | Helikopter datang, kamu naik. Epilog: kota tetap di belakang |
| **The Last Broadcast** | Sinyal + 3 malam + shelter utuh tanpa kerusakan | Kamu bertahan tanpa kehilangan apa pun; ending "bersih" |
| **Endless** | Pemain bisa memilih lanjut setelah sinyal | Kota tetap, hari terus bertambah, horde terus naik. Untuk pencari rekor |

Endless penting: sebagian pemain tidak mau game-nya selesai. Jangan paksa.

---

## 15. UI / UX

### 15.1 HUD

```text
┌──────────────────────────────────────────────────┐
│ ♥100 ⚡85 🍖72 💧60 🔋62   ⚖ 31/40kg HARI 6 ☀4:12 │
│                                                  │
│                  [ GAME WORLD ]                  │
│                                                  │
│  ┌──┬──┬──┬──┐                 ┌──────────┐      │
│  │🪓│🔫│🩹│🔥│  hotbar         │ minimap  │      │
│  └──┴──┴──┴──┘                 │ ▓▓🏠☠·▓  │      │
│                                └──────────┘      │
│  [ HEAT ▮▮▮▮▯▯ 52 — SERANGAN MUNGKIN ]          │
└──────────────────────────────────────────────────┘
```

Wajib terlihat tanpa buka menu: HP, stamina, hunger, thirst, battery, **berat (kg + status Ringan/Bermuatan/Berat/Kelebihan)**, **hari**, **jam + fase**, **heat**, hotbar, minimap, indikator arah horde.

Berat ditampilkan sebagai `31/40 kg` **plus warna** (hijau/kuning/oranye/merah). Saat pemain masuk status Berat, muncul ikon kecil di dekat ikon karakter — bukan popup, bukan notifikasi yang bisa terlewat. Pemain harus bisa merasakan "saya melambat" tanpa membuka menu.

Heat ditampilkan sebagai **bar + label** ("tenang / waspada / berisik / terlalu berisik"), bukan angka mentah saja. Pemain harus paham "kenapa malam ini ramai".

### 15.2 Layar

`Main Menu` · `Save Select` · `Mode Select` · `Game` · `Pause` · `Inventory` · `Crafting` · `Shelter Panel` · `Map` · `Journal (bestiary + resep + landmark)` · `Night Report` · `Death Screen` · `Settings` · `Tutorial`

**Night Report** adalah layar baru yang penting: ringkasan tiap subuh (zombie dibunuh, struktur rusak, heat akhir, loot masuk, XP). Ini yang membuat progres terasa.

### 15.3 Aturan UX

- Tidak ada menu yang menutupi seluruh dunia saat malam berlangsung — inventory malam hari menampilkan jam + heat di pinggir.
- Semua aksi berdurasi (barricade, reload, loot) punya progress bar di dunia, bukan di HUD.
- Resolusi native 320×180: UI di CanvasLayer dengan skala terpisah (2×/3×), bukan ikut dunia.
- Setiap telegraph audio punya padanan visual (ikon + panah arah).
- Map (M) menampilkan: distrik yang sudah dijelajah, shelter, landmark ditemukan, corpse bag aktif. Bukan peta penuh dari awal.

---

## 16. Audio

| Kategori | Arah |
|----------|------|
| BGM Siang | Ambient drone, gitar/piano minim, "sunyi yang tidak nyaman" |
| BGM Senja | Denyut lambat, ritme naik saat jam mendekati malam |
| BGM Malam | Bass, langkah, distorsi; intensitas naik sesuai heat |
| BGM Serangan | Perkusi + pad; berhenti saat gelombang berakhir (jeda sengaja sunyi) |
| BGM Horde Night | Paduan suara + drum berat |
| SFX Zombie | 3 lapis: geraman dekat, jeritan jauh, langkah (memberi arah) |
| SFX Shelter | Pintu berderit, palu, generator menyala/mati, kaca pecah — **audio shelter adalah informasi** |
| SFX Heat | Dengung listrik naik seiring heat; senyap saat heat diturunkan |
| SFX Event | Signature unik per event |
| SFX UI | Klik, craft, notifikasi, loot |

Aturan: pemain harus bisa mengenali **"pintu mana yang sedang dipukul"** dari suara saja. Ini yang membuat bertahan di dalam shelter menegangkan tanpa melihat ke luar.

---

## 17. Art Direction & Asset Spec

### 17.1 Prinsip

| Item | Nilai |
|------|-------|
| Resolusi native | 320×180, integer scale ke 1280×720 / 1920×1080 |
| Tile | 16×16 |
| Sprite karakter | **24×32** (1,5 × 2 tile) — dinaikkan dari 16×24 di v3.14; lihat §17.3C |
| Palet | 32 warna global + 6 warna aksen per distrik |
| Mood | Gelap, kotor, terbaca. Aksen merah (darah), kuning (api/listrik), hijau (racun) |
| Filter | Nearest, mipmaps OFF, pixel snap ON |
| Arah sprite | **8 arah** (S, SE, E, NE, N, NW, W, SW) — digambar **5 arah**, 3 sisanya mirror di runtime (hemat 37,5%). Senjata tetap berputar bebas sebagai node |

**Aturan keterbacaan (tidak bisa dinegosiasikan):**

1. **Siluet dulu, warna kemudian.** Tiap zombie harus bisa dibedakan dari bentuknya saja di layar 320×180 — karena itu syarat utama agar pemain buta warna tetap bisa main.
2. **Outline 1px** pada karakter dan prop penting; tanah tidak diberi outline.
3. **Pemain adalah titik kontras tertinggi di layar.** Satu warna aksen (jaket teal) **dilarang** dipakai di lingkungan.
4. **Tidak ada anti-aliasing, tidak ada gradien halus.** Hanya ramp 3–4 langkah per material.
5. **Gerakan sprite di-snap ke piksel.** Kamera boleh halus; sprite tidak.

### 17.2 Tileset

**Struktur atlas**

| Item | Nilai |
|------|-------|
| Ukuran atlas | 512×512 px = 32×32 tile (1024 tile per atlas) |
| Tile per distrik | **±260 tile** (nyaman di 1 atlas 1024 tile, 1 texture = 1 draw call) |
| Layer | ground / wall / roof / deco / props (5 `TileMapLayer` terpisah) |
| Terrain mode | Ground & wall: **Match Corners and Sides** (47-tile blob). Pagar, pipa, rel: **Match Sides** (16 tile) |
| Collision | Wall layer punya collision polygon per tile; ground tanpa collision |

**Isi tileset per distrik (±263 tile):**

| Grup | Tile | Catatan |
|------|------|---------|
| Ground blob | 47 × 3 material = 141 | Contoh Suburban: rumput, tanah, aspal. Distrik lain boleh 2 material |
| Sidewalk / tepi jalan | 16 | Match Sides |
| Wall top blob | 47 | Permukaan atas dinding (yang terlihat dari kamera) |
| **Wall face** | **16** | Muka dinding 10 px: depan, ujung, sudut dalam/luar — ini yang membuat dinding terlihat punya tinggi (§17.12) |
| **Low wall / rail** | **6** | Muka 6 px, bisa dilewati peluru (pagar, tembok rendah, tiang) |
| Roof | 15 | Hanya 1 sisi terlihat (top-down miring), di-fade saat pemain masuk bangunan |
| Pintu | 12 | 3 material × 4 state (tertutup, terbuka, dibarricade, rusak) |
| Jendela | 8 | 2 material × 4 state; dipotong dari wall face, **bukan** sprite menghadap 4 arah (§4.2B) |
| Tangga | 4 | Naik/turun, 2 orientasi |
| Dekorasi lantai | 20 | Karpet, retakan, darah kering, sampah |
| **Subtotal** | **±285** | Muat di 1 atlas 1024 tile dengan sisa untuk ekspansi |

**Prop TIDAK masuk tileset distrik.** Prop disimpan di atlas bersama (`props_interior.png`, `props_exterior.png`) supaya bisa dipakai ulang di semua distrik — ini menghemat 40–60% pekerjaan prop:

| Prop | Jumlah | Catatan |
|------|--------|---------|
| Prop kecil (interior) | 40 | Kursi, kaleng, bata, pot, kabel, bingkai |
| Prop besar (interior) | 24 | Lemari, rak, kasur, meja, mesin kasir |
| Prop eksterior | 30 | Mobil (4 warna × 2 kondisi), gerobak, bangku, pagar, tiang listrik |

**Aturan tileset:**

- **Jangan pernah** menaruh detail penting di 1 piksel tile. Di 320×180, 1 piksel = 1/180 tinggi layar; detail halus hilang saat di-scale.
- Semua pintu & jendela adalah **objek state**, bukan tile statis — state-nya disimpan di diff chunk (§4.4), supaya bisa dibuka/dibarricade/rusak.
- Roof layer otomatis di-fade (alpha 0,3) saat pemain di dalam footprint bangunan (Area2D per bangunan → set `modulate.a` layer).
- Tileset per distrik **tidak** dibuat semua sekaligus: EA hanya butuh 5 (Suburban, Commercial, Industrial, Hospital, Mall).

**Collision layer (dipakai konsisten):**

| Layer | Isi |
|-------|-----|
| 1 | Dinding / obstacle statis |
| 2 | Pemain |
| 3 | Zombie |
| 4 | Prop destruktibel (pintu, jendela, barricade) |
| 5 | Interaksi (kontainer, lift, kasur, trader) |
| 6 | Trigger area (zona shelter, zona horde) |

### 17.3 Sprite Pemain

| Item | Nilai |
|------|-------|
| Canvas | **24×32**, pivot di **(12, 31)** — kaki di baseline, bukan tengah |
| Collision | **12×10** di kaki (bukan seluruh sprite) — supaya gerak di lorong sempit tidak terasa mentok |
| Arah | **8** (S, SE, E, NE, N, NW, W, SW). Digambar 5, mirror 3 |
| Total frame di atlas | **240** (30 × 8 arah) · atlas 720×160 |
| **Frame yang harus digambar** | **150** (30 × 5 arah) — 90 frame dihemat lewat mirror |

**Kenapa 8 arah, dan bagaimana biayanya tidak jadi 2× (keputusan v3.6):**

Pemain bergerak 8 arah (WASD/stick), jadi sprite 4 arah membuat gerak diagonal terlihat "menggeser" bukan berjalan. Dengan 8 arah, arah hadap **selalu mengikuti arah gerak**, sementara senjata tetap berputar bebas ke kursor — ini yang membuat gerakan terasa cair tanpa perlu menggambar 240 frame.

```text
Digambar (5 baris):  S · SE · E · NE · N
Mirror di runtime :  SW = SE flip_h · W = E flip_h · NW = NE flip_h
```

```gdscript
# entities/player_sprite.gd — arah 8 arah + mirror, tanpa frame ekstra
const ANIM := ["s", "se", "e", "ne", "n", "ne", "e", "se"]
const FLIP := [false, false, false, false, false, true, true, true]
# index 0..7 = S, SE, E, NE, N, NW, W, SW

func apply_dir(dir: Vector2, anim_base: String) -> void:
    if dir == Vector2.ZERO: return
    var idx := int(round(dir.angle() / (PI / 4.0)))      # -4..4
    idx = posmod(idx + 6, 8)                              # geser: 0 = arah S
    sprite.play(StringName(anim_base + "_" + ANIM[idx]))
    sprite.flip_h = FLIP[idx]
```

> Catatan asimetri: mirror hanya sah kalau desain karakter **simetris secara horizontal** (baju, rambut pendek, tanpa tas selempang). Kalau nanti ada detail asimetris (mis. tas di satu bahu), baris mirror harus digambar manual untuk bagian itu — atau detailnya dipindah ke layer aksesori terpisah.

| Animasi | Frame | FPS | Catatan |
|---------|-------|-----|---------|
| idle | 2 | 3 | Napas halus |
| walk | 6 | 8 | Dipakai juga untuk sprint di FPS 12 (hemat 24 frame) |
| attack_melee | 4 | 12 | Frame 2 adalah hitbox aktif |
| attack_ranged | 3 | 12 | Recoil 1 frame |
| hurt | 2 | 10 | Tidak boleh >0,2s, biar tidak menghambat |
| death | 6 | 10 | Frame terakhir di-hold |
| dodge | 4 | 14 | Roll, arah mengikuti input |
| interact | 3 | 8 | Looting, buka pintu, tidur |

**Variasi pemain tanpa biaya seni baru:** palet jaket 3 varian (teal default, oranye, abu) lewat `ShaderMaterial` palette swap. Ini memberi "3 survivor" tanpa menggambar ulang satu frame pun.

### 17.3B Set Final v1 — Sudah Ada, Bukan Template

Pemain sudah punya set lengkap: **150 frame digambar** (30 × 5 arah), atlas `480×120`, dipakai langsung oleh `SpriteFactory.player_frames()`. Generator: `tools/make_player_sprites.py`. Lembar review: `docs/art/player-character-sheet.png` dan `docs/art/player-sheet-final.png`.

**Keputusan seni yang mengikat karakter lain** (dipakai juga untuk zombie & NPC, supaya gaya konsisten):

| Keputusan | Nilai | Alasan |
|---|---|---|
| Arah cahaya | **dari atas**, bukan kiri-atas | Baris E/SE dipakai juga sebagai W/SW lewat `flip_h`. Cahaya dari kiri akan terbalik saat mirror dan karakter terbaca berbeda. Ini konsekuensi langsung dari strategi mirror §17.3, bukan selera. |
| Kepala | **6 px**, bahu 8 px (rasio 0,75) | Wajah 5 px menyisakan 1 px di antara kedua mata — pada 320×180 itu terbaca seperti topeng/pelindung mata. |
| Tangan & sepatu | 1 nada lebih terang dari lengan/kaki | Menandai ujung anggota badan tanpa menambah outline (yang akan menebalkan siluet 14 px). |
| Pemisah bagian | **selout** 1 px (nada gelap di tepi dalam) | Tanpa selout, lengan dan badan menyatu jadi satu blok. |
| Simetri | **wajib** — tidak ada tas selempang / tambalan satu sisi | Detail asimetris membatalkan baris mirror, biaya naik ±60% (§17.3). |
| Palet | **26 warna**, 3 langkah per material | Batas §17.1: 32 global; tanpa anti-aliasing, tanpa gradien halus. |

### Proporsi — diukur dari referensi, bukan selera

Permintaan "semirip manusia" tidak bisa dijawab dengan perasaan, jadi diukur dari foto model berdiri penuh (`image-search/...reference-3.jpg`, diukur otomatis lewat ambang kontras):

| Ukuran | Foto (px) | Rasio | Kanvas 24 px | Sprite |
|---|---|---|---|---|
| Tinggi total | 1063 | 1,00 | 24 | 24 |
| Tinggi kepala | ~144 | 13,5% | 3,2 | **5** (20,8%) |
| Bahu | 240 | 22,6% | 5,4 | 10–11 |
| Lebar kepala | 96 | 9,0% | 2,2 | 6 |
| **Bahu : kepala** | | **2,5** | | **1,7–1,8** |
| Leher | 50 | 4,7% | 1,1 | 1 |
| Badan (leher–crotch) | 428 | 40,3% | 9,7 | 7 |
| Kaki (crotch–telapak) | 441 | **41,5%** | 10,0 | **10** |

**Kepala 3 px tidak mungkin** — tidak ada ruang untuk dua mata. Jadi satu-satunya penyimpangan yang boleh adalah kepala: **5 px**, yang menyerap seluruh selisih (20,8% vs 13,5%). Konsekuensinya **kaki tetap 10 px = 41,7%**, praktis sama dengan manusia asli.

Versi sebelumnya (v1) memakai kepala 6 + kaki 8 = **1:3,8 kepala** — itu proporsi chibi, dan itulah sebabnya sprite terlihat "kurang manusia" meski shadingnya benar. v2 = **1:4,8** dengan kaki 42%.

#### Aturan wajah di 16×24 (hasil percobaan, bukan selera)

Wajah adalah bagian yang paling cepat gagal di kanvas 16×24. Diuji **6 varian** dan diperiksa pada zoom 14× *dan* skala main 4× (karakter 24 px di layar 320×180, sesuai ukuran sebenarnya dilihat pemain):

| Aturan | Kenapa | Kalau dilanggar |
|---|---|---|
| Minimal **3 baris**: rambut / **dahi** / mata | Dahi adalah pemisah antara massa rambut gelap dan mata gelap | Mata menempel di bawah rambut → keduanya menyatu jadi satu blok hitam; wajah hilang, kepala terbaca sebagai helm |
| Sisi baris mata = **kulit**, bukan rambut | Mata butuh latar terang untuk terbaca | Kedua mata menyatu dengan rambut di kiri-kanan → wajah terbaca sebagai topeng |
| Hidung **2 px terang** di bawah mata | Memberi tonjolan tengah wajah | Wajah rata, tanpa kedalaman |
| Mulut **2 px** `y` (bukan 1 px) | 1 px tidak terbaca, hanya menambah kotoran | Ekspresi hilang |
| Kepala **tidak boleh < 6 baris** | 5 baris = rambut+dahi+mata+mulut tanpa dagu | Dagu menempel di leher, wajah terasa terpotong |

**Konsekuensi yang harus diterima:** wajah yang terbaca menuntut kepala **6 baris (5 px)**, sehingga rasio kepala menjadi **1:4,8**, bukan 1:7,4 seperti manusia asli. Ini bukan kemalasan — pada 1:7,4 kepala hanya 3 px dan **tidak ada satu pun** dari 6 varian yang berhasil. Pilihan sebenarnya adalah: proporsi anatomis dengan wajah kosong, atau proporsi 1:4,8 dengan wajah yang terbaca. Di game bertahan hidup, wajah yang terbaca lebih penting.

**Aturan lengan (ditemukan saat koreksi yang sama):** baris bahu **harus menyambung** ke lengan (14 px penuh). Kalau lengan hanya ditempel 1 px di luar badan tanpa baris bahu, hasilnya terbaca sebagai **kaus tanpa lengan**, bukan jaket.

**Hasil uji keterbacaan.** Dua bagian: yang bisa diperiksa mesin (dijalankan otomatis setiap generate) dan yang harus dinilai mata.

```text
Otomatis (tools/make_player_sprites.py -> validate()):
  sel diperiksa      : 150
  sel kosong         : 0
  isi menyentuh tepi : 0        (outline boleh, isi tidak)
  isi di baris 0     : 0        (ruang untuk topi/aksesori kepala)

Manual (zoom 12x-20x):
  Siluet terbaca tanpa warna (teal -> abu-abu)?   -> YA, bahu vs pinggang berbeda
  Mata terbaca terpisah di wajah 6 px?           -> YA (2 px jarak antar mata)
  Arah hadap terbaca dari siluet saja?           -> YA (hidung di E, tas di N)
  Dua kaki terpisah, tidak jadi satu balok?      -> YA (celah 1 px + selout)
  Tas terbaca sebagai tas, bukan bongkahan?      -> YA di N/NE/E; hanya tali di S/SE
```

**Yang belum ada di v1 — jangan dianggap selesai:**

1. Transisi `death` dan `dodge` masih pose tunggal; belum di-keyframe per frame seperti walk.
2. Belum ada varian `hurt` yang berbeda per arah serangan.
3. Palette swap oranye/abu (§17.3) belum dibuat, tapi tinggal mengganti huruf `j/J/k` di generator.
4. Belum ada senjata di tangan — sesuai §17.1, senjata adalah node terpisah yang berputar bebas.

### 17.3C Kanvas Dinaikkan 16×24 → 24×32 (v3.14)

Referensi visual eksternal (288×52, karakter ~51 px) menunjukkan proporsi **1:4** untuk karakter yang terbaca bagus. Proporsi kita sudah 1:4 sejak v3.12 — jadi selisihnya **bukan proporsi, tapi resolusi**: di 16×24 wajah hanya kebagian 3 baris, dan 3 baris tidak cukup untuk rambut + dahi + mata.

| Item | 16×24 (v1–v2) | **24×32 (v3.14)** |
|---|---|---|
| Kepala | 6 baris (25%) | **8 baris (25%)** — 6 baris khusus wajah |
| Wajah | 3 baris | **6 baris**: rambut ×2, dahi, mata, hidung, mulut |
| Badan | 7 baris | 10 baris |
| Kaki | 10 baris (42%) | **13 baris (41%)** |
| Piksel per sel | 384 | 768 |
| Pivot | (8,23) | **(12,31)** |
| Collider | 10×10 | **12×10** |
| Shadow | 14×7 | **16×7** |
| Atlas | 480×120 | **720×160** |

**Aturan simetri kanvas (baru, wajib):** kanvas 24 px punya sumbu cermin di **x=11,5**, sedangkan siluet selebar 16 px (bahu) berpusat di x=11,5 hanya kalau ia menempati x4..x19. Kalau tidak persis, `flip_h` untuk arah W/SW menggeser karakter **1 px** dan jalannya terlihat pincang. Ini sudah dicek otomatis: piksel yang berbeda antara frame S dan cerminnya **78 dari 440** — semuanya berasal dari shading asimetris (rambut disisir), bukan dari pergeseran siluet.

**Biaya:** semua aset karakter lain (7 tipe zombie, NPC) kini harus 24×32 juga. Kalau tidak, satu layar akan berisi dua resolusi karakter dan itu langsung terlihat. Zombie walker tetap 16×24 sampai setnya dibuat — ini utang teknis yang dicatat, bukan dilupakan.

### 17.4 Sprite Zombie

| Zombie | Canvas | Frame/arah | Atlas (×8) | Digambar (×5) | Siluet yang membedakan |
|--------|--------|-----------|-----------|---------------|------------------------|
| Walker | 16×24 | 16 | 128 | **80** | Bungkuk, tangan menjuntai |
| Runner | 16×24 | 16 | 128 | 80 | Condong ke depan, langkah lebar |
| Spitter | 16×24 | 16 (+3 spit) | 152 | 95 | Perut besar, leher panjang |
| Screamer | 16×24 | 16 | 128 | 80 | Kurus, mulut terbuka permanen |
| Tank | 24×32 | 16 | 128 | 80 | Massif, bahu lebar, 1,5× tinggi pemain |
| Exploder | 16×24 | 16 | 128 | 80 | Bengkak, urat menyala (2 frame pulsing) |
| Stalker | 16×24 | 16 (+4 leap) | 160 | 100 | Sangat kurus, merunduk, hampir menyentuh tanah |
| **The Hive** (boss) | 48×48 | 30 | 30 | 30 | Sarang besar, bukan humanoid; 3 fase visual |

Total zombie humanoid: **896 frame di atlas, ±595 frame digambar** (7 tipe). Tanpa strategi mirror, angka ini akan jadi 1.152 frame digambar — itulah alasan mirror dipakai, bukan karena malas.

**Aturan arah untuk zombie:** zombie juga 8 arah + mirror, karena mereka mengejar pemain secara diagonal hampir sepanjang waktu. Zombie 4 arah akan terlihat "meluncur" — dan itu merusak salah satu hal terbaik di game ini: melihat kerumunan datang dari sudut.

**Aturan zombie:**

- **Walk 4 frame, bukan 6.** Gaya jalan zombie (pincang) justru lebih terbaca dengan 4 frame; ini menghemat 33% animasi walk di 7 tipe.
- **Jangan bedakan tipe hanya dengan warna.** Runner merah vs Walker hijau = gagal untuk buta warna. Bedakan dengan **postur, tinggi, dan lebar**.
- Exploder wajib punya **pola kedip** (bukan cuma warna) 2 detik sebelum meledak — ini telegraph, bukan hiasan.
- Detail kecil (jam tangan, luka, seragam) hanya di 1 frame idle, tidak di semua frame.
- Zombie **boleh asimetris** (baju robek di satu sisi) karena mayat tidak harus simetris — tapi kalau asimetris, baris mirror tidak bisa dipakai dan biayanya naik ±60%. Untuk EA: **jaga simetri**, taruh kerusakan di tekstur/warna, bukan di bentuk.

### 17.5 Sprite NPC

Keputusan scope: **NPC = trader saja** (2 lokasi, §11.3). Tidak ada companion AI, tidak ada survivor yang bergerak bebas (anti-pilar §2.3).

| NPC | Canvas | Frame | Animasi |
|-----|--------|-------|---------|
| Trader A (Police Checkpoint) | 16×24 | 8 | idle 2, talk 4, gesture 2 |
| Trader B (Commercial Market) | 16×24 | 8 | idem, palet & pakaian beda |
| Props trader | 16×32 | — | Meja, tenda, kotak dagangan, papan harga |

**"NPC rasa" tanpa AI (ditunda ke pasca-1.0, Q11):** 3–5 sosok statis di landmark — duduk, sudah mati, atau membelakangi player sambil memegang catatan. Tidak bisa diajak bicara; hanya memberi cerita lewat posisi. Biaya: 1 frame per sosok + 1 prop. Bukan dipotong permanen — disimpan untuk pengembangan setelah 1.0, karena tidak mengubah gameplay dan tidak boleh menahan jadwal.

> **Catatan penting:** dokumen ini mengunci NPC ke trader. Kalau kamu ingin NPC yang bergerak, berdagang sambil berjalan, atau menemani — itu sistem baru (pathfinding, jadwal, dialog, state) dan menambah ±4–6 minggu. Belum ada di scope; kalau diinginkan, harus diputuskan sebelum Phase 4.

### 17.6 Prop, Item, Efek, UI

| Kategori | Jumlah | Canvas | Catatan |
|----------|--------|--------|---------|
| Item icon | ±60 | 16×16 | Dibaca di inventory & dunia |
| UI icon | ±40 | 8×8 dan 16×16 | HP, stamina, hunger, thirst, battery, heat |
| Senjata (dunia) | 10 | 16×8 | 1 sprite per senjata, rotasi lewat node |
| Struktur shelter | ±14 | 16×16 / 16×32 | Pintu, jendela, generator, turret, kasur, kebun |
| Efek | ±20 | 16×16 / 32×32 | Darah 4, muzzle 2, impact 3, asap 4, api 4, percikan 3 |
| Corpse bag | 1 | 16×16 | Harus sangat mudah dikenali (ikon + warna) |
| Kereta dorong | 1 | 16×24 | Opsional (Q7) |

**Aturan item icon:** semua icon digambar **pada grid yang sama** dengan pencahayaan dari kiri atas. Icon yang "menyala dari bawah" akan terlihat seperti aset dari game lain.

### 17.7 Naming, Atlas & Import Godot

```text
assets/sprites/
├── chars/player/player.png          + player.tres (SpriteFrames)
├── chars/zombies/walker/walker.png  + walker.tres
├── chars/npc/trader_a.png           + trader_a.tres
├── tiles/suburban/suburban.png      + suburban_tileset.tres
├── props/props_interior.png
├── items/icons_16.png               + atlas .tres
├── ui/icons_ui.png
└── fx/fx_blood.png
```

| Aturan | Nilai |
|--------|-------|
| Awalan nama | `chr_`, `zom_`, `npc_`, `tile_`, `prop_`, `icon_`, `fx_`, `ui_` |
| Nama animasi di SpriteFrames | `walk_s`, `walk_n`, `walk_e`, `attack_melee_s`, `death_e` (arah di akhir) |
| Format | PNG, 1 atlas per karakter (bukan 1 file per frame) |
| Import | Filter OFF, Mipmap OFF, Compress **Lossless**, Fix Alpha Border ON |
| Pivot | Karakter: `(8, 23)` · Prop: sesuai titik duduk di lantai |
| Y-sort | Semua karakter & prop pakai Y-sort berdasarkan kaki; prop diberi `y_sort_offset` bila perlu |

**Kenapa 1 atlas per karakter:** puluhan file PNG kecil = ratusan draw call dan load stutter. 1 atlas = 1 texture = 1 draw call per karakter, dan `SpriteFrames` bisa menunjuk `AtlasTexture` di dalamnya.

### 17.8 Volume & Jadwal Aset (ini critical path)

Perkiraan kerja **1 pixel artist penuh waktu**:

| Pekerjaan | Perkiraan |
|-----------|-----------|
| Tileset 1 distrik (±260 tile) | 2,5 minggu |
| Player (150 frame digambar, 8 arah) | 1,3 minggu |
| 1 zombie humanoid (80 frame digambar) | 4,5 hari |
| 7 zombie + boss (±595 frame) | 6,5 minggu |
| Prop interior + eksterior | 3 minggu |
| Item + UI icon | 1,5 minggu |
| Efek + polish | 1 minggu |
| **Total 5 distrik (EA)** | **±27 minggu** |
| **Total 8 distrik (1.0)** | **±35 minggu** |

Art adalah **jalur kritis** proyek ini, bukan coding. Konsekuensi yang harus diterima sekarang:

1. **Untuk EA (minggu 28):** 5 distrik **tidak akan selesai** oleh 1 artist tanpa mulai sejak minggu 1. Pilih salah satu: (a) 2 artist, (b) EA dengan 3 distrik bernuansa lengkap + 2 distrik "greybox bertekstur", atau (c) mundurkan EA ke minggu 34.
2. **Placeholder sampai minggu 14** (§17.9). Jangan ada seni final sebelum slice lulus gate.
3. **Pangkas biaya dengan cara yang tidak terlihat:**
   - **8 arah dengan 5 baris + mirror**: −37,5% frame (90 frame player, ±300 frame zombie)
   - Walk zombie 4 frame (bukan 6): −33% animasi walk
   - **Base body + varian**: 1 rig humanoid (walker) dipakai semua zombie, varian hanya kepala/torso/aksesori → hemat **±35%**
   - Player sprint memakai walk di FPS lebih tinggi: −24 frame
   - Palette swap untuk variasi karakter: 0 frame tambahan
   - NPC statis (bukan berjalan): 0 sistem tambahan

**Kalau waktu seni mepet, urutan pemangkasan:** NPC rasa (§17.5) → distrik 5 → variasi prop → frame walk 6→4 di player → efek polish. **Jangan** pernah memangkas: telegraph zombie, state pintu/jendela, atau icon HUD.

### 17.9 Placeholder & Sumber Seni

| Tahap | Yang dipakai |
|-------|--------------|
| Phase 0–1 (minggu 1–7) | Kotak berwarna + 1 tileset gratis (mis. Kenney/itch.io CC0), siluet karakter dari kotak |
| Phase 2–3 (minggu 8–19) | Placeholder bertekstur: 3 warna per distrik, sprite karakter 4 frame jalan saja |
| Phase 4+ (minggu 20+) | Seni final bertahap, distrik per distrik |

**Aturan placeholder:** semua placeholder harus punya ukuran canvas, pivot, dan nama animasi **yang sama** dengan seni final. Kalau tidak, penggantian seni nanti akan memakan waktu coding yang tidak direncanakan.

**Opsi sumber seni:** **1 pixel artist kontrak 5–6 bulan** (diputuskan, Q10). Tileset komersial boleh dipakai untuk ground/wall bila perlu, **karakter wajib custom** — gaya campur pada karakter langsung terasa murah. NPC rasa (Q11) **disimpan untuk pengembangan pasca-1.0**, bukan dipotong permanen.

### 17.11 Proyeksi: Kenapa Top-Down, Bukan Isometrik (keputusan v3.7)

Pertanyaan ini wajar muncul: isometrik terlihat lebih "mahal" dan lebih cocok untuk game yang menjual *rumah yang kamu bangun*. Tapi untuk game **ini**, dengan resolusi dan kapasitas yang sudah dikunci, isometrik kalah di tiga hal yang tidak bisa ditawar.

**Perbandingan langsung:**

| Aspek | Top-Down (sekarang) | Isometrik 2:1 | Selisih |
|-------|---------------------|---------------|---------|
| Tile | 16×16 persegi | 32×16 belah ketupat | — |
| **Area yang terlihat di 320×180** | **±220 tile** (20×11) | **±110–130 tile** | **isometrik ± separuh** |
| Collision & pathfinding | AABB persegi, langsung | matematika diagonal, navmesh per belah ketupat | +3–4 minggu sistem |
| Okclusion dinding | atap di-fade per bangunan | shader transparan per occluder, terus-menerus | +4–6 minggu + bug visual |
| 8 arah sprite | 5 baris digambar + 3 mirror | 5 baris, tapi tiap pose lebih mahal (±13–18 jam vs 8) | +25–35% waktu sprite |
| Tileset per distrik | ±263 tile | ±500–650 tile (belah ketupat + sisi dinding 2 arah) | **±2× waktu tileset** |
| Audio/visual readability | jarak & arah jelas | diagonal lebih sulit dibaca di layar kecil | risiko desain |
| Waktu seni total (8 distrik) | ±35 minggu | **±55–70 minggu** | +20–35 minggu |

**Tiga alasan yang menentukan:**

1. **Area pandang jadi separuh.** Di 320×180, tile isometrik 32×16 hanya memberi ±10 kolom belah ketupat. GDD ini sudah menulis bahwa 20×11 tile itu sempit — 18 zombie sudah "banjir" (§5.4). Dengan isometrik, jumlah zombie harus diturunkan lagi **atau** resolusi dinaikkan (yang menaikkan biaya seni lagi). Untuk game yang intinya *melihat kerumunan datang*, memotong separuh pandangan adalah kemunduran.
2. **Okclusion membunuh keterbacaan.** Di isometrik, dinding dan atap **selalu** menutupi sesuatu. Solusi standarnya adalah shader transparan per occluder — dan itu sumber bug klasik: karakter hilang di balik sudut, barricade tidak terlihat, zombie datang dari balik dinding tanpa terlihat. Pilar 5 kita ("bahaya terbaca, tidak ada kematian dari off-screen") langsung bertabrakan dengan ini.
3. **Satu artist, 35 minggu vs 55–70 minggu.** Isometrik bukan pilihan gaya, itu pilihan anggaran. Dengan 1 artist (Q10) dan EA di minggu 28, isometrik berarti EA bergeser 5–7 bulan.

**Yang dipakai sebagai gantinya: Top-Down "3/4 dengan tinggi" (bukan isometrik):**

Kedalaman visual tetap didapat, tanpa membayar harga isometrik:

| Teknik | Efek yang didapat | Biaya |
|--------|-------------------|-------|
| **Wall face tile** (dinding punya muka 8–12px) | Bangunan terlihat punya tinggi, bukan garis | 1 varian tile per material |
| **Roof fade** saat pemain masuk | Kamu "masuk rumah", bukan "masuk kotak" | sudah ada (§17.2) |
| **Drop shadow** di bawah karakter & prop | Karakter tidak terlihat mengambang | 1 sprite blur per ukuran |
| **Prop tinggi** (lemari, rak, pagar) digambar dengan muka | Interior terasa beruang | masuk atlas prop |
| **Lighting bertingkat** + prop gelap | Malam terasa punya volume | sudah ada (Battery/Light2D) |
| **Lantai 2 lewat tangga** (pindah layer, bukan kamera isometrik) | Verticality untuk vantage point & loot | sudah ada (§4.3) |

Ini pendekatan yang dipakai Nuclear Throne, Hotline Miami, Darkwood, dan Project Zomboid — semuanya terasa punya tempat, tanpa satu baris matematika diagonal.

**Kalau tetap ingin isometrik**, ini yang harus diubah lebih dulu (jangan mulai seni sebelum semuanya beres):

```text
1. Resolusi naik ke 480×270 (agar area pandang tidak separuh) → semua template aset dibuat ulang
2. Tile jadi 32×16 + aturan collider baru → map generator, BSP, autotile, streaming ditulis ulang
3. Navmesh per belah ketupat → uji ulang AI 8 tipe zombie, termasuk Tank 24×32 → 32×40
4. Occlusion system (shader + sorting) → tambah 4–6 minggu dan satu kelas bug baru
5. Jadwal: EA minggu 28 → minggu 40–46. 1 artist → 2 artist.
6. Uji dulu: greybox isometrik 1 hari + 1 hari top-down, 5 tester, pilih yang lebih terbaca. JANGAN memutuskan dari screenshot.
```

**Keputusan: tetap Top-Down dengan penambahan tinggi (3/4 look).** Isometrik tidak dipakai untuk game ini, dan alasannya dicatat di sini supaya tidak dibuka ulang tanpa data baru.

### 17.12 Kontrak Proyeksi Top-Down 3/4 (DIKUNCI)

Keputusan D22 dikunci di sini sebagai **angka**, bukan sebagai selera. Lembar visualnya: `docs/art/projection-3q-spec.png`.

| Aturan | Nilai | Alasan |
|--------|-------|--------|
| Tile | **16×16 persegi, tanpa rotasi kamera** | Collision AABB, autotile native, pathfinding langsung |
| Muka dinding eksterior | **10 px** (6 px atas + 10 px muka) | Memberi rasa tinggi tanpa proyeksi diagonal |
| Muka dinding rendah / pagar | **6 px** | Bisa dilewati peluru, tetap terbaca punya volume |
| Atap | **alpha 0,25–0,35** saat pemain di dalam footprint | Tidak pernah menutupi pemain (larangan oklusi) |
| Shadow karakter | **ellipse 16×7, offset (0, −1), alpha 45%** — *dikoreksi dari 32×14, lihat catatan* | Karakter tidak terlihat mengambang |
| Y-sort key | **titik kaki (pivot 12,31)** — bukan tengah sprite | Urutan gambar benar saat pemain di belakang meja |
| Perspective scaling | **TIDAK ADA.** Objek di "atas" layar tidak mengecil | Menjaga keterbacaan & ukuran sprite konsisten |
| Arah sprite | 8 arah, 5 baris digambar + 3 mirror (§17.3) | Konsisten dengan gerak 8 arah |

> **Koreksi shadow (v3.12).** Nilai lama 32×14 berasal dari perkiraan, bukan pengukuran. Diuji pada skala asli 320×180: ellipse 32 px = selebar **2× karakter**, dan dengan alpha 45% ia terbaca sebagai genangan air, bukan kontak kaki. Dibandingkan langsung di `docs/art/ingame-scale-check.png`. Lebar karakter 16 px (bahu) → shadow **16×7** (setengah tinggi untuk perspektif), offset **−1 px** karena telapak kaki di (8,23) dan baseline sel 24. Ini satu-satunya perubahan pada §17.12 yang dikunci; kalau tidak disetujui, kembalikan ke 32×14 dan konsekuensinya adalah genangan gelap di bawah setiap karakter.

**Tes penerimaan aset (dipakai saat review seni, bukan selera):**

```text
□ Tanpa shadow, apakah karakter terlihat mengambang?           → harus TIDAK
□ Apakah dinding terbaca punya tinggi dari 4 sisi kamera?      → harus YA (muka terlihat)
□ Apakah ada tile/objek yang menutupi kepala pemain?           → harus TIDAK
□ Apakah sprite di bagian atas layar terlihat lebih kecil?     → harus TIDAK
□ Apakah dua karakter bertumpuk punya urutan benar via kaki?   → harus YA
□ Apakah bentuk tile konsisten persegi (tidak ada belah ketupat)? → harus YA
```

Aset yang gagal di salah satu baris di atas **dikembalikan ke artist**, bukan "diperbaiki nanti di engine". Satu tile isometrik yang lolos ke atlas akan memaksa kompromi di collision dan culling, dan itu biaya yang jauh lebih besar daripada menggambar ulang 1 tile.

**Yang secara sadar TIDAK kita dapat** (supaya tidak ada ekspektasi salah): tidak ada bayangan panjang dari matahari, tidak ada parallax gedung tinggi, tidak ada rotasi kamera, tidak ada objek yang saling menutupi secara diagonal. Kalau salah satu ini ternyata sangat dibutuhkan, itu tanda bahwa proyeksi perlu dibuka kembali lewat §17.11 — dengan greybox 2 hari + 5 tester, bukan dengan menambal satu aset.

### 17.10 Template Aset Siap Pakai

Lembar kerja sudah dibuat dan ikut di repo:

| Berkas | Isi |
|--------|-----|
| `docs/art/player-sheet-guide.png` | Berlabel: 30×4 sel, pivot, nama animasi, FPS |
| `docs/art/player-sheet-1x.png` | Kanvas bersih 480×96 px (untuk Aseprite) |
| `docs/art/zombie-sheet-guide.png` · `zombie-sheet-1x.png` | Base body walker, 16×4 sel, 256×96 px |
| `docs/art/npc-trader-sheet-guide.png` · `npc-trader-sheet-1x.png` | Trader, 8×2 sel, 128×48 px |
| `docs/art/tileset-atlas-map.png` | Peta atlas 32×32 sel + pembagian region |

Aturan pemakaian ada di `docs/art/README.md`. Lembar ini **deterministik**: dibuat ulang dari `tools/make_asset_templates.py` — kalau spesifikasi §17 berubah, ubah script, jangan gambar ulang manual.

---

## 18. Arsitektur Teknis (Godot 4.7.2)

### 18.1 Struktur Proyek

```text
res://
├── scenes/
│   ├── main.tscn
│   ├── world/{world.tscn, chunk.tscn, building_interior.tscn}
│   ├── entities/{player.tscn, corpse_bag.tscn}
│   ├── entities/zombies/{walker,runner,spitter,screamer,tank,exploder,stalker,hive}.tscn
│   ├── shelter/{shelter.tscn, structure_*.tscn, turret.tscn}
│   └── ui/{hud,night_report,inventory,crafting,shelter_panel,map,journal,death}.tscn
├── scripts/
│   ├── autoload/{game_manager,event_bus,save_manager,audio_manager,world_clock,
│   │             night_director,heat_system,world_sim}.gd
│   ├── generation/{map_generator,district_gen,building_gen,bsp_tree,room_data,
│   │               loot_table,biome_data}.gd
│   ├── systems/{crafting,inventory,streaming,shelter_damage,trader}.gd
│   └── entities/{player_controller,zombie_ai,weapon_base,projectile}.gd
├── resources/
│   ├── weapons/ zombies/ recipes/ loot_tables/ districts/ buildings/ events/ skills/
├── assets/{sprites,audio,fonts}
└── project.godot
```

### 18.2 World Clock

```gdscript
# autoload/world_clock.gd
extends Node

signal phase_changed(phase: StringName)        # DAY, DUSK, NIGHT, DAWN
signal hour_changed(day: int, minutes: int)
signal night_started(day: int, is_horde: bool)
signal dawn_started(day: int)

const DAY_LEN := 600.0
const DUSK_LEN := 90.0
const DAWN_LEN := 30.0

var day: int = 1
var phase: StringName = &"DAY"
var time_in_phase: float = 0.0
var pressure: float = 1.0
var speed_mult: float = 1.0
var _sleeping: bool = false

func night_len() -> float:
    return minf(180.0 + 15.0 * (day - 1), 300.0)

func is_horde_night() -> bool:
    return day % 5 == 0

func _process(delta: float) -> void:
    time_in_phase += delta * (10.0 if _sleeping else 1.0)

    match phase:
        &"DAY":
            if time_in_phase >= DAY_LEN: _enter(&"DUSK")
        &"DUSK":
            if time_in_phase >= DUSK_LEN: _enter(&"NIGHT")
        &"NIGHT":
            if time_in_phase >= night_len(): _enter(&"DAWN")
        &"DAWN":
            if time_in_phase >= DAWN_LEN: _next_day()

func _recalc() -> void:
    pressure = minf(1.0 + 0.05 * (day - 1), 2.0)
    speed_mult = minf(1.0 + (pressure - 1.0) * 0.4, 1.25)
```

### 18.3 Streaming Chunk

```gdscript
# systems/streaming.gd
const CHUNK_TILES := 32
const ACTIVE_RADIUS := 1      # 3×3 chunk penuh
const SIM_RADIUS := 6         # simulasi kasar

var _loaded: Dictionary = {}  # Vector2i -> Chunk

func _process(_delta: float) -> void:
    var center := world_to_chunk(GameManager.player.global_position)
    for x in range(-SIM_RADIUS, SIM_RADIUS + 1):
        for y in range(-SIM_RADIUS, SIM_RADIUS + 1):
            var c := center + Vector2i(x, y)
            if not is_in_bounds(c):
                continue
            var dist: int = maxi(absi(x), absi(y))
            _ensure_chunk(c, dist)
    _unload_far(center)

func _ensure_chunk(c: Vector2i, dist: int) -> void:
    if not _loaded.has(c):
        _loaded[c] = ChunkLoader.load_from_diff(c)     # tilemap + diff state
    var lvl: int = 0 if dist <= ACTIVE_RADIUS else (1 if dist <= SIM_RADIUS else 2)
    _loaded[c].set_sim_level(lvl)   # 0 = full 60 tick, 1 = 5 tick, 2 = frozen
```

Aturan teknis:

- `NavigationRegion2D` di-bake **per chunk**, di-thread, sekali waktu load.
- TileMapLayer terpisah: floor / wall / deco / props.
- Chunk yang di-unload menulis diff (pintu, kontainer, populasi, mayat) lalu dibebaskan.
- Budget: 60 FPS di i3-8100 / GTX 1050, 20 zombie aktif + 40 proyektil + 9 chunk penuh.

### 18.4 Heat & Serangan

```gdscript
# autoload/heat_system.gd
signal heat_changed(value: float, tier: StringName)

var heat: float = 0.0

func night_attack(day: int) -> Dictionary:
    var horde := day % 5 == 0
    var roll := randf()
    var chance := 0.0
    if horde:
        chance = 1.0
    elif heat >= 75.0:
        chance = 0.90
    elif heat >= 50.0:
        chance = 0.60
    elif heat >= 25.0:
        chance = 0.25

    if roll > chance:
        return {"attack": false}

    var strength := 0.0
    if horde:
        strength = 16.0 + 1.6 * (day / 5)
    else:
        strength = 2.0 + heat * 0.16 + day * 0.25
    return {"attack": true, "strength": strength, "horde": horde}
```

### 18.5 Event Bus (relevan untuk open world)

```gdscript
# autoload/event_bus.gd
signal player_damaged(amount: int, source: StringName)
signal player_died()
signal zombie_killed(ztype: StringName, pos: Vector2)
signal phase_changed(phase: StringName)
signal night_started(day: int, horde: bool)
signal night_ended(day: int, report: Dictionary)
signal heat_changed(value: float, tier: StringName)
signal shelter_damaged(structure_id: StringName, hp_left: float)
signal shelter_breached()
signal structure_built(structure_id: StringName)
signal chunk_loaded(coords: Vector2i)
signal container_looted(container_id: int)
signal corpse_bag_dropped(pos: Vector2)
signal trader_restocked(day: int)
signal skill_leveled(cabang: StringName, level: int)
signal event_started(event_id: StringName, tier: int)
```

### 18.6 Save

- JSON untuk meta/player/shelter (mudah debug & migrasi versi), biner sparse untuk `world_diff`.
- Diff per chunk hanya berisi field yang berubah, dengan `schema_version` untuk migrasi.
- Simpan `seed` + `day` + `heat` + struktur + storage + corpse bag + populasi chunk yang pernah dikunjungi.

### 18.7 Debug (dev build)

```text
F1  Toggle fog of war          F5  Maju ke malam berikutnya (skip siang)
F2  God mode                   F6  Paksa serangan malam (strength manual)
F3  Spawn 8 zombie             F7  Isi semua stok shelter
F4  Paksa event                F8  Teleport ke shelter
```

---

## 19. Aksesibilitas

| Fitur | Alasan |
|-------|--------|
| Rebind semua tombol | Dasar |
| Full gamepad + aim assist | Twin-stick |
| Screen shake slider 0–100% | Getaran berlebihan |
| Toggle hit-stop | Sebagian pemain terganggu |
| Telegraph visual untuk semua audio | Tunarungu |
| Palet alternatif (deuteranopia) | Loot & tier bergantung warna |
| **Mode "Longer Day"** (siang ×1.3, tanpa memengaruhi skor) | Pemain baru & disabilitas |
| **Mode "Calmer Nights"** (serangan malam ×0.6, tanpa memengaruhi skor) | Aksesibilitas |
| UI scale 2×/3× | 320×180 native |
| Auto-pause saat menu | 320×180 + layar kecil |

---

## 20. Appendix — Angka Balance

```text
PLAYER
  HP 100 · Stamina 100 · Hunger 100 (−1/20s) · Thirst 100 (−1/12s) · Battery 100
  Armor 0–40% · Walk 80 · Sprint 128 · Aim-walk 60
  i-frame saat kena 0.6s · Dodge i-frame 0.25s

BERAT (§8.5)
  Kapasitas 30 kg dasar · tas 40/50 · skill +5×2 · maks 60
  Slot 20 (UI), berat = batas fisik
  ≤50% Ringan ×1.00 · 50–80% Bermuatan ×0.95 · 80–100% Berat ×0.85 · >100% Kelebihan ×0.65
  Kelebihan: tanpa sprint, tanpa dodge, regen ×0.5, suara ×1.35
  Drop bag (G): berat langsung normal, tas bisa diambil 2 hari
  Senjata & armor di hotbar TETAP dihitung (Q8) — contoh 4 senjata + vest + helm ≈ 17 kg
  Kereta dorong: opsional (Q7), muatan 40 kg, tidak bisa sprint

KONSUMSI
  Food +40 hunger · Water +50 thirst · Bandage +20 HP · Medkit +50 HP
  Battery item +30 · Recharge di generator 30/menit

CLOCK
  Siang 600s · Senja 90s · Malam 180s +15/hari (cap 300s) · Subuh 30s
  Hari penuh hari-1 = 900s (15 menit)

KESULITAN
  night_pressure = 1.00 + 0.05 × (hari−1) cap 2.00
  speed_mult = min(1 + (pressure−1)×0.4, 1.25)
  populasi chunk = dasar × min(1 + 0.04×(hari−1), 2.5)
  horde night: hari % 5 == 0

HEAT
  Generator +0.5/menit · Floodlight +0.2/menit · Tembakan +4 · Ledakan +8
  Gelap & sunyi −0.4/menit · Hujan −0.6/menit
  Ambang: 25 / 50 / 75 · Serangan: 25% / 60% / 90% · Horde 100%

SERANGAN
  Probe 2–4 · Breach 5–9 · Siege 11–16 · Horde 16–24 (2–3 gelombang, jeda 20s)

DUEL MATH
  Walker 30 → pistol 3 (1.0s) / wrench 2 (1.25s)
  Runner 18 → pistol 2 · Tank 150 → rifle 4 / pistol 13 · Nest 900

SHELTER
  Tier 1: bed + 2 barricade · Tier 2: generator + workbench 2 + storage 2
  Tier 3: radio + workbench 3 + turret 2 + generator 2
  Door HP 120/240/400 · Turret 12 DMG / 200px
  Pindah shelter: cooldown 3 hari, struktur −50% material
  Storage 1/2/3 halaman = 60/120/180 kg

NIGHT RAID (§7.5)
  Valid: di luar ≥50% malam · Sukses: hidup saat subuh
  Auto-resolve shelter ×0.85 · breach = −25% storage
  Score = menit di luar + 0.2 × kill malam → <6 none, 6–9 Bronze, 10–15 Silver, ≥16 Gold
  Fatigue 1 hari: stamina maks −15% (satu-satunya penalti; Q9)
  Horde night: cache minimum Gold

ASET (§17)
  PROYEKSI: Top-Down 3/4 DIKUNCI (§17.12) — tanpa rotasi kamera, tanpa perspective scaling
  Tile 16×16 · wall face 10 px · roof fade 0,25–0,35 · shadow 32×14 alpha 45%
  Jendela 4 state: utuh (lihat, tidak masuk) · pecah (lihat, masuk 0,45s) ·
    papan (tidak lihat, HP 60) · barikade (tidak lihat, HP 120) · layer vision blocker terpisah
  Karakter 16×24 (pivot 8,23) · collision pemain 10×10
  Arah: 8 (digambar 5 baris, mirror: SE→SW · E→W · NE→NW)
  Player 240 frame di atlas / 150 digambar
  Zombie humanoid 128 di atlas / 80 digambar per tipe → 7 tipe ±595 digambar
  Boss 30 · NPC trader 8
  Tileset/distrik ±285 tile (termasuk wall face 16 + low wall 6) · 5 layer TileMapLayer
  1 artist: 2,5 minggu/distrik → 5 distrik ±26 minggu (jalur kritis)

EKONOMI
  Tanpa mata uang. Storage 1/2/3 halaman · Trader restock 3 hari
  Chunk respawn 7 hari · Corpse bag bertahan 3 hari
```

---

## 21. Roadmap (Early Access di Minggu 28, 1.0 di Minggu 44)

**Kenyataan scope:** open world + shelter + crafting + pertahanan malam adalah **±3×** pekerjaan v3.1. Menjanjikan launch penuh 24–26 minggu adalah kebohongan. Jadi: slice dulu, EA lebih awal, 1.0 belakangan.

### Phase 0 — Fondasi (Minggu 1–2)

```text
☐ Godot 4.7.2, 320×180, nearest, integer scale, pixel snap
☐ Input map keyboard+mouse & gamepad
☐ Tuning file terpusat (semua angka §20 di satu resource)
☐ Event Bus, GameManager, WorldClock skeleton
☐ Debug overlay + hotkey debug
Gate: gerak & serang di 1 chunk statis, 60 FPS, dua input jalan
```

### Phase 1 — Slice (Minggu 3–7) ⭐ gate terpenting

```text
☐ Player: gerak, aim, 2 melee, 1 ranged, dodge
☐ Walker + Runner, AI dengan INVESTIGATE
☐ 1 blok Suburban (6–8 bangunan, interior template)
☐ Loop: siang jelajah → senja → malam bertahan → subuh
☐ Shelter: klaim, 1 pintu, 2 jendela barricade, bed, storage
☐ Serangan malam dasar (Probe → Breach) + heat sederhana
☐ Hunger/thirst/battery + food/water/battery loot
☐ Berat dasar: kg di item, 4 ambang, HUD kg, Drop & Run
☐ HUD, night report, save/load
☐ **Aset:** 1 tileset Suburban (placeholder bersih, ukuran/pivot final) + player idle/walk 8 arah + walker walk 8 arah
  → semua placeholder WAJIB pakai canvas/pivot/nama animasi final (§17.9)
Gate (7 playtester, 2 sesi):
  □ 4/7 bilang "malam terasa menegangkan, tapi adil"
  □ 5/7 menyebut shelter sebagai "rumah", bukan menu
  □ Rata-rata sesi > 40 menit tanpa dipaksa
  □ Tidak ada kematian yang tidak bisa dijelaskan pemain
GAGAL → perbaiki, jangan lanjut.
```

### Phase 2 — Survival Core (Minggu 8–13)

```text
☐ Crafting 16 resep + workbench tier 1–2
☐ Shelter struktur lengkap tier 1–2 (generator, floodlight, spike, water, garden)
☐ Auto-resolve serangan + laporan kerusakan
☐ Heat penuh (semua sumber & decay) + noisemaker
☐ Night raid: valid/sukses, Nightfall Cache (Bronze/Silver/Gold), Fatigue, auto-resolve ×0.85
☐ **Berat/encumbrance**: kg per item, ambang 4 status, Drop & Run, tas + kereta dorong
☐ Death, corpse bag, respawn subuh, 3 mode
☐ Stamina/armor/perbaikan struktur
Gate: pemain bisa bertahan 5 hari tanpa bug; auto-resolve tidak pernah terasa curang
```

### Phase 3 — World (Minggu 14–19)

```text
☐ Chunk streaming + diff state + save sparse
☐ Map generator kota 384×384, 3 distrik (Suburban, Commercial, Industrial)
☐ Interior prosedural 5 archetype × 3 kekacauan
☐ Populasi per chunk, wandering horde, respawn 7 hari
☐ Trader (2 lokasi, restock 3 hari)
☐ Map & journal
☐ **Aset:** tileset Commercial & Industrial final (2,5 minggu/artist/distrik)
Gate: 3 distrik, 40+ bangunan, jalan dari ujung ke ujung tanpa loading, FPS stabil
```

### Phase 4 — Depth (Minggu 20–26)

```text
☐ Spitter, Screamer, Tank, Exploder, Stalker
☐ Skill tree 3 cabang (30 node) + XP curve
☐ Distrik Hospital, Mall (5 distrik total)
☐ Landmark 5 (Hospital wing, Mall atrium, Police, Water treatment, Hive nest)
☐ Night Director 10 event
☐ Turret, radio, shelter tier 3
☐ Audio lengkap
☐ **Aset:** zombie lengkap (7 tipe, base-body + varian), NPC trader 2, tileset Hospital & Mall, item + UI icon
Gate: 20 tester, funnel hari-5 ≥50%, tidak ada save corruption
```

### Phase 5 — EA Launch (Minggu 27–28)

```text
☐ Balance pass dari telemetri
☐ Performance (streaming, pooling, LOD) di mesin minimum
☐ Accessibility pass
☐ Steam page + trailer + demo (hari 1–5)
☐ Localization EN/ID
☐ **Art gate:** 3 distrik bernuansa lengkap + 2 distrik greybox bertekstur (pilihan default §17.8),
  ATAU 2 artist, ATAU EA mundur ke minggu 34. Diputuskan sebelum Phase 5, bukan di tengahnya
🚀 EARLY ACCESS
```

### Phase 6 — Menuju 1.0 (Minggu 29–44)

```text
☐ Distrik ke-6–8: Residential Tower, Police/Fire, Quarantine Wall **(dikonfirmasi v3.3: total 8 distrik untuk 1.0)**
☐ **Aset:** tileset 3 distrik terakhir (±7,5 minggu artist) + The Hive + senjata 10 + NPC rasa (opsional)
☐ The Hive boss + landmark The Bridge Out
☐ Radio tower & 3 ending + endless
☐ 24 resep, 12 blueprint, 10 senjata
☐ Modifier / difficulty mutator
☐ Workshop support (opsional)
☐ 1.0 🚀
```

### Cut List (diputuskan sekarang)

| Fitur | Keputusan |
|-------|-----------|
| Multiplayer / co-op | ❌ |
| Peta lebih dari 1 kota | ❌ |
| Kendaraan | ❌ (alasan: biaya AI + streaming tidak sepadan) |
| NPC survivor / companion AI | ❌ (trader saja) |
| Base building bebas (modular grid) | ❌ — struktur terpasang di slot bangunan |
| 200 resep | ❌ 24 |
| 8 distrik saat EA | ❌ 5 saat EA |
| Skill tree 60 node | ❌ 30 |
| Mobile / console day-one | ⏸ pasca-1.0 |
| Mod support | ⏸ pasca-1.0 |
| Kereta dorong | ⏸ **opsional** — dipotong kalau Phase 2 mepet (Q7/D16) |

---

## 21B. Prototipe Greybox (kode di repo)

Greybox 1 ruangan sudah ada di `game/` untuk menguji kontrak desain **sebelum** satu pixel seni final. Bukan demo, bukan vertical slice — alat verifikasi.

| Diuji di greybox | Status | Bukti lulus/gagal |
|------------------|--------|-------------------|
| 8 arah sprite (5 digambar + 3 mirror) | sudah | Arah hadap mengikuti gerak; mirror tidak terlihat aneh |
| Pivot (8,23) + collision 10×10 di kaki | sudah | Pemain tidak mentok di lorong 1 tile |
| **Berat → kecepatan** (4 ambang) + Drop & Run | sudah | Saat Kelebihan, Runner (96 px/s) menangkap pemain (52 px/s) |
| Lampu → baterai → heat → serangan | sudah | Mematikan lampu menurunkan heat & frekuensi serangan |
| Siklus siang–malam memanjang | sudah | Malam hari 5 terasa jelas lebih panjang |
| Wall face 10 px + roof fade | sudah | Bangunan terbaca punya tinggi; pemain tidak tertutup atap |
| Walker chase + attack + LOS | sudah | Tidak ada serangan menembus dinding |
| **Belum**: menembak, navmesh, inventory, crafting, hunger/thirst | — | Phase 1–2 (§21) |

**Aturan pemakaian:** angka di `game/scripts/autoload/tuning.gd` mengikuti §20. Yang dipendekkan hanya durasi fase (siang 120 s, malam 30 s) agar bisa dites dalam 2 menit. **Jangan menaikkan angka produksi karena greybox terasa enak** — kalau ada yang perlu diubah, ubah §20 dulu beserta alasannya.

**Batas jujur:** kode greybox ditulis tanpa bisa menjalankan engine di lingkungan ini. Verifikasi otomatis tersedia lewat `tools/lint_gdscript.py` (kurung, indentasi, path aset, nama signal & konstanta, fungsi ganda, `in (A,B)`, dan `:=` dari ekspresi Variant). Putaran tes pertama di Godot 4.7.2 menemukan 4 error parser — semuanya dari asumsi sintaks Python — dan sudah diperbaiki; rinciannya di `game/README.md` bagian *Perbaikan setelah tes pertama*.

**Pelajaran untuk sisa proyek:** dua pola yang harus dihindari di GDScript — `x in (A, B)` (tidak ada) dan `:=` pada ekspresi yang menyentuh variabel untyped. Keduanya sudah dicegat lint, jadi biayanya sekarang nol.

---

## 22. Metrik & Playtest

### 22.1 Telemetri (CSV lokal, opt-in)

```text
Per hari:  hari, fase terpakai (siang/malam), jarak ditempuh, bangunan dijelajah,
           kontainer dibuka, zombie dibunuh, damage diterima, HP akhir
Per malam: heat awal, serangan (ya/tidak), strength, struktur rusak, breach (ya/tidak),
           tidur (ya/tidak), night raid (ya/tidak), waktu bertahan
Per shelter: tier, hari tier tercapai, jumlah struktur, kerusakan kumulatif
Per ekspedisi: berat awal/akhir (kg), status terakhir, drop bag dipakai (ya/tidak),
           item dibuang, jumlah pulang-pergi
Per malam: night raid valid (ya/tidak), score, cache tier, shelter breach saat raid (ya/tidak)
Per run:   hari bertahan, penyebab mati, jarak dari shelter saat mati, corpse bag diambil,
           shelter hancur (ya/tidak), pindah shelter (jumlah), mode
```

### 22.2 Yang Diukur

| Metrik | Target | Kalau gagal, ubah apa |
|--------|--------|-----------------------|
| Hari bertahan (median) | 8–14 hari ke ending | Kalau <6: kurangi pressure; kalau >20: naikkan heat/agresi |
| Pemain tidur tiap malam | <40% | Malam terlalu keras atau auto-resolve terlalu kejam |
| Shelter breached per 5 hari | 0,8–1,5 | >2 = terlalu keras; 0 = tidak ada taruhan |
| Waktu di shelter vs ekspedisi | 25% / 75% | >40% di shelter = pemain takut keluar |
| Storage penuh (hari) | hari 4–6 | Kalau hari 2: tier 2 terlalu cepat |
| Corpse bag diambil kembali | >70% | <50%: penalti terlalu berat |
| Hapus save karena frustrasi | <10% tester | Investigasi langsung |
| **Status Berat/Kelebihan saat pulang ekspedisi** | 20–35% waktu | Kalau ~0%: berat tidak pernah jadi keputusan. Kalau >50%: kapasitas terlalu kecil |
| **Drop & Run dipakai** | >20% pemain pernah | Kalau 0%: tidak pernah ada momen "buang tas" → naikkan ancaman kejar |
| **Waktu mengatur berat/inventory** | <20% waktu main | Kalau lebih: naikkan kapasitas dasar (§8.5 aturan 5) |
| **Night raid dilakukan** | >25% pemain pernah | Kalau 0%: cache terlalu murah / risiko terlalu berat |
| **Night raid berhasil vs gagal** | 55–75% berhasil | <40%: terlalu keras; >85%: tidak ada taruhan |
| FPS minimum (mesin minimum) | ≥55 | Potong radius simulasi, bukan fitur |

### 22.3 Protokol

- 7 tester di Phase 1 (2 sesi × 45 menit), 20 tester di Phase 4.
- 4 pertanyaan wajib: (1) Kapan kamu merasa rumahmu terancam? (2) Kapan kamu hampir mati, dan kenapa itu salahmu? (3) Apa yang kamu lakukan saat matahari mulai turun? (4) Apakah kamu ingin lanjut besok?
- Tester baru tiap fase. Jangan pakai orang yang sama terus — bias.

---

## 23. Ide yang Dipensiunkan

| Ide | Dari | Alasan pensiun |
|-----|------|----------------|
| Struktur 5 floor roguelite | v3.0/v3.1 | Bertabrakan dengan open world + shelter (pivot v3.2) |
| Signal & meta tree antar-run | v3.0/v3.1 | Tidak relevan: progresi sekarang di dalam save (§12) |
| Wave terjadwal | v2 | Event terpicu keadaan lebih bermakna (§7.2) |
| Timer siang 70 detik | v2 | Terlalu pendek untuk satu objektif |
| Scrap carry 50% saat mati | v2 | Menciptakan strategi "timbun lalu mati" |
| Meter Hunger tanpa konteks | v3.1 | Dihapus karena run 30 menit; **kembali** di v3.2 karena save 10–30 jam (§0.3) |
| ~~Sprite 8 arah~~ | v2 | **DIBATALKAN di v3.6** — 8 arah dipakai kembali, dengan 5 baris + mirror supaya biayanya +25%, bukan +100% (§17.3) |
| Deteksi zombie 250px | v2 | Di luar layar = tidak adil |
| Barricade sebagai pilar (tower defense) | v1 | Shelter sudah jadi pilar; barricade jadi bagiannya, bukan game sendiri |
| Judul "Dead Pixel" | v1/v2 | Bertabrakan dengan *Dead Pixels* (CSR-Studios, 2012) |
| Kendaraan, NPC companion, base modular bebas | v3.2 cut | Di luar kapasitas 44 minggu |

---

## 24. Keputusan

### 24.1 Sudah diputuskan

| # | Pertanyaan | Keputusan | Konsekuensi |
|---|-----------|-----------|-------------|
| D1 | Struktur game | **Open world 1 kota + shelter** | v3.0/v3.1 (roguelite) pensiun |
| D2 | Kematian default | **Corpse bag + respawn subuh**, Ironman opsional | Save tidak hilang; corpse bag wajib diambil lagi (§13.2) |
| D3 | Hunger | **Kembali** (Hunger + Thirst + Battery) | Alasan di §0.4; tetap dijaga agar bukan pekerjaan rumah |
| D4 | Panjang siang | **600s**, malam 180–300s | Validasi di §5.1 |
| D5 | Shelter | **1 shelter aktif, bisa pindah** | Memilih shelter = keputusan strategis (§6.1) |
| D6 | Serangan malam | **Heat (0–100) + horde tiap 5 hari** | Kegiatan siang punya harga (§7) |
| D7 | Skor | **Hari bertahan** | Tanpa mata uang meta |
| D8 | Scope | **EA di minggu 28, 1.0 minggu 44** | 5 distrik saat EA (§21) |
| D9 | Malam = loot atau bertahan | **Dua-duanya**: bertahan di shelter, atau night raid berisiko | §3.3 aturan 4 |
| D10 | Shelter boleh pindah? | **Boleh, cooldown 3 hari** (Q1) | Komitmen, bukan refleks (§6.1). Bebas cooldown kalau shelter hancur |
| D11 | Auto-resolve saat pemain pergi? | **Boleh, 0,85× pertahanan** + sistem hadiah night raid (Q2) | §7.5. Tanpa hadiah, night raid hanya penalti |
| D12 | The Hive wajib untuk ending? | **Opsional** (Q3) | Mengalahkannya menurunkan heat global −25 (§14.1) |
| D13 | Jumlah distrik di 1.0 | **8 distrik, dipertahankan** (Q5) | Phase 6 menambah Residential Tower, Police/Fire, Quarantine Wall |
| D14 | Semua item punya berat? | **Ya**, berat memengaruhi kecepatan, sprint, dodge, noise | §8.5; mekanik Drop & Run wajib ada bersamaan |
| D15 | Berat dasar | **30 kg**, maks 60 kg lewat tas + skill | Kalau playtest mengatur berat >20% waktu, naikkan — jangan hapus |
| D16 | Kereta dorong | **Opsional** (Q7) | Boleh dipotong tanpa merusak sistem berat (§8.5 aturan 7) |
| D17 | Berat senjata & armor | **Dihitung semua, termasuk slot hotbar** (Q8) | 4 senjata + vest + helm = 17 kg sebelum loot (§8.5 aturan 6) |
| D18 | Penalti Fatigue | **−15% stamina maks saja, 1 hari** (Q9) | Tidak ada penalti hunger/thirst; shelter damage sudah jadi penalti utama |
| D19 | Spesifikasi aset | **Tileset 16×16 per distrik (±263 tile), karakter 16×24, 8 arah (5 digambar + 3 mirror)** | §17. Tambahan ±3 minggu seni untuk 8 arah (§17.8) |
| D20 | NPC | **Trader saja (2 lokasi, statis)**. NPC rasa ditunda ke pasca-1.0 | Tanpa companion AI. NPC bergerak = +4–6 minggu (§17.5) |
| D21 | Sumber seni | **1 artist kontrak 5–6 bulan** (Q10) | Karakter wajib custom; tileset komersial boleh untuk ground/wall (§17.9) |
| D22 | Proyeksi kamera | **DIKUNCI: Top-Down 3/4** — tile 16×16, wall face 10 px, roof fade, shadow; tanpa perspective scaling | Kontrak angka + tes penerimaan di §17.12. Isometrik ditolak: area pandang separuh, okclusion, +20–35 minggu (§17.11) |

### 24.2 Masih terbuka (jawab sebelum Phase 1 selesai)

| # | Pertanyaan | Default sementara | Kenapa penting |
|---|-----------|-------------------|----------------|
| Q4 | Skill tree respec: gratis 1× atau berbayar? | Berbayar (1 rare item) | Menentukan seberapa berani pemain bereksperimen |
| Q6 | Apakah perlu kesulitan "story mode" (serangan 0,6×)? | Ada sebagai aksesibilitas, tanpa skor | Ramah pemain baru |

---

_versi 3.2 — 26 Oktober 2026_

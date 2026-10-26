# The End Has Come

## Game Design Document v3.0 — Canonical

### Top-Down · Roguelite · Singleplayer · Procedural · Godot 4.4

> **Dokumen ini menggantikan v1 dan v2.** Kalau ada pertentangan antara dokumen ini dan ingatan kita soal versi lama, dokumen ini yang menang.
> Ide dari v1/v2 yang sengaja **tidak** dipakai dicatat di §19 supaya tidak muncul lagi sebagai "katanya dulu ada".

---

## 0. Changelog v3.0 & Keputusan yang Berubah

| # | Isu | v1 | v2 | **v3 (berlaku sekarang)** |
|---|-----|----|----|---------------------------|
| 1 | Struktur | Survival open-world + shelter | Roguelike run-based | **Roguelite run-based, 5 floor** (§3) |
| 2 | Jumlah malam | 15–25 malam per run | 3–5 malam × 5–7 floor | **1 siklus malam per floor = 5 malam per run** |
| 3 | Durasi run | 10–30 menit | target 20–40 menit | **DIHAPUS sebagai target** (§3.1) |
| 4 | Siang | timer 10–15 menit/hari | 70 detik | **150–240 detik, dan siang tidak pernah membunuh pemain** (§4) |
| 5 | Malam | timer 50 detik + wave | wave 1-3 terjadwal | **150–210 detik + Night Director (event, bukan wave)** (§4, §5) |
| 6 | Angka zombie | 10–120 per malam (linear) | `5 + night×3` | **budget 24–56 total, cap 10–18 bersamaan** (§5.4) |
| 7 | Ekonomi meta | Scrap carry 50% saat mati | Scrap = meta + in-run | **Salvage (hangus) vs Signal (milestone)** (§11) |
| 8 | Judul | Dead Pixel: Survive the Night | idem | **The End Has Come** |
| 9 | Skill tree | 3 cabang in-run | dihapus | **Dihapus** — diganti meta tree + loot (§11) |
| 10 | Roadmap | 24 minggu, playtest minggu 21 | 26 minggu | **24 minggu, slice-first, playtest minggu 5** (§18) |

**Alasan perubahan besar** (ringkas): v1 dan v2 sebenarnya dua game berbeda yang ditempel. v2 lebih layak dikerjakan untuk solo dev, jadi v2 yang jadi tulang, dan v1 disumbangkan bagian yang masih relevan (crafting, art, audio, UI, komposisi zombie). Yang dibuang adalah semua janji yang saling bertabrakan: target durasi, wave terjadwal + barricade, dan ekonomi scrap yang bisa di-farm dengan sengaja mati.

---

## 1. Overview

| Item | Detail |
|------|--------|
| **Judul** | The End Has Come |
| **Genre** | Top-Down Roguelite Zombie Survival |
| **Perspektif** | Top-down, mouse/gamepad aim, free rotation |
| **Struktur** | Run-based, permadeath, 5 floor, 1 siklus siang–malam per floor |
| **Multiplayer** | Singleplayer only |
| **Map** | Procedural (BSP hybrid) tiap floor, seed bisa di-share |
| **Engine** | Godot 4.4 (GDScript, Forward+) — **versi di-pin, jangan campur API 4.2/4.3** |
| **Art** | Pixel art, tile 16×16, resolusi native 320×180 |
| **Target platform** | PC (Steam), keyboard+mouse **dan** gamepad |
| **Durasi run** | **Tidak dijanjikan.** Lihat §3.1 — panjang run adalah konsekuensi struktur, bukan target desain |
| **Referensi rasa** | Nuclear Throne (feel tembakan), Darkest Dungeon (tekanan ekspedisi), Brotato (skala angka), Project Zomboid (tema) |
| **Yang dijual** | "3 menit malam yang bikin kamu menyesal karena serakah" |

---

## 2. Core Concept

### 2.1 Elevator Pitch

> Malam turun di kota yang sudah mati. Kamu punya satu siklus siang untuk mempersiapkan diri, dan satu malam untuk bertahan di gedung yang sama. Lift ke bawah baru hidup saat fajar — jadi satu-satunya cara keluar adalah **selamat sampai pagi**. Lima gedung. Lima malam. Satu fajar.

### 2.2 Design Pillars

| # | Pilar | Konsekuensi desain (wajib dicek tiap fitur) |
|---|-------|---------------------------------------------|
| 1 | **Malam adalah bahaya, siang adalah anggaran** | Timer siang tidak pernah membunuh. Yang membunuh hanya malam. |
| 2 | **Keserakahan harus selalu masuk akal** | Loot terbaik ada di luar tempat aman saat malam. Pemain selalu bisa memilih "cukup". |
| 3 | **Bahaya harus bisa dibaca** | Setiap ancaman punya telegraph audio **dan** visual. Tidak ada kematian dari off-screen tanpa tanda. |
| 4 | **Kegagalan harus terasa seperti keputusan sendiri** | Kematian datang dari loot ke-3 yang tidak perlu, bukan dari angka yang tidak terlihat. |
| 5 | **Satu malam = satu cerita** | Setiap malam punya event acak/terpicu yang bisa diceritakan ulang. |

### 2.3 Anti-Pilar (yang game ini **bukan**)

- **Bukan** tower defense. Barricade itu alat, bukan tujuan. Kamu tidak "menang" dengan menumpuk dinding.
- **Bukan** horde shooter 100 zombie di layar. Layar cuma 20×11 tile; 18 zombie sudah terasa seperti banjir.
- **Bukan** open world. Tidak ada world map, tidak ada NPC trader permanen, tidak ada base building antar-run.
- **Bukan** game panjang. Satu run harus selesai dalam satu duduk.

---

## 3. Struktur Run

### 3.1 Kenapa Target Durasi Run Dihapus

Angka "20–40 menit" di v2 **tidak mungkin** dengan timer v2 sendiri: 3–5 malam × 5–7 floor dengan 1 hari = 120 detik berarti 30–70 menit murni jam game, sebelum inventory dan crafting. Angka itu bukan salah tuning, tapi salah aritmetika.

**Keputusan:** durasi run tidak lagi menjadi target desain. Yang diukur dan di-tuning adalah **panjang tiap fase** (§4), karena itulah yang dirasakan pemain tiap 30 detik. Panjang run dibiarkan menjadi konsekuensi struktur: 5 floor × 1 siklus.

| Yang dihapus | Diganti dengan |
|--------------|----------------|
| "Target Run Length 20–40 menit" | Table fase per floor (§4.2) + telemetri median waktu per fase |
| "3–5 malam per floor" | 1 siklus per floor |
| "Win rate 10–20%" sebagai target awal | Diukur dulu di playtest, target ditetapkan setelah 3 sesi |

> **Catatan aritmetika (bukan janji):** 5 floor × ±7 menit clock = ±35 menit. Kalau nanti terbukti terlalu panjang saat playtest, yang dipotong adalah **siang floor 1–2**, jangan pernah memotong malam — memotong malam berarti memotong inti game.

### 3.2 Run Flow

```
MULAI RUN  (pilih survivor + 1 starting perk)
        │
        ▼
┌──────────────────────────────────────────────────────┐
│  FLOOR n dari 5   (biome berbeda per floor)          │
│                                                      │
│   ☀️  SIANG   anggaran waktu: jelajah, loot, craft,  │
│              pilih tempat bertahan, barricade        │
│        │                                             │
│        ▼   senja 30s (peringatan, lampu mulai perlu) │
│   🌙  MALAM   bahaya naik 3 tingkat + event acak /   │
│              terpicu. Lift terkunci.                 │
│        │                                             │
│        ▼   subuh 15s (zombie mundur)                 │
│   🛗  LIFT HIDUP → turun ke floor n+1                │
└──────────────────────────────────────────────────────┘
        │
        ▼ (setelah floor 5 malamnya = boss)
   💀 MATI → Run Summary → Signal payout → Hub
   🏆 BOSS MATI + naik ke permukaan → Ending → Hub
```

**Aturan kunci yang wajib dipegang sistem:**

1. **Lift hanya hidup saat subuh.** Pemain tidak bisa kabur dari malam. Ini yang membuat 5 malam selalu terjadi dan selalu berarti.
2. **Malam tidak "dimenangkan" dengan membunuh semua zombie.** Malam selesai karena **timer mencapai subuh** (atau pemain tidur, §4.5). Ini spec resmi kondisi selesai malam — di v2 hal ini tidak pernah didefinisikan.
3. **Tidak ada malam tambahan, tidak ada floor tambahan.** Run berakhir hanya karena mati atau mengalahkan boss floor 5.
4. **Seed di-generate per run**, ditampilkan di HUD pause, dan bisa di-share untuk challenge.

### 3.3 Floor / Biome (5, bukan 7)

| Floor | Biome | Zona rasa | Zombie baru | Loot fokus |
|-------|-------|-----------|-------------|------------|
| 1 | **Suburban** | Rumah, jalan, pagar. Ruang terbuka, banyak jalan keluar | Walker | Food, cloth |
| 2 | **Industrial** | Gudang besar, lorong servis, chokepoint | Runner | Scrap, fuel |
| 3 | **Hospital** | Lorong sempit, banyak pintu, ruang tertutup | Spitter | Medical, chemical |
| 4 | **Mall** | Atrium luas, banyak loot, banyak zombie, sedikit pengaman | Tank, Screamer | Mixed, rare |
| 5 | **The Bunker** | Gelap, sempit, listrik mati, boss | Exploder + **The Hive** | Blueprint, ending |

> Forest, Lab, dan Bunker-2 dari v1 dipensiunkan jadi **modifier** run (ascension), bukan biome baru. Alasan: 7 biome = 7 tileset = 3 bulan seni untuk variasi yang jarang dilihat.

### 3.4 Kondisi Menang & Kalah

| Kondisi | Hasil |
|---------|-------|
| HP 0 | Mati permanen → Run Summary → Signal sesuai floor tertinggi |
| Mengalahkan The Hive lalu naik lift darurat | Menang → Ending (1 dari 3, sesuai survivor) → unlock modifier |
| Menutup game / quit saat run | Dianggap mati, Signal tetap dihitung (anti save-scum) |

---

## 4. Siklus Siang–Malam (Timer & Bahaya)

### 4.1 Prinsip Timer

- **Siang = anggaran.** Timer siang memberi tahu kapan lampu mati, bukan kapan kamu mati. Tidak ada kerusakan, tidak ada penalti di detik 0.
- **Malam = tekanan.** Timer malam memberi tahu kapan kamu selamat. Ini satu-satunya timer yang benar-benar menentukan hidup-mati.
- **Pemain harus bisa "membelanjakan" waktu.** Aksi tertentu memakan waktu lebih dari sekadar animasi: membuka kontainer berat, membangun barricade, reload besar.
- **Tidur = jalan pintas.** Pemain yang sudah siap bisa mempercepat siang (§4.5). Ini yang membuat timer tidak terasa seperti menunggu.

### 4.2 Fase & Nilai Nyata

| Fase | Fungsi | Nilai | Alasan angka ini |
|------|--------|-------|------------------|
| **Siang** | Jelajah, loot, craft, siapkan pertahanan | 150s → 240s (naik per floor) | Pemain bergerak 80 px/s; satu "objektif" (jalan + loot 2 ruangan) ±40–50s. Anggaran ini memberi 3–4 objektif. |
| **Senja** | Peringatan, pindah posisi, pasang lampu | 30s | Cukup untuk satu perjalanan pendek antar ruangan, tidak cukup untuk ekspedisi baru |
| **Malam** | Inti game: bertahan + event | 150s → 210s | 3 sub-fase (§4.4). Di bawah 120s event tidak punya ruang bernapas; di atas 240s terasa mengulur |
| **Subuh** | Zombie mundur, jendela aman, lift hidup | 15s | Ritme "lega" yang pendek, cukup untuk panik-heal |

**Tabel per floor (detik):**

| Floor | Siang | Senja | Malam | Subuh | Clock floor |
|-------|-------|-------|-------|-------|-------------|
| 1 | 150 | 30 | 150 | 15 | 5:45 |
| 2 | 180 | 30 | 165 | 15 | 6:30 |
| 3 | 200 | 30 | 180 | 15 | 7:05 |
| 4 | 220 | 30 | 195 | 15 | 7:40 |
| 5 | 240 | 30 | 210 | 15 | 8:15 |

**Anggaran siang vs isi map** (validasi bahwa timer masuk akal, contoh floor 3, 200s):

```
Jalan antar ruangan (rata-rata)     40s
Loot 3 kontainer                    45s
Craft 1–2 resep di bench            30s
Barricade 2 pintu                   30s
Reposisi ke shelter / lift          25s
Sisa buffer untuk kejadian tak terduga 30s
```

Timer siang yang **terlalu pendek** adalah kegagalan desain yang paling mahal: pemain berhenti mengambil risiko dan game jadi menunggu. Kalau ragu, tambah 15s, jangan kurangi.

### 4.3 Kontrol Waktu oleh Pemain

| Aksi | Efek waktu | Biaya |
|------|-----------|-------|
| Reload senjata besar (rifle) | +1.2s real time | — (sudah jadi bagian combat) |
| Buka kontainer terkunci | +1.5s | butuh pry bar / 1 salvage |
| Bangun barricade | +6s | 2 wood + 1 scrap |
| **Bunk Down** (tidur) | Siang dipotong → malam mulai dalam 5s | 1 torch, harus di shelter room, tidak ada zombie dalam 8 tile |
| Ganti hari manual | — | **tidak ada** (tidak ada fast-forward) |

`Bunk Down` memberi +30 HP dan +50 stamina, tapi kamu kehilangan sisa siang **dan** memicu 1 event saat malam dimulai (bukan 0). Jadi tidur itu aman-dan-tidak-gratis.

### 4.4 Malam: 3 Sub-fase & Eskalasi Bahaya

Malam dibagi 33% / 42% / 25%:

| Sub-fase | Nama | Floor 1 | Floor 5 | Phase mult | Suasana |
|----------|------|---------|---------|------------|---------|
| N1 | **The Fall** | 0:50 | 1:10 | ×1.00 | Gelap, ambient spawn mulai, pemain orientasi |
| N2 | **Deep Night** | 1:03 | 1:28 | ×1.20 | Event bisa dipicu; loot malam muncul |
| N3 | **Dead Hours** | 0:37 | 0:52 | ×1.45 | Puncak; event lethal hanya boleh di sini |

**Night Pressure** (satu angka yang dipakai semua sistem):

```
pressure = floor_mult × phase_mult × noise_mult

floor_mult = 1.0 + 0.12 × (floor - 1)     # F1 1.00 → F5 1.48
phase_mult = 1.00 / 1.20 / 1.45           # N1 / N2 / N3
noise_mult = 1.00 diam
           = 1.10 sprint >3s
           = 1.25 tembakan dalam 30s terakhir

speed_mult  = min(1.0 + (pressure - 1.0) × 0.4, 1.25)   # runner tidak boleh > sprint pemain
detect_mult = min(pressure, 1.8)                        # dan tetap dibatasi 150px (batas layar)
spawn_interval = base_interval / min(pressure, 1.8)
```

Arti konkretnya saat malam:

1. **Penglihatan menyusut.** Tanpa lampu, radius lihat 40px. Lampu sulung 80px. Flashlight 140px tapi **terlihat zombie** (noise_mult +0.10 untuk pemain di radius 120px).
2. **Indera zombie naik.** Detect naik sampai 150px dan hearing radius naik 40% di N3.
3. **Ambient spawn mengalir terus** (§5.4), bukan menunggu wave.
4. **Event dipicu Night Director** (§5), 2–3 per malam.
5. **Loot malam aktif.** Kontainer gelap (§9.4) hanya bisa dibuka saat malam, dan isinya 1 tier lebih tinggi.

HUD menampilkan status ini secara eksplisit: ikon bulan + label **Calm / Stirring / Hunted / Overrun** (dari pressure), supaya eskalasi terbaca, bukan cuma terasa.

### 4.5 Kondisi Selesai Malam (spec resmi)

Malam berakhir **hanya** jika salah satu terpenuhi:

```text
1. Timer malam mencapai 0  → subuh, semua zombie disengage & mundur, lift hidup
2. Bunk Down berhasil      → malam diakhiri lebih awal, loot malam hangus, tidak ada bonus
```

Bukan kondisi selesai: membunuh semua zombie (tidak akan pernah tercapai, karena ambient spawn terus), keluar map, atau menyentuh lift (lift mati sampai subuh).

---

## 5. Night Director — Event, Bukan Wave

### 5.1 Kenapa Wave Terjadwal Dibuang

v2 punya wave 1-3 dengan jadwal tetap. Masalahnya: wave terjadwal membuat **layout map dan barricade tidak berarti** (zombie datang dari luar layar tanpa peduli ruangan), dan membuat malam terasa seperti minigame terpisah dari game-nya. Diganti dengan **event yang dipicu keadaan pemain + undian berbobot**.

Hasilnya: bermain berisik → didatangi. Bersembunyi diam → didatangi hal lain. Serakah → didatangi lebih banyak. Pemain selalu punya kausalitas yang bisa dibaca.

### 5.2 Struktur Director

```text
Saat malam mulai:
  deck = pool event untuk floor ini
  sisa undian = 2 (floor 1-2) atau 3 (floor 3-5)
  cooldown = 12s, tidak ada event sebelum malam berjalan 20s

Tiap frame:
  jika ada event aktif → tunggu
  jika cooldown > 0 → kurangi
  jika sisa undian = 0 → tidak ada event lagi (kecuali pity/quiet)
  jika kondisi pemicu terpenuhi  → paksa event itu (bobot ×3)
  jika waktu masuk jendela undian → undi dari deck berbobot

Aturan keadilan (tidak bisa dinegosiasikan):
  □ maksimal 1 event Tier 3 per malam
  □ event Tier ≥2 tidak muncul di 20s pertama malam
  □ cooldown minimal 25s antar event
  □ pity: HP < 35% → hanya Tier 0/1 sampai subuh
  □ setiap telegraph audio WAJIB punya padanan visual
  □ spawn ≥200px dari pemain, tidak pernah di kerucut pandang 60° depan pemain
  □ event tidak menembus barricade penuh, kecuali event Breach
  □ kalau cap zombie penuh, burst event dikurangi, TIDAK ditunda (ritme > jumlah)
```

### 5.3 Daftar Event

| ID | Nama | Tier | Bobot | Pemicu | Telegraph | Counterplay |
|----|------|------|-------|--------|-----------|-------------|
| `echo_migration` | **Echo Migration** | 3 | 2 | 3+ tembakan dalam 45s, **atau** 1 undian di N2/N3. Bobot ×2 kalau salvage dibawa >200 | Lolongan berlapis + panah tepi layar 3s | Barricade + chokepoint, atau senyap 20s |
| `hunter_pack` | **Hunter Pack** | 2 | 3 | Sprint kumulatif >10s, atau 2 tembakan | Langkah cepat yang makin dekat (panning L/R) | Dodge roll, senjata cepat, jangan lari lurus |
| `screamer_rally` | **Screamer Rally** | 3 | 2 | Spawn screamer diam-diam di dark zone | Jeritan pertama + ikon di HUD | Bunuh sebelum jeritan ke-3 |
| `breach` | **Breach** | 2 | 3 | Pemain di ruangan berbarricade ≥30s | Kayu retak 2s + debu | Perbaiki, atau keluar sebelum jebol |
| `grid_collapse` | **Grid Collapse** | 1 | 4 | Undian di N2 | Lampu berkedip, suara trafo | Pakai torch/flare, radius −40% selama 45s |
| `acid_rain` | **Acid Rain** | 2 | 2 | Undian di N2/N3 (bukan di Bunker dalam) | Tetesan + langit hijau + suara hujan | Masuk indoor; loot outdoor jadi berisiko |
| `care_package` | **Care Package** | 1 | 3 | Undian, **atau** pemain menyalakan flare | Suara beacon | Rebut cepat: beacon memanggil zombie tiap 10s, 3 gelombang |
| `the_quiet` | **The Quiet** | 0 | 3 | Pity (HP<35%) atau 90s tanpa event | Musik meredup, ambient hilang | 20s loot gratis — sengaja diberi |
| `collapse` | **Structural Collapse** | 1 | 3 | 60s di area yang sama | Gemuruh + debu | Jalur baru terbuka (bisa jadi keuntungan) |
| `stragglers` | **Stragglers** | 1 | 4 | Otomatis kalau zombie hidup < 50% cap | — (drip biasa) | +4 zombie ambient, 40s |
| `trader` | **The Trader** | 0 | 2 | Siang/senja saja, tidak pernah saat malam | Lampu hangat + suara radio | Tukar salvage ↔ gear; bisa diabaikan |
| `hive_stirs` | **The Hive Stirs** | 4 | — | Floor 5, N2 (scripted) | Getaran layar + dinding berdenyut | Boss fight, 3 fase (§8.5) |

Catatan: `the_quiet` bukan bug — ia ada di deck supaya ritme malam punya lembah. Malam tanpa jeda terasa melelahkan, bukan menegangkan.

### 5.4 Angka Zombie yang Masuk Akal

**Batasan fisik:** viewport 320×180 = **20×11 tile**. Area main yang terlihat ±18×9 tile.

| Aturan | Nilai | Alasan |
|--------|-------|--------|
| **Cap bersamaan** | `8 + 2 × floor` → F1 **10**, F5 **18**; hard cap **20** | 20 zombie = ±1 per 5 tile² — sudah terasa seperti kerumunan penuh |
| **Cap saat event burst** | cap + 6, maks **24**, maksimal 20s | Burst harus terasa, tapi tidak menutupi layar |
| **Budget total per malam** | `16 + 8 × floor` → F1 **24**, F5 **56** | Membatasi durasi "pekerjaan" malam supaya tidak jadi grinding |
| **Jarak spawn** | ≥200px dari pemain, di luar pandangan bila memungkinkan | Di layar 320px, spawn 200px = masih di luar layar |
| **Jeda spawn ambient** | N1 9s / N2 6s / N3 4s, dibagi `min(pressure, 1.8)` | Mengalir, tidak menumpuk |
| **Burst event** | 6–10 zombie, jarak antar spawn 0.6–1.2s | Cukup untuk panik, tidak untuk mustahil |
| **Jarak deteksi maksimum** | **150px** (semua tipe, setelah multiplier) | Di atas 160px zombie mendeteksi dari luar layar = tidak adil |

Aritmetika floor 1 (malam 150s, budget 24): N1 50s → 5 spawn, N2 63s → 10, N3 37s → 9 = 24. Cocok. **Kalau angka budget dan interval tidak cocok, yang diubah interval-nya** — budget adalah anggaran desain, interval cuma cara membaginya.

Total zombie dibunuh per run penuh: **±180–220**. Cukup untuk merasa kuat, tidak cukup untuk bosan.

---

## 6. Player Systems

### 6.1 Stats

| Stat | Nilai awal | Aturan |
|------|-----------|--------|
| **HP** | 100 | Tidak regen. Sembuh lewat item, Bunk Down (+30), atau subuh (+10) |
| **Stamina** | 100 | Sprint −18/s, regen 22/s setelah jeda 0.8s. Dodge −25 |
| **Hunger** | 100 | −1 per 15s; di 0 → −1 HP/2s. Makanan +25/+50 |
| **Armor** | 0 | 2 slot (vest/helm), reduksi 15–40%, rusak saat kena |
| **i-frame saat kena** | 0.6s | Wajib. Tanpa ini, kerumunan = kematian instan tanpa counterplay |
| **Move / Sprint** | 80 / 128 px/s | Sprint hanya bisa sambil tidak menembak |

### 6.2 Kontrol

```text
KEYBOARD + MOUSE                     GAMEPAD (wajib, setara)
WASD            gerak 8 arah         Left stick     gerak
Mouse           arah bidik           Right stick    arah bidik
Left click      serang               RT             serang
Right click     aim / alt            LT             aim (perlambat, akurasi naik)
R               reload               X              reload
E               interact             A              interact
Q               lempar item          LB             lempar
1–4             hotbar               D-pad          hotbar
Shift           sprint               Left stick click sprint
Space           dodge roll           B              dodge
Tab             inventory            Start          pause
C               crafting             Select         map
M               map
F1–F4           debug (dev build only)
```

Aturan: **tidak boleh ada aksi inti yang hanya ada di satu perangkat.** Twin-stick tanpa gamepad = kehilangan separuh pasar Steam.

### 6.3 Inventory & Hotbar

- Grid 6×3 = 18 slot, hotbar 4 slot.
- Item menumpuk maks 5 (ammo 20). Tidak ada rotasi barang.
- Berat tidak dibatasi — tapi salvage yang dibawa memengaruhi bobot event (§5.3).
- Mengambil item saat malam butuh 0.4s (bukan instan) supaya tidak bisa "grab sambil lari" tanpa risiko.

### 6.4 Dodge Roll

| Parameter | Nilai |
|-----------|-------|
| Stamina | 25 |
| Durasi | 0.30s |
| Jarak | 3 tile (48px) |
| I-frame | 0.25s |
| Cooldown | 0.8s |
| Arah | 8 arah, mengikuti input gerak |

Dodge adalah satu-satunya jawaban untuk Runner dan burst event. Kalau dodge tidak terasa enak di minggu 3 prototipe, **hentikan semua fitur lain** sampai enak — ini fitur yang menentukan game terasa responsif atau tidak.

---

## 7. Combat

### 7.1 Prinsip

- Bullet punya travel time (bukan hitscan) → bisa di-dodge, bisa meleset karena jarak.
- Spread naik saat bergerak; aim (klik kanan/LT) memperlambat pemain tapi menaikkan akurasi.
- Melee punya arc 90°, hitbox aktif 0.18s, dan **selalu** memberi knockback.
- Setiap musuh punya telegraph sebelum menyerang (minimal 0.35s).

### 7.2 Senjata (6 inti + 2 craftable)

| Senjata | Tipe | DMG | Serangan/dtk | Jangkauan | Ammo | Catatan |
|---------|------|-----|--------------|-----------|------|---------|
| Pipe Wrench | Melee | 22 | 1.6 | 26px | ∞ | Knockback 80. Stamina 8 |
| Machete | Melee | 15 | 2.6 | 24px | ∞ | Bleed 2/s selama 4s |
| Fire Axe | Melee | 40 | 0.85 | 30px | ∞ | Bisa merusak pintu/barricade. Stamina 20 |
| Pipe Pistol | Ranged | 12 | 3.0 | 220px | 8 mag | Ammo paling umum |
| Sawed-off | Ranged | 6×6 pellet | 1.1 | 90px | 2 | Mematikan di <60px |
| Bolt Rifle | Ranged | 45 | 0.8 | 300px | 5 | Pierce 1, reload 2.2s |
| Nailgun *(craft)* | Ranged | 7 | 8.0 | 150px | 30 | Spread 8°, murah |
| Molotov *(craft)* | Throw | 8/s api | — | radius 48px | 1 | 4s, area denial |

**TTK target** (dasar balancing, jangan diubah tanpa mengukur ulang):
Walker 30 HP → pistol 3 tembakan (1.0s) / wrench 2 pukulan (1.25s).
Runner 18 HP → pistol 2 tembakan.
Tank 150 HP → rifle 4 tembakan / pistol 13 (memang harus jadi mini-boss).
Boss 900 HP → ±25s DPS murni, jadi 60–90s fight dengan fase.

### 7.3 Combat Feel (checklist yang tidak boleh dilewat)

```
□ Screen shake 2–4px saat hit (bisa dimatikan di opsi aksesibilitas)
□ Hit-stop 2–3 frame saat critical / kill
□ Blood pixel splatter + decal yang tidak hilang sampai subuh
□ Muzzle flash + light 1 frame
□ Knockback konsisten (jangan cuma di senjata berat)
□ Audio: 3 lapis (impact, tail, ambient ducking)
□ Angka damage OPSIONAL (default: mati) — jangan sampai game terasa RPG
```

---

## 8. Zombie

### 8.1 Tabel Statistik

| Zombie | HP | Speed px/s | DMG | Atk range | Detect | Muncul | Peran |
|--------|----|-----------|-----|-----------|--------|--------|-------|
| **Walker** | 30 | 36 | 8 | 22px | 120px | F1 | Massa, mudah di-kite, mengajarkan ritme |
| **Runner** | 18 | 96 | 6 | 20px | 140px | F2 | Memaksa dodge; tidak boleh lebih cepat dari sprint (128) |
| **Spitter** | 26 | 44 | 10 + poison 3/s (3s) | 90–150px | 130px | F3 | Area denial, jaga jarak |
| **Tank** | 150 | 30 | 22 | 26px | 110px | F4 | Penghancur barricade, harus di-kite |
| **Screamer** | 40 | 40 | 5 | 20px | 150px | F4 | Pemanggil; prioritas tertinggi |
| **Exploder** | 22 | 64 | 55 (radius 56px) | self | 130px | F5 | Berkedip merah 2s sebelum meledak |
| **The Hive** (boss) | 900 | 34 | 18 / 25 | — | — | F5 | 3 fase, spawn add |

Spitter detect 130px (bukan 250px seperti di v2) karena 250px > setengah lebar layar: pemain akan kena proyektil dari luar pandangan tanpa bisa membalas.

### 8.2 State Machine

```text
                 ┌───────────┐
      noise ────►│ INVESTIGATE│──► tidak ada apa-apa ──► WANDER
                 └─────┬─────┘
                       │ lihat pemain (LOS + jarak)
                       ▼
   IDLE ◄── 8s ──┌───────────┐
                 │   CHASE    │◄───┐
                 └─────┬─────┘    │ keluar attack range
                       │ masuk attack range
                       ▼
                 ┌───────────┐
                 │  ATTACK    │───► HP ≤ 0 ──► DEAD
                 └───────────┘
```

Beda dari v2: ada **INVESTIGATE** (zombie mendatangi sumber suara). Tanpa state ini, semua sistem noise (§4.4) tidak ada artinya.

### 8.3 Implementasi Godot (versi valid, bukan pseudocode v2)

```gdscript
# entities/zombie_ai.gd
# Potongan inti. _wander(), _investigate(), dan transisi INVESTIGATE ada di repo.
extends CharacterBody2D

enum State { IDLE, WANDER, INVESTIGATE, CHASE, ATTACK, DEAD }

@export var data: ZombieData

@onready var agent: NavigationAgent2D = $NavigationAgent2D
@onready var body_sprite: AnimatedSprite2D = $AnimatedSprite2D

var state: State = State.IDLE
var target: Node2D = null
var _sight_timer: float = 0.0
var _repath_timer: float = 0.0
var _attack_timer: float = 0.0
var _last_target_pos: Vector2 = Vector2.INF

const SIGHT_INTERVAL: float = 0.2    # 5x/detik, bukan 60x
const REPATH_INTERVAL: float = 0.25
const REPATH_MIN_DIST: float = 32.0

func _physics_process(delta: float) -> void:
    if state == State.DEAD or data == null:
        return

    _sight_timer -= delta
    _repath_timer -= delta
    _attack_timer = maxf(_attack_timer - delta, 0.0)

    match state:
        State.IDLE, State.WANDER:
            _wander(delta)
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
    var player: Node2D = GameManager.player
    if player == null or not is_instance_valid(player):
        return   # zombie spawn sebelum player siap: jangan crash
    if GameManager.player_is_dead:
        return

    var detect: float = minf(data.detection_range * NightDirector.detect_multiplier, 150.0)
    if global_position.distance_to(player.global_position) > detect:
        return
    if not _has_line_of_sight(player):
        return

    target = player
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

    # Repath hanya kalau target benar-benar berpindah jauh.
    if _repath_timer <= 0.0:
        _repath_timer = REPATH_INTERVAL
        if target.global_position.distance_squared_to(_last_target_pos) > REPATH_MIN_DIST * REPATH_MIN_DIST:
            _last_target_pos = target.global_position
            agent.target_position = _last_target_pos

    var next: Vector2 = agent.get_next_path_position()
    var dir: Vector2 = (next - global_position).normalized()
    velocity = dir * data.speed * NightDirector.speed_multiplier
    move_and_slide()
    body_sprite.flip_h = dir.x < 0.0

func _attack() -> void:
    if target == null:
        state = State.IDLE
        return
    if _attack_timer <= 0.0:
        _attack_timer = data.attack_cooldown
        body_sprite.play(&"attack")
        EventBus.player_damaged.emit(int(data.damage), data.zombie_name)
    if global_position.distance_to(target.global_position) > data.attack_range:
        state = State.CHASE

func _has_line_of_sight(player: Node2D) -> bool:
    var query := PhysicsRayQueryParameters2D.create(
        global_position, player.global_position, 1)   # layer 1 = dinding
    return get_world_2d().direct_space_state.intersect_ray(query).is_empty()
```

### 8.4 Catatan Performa AI

- Deteksi pakai **distance check dulu**, baru raycast. Jangan raycast 40 zombie tiap frame.
- `NavigationAgent2D.target_position` maksimal 4×/detik per zombie.
- Zombie di luar layar: matikan `_physics_process` lewat `VisibleOnScreenNotifier2D` + timer 2s (buffer supaya tidak flicker).
- Semua angka di `ZombieData` (.tres), **jangan** hardcode di script.

### 8.5 Boss: The Hive

| Fase | HP | Perilaku |
|------|----|----------|
| 1 | 900 → 600 | Merayap lambat, memanggil 4 walker tiap 12s. Mengajarkan "add dulu, boss kemudian" |
| 2 | 600 → 300 | Membuka dinding, memaksa pemain berpindah ruangan; spitter di lorong |
| 3 | 300 → 0 | Charge + scream; lampu mati total. 90s terakhir adalah puncak game |

Boss hanya di Floor 5, satu boss, tiga fase. Tidak ada "random boss per run" — variasi datang dari modifier.

---

## 9. Crafting, Loot & Survival

### 9.1 Resource

| Resource | Sumber | Kegunaan |
|----------|--------|----------|
| 🪵 Wood | Furnitur, pohon, barricade lama | Barricade, torch, senjata dasar |
| 🔩 Scrap | Mobil, mesin, zombie industrial | Senjata, ammo, trap, perbaikan |
| 🧪 Chemical | Apotek, lab, spitter | Medkit, molotov, ammo khusus |
| 🔌 Electronics | Toko, panel listrik | Flashlight, turret, upgrade lampu |
| 🧵 Cloth | Rumah, zombie | Bandage, armor ringan |

### 9.2 Recipe Inti (12 untuk launch, bukan 20)

```text
Wood ×4 + Scrap ×1                 → Bandage ringan (heal 20)
Chemical ×3 + Cloth ×2             → Medkit (heal 50)
Scrap ×5                           → Pistol ammo ×12
Scrap ×4 + Wood ×2                 → Nailgun ammo ×30
Wood ×3 + Scrap ×2                 → Torch (radius 80, 90s)
Scrap ×6 + Electronics ×2          → Flashlight (radius 140, cone)
Wood ×6 + Scrap ×2                 → Barricade (1 tile, 120 HP)
Wood ×2 + Scrap ×1                 → Repair kit (+60 HP barricade)
Chemical ×2 + Cloth ×1 + Scrap ×1  → Molotov
Scrap ×8 + Electronics ×3          → Spike trap (DMG 30, sekali pakai)
Scrap ×10 + Electronics ×4         → Nailgun
Scrap ×15 + Electronics ×5 + Chemical ×3 → Turret kecil (30s, ammo terbatas)
```

Resep di v1 (20 resep, turret otomatis penuh) dipotong: turret penuh mengubah game jadi tower defense, yang bertentangan dengan §2.3.

### 9.3 Barricade (aksesori, bukan pilar)

- 1 tile, 120 HP, butuh 6s untuk dipasang, maks 6 barricade aktif.
- Zombie menyerang barricade 8 DMG/detik; Tank 30/detik.
- Barricade **tidak** memblokir event (§5.2), hanya memperlambat.
- Barricade yang hancur memberi +1 wood (dorongan untuk repot memperbaiki).

### 9.4 Loot

| Tier | Kapan | Isi |
|------|-------|-----|
| Common | Siang, kontainer biasa | Wood, cloth, food, ammo sedikit |
| Uncommon | Siang, kontainer terkunci | Scrap, chemical, bandage |
| **Night-only** | Hanya saat malam, kontainer gelap | Electronics, blueprint, medkit, senjata |
| Event | `care_package`, `trader` | 1 rare item + risiko |

Kontainer gelap diberi tanda visual jelas saat siang ("terkunci sampai gelap"). Ini janji ke pemain: **keserakahan selalu ditawarkan lebih dulu, bukan dijebak.**

---

## 10. Map Generation

### 10.1 Pipeline

```text
Step 1  BSP split          → 4–5 split rekursif
Step 2  Room placement     → 8–12 ruangan (6–10 tile)
Step 3  Corridor connect   → L-shape + 1 loop tambahan (WAJIB: tanpa loop, map jadi pohon dan pemain terpojok)
Step 4  Populate           → spawn, lift, loot, bench, dark zone, shelter room
Step 5  Validate           → semua ruangan reachable; lift ≤ 3 ruangan dari spawn;
                            minimal 7 kontainer; minimal 1 shelter room
Step 6  Bake navigation    → sekali, saat floor selesai digenerate
```

**Kenapa wajib ada loop:** map pohon (tree) membuat pemain yang dikejar tidak punya jalan memutar. Di game dengan Runner, ini berarti kematian tanpa counterplay.

### 10.2 Tile

```text
Floor      walkable
Wall       blocking, sebagian bisa dihancurkan (axe/tank)
Door       buka/tutup, bisa dibarricade
Window     terlihat, bisa dipecah zombie
Tree       blocking, ditebang (wood)
Car        blocking, meledak jika ditembak (DMG 40, radius 64)
Water      slow 50%, tidak bisa barricade
Fire       DoT, menyebar 1 tile/2s
Stairs     lift (mati sampai subuh)
Crate      lootable
Barrel     meledak (DMG 50, radius 48)
Dark zone  spawn point + loot tier naik
Shelter    boleh Bunk Down
```

### 10.3 Struktur Kode

```gdscript
func generate_floor(floor_number: int, run_seed: int, retry: int = 0) -> FloorData:
    var rng := RandomNumberGenerator.new()
    rng.seed = hash(str(run_seed) + ":" + str(floor_number) + ":" + str(retry))  # deterministik

    var bsp := BSPTree.new(Vector2i(72, 48), rng)   # map 72×48 tile
    bsp.split(6, 4)                                # positional: GDScript tidak punya named argumen
    var rooms: Array[RoomData] = bsp.create_rooms(4, 10)

    var corridors: Array[Vector2i] = connect_rooms(rooms, rng, 1)  # 1 loop tambahan
    var data := FloorData.new(rooms, corridors, floor_number)

    place_spawn_and_lift(data, rng)
    place_loot(data, rng)
    place_hazards(data, rng)

    if not validate(data):
        if retry >= 3:
            push_error("Floor %d gagal generate 3x, pakai template fallback" % floor_number)
            return FloorData.fallback(floor_number, run_seed)
        return generate_floor(floor_number, run_seed, retry + 1)

    navigation_region.bake_navigation_polygon(true)
    return data
```

---

## 11. Kematian, Skor & Ekonomi Meta (ditulis ulang)

### 11.1 Masalah Ekonomi v2

v2: scrap yang dibawa = 50% saat mati, dan scrap juga dipakai upgrade permanen.
→ Strategi optimal: **jangan crafting, timbun scrap, mati.** Itu kebalikan dari pilar survival. Diperbaiki total.

### 11.2 Dua Mata Uang, Dua Fungsi

| Mata uang | Didapat | Dipakai | Saat mati |
|-----------|---------|---------|-----------|
| **Salvage** (in-run) | Zombie, loot, dekorasi | Crafting, barricade, ammo, trader | **Hangus 100%** |
| **Signal** (meta) | Milestone run (tabel di bawah) | Meta upgrade | **Tetap** |

Aturan yang membuat ini tidak bisa dieksploitasi:

1. Signal dibayar **berdasarkan pencapaian floor tertinggi**, bukan per-item yang dibawa. Mati di floor 1 = dapat sedikit, bukan dapat "tabungan".
2. Tidak ada konversi Salvage → Signal. Nol.
3. Blueprint **bukan** mata uang: dibuka lewat kondisi sekali-seumur-hidup (kill 50 walker, kalahkan boss, dll).

### 11.3 Tabel Signal

| Pencapaian | Signal | Catatan |
|------------|--------|---------|
| Mencapai Floor 2 | 20 | Dasar |
| Mencapai Floor 3 | 50 | Kumulatif (bukan 20+50) |
| Mencapai Floor 4 | 95 | |
| Mencapai Floor 5 | 155 | |
| Kalahkan The Hive | 255 | Sama dengan full clear |
| Bestiary entry baru (per tipe) | +10 | Sekali per tipe, seumur akun |
| Modifier aktif | ×1.0 – ×2.0 | Pengganda di akhir |

Rata-rata run yang mati di floor 3: **50 Signal**. Kalahkan boss: **255**.

### 11.4 Meta Upgrade

| Upgrade | Tier | Cost | Efek |
|---------|------|------|------|
| Starting Flashlight | 1 | 60 | Mulai dengan flashlight (bukan cuma torch) |
| +1 Inventory slot (×2) | 1/2 | 50 / 90 | +4 slot |
| Barricade Kit | 1 | 70 | Mulai dengan 2 plank |
| Stamina Training | 2 | 150 | +15 stamina maks |
| Map Intel | 2 | 120 | 1 ruangan acak terlihat di map tiap floor |
| Craft Discount | 2 | 140 | −10% resource |
| Field Medic | 2 | 180 | +1 bandage, heal +20% |
| Scavenger's Eye | 3 | 220 | 1 kontainer rare ditandai per floor |
| Second Wind | 3 | 300 | Bangkit 1× per run di 30% HP |
| Survivor: The Runner | 3 | 250 | +sprint, −HP |
| Survivor: The Medic | 3 | 250 | +heal, −damage |

**Aturan meta:** total kekuatan mentah dari meta maksimal **+15%** (HP, damage, speed). Sisanya harus berupa **opsi dan tempo** (slot, discount, informasi, revive). Kalau meta membuat floor 1–2 jadi trivial, meta-nya salah.

Total untuk membuka semua: **±1.870 Signal** ≈ 10–15 run. Target panjang meta: 8–12 jam, bukan 40 jam.

### 11.5 Kematian & Ringkasan Run

```text
💀 RUN SUMMARY
  Floor dicapai         3 / 5
  Malam selamat         2
  Zombie dibunuh        147
  Event dialami         Echo Migration, Breach, The Quiet
  Penyebab mati         Exploder (dekat barricade)
  Signal                +50
  Unlock baru?          Blueprint: Nailgun

  [ Lihat replay seed ]  [ Kembali ke Hub ]
```

Menampilkan **penyebab mati** secara eksplisit adalah bagian dari pilar 4: kematian harus terbaca sebagai keputusan, bukan sebagai keberuntungan buruk.

---

## 12. UI / UX

### 12.1 HUD

```text
┌────────────────────────────────────────────────┐
│ ♥100  ⚡85  🍖72     FLOOR 3  ☀ 2:14  🌙 Calm │
│                                                │
│                 [ GAME WORLD ]                 │
│                                                │
│  ┌──┬──┬──┬──┐                 ┌──────────┐    │
│  │🪓│🔫│🩹│🔥│  hotbar         │ minimap  │    │
│  └──┴──┴──┴──┘                 │ ▓▓·☠·▓▓  │    │
│                                └──────────┘    │
│  [ EVENT: ECHO MIGRATION ← ]                   │
└────────────────────────────────────────────────┘
```

Elemen wajib di HUD: HP, stamina, hunger, **floor**, **fase + timer**, **danger tier**, hotbar, minimap (hanya area terjelajah), banner event (dengan panah arah).

### 12.2 Layar

`Main Menu` · `Hub (meta)` · `Run Setup (survivor, modifier, seed)` · `Game` · `Pause` · `Run Summary` · `Bestiary` · `Settings` · `Tutorial`.

### 12.3 Aturan UX

- Semua angka kritis terlihat **tanpa** membuka menu.
- Semua kemampuan yang butuh waktu (barricade, reload) punya progress bar di dunia, bukan di HUD.
- Tidak ada tooltip yang menutupi 1/3 layar — resolusi native 320×180, UI harus di-scale terpisah dari dunia (CanvasLayer + skala 2×/3×).
- Setiap telegraph audio punya padanan visual (icon + arah). Pemain tunarungu harus bisa main penuh.

---

## 13. Audio

| Kategori | Arah |
|----------|------|
| BGM Siang | Ambient, drone, "sunyi yang tidak nyaman" |
| BGM Senja | Detak / denyut naik, instrument minim |
| BGM Malam N1 | Bass rendah, langkah, jauh |
| BGM Malam N2–N3 | Perkusi, distorsi, tempo naik per pressure tier |
| BGM Boss | Heavy percussion + choir |
| SFX Zombie | 3 lapis: geraman dekat, jeritan jauh, langkah (memberi info arah) |
| SFX Combat | Impact, tail, shell drop, dan **ducking** saat kill besar |
| SFX Event | Signature unik per event (Echo Migration, Breach, Care Package) |
| SFX UI | Klik, craft, notifikasi |

Aturan: **audio adalah sistem gameplay**, bukan hiasan. Pemain harus bisa mengenali event dari suara sebelum melihatnya, dan sebaliknya dari visual sebelum mendengarnya.

---

## 14. Art Direction

| Item | Nilai |
|------|-------|
| Resolusi native | 320×180, di-scale integer ke 1280×720 / 1920×1080 |
| Tile | 16×16 |
| Palet | 32 warna (1 ramp per material) |
| Mood | Gelap, kotor, terbaca. Abu-abu, coklat, hijau gelap; aksen merah/kuning/putih |
| Filter | Nearest, viewport stretch, pixel snap ON |

**Sprite yang wajib ada (player):** idle, walk (4 arah), attack melee, attack ranged, hurt, death, dodge, interact.
**Keputusan:** **4 arah + rotasi senjata**, bukan 8 arah. Untuk twin-stick, 8 arah sprite menggandakan biaya animasi dengan hasil visual yang hampir tidak terasa; rotasi node senjata memberi presisi bidik.

**Prioritas aset (jangan dibalik):** tile + player + walker → zombie lain → UI → efek → dekorasi. Placeholder kotak berwarna dipakai sampai minggu 14; seni final baru masuk setelah slice terbukti seru.

---

## 15. Arsitektur Teknis (Godot 4.4)

### 15.1 Struktur Proyek

```text
res://
├── scenes/
│   ├── main.tscn
│   ├── world/game_world.tscn
│   ├── entities/player.tscn
│   ├── entities/zombies/{walker,runner,spitter,tank,screamer,exploder,hive}.tscn
│   ├── systems/{night_director.tscn,spawn_director.tscn}
│   └── ui/{hud,run_summary,hub,crafting,inventory}.tscn
├── scripts/
│   ├── autoload/{game_manager,event_bus,save_manager,audio_manager,night_director}.gd
│   ├── generation/{map_generator,bsp_tree,room_data,loot_table,biome_data}.gd
│   ├── systems/{crafting,inventory,day_night,fog_of_war,spawn_director}.gd
│   └── entities/{player_controller,zombie_ai,weapon_base,projectile}.gd
├── resources/
│   ├── weapons/ zombies/ recipes/ loot_tables/ biomes/ events/
├── assets/{sprites,audio,fonts}
└── project.godot
```

### 15.2 Event Bus

```gdscript
# autoload/event_bus.gd
extends Node

# Player
signal player_damaged(amount: int, source: String)
signal player_healed(amount: int)
signal player_died()
signal stamina_changed(current: float, maximum: float)

# Combat
signal zombie_killed(zombie_type: StringName, position: Vector2)
signal zombie_spawned(zombie_type: StringName)
signal player_attacked(weapon_id: StringName)

# Cycle (BARU — ini yang menggantikan wave_*)
signal phase_changed(phase: StringName)              # DAY, DUSK, NIGHT, DAWN
signal night_subphase_changed(subphase: StringName)  # FALL, DEEP, DEAD_HOURS
signal danger_tier_changed(tier: int, pressure: float)
signal night_ended(reason: StringName)               # DAWN, BUNK_DOWN

# Night Director (BARU)
signal event_started(event_id: StringName, tier: int)
signal event_ended(event_id: StringName)
signal event_telegraph(event_id: StringName, direction: Vector2)

# Systems
signal item_picked_up(item_id: StringName, amount: int)
signal item_crafted(recipe_id: StringName)
signal floor_generated(floor_number: int, run_seed: int)
signal floor_cleared(floor_number: int)
signal run_ended(signal_earned: int, floor_reached: int)

# UI
signal show_notification(text: String, kind: StringName)
signal show_crafting_ui()
```

Catatan: `wave_started` / `wave_cleared` **dihapus**. Semua yang dulu mendengarkan wave sekarang mendengarkan `event_*` dan `danger_tier_changed`.

### 15.3 Data-Driven Resource (GDScript valid)

```gdscript
# resources/weapon_data.gd
class_name WeaponData
extends Resource

enum WeaponType { MELEE, RANGED, THROWABLE }

@export var weapon_name: String = ""
@export var weapon_type: WeaponType = WeaponType.MELEE
@export var damage: float = 10.0
@export var attacks_per_second: float = 2.0
@export var attack_range: float = 26.0      # JANGAN pakai nama "range"
@export var magazine_size: int = 0          # 0 = melee
@export var reload_time: float = 0.0
@export var spread_degrees: float = 0.0
@export var knockback: float = 40.0
@export var stamina_cost: float = 0.0
@export var ammo_type: StringName = &""
@export var sprite: Texture2D
@export var sfx_attack: AudioStream
```

```gdscript
# resources/zombie_data.gd
class_name ZombieData
extends Resource

@export var zombie_name: StringName = &"walker"
@export var max_hp: float = 30.0
@export var speed: float = 36.0
@export var damage: float = 8.0
@export var attack_range: float = 22.0
@export var attack_cooldown: float = 1.0
@export var detection_range: float = 120.0
@export var xp_reward: int = 1
@export var loot_table: LootTable
@export var spritesheet: Texture2D
@export var special_ability: StringName = &"none"  # spit, charge, scream, explode
```

> v2 menulis `@export var weapon_type: enum { ... }` dan `@export var range: float` — keduanya **error** di GDScript. Versi di atas yang dipakai.

### 15.4 Night Director (kerangka)

```gdscript
# autoload/night_director.gd
extends Node

var pressure: float = 1.0
var speed_multiplier: float = 1.0
var detect_multiplier: float = 1.0

var _pool: Array[StringName] = []
var _draws_left: int = 0
var _lethal_drawn: int = 0
var _cooldown: float = 0.0
var _active: StringName = &""

func begin_night(floor_number: int, rng: RandomNumberGenerator) -> void:
    _pool = EventDB.pool_for_floor(floor_number).duplicate()
    _pool.shuffle()
    _draws_left = 2 if floor_number <= 2 else 3
    _lethal_drawn = 0
    _cooldown = 12.0
    _active = &""
    _recalc(floor_number, 1.0, 0.0)
    EventBus.night_subphase_changed.emit(&"FALL")

func _recalc(floor_number: int, phase_mult: float, noise_mult: float) -> void:
    pressure = minf((1.0 + 0.12 * (floor_number - 1)) * phase_mult * noise_mult, 2.0)
    speed_multiplier = minf(1.0 + (pressure - 1.0) * 0.4, 1.25)
    detect_multiplier = minf(pressure, 1.8)
    EventBus.danger_tier_changed.emit(_tier_for(pressure), pressure)

func _tier_for(p: float) -> int:
    if p < 1.1: return 0      # Calm
    if p < 1.35: return 1     # Stirring
    if p < 1.7: return 2      # Hunted
    return 3                  # Overrun

func night_budget(floor_number: int) -> int:
    return 16 + 8 * floor_number          # F1 24 ... F5 56

func concurrent_cap(floor_number: int) -> int:
    return mini(8 + 2 * floor_number, 20) # F1 10 ... F5 18
```

### 15.5 Spawn Director

```gdscript
func spawn_interval(subphase: StringName) -> float:
    var base: float = {&"FALL": 9.0, &"DEEP": 6.0, &"DEAD_HOURS": 4.0}[subphase]
    return base / minf(NightDirector.pressure, 1.8)
```

### 15.6 Save File

```text
user://save_meta.json
  version, signal, upgrades{}, survivors_unlocked[], bestiary{}, blueprints[],
  first_clear_flags[], modifiers_unlocked[]
Aturan: ditulis hanya di akhir run. Tidak ada save saat run berjalan (roguelite, bukan checkpoint).
```

### 15.7 Performa & Debug

```text
PERFORMA
├── Object pool: zombie, projectile, blood decal (jangan queue_free + instantiate)
├── Nav bake: HANYA sekali per floor, on_thread = true
├── Culling: VisibleOnScreenNotifier2D + timer 2s untuk zombie
├── TileMapLayer terpisah: floor / wall / deco
├── Batas GPUParticles2D aktif: 12
└── Budget: 60 FPS di i3-8100 / GTX 1050, 30 zombie + 40 proyektil

DEBUG (dev build)
├── F1  Toggle fog of war
├── F2  God mode
├── F3  Maju ke sub-fase malam berikutnya
├── F4  Paksa event (pilih dari deck)
├── F5  Spawn 8 zombie
├── F6  Isi inventory test kit
└── F7  Teleport ke lift
```

---

## 16. Aksesibilitas

| Fitur | Alasan |
|-------|--------|
| Rebind semua tombol | Dasar |
| Full gamepad + aim assist ringan | Twin-stick |
| Screen shake slider (0–100%) | Getaran berlebihan bikin mual |
| Toggle hit-stop | Sebagian pemain terganggu |
| Telegraph visual untuk semua audio | Tunagrahita/tunarungu |
| Palet alternatif (deuteranopia) untuk loot tier | Loot bergantung warna |
| Mode "Slow Night" (timer malam ×1.25) | Aksesibilitas, tidak memengaruhi Signal |
| Ukuran UI scale (2× / 3×) | 320×180 native |

---

## 17. Appendix — Angka Balance (satu tempat)

```text
PLAYER
  HP 100 · Stamina 100 · Hunger 100 (−1/15s) · Armor 0–40%
  Walk 80 · Sprint 128 · Aim-walk 60
  i-frame setelah kena 0.6s · Dodge i-frame 0.25s

DUEL MATH
  Walker 30HP → pistol 3 tembakan (1.0s) | wrench 2 pukulan (1.25s)
  Runner 18HP → pistol 2 tembakan
  Tank 150HP → rifle 4 tembakan | pistol 13
  Boss 900HP → ±25s DPS murni → 60–90s fight

NIGHT (per floor)
  Budget      24 / 32 / 40 / 48 / 56
  Cap         10 / 12 / 14 / 16 / 18   (hard 20, burst 24)
  Interval    9s / 6s / 4s per sub-fase (dibagi min(pressure,1.8))
  Detect max  150px (semua tipe)

PRESSURE
  floor_mult 1.00–1.48 · phase 1.00/1.20/1.45 · noise 1.00/1.10/1.25
  speed_mult  ≤1.25 · detect_mult ≤1.8

ECONOMY
  Salvage: hangus saat mati
  Signal: 20 / 50 / 95 / 155 / 255 (kumulatif per floor tertinggi)
  Meta total ±1.870 Signal ≈ 10–15 run
```

---

## 18. Roadmap (24 Minggu, Slice-First)

**Aturan roadmap:** tidak ada fase yang boleh mulai sebelum gate fase sebelumnya lulus. Kalau gate gagal, potong scope, jangan geser tanggal.

### Phase 0 — Fondasi (Minggu 1)

```text
☐ Godot 4.4 project, 320×180, nearest filter, pixel snap
☐ Input map: keyboard+mouse DAN gamepad
☐ Debug overlay (FPS, state, pressure) + tuning file (semua angka di satu .tres)
☐ Event Bus + GameManager skeleton
Gate: bisa gerak di 1 ruangan statis, 60 FPS, dua perangkat input jalan
```

### Phase 1 — Vertical Slice (Minggu 2–5)

```text
☐ Player: gerak, aim, 1 melee, 1 ranged, dodge roll (harus enak)
☐ Walker + Runner (AI, state, attack, mati)
☐ HP, stamina, damage, i-frame, knockback, hit-stop, screen shake
☐ 1 map BSP sederhana (6 ruangan) + navigation + fog of war
☐ Timer siang/malam + Night Pressure + HUD danger tier
☐ 2 event: echo_migration, the_quiet
☐ Loot 6 kontainer + pickup
Gate (Minggu 5, 5 playtester eksternal):
  □ 3 dari 5 bilang "dodge-nya enak"
  □ Bisa menghabiskan 1 malam dan mau main lagi
  □ Tidak ada kematian yang tidak bisa dijelaskan pemain
  □ Median malam terasa 2–4 menit, bukan terlalu pendek/panjang
JIKA GAGAL: jangan lanjut ke Phase 2. Perbaiki feel.
```

### Phase 2 — Struktur Run (Minggu 6–9)

```text
☐ 5 floor, biome Suburban + Industrial
☐ Lift (hidup saat subuh) + transisi floor
☐ Run state machine: setup → floor → night → dawn → next → death → summary
☐ Death screen + penyebab mati + seed
☐ Save meta (Signal, upgrade kosong dulu) + anti save-scum
☐ Loot tier + night-only container
Gate: bisa main 1 run penuh (mati di floor 1 sampai menang) tanpa crash
```

### Phase 3 — Lapisan Survival (Minggu 10–14)

```text
☐ Inventory grid + hotbar + drag/drop
☐ Crafting 12 resep + bench
☐ Barricade + repair + torch/flashlight (lampu memengaruhi deteksi)
☐ 2 trap (spike, molotov area)
☐ Spitter, Tank, Screamer + special ability masing-masing
☐ 8 event (semua kecuali trader & hive_stirs)
☐ Bunk Down + shelter room
Gate: pemain yang bagus bisa bertahan malam tanpa menembak sekali pun (stealth/lampu/barricade)
```

### Phase 4 — Konten & Polish (Minggu 15–18)

```text
☐ Biome Hospital, Mall, Bunker
☐ Exploder + The Hive (3 fase)
☐ 8 senjata (6 inti + 2 craft)
☐ 3 survivor (Scavenger default, Runner, Medic)
☐ Meta tree lengkap (11 upgrade)
☐ Audio lengkap (BGM per fase + SFX event)
☐ Seni final (bukan placeholder)
☐ Onboarding: 3 menit tutorial tanpa teks dinding
Gate: 10 playtester, tidak ada yang butuh dijelaskan cara main
```

### Phase 5 — Balance & Demo (Minggu 19–21)

```text
☐ Telemetri: median waktu per fase, penyebab mati, floor funnel, penggunaan event
☐ Balance angka (§17) berdasarkan data, bukan feeling
☐ Demo publik (floor 1–2) + Next Fest
☐ Steam page + wishlist + trailer 45s
☐ Accessibility pass
Gate: funnel floor 1→2 minimal 70% tester, death cause tidak didominasi satu hal
```

### Phase 6 — Launch (Minggu 22–24)

```text
☐ Bug fix, performance, controller QA
☐ Localization EN/ID (teks UI terpisah dari kode)
☐ Build Steam (Windows + Linux), depot, achievements (12, bukan 30)
☐ Launch 🚀
```

### Cut List (diputuskan sekarang, bukan nanti)

| Fitur | Keputusan |
|-------|-----------|
| Multiplayer / co-op | ❌ Tidak ada |
| 7 biome | ❌ 5 |
| 20 resep | ❌ 12 |
| 5 survivor | ❌ 3 |
| Open world + NPC trader permanen | ❌ (trader jadi event) |
| Skill tree in-run | ❌ (meta tree) |
| 30 achievement | ❌ 12 |
| Mobile port | ⏸ Setelah launch, kalau ada permintaan |
| Mod support | ⏸ Pasca-launch |

---

## 19. Ide yang Dipensiunkan (dari v1 / v2)

Dicatat supaya tidak muncul lagi tanpa keputusan sadar:

| Ide | Dari | Alasan pensiun |
|-----|------|----------------|
| Shelter/base building permanen | v1 | Bertabrakan dengan run-based; barricade per-floor sudah cukup |
| Skill tree 3 cabang in-run | v1 | Duplikasi dengan meta tree; menambah UI besar tanpa menambah keputusan |
| Wave 1–3 terjadwal tiap malam | v2 | Membuat map & barricade tidak berarti (§5.1) |
| Timer siang 70 detik | v2 | Terlalu pendek untuk satu objektif; memaksa pemain melewatkan loot |
| 15–25 malam per run | v1/v2 | Membuat run jadi maraton; diganti 5 malam yang masing-masing berarti |
| Scrap 50% carry saat mati | v2 | Menciptakan strategi "timbun lalu mati" (§11.1) |
| Sprite 8 arah | v2 | Biaya seni 2×, hasil terasa hampir sama untuk twin-stick (4 arah + rotasi senjata) |
| Deteksi spitter 250px | v2 | Di luar layar = tidak adil (§8.1) |
| 7 biome / 10 senjata / 30 achievement | v1/v2 | Di luar kapasitas 24 minggu |
| Judul "Dead Pixel" | v1/v2 | Bertabrakan dengan *Dead Pixels* (CSR-Studios, 2012) — zombie, pixel, prosedural |

---

## 20. Metrik & Protokol Playtest

### 20.1 Telemetri (CSV lokal, opt-in)

```text
Per run:   seed, survivor, floor_reached, death_cause, nights_survived,
           signal_earned, duration per fase
Per floor: waktu siang terpakai, kontainer diambil, barricade dibangun,
           bunk_down (ya/tidak), zombie dibunuh, damage diterima
Per event: event_id, detik event dimulai, damage diterima 10s setelahnya,
           pemain mati dalam 10s (ya/tidak), respon pemain (lari/fight/hide)
```

### 20.2 Yang Diukur (dan target sementaranya)

| Metrik | Target sementara | Kalau gagal, ubah apa |
|--------|------------------|------------------------|
| Funnel floor 1 → 2 | ≥70% tester | Kurangi malam floor 1, tambah tutorial |
| Funnel floor 3 → 4 | ≥40% | Kurangi budget malam floor 3 |
| Penyebab mati dominan | <35% dari satu penyebab | Rebalance sumber itu |
| Kematian <10s setelah event mulai | <15% | Perbaiki telegraph / pity rule |
| Pemain bunk down tiap malam | <25% | Malam terlalu keras atau siang terlalu pendek |
| Pemain tidak pernah bunk down | >0% (harus ada) | Bunk down kurang jelas ditawarkan |
| Median waktu siang terpakai | 70–90% dari timer | Kalau 100%, timer terlalu pendek |
| Ammo habis tapi tidak bisa craft | <20% run | Naikkan drop scrap / ammo |

### 20.3 Protokol

- 5 tester minggu 5 (think-aloud, 30 menit, tanpa arahan).
- 3 pertanyaan wajib setelah sesi: (1) Apa yang kamu takutkan malam itu? (2) Kapan kamu hampir mati dan kenapa itu salahmu? (3) Mau main lagi sekarang?
- Tester baru setiap fase, jangan pakai orang yang sama terus — bias.

---

## 21. Keputusan Terbuka (untuk didiskusikan)

| # | Pertanyaan | Default sementara di dokumen ini |
|---|-----------|----------------------------------|
| Q1 | Apakah `Bunk Down` terlalu mudah jadi "skip malam"? | Ada, tapi memicu 1 event dan menghanguskan loot malam |
| Q2 | Apakah Hunger perlu dipertahankan? | Ya, tapi ringan (−1/15s) — kalau playtest mengabaikannya, hapus |
| Q3 | Barricade inti atau aksesori? | Aksesori (maks 6 aktif) |
| Q4 | 5 floor cukup, atau 4 floor + 1 boss room terpisah? | 5 floor, boss di puncak floor 5 |
| Q5 | Judul "The End Has Come" perlu subtitle pemasaran? | Tidak di GDD; diputuskan saat bikin Steam page |
| Q6 | Apakah survivor berbeda harus mengubah run secara signifikan? | Ya: 1 perk + 1 stat berbeda, bukan karakter baru total |

---

_versi 3.0 — 26 Oktober 2026_

# <span style="color:#ffffff;background-color:#252523">Game Design Document (GDD)</span>

## <span style="color:#ffffff;background-color:#252523">2D Pixel-Art Zombie Survival Game</span>

## <span style="color:#ffffff;background-color:#252523">1\. Overview</span>

| <span style="color:#ffffff;background-color:#252523">Item</span> |   |
| --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">**Judul (Sementara)**</span> | <span style="color:#f4f0eb;background-color:#252523">*Dead Pixel: Survive the Night*</span><span style="color:#f4f0eb;background-color:#252523"> (contoh)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Genre**</span> | <span style="color:#f4f0eb;background-color:#252523">2D Top-Down / Side-Scroll Survival</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Art Style**</span> | <span style="color:#f4f0eb;background-color:#252523">Pixel Art (16-bit / 32-bit style)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Platform**</span> | <span style="color:#f4f0eb;background-color:#252523">PC (Steam), bisa expand ke Mobile</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Engine**</span> | <span style="color:#f4f0eb;background-color:#252523">Godot / Unity / GameMaker (pilih salah satu)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Target Audience**</span> | <span style="color:#f4f0eb;background-color:#252523">Gamer 15-35 tahun, fans survival & zombie genre</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Playtime**</span> | <span style="color:#f4f0eb;background-color:#252523">10-30 menit per run (roguelike) atau continuous (open world)</span> |

## <span style="color:#ffffff;background-color:#252523">2\. Core Concept (Konsep Inti)</span>

### <span style="color:inherit;background-color:#252523">**Elevator Pitch**</span>

> <span style="color:#c7c2bc;background-color:#252523">*"Bertahan hidup selama mungkin di dunia yang dipenuhi zombie. Cari resource, craft senjata, bangun shelter, dan survive setiap malam yang semakin brutal."*</span>

### <span style="color:inherit;background-color:#252523">**Design Pillars**</span>

<span style="color:#f4f0eb;background-color:#252523">🔫 1. SURVIVAL TENSION → Resource selalu terasa kurang, setiap keputusan penting </span>

<span style="color:#f4f0eb;background-color:#252523">🧟 2. ESCALATING THREAT → Zombie makin kuat & banyak seiring waktu </span>

<span style="color:#f4f0eb;background-color:#252523">🔨 3. CRAFTING & BUILDING → Player punya kebebasan craft & bangun pertahanan </span>

<span style="color:#f4f0eb;background-color:#252523">🎯 4. RISK vs REWARD → Explore lebih jauh = loot bagus tapi bahaya tinggi</span>

## <span style="color:#ffffff;background-color:#252523">3\. Core Gameplay Loop</span>

<span style="color:#f4f0eb;background-color:#252523">Ini adalah </span><span style="color:#f4f0eb;background-color:#252523">**jantung game**</span><span style="color:#f4f0eb;background-color:#252523"> — yang player lakukan berulang-ulang:</span>

```
text
    ┌─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
 ☀️ SIANG                                         │
 ├─ Explore map                                   │
 ├─ Scavenge resources (kayu, besi, makanan)      │
 ├─ Craft senjata & item                          │
 ├─ Upgrade/repair shelter                        │
 ├─ Trade dengan NPC (optional)                   │
 │                                                │
 ▼                                                │
 🌙 MALAM                                         │
 ├─ Zombie muncul (wave-based atau free-roam)     │
 ├─ Defend shelter / survive                      │
 ├─ Gunakan trap & senjata                        │
 ├─ Boss zombie (setiap X malam)                  │
 │                                                │
 ▼                                                │
 📊 HASIL                                         │
 ├─ Dapat XP / skill point                        │
 ├─ Unlock blueprint baru                         │
 ├─ Malam berikutnya = LEBIH SULIT ──────────────┘
```

---

## <span style="color:#ffffff;background-color:#252523">4\. Zombie Design</span>

### <span style="color:inherit;background-color:#252523">**Tipe Zombie**</span>

| <span style="color:#ffffff;background-color:#252523">TipePerilakuPertama MunculDifficulty</span> |   |   |   |
| --- | --- | --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">**Walker**</span> | <span style="color:#f4f0eb;background-color:#252523">Jalan pelan, serangan dekat</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 1</span> | <span style="color:#f4f0eb;background-color:#252523">⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Runner**</span> | <span style="color:#f4f0eb;background-color:#252523">Lari cepat, HP rendah</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 3</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Spitter**</span> | <span style="color:#f4f0eb;background-color:#252523">Serangan jarak jauh (acid)</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 5</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Tank**</span> | <span style="color:#f4f0eb;background-color:#252523">HP tinggi, lambat, damage besar</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 7</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Screamer**</span> | <span style="color:#f4f0eb;background-color:#252523">Panggil zombie lain jika melihat player</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 10</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Exploder**</span> | <span style="color:#f4f0eb;background-color:#252523">Meledak saat dekat player</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 12</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐⭐⭐</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Boss: The Hive**</span> | <span style="color:#f4f0eb;background-color:#252523">Boss besar, spawn zombie kecil</span> | <span style="color:#f4f0eb;background-color:#252523">Malam 15</span> | <span style="color:#f4f0eb;background-color:#252523">⭐⭐⭐⭐⭐</span> |

### <span style="color:inherit;background-color:#252523">**Spawning Rules**</span>

```
text
- Zombie spawn di luar layar / dari "dark zones"
- Jumlah zombie = base_count + (night_number × multiplier)
- Setiap 5 malam = mini-boss wave
- Setiap 15 malam = major boss
```

## <span style="color:#ffffff;background-color:#252523">5\. Player Systems</span>

### <span style="color:inherit;background-color:#252523">**A. Stats & Survival Needs**</span>

```
text
❤️ Health (HP)      → Berkurang saat diserang. Heal dengan medkit/makanan.
🍖 Hunger           → Turun seiring waktu. 0 = HP mulai berkurang.
⚡ Stamina          → Untuk sprint & melee attack. Regen otomatis.
🛡️ Armor            → Reduce damage. Bisa rusak seiring waktu.
```

### <span style="color:inherit;background-color:#252523">**B. Inventory System**</span>

```
text
┌──────────────────────────────┐
│  INVENTORY (Grid-based)      │
│  ┌──┬──┬──┬──┬──┬──┐        │
│  │🪓│🔫│🍖│🩹│🪵│⬜│        │
│  ├──┼──┼──┼──┼──┼──┤        │
│  │🔩│⬜│⬜│⬜│⬜│⬜│        │
│  └──┴──┴──┴──┴──┴──┘        │
│                              │
│  Slots: 12 (upgradeable)     │
│  Hotbar: 4 quick-access      │
└──────────────────────────────┘
```

### <span style="color:inherit;background-color:#252523">**C. Skill / Upgrade Tree**</span>

```
text
        🧑 SURVIVOR
       /     |      \
     🔫      🔨      🏃
   COMBAT  CRAFTING  AGILITY
    │        │         │
    ├ +DMG   ├ Faster  ├ +Speed
    ├ +Ammo  ├ Better  ├ +Stamina
    └ Crit%  └ New     └ Dodge%
               Recipes
```

## <span style="color:#ffffff;background-color:#252523">6\. Crafting System</span>

### <span style="color:inherit;background-color:#252523">**Resource Types**</span>

| <span style="color:#ffffff;background-color:#252523">ResourceSumberKegunaan</span> |   |   |
| --- | --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">🪵 Kayu</span> | <span style="color:#f4f0eb;background-color:#252523">Pohon, furnitur</span> | <span style="color:#f4f0eb;background-color:#252523">Barricade, senjata dasar</span> |
| <span style="color:#f4f0eb;background-color:#252523">🔩 Scrap Metal</span> | <span style="color:#f4f0eb;background-color:#252523">Mobil, bangunan</span> | <span style="color:#f4f0eb;background-color:#252523">Senjata, armor, trap</span> |
| <span style="color:#f4f0eb;background-color:#252523">🧪 Chemical</span> | <span style="color:#f4f0eb;background-color:#252523">Lab, apotek</span> | <span style="color:#f4f0eb;background-color:#252523">Medkit, molotov, ammo</span> |
| <span style="color:#f4f0eb;background-color:#252523">🔋 Electronics</span> | <span style="color:#f4f0eb;background-color:#252523">Toko, rumah</span> | <span style="color:#f4f0eb;background-color:#252523">Turret, lampu, upgrade</span> |
| <span style="color:#f4f0eb;background-color:#252523">🧵 Cloth</span> | <span style="color:#f4f0eb;background-color:#252523">Rumah, zombie drop</span> | <span style="color:#f4f0eb;background-color:#252523">Bandage, armor ringan</span> |

### <span style="color:inherit;background-color:#252523">**Contoh Crafting Recipes**</span>

```
text
🪵 × 5 + 🔩 × 3          → 🪓 Axe (Melee Weapon)
🔩 × 10 + 🔋 × 2         → 🔫 Pipe Gun (Ranged)
🧪 × 3 + 🧵 × 2          → 🩹 Medkit (Heal 50 HP)
🪵 × 10 + 🔩 × 5         → 🧱 Barricade (Defense)
🧪 × 2 + 🧵 × 1          → 🔥 Molotov (Area DMG)
🔩 × 15 + 🔋 × 5 + 🧪×3  → 🤖 Auto Turret (Defense)
```

---

## <span style="color:#ffffff;background-color:#252523">🗺️ 7. World Design</span>

### <span style="color:inherit;background-color:#252523">**Map Structure**</span>

```
text
┌──────────────────────────────────────────┐
│                                          │
│    🌲🌲  ⛺ SHELTER    🏥 Hospital      │
│    🌲🌲  (Safe Zone)   (Loot: Medical)  │
│                                          │
│    🏘️ Residential    🏭 Factory         │
│    (Loot: Food,      (Loot: Metal,      │
│     Cloth)            Electronics)       │
│                                          │
│    🏪 Market          ☠️ DARK ZONE       │
│    (Loot: Mixed,     (High Risk,        │
│     NPC Trader)       Rare Loot)        │
│                                          │
│    🅿️ Parking Lot    🔬 Lab             │
│    (Loot: Scrap)     (Loot: Chemical,   │
│                       Blueprint)         │
└──────────────────────────────────────────┘
```

### <span style="color:inherit;background-color:#252523">**Zone Difficulty**</span>

```
text
🟢 Safe Zone (Shelter)     → Tidak ada zombie
🟡 Residential Area        → Zombie density: LOW
🟠 Commercial Area         → Zombie density: MEDIUM
🔴 Industrial/Lab          → Zombie density: HIGH
⚫ Dark Zone               → Zombie density: EXTREME + rare loot
```

---

## <span style="color:#ffffff;background-color:#252523">⚔️ 8. Combat System</span>

### <span style="color:inherit;background-color:#252523">**Senjata Categories**</span>

| <span style="color:#ffffff;background-color:#252523">KategoriContohProsCons</span> |   |   |   |
| --- | --- | --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">**Melee**</span> | <span style="color:#f4f0eb;background-color:#252523">Bat, Axe, Knife</span> | <span style="color:#f4f0eb;background-color:#252523">No ammo, reliable</span> | <span style="color:#f4f0eb;background-color:#252523">Harus dekat</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Ranged**</span> | <span style="color:#f4f0eb;background-color:#252523">Pistol, Shotgun, Bow</span> | <span style="color:#f4f0eb;background-color:#252523">Aman dari jarak jauh</span> | <span style="color:#f4f0eb;background-color:#252523">Butuh ammo</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Throwable**</span> | <span style="color:#f4f0eb;background-color:#252523">Molotov, Grenade</span> | <span style="color:#f4f0eb;background-color:#252523">Area damage</span> | <span style="color:#f4f0eb;background-color:#252523">Limited supply</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Trap**</span> | <span style="color:#f4f0eb;background-color:#252523">Spike, Landmine, Turret</span> | <span style="color:#f4f0eb;background-color:#252523">Passive damage</span> | <span style="color:#f4f0eb;background-color:#252523">Butuh setup</span> |

### <span style="color:inherit;background-color:#252523">**Combat Feel (Penting!)**</span>

```
text
✅ Screen shake saat hit
✅ Knockback pada zombie
✅ Blood particle effects (pixel splatter)
✅ Hit-stop/freeze frame (2-3 frame) saat critical hit
✅ Muzzle flash untuk ranged weapon
✅ Sound feedback yang satisfying
```

---

## <span style="color:#ffffff;background-color:#252523">🌙 9. Day-Night Cycle & Difficulty Scaling</span>

```
text
TIMELINE PER CYCLE:
├── 00:00 ─ 06:00  → 🌙 MALAM (Zombie Active - DANGER)
├── 06:00 ─ 07:00  → 🌅 Pagi (Zombie mulai mundur)
├── 07:00 ─ 18:00  → ☀️ SIANG (Exploration Phase)
├── 18:00 ─ 19:00  → 🌆 Sore (Warning - siap-siap!)
└── 19:00 ─ 00:00  → 🌙 MALAM (Zombie mulai muncul)

REAL TIME: 1 game day = 10-15 menit real time (adjustable)
```

### <span style="color:inherit;background-color:#252523">**Difficulty Progression**</span>

```
text
Night  1-3:   Walker only, 10-20 zombie
Night  4-7:   +Runner, +Spitter, 30-50 zombie
Night  8-12:  +Tank, 50-80 zombie
Night 13-15:  +Screamer, +Exploder, 80-120 zombie
Night 15:     🔥 FIRST BOSS 🔥
Night 16+:    Everything scales harder
               Special mutated variants appear
```

---

## <span style="color:#ffffff;background-color:#252523">🎨 10. Art Direction</span>

### <span style="color:inherit;background-color:#252523">**Visual Style**</span>

```
text
Resolution  : 320×180 (upscaled to 1920×1080)
Tile Size   : 16×16 pixels
Color Palette: Limited (32-48 colors)

Mood Board Keywords:
- Dark & gritty tapi tetap readable
- Warna dominan: abu-abu, coklat, hijau gelap
- Highlight: merah (darah), kuning (api), putih (UI)
- Inspirasi: Project Zomboid, Death Road to Canada, Nuclear Throne
```

### <span style="color:inherit;background-color:#252523">**Animation Priority**</span>

```
text
Player:  Idle, Walk, Run, Attack(melee), Attack(ranged),
         Hurt, Death, Craft, Interact
Zombie:  Idle, Walk, Run, Attack, Hurt, Death,
         Special (per tipe)
```

---

## <span style="color:#ffffff;background-color:#252523">🔊 11. Audio Design</span>

| <span style="color:#ffffff;background-color:#252523">KategoriDetail</span> |   |
| --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">**BGM Siang**</span> | <span style="color:#f4f0eb;background-color:#252523">Ambient, tenang tapi uneasy</span> |
| <span style="color:#f4f0eb;background-color:#252523">**BGM Malam**</span> | <span style="color:#f4f0eb;background-color:#252523">Intens, fast-paced, adrenaline</span> |
| <span style="color:#f4f0eb;background-color:#252523">**BGM Boss**</span> | <span style="color:#f4f0eb;background-color:#252523">Epic, heavy percussion</span> |
| <span style="color:#f4f0eb;background-color:#252523">**SFX Zombie**</span> | <span style="color:#f4f0eb;background-color:#252523">Groaning, screaming, footsteps</span> |
| <span style="color:#f4f0eb;background-color:#252523">**SFX Combat**</span> | <span style="color:#f4f0eb;background-color:#252523">Impact sounds, gunshots, explosions</span> |
| <span style="color:#f4f0eb;background-color:#252523">**SFX UI**</span> | <span style="color:#f4f0eb;background-color:#252523">Click, craft complete, notification</span> |

## <span style="color:#ffffff;background-color:#252523">12\. UI/UX Layout</span>

```
text
┌──────────────────────────────────────────────┐
│ ❤️❤️❤️❤️ HP    🍖▓▓▓░ Hunger    Day 7 🌙   │
│                                              │
│                                              │
│                                              │
│              [GAME WORLD]                    │
│                                              │
│                                              │
│                                              │
│                                              │
│ ┌──┬──┬──┬──┐              🧭 Minimap       │
│ │🪓│🔫│🩹│🔥│ Hotbar       ┌─────────┐      │
│ └──┴──┴──┴──┘              │ · · ☠ · │      │
│ ⚡▓▓▓▓░░ Stamina           │ · 🏠 · · │      │
│                            └─────────┘       │
└──────────────────────────────────────────────┘
```

---

## <span style="color:#ffffff;background-color:#252523">🚀 13. Development Roadmap</span>

### <span style="color:inherit;background-color:#252523">**Phase 1: Prototype (Minggu 1-4)**</span>

```
text
☐ Player movement & basic controls
☐ Basic tilemap & world
☐ 1 melee weapon, 1 ranged weapon
☐ Walker zombie AI (chase, attack)
☐ Basic HP system
☐ Day-night cycle (visual only)
```

### <span style="color:inherit;background-color:#252523">**Phase 2: Core Loop (Minggu 5-10)**</span>

```
text
☐ Resource gathering
☐ Crafting system (3-5 recipes)
☐ Inventory UI
☐ Hunger system
☐ Zombie spawning berdasarkan malam
☐ 3 tipe zombie
☐ Basic shelter/barricade building
```

### <span style="color:inherit;background-color:#252523">**Phase 3: Content & Polish (Minggu 11-18)**</span>

```
text
☐ Semua tipe zombie
☐ Boss zombie
☐ Full crafting recipes
☐ Skill/upgrade tree
☐ Map expansion (semua zone)
☐ NPC trader
☐ Trap system
☐ Sound & music implementation
```

### <span style="color:inherit;background-color:#252523">**Phase 4: Testing & Launch (Minggu 19-24)**</span>

```
text
☐ Balancing (damage, spawn rate, resources)
☐ Bug fixing
☐ Performance optimization
☐ Playtesting feedback loop
☐ Trailer & store page
☐ LAUNCH 🚀
```

## <span style="color:#ffffff;background-color:#252523">✅ Quick Summary</span>

```
text
🎮 GAME = 2D Pixel Art Zombie Survival
🔁 LOOP = Explore (Siang) → Survive (Malam) → Upgrade → Repeat
🧟 HOOK = Zombie makin kuat tiap malam
⚡ FEEL = Satisfying combat + tense survival + rewarding crafting
🎯 MVP  = Player + Zombie + Combat + Day/Night + Crafting
```

\_\_\_

# <span style="color:#ffffff;background-color:#252523">Game Design Document v2.0</span>

## <span style="color:#ffffff;background-color:#252523">Dead Pixel: Survive the Night</span>

### <span style="color:#ffffff;background-color:#252523">Top-Down · Roguelike · Singleplayer · Procedural · Godot</span>

---

## <span style="color:#ffffff;background-color:#252523">📌 1. Updated Overview</span>

| <span style="color:#ffffff;background-color:#252523">ItemDetail</span> |   |
| --- | --- |
| <span style="color:#f4f0eb;background-color:#252523">**Genre**</span> | <span style="color:#f4f0eb;background-color:#252523">Top-Down Roguelike Zombie Survival</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Perspective**</span> | <span style="color:#f4f0eb;background-color:#252523">Top-Down (free rotation, mouse aim)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Structure**</span> | <span style="color:#f4f0eb;background-color:#252523">Roguelike (permadeath, procedural, run-based)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Multiplayer**</span> | <span style="color:#f4f0eb;background-color:#252523">Singleplayer Only</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Map**</span> | <span style="color:#f4f0eb;background-color:#252523">Procedurally Generated setiap run</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Engine**</span> | <span style="color:#f4f0eb;background-color:#252523">Godot 4.x (GDScript)</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Art Style**</span> | <span style="color:#f4f0eb;background-color:#252523">Pixel Art 16×16 tile, 320×180 native res</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Target Run Length**</span> | <span style="color:#f4f0eb;background-color:#252523">20-40 menit per run</span> |
| <span style="color:#f4f0eb;background-color:#252523">**Inspirasi**</span> | <span style="color:#f4f0eb;background-color:#252523">Nuclear Throne, Enter the Gungeon, Project Zomboid, Brotato</span> |

---

## <span style="color:#ffffff;background-color:#252523">🔄 2. Roguelike Structure</span>

### <span style="color:inherit;background-color:#252523">**A. Run Flow (Satu Siklus Run)**</span>

```
text
┌─────────────────────────────────────────────────────┐
│                    MULAI RUN                        │
│         (Pilih Survivor / Loadout awal)             │
└──────────────────────┬──────────────────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │       FLOOR / ZONE 1         │
        │  ┌────────────────────────┐  │
        │  │ ☀️ Siang: Explore      │  │
        │  │    Loot, Craft, Prep   │  │
        │  ├────────────────────────┤  │
        │  │ 🌙 Malam: Survive      │  │
        │  │    Wave 1-3 zombie     │  │
        │  └────────────────────────┘  │
        │         ✅ Clear?            │
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │       FLOOR / ZONE 2         │
        │  (Map baru, zombie lebih     │
        │   kuat, loot lebih bagus)    │
        │  ☀️ Explore → 🌙 Survive    │
        └──────────────┬───────────────┘
                       ▼
              ... repeat ...
                       ▼
        ┌──────────────────────────────┐
        │     FLOOR 5: BOSS RUN        │
        │  ☀️ Explore → 🌙 BOSS FIGHT │
        └──────────────┬───────────────┘
                       ▼
              ┌────────┴────────┐
              ▼                 ▼
         💀 MATI            🏆 MENANG
     (Run Over, Score)   (Unlock Ending,
      Stats, Unlocks)     Bonus Rewards)
              │                 │
              └────────┬────────┘
                       ▼
              🏠 HUB / META SCREEN
         (Upgrade permanen, pilih
          survivor baru, mulai run)
```

### <span style="color:inherit;background-color:#252523">**B. Run Parameters**</span>

```
text
📊 SETIAP RUN DI-GENERATE DENGAN:
├── Random Seed (bisa di-share untuk challenge)
├── 5-7 Floors/Zones per run
├── 3-5 Malam per floor (total ~15-25 malam per run)
├── Random loot tables per floor
├── Random zombie composition per floor
├── Random events (supply drop, horde, storm, dll)
└── Random boss di floor terakhir
```

### <span style="color:inherit;background-color:#252523">**C. Meta-Progression (Roguelite Elements)**</span>

> <span style="color:#c7c2bc;background-color:#252523">*Meskipun roguelike, meta-progression kecil membuat player tidak frustrasi.*</span>

```
text
🔓 UNLOCK YANG PERSIST ANTAR RUN:

├── 🧑 Survivor Baru
│   ├── Default: "The Scavenger" (balanced)
│   ├── Unlock: "The Medic" (start dengan medkit, +heal)
│   ├── Unlock: "The Engineer" (start dengan turret blueprint)
│   ├── Unlock: "The Runner" (+speed, -HP)
│   └── Unlock: "The Tank" (+HP, -speed)
│
├── 📜 Blueprint / Recipe Baru
│   ├── Muncul di crafting pool setelah unlock
│   └── Contoh: Unlock "Flamethrower" setelah kill 500 zombie
│
├── 🏠 Hub Upgrades (beli dengan "Scrap" yang dibawa saat mati)
│   ├── +1 Starting HP
│   ├── +2 Inventory Slots
│   ├── Start dengan random weapon
│   └── Discount di trader
│
└── 📖 Bestiary / Lore
    └── Unlock info zombie baru setelah encounter pertama
```

### <span style="color:inherit;background-color:#252523">**D. Death & Scoring**</span>

```
text
💀 SAAT MATI:
├── Tampilkan "Run Summary"
│   ├── Nights Survived: 14
│   ├── Zombies Killed: 342
│   ├── Floors Cleared: 3/5
│   ├── Damage Dealt: 12,450
│   └── Score: 8,750
│
├── "Scrap" yang dibawa = 50% dari total scrap saat mati
│   (bisa di-upgrade di meta agar bawa lebih banyak)
│
└── Unlock check → ada yang baru? → tampilkan!
```

---

## <span style="color:#ffffff;background-color:#252523">🗺️ 3. Procedural Map Generation</span>

### <span style="color:inherit;background-color:#252523">**A. Algoritma: Room-Based + Corridor (BSP Hybrid)**</span>

> <span style="color:#c7c2bc;background-color:#252523">*Cocok untuk top-down survival: ruang jelas, chokepoint natural, mudah di-navigate.*</span>

```
text
GENERATION PIPELINE (setiap floor):

Step 1: BSP TREE SPLIT
┌─────────────────────────────┐
│                             │
│  Bagi map jadi sub-areas    │
│  secara rekursif            │
│                             │
└─────────────────────────────┘
          ▼
Step 2: ROOM PLACEMENT
┌──────┐         ┌────────┐
│Room A│         │Room B  │
│      │         │        │
└──┬───┘         └───┬────┘
   │                 │
   │   ┌─────────┐   │
   └───┤ Room C  ├───┘
       │         │
       └────┬────┘
            │
       ┌────┴────┐
       │ Room D  │
       │ (Boss)  │
       └─────────┘
          ▼
Step 3: CORRIDOR CONNECTION
   Hubungkan semua room dengan
   corridor (A* atau direct L-shape)
          ▼
Step 4: POPULATE
   ├── Place spawn point (Room A)
   ├── Place exit/stairs (Room D)
   ├── Place loot containers (random)
   ├── Place crafting stations (1-2 per floor)
   ├── Place zombie spawn zones (dark areas)
   ├── Place obstacles (cars, debris, walls)
   └── Place trap opportunities
          ▼
Step 5: FOG OF WAR
   ├── Semua tile tersembunyi
   ├── Reveal berdasarkan line-of-sight player
   └── "Explored" tetap terlihat tapi gelap
```

### <span style="color:inherit;background-color:#252523">**B. Tile Types**</span>

```
text
🟫 Floor (walkable)
🧱 Wall (blocking, bisa dihancurkan sebagian)
🚪 Door (bisa dibuka/tutup, bisa di-barricade)
🪟 Window (bisa dilihat, zombie bisa break)
🌲 Tree (blocking, bisa di-chop untuk kayu)
🚗 Car (blocking, bisa meledak jika ditembak)
💧 Water (slow movement, tidak bisa bangun di sini)
🔥 Fire (damage over time, spreadable)
⬆️ Stairs (exit ke floor berikutnya)
📦 Crate (lootable, random isi)
🛢️ Barrel (meledak jika ditembak)
```

### <span style="color:inherit;background-color:#252523">**C. Floor Biomes (Variasi per Run)**</span>

```
text
🏘️ SUBURBAN     → Rumah, jalan, pagar. Loot: food, cloth
🏭 INDUSTRIAL   → Gudang, pabrik. Loot: metal, electronics
🏥 HOSPITAL     → Lorong sempit, kamar. Loot: medical, chemical
🌲 FOREST       → Pohon lebat, visibility rendah. Loot: wood, herbs
🏬 MALL         → Ruang besar, banyak loot, banyak zombie
🔬 LAB          → Trap, zombie spesial. Loot: rare blueprint
☠️ BUNKER       → Floor terakhir. Gelap, sempit, boss.
```

### <span style="color:inherit;background-color:#252523">**D. Godot Implementation Notes**</span>

```
gdscript
# Pseudocode struktur generation
func generate_floor(floor_number: int, seed_value: int):
    var rng = RandomNumberGenerator.new()
    rng.seed = seed_value + floor_number

    # 1. BSP split
    var bsp_tree = BSPTree.new(map_size, rng)
    bsp_tree.split(min_room_size=6, max_splits=5)

    # 2. Create rooms
    var rooms = bsp_tree.create_rooms(min_size=4, max_size=10)

    # 3. Connect corridors
    var corridors = connect_rooms(rooms, rng)

    # 4. Populate
    populate_rooms(rooms, floor_number, rng)
    place_spawn_and_exit(rooms)
    place_loot(rooms, floor_number, rng)
    place_zombie_zones(rooms, floor_number, rng)

    # 5. Apply to TileMap
    apply_to_tilemap(rooms, corridors)

    # 6. Setup Navigation
    navigation_region.bake_navigation_polygon()
```

---

## <span style="color:#ffffff;background-color:#252523">🎮 4. Top-Down Controls & Combat</span>

### <span style="color:inherit;background-color:#252523">**A. Control Scheme (Twin-Stick Style)**</span>

```
text
KEYBOARD + MOUSE:
┌─────────────────────────────────────────┐
│  W/A/S/D      → Movement (8 arah)      │
│  Mouse Move   → Aim direction          │
│  Left Click   → Attack (melee/ranged)  │
│  Right Click  → Secondary / Aim down   │
│  R            → Reload                 │
│  E            → Interact (loot, door)  │
│  Q            → Throw item             │
│  1-4          → Hotbar select          │
│  Tab          → Inventory              │
│  C            → Crafting menu          │
│  M            → Full map (explored)    │
│  Shift        → Sprint (pakai stamina) │
│  Space        → Dodge roll             │
└─────────────────────────────────────────┘
```

### <span style="color:inherit;background-color:#252523">**B. Aiming & Shooting System**</span>

```
text
        Mouse Cursor
            ✕
            │
            │  ← Bullet trajectory
            │
     🔫 Player
      ↗
   Sprite rotation
   mengikuti mouse angle

MELEE:
├── Swing arc 90° ke arah mouse
├── Hitbox aktif 0.2 detik
├── Knockback zombie yang terkena
└── Cooldown per senjata

RANGED:
├── Projectile dari player ke mouse direction
├── Bullet travel time (bukan hitscan) → bisa di-dodge
├── Spread (akurasi berkurang saat move)
├── Ammo system (reload manual)
└── Muzzle flash + screen shake
```

### <span style="color:inherit;background-color:#252523">**C. Field of View & Visibility**</span>

```
text
         ╲         ╱
          ╲  FOV  ╱     ← 120° cone ke arah mouse
           ╲     ╱
            ╲   ╱
        🔫 Player
            │
            │  ← Belakang = gelap/fog
            │

IMPLEMENTASI GODOT:
├── Light2D (point light) di player
├── Shadow casting dari wall tiles
├── Raycast2D untuk line-of-sight check
├── Fog of war shader (reveal explored area)
└── Zombie hanya detect player jika di FOV + LOS
```

### <span style="color:inherit;background-color:#252523">**D. Dodge Roll**</span>

```
text
⚡ STAMINA COST: 25%
⏱️ DURATION: 0.3 detik
📏 DISTANCE: 3 tile
🛡️ I-FRAMES: 0.25 detik (invincible)
⏳ COOLDOWN: 0.8 detik

→ Penting untuk escape dari swarm zombie
→ Bisa roll ke segala arah (WASD saat roll)
```

---

## <span style="color:#ffffff;background-color:#252523">🧟 5. Zombie AI (Top-Down Specific)</span>

### <span style="color:inherit;background-color:#252523">**A. State Machine**</span>

```
text
                    ┌──────────┐
            ┌──────►│   IDLE   │◄──────┐
            │       └────┬─────┘       │
            │            │              │
            │     Detect player         │ Lose sight
            │     (FOV + LOS)          │ > 8 detik
            │            │              │
            │       ┌────▼─────┐       │
            │       │  CHASE   ├───────┤
            │       └────┬─────┘       │
            │            │              │
            │     In attack range       │
            │            │              │
            │       ┌────▼─────┐       │
            │       │ ATTACK   ├───────┘
            │       └────┬─────┘
            │            │
            │     Player dead
            │            │
            │       ┌────▼─────┐
            └───────┤  WANDER  │
                    └──────────┘
```

### <span style="color:inherit;background-color:#252523">**B. Godot AI Implementation**</span>

```
gdscript
# zombie_ai.gd
extends CharacterBody2D

enum State { IDLE, WANDER, CHASE, ATTACK, DEAD }
var current_state = State.IDLE

@onready var nav_agent = $NavigationAgent2D
@onready var detection_area = $DetectionArea  # Area2D
@onready var attack_area = $AttackArea        # Area2D
@onready var sprite = $AnimatedSprite2D

var player: CharacterBody2D
var speed: float = 40.0
var damage: float = 10.0
var attack_cooldown: float = 1.0
var attack_timer: float = 0.0

func _physics_process(delta):
    match current_state:
        State.IDLE:
            _idle_state(delta)
        State.WANDER:
            _wander_state(delta)
        State.CHASE:
            _chase_state(delta)
        State.ATTACK:
            _attack_state(delta)
        State.DEAD:
            pass

func _chase_state(delta):
    nav_agent.target_position = player.global_position
    var direction = (nav_agent.get_next_path_position()
                     - global_position).normalized()
    velocity = direction * speed
    move_and_slide()

    # Face direction
    sprite.flip_h = direction.x < 0

    if attack_area.has_overlapping_bodies():
        current_state = State.ATTACK

func _attack_state(delta):
    attack_timer -= delta
    if attack_timer <= 0:
        _deal_damage_to_player()
        attack_timer = attack_cooldown

    if not attack_area.has_overlapping_bodies():
        current_state = State.CHASE
```

### <span style="color:inherit;background-color:#252523">**C. Zombie Behavior per Type (Top-Down)**</span>

```
text
🚶 WALKER
   ├── Pathfinding: Navigation2D, avoid obstacles
   ├── Speed: 30-40 px/s
   ├── Detect range: 150 px
   └── Behavior: Direct chase, melee attack

🏃 RUNNER
   ├── Speed: 80-100 px/s
   ├── Detect range: 200 px
   ├── Behavior: Rush langsung, bisa dodge trap? No.
   └── Weakness: HP rendah (1-2 hit)

🤮 SPITTER
   ├── Speed: 25 px/s
   ├── Detect range: 250 px
   ├── Behavior: Jaga jarak 100-150px, shoot projectile
   ├── Projectile: Acid blob, AoE poison pool
   └── Weakness: Melee range = helpless

🛡️ TANK
   ├── Speed: 20 px/s
   ├── HP: 5x normal
   ├── Behavior: Charge attack (dash ke player)
   ├── Charge: Break barricade & knockback player
   └── Weakness: Slow turn rate, bisa di-kite

📢 SCREAMER
   ├── Speed: 35 px/s
   ├── Behavior: Lari dari player, scream setiap 5 detik
   ├── Scream: Spawn 3-5 walker di sekitar screamer
   └── Priority: HARUS dibunuh duluan!

💥 EXPLODER
   ├── Speed: 50 px/s
   ├── Behavior: Rush player, explode saat dekat (50px)
   ├── Explosion: 80px radius, high damage
   └── Warning: Flashing red 2 detik sebelum explode
```

---

## <span style="color:#ffffff;background-color:#252523">🏗️ 6. Godot Technical Architecture</span>

### <span style="color:inherit;background-color:#252523">**A. Project Structure**</span>

```
text
res://
├── scenes/
│   ├── main.tscn              # Entry point, manages runs
│   ├── hub/
│   │   └── hub_screen.tscn    # Meta screen antar run
│   ├── game/
│   │   ├── game_world.tscn    # Active run world
│   │   ├── day_night_cycle.tscn
│   │   └── wave_manager.tscn
│   ├── player/
│   │   ├── player.tscn        # Player character
│   │   └── player_camera.tscn
│   ├── zombies/
│   │   ├── zombie_base.tscn   # Base zombie (inherited)
│   │   ├── walker.tscn
│   │   ├── runner.tscn
│   │   ├── spitter.tscn
│   │   ├── tank.tscn
│   │   ├── screamer.tscn
│   │   └── exploder.tscn
│   ├── items/
│   │   ├── pickup.tscn
│   │   ├── projectile.tscn
│   │   └── trap.tscn
│   ├── ui/
│   │   ├── hud.tscn
│   │   ├── inventory_ui.tscn
│   │   ├── crafting_ui.tscn
│   │   ├── minimap.tscn
│   │   └── run_summary.tscn
│   └── effects/
│       ├── blood_splatter.tscn
│       ├── explosion.tscn
│       └── muzzle_flash.tscn
│
├── scripts/
│   ├── autoload/
│   │   ├── game_manager.gd    # Run state, score, meta
│   │   ├── event_bus.gd       # Global signals
│   │   ├── save_manager.gd    # Meta-progression save
│   │   └── audio_manager.gd   # BGM & SFX
│   ├── generation/
│   │   ├── map_generator.gd   # BSP + room placement
│   │   ├── room_data.gd       # Room templates
│   │   ├── loot_table.gd      # Weighted random loot
│   │   └── biome_data.gd      # Biome rules per floor
│   ├── systems/
│   │   ├── crafting_system.gd
│   │   ├── inventory_system.gd
│   │   ├── day_night_system.gd
│   │   ├── wave_system.gd     # Zombie wave spawning
│   │   └── fog_of_war.gd
│   └── entities/
│       ├── player_controller.gd
│       ├── zombie_ai.gd
│       ├── weapon_base.gd
│       └── projectile.gd
│
├── resources/
│   ├── weapons/               # Weapon .tres files
│   ├── zombies/               # Zombie stat .tres files
│   ├── recipes/               # Crafting recipe .tres files
│   ├── loot_tables/           # Loot table .tres files
│   └── biomes/                # Biome config .tres files
│
├── assets/
│   ├── sprites/
│   │   ├── player/            # 8-direction spritesheets
│   │   ├── zombies/           # Per-type spritesheets
│   │   ├── tiles/             # Tileset per biome
│   │   ├── items/             # Item icons + world sprites
│   │   └── effects/           # Particles, blood, fire
│   ├── audio/
│   │   ├── bgm/
│   │   └── sfx/
│   └── fonts/
│       └── pixel_font.tres
│
└── project.godot
```

### <span style="color:inherit;background-color:#252523">**B. Key Godot Nodes & Systems**</span>

```
text
PLAYER NODE TREE:
Player (CharacterBody2D)
├── CollisionShape2D
├── AnimatedSprite2D (8-dir animation)
├── Camera2D
│   └── PointLight2D (player light + shadow)
├── AimRayCast (RayCast2D → mouse direction)
├── WeaponSlot (Node2D → rotate to mouse)
│   └── MuzzlePoint (Marker2D)
├── InteractionArea (Area2D)
├── HurtBox (Area2D)
├── DodgeCooldownTimer (Timer)
└── StaminaRegenTimer (Timer)

ZOMBIE NODE TREE:
ZombieBase (CharacterBody2D)
├── CollisionShape2D
├── AnimatedSprite2D
├── NavigationAgent2D (pathfinding)
├── DetectionArea (Area2D, radius per type)
├── AttackArea (Area2D, melee range)
├── HitBox (Area2D)
├── StateMachine (Node)
└── BloodParticles (GPUParticles2D)

GAME WORLD NODE TREE:
GameWorld (Node2D)
├── TileMapLayer (floor)
├── TileMapLayer (walls, collision)
├── TileMapLayer (decorations)
├── NavigationRegion2D (baked for zombie AI)
├── YSort (Node2D)
│   ├── Player
│   ├── Zombies (Node2D)
│   ├── Items (Node2D)
│   └── Traps (Node2D)
├── LightingLayer (CanvasModulate for day/night)
├── FogOfWar (Sprite2D + Shader)
├── WaveManager (Node)
├── DayNightCycle (Node)
└── SpawnPoints (Node2D, markers)
```

### <span style="color:inherit;background-color:#252523">**C. Signal Architecture (Event Bus)**</span>

```
gdscript
# autoload/event_bus.gd
extends Node

# Player
signal player_damaged(amount: int, source: String)
signal player_healed(amount: int)
signal player_died()
signal stamina_changed(current: float, max: float)

# Combat
signal zombie_killed(zombie_type: String, position: Vector2)
signal zombie_spawned(zombie_type: String)
signal player_attacked(weapon_type: String)

# Game Flow
signal day_started(day_number: int)
signal night_started(night_number: int)
signal wave_started(wave_number: int, zombie_count: int)
signal wave_cleared(wave_number: int)
signal floor_cleared(floor_number: int)
signal run_ended(score: int, nights_survived: int)

# Systems
signal item_picked_up(item_id: String, amount: int)
signal item_crafted(recipe_id: String)
signal inventory_full()
signal trap_triggered(trap_type: String, position: Vector2)

# UI
signal update_hud()
signal show_notification(text: String, type: String)
signal show_crafting_ui()
```

### <span style="color:inherit;background-color:#252523">**D. Data-Driven Design (Resources)**</span>

```
gdscript
# resources/weapon_data.gd
class_name WeaponData
extends Resource

@export var weapon_name: String
@export var weapon_type: enum { MELEE, RANGED, THROWABLE }
@export var damage: float
@export var attack_speed: float      # attacks per second
@export var range: float             # pixels
@export var ammo_max: int            # 0 = melee
@export var reload_time: float
@export var spread_angle: float      # degrees, 0 = perfect
@export var knockback: float
@export var sprite: Texture2D
@export var attack_animation: String
@export var sound_effect: AudioStream

# resources/zombie_data.gd
class_name ZombieData
extends Resource

@export var zombie_name: String
@export var max_hp: float
@export var speed: float
@export var damage: float
@export var attack_cooldown: float
@export var detection_range: float
@export var xp_reward: int
@export var loot_table: LootTable
@export var spritesheet: Texture2D
@export var special_ability: String  # "none", "spit", "charge", "scream", "explode"
```

---

## <span style="color:#ffffff;background-color:#252523">🌙 7. Day-Night & Wave System (Detailed)</span>

### <span style="color:inherit;background-color:#252523">**A. Cycle Timing**</span>

```
text
SATU GAME DAY = 120 detik real time (adjustable)

☀️ SIANG (70 detik):
├── 0-5s   : "Day X" notification
├── 5-60s  : Free exploration, loot, craft
├── 60-65s : Warning! "Night is approaching..."
└── 65-70s : Screen darkens, BGM changes

🌙 MALAM (50 detik):
├── 0-5s   : "Night X" + first wave spawns
├── 5-40s  : 2-3 waves of zombie
├── 40-45s : Final wave (hardest)
└── 45-50s : Dawn approaching, zombie flee
```

### <span style="color:inherit;background-color:#252523">**B. Wave Spawning Logic**</span>

```
gdscript
# wave_system.gd
func spawn_wave(night_number: int, wave_number: int):
    var base_count = 5 + (night_number * 3)
    var wave_multiplier = 1.0 + (wave_number * 0.3)
    var total_zombies = int(base_count * wave_multiplier)

    # Determine zombie composition
    var composition = get_composition(night_number)
    # Example night 5: { "walker": 0.5, "runner": 0.3, "spitter": 0.2 }

    var spawn_points = get_valid_spawn_points()  # Off-screen, dark zones

    for i in range(total_zombies):
        var zombie_type = pick_weighted_random(composition)
        var spawn_pos = spawn_points.pick_random()
        spawn_zombie(zombie_type, spawn_pos)
        await get_tree().create_timer(0.3).timeout  # Stagger spawns
```

---

## <span style="color:#ffffff;background-color:#252523">🚀 8. Updated Development Roadmap</span>

### <span style="color:inherit;background-color:#252523">**Phase 1: Core Prototype (Minggu 1-4)**</span>

```
text
🎯 GOAL: Player bisa gerak, tembak, zombie bisa mati

☐ Godot project setup (320×180, pixel snap ON)
☐ Player: 8-dir movement + mouse aim
☐ Player: basic melee attack (swing arc)
☐ Player: basic ranged attack (projectile)
☐ 1 test room (static tilemap)
☐ Walker zombie: spawn, chase, attack, die
☐ Basic HP system (player + zombie)
☐ Camera follow player
☐ Day/night visual (CanvasModulate color shift)
☐ PLACEHOLDER ART (colored rectangles OK)

✅ MILESTONE: Bisa jalan, tembak zombie, mati
```

### <span style="color:inherit;background-color:#252523">**Phase 2: Roguelike Foundation (Minggu 5-8)**</span>

```
text
🎯 GOAL: Procedural map + run structure berjalan

☐ BSP map generator (rooms + corridors)
☐ TileMap auto-tiling (floor, wall, door)
☐ NavigationRegion2D baking per generated map
☐ Fog of war (shader-based)
☐ Run state machine (start → floor → night → next floor → death)
☐ Wave spawner (zombie count scaling)
☐ Loot drops dari zombie (random pickup)
☐ Item pickup system
☐ Death screen + restart run
☐ Basic HUD (HP, ammo, night counter)

✅ MILESTONE: Bisa main 1 run dari awal sampai mati
```

### <span style="color:inherit;background-color:#252523">**Phase 3: Survival Systems (Minggu 9-14)**</span>

```
text
🎯 GOAL: Crafting, inventory, hunger, semua sistem survival

☐ Inventory system (grid-based)
☐ Crafting system + UI
☐ Resource types (wood, metal, chemical, cloth)
☐ Resource nodes di map (tree, crate, car)
☐ Hunger system
☐ Stamina + dodge roll
☐ Barricade building (placeable walls)
☐ Trap system (spike, mine)
☐ 3 senjata melee + 3 senjata ranged
☐ 4 tipe zombie (walker, runner, spitter, tank)
☐ Day/night full cycle dengan timer

✅ MILESTONE: Game terasa seperti survival, bukan sekadar shooter
```

### <span style="color:inherit;background-color:#252523">**Phase 4: Content & Polish (Minggu 15-20)**</span>

```
text
🎯 GOAL: Semua konten, meta-progression, game feel

☐ Semua tipe zombie (screamer, exploder)
☐ Boss zombie (floor 5)
☐ 3+ biome variations
☐ Meta-progression (hub, unlocks, scrap)
☐ 3 playable survivor (unlockable)
☐ Full weapon arsenal (8-10 senjata)
☐ Full crafting tree (15-20 recipes)
☐ Random events (supply drop, horde night, storm)
☐ Pixel art final (semua sprite)
☐ Sound effects + BGM
☐ Screen shake, particles, juice
☐ Run summary + scoring

✅ MILESTONE: Game lengkap, siap playtest
```

### <span style="color:inherit;background-color:#252523">**Phase 5: Balancing & Launch (Minggu 21-26)**</span>

```
text
🎯 GOAL: Balance, optimize, ship!

☐ Playtesting (minimal 10 tester)
☐ Difficulty balancing (zombie stats, loot rates, hunger)
☐ Performance optimization (object pooling, culling)
☐ Bug fixing
☐ Steam page / itch.io page
☐ Trailer
☐ Tutorial / first-run onboarding
☐ LAUNCH 🚀

✅ MILESTONE: Game rilis!
```

---

## <span style="color:#ffffff;background-color:#252523">⚡ 9. Godot-Specific Tips & Best Practices</span>

```
text
🔧 PERFORMANCE:
├── Gunakan Object Pooling untuk zombie & projectile
│   (jangan queue_free + instantiate terus-menerus)
├── NavigationRegion2D: rebake HANYA saat map berubah
├── Gunakan VisibleOnScreenNotifier2D untuk disable
│   zombie yang jauh dari kamera
├── TileMap: gunakan layers terpisah untuk floor/wall/deco
└── Particles: batasi max GPUParticles2D aktif

🔧 PIXEL ART SETUP:
├── Project Settings → Rendering → Textures:
│   ├── Default Texture Filter: Nearest
│   └── Canvas Items → Default Texture Filter: Nearest
├── Window → Stretch → Mode: viewport
├── Window → Stretch → Aspect: keep
└── Viewport size: 320×180, Window size: 1280×720

🔧 DEBUG:
├── Toggle fog of war dengan key (F1)
├── God mode (F2) untuk testing
├── Spawn zombie wave (F3)
├── Teleport ke exit (F4)
└── Print generation seed di console
```

---

## <span style="color:#ffffff;background-color:#252523">📊 10. Key Metrics to Track (Balancing)</span>

```
📈 DATA YANG PERLU DI-LOG SAAT PLAYTEST:

├── Average run duration (target: 20-40 min)
├── Death cause distribution (zombie type, hunger, boss)
├── Floor reached distribution (apakah floor 3 terlalu hard?)
├── Most used weapon (apakah ada weapon yang OP/useless?)
├── Resource economy (apakah player sering kehabisan ammo?)
├── Time spent crafting vs exploring vs fighting
├── Dodge roll usage frequency
└── Win rate (target: 10-20% untuk roguelike)
```

extends Node
## TUNING — semua angka di satu tempat (§20 GDD).
##
## Nilai bertanda GREYBOX dipendekkan agar bisa dites dalam hitungan menit.
## Angka produksi tetap yang tertulis di GDD §20 dan tidak boleh "dinaikkan"
## diam-diam hanya karena greybox terasa enak.

# --- geometri ---------------------------------------------------------------
const TILE := 16
const VIEW := Vector2i(320, 180)
const PLAYER_CANVAS := Vector2i(16, 24)
const PLAYER_PIVOT := Vector2i(8, 23)      # kaki di baseline (§17.3)

# --- player (§6.1) ----------------------------------------------------------
const HP_MAX := 100.0
const STAMINA_MAX := 100.0
const STAMINA_SPRINT := 18.0               # per detik
const STAMINA_REGEN := 22.0                # per detik setelah jeda
const STAMINA_REGEN_DELAY := 0.8
const BATTERY_MAX := 100.0
const BATTERY_FLASHLIGHT := 1.0            # per detik
const IFRAME_HIT := 0.6
const DODGE_STAMINA := 25.0
const DODGE_TIME := 0.30
const DODGE_IFRAME := 0.25
const DODGE_COOLDOWN := 0.8
const DODGE_DISTANCE := 48.0

const WALK_SPEED := 80.0
const SPRINT_SPEED := 128.0
const AIM_SPEED := 60.0

# --- berat / encumbrance (§8.5) --------------------------------------------
const CARRY_BASE := 30.0
const CARRY_BAG_SMALL := 40.0
const W_GEAR := 6.0                        # pistol 1.2 + wrench 2.2 + vest 2.6
const W_WOOD := 2.0
const W_SCRAP := 2.5

# --- waktu (§5.1) -----------------------------------------------------------
# GREYBOX: siang 120 s, malam 30 s. Produksi: 600 s / 180–300 s.
const DAY_SECONDS := 120.0
const DUSK_SECONDS := 10.0
const NIGHT_SECONDS := 30.0
const DAWN_SECONDS := 5.0
const NIGHT_GROWTH := 5.0                  # +5 s per hari (produksi +15)

# --- heat & serangan (§7) ---------------------------------------------------
const HEAT_LIGHT := 0.4                    # per detik saat lampu menyala
const HEAT_DECAY := 0.4                    # per detik saat lampu mati
const HEAT_ATTACK_CHANCE := {25.0: 0.25, 50.0: 0.60, 75.0: 0.90}
const ATTACK_CAP := 10                     # cap zombie bersamaan (greybox)

# --- zombie (§10.1) ---------------------------------------------------------
const Z_WALKER_HP := 30.0
const Z_WALKER_SPEED := 36.0
const Z_WALKER_DAMAGE := 8.0
const Z_WALKER_ATTACK_RANGE := 22.0
const Z_WALKER_ATTACK_CD := 1.0
const Z_WALKER_DETECT := 120.0
const DETECT_MAX := 150.0                  # batas keras layar (§5.4)

# --- kamera & dunia ---------------------------------------------------------
const ROOM := Vector2i(19, 10)             # ruangan greybox dalam tile
const ROOF_FADE := 0.30                    # alpha atap saat pemain di dalam (§17.12)


## Kecepatan jalan setelah dikoreksi berat (§8.5 tabel ambang).
func speed_for_weight(kg: float, sprinting := false, aiming := false) -> float:
	var cap := CARRY_BASE
	var ratio := kg / cap
	var base := SPRINT_SPEED if sprinting else WALK_SPEED
	if aiming:
		base = AIM_SPEED
	var mult := 1.0
	if ratio <= 0.5:
		mult = 1.00
	elif ratio <= 0.8:
		mult = 0.95
	elif ratio <= 1.0:
		mult = 0.85
	else:
		mult = 0.65
		if sprinting:
			base = WALK_SPEED          # kelebihan muatan: tidak bisa sprint
	return base * mult


## Nama status berat untuk HUD (§8.5).
func weight_status(kg: float) -> String:
	var ratio := kg / CARRY_BASE
	if ratio <= 0.5:
		return "RINGAN"
	elif ratio <= 0.8:
		return "BERMUATAN"
	elif ratio <= 1.0:
		return "BERAT"
	return "KELEBIHAN"


func weight_color(kg: float) -> Color:
	var ratio := kg / CARRY_BASE
	if ratio <= 0.5:
		return Color(0.45, 0.85, 0.55)
	elif ratio <= 0.8:
		return Color(0.92, 0.85, 0.42)
	elif ratio <= 1.0:
		return Color(0.95, 0.6, 0.3)
	return Color(0.92, 0.35, 0.35)


## Night pressure (§5.3): satu angka untuk speed & detect.
func pressure(day: int, phase: StringName) -> float:
	var floor_mult := minf(1.0 + 0.05 * float(day - 1), 2.0)
	var phase_mult := 1.0
	match phase:
		&"DUSK":
			phase_mult = 1.10
		&"NIGHT":
			phase_mult = 1.20
		&"DAWN":
			phase_mult = 1.00
	return minf(floor_mult * phase_mult, 2.0)


func speed_multiplier(day: int, phase: StringName) -> float:
	return minf(1.0 + (pressure(day, phase) - 1.0) * 0.4, 1.25)

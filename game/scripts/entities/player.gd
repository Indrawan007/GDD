extends CharacterBody2D
## Player greybox.
## Yang SUDAH ada: gerak 8 arah, berat → kecepatan, sprint/stamina, dodge + i-frame,
## lampu + baterai, interact (ambil kayu), Drop & Run (G), HP + i-frame saat kena.
## Yang BELUM: menembak, inventory grid, hunger/thirst (§8.1) — menyusul di Phase 2.

signal stats_changed

const DIR_NAMES := ["s", "se", "e", "ne", "n"]
const DIR_ANIM := ["s", "se", "e", "ne", "n", "ne", "e", "se"]
const DIR_FLIP := [false, false, false, false, false, true, true, true]

var hp: float = Tuning.HP_MAX
var stamina: float = Tuning.STAMINA_MAX
var battery: float = Tuning.BATTERY_MAX
var carry: float = Tuning.W_GEAR
var dead: bool = false

var _flashlight: bool = false
var _iframes: float = 0.0
var _stamina_delay: float = 0.0
var _dodge_time: float = 0.0
var _dodge_dir: Vector2 = Vector2.ZERO
var _dodge_cd: float = 0.0
var _dodge_requested: bool = false
var _vault_time: float = 0.0
var _vault_from: Vector2 = Vector2.ZERO
var _vault_to: Vector2 = Vector2.ZERO
var _attack_time: float = 0.0
var _light: PointLight2D

@onready var sprite: AnimatedSprite2D = $Sprite
@onready var shadow: Sprite2D = $Shadow
@onready var weapon: Node2D = $Weapon
@onready var camera: Camera2D = $Camera2D


func _ready() -> void:
	GameManager.player = self
	collision_layer = 2
	collision_mask = 1 | 8
	EventBus.emit_signal("weight_changed", carry, Tuning.weight_status(carry))
	EventBus.emit_signal("battery_changed", battery)


func _physics_process(delta: float) -> void:
	if dead:
		return

	_tick_timers(delta)
	_tick_light(delta)

	if _vault_time > 0.0:
		_vault_time = maxf(_vault_time - delta, 0.0)
		var t: float = 1.0 - (_vault_time / Tuning.VAULT_TIME)
		global_position = _vault_from.lerp(_vault_to, clampf(t, 0.0, 1.0))
		_iframes = maxf(_iframes, 0.1)
		if _vault_time <= 0.0:
			EventBus.emit_signal("vault_finished", Vector2i(roundi(_vault_to.x / 16.0), roundi(_vault_to.y / 16.0)))
		return

	var input := _read_move_input()
	var sprinting := Input.is_key_pressed(KEY_SHIFT) and input != Vector2.ZERO
	var aiming := Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)

	# --- dodge -------------------------------------------------------------
	if _dodge_requested:
		_dodge_requested = false
		if _dodge_cd <= 0.0 and stamina >= Tuning.DODGE_STAMINA and _dodge_time <= 0.0:
			_start_dodge(input)

	if _dodge_time > 0.0:
		velocity = _dodge_dir * (Tuning.DODGE_DISTANCE / Tuning.DODGE_TIME)
	else:
		if sprinting and stamina > 0.0 and Tuning.weight_status(carry) != "KELEBIHAN":
			stamina = maxf(stamina - Tuning.STAMINA_SPRINT * delta, 0.0)
			_stamina_delay = Tuning.STAMINA_REGEN_DELAY
		else:
			sprinting = false
			if _stamina_delay <= 0.0:
				stamina = minf(stamina + Tuning.STAMINA_REGEN * delta, Tuning.STAMINA_MAX)
		velocity = input * Tuning.speed_for_weight(carry, sprinting, aiming)

	move_and_slide()
	_face_mouse()
	_update_animation(input, sprinting)


func _tick_timers(delta: float) -> void:
	_iframes = maxf(_iframes - delta, 0.0)
	_dodge_cd = maxf(_dodge_cd - delta, 0.0)
	_dodge_time = maxf(_dodge_time - delta, 0.0)
	_stamina_delay = maxf(_stamina_delay - delta, 0.0)
	_attack_time = maxf(_attack_time - delta, 0.0)
	modulate.a = 0.55 if _iframes > 0.0 else 1.0


func _tick_light(delta: float) -> void:
	if _flashlight and battery > 0.0:
		battery = maxf(battery - Tuning.BATTERY_FLASHLIGHT * delta, 0.0)
		EventBus.emit_signal("battery_changed", battery)
		if battery <= 0.0:
			_set_flashlight(false)
			EventBus.emit_signal("notify", "BATERAI HABIS", &"warn")


func _read_move_input() -> Vector2:
	var v := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT):
		v.x -= 1.0
	if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT):
		v.x += 1.0
	if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP):
		v.y -= 1.0
	if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN):
		v.y += 1.0
	# gamepad (kiri: gerak)
	var jx := Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	var jy := Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
	if Vector2(jx, jy).length() > 0.25:
		v = Vector2(jx, jy)
	return v.normalized()


func _start_dodge(input: Vector2) -> void:
	var dir := input
	if dir == Vector2.ZERO:
		dir = (get_global_mouse_position() - global_position).normalized()
	_dodge_dir = dir
	_dodge_time = Tuning.DODGE_TIME
	_dodge_cd = Tuning.DODGE_COOLDOWN
	_iframes = maxf(_iframes, Tuning.DODGE_IFRAME)
	stamina = maxf(stamina - Tuning.DODGE_STAMINA, 0.0)
	_stamina_delay = Tuning.STAMINA_REGEN_DELAY
	_play("dodge")


func _face_mouse() -> void:
	var aim := get_global_mouse_position() - global_position
	weapon.rotation = aim.angle()


func _update_animation(input: Vector2, sprinting: bool) -> void:
	if _dodge_time > 0.0 or _attack_time > 0.0:
		return
	if input == Vector2.ZERO:
		_play("idle", _dir_index_from_angle(0.0))
		return
	var idx := _dir_index_from_angle(input.angle())
	_play("walk", idx)
	sprite.speed_scale = 1.6 if sprinting else 1.0


## Sudut -> indeks 0..7 (S, SE, E, NE, N, NW, W, SW), lalu dipetakan ke 5 baris.
func _dir_index_from_angle(angle: float) -> int:
	var idx := int(round(angle / (PI / 4.0)))       # -4..4, 0 = kanan (E)
	idx = posmod(idx + 2, 8)                        # geser supaya 0 = S
	return idx


func _play(anim_base: String, dir_idx: int = 0) -> void:
	var mapped: String = DIR_ANIM[dir_idx % 8]
	var anim_name := StringName("%s_%s" % [anim_base, mapped])
	if sprite.sprite_frames and sprite.sprite_frames.has_animation(anim_name):
		if sprite.animation != anim_name:
			sprite.play(anim_name)
		sprite.flip_h = DIR_FLIP[dir_idx % 8]
	sprite.speed_scale = 1.0


# --- interaksi & input event ------------------------------------------------
func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey) or not event.pressed or event.echo:
		return
	match (event as InputEventKey).physical_keycode:
		KEY_F:
			_set_flashlight(not _flashlight)
		KEY_G:
			drop_bag()
		KEY_SPACE:
			_dodge_requested = true
		KEY_E:
			if not try_vault():
				try_pickup()
		KEY_R:
			recharge_battery()


func is_flashlight_on() -> bool:
	return _flashlight


func _set_flashlight(on: bool) -> void:
	_flashlight = on and battery > 0.0
	if _light:
		_light.enabled = _flashlight
	EventBus.emit_signal("flashlight_toggled", _flashlight)


## Masuk/keluar lewat jendela. Hanya jendela PECAH yang bisa dilewati (§4.7).
func try_vault() -> bool:
	if _vault_time > 0.0:
		return false
	if Tuning.weight_status(carry) == Tuning.VAULT_BLOCKED_WEIGHT:
		EventBus.emit_signal("notify", "Kelebihan muatan — buang tas dulu (G)", &"warn")
		return false

	var aim := (get_global_mouse_position() - global_position).normalized()
	if aim == Vector2.ZERO:
		return false
	var probe := global_position + aim * 14.0
	var target_cell := Vector2i(floori(probe.x / 16.0), floori(probe.y / 16.0))

	for w in get_tree().get_nodes_in_group("window"):
		if w.cell != target_cell:
			continue
		if not w.can_vault():
			EventBus.emit_signal("notify", "Jendela tidak bisa dilewati (utuh/papan/barikade)", &"warn")
			return true                       # konsumsi input, jangan jatuh ke loot
		_begin_vault(w.global_position + aim * 18.0)
		return true
	return false


func _begin_vault(dest: Vector2) -> void:
	_vault_from = global_position
	_vault_to = dest
	_vault_time = Tuning.VAULT_TIME
	_iframes = maxf(_iframes, Tuning.VAULT_TIME)
	stamina = maxf(stamina - 10.0, 0.0)
	_play("dodge", _dir_index_from_angle((dest - _vault_from).angle()))
	EventBus.emit_signal("vault_started", Vector2i(roundi(_vault_from.x / 16.0), roundi(_vault_from.y / 16.0)))
	EventBus.emit_signal("notify", "Melewati jendela…", &"info")


func try_pickup() -> void:
	var crates := get_tree().get_nodes_in_group("crate")
	for c in crates:
		if c.has_method("try_loot") and global_position.distance_to(c.global_position) < 20.0:
			if c.try_loot():
				add_weight(Tuning.W_WOOD)
				EventBus.emit_signal("notify", "+2 kg kayu", &"loot")
			return


func add_weight(kg: float) -> void:
	carry += kg
	EventBus.emit_signal("weight_changed", carry, Tuning.weight_status(carry))


## Drop & Run (§8.5): seluruh muatan non-gear jatuh, kecepatan langsung normal.
func drop_bag() -> void:
	if carry <= Tuning.W_GEAR:
		EventBus.emit_signal("notify", "Tidak ada yang bisa dibuang", &"warn")
		return
	var dropped := carry - Tuning.W_GEAR
	carry = Tuning.W_GEAR
	EventBus.emit_signal("bag_dropped", dropped)
	EventBus.emit_signal("weight_changed", carry, Tuning.weight_status(carry))
	EventBus.emit_signal("notify", "Tas dibuang: −%.1f kg" % dropped, &"bag")
	var bag := Bag.new()
	bag.amount = dropped
	bag.position = global_position
	get_parent().add_child(bag)


func recharge_battery() -> void:
	if battery >= Tuning.BATTERY_MAX:
		return
	if WorldClock.phase == &"NIGHT":
		EventBus.emit_signal("notify", "Generator tidak bisa dinyalakan saat malam", &"warn")
		return
	battery = Tuning.BATTERY_MAX
	EventBus.emit_signal("battery_changed", battery)
	EventBus.emit_signal("notify", "Baterai diisi penuh", &"ok")


func take_damage(amount: float, source: StringName = &"zombie") -> void:
	if dead or _iframes > 0.0:
		return
	hp = maxf(hp - amount, 0.0)
	_iframes = Tuning.IFRAME_HIT
	EventBus.emit_signal("player_damaged", amount, source)
	_attack_time = 0.25
	_play("hurt", 0)
	if hp <= 0.0:
		_dead()


func _dead() -> void:
	dead = true
	velocity = Vector2.ZERO
	_play("death", 0)
	EventBus.emit_signal("player_died")


func debug_revive() -> void:
	dead = false
	hp = Tuning.HP_MAX
	carry = Tuning.W_GEAR
	stamina = Tuning.STAMINA_MAX
	battery = Tuning.BATTERY_MAX
	modulate.a = 1.0
	_play("idle", 0)
	EventBus.emit_signal("weight_changed", carry, Tuning.weight_status(carry))

extends Node2D
## Main greybox: membangun 1 ruangan (19×10 tile), shelter, pemain, lalu
## menjalankan siklus siang–malam + heat + serangan malam sederhana.
##
## CATATAN JUJUR: lantai & dinding di sini masih Sprite2D per tile supaya
## nol risiko API. Build produksi memakai TileMapLayer + autotile (§17.2).

const TILE := 16

var _player                      # untyped: akses properti script (hp, carry, dead)
var _ysort: Node2D
var _roof_root: Node2D
var _world_root: Node2D
var _hud                      # untyped: akses set_heat()

var _heat: float = 0.0
var _attack_timer: float = 0.0
var _attack_wave: int = 0
var _inside_room: bool = false
var _last_delta: float = 0.016


func _ready() -> void:
	GameManager.reset()

	_world_root = Node2D.new()
	_world_root.name = "World"
	add_child(_world_root)

	_build_room()

	_ysort = Node2D.new()
	_ysort.name = "YSort"
	_ysort.y_sort_enabled = true
	add_child(_ysort)

	_spawn_player()
	_spawn_crates()

	_build_roof()

	_hud = preload("res://scripts/hud.gd").new()
	add_child(_hud)

	EventBus.night_started.connect(_on_night_started)
	EventBus.zombie_killed.connect(_on_zombie_killed)
	EventBus.player_died.connect(_on_player_died)
	EventBus.notify.connect(_on_notify)

	EventBus.emit_signal("notify", "GREYBOX: WASD gerak · F lampu · E ambil · G buang tas · SPASI dodge", &"info")


# ---------------------------------------------------------------- world ----
func _build_room() -> void:
	var floor_a: Texture2D = load("res://assets/generated/floor_a.png")
	var floor_b: Texture2D = load("res://assets/generated/floor_b.png")
	var wall_tex: Texture2D = load("res://assets/generated/wall.png")
	var size: Vector2i = Tuning.ROOM

	for x in range(-1, size.x + 1):
		for y in range(-1, size.y + 1):
			var is_wall := x < 0 or y < 0 or x >= size.x or y >= size.y
			if is_wall:
				_add_static_tile(wall_tex, Vector2i(x, y), true)
			else:
				var t := floor_a if (x + y) % 2 == 0 else floor_b
				_add_static_tile(t, Vector2i(x, y), false)


func _add_static_tile(tex: Texture2D, cell: Vector2i, blocking: bool) -> void:
	var sprite := Sprite2D.new()
	sprite.texture = tex
	sprite.centered = false
	sprite.position = Vector2(cell.x * TILE, cell.y * TILE)
	_world_root.add_child(sprite)

	if blocking:
		var body := StaticBody2D.new()
		body.position = Vector2(cell.x * TILE + TILE * 0.5, cell.y * TILE + TILE * 0.5)
		body.collision_layer = 1
		body.collision_mask = 0
		var shape := CollisionShape2D.new()
		var rect := RectangleShape2D.new()
		rect.size = Vector2(TILE, TILE)
		shape.shape = rect
		body.add_child(shape)
		_world_root.add_child(body)


## Atap di-fade saat pemain di dalam ruangan (§17.12).
func _build_roof() -> void:
	_roof_root = Node2D.new()
	_roof_root.name = "Roof"
	_roof_root.z_index = 10
	add_child(_roof_root)

	var roof_tex: Texture2D = load("res://assets/generated/roof.png")
	var size: Vector2i = Tuning.ROOM
	for x in range(0, size.x):
		for y in range(0, size.y):
			var sprite := Sprite2D.new()
			sprite.texture = roof_tex
			sprite.centered = false
			sprite.position = Vector2(x * TILE, y * TILE)
			_roof_root.add_child(sprite)


func _spawn_player() -> void:
	var pl := CharacterBody2D.new()
	pl.name = "Player"
	pl.set_script(load("res://scripts/entities/player.gd"))
	pl.position = Vector2(3.5 * TILE, 5.0 * TILE)
	pl.z_index = 1

	# PENTING: anak dibuat SEBELUM masuk SceneTree, kalau tidak @onready di
	# player.gd ($Sprite, $Shadow, ...) sudah resolve ke null saat _ready().
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(10, 10)                     # collision 10×10 di kaki (§17.3)
	shape.shape = rect
	shape.position = Vector2(0, -5)
	pl.add_child(shape)

	var shadow := Sprite2D.new()
	shadow.name = "Shadow"
	shadow.texture = load("res://assets/generated/shadow.png")
	shadow.position = Vector2(0, -2)                # offset (0,−2) (§17.12)
	shadow.z_index = -1
	pl.add_child(shadow)

	var sprite := AnimatedSprite2D.new()
	sprite.name = "Sprite"
	sprite.sprite_frames = SpriteFactory.player_frames()
	sprite.offset = Vector2(0, -11)                 # pivot (8,23) → kaki di origin
	sprite.animation = &"idle_s"
	pl.add_child(sprite)

	var weapon := Line2D.new()
	weapon.name = "Weapon"
	weapon.points = PackedVector2Array([Vector2(2, 0), Vector2(12, 0)])
	weapon.width = 2.0
	weapon.default_color = Color(0.85, 0.82, 0.7)
	weapon.position = Vector2(0, -10)
	pl.add_child(weapon)

	var cam := Camera2D.new()
	cam.name = "Camera2D"
	cam.enabled = true
	cam.position_smoothing_enabled = false
	pl.add_child(cam)

	_player = pl
	_ysort.add_child(pl)


func _spawn_crates() -> void:
	for cell in [Vector2i(6, 2), Vector2i(13, 7), Vector2i(15, 2), Vector2i(8, 8)]:
		var crate := Crate.new()
		crate.position = Vector2(cell.x * TILE + 8, cell.y * TILE + 14)
		_ysort.add_child(crate)


# ---------------------------------------------------------------- loop -----
func _process(delta: float) -> void:
	_last_delta = delta
	_update_roof()
	_update_heat(delta)
	_update_night_attacks(delta)


func _update_roof() -> void:
	if _player == null:
		return
	var size: Vector2i = Tuning.ROOM
	var inside := _player.global_position.x > 0 and _player.global_position.y > 0 \
			and _player.global_position.x < size.x * TILE \
			and _player.global_position.y < size.y * TILE
	if inside != _inside_room:
		_inside_room = inside
	var target := Tuning.ROOF_FADE if inside else 1.0
	_roof_root.modulate.a = move_toward(_roof_root.modulate.a, target, 4.0 * _last_delta)


func _update_heat(delta: float) -> void:
	var lit := _player != null and _player.call("is_flashlight_on") == true
	if lit:
		_heat = minf(_heat + Tuning.HEAT_LIGHT * delta, 100.0)
	else:
		_heat = maxf(_heat - Tuning.HEAT_DECAY * delta, 0.0)
	EventBus.emit_signal("heat_changed", _heat)
	if _hud:
		_hud.set_heat(_heat)


func _update_night_attacks(delta: float) -> void:
	if WorldClock.phase != &"NIGHT" or _heat < 25.0:
		return
	_attack_timer -= delta
	if _attack_timer > 0.0:
		return
	_attack_timer = 8.0
	if GameManager.alive_zombies >= Tuning.ATTACK_CAP:
		return
	_attack_wave += 1
	var count := clampi(int(_heat / 30.0) + 1, 1, 4)
	for i in count:
		_spawn_zombie(_edge_position())


func _on_night_started(day: int, horde: bool) -> void:
	_attack_timer = 3.0
	_attack_wave = 0
	var msg := "MALAM %d" % day
	if horde:
		msg += " — HORDE"
	EventBus.emit_signal("notify", msg, &"night")
	if horde:
		for i in 4:
			_spawn_zombie(_edge_position())


func _edge_position() -> Vector2:
	# satu tile di dalam dinding, supaya tidak spawn di dalam collider
	var size: Vector2i = Tuning.ROOM
	var x_min := 1.0 * TILE
	var x_max := (size.x - 1) * TILE
	var y_min := 1.0 * TILE
	var y_max := (size.y - 1) * TILE
	match randi() % 4:
		0:
			return Vector2(randf_range(x_min, x_max), y_max)
		1:
			return Vector2(randf_range(x_min, x_max), y_min)
		2:
			return Vector2(x_min, randf_range(y_min, y_max))
		_:
			return Vector2(x_max, randf_range(y_min, y_max))


func _spawn_zombie(pos: Vector2) -> void:
	if GameManager.alive_zombies >= Tuning.ATTACK_CAP:
		return
	var z := Zombie.new()
	z.position = pos
	z.z_index = 1

	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(10, 10)
	shape.shape = rect
	shape.position = Vector2(0, -5)
	z.add_child(shape)

	var shadow := Sprite2D.new()
	shadow.texture = load("res://assets/generated/shadow.png")
	shadow.position = Vector2(0, -2)
	shadow.z_index = -1
	z.add_child(shadow)

	var sprite := AnimatedSprite2D.new()
	sprite.name = "Sprite"
	sprite.sprite_frames = SpriteFactory.walker_frames()
	sprite.offset = Vector2(0, -11)
	sprite.animation = &"idle_s"
	z.add_child(sprite)

	_ysort.add_child(z)


# ---------------------------------------------------------------- input ----
func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey) or not event.pressed or event.echo:
		return
	match (event as InputEventKey).physical_keycode:
		KEY_F5:
			WorldClock.skip_phase()
			EventBus.emit_signal("notify", "SKIP → %s" % WorldClock.phase, &"info")
		KEY_F3:
			_spawn_zombie(_edge_position())
			EventBus.emit_signal("notify", "Spawn 1 walker", &"info")
		KEY_F2:
			if _player and _player.has_method("debug_revive"):
				_player.call("debug_revive")
			EventBus.emit_signal("notify", "God mode / revive", &"info")
		KEY_F1:
			_roof_root.visible = not _roof_root.visible


func _on_zombie_killed(_kind: StringName, pos: Vector2) -> void:
	EventBus.emit_signal("notify", "Walker mati", &"kill")
	# greybox: hadiah kecil agar berat terasa
	if _player and _player.has_method("add_weight") and randf() < 0.5:
		_player.add_weight(Tuning.W_SCRAP)
		EventBus.emit_signal("notify", "+2.5 kg scrap", &"loot")


func _on_player_died() -> void:
	EventBus.emit_signal("notify", "MATI — tekan F2 untuk revive (greybox)", &"warn")


func _on_notify(_text: String, _kind: StringName) -> void:
	pass

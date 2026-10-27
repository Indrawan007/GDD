class_name WindowNode
extends Node2D
## Jendela dengan 4 state (§4.7). Node2D supaya bisa jadi titik NavigationLink.
##
##   intact    : lihat YA, masuk TIDAK, tembus peluru TIDAK (kaca pecah dulu)
##   broken    : lihat YA, masuk YA (vault 0,45 s), tembus peluru YA
##   boarded   : lihat TIDAK, masuk TIDAK, tembus TIDAK, HP 60
##   barricade : lihat TIDAK, masuk TIDAK, tembus TIDAK, HP 120

enum State { INTACT, BROKEN, BOARDED, BARRICADE }

const NAMES := ["intact", "broken", "boarded", "barricade"]
const HP_BY_STATE := {"boarded": 60.0, "barricade": 120.0, "intact": 20.0}
const VAULT_TIME := 0.45
const ZOMBIE_CLIMB_TIME := 1.2

var state: State = State.INTACT
var hp: float = 20.0
var cell: Vector2i = Vector2i.ZERO
var _sprite: Sprite2D
var _body: StaticBody2D
var _shape: CollisionShape2D


func setup(at_cell: Vector2i) -> void:
	cell = at_cell
	name = "Window_%d_%d" % [at_cell.x, at_cell.y]
	position = Vector2(at_cell.x * 16 + 8, at_cell.y * 16 + 8)

	_sprite = Sprite2D.new()
	_sprite.name = "Sprite"
	_sprite.offset = Vector2(0, -8)
	_sprite.z_index = 1
	add_child(_sprite)

	_body = StaticBody2D.new()
	_body.name = "Body"
	_body.collision_layer = 1 | 16          # dinding + layer vision blocker
	_body.collision_mask = 0
	_shape = CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(16, 16)
	_shape.shape = rect
	_body.add_child(_shape)
	add_child(_body)

	_apply(State.INTACT)


func _apply(new_state: State) -> void:
	state = new_state
	var key: String = NAMES[new_state]
	_sprite.texture = load("res://assets/generated/window_%s.png" % key)
	if HP_BY_STATE.has(key):
		hp = HP_BY_STATE[key]
	# pecah = tidak menahan gerak & tidak menahan pandangan.
	# Catatan: `state` (bukan parameter `new_state`) — pakai parameter lama akan
	# menggeser index enum dan membuat jendela PECAH justru menahan gerak.
	var punched: bool = state == State.BROKEN
	_body.set_collision_layer_value(1, not punched)
	_body.set_collision_layer_value(4, true)         # tetap bisa dihancurkan
	_body.set_collision_layer_value(5, not punched)  # layer vision blocker


# ---------------------------------------------------------------- publik ----
func blocks_movement() -> bool:
	return state != State.BROKEN


func blocks_vision() -> bool:
	return state == State.BOARDED or state == State.BARRICADE


func can_vault() -> bool:
	return state == State.BROKEN


func can_drop_through() -> bool:
	return state in (State.BROKEN, State.INTACT)     # keluar lewat jendela


## Peluru yang mengenai kaca utuh akan memecahkannya.
func on_projectile_hit() -> void:
	if state == State.INTACT:
		_smash()
	elif state in (State.BOARDED, State.BARRICADE):
		damage(20.0)


func damage(amount: float) -> void:
	if state in (State.INTACT, State.BROKEN):
		return
	hp -= amount
	if hp <= 0.0:
		if state == State.BARRICADE:
			_apply(State.BOARDED)      # barikade rusak → tinggal papan
			hp = 60.0
		else:
			_apply(State.BROKEN)       # papan hancur → lubang


func _smash() -> void:
	_apply(State.BROKEN)
	EventBus.emit_signal("window_changed", cell, StringName("broken"))
	EventBus.emit_signal("notify", "Kaca pecah — jendela bisa dilewati", &"warn")


func board_up() -> bool:
	if state != State.BROKEN:
		return false
	_apply(State.BOARDED)
	EventBus.emit_signal("window_changed", cell, StringName("boarded"))
	return true


func barricade_up() -> bool:
	if state != State.BOARDED:
		return false
	_apply(State.BARRICADE)
	EventBus.emit_signal("window_changed", cell, StringName("barricade"))
	return true

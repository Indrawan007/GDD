class_name Zombie
extends CharacterBody2D
## Walker greybox: chase + attack + mati. LOS memakai raycast ke layer 1 (dinding).
## Belum: NavigationAgent2D (menyusul di Phase 1; greybox pakai steering langsung),
## state INVESTIGATE, dan 6 tipe lain (§10).

const DIR_ANIM := ["s", "se", "e", "ne", "n", "ne", "e", "se"]
const DIR_FLIP := [false, false, false, false, false, true, true, true]

var hp: float = Tuning.Z_WALKER_HP
var dead: bool = false

var _attack_timer: float = 0.0
var _sight_timer: float = 0.0
var _has_target: bool = false

@onready var sprite: AnimatedSprite2D = $Sprite


func _ready() -> void:
	collision_layer = 8
	collision_mask = 1 | 2
	GameManager.alive_zombies += 1
	EventBus.emit_signal("zombie_spawned", &"walker")


func _physics_process(delta: float) -> void:
	if dead:
		return

	_attack_timer = maxf(_attack_timer - delta, 0.0)
	_sight_timer -= delta

	var p = GameManager.player          # untyped: butuh akses properti script (dead, take_damage)
	if p == null or not is_instance_valid(p) or p.get("dead") == true:
		velocity = velocity.lerp(Vector2.ZERO, 0.1)
		move_and_slide()
		return

	if _sight_timer <= 0.0:
		_sight_timer = 0.2                       # 5x/detik, bukan tiap frame (§10.4)
		_has_target = _can_see(p)

	if not _has_target:
		velocity = velocity.lerp(Vector2.ZERO, 0.08)
		move_and_slide()
		_play("idle")
		return

	var to_player := p.global_position - global_position
	var dist := to_player.length()

	if dist <= Tuning.Z_WALKER_ATTACK_RANGE:
		velocity = Vector2.ZERO
		move_and_slide()
		_play("attack")
		if _attack_timer <= 0.0:
			_attack_timer = Tuning.Z_WALKER_ATTACK_CD
			p.take_damage(Tuning.Z_WALKER_DAMAGE, &"walker")
		return

	var mult := Tuning.speed_multiplier(WorldClock.day, WorldClock.phase)
	velocity = to_player.normalized() * Tuning.Z_WALKER_SPEED * mult
	move_and_slide()
	_face(to_player)
	_play("walk")


func _can_see(p: Node2D) -> bool:
	var detect := minf(Tuning.Z_WALKER_DETECT * Tuning.pressure(WorldClock.day, WorldClock.phase),
			Tuning.DETECT_MAX)
	if global_position.distance_to(p.global_position) > detect:
		return false
	var query := PhysicsRayQueryParameters2D.create(global_position, p.global_position, 1)
	return get_world_2d().direct_space_state.intersect_ray(query).is_empty()


func _face(dir: Vector2) -> void:
	var idx := posmod(int(round(dir.angle() / (PI / 4.0))) + 2, 8)
	sprite.flip_h = DIR_FLIP[idx]


func _play(anim_base: String) -> void:
	var dir := _current_dir_index()
	var anim_name := StringName("%s_%s" % [anim_base, DIR_ANIM[dir % 8]])
	if sprite.sprite_frames and sprite.sprite_frames.has_animation(anim_name) and sprite.animation != anim_name:
		sprite.play(anim_name)


func _current_dir_index() -> int:
	var p = GameManager.player
	if p == null:
		return 0
	var dir := p.global_position - global_position
	if dir == Vector2.ZERO:
		return 0
	return posmod(int(round(dir.angle() / (PI / 4.0))) + 2, 8)


func take_damage(amount: float) -> void:
	if dead:
		return
	hp -= amount
	if hp <= 0.0:
		_die()


func _die() -> void:
	dead = true
	GameManager.alive_zombies = maxi(GameManager.alive_zombies - 1, 0)
	EventBus.emit_signal("zombie_killed", &"walker", global_position)
	_play("death")
	velocity = Vector2.ZERO
	await get_tree().create_timer(0.9).timeout
	queue_free()

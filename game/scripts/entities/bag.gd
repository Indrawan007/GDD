class_name Bag
extends Area2D
## Tas hasil Drop & Run (§8.5). Bisa diambil lagi; zombie tidak mengambilnya.

var amount: float = 0.0
var _arm: float = 1.2          # jangan langsung terambil saat baru dibuang


func _ready() -> void:
	add_to_group("bag")
	var sprite := Sprite2D.new()
	sprite.texture = load("res://assets/generated/bag.png")
	sprite.offset = Vector2(0, -8)
	add_child(sprite)

	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(12, 10)
	shape.shape = rect
	shape.position = Vector2(0, -4)
	add_child(shape)


func _process(delta: float) -> void:
	_arm = maxf(_arm - delta, 0.0)
	var p = GameManager.player
	if _arm > 0.0 or p == null or not is_instance_valid(p):
		return
	if p.get("dead") == true:
		return
	if global_position.distance_to(p.global_position) < 16.0:
		p.call("add_weight", amount)
		EventBus.emit_signal("bag_recovered", amount)
		EventBus.emit_signal("notify", "Tas diambil: +%.1f kg" % amount, &"bag")
		queue_free()

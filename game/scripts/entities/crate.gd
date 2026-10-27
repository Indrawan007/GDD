class_name Crate
extends StaticBody2D
## Kontainer greybox: berdiri sebagai penghalang, bisa di-loot sekali.

var looted: bool = false


func _ready() -> void:
	add_to_group("crate")
	collision_layer = 1
	collision_mask = 0
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(12, 12)
	shape.shape = rect
	shape.position = Vector2(0, -3)
	add_child(shape)

	var sprite := Sprite2D.new()
	sprite.texture = load("res://assets/generated/crate.png")
	sprite.offset = Vector2(0, -8)
	add_child(sprite)


func try_loot() -> bool:
	if looted:
		return false
	looted = true
	modulate = Color(0.55, 0.55, 0.55)
	return true

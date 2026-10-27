class_name SpriteFactory
extends RefCounted
## Membangun SpriteFrames dari atlas 8 arah di runtime.
## Atlas dibuat oleh tools/make_greybox_assets.py: 5 baris digambar (S, SE, E, NE, N),
## 3 arah sisanya = mirror (flip_h) sesuai §17.3.

const PLAYER_ATLAS := "res://assets/generated/player.png"
const WALKER_ATLAS := "res://assets/generated/walker.png"

const DIRS5 := ["s", "se", "e", "ne", "n"]

const PLAYER_ANIMS := [
	["idle", 2, 3.0, true],
	["walk", 6, 8.0, true],
	["attack_melee", 4, 12.0, false],
	["attack_ranged", 3, 12.0, false],
	["hurt", 2, 10.0, false],
	["death", 6, 10.0, false],
	["dodge", 4, 14.0, false],
	["interact", 3, 8.0, false],
]

const WALKER_ANIMS := [
	["idle", 2, 3.0, true],
	["walk", 4, 6.0, true],
	["attack", 4, 10.0, false],
	["hurt", 1, 8.0, false],
	["death", 5, 8.0, false],
]


static func _build(path: String, anims: Array, cell := Vector2i(16, 24)) -> SpriteFrames:
	var tex := load(path) as Texture2D
	var frames := SpriteFrames.new()
	frames.remove_animation("default")

	var col := 0
	for entry in anims:
		var anim_name: String = entry[0]
		var count: int = entry[1]
		var fps: float = entry[2]
		var loops: bool = entry[3]

		for row in DIRS5.size():
			var full := StringName("%s_%s" % [anim_name, DIRS5[row]])
			frames.add_animation(full)
			frames.set_animation_speed(full, fps)
			frames.set_animation_loop(full, loops)
			for i in count:
				var at := AtlasTexture.new()
				at.atlas = tex
				at.region = Rect2((col + i) * cell.x, row * cell.y, cell.x, cell.y)
				frames.add_frame(full, at)
		col += count

	return frames


static func player_frames() -> SpriteFrames:
	return _build(PLAYER_ATLAS, PLAYER_ANIMS)


static func walker_frames() -> SpriteFrames:
	return _build(WALKER_ATLAS, WALKER_ANIMS)

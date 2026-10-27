extends CanvasLayer
## HUD greybox. Menampilkan angka yang di GDD wajib terlihat tanpa buka menu:
## HP, stamina, baterai, BERAT (kg + status), hari & jam, heat. (§12.1, §15.1)

var _labels: Dictionary = {}
var _notify: Label
var _notify_timer: float = 0.0


func _ready() -> void:
	layer = 20
	_build()
	EventBus.weight_changed.connect(func(_kg, _s): _refresh())
	EventBus.battery_changed.connect(func(_v): _refresh())
	EventBus.heat_changed.connect(func(_v): _refresh())
	EventBus.notify.connect(_on_notify)
	EventBus.player_damaged.connect(func(_a, _s): _refresh())


func _mk(name: String, pos: Vector2, size := 7) -> Label:
	var l := Label.new()
	l.name = name
	l.position = pos
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", Color(0.92, 0.94, 0.9))
	_labels[name] = l
	add_child(l)
	return l


func _build() -> void:
	var band := ColorRect.new()
	band.color = Color(0.06, 0.07, 0.08, 0.72)
	band.position = Vector2(0, 0)
	band.size = Vector2(320, 26)
	add_child(band)

	_mk("stats", Vector2(4, 2))
	_mk("weight", Vector2(4, 10))
	_mk("clock", Vector2(200, 2), 7)
	_mk("phase", Vector2(200, 10), 7)
	_mk("heat", Vector2(4, 18), 6)

	_notify = _mk("notify", Vector2(4, 168), 7)
	_notify.add_theme_color_override("font_color", Color(0.98, 0.86, 0.55))


func _process(delta: float) -> void:
	_notify_timer = maxf(_notify_timer - delta, 0.0)
	if _notify_timer <= 0.0 and _notify:
		_notify.text = ""
	_refresh()


func _refresh() -> void:
	var p = GameManager.player
	if p == null or not is_instance_valid(p):
		return

	var hp: float = p.get("hp")
	var st: float = p.get("stamina")
	var bat: float = p.get("battery")
	var kg: float = p.get("carry")

	_labels["stats"].text = "HP %d   STAM %d   BAT %d" % [int(hp), int(st), int(bat)]

	var status: String = Tuning.weight_status(kg)
	var col: Color = Tuning.weight_color(kg)
	_labels["weight"].text = "%s  %.1f / %d kg" % [status, kg, int(Tuning.CARRY_BASE)]
	_labels["weight"].add_theme_color_override("font_color", col)

	_labels["clock"].text = "HARI %d  %s" % [WorldClock.day, WorldClock.clock_label()]
	_labels["phase"].text = _phase_label()
	_labels["phase"].add_theme_color_override("font_color", _phase_color())



func set_heat(value: float) -> void:
	var tier := "TENANG"
	if value >= 75.0:
		tier = "TERLALU BERISIK"
	elif value >= 50.0:
		tier = "BERISIK"
	elif value >= 25.0:
		tier = "WASPADA"
	_labels["heat"].text = "HEAT %d  %s" % [int(value), tier]
	_labels["heat"].add_theme_color_override(
		"font_color",
		Color(0.95, 0.55, 0.35) if value >= 50.0 else Color(0.75, 0.78, 0.72)
	)


func _phase_label() -> String:
	match WorldClock.phase:
		&"DAY": return "SIANG  %ds" % int(WorldClock.seconds_left())
		&"DUSK": return "SENJA  %ds" % int(WorldClock.seconds_left())
		&"NIGHT": return "MALAM  %ds" % int(WorldClock.seconds_left())
		_: return "SUBUH  %ds" % int(WorldClock.seconds_left())


func _phase_color() -> Color:
	match WorldClock.phase:
		&"DAY": return Color(0.98, 0.90, 0.55)
		&"DUSK": return Color(0.95, 0.62, 0.35)
		&"NIGHT": return Color(0.55, 0.65, 0.95)
		_: return Color(0.75, 0.85, 0.95)


func _on_notify(text: String, kind: StringName) -> void:
	if _notify == null:
		return
	_notify.text = text
	_notify_timer = 3.0
	match kind:
		&"warn":
			_notify.add_theme_color_override("font_color", Color(0.95, 0.45, 0.42))
		&"night":
			_notify.add_theme_color_override("font_color", Color(0.6, 0.72, 1.0))
		&"loot", &"bag":
			_notify.add_theme_color_override("font_color", Color(0.65, 0.9, 0.6))
		_:
			_notify.add_theme_color_override("font_color", Color(0.95, 0.9, 0.7))

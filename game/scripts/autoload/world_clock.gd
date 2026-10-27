extends Node
## Jam dunia (§5). Fase: DAY -> DUSK -> NIGHT -> DAWN -> hari berikutnya.
## GREYBOX: durasi dipendekkan lewat Tuning agar bisa dites cepat.

var day: int = 1
var phase: StringName = &"DAY"
var time_in_phase: float = 0.0
var running: bool = true


func _process(delta: float) -> void:
	if not running:
		return
	time_in_phase += delta
	EventBus.clock_tick.emit(day, seconds_left())

	match phase:
		&"DAY":
			if time_in_phase >= Tuning.DAY_SECONDS:
				_enter(&"DUSK")
		&"DUSK":
			if time_in_phase >= Tuning.DUSK_SECONDS:
				_enter(&"NIGHT")
		&"NIGHT":
			if time_in_phase >= night_length():
				_enter(&"DAWN")
		&"DAWN":
			if time_in_phase >= Tuning.DAWN_SECONDS:
				_next_day()


func night_length() -> float:
	return Tuning.NIGHT_SECONDS + Tuning.NIGHT_GROWTH * float(day - 1)


func phase_length() -> float:
	match phase:
		&"DAY": return Tuning.DAY_SECONDS
		&"DUSK": return Tuning.DUSK_SECONDS
		&"NIGHT": return night_length()
		_: return Tuning.DAWN_SECONDS


func seconds_left() -> float:
	return maxf(phase_length() - time_in_phase, 0.0)


func clock_label() -> String:
	var frac := clampf(1.0 - seconds_left() / maxf(phase_length(), 0.01), 0.0, 1.0)
	var hour := 0.0
	match phase:
		&"DAY": hour = 6.0 + frac * 12.0        # 06:00 -> 18:00
		&"DUSK": hour = 18.0 + frac * 2.0
		&"NIGHT": hour = 20.0 + frac * 9.0
		_: hour = 5.0 + frac
	var h := int(hour) % 24
	var m := int((hour - floor(hour)) * 60.0)
	return "%02d:%02d" % [h, m]


func _enter(new_phase: StringName) -> void:
	phase = new_phase
	time_in_phase = 0.0
	EventBus.phase_changed.emit(phase)

	if phase == &"NIGHT":
		EventBus.night_started.emit(day, is_horde_night())
	elif phase == &"DAWN":
		EventBus.night_ended.emit(day)


func _next_day() -> void:
	day += 1
	_enter(&"DAY")


func is_horde_night() -> bool:
	return day % 5 == 0


## Debug (F5): lompat ke fase berikutnya.
func skip_phase() -> void:
	match phase:
		&"DAY": _enter(&"DUSK")
		&"DUSK": _enter(&"NIGHT")
		&"NIGHT": _enter(&"DAWN")
		_: _next_day()

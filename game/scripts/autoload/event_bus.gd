extends Node
## Event bus global (§18.5 GDD). Semua sistem bicara lewat sini, bukan get_node.

signal player_damaged(amount: float, source: StringName)
signal player_died()
signal player_stats_changed()
signal weight_changed(kg: float, status: String)
signal battery_changed(value: float)
signal flashlight_toggled(on: bool)
signal bag_dropped(kg: float)
signal bag_recovered(kg: float)
signal window_changed(cell: Vector2i, state: StringName)
signal vault_started(from_cell: Vector2i)
signal vault_finished(to_cell: Vector2i)

signal zombie_spawned(kind: StringName)
signal zombie_killed(kind: StringName, pos: Vector2)

signal phase_changed(phase: StringName)
signal clock_tick(day: int, seconds_left: float)
signal night_started(day: int, horde: bool)
signal night_ended(day: int)
signal heat_changed(value: float)

signal notify(text: String, kind: StringName)

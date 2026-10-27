extends Node
## GameManager: referensi pemain/zombie + spawn, tanpa singleton-maze.

var player: Node2D = null
var zombie_parent: Node2D = null
var alive_zombies: int = 0


func reset() -> void:
	player = null
	zombie_parent = null
	alive_zombies = 0
	WorldClock.day = 1
	WorldClock.phase = &"DAY"
	WorldClock.time_in_phase = 0.0


func player_is_dead() -> bool:
	if player == null or not is_instance_valid(player):
		return true
	return player.get("dead") == true

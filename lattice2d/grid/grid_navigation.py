UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def get_distance(start_position, end_position):
	return abs(start_position[0] - end_position[0]) + abs(start_position[1] - end_position[1])

def get_direction(start_position, end_position):
	assert get_distance(start_position, end_position) == 1

	if start_position[1] < end_position[1]:
		return UP
	elif start_position[0] < end_position[0]:
		return RIGHT
	elif start_position[1] > end_position[1]:
		return DOWN
	else:
		return LEFT

def reverse_direction(direction):
	return (direction + 2) % 4
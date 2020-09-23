import math


def within_circle_bounds(start_position, end_position, radius):
	distance = math.sqrt(((start_position[0] - end_position[0]) ** 2) + ((start_position[1] - end_position[1]) ** 2))
	return distance < radius


def within_rect_bounds(start_position, end_position, dimensions):
	valid_x = start_position[0] - dimensions[0] // 2 < end_position[0] < start_position[0] + dimensions[0] // 2
	valid_y = start_position[1] - dimensions[1] // 2 < end_position[1] < start_position[1] + dimensions[1] // 2
	return valid_x and valid_y


def within_square_bounds(start_position, end_position, width):
	return within_rect_bounds(start_position, end_position, (width, width))

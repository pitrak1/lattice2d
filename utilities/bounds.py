import math

def within_circle_bounds(start_x, start_y, end_x, end_y, radius):
	distance = math.sqrt(((start_x - end_x) ** 2) + ((start_y - end_y) ** 2 ))
	return distance < radius

def within_rect_bounds(start_x, start_y, end_x, end_y, width, height):
	valid_x = end_x > start_x - width // 2 and end_x < start_x + width // 2
	valid_y = end_y > start_y - height // 2 and end_y < start_y + height // 2
	return valid_x and valid_y

def within_square_bounds(start_x, start_y, end_x, end_y, width):
	return within_rect_bounds(start_x, start_y, end_x, end_y, width, width)
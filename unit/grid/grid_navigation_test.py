import pytest
from lattice2d.grid.grid_navigation import \
	get_distance, \
	get_direction, \
	reverse_direction, \
	UP, \
	RIGHT, \
	DOWN, \
	LEFT

class TestGetDistance():
	def test_returns_distance_if_zero(self):
		assert get_distance((1, 1), (1, 1)) == 0

	def test_returns_distance_if_one(self):
		assert get_distance((2, 2), (1, 2)) == 1

	def test_returns_distance_if_more_than_one(self):
		assert get_distance((0, 0), (-3, -4)) == 7

class TestGetDirection():
	def test_throws_error_if_distance_is_not_one(self):
		with pytest.raises(AssertionError):
			get_direction((0, 0), (2, 0))

	def test_returns_direction(self):
		assert get_direction((1, 1), (1, 2)) == UP
		assert get_direction((-1, -2), (0, -2)) == RIGHT
		assert get_direction((0, 0), (0, -1)) == DOWN
		assert get_direction((2, 3), (1, 3)) == LEFT

class TestReverseDirection():
	def test_returns_the_opposite_of_the_given_direction(self):
		assert reverse_direction(UP) == DOWN
		assert reverse_direction(RIGHT) == LEFT
		assert reverse_direction(DOWN) == UP
		assert reverse_direction(LEFT) == RIGHT
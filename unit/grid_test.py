import pytest
from lattice2d.grid import UP, RIGHT, DOWN, LEFT, get_distance, get_direction, reverse_direction, Actor, EmptyTile, Tile, TileGrid
import types

class TestGetDistance():
	def test_returns_distance_if_zero(self):
		assert get_distance(1, 1, 1, 1) == 0

	def test_returns_distance_if_one(self):
		assert get_distance(2, 2, 1, 2) == 1

	def test_returns_distance_if_more_than_one(self):
		assert get_distance(0, 0, -3, -4) == 7

class TestGetDirection():
	def test_throws_error_if_distance_is_not_one(self):
		with pytest.raises(AssertionError):
			get_direction(0, 0, 2, 0)

	def test_returns_direction(self):
		assert get_direction(1, 1, 1, 2) == UP
		assert get_direction(-1, -2, 0, -2) == RIGHT
		assert get_direction(0, 0, 0, -1) == DOWN
		assert get_direction(2, 3, 1, 3) == LEFT

class TestReverseDirection():
	def test_returns_the_opposite_of_the_given_direction(self):
		assert reverse_direction(UP) == DOWN
		assert reverse_direction(RIGHT) == LEFT
		assert reverse_direction(DOWN) == UP
		assert reverse_direction(LEFT) == RIGHT

class TestActor():
	def test_allows_setting_grid_position(self):
		actor = Actor()
		actor.set_grid_position(1, 2)
		assert actor.grid_x == 1
		assert actor.grid_y == 2

class TestEmptyTile():
	def test_allows_setting_grid_position(self):
		tile = EmptyTile()
		tile.set_grid_position(1, 2)
		assert tile.grid_x == 1
		assert tile.grid_y == 2

class TestTile():
	def test_allows_setting_grid_position(self):
		tile = Tile()
		tile.set_grid_position(1, 2)
		assert tile.grid_x == 1
		assert tile.grid_y == 2

	class TestAddActor():
		def test_adds_actor_to_children(self):
			tile = Tile()
			actor = Actor()
			tile.add_actor(actor)
			assert tile.children == [actor]

		def test_sets_grid_position_of_actor(self):
			tile = Tile()
			tile.set_grid_position(1, 2)
			actor = Actor()
			tile.add_actor(actor)
			assert actor.grid_x == 1
			assert actor.grid_y == 2

	class TestRemoveActor():
		def test_throws_error_if_actor_is_not_in_children(self):
			tile = Tile()
			actor = Actor()
			with pytest.raises(AssertionError):
				tile.remove_actor(actor)

		def test_removes_actor_from_children(self):
			tile = Tile()
			actor = Actor()
			tile.add_actor(actor)
			tile.remove_actor(actor)
			assert len(actor.children) == 0

		def test_clears_actor_grid_position(self):
			tile = Tile()
			tile.set_grid_position(1, 2)
			actor = Actor()
			tile.add_actor(actor)
			tile.remove_actor(actor)
			assert actor.grid_x == None
			assert actor.grid_y == None

class TestTileGrid():
	def test_initializes_empty_grid(self):
		grid = TileGrid(5, 5)
		assert isinstance(grid.children[0], EmptyTile)
		assert isinstance(grid.children[5 * 5 - 1], EmptyTile)

	class TestAddTile():
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid(5, 5)
			with pytest.raises(AssertionError):
				grid.add_tile(-1, 0, {})
			with pytest.raises(AssertionError):
				grid.add_tile(5, 0, {})
			with pytest.raises(AssertionError):
				grid.add_tile(0, -1, {})
			with pytest.raises(AssertionError):
				grid.add_tile(0, 5, {})

		def test_adds_tile_to_children(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile(2, 1, tile)
			assert grid.children[1 * 5 + 2] == tile

		def test_sets_grid_position_for_tile(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile(2, 1, tile)
			assert tile.grid_x == 2
			assert tile.grid_y == 1

		def test_calls_add_adjacent_links_for_each_direction_if_within_range(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile(2, 1, tile)
			assert grid.add_adjacent_links.call_count == 4

		def test_does_not_call_add_adjacent_links_if_direction_out_of_bounds(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile(4, 4, tile)
			assert grid.add_adjacent_links.call_count == 2

	class TestAddActor():
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid(5, 5)
			with pytest.raises(AssertionError):
				grid.add_actor(-1, 0, {})
			with pytest.raises(AssertionError):
				grid.add_actor(5, 0, {})
			with pytest.raises(AssertionError):
				grid.add_actor(0, -1, {})
			with pytest.raises(AssertionError):
				grid.add_actor(0, 5, {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid(5, 5)
			with pytest.raises(AssertionError):
				grid.add_actor(3, 3, {})

		def test_calls_add_actor_on_tile(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile(3, 3, tile)
			mocker.patch.object(tile, 'add_actor')
			actor = Actor()
			grid.add_actor(3, 3, actor)
			tile.add_actor.assert_called_once_with(actor)

	class TestMoveActor():
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid(5, 5)
			with pytest.raises(AssertionError):
				grid.move_actor(-1, 0, {})
			with pytest.raises(AssertionError):
				grid.move_actor(5, 0, {})
			with pytest.raises(AssertionError):
				grid.move_actor(0, -1, {})
			with pytest.raises(AssertionError):
				grid.move_actor(0, 5, {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid(5, 5)
			with pytest.raises(AssertionError):
				grid.move_actor(3, 3, {})

		def test_calls_remove_actor_on_start_tile(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile(3, 3, start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile(3, 4, end_tile)

			actor = Actor()
			grid.add_actor(3, 3, actor)

			grid.move_actor(3, 4, actor)
			start_tile.remove_actor.assert_called_once_with(actor)

		def test_calls_add_actor_on_end_tile(self, mocker):
			grid = TileGrid(5, 5)
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile(3, 3, start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile(3, 4, end_tile)

			actor = Actor()
			grid.add_actor(3, 3, actor)

			grid.move_actor(3, 4, actor)
			end_tile.add_actor.assert_called_once_with(actor)


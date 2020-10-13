import pytest

from lattice2d.command import Command
from lattice2d.grid import \
	GridEntity, \
	TileGrid, \
	Tile, \
	get_distance, \
	get_direction, \
	reverse_direction, \
	UP, \
	RIGHT, \
	DOWN, \
	LEFT
from lattice2d.config import Config


class TestGetDistance:
	def test_returns_distance_if_zero(self):
		assert get_distance((1, 1), (1, 1)) == 0

	def test_returns_distance_if_one(self):
		assert get_distance((2, 2), (1, 2)) == 1

	def test_returns_distance_if_more_than_one(self):
		assert get_distance((0, 0), (-3, -4)) == 7


class TestGetDirection:
	def test_throws_error_if_distance_is_not_one(self):
		with pytest.raises(AssertionError):
			get_direction((0, 0), (2, 0))

	def test_returns_direction(self):
		assert get_direction((1, 1), (1, 2)) == UP
		assert get_direction((-1, -2), (0, -2)) == RIGHT
		assert get_direction((0, 0), (0, -1)) == DOWN
		assert get_direction((2, 3), (1, 3)) == LEFT


class TestReverseDirection:
	def test_returns_the_opposite_of_the_given_direction(self):
		assert reverse_direction(UP) == DOWN
		assert reverse_direction(RIGHT) == LEFT
		assert reverse_direction(DOWN) == UP
		assert reverse_direction(LEFT) == RIGHT


class TestGridEntity:
	def test_gets_and_sets_grid_position(self):
		entity = GridEntity()
		entity.set_grid_position((2, 3))
		assert entity.get_grid_position() == (2, 3)

	def test_gets_scaled_position_from_base_position_and_scale(self):
		entity = GridEntity()
		entity.set_grid_position((2, 3))

		command = Command('adjust_grid_position', {'base_position': (1, 2)})
		entity.on_command(command)

		command = Command('adjust_grid_scale', {'base_scale': 1.5})
		entity.on_command(command)

		(x, y) = entity.get_scaled_position((4, 5), (100, 200))
		assert x == (((2 + 4) * Config()['grid']['size'] + 100) * 1.5) + 1
		assert y == (((3 + 5) * Config()['grid']['size'] + 200) * 1.5) + 2


class TestTile:
	class TestAddActor:
		def test_adds_actor_to_children(self):
			tile = Tile()
			actor = GridEntity()
			tile.add_actor('some_key', actor)
			assert tile.get_actor('some_key') == actor

		def test_sets_grid_position_of_actor(self):
			tile = Tile()
			tile.set_grid_position((1, 2))
			actor = GridEntity()
			tile.add_actor('key', actor)
			assert actor.grid_position == (1, 2)

	class TestRemoveActor:
		def test_throws_error_if_actor_is_not_in_children(self):
			tile = Tile()
			with pytest.raises(AssertionError):
				tile.remove_actor('key')

		def test_removes_actor_from_children(self):
			tile = Tile()
			actor = GridEntity()
			tile.add_actor('key', actor)
			tile.remove_actor('key')
			with pytest.raises(KeyError):
				assert tile.get_actor('key')

		def test_clears_actor_grid_position(self):
			tile = Tile()
			tile.set_grid_position((1, 2))
			actor = GridEntity()
			tile.add_actor('key', actor)
			tile.remove_actor('key')
			assert actor.grid_position == (None, None)


class TestTileGrid:
	def test_initializes_empty_grid(self):
		grid = TileGrid((5, 5))
		assert isinstance(grid.get_tile_at_position((0, 0)), GridEntity)
		assert isinstance(grid.get_tile_at_position((4, 4)), GridEntity)

	class TestAddTile:
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.add_tile((-1, 0), {})
			with pytest.raises(AssertionError):
				grid.add_tile((5, 0), {})
			with pytest.raises(AssertionError):
				grid.add_tile((0, -1), {})
			with pytest.raises(AssertionError):
				grid.add_tile((0, 5), {})

		def test_adds_tile_to_children(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((2, 1), tile)
			assert grid.get_tile_at_position((2, 1)) == tile

		def test_sets_grid_position_for_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((2, 1), tile)
			assert tile.grid_position == (2, 1)

		def test_calls_add_adjacent_links_for_each_direction_if_within_range(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((2, 1), tile)
			assert grid.add_adjacent_links.call_count == 4

		def test_does_not_call_add_adjacent_links_if_direction_out_of_bounds(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((4, 4), tile)
			assert grid.add_adjacent_links.call_count == 2

	class TestAddActor:
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.add_actor((1, 0), 'key', {})
			with pytest.raises(AssertionError):
				grid.add_actor((5, 0), 'key', {})
			with pytest.raises(AssertionError):
				grid.add_actor((0, -1), 'key', {})
			with pytest.raises(AssertionError):
				grid.add_actor((0, 5), 'key', {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.add_actor((3, 3), 'some_key', {})

		def test_calls_add_actor_on_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((3, 3), tile)
			mocker.patch.object(tile, 'add_actor')
			actor = GridEntity()
			grid.add_actor((3, 3), 'key', actor)
			tile.add_actor.assert_called_once_with('key', actor)

	class TestMoveActor:
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.move_actor((0, 0), (-1, 0), {})
			with pytest.raises(AssertionError):
				grid.move_actor((0, 0), (5, 0), {})
			with pytest.raises(AssertionError):
				grid.move_actor((0, 0), (0, -1), {})
			with pytest.raises(AssertionError):
				grid.move_actor((0, 5), (0, 0), {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.move_actor((3, 2), (3, 3), {})

		def test_calls_remove_actor_on_start_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile((3, 3), start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile((3, 4), end_tile)

			actor = GridEntity()
			grid.add_actor((3, 3), 'key', actor)

			grid.move_actor((3, 3), (3, 4), 'key')
			start_tile.remove_actor.assert_called_once_with('key')

		def test_calls_add_actor_on_end_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile((3, 3), start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile((3, 4), end_tile)

			actor = GridEntity()
			grid.add_actor((3, 3), 'key', actor)

			grid.move_actor((3, 3), (3, 4), 'key')
			end_tile.add_actor.assert_called_once_with('key', actor)

	class TestAdjustGridPositionHandler:
		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'default_handler')
			command = Command('adjust_grid_position', {'adjust': (30, 40)})
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['base_position'] == (30, 40)

	class TestAdjustGridScaleHandler:
		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'default_handler')
			command = Command('adjust_grid_scale', {'adjust': 1.5})
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['base_scale'] == 1.5

	class TestMousePressHandler:
		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			grid.base_position = (50, 100)
			grid.base_scale = 0.5
			mocker.patch.object(grid, 'default_handler')
			command = Command('mouse_press', {'x': 150, 'y': 400})
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['x'] == 200
			assert get_positional_args(grid.default_handler, 0, 0).data['y'] == 600

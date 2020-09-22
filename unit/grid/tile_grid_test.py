import pytest
from lattice2d.grid.tile_grid import TileGrid
from lattice2d.grid.tile import Tile
from lattice2d.grid.actor import Actor
from lattice2d.grid.empty_tile import EmptyTile
from lattice2d.command import Command

class TestTileGrid():
	def test_initializes_empty_grid(self):
		grid = TileGrid((5, 5))
		assert isinstance(grid.children[0], EmptyTile)
		assert isinstance(grid.children[5 * 5 - 1], EmptyTile)

	class TestAddTile():
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
			assert grid.children[1 * 5 + 2] == tile

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

	class TestAddActor():
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.add_actor((1, 0), {})
			with pytest.raises(AssertionError):
				grid.add_actor((5, 0), {})
			with pytest.raises(AssertionError):
				grid.add_actor((0, -1), {})
			with pytest.raises(AssertionError):
				grid.add_actor((0, 5), {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.add_actor((3, 3), {})

		def test_calls_add_actor_on_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')
			tile = Tile()
			grid.add_tile((3, 3), tile)
			mocker.patch.object(tile, 'add_actor')
			actor = Actor()
			grid.add_actor((3, 3), actor)
			tile.add_actor.assert_called_once_with(actor)

	class TestMoveActor():
		def test_throws_error_if_indices_out_of_bounds(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.move_actor((-1, 0), {})
			with pytest.raises(AssertionError):
				grid.move_actor((5, 0), {})
			with pytest.raises(AssertionError):
				grid.move_actor((0, -1), {})
			with pytest.raises(AssertionError):
				grid.move_actor((0, 5), {})

		def test_throws_error_if_destination_is_not_tile(self):
			grid = TileGrid((5, 5))
			with pytest.raises(AssertionError):
				grid.move_actor((3, 3), {})

		def test_calls_remove_actor_on_start_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile((3, 3), start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile((3, 4), end_tile)

			actor = Actor()
			grid.add_actor((3, 3), actor)

			grid.move_actor((3, 4), actor)
			start_tile.remove_actor.assert_called_once_with(actor)

		def test_calls_add_actor_on_end_tile(self, mocker):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'add_adjacent_links')

			start_tile = Tile()
			mocker.patch.object(start_tile, 'remove_actor')
			grid.add_tile((3, 3), start_tile)

			end_tile = Tile()
			mocker.patch.object(end_tile, 'add_actor')
			grid.add_tile((3, 4), end_tile)

			actor = Actor()
			grid.add_actor((3, 3), actor)

			grid.move_actor((3, 4), actor)
			end_tile.add_actor.assert_called_once_with(actor)

	class TestAdjustGridPositionHandler():
		def test_adjust_base_position(self):
			grid = TileGrid((5, 5))
			command = Command('adjust_grid_position', { 'adjust': (30, 40) })
			grid.on_command(command)
			assert grid.base_position == (30, 40)

		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'default_handler')
			command = Command('adjust_grid_position', { 'adjust': (30, 40) })
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['base_position'] == (30, 40)
	
	class TestAdjustGridScaleHandler():
		def test_adjust_base_scale(self):
			grid = TileGrid((5, 5))
			command = Command('adjust_grid_scale', { 'adjust': 1.5 })
			grid.on_command(command)
			assert grid.base_scale == 1.5

		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			mocker.patch.object(grid, 'default_handler')
			command = Command('adjust_grid_scale', { 'adjust': 1.5 })
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['base_scale'] == 1.5
	
	class TestMousePressHandler():
		def test_updates_the_command_and_sends_to_default_handler(self, mocker, get_positional_args):
			grid = TileGrid((5, 5))
			grid.base_position = (50, 100)
			grid.base_scale = 0.5
			mocker.patch.object(grid, 'default_handler')
			command = Command('mouse_press', { 'x': 150, 'y': 400 })
			grid.on_command(command)
			assert get_positional_args(grid.default_handler, 0, 0).data['x'] == 200
			assert get_positional_args(grid.default_handler, 0, 0).data['y'] == 600
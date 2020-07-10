import pytest
from lattice2d.grid.tile import Tile
from lattice2d.grid.actor import Actor

class TestTile():
	class TestAddActor():
		def test_adds_actor_to_children(self):
			tile = Tile()
			actor = Actor()
			tile.add_actor(actor)
			assert tile.children == [actor]

		def test_sets_grid_position_of_actor(self):
			tile = Tile()
			tile.set_grid_position((1, 2))
			actor = Actor()
			tile.add_actor(actor)
			assert actor.grid_position == (1, 2)

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
			tile.set_grid_position((1, 2))
			actor = Actor()
			tile.add_actor(actor)
			tile.remove_actor(actor)
			assert actor.grid_position == (None, None)
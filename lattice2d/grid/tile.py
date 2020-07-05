from lattice2d.grid.grid_entity import GridEntity

class Tile(GridEntity):
	def add_actor(self, actor):
		self.children.append(actor)
		actor.set_grid_position(self.grid_position)

	def remove_actor(self, actor):
		assert actor in self.children

		self.children.remove(actor)
		actor.set_grid_position((None, None))
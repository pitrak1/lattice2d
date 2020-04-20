from lattice2d.nodes import Node

GRID_WIDTH = 10
GRID_HEIGHT = 10

class Actor(Node):
	def __init__(self):
		super().__init__()
		self.grid_x = None
		self.grid_y = None

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

class EmptyTile(Node):
	def __init__(self, grid_x=None, grid_y=None):
		super().__init__()
		self.grid_x = grid_x
		self.grid_y = grid_y

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

class Tile(EmptyTile):
	def add_actor(self, actor):
		self.children.append(actor)
		actor.set_position(self.grid_y, self.grid_y)

	def remove_actor(self, actor):
		assert actor in self.children

		self.children.remove(actor)
		actor.set_position(None, None)

class TileGrid(Node):
	def __init__(self):
		super().__init__()
		for i in range(GRID_HEIGHT * GRID_WIDTH):
			self.children.append(EmptyTile())

	def add_links(self, start_tile, end_tile):
		raise NotImplementedError

	def add_tile(self, grid_x, grid_y, tile):
		assert grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT

		self.children[grid_y * GRID_WIDTH + grid_x] = tile
		tile.set_position(grid_x, grid_y)

		if grid_y + 1 < GRID_HEIGHT:
			up_tile = self.children[(grid_y + 1) * GRID_WIDTH + grid_x]
			self.add_links(tile, up_tile)

		if grid_x + 1 < GRID_WIDTH:
			right_tile = self.children[grid_y * GRID_WIDTH + (grid_x + 1)]
			self.add_links(tile, right_tile)

		if grid_y - 1 >= 0:
			down_tile = self.children[(grid_y - 1) * GRID_WIDTH + grid_x]
			self.add_links(tile, down_tile)

		if grid_x - 1 >= 0:
			left_tile = self.children[grid_y * GRID_WIDTH + (grid_x - 1)]
			self.add_links(tile, left_tile)

	def add_actor(self, grid_x, grid_y, actor):
		assert grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT
		assert isinstance(self.children[grid_y * GRID_WIDTH + grid_x], Tile)
		self.children[grid_y * GRID_WIDTH + grid_x].add_actor(actor)

	def move_actor(self, grid_x, grid_y, actor):
		assert grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT
		assert isinstance(self.children[grid_y * GRID_WIDTH + grid_x], Tile)

		[start_x, start_y] = actor.get_grid_position()
		self.children[start_x * GRID_WIDTH + start_y].remove_actor(actor)
		self.children[grid_y * GRID_WIDTH + grid_x].add_actor(actor)



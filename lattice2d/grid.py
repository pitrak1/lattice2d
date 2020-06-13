from lattice2d.nodes import Node
from lattice2d.config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE
from lattice2d.utilities.bounds import within_square_bounds

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def get_distance(start_x, start_y, end_x, end_y):
	return abs(start_x - end_x) + abs(start_y - end_y)

def get_direction(start_x, start_y, end_x, end_y):
	assert get_distance(start_x, start_y, end_x, end_y) == 1

	if start_y < end_y:
		return UP
	elif start_x < end_x:
		return RIGHT
	elif start_y > end_y:
		return DOWN
	else:
		return LEFT

def reverse_direction(direction):
	return (direction + 2) % 4

class CommonGridEntity(Node):
	def __init__(self, grid_x=None, grid_y=None):
		super().__init__()
		self.grid_x = grid_x
		self.grid_y = grid_y

	def set_grid_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

class Actor(CommonGridEntity):
	pass

class EmptyTile(CommonGridEntity):
	pass

class CommonTile():
	def add_actor(self, actor):
		self.children.append(actor)
		actor.set_grid_position(self.grid_x, self.grid_y)

	def remove_actor(self, actor):
		assert actor in self.children

		self.children.remove(actor)
		actor.set_grid_position(None, None)

class Tile(CommonGridEntity, CommonTile):
	pass

class CommonScaledGridEntity(CommonGridEntity):
	def __init__(self, grid_x=None, grid_y=None, base_x=None, base_y=None):
		super().__init__(grid_x, grid_y)
		self.base_x = base_x
		self.base_y = base_y
		self.base_scale = 1.0

	def adjust_grid_position_handler(self, command):
		self.base_x = command.data['base_x']
		self.base_y = command.data['base_y']
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = command.data['base_scale']
		self.default_handler(command)

	def get_scaled_x_position(self, grid_x, offset_x):
		return ((grid_x * GRID_SIZE + offset_x) * self.base_scale) + self.base_x

	def get_scaled_y_position(self, grid_y, offset_y):
		return ((grid_y * GRID_SIZE + offset_y) * self.base_scale) + self.base_y

class ScaledActor(CommonScaledGridEntity):
	pass

class ScaledEmptyTile(CommonScaledGridEntity):
	pass

class ScaledTile(CommonScaledGridEntity, CommonTile):
	pass

class TileGrid(Node):
	def __init__(self, grid_height, grid_width):
		super().__init__()
		self.grid_height = grid_height
		self.grid_width = grid_width
		for i in range(self.grid_height * self.grid_width):
			self.children.append(EmptyTile(i % self.grid_width, i // self.grid_height))

	def add_adjacent_links(self, start_tile, end_tile):
		raise NotImplementedError

	def add_tile(self, grid_x, grid_y, tile):
		assert grid_x >= 0 and grid_x < self.grid_width and grid_y >= 0 and grid_y < self.grid_height

		self.children[grid_y * self.grid_width + grid_x] = tile
		tile.set_grid_position(grid_x, grid_y)

		if grid_y + 1 < self.grid_height:
			up_tile = self.children[(grid_y + 1) * self.grid_width + grid_x]
			self.add_adjacent_links(tile, up_tile)

		if grid_x + 1 < self.grid_width:
			right_tile = self.children[grid_y * self.grid_width + (grid_x + 1)]
			self.add_adjacent_links(tile, right_tile)

		if grid_y - 1 >= 0:
			down_tile = self.children[(grid_y - 1) * self.grid_width + grid_x]
			self.add_adjacent_links(tile, down_tile)

		if grid_x - 1 >= 0:
			left_tile = self.children[grid_y * self.grid_width + (grid_x - 1)]
			self.add_adjacent_links(tile, left_tile)

	def add_actor(self, grid_x, grid_y, actor):
		assert grid_x >= 0 and grid_x < self.grid_width and grid_y >= 0 and grid_y < self.grid_height
		assert isinstance(self.children[grid_y * self.grid_width + grid_x], Tile) or isinstance(self.children[grid_y * self.grid_width + grid_x], ScaledTile)
		self.children[grid_y * self.grid_width + grid_x].add_actor(actor)

	def move_actor(self, grid_x, grid_y, actor):
		assert grid_x >= 0 and grid_x < self.grid_width and grid_y >= 0 and grid_y < self.grid_height
		assert isinstance(self.children[grid_y * self.grid_width + grid_x], Tile) or isinstance(self.children[grid_y * self.grid_width + grid_x], ScaledTile)

		self.children[actor.grid_y * self.grid_width + actor.grid_x].remove_actor(actor)
		self.children[grid_y * self.grid_width + grid_x].add_actor(actor)

class ScaledTileGrid(TileGrid):
	def __init__(self, grid_width, grid_height, base_x=0, base_y=0):
		super().__init__(grid_width, grid_height)
		self.base_x = base_x
		self.base_y = base_y
		self.base_scale = 1.0

	def adjust_grid_position_handler(self, command):
		self.base_x += command.data['adjust_x']
		self.base_y += command.data['adjust_y']
		command.data.update({ 'base_x': self.base_x, 'base_y': self.base_y })
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = self.base_scale * command.data['adjust']
		command.data.update({ 'base_scale': self.base_scale })
		self.default_handler(command)

	def mouse_press_handler(self, command):
		command.data['x'] = (command.data['x'] - self.base_x) // self.base_scale
		command.data['y'] = (command.data['y'] - self.base_y) // self.base_scale
		self.default_handler(command)

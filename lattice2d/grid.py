from lattice2d.nodes import Node
from lattice2d.config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE
from lattice2d.utilities.bounds import within_square_bounds

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def get_distance(start_position, end_position):
	return abs(start_position[0] - end_position[0]) + abs(start_position[1] - end_position[1])

def get_direction(start_position, end_position):
	assert get_distance(start_position, end_position) == 1

	if start_position[1] < end_position[1]:
		return UP
	elif start_position[0] < end_position[0]:
		return RIGHT
	elif start_position[1] > end_position[1]:
		return DOWN
	else:
		return LEFT

def reverse_direction(direction):
	return (direction + 2) % 4

class CommonGridEntity(Node):
	def __init__(self, grid_position=(None, None)):
		super().__init__()
		self.grid_position = grid_position

	def set_grid_position(self, grid_position):
		self.grid_position = grid_position

class Actor(CommonGridEntity):
	pass

class EmptyTile(CommonGridEntity):
	pass

class CommonTile():
	def add_actor(self, actor):
		self.children.append(actor)
		actor.set_grid_position(self.grid_position)

	def remove_actor(self, actor):
		assert actor in self.children

		self.children.remove(actor)
		actor.set_grid_position((None, None))

class Tile(CommonGridEntity, CommonTile):
	pass

class CommonScaledGridEntity(CommonGridEntity):
	def __init__(self, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(grid_position)
		self.base_position = base_position
		self.base_scale = 1.0

	def adjust_grid_position_handler(self, command):
		self.base_position = command.data['base_position']
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = command.data['base_scale']
		self.default_handler(command)

	def get_scaled_x_position(self, grid_x, offset_x):
		return ((grid_x * GRID_SIZE + offset_x) * self.base_scale) + self.base_position[0]

	def get_scaled_y_position(self, grid_y, offset_y):
		return ((grid_y * GRID_SIZE + offset_y) * self.base_scale) + self.base_position[1]

class ScaledActor(CommonScaledGridEntity):
	pass

class ScaledEmptyTile(CommonScaledGridEntity):
	pass

class ScaledTile(CommonScaledGridEntity, CommonTile):
	pass

class TileGrid(Node):
	def __init__(self, grid_dimensions):
		super().__init__()
		self.grid_dimensions = grid_dimensions
		for i in range(self.grid_dimensions[0] * self.grid_dimensions[1]):
			self.children.append(EmptyTile((i % self.grid_dimensions[0], i // self.grid_dimensions[1])))

	def add_adjacent_links(self, start_tile, end_tile):
		raise NotImplementedError

	def add_tile(self, grid_position, tile):
		assert grid_position[0] >= 0 and grid_position[0] < self.grid_dimensions[0]
		assert grid_position[1] >= 0 and grid_position[1] < self.grid_dimensions[1]

		self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]] = tile
		tile.set_grid_position(grid_position)

		if grid_position[1] + 1 < self.grid_dimensions[1]:
			up_tile = self.children[(grid_position[1] + 1) * self.grid_dimensions[0] + grid_position[0]]
			self.add_adjacent_links(tile, up_tile)

		if grid_position[0] + 1 < self.grid_dimensions[0]:
			right_tile = self.children[grid_position[1] * self.grid_dimensions[0] + (grid_position[0] + 1)]
			self.add_adjacent_links(tile, right_tile)

		if grid_position[1] - 1 >= 0:
			down_tile = self.children[(grid_position[1] - 1) * self.grid_dimensions[0] + grid_position[0]]
			self.add_adjacent_links(tile, down_tile)

		if grid_position[0] - 1 >= 0:
			left_tile = self.children[grid_position[1] * self.grid_dimensions[0] + (grid_position[0] - 1)]
			self.add_adjacent_links(tile, left_tile)

	def add_actor(self, grid_position, actor):
		assert grid_position[0] >= 0 and grid_position[0] < self.grid_dimensions[0]
		assert grid_position[1] >= 0 and grid_position[1] < self.grid_dimensions[1]
		assert isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], Tile) or isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], ScaledTile)
		self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]].add_actor(actor)

	def move_actor(self, grid_position, actor):
		assert grid_position[0] >= 0 and grid_position[0] < self.grid_dimensions[0] and grid_position[1] >= 0 and grid_position[1] < self.grid_dimensions[1]
		assert isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], Tile) or isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], ScaledTile)

		self.children[actor.grid_position[1] * self.grid_dimensions[0] + actor.grid_position[0]].remove_actor(actor)
		self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]].add_actor(actor)

class ScaledTileGrid(TileGrid):
	def __init__(self, grid_dimensions, base_position=(0, 0)):
		super().__init__(grid_dimensions)
		self.base_position = base_position
		self.base_scale = 1.0

	def adjust_grid_position_handler(self, command):
		self.base_position = (self.base_position[0] + command.data['adjust'][0], self.base_position[1] + command.data['adjust'][1])
		command.data.update({ 'base_position': self.base_position })
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = self.base_scale * command.data['adjust']
		command.data.update({ 'base_scale': self.base_scale })
		self.default_handler(command)

	def mouse_press_handler(self, command):
		command.data['x'] = (command.data['x'] - self.base_position[0]) // self.base_scale
		command.data['y'] = (command.data['y'] - self.base_position[1]) // self.base_scale
		self.default_handler(command)

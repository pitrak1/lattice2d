from lattice2d.nodes.node import Node
from lattice2d.grid.empty_tile import EmptyTile
from lattice2d.grid.tile import Tile

class TileGrid(Node):
	def __init__(self, grid_dimensions, base_position=(0, 0)):
		super().__init__()
		self.grid_dimensions = grid_dimensions
		for i in range(self.grid_dimensions[0] * self.grid_dimensions[1]):
			self.children.append(EmptyTile((i % self.grid_dimensions[0], i // self.grid_dimensions[1])))
		self.base_position = base_position
		self.base_scale = 1.0

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
		assert isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], Tile)
		self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]].add_actor(actor)

	def move_actor(self, grid_position, actor):
		assert grid_position[0] >= 0 and grid_position[0] < self.grid_dimensions[0] and grid_position[1] >= 0 and grid_position[1] < self.grid_dimensions[1]
		assert isinstance(self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]], Tile)

		self.children[actor.grid_position[1] * self.grid_dimensions[0] + actor.grid_position[0]].remove_actor(actor)
		self.children[grid_position[1] * self.grid_dimensions[0] + grid_position[0]].add_actor(actor)

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
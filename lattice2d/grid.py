from lattice2d.config import Config
from lattice2d.nodes import Node

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


class GridEntity(Node):
	def __init__(self, grid_position=(None, None), base_position=(0, 0)):
		super().__init__()
		self.grid_position = grid_position
		self.base_position = base_position
		self.base_scale = 1.0

	def get_grid_position(self):
		return self.grid_position

	def set_grid_position(self, grid_position):
		self.grid_position = grid_position

	def set_base_position(self, position):
		self.base_position = position

	def adjust_grid_position_handler(self, command):
		self.base_position = command.data['base_position']
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = command.data['base_scale']
		self.default_handler(command)

	def get_scaled_position(self, grid_offset, raw_offset):
		x = (((self.grid_position[0] + grid_offset[0]) * Config()['grid']['size'] + raw_offset[0])
		     * self.base_scale) + self.base_position[0]
		y = (((self.grid_position[1] + grid_offset[1]) * Config()['grid']['size'] + raw_offset[1])
		     * self.base_scale) + self.base_position[1]
		return x, y


class Actor(GridEntity):
	def on_exit_tile(self, tile):
		pass

	def on_enter_tile(self, tile):
		pass

	def on_attack(self, actor):
		pass

	def on_defend(self, actor):
		pass


class Tile(GridEntity):
	def add_actor(self, key, actor):
		if self.before_actor_enter(actor): return
		if actor.on_enter_tile(self): return
		self.add_actor_without_callbacks(key, actor)
		self.after_actor_enter(actor)

	def add_actor_without_callbacks(self, key, actor):
		self._children[key] = actor
		actor.set_grid_position(self.grid_position)

	def remove_actor(self, key):
		assert key in self._children.keys()
		actor = self.get_actor(key)
		if self.before_actor_exit(actor): return
		if actor.on_exit_tile(self): return
		self.remove_actor_without_callbacks(key)
		self.after_actor_exit(actor)

	def remove_actor_without_callbacks(self, key):
		assert key in self._children.keys()
		self._children[key].set_grid_position((None, None))
		del self._children[key]

	def get_actor(self, key):
		assert key in self._children.keys()
		return self._children[key]

	def before_actor_enter(self, actor):
		pass

	def after_actor_enter(self, actor):
		pass

	def before_actor_exit(self, actor):
		pass

	def after_actor_exit(self, actor):
		pass


class TileGrid(Node):
	def __init__(self, grid_dimensions, base_position=(0, 0)):
		super().__init__()
		self._grid_dimensions = grid_dimensions
		for i in range(self._grid_dimensions[0] * self._grid_dimensions[1]):
			self._children[i] = Config()['empty_tile_class']((i % self._grid_dimensions[0], i // self._grid_dimensions[1]))
		self.base_position = base_position
		self.base_scale = 1.0

	def add_adjacent_links(self, start_tile, end_tile):
		raise NotImplementedError

	def get_tile_at_position(self, grid_position):
		return self._children[grid_position[1] * self._grid_dimensions[0] + grid_position[0]]

	def add_tile(self, grid_position, tile):
		assert 0 <= grid_position[0] < self._grid_dimensions[0]
		assert 0 <= grid_position[1] < self._grid_dimensions[1]

		self._children[grid_position[1] * self._grid_dimensions[0] + grid_position[0]] = tile
		tile.set_grid_position(grid_position)
		tile.base_position = self.base_position

		if grid_position[1] + 1 < self._grid_dimensions[1]:
			up_tile = self._children[(grid_position[1] + 1) * self._grid_dimensions[0] + grid_position[0]]
			self.add_adjacent_links(tile, up_tile)

		if grid_position[0] + 1 < self._grid_dimensions[0]:
			right_tile = self._children[grid_position[1] * self._grid_dimensions[0] + (grid_position[0] + 1)]
			self.add_adjacent_links(tile, right_tile)

		if grid_position[1] - 1 >= 0:
			down_tile = self._children[(grid_position[1] - 1) * self._grid_dimensions[0] + grid_position[0]]
			self.add_adjacent_links(tile, down_tile)

		if grid_position[0] - 1 >= 0:
			left_tile = self._children[grid_position[1] * self._grid_dimensions[0] + (grid_position[0] - 1)]
			self.add_adjacent_links(tile, left_tile)

	def add_actor(self, grid_position, key, actor):
		assert 0 <= grid_position[0] < self._grid_dimensions[0]
		assert 0 <= grid_position[1] < self._grid_dimensions[1]
		assert isinstance(self._children[grid_position[1] * self._grid_dimensions[0] + grid_position[0]], Tile)
		actor.set_base_position(self.base_position)
		self._children[grid_position[1] * self._grid_dimensions[0] + grid_position[0]].add_actor(key, actor)

	def move_actor(self, start_grid_position, end_grid_position, key):
		assert 0 <= start_grid_position[0] < self._grid_dimensions[0] \
		       and 0 <= start_grid_position[1] < self._grid_dimensions[1]
		assert 0 <= end_grid_position[0] < self._grid_dimensions[0] and 0 <= end_grid_position[1] < \
		       self._grid_dimensions[1]

		start_tile = self._children[start_grid_position[1] * self._grid_dimensions[0] + start_grid_position[0]]
		end_tile = self._children[end_grid_position[1] * self._grid_dimensions[0] + end_grid_position[0]]

		assert isinstance(end_tile, Tile)

		actor = start_tile.get_actor(key)
		if start_tile.before_actor_exit(actor): return
		if end_tile.before_actor_enter(actor): return
		if actor.on_exit_tile(start_tile): return
		if actor.on_enter_tile(end_tile): return
		start_tile.remove_actor_without_callbacks(key)
		end_tile.add_actor_without_callbacks(key, actor)
		if start_tile.after_actor_exit(actor): return
		end_tile.after_actor_enter(actor)

	def adjust_grid_position_handler(self, command):
		self.base_position = (
			self.base_position[0] + command.data['adjust'][0], self.base_position[1] + command.data['adjust'][1])
		command.data.update({'base_position': self.base_position})
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = self.base_scale * command.data['adjust']
		command.data.update({'base_scale': self.base_scale})
		self.default_handler(command)

	def mouse_press_handler(self, command):
		command.data['x'] = (command.data['x'] - self.base_position[0]) // self.base_scale
		command.data['y'] = (command.data['y'] - self.base_position[1]) // self.base_scale
		self.default_handler(command)

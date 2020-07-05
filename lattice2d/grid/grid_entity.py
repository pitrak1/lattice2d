from lattice2d.nodes.node import Node
from lattice2d.config import Config

class GridEntity(Node):
	def __init__(self, grid_position=(None, None), base_position=(0, 0)):
		super().__init__()
		self.grid_position = grid_position
		self.base_position = base_position
		self.base_scale = 1.0

	def set_grid_position(self, grid_position):
		self.grid_position = grid_position

	def adjust_grid_position_handler(self, command):
		self.base_position = command.data['base_position']
		self.default_handler(command)

	def adjust_grid_scale_handler(self, command):
		self.base_scale = command.data['base_scale']
		self.default_handler(command)

	def get_scaled_x_position(self, grid_x, offset_x):
		return ((grid_x * Config()['grid']['size'] + offset_x) * self.base_scale) + self.base_position[0]

	def get_scaled_y_position(self, grid_y, offset_y):
		return ((grid_y * Config()['grid']['size'] + offset_y) * self.base_scale) + self.base_position[1]
from lattice2d.utilities.log import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.grid.actor import Actor

class Player(Actor):
	def __init__(self, name, connection=None, game=None, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(grid_position, base_position)
		self.name = name
		self.connection = connection
		self.game = game
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.nodes import Node

class FullPlayer(Node):
	def __init__(self, name, connection, game=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.game = game
		self.grid_x = None
		self.grid_y = None

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

class FullPlayerList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		log(f'Adding {item.name} to player list', LOG_LEVEL_INTERNAL_LOW)
		super().append(item)

	def destroy_by_connection(self, connection):
		player = self.find_by_connection(connection)
		assert player
		log(f'Removing player {player.name} from player list', LOG_LEVEL_INTERNAL_LOW)
		if player.game: player.game.remove_player(player)
		for i in range(len(self)):
			if self[i].connection == player.connection:
				del self[i]

	def destroy_by_name(self, name):
		player = self.find_by_name(name)
		assert player
		log(f'Removing player {player.name} from player list', LOG_LEVEL_INTERNAL_LOW)
		if player.game: player.game.remove_player(player)
		for i in range(len(self)):
			if self[i].name == player.name:
				del self[i]
		
	def find_by_name(self, player_name):
		try:
			return next(player for player in self if player.name == player_name)
		except StopIteration:
			return False

	def find_by_connection(self, connection):
		try:
			return next(player for player in self if player.connection == connection)
		except StopIteration:
			return False
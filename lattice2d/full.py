from lattice2d.nodes import Node, RootNode
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.network import Server, NetworkCommand

FULL_COMMAND_TYPES = [
	'broadcast_players_in_game'
]

class FullPlayer(Node):
	def __init__(self, name, connection, game=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.game = game

class FullPlayerList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		super().append(item)

	def destroy_by_connection(self, connection):
		player = self.find_by_connection(connection)
		assert player
		if player.game: player.game.remove_player(player)
		for i in range(len(self)):
			if self[i].connection == player.connection:
				del self[i]

	def destroy_by_name(self, name):
		player = self.find_by_name(name)
		assert player
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

class FullGame(RootNode):
	def __init__(self, name, destroy_game):
		super().__init__()
		self.name = name
		self.players = FullPlayerList()
		self.destroy_game = destroy_game

	def add_player(self, player, host=False):
		assert player not in self.players
		player.game = self
		player.host = host
		self.players.append(player)
		self.send_players_in_game(player)

	def remove_player(self, player):
		assert player in self.players
		player.game = None
		self.players.remove(player)
		if self.players:
			self.send_players_in_game()
		else:
			self.destroy_game(self.name)

	def remove_player_by_connection(self, connection):
		pass

	def send_players_in_game(self, exception=None):
		parsed_players = [(player.name, player.host) for player in self.players]
		for player in self.players:
			if player != exception:
				NetworkCommand.create_and_send(
					'broadcast_players_in_game', 
					{ 'players': parsed_players }, 
					'success', 
					player.connection
				)

class FullGameList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		super().append(item)
		
	def add_player_to_game(self, game_name, player, host=False):
		game = self.find_by_name(game_name)
		assert game
		game.add_player(player, host)

	def destroy(self, game_name):
		game = self.find_by_name(game_name)
		assert game and len(game.players) == 0
		for i in range(len(self)):
			if self[i].name == game.name:
				del self[i]

	def find_by_name(self, game_name):
		try:
			return next(game for game in self if game.name == game_name)
		except StopIteration:
			return False

class FullServer(RootNode):
	def __init__(self):
		super().__init__()
		self.players = FullPlayerList()
		self.children = FullGameList()
		self.server = Server(self.add_command)

	def run(self):
		self.update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.update_thread.start()
		self.server.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def add_command(self, command):
		player = self.players.find_by_connection(command.connection)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', LOG_LEVEL_INTERNAL_LOW)
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.command_queue.append(command)

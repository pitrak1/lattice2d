import threading
from lattice2d.nodes import Node, RootNode, RootNodeWithHandlers
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.network import Server, NetworkCommand
from lattice2d.config import Config

class FullServerPlayer(Node):
	def __init__(self, name, connection, state=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.state = state

class FullServerPlayerList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		log(f'Adding {item.name} to player list', LOG_LEVEL_INTERNAL_LOW)
		super().append(item)

	def destroy_by_connection(self, connection):
		player = self.find_by_connection(connection)
		assert player
		log(f'Removing player {player.name} from player list', LOG_LEVEL_INTERNAL_LOW)
		if player.state: player.state.remove_player(player)
		for i in range(len(self)):
			if self[i].connection == player.connection:
				del self[i]

	def destroy_by_name(self, name):
		player = self.find_by_name(name)
		assert player
		log(f'Removing player {player.name} from player list', LOG_LEVEL_INTERNAL_LOW)
		if player.state: player.state.remove_player(player)
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

class FullServerState(Node):
	def __init__(self, set_state, add_command, name, destroy_game, players):
		super().__init__()
		self.set_state = set_state
		self.add_command = add_command
		self.name = name
		self.destroy_game = destroy_game
		self.players = players

	def add_player(self, player, host=False):
		assert player not in self.players
		log(f'Adding {player.name} to game {self.name}', LOG_LEVEL_INTERNAL_LOW)
		player.state = self
		player.host = host
		self.players.append(player)
		self.send_players_in_game(player)

	def remove_player(self, player):
		assert player in self.players
		log(f'Removing {player.name} from game {self.name}', LOG_LEVEL_INTERNAL_LOW)
		player.state = None
		self.players.remove(player)
		if self.players:
			self.send_players_in_game()
		else:
			self.destroy_game(self.name)

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

class FullServerGame(RootNode):
	def __init__(self, name, destroy_game):
		super().__init__()
		self.name = name
		self.current_state = Config().server_starting_state(self.set_state, self.add_command, self.name, destroy_game, FullServerPlayerList())
		self.children = [self.current_state]

	def set_state(self, state):
		self.current_state = state
		self.children = [self.current_state]

class FullServerGameList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		log(f'Adding {item.name} to game list', LOG_LEVEL_INTERNAL_LOW)
		super().append(item)
		
	def add_player_to_game(self, game_name, player, host=False):
		game = self.find_by_name(game_name)
		assert game
		log(f'Adding {player.name} to game {game_name} in game list', LOG_LEVEL_INTERNAL_LOW)
		player.state = game.current_state
		player.host = host
		game.current_state.players.append(player)

	def destroy(self, game_name):
		game = self.find_by_name(game_name)
		assert game and len(game.current_state.players) == 0
		log(f'Removing game {game_name} from game list', LOG_LEVEL_INTERNAL_LOW)
		for i in range(len(self)):
			if self[i].name == game.name:
				del self[i]

	def find_by_name(self, game_name):
		try:
			return next(game for game in self if game.name == game_name)
		except StopIteration:
			return False

class FullServer(RootNodeWithHandlers):
	def __init__(self):
		super().__init__()
		self.players = FullServerPlayerList()
		self.children = FullServerGameList()
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
		if player and player.state:
			log(f'Adding command type {command.type} to game {player.state.name}', LOG_LEVEL_INTERNAL_LOW)
			player.state.add_command(command)
		else:
			log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.command_queue.append(command)

def run():
	server = FullServer()
	server.run()

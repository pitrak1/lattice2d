import threading
from lattice2d.nodes import Node, RootNode, RootNodeWithHandlers
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.network import Server, NetworkCommand
from lattice2d.config import Config
from lattice2d.full.common import FullPlayer, FullPlayerList

class FullServerState(Node):
	def __init__(self, game):
		super().__init__()
		self.game = game

	def broadcast_players_in_game_handler(self, command):
		try:
			self.game.broadcast_players(command.data['exception'])
		except KeyError:
			self.game.broadcast_players()

	def leave_game_handler(self, command):
		self.game.remove_player(self.players.find_by_connection(command.connection))

	def get_current_player_handler(self, command):
		if self.game.is_current_player(self.game.players.find_by_connection(command.connection)):
			player_name = 'self'
		else:
			player_name = self.game.get_current_player().name
		command.update_and_send(status='success', data={ 'player_name': player_name })
	
class FullServerGame(RootNode):
	def __init__(self, name, destroy_game):
		super().__init__()
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.players = FullPlayerList()

	def set_state(self, state):
		self.current_state = state
		self.children = [self.current_state]

	def get_current_player(self):
		return self.players[self.current_player_index]

	def is_current_player(self, player):
		return player.connection == self.players[self.current_player_index].connection

	def add_player(self, player, host=False):
		assert player not in self.players
		log(f'Adding {player.name} to game {self.name}', LOG_LEVEL_INTERNAL_LOW)
		player.game = self
		player.host = host
		self.players.append(player)
		self.broadcast_players(player)

	def remove_player(self, player):
		assert player in self.players
		log(f'Removing {player.name} from game {self.name}', LOG_LEVEL_INTERNAL_LOW)
		player.game = None
		self.players.remove(player)
		if self.players:
			self.broadcast_players()
		else:
			self.destroy_game(self.name)

	def broadcast_players(self, exception=None):
		parsed_players = [(player.name, player.host) for player in self.players]
		for player in self.players:
			if player != exception:
				NetworkCommand.create_and_send(
					'broadcast_players_in_game', 
					{ 'players': parsed_players }, 
					'success', 
					player.connection
				)

class FullServerGameList(list):
	def append(self, item):
		assert not self.find_by_name(item.name)
		log(f'Adding {item.name} to game list', LOG_LEVEL_INTERNAL_LOW)
		super().append(item)
		
	def add_player_to_game(self, game_name, player, host=False):
		game = self.find_by_name(game_name)
		assert game
		log(f'Adding {player.name} to game {game_name} in game list', LOG_LEVEL_INTERNAL_LOW)
		game.add_player(player)

	def destroy(self, game_name):
		game = self.find_by_name(game_name)
		assert game and len(game.players) == 0
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
		self.players = FullPlayerList()
		self.children = FullServerGameList()

	def run(self):
		self.update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.update_thread.start()
		self.server.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def destroy_game_handler(self, command):
		self.children.destroy[command.data['game_name']]
		command.update_and_send(status='success')

	def create_player_handler(self, command):
		self.players.append(FullPlayer(command.data['player_name'], command.connection))
		command.update_and_send(status='success')

	def create_game_handler(self, command):
		self.children.append(FullServerGame(command.data['game_name'], self.children.destroy))
		command.update_and_send(status='success')

	def get_games_handler(self, command):
		parsed_games = [(game.name, len(game.players)) for game in self.children]
		command.update_and_send(status='success', data={ 'games': parsed_games })

	def join_game_handler(self, command):
		player = self.players.find_by_connection(command.connection)
		self.children.add_player_to_game(command.data['game_name'], player, False)
		command.update_and_send(status='success')

	def logout_handler(self, command):
		self.players.destroy_by_connection(command.connection)
		command.update_and_send(status='success')

	def add_command(self, command):
		player = self.players.find_by_connection(command.connection)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', LOG_LEVEL_INTERNAL_LOW)
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.command_queue.append(command)

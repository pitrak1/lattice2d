import threading
from lattice2d.nodes import Node, RootNode, RootNodeWithHandlers
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH, LOG_LEVEL_INTERNAL_LOW
from lattice2d.network import Server, NetworkCommand
from lattice2d.config import Config
from lattice2d.full.common import Player

class ServerState(Node):
	def __init__(self, game, custom_data):
		super().__init__()
		self.game = game
		self.custom_data = custom_data

	def broadcast_players_in_game_handler(self, command):
		if 'exception' in command.data.keys():
			self.game.broadcast_players(command.data['exception'])
		else:
			self.game.broadcast_players()

	def leave_game_handler(self, command):
		self.game.remove_player(self.players.find_by_connection(command.connection))

	def get_current_player_handler(self, command):
		player = next(iter(p for p in self.game.players if p.connection == command.connection), False)
		if self.game.is_current_player(player):
			player_name = 'self'
		else:
			player_name = self.game.get_current_player().name
		command.update_and_send(status='success', data={ 'player_name': player_name })
	
class ServerGame(RootNode):
	def __init__(self, name, destroy_game):
		super().__init__()
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.players = []
		self.__set_state(Config()['server_states']['starting_state'])

	def __set_state(self, state, custom_data={}):
		self.__current_state = state(self, custom_data)

		state_data = next(s for s in Config()['server_states']['states'] if s['state'] == state)
		for key, value in state_data['transitions'].items():
			setattr(self.__current_state, key, lambda custom_data={} : self.__set_state(value, custom_data={}))

		self.children = [self.__current_state]

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

class ServerCore(RootNodeWithHandlers):
	def __init__(self, config):
		Config(config)
		super().__init__()
		self.server = Server(self.add_command)
		self.players = []

	def run(self):
		self.update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.update_thread.start()
		self.server.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def destroy_game(self, game_name):
		game = next(g for g in self.children if g.name == game_name)
		assert game and len(game.players) == 0
		log(f'Removing game {game_name} from game list', LOG_LEVEL_INTERNAL_LOW)
		self.children.remove(game)

	def destroy_game_handler(self, command):
		game_name = command.data['game_name']
		self.destroy_game(game_name)

	def create_player_handler(self, command):
		self.players.append(FullPlayer(command.data['player_name'], command.connection))
		command.update_and_send(status='success')

	def create_game_handler(self, command):
		self.children.append(ServerGame(command.data['game_name'], self.destroy_game))
		command.update_and_send(status='success')

	def get_games_handler(self, command):
		parsed_games = [(game.name, len(game.players)) for game in self.children]
		command.update_and_send(status='success', data={ 'games': parsed_games })

	def join_game_handler(self, command):
		game_name = command.data['game_name']
		player = next(p for p in self.players if p.connection == command.connection)
		game = next(g for g in self.children if g.name == game_name)
		log(f'Adding {player.name} to game {game_name} in game list', LOG_LEVEL_INTERNAL_LOW)
		game.add_player(player)
		command.update_and_send(status='success')

	def logout_handler(self, command):
		player = next(p for p in self.players if p.connection == command.connection)
		self.players.remove(player)
		command.update_and_send(status='success')

	def add_command(self, command):
		player = next(iter(p for p in self.players if p.connection == command.connection), False)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', LOG_LEVEL_INTERNAL_LOW)
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.command_queue.append(command)
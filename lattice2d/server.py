from lattice2d.nodes import Node, RootNode
import threading
from lattice2d.config import Config
from lattice2d.network import Server
from lattice2d.utilities import log
from lattice2d.states import StateMachine, State


class ServerCore(RootNode):
	def __init__(self, test=False):
		super().__init__()
		if not test:
			self.__network = Server(self.add_command)
		self.__players = []

	def run(self, test=False):
		self.__update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.__update_thread.start()
		if not test:
			self.__network.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def get_players(self):
		return self.__players

	def destroy_game(self, game_name):
		assert game_name in self._children.keys()
		assert len(self._children[game_name].get_players()) == 0
		log(f'Removing game {game_name} from game list', 'lattice2d_core')
		del self._children[game_name]

	def destroy_game_handler(self, command):
		game_name = command.data['game_name']
		self.destroy_game(game_name)
		command.update_and_send(status='success')

	def create_player_handler(self, command):
		self.__players.append(Config()['player_class'](command.data['player_name'], command.connection))
		command.update_and_send(status='success')

	def create_game_handler(self, command):
		self._children[command.data['game_name']] = ServerGame(command.data['game_name'], self.destroy_game)
		command.update_and_send(status='success')

	def get_games_handler(self, command):
		parsed_games = [(game.name, len(game.get_players())) for game in self._children.values()]
		command.update_and_send(status='success', data={'games': parsed_games})

	def join_game_handler(self, command):
		game_name = command.data['game_name']
		player = next(p for p in self.__players if p.connection == command.connection)
		game = next(g for g in self._children.values() if g.name == game_name)
		log(f'Adding {player.name} to game {game_name} in game list', 'lattice2d_core')
		game.add_player(player)
		command.update_and_send(status='success')

	def logout_handler(self, command):
		player = next(p for p in self.__players if p.connection == command.connection)
		self.__players.remove(player)
		command.update_and_send(status='success')

	def add_command(self, command):
		player = next(iter(p for p in self.__players if p.connection == command.connection), False)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', 'lattice2d_core')
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', 'lattice2d_core')
			self._command_queue.append(command)


class ServerGame(StateMachine):
	def __init__(self, name, destroy_game):
		super().__init__(Config()['server_states'])
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.__players = []

	def get_players(self):
		return self.__players

	def get_current_player(self):
		return self.__players[self.current_player_index]

	def is_current_player(self, player):
		return player.connection == self.__players[self.current_player_index].connection

	def add_player(self, player, host=False):
		assert player not in self.__players
		log(f'Adding {player.name} to game {self.name}', 'lattice2d_core')
		player.game = self
		player.host = host
		self.__players.append(player)
		self.broadcast_players(player)

	def remove_player(self, player):
		assert player in self.__players
		log(f'Removing {player.name} from game {self.name}', 'lattice2d_core')
		player.game = None
		self.__players.remove(player)
		if self.__players:
			self.broadcast_players()
		else:
			self.destroy_game(self.name)

	def broadcast_players(self, exception=None):
		parsed_players = [(player.name, player.host) for player in self.__players]
		for player in self.__players:
			if player != exception:
				Command.create_and_send(
					'broadcast_players_in_game',
					{'players': parsed_players},
					'success',
					player.connection
				)


class ServerState(State):
	def broadcast_players_in_game_handler(self, command):
		if 'exception' in command.data.keys():
			self.state_machine.broadcast_players(command.data['exception'])
		else:
			self.state_machine.broadcast_players()

	def leave_game_handler(self, command):
		self.state_machine.remove_player(
			next(p for p in self.state_machine.get_players() if p.connection == command.connection))

	def get_current_player_handler(self, command):
		player = next(iter(p for p in self.state_machine.get_players() if p.connection == command.connection), False)
		if self.state_machine.is_current_player(player):
			player_name = 'self'
		else:
			player_name = self.state_machine.get_current_player().name
		command.update_and_send(status='success', data={'player_name': player_name})


class Player(Node):
	def __init__(self, name, connection=None, game=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.game = game

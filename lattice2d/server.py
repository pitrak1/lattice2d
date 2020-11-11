from lattice2d.nodes import Node, RootNode
import threading
from lattice2d.config import Config
from lattice2d.network import Server
from lattice2d.utilities import log
from lattice2d.states import StateMachine, State
from lattice2d.command import Command


class ServerCore(RootNode):
	def __init__(self, test=False):
		super().__init__()
		if not test:
			self.__network = Server(self.add_command)
		self.players = []

	def run(self, test=False):
		self.__update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.__update_thread.start()
		if not test:
			self.__network.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def destroy_game(self, game_name):
		assert game_name in self._children.keys()
		assert len(self._children[game_name].players) == 0
		log(f'Removing game {game_name} from game list', 'lattice2d_core')
		del self._children[game_name]

	def destroy_game_handler(self, command):
		game_name = command.data['game_name']
		self.destroy_game(game_name)
		command.update_and_send(status='success')

	def create_player_handler(self, command):
		self.players.append(Config()['player_class'](command.data['player_name'], command.connection))
		command.update_and_send(status='success')

	def create_game_handler(self, command):
		self._children[command.data['game_name']] = ServerGame(command.data['game_name'], self.destroy_game)
		command.update_and_send(status='success')

	def get_games_handler(self, command):
		parsed_games = [(game.name, len(game.players)) for game in self._children.values()]
		command.update_and_send(status='success', data={'games': parsed_games})

	def join_game_handler(self, command):
		game_name = command.data['game_name']
		player = next(p for p in self.players if p.connection == command.connection)
		game = next(g for g in self._children.values() if g.name == game_name)
		log(f'Adding {player.name} to game {game_name} in game list', 'lattice2d_core')
		game.add_player(player)
		command.update_and_send(status='success')

	def logout_handler(self, command):
		player = next(p for p in self.players if p.connection == command.connection)
		self.players.remove(player)
		command.update_and_send(status='success')

	def add_command(self, command):
		player = next(iter(p for p in self.players if p.connection == command.connection), False)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', 'lattice2d_core')
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', 'lattice2d_core')
			self.command_queue.append(command)


class ServerGame(StateMachine):
	def __init__(self, name, destroy_game):
		super().__init__(Config()['server_states'])
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.players = []

	def get_current_player(self):
		return self.players[self.current_player_index]

	def is_current_player(self, player):
		return player.connection == self.players[self.current_player_index].connection

	def add_player(self, player, host=False):
		assert player not in self.players
		log(f'Adding {player.name} to game {self.name}', 'lattice2d_core')
		player.game = self
		player.host = host
		self.players.append(player)
		self.broadcast_players(player)

	def remove_player(self, player):
		assert player in self.players
		log(f'Removing {player.name} from game {self.name}', 'lattice2d_core')
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
			next(p for p in self.state_machine.players if p.connection == command.connection))

	def get_current_player_handler(self, command):
		player = next(iter(p for p in self.state_machine.players if p.connection == command.connection), False)
		if self.state_machine.is_current_player(player):
			player_name = 'self'
		else:
			player_name = self.state_machine.get_current_player().name
		command.update_and_send(status='success', data={'player_name': player_name})

	def register_component(self, identifier, layer_name, component, redraw=True):
		pass


class Player(Node):
	def __init__(self, name, connection=None, game=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.game = game

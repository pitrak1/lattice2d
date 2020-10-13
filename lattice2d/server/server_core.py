import threading

from lattice2d.config import Config
from lattice2d.network import Server
from lattice2d.nodes import RootNode
from lattice2d.server.server_game import ServerGame
from lattice2d.utilities.log import log


class ServerCore(RootNode):
	def __init__(self, config, test=False):
		Config(config)
		super().__init__()
		self.test = test
		if not test:
			self.network = Server(self.add_command)
		self.players = []

	def run(self):
		if self.test:
			self.__on_update_loop()
		self.update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.update_thread.start()
		self.network.run()

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
			self._command_queue.append(command)

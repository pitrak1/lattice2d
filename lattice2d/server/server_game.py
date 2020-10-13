from lattice2d.command import Command
from lattice2d.config import Config
from lattice2d.nodes import RootNode
from lattice2d.utilities.log import log
from lattice2d.states import StateMachine


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

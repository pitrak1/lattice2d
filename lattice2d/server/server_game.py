from lattice2d.command import Command
from lattice2d.config import Config
from lattice2d.nodes import RootNode
from lattice2d.utilities.log import log, LOG_LEVEL_INTERNAL_LOW


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
			setattr(self.__current_state, key, lambda data={}: self.__set_state(value))

		self._children['state'] = self.__current_state

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
				Command.create_and_send(
					'broadcast_players_in_game',
					{'players': parsed_players},
					'success',
					player.connection
				)

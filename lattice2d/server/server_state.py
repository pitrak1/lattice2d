from lattice2d.nodes import Node


class ServerState(Node):
	def __init__(self, game, custom_data={}):
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
		command.update_and_send(status='success', data={'player_name': player_name})

from lattice2d.states import State


class ServerState(State):
	def broadcast_players_in_game_handler(self, command):
		if 'exception' in command.data.keys():
			self.state_machine.broadcast_players(command.data['exception'])
		else:
			self.state_machine.broadcast_players()

	def leave_game_handler(self, command):
		self.state_machine.remove_player(next(p for p in self.state_machine.players if p.connection == command.connection))

	def get_current_player_handler(self, command):
		player = next(iter(p for p in self.state_machine.players if p.connection == command.connection), False)
		if self.state_machine.is_current_player(player):
			player_name = 'self'
		else:
			player_name = self.state_machine.get_current_player().name
		command.update_and_send(status='success', data={'player_name': player_name})

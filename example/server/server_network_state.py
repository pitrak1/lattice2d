from lattice2d.server.server_state import ServerState


class ServerNetworkState(ServerState):
	def some_network_command_handler(self, command):
		command.update_and_send(status='success')

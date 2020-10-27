from lattice2d.server import ServerState


class ServerNetworkState(ServerState):
	def some_network_command_handler(self, command):
		command.update_and_send(status='success')

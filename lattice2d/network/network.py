from lattice2d.nodes.node import Node
from lattice2d.network.network_command import deserialize

class Network(Node):
	def __init__(self, add_command):
		super().__init__()
		self.add_command = add_command

	def receive(self, connection):
		while True:
			received = connection.recv(4096)
			if not received: break
			command_strings = received.decode()[:-1].split('|')
			for command in command_strings:
				log(f'Received {command}', LOG_LEVEL_INTERNAL_HIGH)
				result = deserialize(command)
				result.connection = connection
				self.add_command(result)
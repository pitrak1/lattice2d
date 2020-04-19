import socket
from utilities.serialize import deserialize
from nodes import NETWORK_COMMAND_TYPES

class Network():
	def __init__(self, add_command):
		self.add_command = add_command

	def receive(self, connection):
		if not self.testing:
			while True:
				received = connection.recv(4096)
				if not received: break
				command_strings = received.decode()[:-1].split('|')
				for command in command_strings:
					result = deserialize(command)
					result.connection = connection
					self.add_command(result)

class Server(Network):
	def __init__(self, add_command):
		super().__init__(add_command)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('0.0.0.0', 8080))
		self.socket.listen(5)

	def run(self):
		while True:
			connection, address = self.socket.accept()
			client_thread = threading.Thread(target=self.receive, args=(connection,), daemon=True)
			client_thread.start()

class Client(Network):
	def __init__(self, add_command):
		super().__init__(add_command)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect(('0.0.0.0', 8080))
		self.receive_thread = threading.Thread(target=self.receive, args(self.socket,), daemon=True)
		self.receive_thread.start()
		self.handlers = {}
		for entry in NETWORK_COMMAND_TYPES:
			self.handlers[entry] = lambda command : pass

	def on_command(self, command):
		return self.handlers[command.type](command)

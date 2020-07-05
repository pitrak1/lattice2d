import socket
import threading
from lattice2d.config import Config
from lattice2d.network.network import Network
from lattice2d.network.network_command import NetworkCommand

class Client(Network):
	def __init__(self, add_command):
		super().__init__(add_command)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((Config()['network']['ip_address'], Config()['network']['port']))
		self.receive_thread = threading.Thread(target=self.receive, args=(self.socket,), daemon=True)
		self.receive_thread.start()

	def default_handler(self, command):
		if isinstance(command, NetworkCommand):
			if command.status == 'pending':
				command.update_and_send(connection=self.socket)
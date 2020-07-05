import socket
import threading
from lattice2d.config import Config
from lattice2d.network.network import Network

class Server(Network):
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((Config()['network']['ip_address'], Config()['network']['port']))
		self.socket.listen(5)

		while True:
			connection, address = self.socket.accept()
			client_thread = threading.Thread(target=self.receive, args=(connection,), daemon=True)
			client_thread.start()
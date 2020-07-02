import socket
import json
import threading
from lattice2d.nodes import Node, RootNode, Command
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH
from lattice2d.config import Config

def serialize(command):
	if isinstance(command, NetworkCommand):
		converted = { 'type': command.type, 'data': command.data, 'status': command.status }
	else:
		converted = { 'type': command.type, 'data': command.data }

	return json.dumps(converted) + '|'

def deserialize(command):
	deserialized = json.loads(command)

	if 'status' in deserialized.keys():
		return NetworkCommand(deserialized['type'], deserialized['data'], deserialized['status'], None)
	else:
		return Command(deserialized['type'], deserialized['data'])

class NetworkCommand(Command):
	def __init__(self, type_, data={}, status=None, connection=None):
		super().__init__(type_, data)
		self.status = status
		self.connection = connection

	def update_and_send(self, status=None, data=None, connection=None):
		if status: self.status = status
		if data: self.data.update(data)
		if connection: self.connection = connection
		self.connection.send(serialize(self).encode())

	@classmethod
	def create_and_send(cls, type_, data, status, connection):
		command = cls(type_, data, status)
		connection.send(serialize(command).encode())
		return command

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

class Server(Network):
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((Config()['network']['ip_address'], Config()['network']['port']))
		self.socket.listen(5)

		while True:
			connection, address = self.socket.accept()
			client_thread = threading.Thread(target=self.receive, args=(connection,), daemon=True)
			client_thread.start()

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

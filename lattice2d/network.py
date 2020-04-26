import socket
import json
import threading
from lattice2d.nodes import Node, RootNode, Command
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_HIGH

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

class Player(Node):
	def __init__(self, name, connection, game=None):
		super().__init__()
		self.name = name
		self.connection = connection
		self.game = game

class Game(RootNode):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.players = []

class ServerCore(RootNode):
	def __init__(self):
		super().__init__()
		self.players = []
		self.server = Server(self.add_command)

	def run(self):
		self.update_thread = threading.Thread(target=self.__on_update_loop, daemon=True)
		self.update_thread.start()
		self.server.run()

	def __on_update_loop(self):
		while True:
			self.on_update()

	def add_command(self, command):
		player = self.find_player_by_connection(command.connection)
		if player and player.game:
			log(f'Adding command type {command.type} to game {player.game.name}', LOG_LEVEL_INTERNAL_LOW)
			player.game.add_command(command)
		else:
			log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.command_queue.append(command)

	def find_game_by_name(self, game_name):
		try:
			return next(game for game in self.children if game.name == game_name)
		except StopIteration:
			return False

	def find_player_by_name(self, player_name):
		try:
			return next(player for player in self.players if player.name == player_name)
		except StopIteration:
			return False

	def find_player_by_connection(self, connection):
		try:
			return next(player for player in self.players if player.connection == connection)
		except StopIteration:
			return False

class Client(Network):
	def __init__(self, add_command):
		super().__init__(add_command)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect(('0.0.0.0', 8080))
		self.receive_thread = threading.Thread(target=self.receive, args=(self.socket,), daemon=True)
		self.receive_thread.start()

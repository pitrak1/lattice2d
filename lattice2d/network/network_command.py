import json
from lattice2d.nodes.command import Command

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
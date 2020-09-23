import json


def serialize(command):
	converted = {'type': command.type, 'data': command.data, 'status': command.status}
	return json.dumps(converted) + '|'


def deserialize(command):
	deserialized = json.loads(command)

	if 'status' in deserialized.keys():
		return Command(deserialized['type'], deserialized['data'], deserialized['status'], None)
	else:
		return Command(deserialized['type'], deserialized['data'])


class Command:
	def __init__(self, type_, data={}, status=None, connection=None):
		self.type = type_
		self.data = data
		self.status = status
		self.connection = connection

	def update_and_send(self, status=None, data=None, connection=None):
		if status:
			self.status = status
		if data:
			self.data.update(data)
		if connection:
			self.connection = connection
		self.connection.send(serialize(self).encode())

	@classmethod
	def create_and_send(cls, type_, data, status, connection):
		command = cls(type_, data, status)
		connection.send(serialize(command).encode())
		return command

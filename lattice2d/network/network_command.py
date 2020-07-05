from lattice2d.nodes.command import Command

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
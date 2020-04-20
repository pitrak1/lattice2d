import json
from lattice2d.commands import Command, NetworkCommand

def serialize(command):
	if isinstance(command, NetworkCommand):
		converted = { 'type': command.type, 'data': command.data, 'status': command.status, 'connection': command.connection }
	else:
		converted = { 'type': command.type, 'data': command.data }

	return json.dumps(converted) + '|'

def deserialize(command):
	deserialized = json.loads(command)

	if 'status' in deserialized.keys():
		return NetworkCommand(deserialized['type'], deserialized['data'], deserialized['status'], deserialized['connection'])
	else:
		return Command(deserialized['type'], deserialized['data'])
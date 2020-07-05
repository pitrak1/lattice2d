import json
from lattice2d.network.network_command import NetworkCommand

def serialize(command):
	if isinstance(command, NetworkCommand):
		converted = { 'type': command.type, 'data': command.data, 'status': command.status }
	else:
		converted = { 'type': command.type, 'data': command.data }

	return json.dumps(converted) + '|'

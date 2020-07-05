import json
from lattice2d.network.network_command import NetworkCommand
from lattice2d.nodes.command import Command

def deserialize(command):
	deserialized = json.loads(command)

	if 'status' in deserialized.keys():
		return NetworkCommand(deserialized['type'], deserialized['data'], deserialized['status'], None)
	else:
		return Command(deserialized['type'], deserialized['data'])
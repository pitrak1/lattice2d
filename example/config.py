import os
import copy
from definitions import ROOT_DIR
from constants import CONSTANTS
from client.client_component_state import ClientComponentState
from client.client_network_state import ClientNetworkState
from server.server_network_state import ServerNetworkState
from lattice2d.grid.player import Player

CONFIG = copy.deepcopy(CONSTANTS)
CONFIG.update({
	'command_types': ['some_network_command'],
	'player_class': Player,
	'client_states': {
		'starting_state': ClientComponentState,
		'states': [
			{
				'state': ClientComponentState,
				'transitions': {
					'to_network_state': ClientNetworkState
				}
			},
			{
				'state': ClientNetworkState,
				'transitions': {}
			}
		]
	},
	'server_states': {
		'starting_state': ServerNetworkState,
		'states': [
			{
				'state': ServerNetworkState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(ROOT_DIR,'assets'),
		'tiles': [],
		'characters': {},
		'custom': [
			{
				'variable_name': 'background',
				'location': 'background.jpg',
				'type': 'single'
			}
		]
	}
})
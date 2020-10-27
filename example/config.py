import os
import copy
from definitions import ROOT_DIR
from constants import CONSTANTS
from client.client_component_state import ClientComponentState
from client.client_network_state import ClientNetworkState
from server.server_network_state import ServerNetworkState
from lattice2d.grid import Tile
from lattice2d.server import Player

CONFIG = copy.deepcopy(CONSTANTS)
CONFIG.update({
	'command_types': ['some_network_command'],
	'player_class': Player,
	'empty_tile_class': Tile,
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
		'path': os.path.join(ROOT_DIR, 'assets'),
		'resources': [
			{
				'key': 'background',
				'location': 'background.jpg',
				'type': 'single'
			},
			{
				'key': 'grey_button',
				'location': 'grey_button.png',
				'type': 'grid',
				'rows': 3,
				'columns': 3
			},
			{
				'key': 'grey_panel',
				'location': 'grey_panel.png',
				'type': 'grid',
				'rows': 3,
				'columns': 3
			}
		]
	}
})

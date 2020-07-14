import os
import copy
from definitions import ROOT_DIR
from constants import CONSTANTS
from client.client_component_state import ClientComponentState
from server.server_component_state import ServerComponentState

CONFIG = copy.deepcopy(CONSTANTS)
CONFIG.update({
	'command_types': [],
	'client_states': {
		'starting_state': ClientComponentState,
		'states': [
			{
				'state': ClientComponentState,
				'transitions': {}
			}
		]
	},
	'server_states': {
		'starting_state': ServerComponentState,
		'states': [
			{
				'state': ServerComponentState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(ROOT_DIR,'assets'),
		'tiles': [],
		'characters': {},
		'custom': {
			'background': {
				'location': 'background.jpg',
				'type': 'single'
			}
		}
	}
})

import os

import pytest

from lattice2d.config import Config
from lattice2d.definitions import ROOT_DIR
from lattice2d.grid import Player
from lattice2d.server.server_state import ServerState

TEST_CONFIG = {
	'window_dimensions': (100, 100),
	'log_level': 3,
	'network': {
		'ip_address': '0.0.0.0',
		'port': 8080
	},
	'group_count': 2,
	'grid': {
		'width': 2,
		'height': 2,
		'size': 100
	},
	'player_class': Player,
	'command_types': ['test_command', 'test_command_2'],
	'client_states': {},
	'server_states': {
		'starting_state': ServerState,
		'states': [
			{
				'state': ServerState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(ROOT_DIR, 'assets'),
		'tiles': [],
		'characters': [
			{
				'variable_name': 'test_character',
				'display_name': 'Test Character',
				'location': 'test.jpg',
				'type': 'single'
			}
		],
		'custom': [
			{
				'variable_name': 'test_custom',
				'location': 'test.jpg',
				'type': 'single'
			}
		]
	}
}


@pytest.fixture
def get_positional_args():
	def _get_positional_args(stub, call_number, arg_number=None):
		if arg_number is not None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]

	return _get_positional_args


@pytest.fixture
def get_keyword_args():
	def _get_keyword_args(stub, call_number, key=None):
		if key is not None:
			return stub.call_args_list[call_number][1][key]
		else:
			return stub.call_args_list[call_number][1]

	return _get_keyword_args


@pytest.fixture(autouse=True)
def set_config():
	Config(TEST_CONFIG)

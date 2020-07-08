import pytest
import os
from lattice2d.definitions import ROOT_DIR
from lattice2d.config import Config
from unit.client.client_state_test import FakeClientState

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
	'command_types': [],
	'client_states': {
		'starting_state': FakeClientState,
		'states': [
			{
				'state': FakeClientState,
				'transitions': {}
			}
		]
	},
	'server_states': {},
	'assets': {
		'path': os.path.join(ROOT_DIR, 'assets'),
		'tiles': [],
		'characters': {
			'test_character': {
				'display_name': 'Test Character',
				'location': 'test.jpg',
				'type': 'single'
			}
		},
		'custom': {
			'test_custom': {
				'location': 'test.jpg',
				'type': 'single'
			}
		}
	}
}

@pytest.fixture
def get_positional_args():
	def _get_positional_args(stub, call_number, arg_number=None):
		if arg_number != None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_positional_args

@pytest.fixture
def get_keyword_args():
	def _get_keyword_args(stub, call_number, key=None):
		if key != None:
			return stub.call_args_list[call_number][1][key]
		else:
			return stub.call_args_list[call_number][1]
	return _get_keyword_args

@pytest.fixture(autouse=True)
def set_config():
	config = Config(TEST_CONFIG)

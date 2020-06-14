import pytest
from lattice2d.config import Config
from lattice2d.full.full_client import FullClientState
from lattice2d.full.full_server import FullServerState

TEST_CONFIG = {
    'command_types': [
        'some_command_type',
        'some_other_command_type'
    ],
    'full_solution': {}
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
def set_command_types():
	config = Config(TEST_CONFIG)

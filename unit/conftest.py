import pytest
from lattice2d.config import Config, TEST_CONFIG

@pytest.fixture
def get_args():
	def _get_args(stub, call_number, arg_number=None):
		if arg_number != None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_args

@pytest.fixture(autouse=True)
def set_command_types():
	config = Config(TEST_CONFIG)

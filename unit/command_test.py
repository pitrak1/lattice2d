import types
import pytest

from lattice2d.command import Command, serialize, deserialize


@pytest.fixture
def create_connection():
	def _create_connection(mocker):
		connection = types.SimpleNamespace()
		connection.send = mocker.stub()
		return connection

	return _create_connection


class TestSerializeDeserialize:
	def test_serializes_and_deserializes_commands(self):
		command = Command('some_command_type', {
			'key1': True,
			'key2': None,
			'key3': 1.5,
			'key4': 'value',
			'key5': [1, 2, 3],
			'key6': {'key1': 'value1'}
		}, 'status', None)
		result = deserialize(serialize(command)[:-1])
		assert result.type == command.type
		assert result.data == command.data
		assert result.status == command.status

	def test_deserializing_removes_connection_from_commands(self):
		command = Command('some_command_type', {
			'key1': True,
			'key2': None,
			'key3': 1.5,
			'key4': 'value',
			'key5': [1, 2, 3],
			'key6': {'key1': 'value1'}
		}, 'status', 'connection')
		result = deserialize(serialize(command)[:-1])
		assert result.connection is None

	def test_adds_pipe_on_serialization(self):
		command = Command('some_command_type', {
			'key1': True,
			'key2': None,
			'key3': 1.5,
			'key4': 'value',
			'key5': [1, 2, 3],
			'key6': {'key1': 'value1'}
		})
		result = serialize(command)
		assert result[-1:] == '|'

	def test_converts_tuples_to_arrays(self):
		command = Command('some_command_type', {'key1': (1, 2)})
		result = deserialize(serialize(command)[:-1])
		assert result.data['key1'] == [1, 2]


class TestCommand:
	def test_sends(self, mocker, create_connection):
		connection = create_connection(mocker)
		command = Command('some_command_type', {'key1': True}, 'status', connection)
		command.update_and_send()
		connection.send.assert_called_once_with(serialize(command).encode())

	def test_updates_and_sends(self, mocker, create_connection):
		connection = create_connection(mocker)
		other_connection = create_connection(mocker)
		command = Command('some_command_type', {'key1': True}, 'status', connection)
		command.update_and_send(status='other_status', data={'key2': False}, connection=other_connection)
		assert command.status == 'other_status'
		assert command.data == {'key1': True, 'key2': False}
		other_connection.send.assert_called_once_with(serialize(command).encode())
		connection.send.assert_not_called()

	def test_creates_and_sends(self, mocker, create_connection):
		connection = create_connection(mocker)
		command = Command.create_and_send('some_command_type', {'key1': True}, 'status', connection)
		assert command.type == 'some_command_type'
		assert command.status == 'status'
		assert command.data == {'key1': True}
		connection.send.assert_called_once_with(serialize(command).encode())

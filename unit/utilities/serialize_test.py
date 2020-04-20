from lattice2d.utilities.serialize import serialize, deserialize
from lattice2d.commands import Command, NetworkCommand

class TestSerialize():
	def test_serializes_and_deserializes_commands(self):
		command = Command('fake_command_type', { 
			'key1': True, 
			'key2': None, 
			'key3': 1.5, 
			'key4': 'value', 
			'key5': [1, 2, 3],
			'key6': { 'key1': 'value1' }		
		})
		result = deserialize(serialize(command)[:-1])
		assert result.type == command.type
		assert result.data == command.data

	def test_serializes_and_deserializes_commands(self):
		command = NetworkCommand('fake_command_type', { 
			'key1': True, 
			'key2': None, 
			'key3': 1.5, 
			'key4': 'value', 
			'key5': [1, 2, 3],
			'key6': { 'key1': 'value1' }		
		}, 'status', 'connection')
		result = deserialize(serialize(command)[:-1])
		assert result.type == command.type
		assert result.data == command.data
		assert result.status == command.status
		assert result.connection == command.connection

	def test_converts_tuples_to_arrays(self):
		command = Command('fake_command_type', { 'key1': (1, 2)	})
		result = deserialize(serialize(command)[:-1])
		assert result.data['key1'] == [1, 2]

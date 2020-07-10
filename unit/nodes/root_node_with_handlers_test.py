from lattice2d.nodes.root_node_with_handlers import RootNodeWithHandlers
from lattice2d.nodes.command import Command

class TestRootNodeWithHandlers():
	def test_calls_on_command_on_self(self, mocker):
		root_node = RootNodeWithHandlers()
		mocker.patch.object(root_node, 'on_command')
		command = Command('some_command_type', {})
		root_node.add_command(command)
		root_node.on_update()
		root_node.on_command.assert_called_once()
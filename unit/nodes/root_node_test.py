import types
from lattice2d.nodes.root_node import RootNode
from lattice2d.command import Command

class TestRootNode():
	def test_calls_on_command_on_self_for_every_command_on_update(self, mocker):
		root_node = RootNode()
		mocker.patch.object(root_node, 'on_command')

		command_1 = Command('some_command_type', {})
		root_node.add_command(command_1)

		command_2 = Command('some_other_command_type', {})
		root_node.add_command(command_2)

		root_node.on_update()
		assert root_node.on_command.call_count == 2

	def test_calls_on_update_for_children_on_update(self, mocker):
		root_node = RootNode()

		child_1 = types.SimpleNamespace()
		child_1.on_command = mocker.stub()
		child_1.on_update = mocker.stub()

		child_2 = types.SimpleNamespace()
		child_2.on_command = mocker.stub()
		child_2.on_update = mocker.stub()

		root_node.children = [child_1, child_2]

		root_node.on_update(1234)
		child_1.on_update.assert_called_once_with(1234)
		child_2.on_update.assert_called_once_with(1234)

	

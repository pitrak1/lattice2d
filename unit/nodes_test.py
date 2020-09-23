import types

from lattice2d.command import Command
from lattice2d.nodes import Node, RootNode


class MyNode(Node):
	def __init__(self):
		super().__init__()
		self.called = False

	# noinspection PyUnusedLocal
	def test_command_handler(self, command):
		self.called = True


class TestNode:
	class TestOnCommand:
		def test_calls_handler_based_on_type(self):
			node = MyNode()
			command = Command('test_command', {})
			node.on_command(command)
			assert node.called

	class TestDefaultHandler:
		def test_calls_on_command_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_command = mocker.stub()

			node = Node()
			node.children = [child]

			command = Command('test_command', {})
			node.on_command(command)
			child.on_command.assert_called_once_with(command)

		def test_returns_false_if_all_children_return_false_by_default(self):
			child_1 = types.SimpleNamespace()
			child_1.on_command = lambda comm: False

			child_2 = types.SimpleNamespace()
			child_2.on_command = lambda comm: False

			node = Node()
			node.children = [child_1, child_2]

			command = Command('test_command', {})
			assert not node.default_handler(command)

		def test_returns_true_if_any_children_return_true_by_default(self):
			child_1 = types.SimpleNamespace()
			child_1.on_command = lambda comm: False

			child_2 = types.SimpleNamespace()
			child_2.on_command = lambda comm: True

			node = Node()
			node.children = [child_1, child_2]

			command = Command('test_command', {})
			assert node.default_handler(command)

	class TestOnUpdate:
		def test_calls_on_update_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_update = mocker.stub()

			node = Node()
			node.children = [child]

			node.on_update(1234)
			child.on_update.assert_called_once_with(1234)

	class TestOnDraw:
		def test_calls_on_draw_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_draw = mocker.stub()

			node = Node()
			node.children = [child]

			node.on_draw()
			child.on_draw.assert_called_once()


class TestRootNode:
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

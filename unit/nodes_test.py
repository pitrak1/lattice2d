import types
import pytest
from nodes import Command, ChildList, Node, RootNode, RootNodeWithHandlers

class TestChildList():
	class TestOnCommand():
		def test_calls_on_command_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_command = mocker.stub()

			child_list = ChildList()
			child_list.append(child)

			command = Command('some_command_type', {})
			child_list.on_command(command)
			child.on_command.assert_called_once_with(command)

	class TestDefaultHandler():
		def test_calls_on_command_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_command = mocker.stub()

			child_list = ChildList()
			child_list.append(child)

			command = Command('some_command_type', {})
			child_list.default_handler(command)
			child.on_command.assert_called_once_with(command)

		def test_returns_false_if_all_children_return_false_by_default(self, mocker):
			child_1 = types.SimpleNamespace()
			child_1.on_command = lambda command : False

			child_2 = types.SimpleNamespace()
			child_2.on_command = lambda command : False

			child_list = ChildList()
			child_list.append(child_1)
			child_list.append(child_2)

			command = Command('some_command_type', {})
			assert not child_list.default_handler(command)

		def test_returns_true_if_any_children_return_true_by_default(self, mocker):
			child_1 = types.SimpleNamespace()
			child_1.on_command = lambda command : False

			child_2 = types.SimpleNamespace()
			child_2.on_command = lambda command : True

			child_list = ChildList()
			child_list.append(child_1)
			child_list.append(child_2)

			command = Command('some_command_type', {})
			assert child_list.default_handler(command)

	class TestOnUpdate():
		def test_calls_on_update_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_update = mocker.stub()

			child_list = ChildList()
			child_list.append(child)

			child_list.on_update(1234)
			child.on_update.assert_called_once_with(1234)

	class TestOnDraw():
		def test_calls_on_draw_for_all_children(self, mocker):
			child = types.SimpleNamespace()
			child.on_draw = mocker.stub()

			child_list = ChildList()
			child_list.append(child)

			child_list.on_draw()
			child.on_draw.assert_called_once()

class TestRootNode():
	def test_calls_on_command_for_every_command_on_update(self, mocker):
		root_node = RootNode()
		mocker.patch.object(root_node.children, 'on_command')

		command_1 = Command('some_command_type', {})
		root_node.add_command(command_1)

		command_2 = Command('some_other_command_type', {})
		root_node.add_command(command_2)

		root_node.on_update()
		assert root_node.children.on_command.call_count == 2

	def test_calls_on_update_for_children_on_update(self, mocker):
		root_node = RootNode()
		mocker.patch.object(root_node.children, 'on_update')
		root_node.on_update(1234)
		root_node.children.on_update.assert_called_once_with(1234)

class TestRootNodeWithHandlers():
	def test_calls_on_command_on_self(self, mocker):
		root_node = RootNodeWithHandlers()
		mocker.patch.object(root_node, 'on_command')
		command = Command('some_command_type', {})
		root_node.add_command(command)
		root_node.on_update()
		root_node.on_command.assert_called_once()

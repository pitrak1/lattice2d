import types
import pytest

from lattice2d.command import Command
from lattice2d.nodes import Node, RootNode


@pytest.fixture
def create_mock_child():
	def _create_mock_child(mocker):
		child = types.SimpleNamespace()
		child.on_command = mocker.stub()
		child.on_update = mocker.stub()
		child.on_draw = mocker.stub()
		return child

	return _create_mock_child


@pytest.fixture
def create_node_with_mock_children(create_mock_child):
	def _create_node_with_mock_children(mocker, number_of_children):
		node = MyNode()
		children = []

		for i in range(0, number_of_children):
			child = create_mock_child(mocker)
			node.add_child(f'child{i}', child)
			children.append(child)

		return node, children

	return _create_node_with_mock_children


@pytest.fixture
def create_root_node_with_mock_children(create_mock_child):
	def _create_node_with_mock_children(mocker, number_of_children):
		node = MyRootNode()
		children = []

		for i in range(0, number_of_children):
			child = create_mock_child(mocker)
			node.add_child(f'child{i}', child)
			children.append(child)

		return node, children

	return _create_node_with_mock_children


class MyNode(Node):
	def __init__(self):
		super().__init__()
		self.called = False

	# noinspection PyUnusedLocal
	def test_command_handler(self, command):
		self.called = True

	def add_child(self, key, child):
		self._children[key] = child

	def get_child(self, key):
		return self._children[key]


class MyRootNode(RootNode):
	def add_child(self, key, child):
		self._children[key] = child

	def add_command_by_name(self, name):
		self.add_command(Command(name, {}))


class TestNode:
	class TestOnCommand:
		def test_calls_handler_based_on_type(self):
			node = MyNode()
			command = Command('test_command', {})
			node.on_command(command)
			assert node.called

	class TestDefaultHandler:
		def test_calls_on_command_for_all_children(self, mocker, create_node_with_mock_children):
			node, children = create_node_with_mock_children(mocker, 1)
			command = Command('test_command_2', {})
			node.on_command(command)
			children[0].on_command.assert_called_once_with(command)

		def test_returns_false_if_all_children_return_false_by_default(self, mocker, create_node_with_mock_children):
			node, children = create_node_with_mock_children(mocker, 2)
			for child in children:
				child.on_command = lambda comm: False
			command = Command('test_command', {})
			assert not node.default_handler(command)

		def test_returns_true_if_any_children_return_true_by_default(self, mocker, create_node_with_mock_children):
			node, children = create_node_with_mock_children(mocker, 2)
			children[0].on_command = lambda comm: False
			children[1].on_command = lambda comm: True
			command = Command('test_command', {})
			assert node.default_handler(command)

	class TestOnUpdate:
		def test_calls_on_update_for_all_children(self, mocker, create_node_with_mock_children):
			node, children = create_node_with_mock_children(mocker, 2)
			node.on_update(1234)
			for child in children:
				child.on_update.assert_called_once_with(1234)

	class TestOnDraw:
		def test_calls_on_draw_for_all_children(self, mocker, create_node_with_mock_children):
			node, children = create_node_with_mock_children(mocker, 2)
			node.on_draw()
			for child in children:
				child.on_draw.assert_called_once()


class TestRootNode:
	def test_calls_on_command_on_self_for_every_command_on_update(self, mocker):
		root_node = MyRootNode()
		mocker.patch.object(root_node, 'on_command')
		root_node.add_command_by_name('some_command_type')
		root_node.add_command_by_name('some_other_command_type')
		root_node.on_update()
		assert root_node.on_command.call_count == 2

	def test_calls_on_update_for_children_on_update(self, mocker, create_root_node_with_mock_children):
		root_node, children = create_root_node_with_mock_children(mocker, 2)
		root_node.on_update(1234)
		children[0].on_update.assert_called_once_with(1234)
		children[1].on_update.assert_called_once_with(1234)

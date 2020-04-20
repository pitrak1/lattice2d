from lattice2d.nodes import Node, RootNode, WindowRootNode
from lattice2d.commands import Command, WINDOW_COMMAND_TYPES

class TestNode():
	def test_passes_to_children_by_default(self, mocker):
		parent_node = Node()

		child_node = Node()
		mocker.patch.object(child_node, 'on_command')
		parent_node.children.append(child_node)

		command = Command(WINDOW_COMMAND_TYPES[0], {})
		parent_node.on_command(command)
		child_node.on_command.assert_called_once_with(command)

	def test_returns_false_if_any_children_return_false_by_default(self, mocker):
		parent_node = Node()

		child_node_1 = Node()
		mocker.patch.object(child_node_1, 'on_command', return_value=True)
		parent_node.children.append(child_node_1)

		child_node_2 = Node()
		mocker.patch.object(child_node_2, 'on_command', return_value=False)
		parent_node.children.append(child_node_2)

		command = Command(WINDOW_COMMAND_TYPES[0], {})
		assert not parent_node.on_command(command)

	def test_returns_true_if_all_children_return_true_by_default(self, mocker):
		parent_node = Node()

		child_node_1 = Node()
		mocker.patch.object(child_node_1, 'on_command', return_value=True)
		parent_node.children.append(child_node_1)

		child_node_2 = Node()
		mocker.patch.object(child_node_2, 'on_command', return_value=True)
		parent_node.children.append(child_node_2)

		command = Command(WINDOW_COMMAND_TYPES[0], {})
		assert parent_node.on_command(command)

	def test_calls_on_update_on_children(self, mocker):
		parent_node = Node()

		child_node = Node()
		mocker.patch.object(child_node, 'on_update')
		parent_node.children.append(child_node)

		parent_node.on_update('dt')
		child_node.on_update.assert_called_once_with('dt')

	def test_calls_on_draw_on_children(self, mocker):
		parent_node = Node()

		child_node = Node()
		mocker.patch.object(child_node, 'on_draw')
		parent_node.children.append(child_node)

		parent_node.on_draw()
		child_node.on_draw.assert_called_once()

class TestRootNode():
	def test_calls_on_command_for_every_child_and_every_command(self, mocker):
		root_node = RootNode()

		child_node_1 = Node()
		mocker.patch.object(child_node_1, 'on_command')
		root_node.children.append(child_node_1)

		child_node_2 = Node()
		mocker.patch.object(child_node_2, 'on_command')
		root_node.children.append(child_node_2)

		command_1 = Command(WINDOW_COMMAND_TYPES[0], {})
		root_node.add_command(command_1)

		command_2 = Command(WINDOW_COMMAND_TYPES[1], {})
		root_node.add_command(command_2)

		root_node.on_update()
		assert child_node_1.on_command.call_count == 2
		assert child_node_2.on_command.call_count == 2

	def test_calls_on_updatefor_every_child(self, mocker):
		root_node = RootNode()

		child_node_1 = Node()
		mocker.patch.object(child_node_1, 'on_update')
		root_node.children.append(child_node_1)

		child_node_2 = Node()
		mocker.patch.object(child_node_2, 'on_update')
		root_node.children.append(child_node_2)

		command_1 = Command(WINDOW_COMMAND_TYPES[0], {})
		root_node.add_command(command_1)

		command_2 = Command(WINDOW_COMMAND_TYPES[1], {})
		root_node.add_command(command_2)

		root_node.on_update()
		child_node_1.on_update.assert_called_once()
		child_node_2.on_update.assert_called_once()

class TestWindowRootNode():
	def test_adds_command_on_key_press(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_key_press('symbol', 'modifiers')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'key_press'

	def test_adds_command_on_text(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_text('text')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'text'

	def test_adds_command_on_text_motion(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_text_motion('motion')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'text_motion'

	def test_adds_command_on_text_motion_select(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_text_motion_select('motion')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'text_motion_select'

	def test_adds_command_on_mouse_press(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_mouse_press('x', 'y', 'button', 'modifiers')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'mouse_press'

	def test_adds_command_on_mouse_drag(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_mouse_drag('x', 'y', 'dx', 'dy', 'button', 'modifiers')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'mouse_drag'

	def test_adds_command_on_mouse_scroll(self, mocker, get_args):
		window_root_node = WindowRootNode()
		mocker.patch.object(window_root_node, 'add_command')
		window_root_node.on_mouse_scroll('x', 'y', 'dx', 'dy')
		assert get_args(window_root_node.add_command, call_number=0, arg_number=0).type == 'mouse_scroll'

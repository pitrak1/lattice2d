import pyglet

from lattice2d.config import Config
from lattice2d.definitions import ROOT_DIR
from lattice2d.command import Command
from lattice2d.network import Client
from lattice2d.nodes import RootNode, Node
from lattice2d.states import StateMachine, State

class InnerAssets:
	_shared_state = {}

	def __init__(self):
		self.__dict__ = self._shared_state


class Assets(InnerAssets):
	def __init__(self):
		super().__init__()

		if not hasattr(self, 'custom'):
			pyglet.resource.path = [Config()['assets']['path']]
			pyglet.resource.reindex()

			self.custom = {}
			for entry in Config()['assets']['resources']:
				self.__load_asset(entry)

	def __getitem__(self, key):
		return self.custom[key]

	def __load_asset(self, entry):
		if entry['type'] == 'single':
			image = pyglet.resource.image(entry['location'])
			self.__center_asset(image)
			self.custom[entry['key']] = image
			return image
		elif entry['type'] == 'gif':
			gif = pyglet.resource.animation(entry['location'])
			self.__center_animation(gif)
			self.custom[entry['key']] = gif
		else:
			image = pyglet.resource.image(entry['location'])
			grid = list(pyglet.image.ImageGrid(image, entry['rows'], entry['columns']))
			[self.__center_asset(i) for i in grid]
			if 'key' in entry.keys():
				self.custom[entry['key']] = grid
			if 'resources' in entry.keys():
				for single_asset in entry['resources']:
					self.custom[single_asset['key']] = grid[single_asset['index']]

	def __center_animation(self, asset):
		asset.anchor_x = asset.get_max_width() / 2
		asset.anchor_y = asset.get_max_height() / 2

	def __center_asset(self, asset):
		asset.anchor_x = asset.width / 2
		asset.anchor_y = asset.height / 2


class ClientState(State):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.add_command = state_machine.add_command
		self.reset()

	def reset(self):
		self._children = {}
		self.__layers = {}
		self.__reset_rendering()

	def register_component(self, identifier, layer, component):
		assert layer in Config()['rendering']['layers']
		assert identifier not in self._children.keys()

		self.__create_groups_for_layer(layer)

		self._children[identifier] = component
		self.__layers[identifier] = layer
		component.register(self.__batch, self.__get_groups_for_layer(layer))
		self.__redraw()

	def get_component(self, identifier):
		assert identifier in self._children.keys()
		return self._children[identifier]

	def remove_component(self, identifier):
		assert identifier in self._children.keys()

		del self._children[identifier]
		self.__redraw()

	def conditionally_remove_component(self, identifier):
		if identifier in self._children.keys():
			del self._children[identifier]
			self.__redraw()

	def on_draw(self):
		self.__batch.draw()

	def default_handler(self, command):
		return any(
			iter(component.on_command(command) for component in self._children.values()))

	def __create_groups_for_layer(self, layer):
		groups_per_layer = Config()['rendering']['groups_per_layer']
		layer_index = Config()['rendering']['layers'].index(layer)
		if not self.__groups[layer_index * groups_per_layer]:
			for i in range(layer_index * groups_per_layer, (layer_index + 1) * groups_per_layer):
				self.__groups[i] = pyglet.graphics.OrderedGroup(i)

	def __get_groups_for_layer(self, layer):
		groups_per_layer = Config()['rendering']['groups_per_layer']
		layer_index = Config()['rendering']['layers'].index(layer)
		return self.__groups[layer_index * groups_per_layer:(layer_index + 1) * groups_per_layer]

	def __reset_rendering(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None] * Config()['rendering']['groups_per_layer'] * len(Config()['rendering']['layers'])

	def __redraw(self):
		self.__reset_rendering()

		for identifier, component in self._children.items():
			layer = self.__layers[identifier]
			self.__create_groups_for_layer(layer)
			component.register(self.__batch, self.__get_groups_for_layer(layer))


class ClientCore(StateMachine):
	def __init__(self):
		super().__init__(Config()['client_states'])
		self.__initialize_window()
		self.__initialize_network()

	def __initialize_window(self):
		self.__window = pyglet.window.Window(
			Config()['window_dimensions'][0],
			Config()['window_dimensions'][1]
		)
		self.__window.push_handlers(self)

	def __initialize_network(self):
		if 'network' in Config().data.keys():
			self._children['network'] = Client(self.add_command)

	def on_draw(self):
		self.__window.clear()
		[child.on_draw() for child in self._children.values()]

	def run(self):
		pyglet.clock.schedule_interval(self.on_update, 1 / 120.0)
		pyglet.app.run()

	def on_activate(self):
		self.add_command(Command('activate'))

	def on_close(self):
		self.add_command(Command('close'))

	def on_context_lost(self):
		self.add_command(Command('context_lost'))

	def on_context_state_lost(self):
		self.add_command(Command('context_state_lost'))

	def on_deactivate(self):
		self.add_command(Command('deactivate'))

	def on_expose(self):
		self.add_command(Command('expose'))

	def on_hide(self):
		self.add_command(Command('hide'))

	def on_key_press(self, symbol, modifiers):
		self.add_command(Command('key_press', {'symbol': symbol, 'modifiers': modifiers}))

	def on_key_release(self, symbol, modifiers):
		self.add_command(Command('key_release', {'symbol': symbol, 'modifiers': modifiers}))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(
			Command('mouse_drag', {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers}))

	def on_mouse_enter(self, x, y):
		self.add_command(Command('mouse_enter', {'x': x, 'y': y}))

	def on_mouse_leave(self, x, y):
		self.add_command(Command('mouse_leave', {'x': x, 'y': y}))

	def on_mouse_motion(self, x, y, dx, dy):
		self.add_command(Command('mouse_motion', {'x': x, 'y': y, 'dx': dx, 'dy': dy}))

	def on_mouse_press(self, x, y, button, modifiers):
		self.add_command(Command('mouse_press', {'x': x, 'y': y, 'button': button, 'modifiers': modifiers}))

	def on_mouse_release(self, x, y, button, modifiers):
		self.add_command(Command('mouse_release', {'x': x, 'y': y, 'button': button, 'modifiers': modifiers}))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.add_command(Command('mouse_scroll', {'x': x, 'y': y, 'dx': dx, 'dy': dy}))

	def on_move(self, x, y):
		self.add_command(Command('move', {'x': x, 'y': y}))

	def on_resize(self, width, height):
		self.add_command(Command('resize', {'width': width, 'height': height}))

	def on_show(self):
		self.add_command(Command('show'))

	def on_text(self, text):
		self.add_command(Command('text', {'text': text}))

	def on_text_motion(self, motion):
		self.add_command(Command('text_motion', {'motion': motion}))

	def on_text_motion_select(self, motion):
		self.add_command(Command('text_motion_select', {'motion': motion}))
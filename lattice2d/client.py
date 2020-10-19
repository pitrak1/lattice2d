import os

import pyglet

from lattice2d.config import Config
from lattice2d.definitions import ROOT_DIR
from lattice2d.command import Command
from lattice2d.network import Client
from lattice2d.nodes import RootNode, Node
from lattice2d.states import StateMachine, State

COMMON = [
	{
		'variable_name': 'test_jpg',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'test_png',
		'location': 'test.png',
		'type': 'single'
	},
	{
		'variable_name': 'test_gif',
		'location': 'test.gif',
		'type': 'gif'
	},
	{
		'variable_name': 'test_single',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'test_grid',
		'location': 'test.jpg',
		'type': 'grid',
		'rows': 9,
		'columns': 8,
		'assets': [
			{
				'variable_name': 'test_grid_entry',
				'index': 0
			}
		]
	},
	{
		'variable_name': 'test_common',
		'location': 'test.jpg',
		'type': 'single'
	}
]

UI = [
	{
		'variable_name': 'test_ui',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'grey_panel',
		'location': 'grey_panel.png',
		'type': 'grid',
		'rows': 3,
		'columns': 3
	},
	{
		'variable_name': 'grey_button',
		'location': 'grey_button.png',
		'type': 'grid',
		'rows': 3,
		'columns': 3
	}
]


class InnerAssets:
	_shared_state = {}

	def __init__(self):
		self.__dict__ = self._shared_state


class Assets(InnerAssets):
	def __init__(self):
		super().__init__()

		if not hasattr(self, 'common'):
			self.__load_local_assets()
			self.__load_config_assets()

	def __load_local_assets(self):
		pyglet.resource.path = [os.path.join(ROOT_DIR, 'assets')]
		pyglet.resource.reindex()

		self.common = {}
		for entry in COMMON:
			self.__load_asset(entry, self.common)

		self.ui = {}
		for entry in UI:
			self.__load_asset(entry, self.ui)

	def __load_config_assets(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.characters = {}
		for entry in Config()['assets']['characters']:
			self.__load_asset(entry, self.characters)

		self.tiles = {}
		for entry in Config()['assets']['tiles']:
			self.__load_asset(entry, self.tiles)

		self.custom = {}
		for entry in Config()['assets']['custom']:
			self.__load_asset(entry, self.custom)

	def __load_asset(self, entry, collection):
		if entry['type'] == 'single':
			image = pyglet.resource.image(entry['location'])
			self.__center_asset(image)
			collection[entry['variable_name']] = image
			return image
		elif entry['type'] == 'gif':
			gif = pyglet.resource.animation(entry['location'])
			self.__center_animation(gif)
			collection[entry['variable_name']] = gif
		else:
			image = pyglet.resource.image(entry['location'])
			grid = list(pyglet.image.ImageGrid(image, entry['rows'], entry['columns']))
			[self.__center_asset(i) for i in grid]
			if 'variable_name' in entry.keys():
				collection[entry['variable_name']] = grid
			if 'assets' in entry.keys():
				for single_asset in entry['assets']:
					collection[single_asset['variable_name']] = grid[single_asset['index']]

	def __center_animation(self, asset):
		asset.anchor_x = asset.get_max_width() / 2
		asset.anchor_y = asset.get_max_height() / 2

	def __center_asset(self, asset):
		asset.anchor_x = asset.width / 2
		asset.anchor_y = asset.height / 2


DRAW_LAYER_BACKGROUND_0 = 0
DRAW_LAYER_BASE_1 = 1
DRAW_LAYER_ENVIRONMENT_2 = 2
DRAW_LAYER_ACTORS_3 = 3
DRAW_LAYER_EFFECTS_4 = 4
DRAW_LAYER_UI_5 = 5
DRAW_LAYER_NOTIFICATIONS_6 = 6

TOTAL_LAYERS = 7


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
		assert 0 <= layer <= 6
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
		if not self.__groups[layer * Config()['group_count']]:
			for i in range(layer * Config()['group_count'], (layer + 1) * Config()['group_count']):
				self.__groups[i] = pyglet.graphics.OrderedGroup(i)

	def __get_groups_for_layer(self, layer):
		return self.__groups[layer * Config()['group_count']:(layer + 1) * Config()['group_count']]

	def __reset_rendering(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None] * Config()['group_count'] * TOTAL_LAYERS

	def __redraw(self):
		self.__reset_rendering()

		for identifier, component in self._children.items():
			layer = self.__layers[identifier]
			self.__create_groups_for_layer(layer)
			component.register(self.__batch, self.__get_groups_for_layer(layer))

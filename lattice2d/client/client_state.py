import pyglet

from lattice2d.config import Config
from lattice2d.nodes import Node

DRAW_LAYER_BACKGROUND_0 = 0
DRAW_LAYER_BASE_1 = 1
DRAW_LAYER_ENVIRONMENT_2 = 2
DRAW_LAYER_ACTORS_3 = 3
DRAW_LAYER_EFFECTS_4 = 4
DRAW_LAYER_UI_5 = 5
DRAW_LAYER_NOTIFICATIONS_6 = 6

TOTAL_LAYERS = 7


class ClientState(Node):
	def __init__(self, add_command, custom_data={}):
		super().__init__()
		self.add_command = add_command
		self.custom_data = custom_data
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

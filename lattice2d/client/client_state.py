import pyglet
from lattice2d.nodes import Node
from lattice2d.client.renderer import Renderer
from lattice2d.config import Config

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
		self.__components = {}
		self.__reset_rendering()

	def register_component(self, identifier, layer, component):
		assert layer >= 0 and layer <= 6
		assert identifier not in self.__components.keys()

		self.__create_groups_for_layer(layer)

		self.__components[identifier] = (layer, component)
		component.register(self.__batch, self.__get_groups_for_layer(layer))
		self.__redraw()

	def get_component(self, identifier):
		assert identifier in self.__components.keys()
		return self.__components[identifier][1]

	def remove_component(self, identifier):
		assert layer >= 0 and layer <= 6
		assert identifier in self.__components.keys()

		del self.__components[identifier]
		self.__redraw()

	def on_draw(self):
		self.__batch.draw()

	def default_handler(self, command):
		return any(iter(layer_and_component[1].on_command(command) for layer_and_component in self.__components.values()))

	def __create_groups_for_layer(self, layer):
		if not self.__groups[layer * Config()['group_count']]:
			for i in range(layer * Config()['group_count'], (layer + 1) * Config()['group_count']):
				self.__groups[i] = pyglet.graphics.OrderedGroup(i)

	def __get_groups_for_layer(self, layer):
		return self.__groups[layer * Config()['group_count']:(layer + 1) * Config()['group_count']]

	def __reset_rendering(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None for i in range(Config()['group_count'] * TOTAL_LAYERS)]

	def __redraw(self):
		self.__reset_rendering()

		for identifier, layer_and_component in self.__components.items():
			self.__create_groups_for_layer(layer_and_component[0])
			layer_and_component[1].register(self.__batch, self.__get_groups_for_layer(layer_and_component[0]))

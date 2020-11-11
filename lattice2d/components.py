import pyglet

from lattice2d.client import Assets
from lattice2d.nodes import Node
from lattice2d.utilities import within_rect_bounds
from lattice2d.config import Config
from lattice2d.utilities import log

class Layer():
	def __init__(self):
		self.batch = pyglet.graphics.Batch()
		self.__group = pyglet.graphics.Group()
		self.groups = []
		for i in range(Config()['rendering']['groups_per_layer']):
			self.groups.append(pyglet.graphics.OrderedGroup(i, self.__group))


class RootComponent(Component):
	def __init__(self):
		super().__init__()
		self.add_command = state_machine.add_command
		self.reset()

	def reset(self):
		self._children = {}
		self.__component_layers = {}
		self.__layers = {}

	def register_component(self, identifier, layer_name, component, redraw=True):
		assert layer_name in Config()['rendering']['layers']
		assert identifier not in self._children.keys()

		self.__create_layer(layer_name)

		self._children[identifier] = component
		self.__component_layers[identifier] = layer_name

		component.register(self.__layers[layer_name])
		if redraw:
			self.__redraw()

	def get_component(self, identifier):
		assert identifier in self._children.keys()
		return self._children[identifier]

	def remove_component(self, identifier, redraw=True):
		assert identifier in self._children.keys()

		del self._children[identifier]
		if redraw:
			self.__redraw()

	def conditionally_remove_component(self, identifier, redraw=True):
		if identifier in self._children.keys():
			del self._children[identifier]
			if redraw:
				self.__redraw()

	def on_draw(self):
		for layer in self.__layers.values():
			layer.batch.draw()

	def default_handler(self, command):
		return any(
			[component.on_command(command) for component in self._children.values()])

	def __create_layer(self, layer_name):
		if layer_name not in self.__layers.keys():
			self.__layers[layer_name] = Layer()

	def __redraw(self):
		self.__layers = {}

		for identifier, component in self._children.items():
			layer_name = self.__component_layers[identifier]
			self.__create_layer(layer_name)
			component.register(self.__layers[layer_name])

class Component(Node):
	def register(self, layer):
		raise NotImplementedError


class Label(pyglet.text.Label, Component):
	def __init__(self, *args, **kwargs):
		pyglet.text.Label.__init__(self, *args, **kwargs)
		Component.__init__(self)

	def register(self, layer, group_index=0):
		self.batch = layer.batch
		if group_index:
			self.group = layer.groups[group_index]
		else:
			self.group = layer.groups[0]

class UnformattedText(pyglet.text.layout.TextLayout, Component):
	def __init__(self, *args, **kwargs):
		pyglet.text.layout.TextLayout.__init__(self, *args, **kwargs)
		Component.__init__(self)

	def set_style(self, attributes):
		self.document.set_style(0, 0, attributes)

	def set_position(self, position, anchor_x='left', anchor_y='center'):
		self.x = position[0]
		self.y = position[1]
		self.anchor_x = anchor_x
		self.anchor_y = anchor_y

	def set_text(self, text):
		self.document.text = text

	def get_text(self):
		return self.document.text

	def register(self, layer, group_index=0):
		self.batch = layer.batch
		if group_index:
			self.group = layer.groups[group_index]
		else:
			self.group = layer.groups[0]

class Background(Component):
	def __init__(self, asset_key):
		super().__init__()
		asset = Assets().custom[asset_key]
		self.sprite = pyglet.sprite.Sprite(asset)
		self.__scale_to_window_size()

	def __scale_to_window_size(self):
		self.sprite.scale_x = Config()['window_dimensions'][0] / self.sprite.width
		self.sprite.scale_y = Config()['window_dimensions'][1] / self.sprite.height
		self.sprite.update(x=Config()['window_dimensions'][0] / 2, y=Config()['window_dimensions'][1] / 2)

	def register(self, layer):
		self.sprite.batch = layer.batch
		self.sprite.group = layer.groups[0]


class Area(Component):
	def __init__(self, position, unit_dimensions, align='center', asset_key='grey_panel'):
		super().__init__()
		self.position = position
		self.unit_dimensions = unit_dimensions
		self.sprites = []

		self.asset = Assets()[asset_key]
		tile_size = self.asset[0].width

		if align == 'left':
			base_x_offset = 0
			base_y_offset = (unit_dimensions[1] - 1) / 2 * tile_size
		else:
			base_x_offset = (unit_dimensions[0] - 1) / 2 * tile_size
			base_y_offset = (unit_dimensions[1] - 1) / 2 * tile_size

		for j in range(unit_dimensions[1]):
			if j == 0:
				base_sprite_index = 0
			elif j == unit_dimensions[1] - 1:
				base_sprite_index = 6
			else:
				base_sprite_index = 3

			for i in range(unit_dimensions[0]):
				if i == 0:
					sprite_index = base_sprite_index + 0
				elif i == unit_dimensions[0] - 1:
					sprite_index = base_sprite_index + 2
				else:
					sprite_index = base_sprite_index + 1
				self.sprites.append(pyglet.sprite.Sprite(self.asset[sprite_index]))
				self.sprites[j * unit_dimensions[0] + i].update(
					x=position[0] - base_x_offset + tile_size * i,
					y=position[1] - base_y_offset + tile_size * j,
				)

	def register(self, layer):
		for sprite in self.sprites:
			sprite.batch = layer.batch
			sprite.group = layer.groups[0]

	def within_bounds(self, position):
		return within_rect_bounds(
			self.position,
			position,
			(self.unit_dimensions[0] * self.asset[0].width, self.unit_dimensions[1] * self.asset[0].height)
		)


class Button(Node):
	def __init__(self, position, unit_dimensions, text, on_click):
		super().__init__()
		self.text = text
		self.area = Area(position, unit_dimensions, asset_key='grey_button')
		self.on_click = on_click
		self.label = Label(
			text,
			x=position[0],
			y=position[1],
			anchor_x='center',
			anchor_y='center',
			align='center',
			font_size=15,
			color=(0, 0, 0, 255)
		)

	def register(self, layer):
		self.area.register(layer)
		self.label.batch = layer.batch
		self.label.group = layer.groups[1]

	def mouse_press_handler(self, command):
		if self.area.within_bounds((command.data['x'], command.data['y'])):
			self.on_click()


class TextBox(Area):
	def __init__(self, position, unit_width, label_text, max_length):
		super().__init__(position, (unit_width, 2), align='left')
		self.label_text = label_text
		self.document = pyglet.text.document.UnformattedDocument('')
		self.document.set_style(0, 100, { 'color': (0, 0, 0, 255), 'font_size': 14 })

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, unit_width * 50, 24)
		self.layout.anchor_x = 'left'
		self.layout.anchor_y = 'center'
		self.layout.x = position[0]
		self.layout.y = position[1]

		self.max_length = max_length
		self.input_label = pyglet.text.Label(label_text, x=position[0], y=position[1] + self.asset[0].width + 15,
		                                     anchor_x='left', anchor_y='center', align='left', font_size=15,
		                                     color=(0, 0, 0, 255))
		self.input_error = pyglet.text.Label('', x=position[0], y=position[1] - 45, anchor_x='left', anchor_y='center',
		                                     align='left', font_size=15, color=(255, 0, 0, 255))
		self.selected = False

	def register(self, layer):
		super().register(layer)
		self.layout.batch = layer.batch
		self.layout.group = layer.groups[1]
		self.caret = pyglet.text.caret.Caret(self.layout, color=(0, 0, 0), batch=layer.batch)
		self.input_label.batch = layer.batch
		self.input_label.group = layer.groups[1]
		self.input_error.batch = layer.batch
		self.input_error.group = layer.groups[1]


	def set_error_text(self, text):
		self.input_error.text = text

	def get_text(self):
		return self.document.text

	def text_handler(self, command):
		if self.selected:
			self.caret.on_text(command.data['text'])
			self.enforce_length()

	def text_motion_handler(self, command):
		if self.selected:
			self.caret.on_text_motion(command.data['motion'])
			self.enforce_length()

	def text_motion_select_handler(self, command):
		if self.selected:
			self.caret.on_text_motion_select(command.data['motion'])
			self.enforce_length()

	def mouse_scroll_handler(self, command):
		if self.selected:
			self.caret.on_mouse_scroll(command.data['x'], command.data['y'], command.data['scroll_x'], command.data['scroll_y'])

	def mouse_press_handler(self, command):
		self.caret.on_mouse_press(command.data['x'], command.data['y'], command.data['button'],
		                          command.data['modifiers'])

		if self.within_bounds((command.data['x'], command.data['y'])):
			self.caret.visible = True
			self.selected = True

		else:
			self.caret.visible = False
			self.selected = False


	def mouse_drag_handler(self, command):
		if self.selected:
			self.caret.on_mouse_drag(command.data['x'], command.data['y'], command.data['dx'], command.data['dy'],
			                         command.data['buttons'], command.data['modifiers'])
			self.enforce_length()

	def on_activate_handler(self, command):
		if self.selected:
			self.caret.on_activate()

	def on_deactivate_handler(self, command):
		if self.selected:
			self.caret.on_deactivate()

	def on_layout_update(self, command):
		if self.selected:
			self.caret.on_layout_update()

	def enforce_length(self):
		if len(self.document.text) > self.max_length:
			stored_caret_position = self.caret.position
			self.document.text = self.document.text[:self.max_length]
			self.caret.mark = self.caret.position = stored_caret_position

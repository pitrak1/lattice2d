import pyglet
from lattice2d.assets import Assets
from lattice2d.config import Config
from lattice2d.nodes import Node
from lattice2d.utilities.bounds import within_rect_bounds

class AreaComponent(Node):
	def __init__(self, position, unit_dimensions, batch, group, align='center'):
		super().__init__()
		self.position = position
		self.unit_dimensions = unit_dimensions
		self.sprites = []

		self.asset = Assets().ui['grey_panel']
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
				self.sprites.append(pyglet.sprite.Sprite(self.asset[sprite_index], batch=batch, group=group))
				self.sprites[j * unit_dimensions[0] + i].update(
					x=position[0] - base_x_offset + tile_size * i, 
					y=position[1] - base_y_offset + tile_size * j,
				)

	def within_bounds(self, position):
		return within_rect_bounds(
			self.position, 
			position, 
			(self.unit_dimensions[0] * self.asset[0].width, self.unit_dimensions[1] * self.asset[0].height)
		)

class BackgroundComponent(Node):
	def __init__(self, asset_key, batch, group):
		super().__init__()
		asset = Assets().custom[asset_key]
		self.sprite = pyglet.sprite.Sprite(asset, batch=batch, group=group)
		self.scale_to_window_size()

	def scale_to_window_size(self):
		self.sprite.scale_x = Config()['window_dimensions'][0] / self.sprite.width
		self.sprite.scale_y = Config()['window_dimensions'][1] / self.sprite.height
		self.sprite.update(x=Config()['window_dimensions'][0] / 2, y=Config()['window_dimensions'][1] / 2)

class ButtonComponent(Node):
	def __init__(self, position, unit_dimensions, text, on_click, batch, area_group, text_group):
		super().__init__()
		self.text = text
		self.area = AreaComponent(position, unit_dimensions, batch=batch, group=area_group)
		self.on_click = on_click
		self.label = pyglet.text.Label(text, x=position[0], y=position[1], anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)

	def mouse_press_handler(self, command):
		if self.area.within_bounds((command.data['x'], command.data['y'])):
			self.on_click()

class TextBoxComponent(AreaComponent):
	def __init__(self, position, unit_width, label_text, max_length, batch, area_group, text_group):
		super().__init__(position, (unit_width, 2), align='left', batch=batch, group=area_group)
		self.label_text = label_text
		self.document = pyglet.text.document.UnformattedDocument('')
		self.document.set_style(0, 0, dict(color=(0, 0, 0, 255), font_size=15))

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, unit_width * 16, 24, multiline=False, batch=batch, group=text_group)
		self.layout.anchor_x = 'left'
		self.layout.anchor_y = 'center'
		self.layout.x = position[0]
		self.layout.y = position[1]

		self.caret = pyglet.text.caret.Caret(self.layout)

		self.max_length = max_length
		self.input_label = pyglet.text.Label(label_text, x=position[0], y=position[1] + self.asset[0].width * 2, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)
		self.input_error = pyglet.text.Label('', x=position[0], y=position[1] - 30, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255), batch=batch, group=text_group)
		self.selected = False

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

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			self.caret.visible = True
			self.caret.on_mouse_press(command.data['x'], command.data['y'], command.data['button'], command.data['modifiers'])
			self.selected = True
		else:
			self.caret.visible = False
			self.caret.mark = self.caret.position = 0
			self.selected = False

	def mouse_drag_handler(self, command):
		if self.selected:
			self.caret.on_mouse_drag(command.data['x'], command.data['y'], command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])
			self.enforce_length()

	def enforce_length(self):
		if len(self.document.text) > self.max_length:
			stored_caret_position = self.caret.position
			self.document.text = self.document.text[:self.max_length]
			self.caret.mark = self.caret.position = stored_caret_position

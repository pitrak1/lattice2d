import pyglet
from lattice2d.client.components.area import Area

class TextBox(Area):
	def __init__(self, position, unit_width, label_text, max_length):
		super().__init__(position, (unit_width, 2), align='left')
		self.label_text = label_text
		self.document = pyglet.text.document.UnformattedDocument('')
		self.document.set_style(0, 0, dict(color=(0, 0, 0, 255), font_size=15))

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, unit_width * 16, 24, multiline=False)
		self.layout.anchor_x = 'left'
		self.layout.anchor_y = 'center'
		self.layout.x = position[0]
		self.layout.y = position[1]

		self.caret = pyglet.text.caret.Caret(self.layout)

		self.max_length = max_length
		self.input_label = pyglet.text.Label(label_text, x=position[0], y=position[1] + self.asset[0].width + 15, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255))
		self.input_error = pyglet.text.Label('', x=position[0], y=position[1] - 60, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255))
		self.selected = False

	def register(self, batch, group_set):
		super().register(batch, group_set)
		self.layout.batch = batch
		self.layout.group = group_set[1]
		self.input_label.batch = batch
		self.input_label.group = group_set[1]
		self.input_error.batch = batch
		self.input_error.group = group_set[1]

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
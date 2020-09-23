from lattice2d.client.components.area import Area
from lattice2d.client.components.label import Label
from lattice2d.nodes import Node


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

	def register(self, batch, group_set):
		self.area.register(batch, group_set)
		self.label.batch = batch
		self.label.group = group_set[1]

	def mouse_press_handler(self, command):
		if self.area.within_bounds((command.data['x'], command.data['y'])):
			self.on_click()

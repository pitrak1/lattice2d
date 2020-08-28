import pyglet
from lattice2d.nodes.node import Node
from lattice2d.client.components.area import Area

class Button(Node):
	def __init__(self, position, unit_dimensions, text, on_click, batch, area_group, text_group):
		super().__init__()
		self.text = text
		self.area = Area(position, unit_dimensions, batch=batch, group=area_group, asset_key='grey_button')
		self.on_click = on_click
		self.label = pyglet.text.Label(text, x=position[0], y=position[1], anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)

	def mouse_press_handler(self, command):
		if self.area.within_bounds((command.data['x'], command.data['y'])):
			self.on_click()
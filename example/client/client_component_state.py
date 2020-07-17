import pyglet
from lattice2d.client.client_state import ClientState
from lattice2d.client.renderer import Renderer
from lattice2d.client.components.background import Background
from lattice2d.client.components.button import Button
from lattice2d.client.components.text_box import TextBox
from lattice2d.client.components.area import Area
from lattice2d.client.components.label import Label
from example.constants import WINDOW_CENTER, CONSTANTS

class ClientComponentState(ClientState):
	def redraw(self):
		self.text_box = TextBox(
			position=(WINDOW_CENTER[0], CONSTANTS['window_dimensions'][1] - 200), 
			unit_width=12,
			label_text='This is a labelled TextBox with a width of 12.',
			max_length=25,
			batch=self.renderer.get_batch(),
			area_group=self.renderer.get_group(1),
			text_group=self.renderer.get_group(2)
		)
		self.children = [
			Background(
				asset_key='background',
				batch=self.renderer.get_batch(), 
				group=self.renderer.get_group(0)
			),
			Label(
				'This Background uses a custom sprite.',
				x=10,
				y=CONSTANTS['window_dimensions'][1] - 40,
				font_size=20,
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Area(
				position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 200),
				unit_dimensions=(10, 5), 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Label(
				'This is a 10x5 Area.',
				x=WINDOW_CENTER[0] // 2,
				y=CONSTANTS['window_dimensions'][1] - 200,
				font_size=20,
				anchor_x='center',
				anchor_y='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			Button(
				position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 380),
				unit_dimensions=(8, 3),
				text='This is a 8x3 Button.', 
				on_click=self.button_press,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(1),
				text_group=self.renderer.get_group(2)
			),
			Label(
				'Clicking the button prints to the terminal.',
				x=WINDOW_CENTER[0] // 2,
				y=CONSTANTS['window_dimensions'][1] - 450,
				font_size=20,
				anchor_x='center',
				anchor_y='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			self.text_box,
			Button(
				position=(WINDOW_CENTER[0] * 1.5, CONSTANTS['window_dimensions'][1] - 380),
				unit_dimensions=(8, 3),
				text='Set TextBox error text', 
				on_click=self.set_error_message,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(1),
				text_group=self.renderer.get_group(2)
			),
			Button(
				position=(WINDOW_CENTER[0], 80),
				unit_dimensions=(8, 3),
				text='Continue to Next State', 
				on_click=self.next_state,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(1),
				text_group=self.renderer.get_group(2)
			),
		]

	def button_press(self):
		print('Button has been pressed!')

	def set_error_message(self):
		message = self.text_box.get_text()
		self.text_box.set_error_text(message)

	def next_state(self):
		self.to_network_state()

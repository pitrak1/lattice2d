from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.button import Button
from lattice2d.client.components.text_box import TextBox
from lattice2d.client.components.area import Area
from lattice2d.client.components.label import Label
from example.constants import WINDOW_CENTER, CONSTANTS

class ClientComponentState(ClientState):
	def __init__(self, add_command, custom_data={}):
		super().__init__(add_command, custom_data)
		self.register_component('background', 0, Background(
			asset_key='background'
		))
		self.register_component('area', 1, Area(
			position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 200),
			unit_dimensions=(10, 5)
		))
		self.register_component('background_label', 1, Label(
			'This Background uses a custom sprite.',
			x=10,
			y=CONSTANTS['window_dimensions'][1] - 40,
			font_size=20,
			color=(0, 0, 0, 255)
		))
		self.register_component('area_label', 2, Label(
			'This is a 10x5 Area.',
			x=WINDOW_CENTER[0] // 2,
			y=CONSTANTS['window_dimensions'][1] - 200,
			font_size=20,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('test_button', 1, Button(
			position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 380),
			unit_dimensions=(8, 3),
			text='This is a 8x3 Button.', 
			on_click=self.button_press
		))
		self.register_component('button_label', 1, Label(
			'Clicking the button prints to the terminal.',
			x=WINDOW_CENTER[0] // 2,
			y=CONSTANTS['window_dimensions'][1] - 450,
			font_size=20,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('text_box', 1, TextBox(
			position=(WINDOW_CENTER[0], CONSTANTS['window_dimensions'][1] - 200), 
			unit_width=12,
			label_text='This is a labelled TextBox with a width of 12.',
			max_length=25
		))
		self.register_component('error_message_button', 1, Button(
			position=(WINDOW_CENTER[0] * 1.5, CONSTANTS['window_dimensions'][1] - 380),
			unit_dimensions=(8, 3),
			text='Set TextBox error text', 
			on_click=self.set_error_message
		))
		self.register_component('next_button', 1, Button(
			position=(WINDOW_CENTER[0], 80),
			unit_dimensions=(8, 3),
			text='Continue to Next State', 
			on_click=self.next_state
		))

	def button_press(self):
		print('Button has been pressed!')

	def set_error_message(self):
		text_box = self.get_component('text_box')
		message = text_box.get_text()
		text_box.set_error_text(message)

	def next_state(self):
		self.to_network_state()

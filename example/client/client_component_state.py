from lattice2d.client import ClientState
from lattice2d.components import Background, Button, TextBox, Area, Label
from example.constants import WINDOW_CENTER, CONSTANTS


class ClientComponentState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.register_component('background', 'background', Background(
			asset_key='background'
		))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 200),
			unit_dimensions=(10, 5)
		))
		self.register_component('area_label', 'notifications', Label(
			'This is a 10x5 Area.',
			x=WINDOW_CENTER[0] // 2,
			y=CONSTANTS['window_dimensions'][1] - 200,
			font_size=20,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('background_label', 'notifications', Label(
			'This Background uses a custom sprite.',
			x=10,
			y=CONSTANTS['window_dimensions'][1] - 40,
			font_size=20,
			color=(0, 0, 0, 255)
		))
		self.register_component('test_button', 'base', Button(
			position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 380),
			unit_dimensions=(8, 3),
			text='This is a 8x3 Button.',
			on_click=self.button_press
		))
		self.register_component('button_label', 'notifications', Label(
			'Clicking the button prints to the terminal.',
			x=WINDOW_CENTER[0] // 2,
			y=CONSTANTS['window_dimensions'][1] - 450,
			font_size=20,
			anchor_x='center',
			anchor_y='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('text_box', 'base', TextBox(
			position=(WINDOW_CENTER[0], CONSTANTS['window_dimensions'][1] - 200),
			unit_width=12,
			label_text='This is a labelled TextBox with a width of 12.',
			max_length=25
		))
		self.register_component('error_message_button', 'base', Button(
			position=(WINDOW_CENTER[0] * 1.5, CONSTANTS['window_dimensions'][1] - 380),
			unit_dimensions=(8, 3),
			text='Set TextBox error text',
			on_click=self.set_error_message
		))
		self.register_component('next_button', 'base', Button(
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

import pyglet
from lattice2d.client.client_state import ClientState
from lattice2d.client.renderer import Renderer
from lattice2d.client.components.button import Button
from lattice2d.client.components.label import Label
from example.constants import WINDOW_CENTER, CONSTANTS
from lattice2d.command import Command

class ClientNetworkState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.response_count = 0
		super().__init__(add_command, custom_data)

	def redraw(self):
		self.response_label = Label(
			str(self.response_count),
			x=WINDOW_CENTER[0] * 1.5,
			y=CONSTANTS['window_dimensions'][1] - 420,
			font_size=20,
			anchor_x='center',
			anchor_y='center',
			color=(255, 255, 255, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(1)
		)
		self.children = [
			Button(
				position=(WINDOW_CENTER[0] // 2, CONSTANTS['window_dimensions'][1] - 380),
				unit_dimensions=(8, 3),
				text='Send Network Command', 
				on_click=self.button_press,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(1),
				text_group=self.renderer.get_group(2)
			),
			Label(
				'Clicking the Button sends a request to the server.',
				x=WINDOW_CENTER[0] // 2,
				y=CONSTANTS['window_dimensions'][1] - 450,
				font_size=20,
				anchor_x='center',
				anchor_y='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			Label(
				'Server responses:',
				x=WINDOW_CENTER[0] * 1.5,
				y=CONSTANTS['window_dimensions'][1] - 380,
				font_size=20,
				anchor_x='center',
				anchor_y='center',
				color=(255, 255, 255, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			self.response_label
		]

	def button_press(self):
		# 	Technically, the server is stateless outside of a game.  States only exist on the server
		# side in the context of a game.  The functionality of managing players and games can be 
		# done without states (and largely without the user of this repo having to write code).
		# However, because we want to show off how the user would actually use this repo, we need
		# to create a game context to see the functionality of our state.  So we create a game,
		# create a player, and then have the player join the game.
		
		if self.response_count == 0:
			self.add_command(Command('create_player', { 'player_name': 'Test Player' }, 'pending'))
			self.add_command(Command('create_game', { 'game_name': 'Test Game' }, 'pending'))
			self.add_command(Command('join_game', { 'game_name': 'Test Game' }, 'pending'))
		self.add_command(Command('some_network_command', status='pending'))

	def some_network_command_handler(self, command):
		if command.status == 'success':
			self.response_count += 1
			self.response_label.text = str(self.response_count)
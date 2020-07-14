import pyglet
from lattice2d.client.client_state import ClientState
from lattice2d.client.renderer import Renderer
from lattice2d.client.components.background import Background
from lattice2d.client.components.button import Button
from lattice2d.client.components.text_box import TextBox
from lattice2d.client.components.area import Area
from example.constants import WINDOW_CENTER

class ClientComponentState(ClientState):
	def redraw(self):
		self.children = [
			Background(
				asset_key='background',
				batch=self.renderer.get_batch(), 
				group=self.renderer.get_group(0)
			),
			Area(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
				unit_dimensions=(10, 15), 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1] + 50),
				unit_dimensions=(6, 2),
				text='Begin', 
				on_click=self.begin,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]

	def begin(self):
		print('test')
		# self.to_create_player_state()

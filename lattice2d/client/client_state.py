from lattice2d.nodes.node import Node
from lattice2d.client.renderer import Renderer

class ClientState(Node):
	def __init__(self, add_command, custom_data={}):
		super().__init__()
		self.add_command = add_command
		self.custom_data = custom_data
		self.renderer = Renderer()
		self.redraw()

	def redraw(self):
		raise NotImplementedError

	def client_redraw_handler(self, command):
		self.renderer.refresh()

	def on_draw(self):
		self.renderer.draw()
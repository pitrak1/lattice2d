import pyglet
from lattice2d.config import Config
from lattice2d.full.full_client import run, FullClientState
from lattice2d.full.full_server import FullServerState

class TestState(FullClientState):
	def redraw(self):
		self.other = [
			pyglet.text.Label(
				'Test', 
				color=(255, 255, 255, 255),
				x=400,
				y=400,
				group=self.renderer.get_group(0), 
				batch=self.renderer.get_batch()
			)
		]

Config({
	'full_solution': {
		'server_starting_state': FullServerState,
		'client_starting_state': TestState,
		'network': True
	}
})
run()

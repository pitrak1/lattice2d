import pyglet
from lattice2d.config import Config
from lattice2d.nodes import WindowRootNode, Node
from lattice2d.network import NetworkCommand, Client

class Renderer():
	def __init__(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None for i in range(Config().group_count)]

	def get_batch(self):
		return self.__batch

	def get_group(self, group_number):
		assert group_number >= 0 and group_number < Config().group_count
		if not self.__groups[group_number]:
			self.__groups[group_number] = pyglet.graphics.OrderedGroup(group_number)
		return self.__groups[group_number]

class FullClientState(Node):
	def __init__(self, set_state, add_command):
		super().__init__()
		self.set_state = set_state
		self.add_command = add_command
		self.renderer = Renderer()
		self.redraw()

	def redraw(self):
		raise NotImplementedError

	def client_redraw_handler(self, command):
		self.renderer = Renderer()
		self.redraw()

	def on_draw(self):
		self.renderer.get_batch().draw()

class FullClientNetwork(Client):
	def __init__(self, add_command, get_state):
		super().__init__(add_command)
		self.get_state = get_state

	def default_handler(self, command):
		if isinstance(command, NetworkCommand):
			if command.status == 'pending':
				command.update_and_send(connection=self.socket)

class FullClient(WindowRootNode):
	def __init__(self):
		super().__init__()
		self.current_state = Config().starting_state(self.set_state, self.add_command)
		if Config().network:
			self.client_network = ClientCore(self.add_command, self.get_state)
		self.children = [self.current_state]

	def set_state(self, state):
		self.current_state = state
		self.children = [self.current_state]

	def get_state(self):
		return self.current_state

def run():
	window = pyglet.window.Window(Config().window_width, Config().window_height)

	@window.event
	def on_draw():
		window.clear()
		game.on_draw()

	@window.event
	def on_update(dt):
		game.on_update(dt)

	game = FullClient()
	window.push_handlers(game)
	pyglet.clock.schedule_interval(on_update, 1 / 120.0)
	pyglet.app.run()
import pyglet
from lattice2d.config import Config
from lattice2d.assets import Assets
from lattice2d.nodes import Node, WindowRootNode
from lattice2d.network import Client

class Renderer():
	def __init__(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None for i in range(Config()['group_count'])]

	def get_batch(self):
		return self.__batch

	def get_group(self, group_number):
		assert group_number >= 0 and group_number < Config()['group_count']
		if not self.__groups[group_number]:
			self.__groups[group_number] = pyglet.graphics.OrderedGroup(group_number)
		return self.__groups[group_number]

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
		self.renderer = Renderer()
		self.redraw()

	def on_draw(self):
		self.renderer.get_batch().draw()

class ClientTransition():
	def __init__(self, core, key, value):
		self.core = core
		self.key = key
		self.value = value

	def run(self, custom_data={}):
		self.core.set_state(self.value, custom_data)

class ClientCore(WindowRootNode):
	def __init__(self, config):
		Config(config)
		super().__init__()
		self.window = pyglet.window.Window(Config()['window_dimensions'][0], Config()['window_dimensions'][1])
		self.window.push_handlers(self)
		if Config()['network']: self.__network = Client(self.add_command)
		self.set_state(Config()['client_states']['starting_state'])

	def set_state(self, state, custom_data={}):
		self.__current_state = state(self.add_command, custom_data)

		state_data = next(s for s in Config()['client_states']['states'] if s['state'] == state)
		self.transitions = {}
		for key, value in state_data['transitions'].items():
			transition = ClientTransition(self, key, value)			
			setattr(self.__current_state, key, transition.run)

		self.children = [self.__current_state]
		if Config()['network']: self.children.append(self.__network)

	def on_draw(self):
		self.window.clear()
		[child.on_draw() for child in self.children]

	def run(self):	
		pyglet.clock.schedule_interval(self.on_update, 1 / 120.0)
		pyglet.app.run()


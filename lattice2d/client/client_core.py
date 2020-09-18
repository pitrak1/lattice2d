import pyglet
from lattice2d.nodes.window_root_node import WindowRootNode
from lattice2d.config import Config
from lattice2d.network.client import Client
from lattice2d.client.client_transition import ClientTransition

class ClientCore(WindowRootNode):
	def __init__(self, config):
		Config(config)
		super(WindowRootNode).__init__()
		self.__initialize_window()
		self.__initialize_network()
		self.__initialize_state_machine()

	def __initialize_window(self):
		self.__window = pyglet.window.Window(
			Config()['window_dimensions'][0], 
			Config()['window_dimensions'][1]
		)
		self.__window.push_handlers(self)

	def __initialize_network(self):
		if Config()['network']:
			self.__network = Client(self.add_command)

	def __initialize_state_machine(self):
		self.set_state(Config()['client_states']['starting_state'])

	def set_state(self, state, custom_data={}):
		self.current_state = state(self.add_command, custom_data)

		state_data = next(s for s in Config()['client_states']['states'] if s['state'] == state)
		for key, value in state_data['transitions'].items():
			transition = ClientTransition(self, key, value)			
			setattr(self.current_state, key, transition.run)

		self.children = [self.current_state]
		if Config()['network']: self.children.append(self.__network)

	def on_draw(self):
		self.__window.clear()
		[child.on_draw() for child in self.children]

	def run(self):	
		pyglet.clock.schedule_interval(self.on_update, 1 / 120.0)
		pyglet.app.run()
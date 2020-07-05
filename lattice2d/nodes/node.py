from lattice2d.config import Config

class Node():
	def __init__(self):
		self.__handlers = {}
		handler_list = [func[:-8] for func in dir(self) if callable(getattr(self, func)) and '_handler' in func]
		for entry in Config()['command_types']:
			if entry in handler_list:
				self.__handlers[entry] = getattr(self, f'{entry}_handler')
			else:
				self.__handlers[entry] = self.default_handler
		self.children = []

	def on_command(self, command):
		return self.__handlers[command.type](command)

	def default_handler(self, command):
		return any(iter(child.on_command(command) for child in self.children))

	def on_update(self, dt=None):
		[child.on_update(dt) for child in self.children]

	def on_draw(self):
		[child.on_draw() for child in self.children]
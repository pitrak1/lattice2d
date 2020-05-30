from lattice2d.utilities.threaded_queue import ThreadedQueue
from lattice2d.config import Config
from lattice2d.utilities.logger import log, LOG_LEVEL_INTERNAL_LOW

class Command():
	def __init__(self, type_, data={}):
		self.type = type_
		self.data = data

class Node():
	def __init__(self):
		self.__handlers = {}
		handler_list = [func[:-8] for func in dir(self) if callable(getattr(self, func)) and '_handler' in func]
		for entry in Config().command_types:
			if entry in handler_list:
				self.__handlers[entry] = getattr(self, f'{entry}_handler')
			else:
				self.__handlers[entry] = self.default_handler
		self.children = []

	def on_command(self, command):
		return self.__handlers[command.type](command)

	def default_handler(self, command):
		results = [child.on_command(command) for child in self.children]
		return any(results)

	def on_update(self, dt=None):
		[child.on_update(dt) for child in self.children]

	def on_draw(self):
		[child.on_draw() for child in self.children]

class RootNode(Node):
	def __init__(self):
		super().__init__()
		self.command_queue = ThreadedQueue()

	def add_command(self, command):
		log(f'Adding command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
		self.command_queue.append(command)

	def on_update(self, dt=None):
		while self.command_queue.has_elements():
			command = self.command_queue.popleft()
			log(f'Handling command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			[child.on_command(command) for child in self.children]
		[child.on_update(dt) for child in self.children]

class RootNodeWithHandlers(RootNode):
	def on_update(self, dt=None):
		while self.command_queue.has_elements():
			command = self.command_queue.popleft()
			log(f'Handling command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.on_command(command)
			[child.on_command(command) for child in self.children]
		[child.on_update(dt) for child in self.children]

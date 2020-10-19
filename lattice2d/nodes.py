from lattice2d.config import Config
from lattice2d.utilities import log, ThreadedQueue


class Node:
	def __init__(self):
		self.__attach_handlers()
		self._children = {}

	def __attach_handlers(self):
		self.__handlers = {}
		handler_list = [func[:-8] for func in dir(self) if callable(getattr(self, func)) and '_handler' in func]
		for entry in Config()['command_types']:
			if entry in handler_list:
				self.__handlers[entry] = getattr(self, f'{entry}_handler')
			else:
				self.__handlers[entry] = self.default_handler

	def on_command(self, command):
		# noinspection PyArgumentList
		return self.__handlers[command.type](command)

	def default_handler(self, command):
		return any(iter(child.on_command(command) for child in self._children.values()))

	def on_update(self, dt=None):
		[child.on_update(dt) for child in self._children.values()]

	def on_draw(self):
		[child.on_draw() for child in self._children.values()]


class RootNode(Node):
	def __init__(self):
		super().__init__()
		self._command_queue = ThreadedQueue()

	def add_command(self, command):
		log(f'Adding command type {command.type}', 'lattice2d_core')
		self._command_queue.append(command)

	def on_update(self, dt=None):
		while self._command_queue.has_elements():
			command = self._command_queue.popleft()
			log(f'Handling command type {command.type}', 'lattice2d_core')
			self.on_command(command)
		[child.on_update(dt) for child in self._children.values()]

from lattice2d.utilities.threaded_queue import ThreadedQueue
from lattice2d.nodes.node import Node
from lattice2d.utilities.log import log, LOG_LEVEL_INTERNAL_LOW

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
			self.on_command(command)
		[child.on_update(dt) for child in self.children]

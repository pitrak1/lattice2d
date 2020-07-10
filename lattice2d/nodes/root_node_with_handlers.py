from lattice2d.nodes.root_node import RootNode
from lattice2d.utilities.log import log, LOG_LEVEL_INTERNAL_LOW

class RootNodeWithHandlers(RootNode):
	def on_update(self, dt=None):
		while self.command_queue.has_elements():
			command = self.command_queue.popleft()
			log(f'Handling command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.on_command(command)
		[child.on_update(dt) for child in self.children]
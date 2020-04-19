from utilities import threaded_queue
from commands import Command, WINDOW_COMMAND_TYPES

class Node():
	def __init__(self):
		self.handlers = {}
		for entry in WINDOW_COMMAND_TYPES:
			self.handlers[entry] = self.default_handler
		self.children = []

	def on_command(self, command):
		return self.handlers[command.type](command)

	def default_handler(self, command):
		results = [child.on_command(command) for child in self.children]
		return all(results)

	def on_update(self, dt=None):
		[child.on_update(dt) for child in self.children]

	def on_draw(self):
		[child.on_draw() for child in self.children]

class RootNode(Node):
	def __init__(self):
		super().__init__()
		self.command_queue = threaded_queue.ThreadedQueue()

	def add_command(self, command):
		self.command_queue.append(command)

	def on_update(self, dt=None):
		while self.command_queue.has_elements():
			command = self.command_queue.popleft()
			[child.on_command(command) for child in self.children]
		[child.on_update(dt) for child in self.children]

class WindowRootNode(RootNode):
	def on_key_press(self, symbol, modifiers):
		self.add_command(Command('key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_text(self, text):
		self.add_command(Command('text', { 'text': text }))

	def on_text_motion(self, motion):
		self.add_command(Command('text_motion', { 'motion': motion }))

	def on_text_motion_select(self, motion):
		self.add_command(Command('text_motion_select', { 'motion': motion }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.add_command(Command('mouse_press', { 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(Command('mouse_drag', { 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.add_command(Command('mouse_scroll', { 'x': x, 'y': y, 'dx': dx, 'dy': dy }))



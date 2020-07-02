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

class WindowRootNode(RootNode):
	def on_activate(self):
		self.add_command(Command('activate'))

	def on_close(self):
		self.add_command(Command('close'))

	def on_context_lost(self):
		self.add_command(Command('context_lost'))

	def on_context_state_lost(self):
		self.add_command(Command('context_state_lost'))

	def on_deactivate(self):
		self.add_command(Command('deactivate'))

	def on_expose(self):
		self.add_command(Command('expose'))

	def on_hide(self):
		self.add_command(Command('hide'))

	def on_key_press(self, symbol, modifiers):
		self.add_command(Command('key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_key_release(self, symbol, modifiers):
		self.add_command(Command('key_release', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(Command('mouse_drag', { 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }))

	def on_mouse_enter(self, x, y):
		self.add_command(Command('mouse_enter', { 'x': x, 'y': y }))

	def on_mouse_leave(self, x, y):
		self.add_command(Command('mouse_leave', { 'x': x, 'y': y }))

	def on_mouse_motion(self, x, y, dx, dy):
		self.add_command(Command('mouse_motion', { 'x': x, 'y': y, 'dx': dx, 'dy': dy }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.add_command(Command('mouse_press', { 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }))

	def on_mouse_release(self, x, y, button, modifiers):
		self.add_command(Command('mouse_release', { 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.add_command(Command('mouse_scroll', { 'x': x, 'y': y, 'dx': dx, 'dy': dy }))

	def on_move(self, x, y):
		self.add_command(Command('move', { 'x': x, 'y': y }))

	def on_resize(self, width, height):
		self.add_command(Command('resize', { 'width': width, 'height': height }))

	def on_show(self):
		self.add_command(Command('show'))

	def on_text(self, text):
		self.add_command(Command('text', { 'text': text }))

	def on_text_motion(self, motion):
		self.add_command(Command('text_motion', { 'motion': motion }))

	def on_text_motion_select(self, motion):
		self.add_command(Command('text_motion_select', { 'motion': motion }))

class RootNodeWithHandlers(RootNode):
	def on_update(self, dt=None):
		while self.command_queue.has_elements():
			command = self.command_queue.popleft()
			log(f'Handling command type {command.type}', LOG_LEVEL_INTERNAL_LOW)
			self.on_command(command)
		[child.on_update(dt) for child in self.children]

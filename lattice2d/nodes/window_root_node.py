from lattice2d.nodes.root_node import RootNode
from lattice2d.nodes.command import Command

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
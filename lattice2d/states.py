import pyglet

from lattice2d.nodes import RootNode, Node


class StateMachine(RootNode):
	def __init__(self, state_data):
		super().__init__()
		self.state_data = state_data
		self.set_state(state_data['starting_state'])

	def set_state(self, state, custom_data={}):
		self._current_state = state(self, custom_data)

		data = next(s for s in self.state_data['states'] if s['state'] == state)
		for key, value in data['transitions'].items():
			setattr(self._current_state, key, lambda data={}: self.set_state(value))

		self._children['state'] = self._current_state

class State(Node):
	def __init__(self, state_machine, custom_data={}):
		super().__init__()
		self.state_machine = state_machine
		self.custom_data = custom_data
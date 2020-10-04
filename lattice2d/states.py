import pyglet

from lattice2d.nodes import RootNode, Node


class StateMachine(RootNode):
	def __init__(self, state_data):
		super().__init__()
		self._state_data = state_data
		self.set_state(state_data['starting_state'])

	def set_state(self, state, custom_data={}):
		self._current_state = state(self, custom_data)

		data = next(s for s in self._state_data['states'] if s['state'] == state)
		for key, value in data['transitions'].items():
			transition = Transition(self, key, value)
			setattr(self._current_state, key, transition.run)

		self._children['state'] = self._current_state


class State(Node):
	def __init__(self, state_machine, custom_data={}):
		super().__init__()
		self.state_machine = state_machine
		self.custom_data = custom_data


class Transition:
	def __init__(self, core, key, value):
		self.core = core
		self.key = key
		self.value = value

	def run(self, custom_data={}):
		self.core.set_state(self.value, custom_data)

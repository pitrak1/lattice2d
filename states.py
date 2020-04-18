class StateController():
	def __init__(self, starting_state):
		self.set_state(starting_state, {})


	def set_state(self, state, data):
		self.current_state = state(self.set_state, data)


class State():
	def __init__(self, set_state, data):
		self.set_state = set_state
		self.data = data
from lattice2d.nodes import Node, RootNode

class StateController(RootNode):
	def __init__(self, starting_state):
		super().__init__()
		self.set_state(starting_state, {})

	def set_state(self, state, data):
		self.current_state = state(self.set_state, data)

class State(Node):
	def __init__(self, set_state, data):
		self.set_state = set_state
		self.data = data
from lattice2d.nodes import Node, RootNode, WindowRootNode

class WindowStateController(WindowRootNode):
	def __init__(self, starting_state, data={}):
		super().__init__()
		self.set_state(starting_state, data)

	def set_state(self, state, data):
		self.current_state = state(self.set_state, data)

class StateController(RootNode):
	def __init__(self, starting_state, data={}):
		super().__init__()
		self.set_state(starting_state, data)

	def set_state(self, state, data):
		self.current_state = state(self.set_state, data)

class State(Node):
	def __init__(self, set_state, data):
		super().__init__()
		self.set_state = set_state
		self.data = data

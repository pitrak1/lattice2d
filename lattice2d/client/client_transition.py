class ClientTransition():
	def __init__(self, core, key, value):
		self.core = core
		self.key = key
		self.value = value

	def run(self, custom_data={}):
		self.core.set_state(self.value, custom_data)
from lattice2d.nodes import Node


class Component(Node):
	def register(self, batch, group_set):
		raise NotImplementedError

import pyglet
from lattice2d.nodes import Node
from lattice2d.client.assets import Assets
from lattice2d.config import Config

class Component(Node):
	def register(self, batch, group_set):
		raise NotImplementedError


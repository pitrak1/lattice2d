import pyglet
from lattice2d.nodes import Node

class Label(pyglet.text.Label, Node):
	def __init__(self, *args, **kwargs):
		pyglet.text.Label.__init__(self, *args, **kwargs)
		Node.__init__(self)

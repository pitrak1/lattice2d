import pyglet
from lattice2d.client.components.component import Component

class Label(pyglet.text.Label, Component):
	def __init__(self, *args, **kwargs):
		pyglet.text.Label.__init__(self, *args, **kwargs)
		Component.__init__(self)

	def register(self, batch, group_set):
		self.batch = batch
		self.group = group_set[0]

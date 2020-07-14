import pyglet
from lattice2d.config import Config

class Renderer():
	def __init__(self):
		self.refresh()

	def add(self, component):
		component.set_batch(self.batch)
		self.components.append(component)

	def draw(self):
		self.batch.draw()

	def get_batch(self):
		return self.batch

	def refresh(self):
		self.batch = pyglet.graphics.Batch()
		self.groups = [None for i in range(Config()['group_count'])]
		self.components = []

	def get_group(self, group_number):
		assert group_number >= 0 and group_number < Config()['group_count']
		if not self.groups[group_number]:
			self.groups[group_number] = pyglet.graphics.OrderedGroup(group_number)
		return self.groups[group_number]
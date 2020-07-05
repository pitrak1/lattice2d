import pyglet
from lattice2d.config import Config

class Renderer():
	def __init__(self):
		self.__batch = pyglet.graphics.Batch()
		self.__groups = [None for i in range(Config()['group_count'])]

	def get_batch(self):
		return self.__batch

	def get_group(self, group_number):
		assert group_number >= 0 and group_number < Config()['group_count']
		if not self.__groups[group_number]:
			self.__groups[group_number] = pyglet.graphics.OrderedGroup(group_number)
		return self.__groups[group_number]
import pyglet
from lattice2d.client.components.component import Component
from lattice2d.client.assets import Assets
from lattice2d.config import Config

class Background(Component):
	def __init__(self, asset_key):
		super().__init__()
		asset = Assets().custom[asset_key]
		self.sprite = pyglet.sprite.Sprite(asset)
		self.__scale_to_window_size()

	def __scale_to_window_size(self):
		self.sprite.scale_x = Config()['window_dimensions'][0] / self.sprite.width
		self.sprite.scale_y = Config()['window_dimensions'][1] / self.sprite.height
		self.sprite.update(x=Config()['window_dimensions'][0] / 2, y=Config()['window_dimensions'][1] / 2)

	def register(self, batch, group_set):
		self.sprite.batch = batch
		self.sprite.group = group_set[0]
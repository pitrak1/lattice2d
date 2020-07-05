import pyglet
from lattice2d.nodes.node import Node
from lattice2d.client.assets import Assets

class Background(Node):
	def __init__(self, asset_key, batch, group):
		super().__init__()
		asset = Assets().custom[asset_key]
		self.sprite = pyglet.sprite.Sprite(asset, batch=batch, group=group)
		self.__scale_to_window_size()

	def __scale_to_window_size(self):
		self.sprite.scale_x = Config()['window_dimensions'][0] / self.sprite.width
		self.sprite.scale_y = Config()['window_dimensions'][1] / self.sprite.height
		self.sprite.update(x=Config()['window_dimensions'][0] / 2, y=Config()['window_dimensions'][1] / 2)
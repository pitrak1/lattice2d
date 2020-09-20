import pyglet
from lattice2d.client.assets import Assets
from lattice2d.config import Config
from lattice2d.nodes import Node
from lattice2d.utilities.bounds import within_rect_bounds

class Area(Node):
	def __init__(self, position, unit_dimensions, align='center', asset_key='grey_panel'):
		super().__init__()
		self.position = position
		self.unit_dimensions = unit_dimensions
		self.sprites = []

		self.asset = Assets().ui[asset_key]
		tile_size = self.asset[0].width

		if align == 'left':
			base_x_offset = 0
			base_y_offset = (unit_dimensions[1] - 1) / 2 * tile_size
		else:
			base_x_offset = (unit_dimensions[0] - 1) / 2 * tile_size
			base_y_offset = (unit_dimensions[1] - 1) / 2 * tile_size

		for j in range(unit_dimensions[1]):
			if j == 0:
				base_sprite_index = 0
			elif j == unit_dimensions[1] - 1:
				base_sprite_index = 6
			else:
				base_sprite_index = 3

			for i in range(unit_dimensions[0]):
				if i == 0:
					sprite_index = base_sprite_index + 0
				elif i == unit_dimensions[0] - 1:
					sprite_index = base_sprite_index + 2
				else:
					sprite_index = base_sprite_index + 1
				self.sprites.append(pyglet.sprite.Sprite(self.asset[sprite_index]))
				self.sprites[j * unit_dimensions[0] + i].update(
					x=position[0] - base_x_offset + tile_size * i, 
					y=position[1] - base_y_offset + tile_size * j,
				)

	def register(self, batch, group_set):
		for sprite in self.sprites:
			sprite.batch = batch
			sprite.group = group_set[0]

	def within_bounds(self, position):
		return within_rect_bounds(
			self.position, 
			position, 
			(self.unit_dimensions[0] * self.asset[0].width, self.unit_dimensions[1] * self.asset[0].height)
		)
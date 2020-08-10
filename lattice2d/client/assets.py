import pyglet
import os
from lattice2d.config import Config
from lattice2d.definitions import ROOT_DIR

COMMON = [
	{
		'variable_name': 'test_jpg',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'test_png',
		'location': 'test.png',
		'type': 'single'
	},
	{
		'variable_name': 'test_gif',
		'location': 'test.gif',
		'type': 'gif'
	},
	{
		'variable_name': 'test_single',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'test_grid',
		'location': 'test.jpg',
		'type': 'grid',
		'rows': 9,
		'columns': 8,
		'assets': [
			{
				'variable_name': 'test_grid_entry',
				'index': 0
			}
		]
	},
	{
		'variable_name': 'test_common',
		'location': 'test.jpg',
		'type': 'single'
	}
]

UI = [
	{
		'variable_name': 'test_ui',
		'location': 'test.jpg',
		'type': 'single'
	},
	{
		'variable_name': 'grey_panel',
		'location': 'grey_panel.png',
		'type': 'grid',
		'rows': 3,
		'columns': 3
	}
]

class InnerAssets:
	_shared_state = {}
	def __init__(self):
		self.__dict__ = self._shared_state

class Assets(InnerAssets):
	def __init__(self):
		super().__init__()
		
		if not hasattr(self, 'common'):
			self.__load_common()
			self.__load_ui()
			self.__load_characters()
			self.__load_tiles()
			self.__load_custom()


	def __load_common(self):
		pyglet.resource.path = [os.path.join(ROOT_DIR,'assets')]
		pyglet.resource.reindex()

		self.common = {}
		for entry in COMMON:
			self.__load_asset(entry, self.common)

	def __load_ui(self):
		pyglet.resource.path = [os.path.join(ROOT_DIR,'assets')]
		pyglet.resource.reindex()

		self.ui = {}
		for entry in UI:
			self.__load_asset(entry, self.ui)

	def __load_characters(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.characters = {}
		for entry in Config()['assets']['characters']:
			self.__load_asset(entry, self.characters)

	def __load_tiles(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.tiles = {}
		for entry in Config()['assets']['tiles']:
			self.__load_asset(entry, self.tiles)

	def __load_custom(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.custom = {}
		for entry in Config()['assets']['custom']:
			self.__load_asset(entry, self.custom)

	def __load_asset(self, entry, collection):
		if entry['type'] == 'single':
			image = pyglet.resource.image(entry['location'])
			self.__center_asset(image)
			collection[entry['variable_name']] = image
			return image
		elif entry['type'] == 'gif':
			gif = pyglet.resource.animation(entry['location'])
			self.__center_animation(gif)
			collection[entry['variable_name']] = gif
		else:
			image = pyglet.resource.image(entry['location'])
			grid = list(pyglet.image.ImageGrid(image, entry['rows'], entry['columns']))
			[self.__center_asset(i) for i in grid]
			if 'variable_name' in entry.keys(): collection[entry['variable_name']] = grid
			if 'assets' in entry.keys():
				for single_asset in entry['assets']:
					collection[single_asset['variable_name']] = grid[single_asset['index']]

	def __center_animation(self, asset):
		asset.anchor_x = asset.get_max_width() / 2
		asset.anchor_y = asset.get_max_height() / 2

	def __center_asset(self, asset):
		asset.anchor_x = asset.width / 2
		asset.anchor_y = asset.height / 2

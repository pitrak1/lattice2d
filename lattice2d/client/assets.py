import pyglet
import os
from lattice2d.config import Config
from lattice2d.definitions import ROOT_DIR

COMMON = {
	'test_jpg': {
		'location': 'test.jpg',
		'type': 'single'
	},
	'test_png': {
		'location': 'test.png',
		'type': 'single'
	},
	'test_gif': {
		'location': 'test.gif',
		'type': 'gif'
	},
	'test_single': {
		'location': 'test.jpg',
		'type': 'single'
	},
	'test_grid': {
		'location': 'test.jpg',
		'type': 'grid',
		'rows': 9,
		'columns': 8	
	},
	'test_common': {
		'location': 'test.jpg',
		'type': 'single'
	}
}

UI = {
	'test_ui': {
		'location': 'test.jpg',
		'type': 'single'
	},
	'grey_panel': {
		'location': 'grey_panel.png',
		'type': 'grid',
		'rows': 3,
		'columns': 3
	}
}

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
		for key, value in COMMON.items():
			self.common[key] = self.__load_asset(value)

	def __load_ui(self):
		pyglet.resource.path = [os.path.join(ROOT_DIR,'assets')]
		pyglet.resource.reindex()

		self.ui = {}
		for key, value in UI.items():
			self.ui[key] = self.__load_asset(value)

	def __load_characters(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.characters = {}
		for key, value in Config()['assets']['characters'].items():
			self.characters[key] = self.__load_asset(value)

	def __load_tiles(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.tiles = {}
		for entry in Config()['assets']['tiles']:
			self.tiles[entry['variable_name']] = self.__load_asset(entry['asset'])

	def __load_custom(self):
		pyglet.resource.path = [Config()['assets']['path']]
		pyglet.resource.reindex()

		self.custom = {}
		for key, value in Config()['assets']['custom'].items():
			self.custom[key] = self.__load_asset(value)

	def __load_asset(self, asset):
		if asset['type'] == 'single':
			image = pyglet.resource.image(asset['location'])
			self.__center_asset(image)
			return image
		elif asset['type'] == 'gif':
			gif = pyglet.resource.animation(asset['location'])
			self.__center_animation(gif)
			return gif
		else:
			image = pyglet.resource.image(asset['location'])
			grid = list(pyglet.image.ImageGrid(image, asset['rows'], asset['columns']))
			[self.__center_asset(i) for i in grid]
			if 'index' in asset.keys():
				return grid[asset['index']]
			else:
				return grid

	def __center_animation(self, asset):
		asset.anchor_x = asset.get_max_width() / 2
		asset.anchor_y = asset.get_max_height() / 2

	def __center_asset(self, asset):
		asset.anchor_x = asset.width / 2
		asset.anchor_y = asset.height / 2

import pyglet

from lattice2d.client import Assets

class TestClient:
	class TestAssets:
		class TestFileTypes:
			def test_loads_jpg(self):
				assert isinstance(Assets().common['test_jpg'], pyglet.image.Texture)

			def test_loads_png(self):
				assert isinstance(Assets().common['test_png'], pyglet.image.Texture)

			def test_loads_gif(self):
				assert isinstance(Assets().common['test_gif'], pyglet.image.animation.Animation)

		class TestLayouts:
			def test_loads_single(self):
				assert isinstance(Assets().common['test_single'], pyglet.image.Texture)

			def test_loads_grid_as_array(self):
				assert isinstance(Assets().common['test_grid'], list)
				assert isinstance(Assets().common['test_grid'][0], pyglet.image.Texture)

			def test_loads_individual_grid_entries_if_keys_provided(self):
				assert isinstance(Assets().common['test_grid_entry'], pyglet.image.Texture)

		class TestGroups:
			def test_loads_common_assets(self):
				assert isinstance(Assets().common['test_common'], pyglet.image.Texture)

			def test_loads_custom_assets(self):
				assert isinstance(Assets().custom['test_custom'], pyglet.image.Texture)

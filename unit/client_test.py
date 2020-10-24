import pyglet
import pytest

from lattice2d.client import Assets, ClientState, ClientCore
from lattice2d.config import Config
from lattice2d.components import Component
from config import CONFIG

@pytest.fixture(autouse=True)
def set_config():
	Config(CONFIG)

class ComponentClass(Component):
	def register(self, batch, group_set):
		pass

class TestClient:
	class TestAssets:
		class TestFileTypes:
			def test_loads_jpg(self):
				assert isinstance(Assets()['test_jpg'], pyglet.image.Texture)

			def test_loads_png(self):
				assert isinstance(Assets()['test_png'], pyglet.image.Texture)

			def test_loads_gif(self):
				assert isinstance(Assets()['test_gif'], pyglet.image.animation.Animation)

		class TestLayouts:
			def test_loads_single(self):
				assert isinstance(Assets()['test_single'], pyglet.image.Texture)

			def test_loads_grid_as_array_if_key_provided(self):
				assert isinstance(Assets()['test_grid'], list)
				assert isinstance(Assets()['test_grid'][0], pyglet.image.Texture)

			def test_loads_individual_grid_entries_if_keys_provided(self):
				assert isinstance(Assets()['test_grid_entry'], pyglet.image.Texture)

class TestClientState:
	def test_registers_and_removes_components(self):
		core = ClientCore()
		state = ClientState(core)
		component = ComponentClass()
		state.register_component('component', 'background', component)
		assert state.get_component('component') == component
		state.remove_component('component')
		with pytest.raises(AssertionError):
			state.get_component('component')

	def test_cannot_register_to_nonexistent_layer(self):
		core = ClientCore()
		state = ClientState(core)
		component = ComponentClass()
		with pytest.raises(AssertionError):
			state.register_component('component', 'fakelayer', component)

	def test_cannot_register_to_identifier_in_use(self):
		core = ClientCore()
		state = ClientState(core)
		component = ComponentClass()
		state.register_component('component', 'background', component)
		with pytest.raises(AssertionError):
			state.register_component('component', 'actors', component)

	def test_can_register_to_identifier_if_removed(self):
		core = ClientCore()
		state = ClientState(core)
		component = ComponentClass()
		state.register_component('component', 'background', component)
		state.remove_component('component')
		state.register_component('component', 'background', component)

	def test_cannot_get_unregistered_identifier(self):
		core = ClientCore()
		state = ClientState(core)
		with pytest.raises(AssertionError):
			state.get_component('component')

	def test_cannot_remove_unregistered_identifier(self):
		core = ClientCore()
		state = ClientState(core)
		with pytest.raises(AssertionError):
			state.remove_component('component')

	def test_resets_components(self):
		core = ClientCore()
		state = ClientState(core)
		component = ComponentClass()
		state.register_component('component', 'background', component)
		state.reset()
		with pytest.raises(AssertionError):
			state.get_component('component')

	def test_conditionally_removes_components(self):
		core = ClientCore()
		state = ClientState(core)
		state.conditionally_remove_component('component')

import pyglet
import types
import pytest
from lattice2d.client.renderer import Renderer

class TestRenderer():
	class TestAdd():
		def test_sets_batch_for_the_component(self, mocker):
			component = types.SimpleNamespace()
			renderer = Renderer()
			renderer.add(component)
			assert component.batch, renderer.batch

		def test_adds_component_to_components_list(self, mocker):
			component = types.SimpleNamespace()
			renderer = Renderer()
			renderer.add(component)
			assert renderer.components == [component]

	class TestRefresh():
		def test_creates_a_new_batch(self, mocker):
			renderer = Renderer()
			renderer.batch = None
			renderer.refresh()
			assert isinstance(renderer.batch, pyglet.graphics.Batch)

		def test_creates_a_new_list_of_groups(self, mocker):
			renderer = Renderer()
			renderer.groups = None
			renderer.refresh()
			assert isinstance(renderer.groups, list)

		def test_creates_a_new_list_of_components(self, mocker):
			renderer = Renderer()
			renderer.components = None
			renderer.refresh()
			assert isinstance(renderer.components, list)

	class TestGetGroup():
		def test_fails_if_group_number_is_negative(self, mocker):
			renderer = Renderer()
			with pytest.raises(AssertionError):
				renderer.get_group(-1)

		def test_fails_if_group_number_is_group_count_or_higher(self, mocker):
			renderer = Renderer()
			with pytest.raises(AssertionError):
				renderer.get_group(2)

		def test_returns_group(self, mocker):
			renderer = Renderer()
			assert isinstance(renderer.get_group(0), pyglet.graphics.OrderedGroup)

		def test_only_creates_groups_as_needed(self, mocker):
			renderer = Renderer()
			renderer.get_group(0)
			assert renderer.groups[1] == None
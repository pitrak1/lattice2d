import pytest
import pyglet
from lattice2d.full.full_client import Renderer

class TestRenderer():
	def test_creates_a_batch(self, mocker):
		renderer = Renderer()
		assert isinstance(renderer.get_batch(), pyglet.graphics.Batch)

	def test_does_not_create_a_group_before_requested(self, mocker):
		mocker.patch('pyglet.graphics.OrderedGroup')
		renderer = Renderer()
		pyglet.graphics.OrderedGroup.assert_not_called()
		renderer.get_group(0)
		pyglet.graphics.OrderedGroup.assert_called_once()

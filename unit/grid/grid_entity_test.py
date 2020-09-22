from lattice2d.grid.grid_entity import GridEntity
from lattice2d.command import Command

class TestGridEntity():
	def test_sets_grid_position(self, mocker):
		entity = GridEntity()
		entity.set_grid_position((2, 3))
		assert entity.grid_position == (2, 3)

	def test_adjusts_base_position(self, mocker):
		entity = GridEntity()
		command = Command('adjust_grid_position', { 'base_position': (1, 2) })
		entity.on_command(command)
		assert entity.base_position == (1, 2)

	def test_adjusts_base_scale(self, mocker):
		entity = GridEntity()
		command = Command('adjust_grid_scale', { 'base_scale': 1.5 })
		entity.on_command(command)
		assert entity.base_scale == 1.5

	def test_gets_applied_x_position(self, mocker):
		entity = GridEntity()
		entity.base_scale = 2
		entity.base_position = (5, 10)
		assert entity.get_scaled_x_position(3, 40) == (3 * 100 + 40) * 2 + 5

	def test_gets_applied_y_position(self, mocker):
		entity = GridEntity()
		entity.base_scale = 2
		entity.base_position = (5, 10)
		assert entity.get_scaled_y_position(2, 50) == (2 * 100 + 50) * 2 + 10
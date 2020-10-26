import os
import definitions

class PlayerClass:
	pass

class StartingState:
	def __init__(self, state_machine, custom_data={}):
		pass

class OtherState:
	def __init__(self, state_machine, custom_data={}):
		pass

class EmptyTile:
	def __init__(self, grid_position=(None, None), base_position=(0, 0)):
		pass


CONFIG = {
	'window_dimensions': (800, 600),
	# 'network': {
	# 	'ip_address': '0.0.0.0',
	# 	'port': 8080
	# },
	'rendering': {
		'layers': ['background', 'base', 'environment', 'actors', 'effects', 'ui', 'notifications'],
		'groups_per_layer': 6
	},
	'grid': {
		'width': 10,
		'height': 10,
		'size': 512
	},
	'command_types': [],
	'player_class': PlayerClass,
	'empty_tile_class': EmptyTile,
	'client_states': {
		'starting_state': StartingState,
		'states': [
			{
				'state': StartingState,
				'transitions': {
					'to_other_state': OtherState
				}
			},
			{
				'state': OtherState,
				'transitions': {}
			}
		]
	},
	'server_states': {
		'starting_state': StartingState,
		'states': [
			{
				'state': StartingState,
				'transitions': {
					'to_other_state': OtherState
				}
			},
			{
				'state': OtherState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(definitions.ROOT_DIR, 'assets'),
		'resources': [
			{
				'key': 'test_jpg',
				'location': 'test.jpg',
				'type': 'single'
			},
			{
				'key': 'test_png',
				'location': 'test.png',
				'type': 'single'
			},
			{
				'key': 'test_gif',
				'location': 'test.gif',
				'type': 'gif'
			},
			{
				'key': 'test_single',
				'location': 'test.jpg',
				'type': 'single'
			},
			{
				'key': 'test_grid',
				'location': 'test.jpg',
				'type': 'grid',
				'rows': 9,
				'columns': 8,
				'resources': [
					{
						'key': 'test_grid_entry',
						'index': 0
					}
				]
			}
		]
	}
}
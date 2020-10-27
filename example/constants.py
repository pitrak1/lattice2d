# 	Technically, the constants and the config did not have to be two separate files.  However, we 
# import the various states into the config itself, so therefore, we cannot import the config into
# the states because it would create a circular import.  So if you want to use the constants in 
# your config throughout your states, you need to put it a different file from the main config.

WINDOW_CENTER = (640, 360)

CONSTANTS = {
	'window_dimensions': (1280, 720),
	'network': {
		'ip_address': '0.0.0.0',
		'port': 8080
	},
	'logging': {
		'lattice2d_core': 'red',
		'lattice2d_network': 'cyan'
	},
	'rendering': {
		'layers': ['background', 'base', 'environment', 'actors', 'effects', 'ui', 'notifications'],
		'groups_per_layer': 3
	},
	'grid': {
		'width': 10,
		'height': 10,
		'size': 512
	}
}

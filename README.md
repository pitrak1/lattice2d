# Lattice2D

A package for boilerplate code for a grid based game using the [`pyglet`](http://pyglet.org/) library.  This package currently supports only square-tile grids, but will hopefully be expanded soon to support hex-tile grids as well.  This package provides a command-based hierarchy structure for game objects and additional functionality for creating clients and servers for network-based games.  

Conceptually, the hierarchy structure works by expecting a set number of commands to be handled by each game object.  Each game object then inherits from a base class that has a list of children that can be populated with other game objects, a method to take a command and call the appropriate handler, and a default handler that passes the command to the children if a handler is not given.  This makes it so game objects can inherit from the base class, add children game objects, and write methods to handle specific commands without having to worry about what's happening behind the scenes.  This means an entire set of game objects can be created and passed commands easily by just inheriting from a base class.

The networking functionality creates special game_objects that inherit from the base class from the command-based hierarchy structure while adding specific network and threading functionality to make creating a game client or game server easier.  Additionally, it creates a new command class that inherits from the command class used in the hierarchy structure while adding attributes to make networking easier.

## Guides to Use

## Package Functionality

Additional documentation for each package is the `README.md` files in each subdirectory.

## Configuration
The configuration for use of this repository is done with a singleton class Config (lattice2d.config).  If an argument is provided to the contructor, configuration values are set (`Config({ 'key', 'value' })`).  If the values just need to be read, the constructor can be called without an argument (`Config().command_types`).  

These are currently the configurable elements:
- window_dimensions: the width and height of the window as a tuple
- log_level: the minimum level to receive messages for the logger (defaults to -1, which displays nothing)
- group_count: the number of groups to have when rendering
- command_types: a list of strings for the command types expected by your nodes
- network:
	- ip_address: the IP address to network on (defaults to 0.0.0.0)
	- port: the port to network on (defaults to 8080)
- grid:
	- width: the width of the grid to create
	- height: the height of the grid to create
	- size: the size in pixels to space the grid
- player_class: the class to use as a player, recommend a subclass of `lattice2d.grid.player`
- client_states:
	- starting_state: the class to start the client state machine on
	- states: the state classes with transitions
		- state: the state class
		- transitions: a dictionary whose keys are method names, and those methods will transition the state to the state class associated to that key
- server_states:
	- starting_state: the class to start the server state machine on
	- states: the state classes with transitions
		- state: the state class
		- transitions: a dictionary whose keys are method names, and those methods will transition the state to the state class associated to that key
- assets:
	- path: the path to all the assets for your game
	- tiles: an array of the tile assets for your game
		- display_name: the label to display on the tile in the game
		- variable_name: a key to reference the asset by
		- asset:
			- location: the file location of the asset
			- type: the type of the asset; single, grid, or gif
			- index: the index of a frame of a grid asset (only for grid assets)
	- characters: a dictionary of the character assets for your game, accessible by the key for the dictionary
		- display_name: the label to display for the character in the game
		- location: the file location of the asset
		- type: the type of the asset; single, grid, or gif
		- index: the index of a frame of a grid asset (only for grid assets)
	- custom: a dictionary of any other assets you need for your game, accessible by the key for the dictionary
		- location: the file location of the asset
		- type: the type of the asset; single, grid, or gif
		- index: the index of a frame of a grid asset (only for grid assets)

Here is an example:
```
{
	'window_dimensions': (1280, 720),
	'log_level': 3,
	'group_count': 6,
	'command_types': ['mouse_press', 'key_press'],
	'network': {
		'ip_address': '0.0.0.0',
		'port': 8080
	},
	'player_class': Player,
	'client_states': {
		'starting_state': ClientState1,
		'states': [
			{
				'state': ClientState1,
				'transitions': {
					'to_client_state_2': ClientState2
				}
			},
			{
				'state': ClientState2,
				'transitions': {}
			}
		]
	},
	'server_states': {
		'starting_state': ServerState1,
		'states': [
			{
				'state': ServerState1,
				'transitions': {
					'to_server_state_2': ServerState2
				}
			},
			{
				'state': ServerState2,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': '/home/myfolder/assets/'
		'tiles': [
			{
				'display_name': 'Tile 1',
				'variable_name': 'tile_1',
				'asset': {
					'location': 'tile_1.jpg',
					'type': 'grid',
					'index': 5
				}
			}
		],
		'characters': {
			'character_1': {
				'display_name': 'Character 1',
				'location': 'character_1.png',
				'type': 'single'
			}
		},
		'custom': {
			'funny_gif': {
				'location': 'funny_gif.gif',
				'type': 'gif'
			}
		}
	}
}
```

## Testing

All tests are stored in the `unit` directory, and are run using pytest.  The following will run all tests `python3 -m pytest`.

## Installing Locally

In order to install this package locally, it needs to be built and then installed.

The following command creates a built package as a compressed file: `python3 setup.py sdist`

After the build, this package can be installed locally using the following command: `pip3 install --user dist/lattice2d-0.0.1.tar.gz`.  

```
python3 setup.py sdist
pip3 install --user dist/lattice2d-1.0.0.tar.gz
```

Note the version on the compressed file may be different depending on the settings in `setup.py`.

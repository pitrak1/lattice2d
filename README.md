# Lattice2D

A package for boilerplate code for a grid based game using the [`pyglet`](http://pyglet.org/) library.  This package currently supports only square-tile grids, but will hopefully be expanded soon to support hex-tile grids as well.  This package provides a command-based hierarchy structure for game objects and additional functionality for creating clients and servers for network-based games.  

## Guides to Use

An example project is located in `/example`.

## Package Functionality
### Command (lattice2d.command)
#### Command Class
- method `update_and_send`
	- updates the status, data, and/or connection and sends using the connection
	- arguments: the status, data, or connection to update
- class method `create_and_send`
	- creates a Command and sends using the given connection
	- arguments: the type, status, data, and connection to use to create the Command

This class is the class that is used to operate the entire command structure.  It has 4 properties: the type, the data, the status, and the connection.  Generally, the status and the connection are only used when sending commands over the network.

#### serialize Function
- arguments: the command to serialize

This function converts a Command to JSON.

#### deserialize Function
- arguments: the command string to deserialize

This function converts a JSON command string to a Command.

### Nodes (lattice2d.nodes)
#### Node Class
- method `on_command`
	- calls handler based on command type
	- arguments: the command to handle
- method `default_handler`
	- calls `on_command` on all children and returns true if any of the children's handlers return true, default handler for all command types
	- arguments: the command to handle
- method `on_update`
	- calls `on_update` on all children
	- arguments: the time since last update (optional)
- method `on_draw`
	- calls `on_draw` on all children
	- arguments: none

This class allows for (hopefully) transparent handling of commands.  The `on_command` method will handle all configured command types (see Configuration section for details) with the `default_handler` method which simply calls `on_command` on all children.  Handlers for specific command types can be created in subclasses and will be called instead of `default handler` if named according to the type of the command they are handling (for instance, commands with type `mouse_press` would be automatically handled by the method called `mouse_press_handler` that takes the command as its only argument).

The `on_update` and `on_draw` methods are for common game loop functionality.

#### RootNode Class
- inherits from Node
- method `add_command`
	- adds a command to the queue
	- arguments: the command to add
- method `on_update`
	- handles all commands in the queue and calls `on_update` on self
	- arguments: the time since last update (optional)

This class is meant to be at the top of the hierarchy of Nodes.  This is because it has a queue (see the `ThreadedQueue` class in the `Utilities` section for details) of commands that are passed to its children during `on_update`.

Additionally, this class contains built in handlers for translating pyglet events into commands.

### States (lattice2d.states)
#### StateMachine Class
- inherits from RootNode
- method `set_state`
    - sets the current state along with custom data
    - arguments: the state class to set and the custom data to include
    
This class is contains functionality to manage the current state and transition to a new state.

#### State Class
- inherits from Node

This class should be the base class for all states.  Managing states requires configuration, so please look at the configuration section below.

#### Transition Class
- method `run`
    - sets the current state to the transition's state along with custom data
    - arguments: the custom data to include
    
This class represents a transition from a given state to another and will automatically be generated on state transition from the configuration.

### Network (lattice2d.network)
#### Network Class
- inherits from Node
- method `receive`
	- reads data from given connection and calls `add_command` given on construction with the result
	- arguments: the connection to read from

This class stores common read functionality for all the following network classes.

#### Server Class
- inherits from Network
- method `run`
	- accepts incoming connections and creates new threads for each connection
	- arguments: none

This class gives the simplest implementation of a threaded, multiclient server application.

#### Client Class
- inherits from Network

This class creates a thread to constantly receive.  It is the simplest implementation for a client reading in a new thread.

### Grid Class

TODO

### Client

TODO

### Server

TODO

# Utilities (lattice2d.utilities)

This package contains many different useful classes and functions, which will be grouped and described below.

## Bounds (lattice2d.utilities.bounds)
These functions determine whether a point is in a shape.

- within_circle_bounds: determines whether a point is within a circle
- within_rect_bounds: determines whether a point is within a rectangle
- within_square_bounds: determines whether a point is within a square

## Log (lattice2d.utilities.log)
This is a useful logger with color coding and a customizable log level.  Log flags and their corresponding colors can be set in the configuration, and then using the log function is as easy as passing the string you want to print and the flag to it.  If the flag is included in the configuration, it will be printed.

## GetPageInfo (lattice2d.utilities.get_page_info)
This package contains a single function `get_page_info` that returns the indices of the elements and indications whether paging forward or backward is possible, given the current page, the size of each page, and the total count of elements.

Example: `[3, 5, False, True] = get_page_info(1, 3, 6)`

## ThreadedQueue (lattice2d.utilities.threaded_queue)
This package contains a deque that requires obtaining a lock to read from and write to.  This class also provides deque functionality used by the classes in this repository (`has_elements`, `popleft`, and `append`).

## ThreadedSync (lattice2d.utilities.threaded_sync)
This package contains a means to make all clients wait on other clients at a particular point.  This class contains a count set on contruction and protected by a lock on reads and writes, and only once the `count` method is called the number of times specified will the `done` method return true.

## Configuration

TODO UPDATE THIS

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

# Lattice2D

A package for boilerplate code for a grid based game using the [`pyglet`](http://pyglet.org/) library.  This package currently supports only square-tile grids, but will hopefully be expanded soon to support hex-tile grids as well.  This package provides a command-based hierarchy structure for game objects and additional functionality for creating clients and servers for network-based games.  

Conceptually, the hierarchy structure works by expecting a set number of commands to be handled by each game object.  Each game object then inherits from a base class that has a list of children that can be populated with other game objects, a method to take a command and call the appropriate handler, and a default handler that passes the command to the children if a handler is not given.  This makes it so game objects can inherit from the base class, add children game objects, and write methods to handle specific commands without having to worry about what's happening behind the scenes.  This means an entire set of game objects can be created and passed commands easily by just inheriting from a base class.

The networking functionality creates special game_objects that inherit from the base class from the command-based hierarchy structure while adding specific network and threading functionality to make creating a game client or game server easier.  Additionally, it creates a new command class that inherits from the command class used in the hierarchy structure while adding attributes to make networking easier.

The functionality will be documented in each package below.

### Node package (lattice2d.nodes)
#### Command Class
This very simple class simply has two attributes: `type` and `data`.  `type` is a string representing what kind of data to expect, and `data` is a dictionary containing data for the command.  `type` should only be set to a command type configured by the `Config` package.

#### Node Class
- method `on_command`
	- calls handler based on command type
	- arguments: the command to handle
- method `default_handler`
	- calls `on_command` on all children, default handler for all command types
	- arguments: the command to handle
- method `on_update`
	- calls `on_update` on all children
	- arguments: the time since last update (optional)
- method `on_draw`
	- calls `on_draw` on all children
	- arguments: none
- attribute `children`
	- a list of children nodes

This class allows for (hopefully) transparent handling of commands.  The `on_command` method will handle all configured command types (see Configuration section for details) with the `default_handler` method which simply calls `on_command` on all children.  Handlers for specific command types can be created in subclasses and will be called instead of `default handler` if named according to the type of the command they are handling (for instance, commands with type `mouse_press` would be automatically handled by the method called `mouse_press_handler` that takes the command as its only argument).

The `on_update` and `on_draw` methods are for common game loop functionality.

#### RootNode Class
- inherits from Node
- method `add_command`
	- adds a command to the queue
	- arguments: the command to add
- method `on_update`
	- handles all commands in the queue and calls `on_update` on all children
	- arguments: the time since last update (optional)

This class is meant to be at the top of the hierarchy of Nodes.  This is because it has a queue (see the `ThreadedQueue` class in the `Utilities` section for details) of commands that are passed to its children during `on_update`.  

#### WindowRootNode Class
- inherits from RootNode

This class simply allows you to use pyglet's `push_handlers` method on an instance of this class to handle common events.  This class has handlers for those event that correspond to handlers for pyglet events, and those handlers add appropriate commands to the queue.

### Network package (lattice2d.network)
#### NetworkCommand Class
- inherits from Command
- method `update_and_send`
	- updates the status, data, and/or connection and sends using the connection
	- arguments: the status, data, or connection to update
- class method `create_and_send`
	- creates a NetworkCommand and sends using the given connection
	- arguments: the type, status, data, and connection to use to create the NetworkCommand

This class adds the `status` and `connection` attributes to a standard Command as well as means to update, create, and send NetworkCommands easily while serializing/deserializing them properly.

#### serialize Function
- arguments: the command to serialize

This function converts a Command to JSON.

#### deserialize Function
- arguments: the commmand string to deserialize

This function converts a JSON command string to a Command or NetworkCommand, depending if `connection` and `status` are included.

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

### Grid Package (lattice2d.grid)
#### Actor Class
- inherits from Node
- method `set_position`
	- sets the `grid_x` and `grid_y` attributes
	- arguments: the grid_x and grid_y values to set

This class is barebones right now, but will eventually be the base class for all player characters and non-player characters in the grid.

#### EmptyTile Class
- inherits from Node
- method `set_position`
	- sets the `grid_x` and `grid_y` attributes
	- arguments: the grid_x and grid_y values to set

This class is barebones right now, but is the stand-in for all tiles on the grid that are empty.

#### Tile Class
- inherits from EmptyTile
- method `add_actor`
	- adds an Actor to this tile
	- arguments: the Actor to add
- method `remove_actor`
	- removes an Actor from this tile
	- arguments: the Actor to remove

This class is the barebones base class for all tiles on the grid, storing actors and other data.

#### TileGrid Class
- inherits from Node
- method `add_tile`
	- places a new tile in the grid and adds links to adjacent tiles based on `add_adjacent_links`
	- arguments: the grid_x and grid_y to add the tile and the tile itself
- virtual method `add_adjacent_links`
	- determines whether links should exist between two adjacent tiles
	- arguments: the two tiles to examine and potentially add links to
- method `add_actor`
	- adds an Actor to the tile at a given position
	- arguments: the grid_x and grid_y of the tile and the Actor to add
- method `move_actor`
	- removes an Actor from one tile and adds it to another
	- arguments: the grid_x and grid_y of the destination tile and the Actor to move

This class is meant to be extensible and customizable, providing a generalized base to work from.  Because we do not always want an Actor to be able to move to an adjacent tile, the `add_tile` method calls the `add_adjacent_links` method on every pair of tiles that may potentially need linkage.

### Full Package (lattice2d.full)
#### FullServer Class
- inherits from RootNode
- method `run`
	- loops in threads to update and receive
	- arguments: none
- method `add_command`
	- adds command to player's game if it exists, otherwise adds to main queue
	- arguments: the command to add
- method `create_player`
	- creates a FullPlayer and adds it to the players list
	- arguments: the name and connection to use in creation
- method: `destroy_player_by_connection`
	- finds the player from the connection, removes them from a game if they are in one, and destroys them
	- arguments: the connection to find the player from
- method: `destroy_player_by_name`
	- finds the player from the name, removes them from a game if they are in one, and destroys them
	- arguments: the name to find the player from
- method: `add_player_to_game_by_connection`
	- adds the player to a game using the player's connection
	- arguments: the game name and the connection to find the player from
- method: `add_player_to_game_by_name`
	- adds the player to a game using the player's name
	- arguments: the game name and the name to find the player from
- method: `create_game`
	- creates a new FullGame and adds it to the children
	- arguments: the game name to create
- method: `destroy_game`
	- finds a game by name and destroys it
	- arguments: the game name to destroy
- method `find_game_by_name`
	- finds game with name in all children, returns False if not found
	- arguments: the game name to look for
- method `find_player_by_name`
	- finds player with name in all children, returns False if not found
	- arguments: the player name to look for
- method `find_game_by_connection`
	- finds player with connection in all children, returns False if not found
	- arguments: the connection to look for

This class takes a more comprehensive approach to a multithreaded server.  It introduces the concept of FullPlayers and FullGames, whose attributes are in the corresponding classes below.  This allows a command to be added to a FullGame's queue instead of the main queue if the FullPlayer sending it has a FullGame associated with them.  This separation of reponsibilities (the main queue for server-wide requests, the game queues for commands for that game) allows commands to not filter through every single game every time a game state changes.

#### FullGame Class
- inherits from RootNode
- method `add_player`
	- adds the given FullPlayer to the game and sets the game and host references for the player
	- arguments: the player to add and whether or not they are host
- method `remove_player`
	- removes the given FullPlayer from the game; destroys the game if empty; broadcasts players left if not
	- arguments: the player to remove
- method `send_players_in_game`
	- sends a NetworkCommand of type `broadcast_players_in_game` to every player in the game other than the exception
	- arguments: the player to be excluded from the broadcast

This class is meant to be used in conjunction with the FullServer above, and is meant to make managing players easier.

#### FullPlayer Class
- inherits from Node

This class is currently very small, only having three attributes: `name`, `connection`, and `game`.

### Utilities
The `lattice2d/utilities` folder contains many useful classes and methods that are used elsewhere in this repository and can be used independently.

#### Bounds (lattice2d.utilities.bounds)
This file contains functions to determine whether a point is in a shape.

- within_circle_bounds: determines whether a point is within a circle
- within_rect_bounds: determines whether a point is within a rectangle
- within_square_bounds: determines whether a point is within a square

#### Logger (lattice2d.utilities.logger)
This file contains a useful logger with color coding, indentation, and a customizable log level.

The log levels are as follows:
- LOG_LEVEL_HIGH
- LOG_LEVEL_MEDIUM
- LOG_LEVEL_LOW
- LOG_LEVEL_INTERNAL_HIGH
- LOG_LEVEL_INTERNAL_LOW

The level can be configured (see the Configuration section for details), and setting a level will print messages on that level and above.  For instance, setting the level to `LOG_LEVEL_LOW` will read all messages logged at that level as well as `LOG_LEVEL_MEDIUM` and `LOG_LEVEL_HIGH`.  Log level for a particular message needs to be set each time a message is sent (for example: `log('some message', LOG_LEVEL_MEDIUM))`)

#### Pagination (lattice2d.utilities.pagination)
This file contains a single function `get_page_info` that returns the indices of the elements and indications whether paging forward or backward is possible, given the current page, the size of each page, and the total count of elements.

Example: `[3, 5, False, True] = get_page_info(1, 3, 6)`

#### ThreadedQueue (lattice2d.utilities.threaded_queue)
This file contains a deque that requires obtaining a lock to read from and write to.  This class also provides deque functionality used by the classes in this repository (`has_elements`, `popleft`, and `append`).

#### ThreadedSync (lattice2d.utilities.threaded_sync)
This file contains a means to make all clients wait on other clients at a particular point.  This class contains a count set on contruction and protected by a lock on reads and writes, and only once the `count` method is called the number of times specified will the `done` method return true.

## Configuration

The configuration for use of this repository is done with a singleton class Config (lattice2d.config).  If an argument is provided to the contructor, configuration values are set (`Config({ 'key', 'value' })`).  If the values just need to be read, the constructor can be called without an argument (`Config().command_types`).  

These are currently the configurable elements:
- command_types: a list of strings for the command types expected by your nodes
- log_level: the minimum level to receive messages for the logger
- full_solution: setting this to True adds commands necessary to use the `Full` package

Here is an example:
```
{
	'command_types': ['mouse_press', 'key_press'],
	'log_level': LOG_LEVEL_MEDIUM,
	'full_solution': True
}
```

## Testing

All tests are stored in the `unit` directory, and are run using pytest.  The following will run all tests `python3 -m pytest`.

## Installing Locally

In order to install this package locally, it needs to be built and then installed.

The following command creates a built package as a compressed file: `python3 setup.py sdist`

After the build, this package can be installed locally using the following command: `pip3 install --user dist/lattice2d-0.0.1.tar.gz`.  Note the version on the compressed file may be different depending on the settings in `setup.py`.

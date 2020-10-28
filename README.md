# Lattice2D

A package for boilerplate code for a grid based game using the [`pyglet`](http://pyglet.org/) library.  This package currently supports only square-tile grids, but will hopefully be expanded soon to support hex-tile grids as well.  This package provides a command-based hierarchy structure for game objects and additional functionality for creating clients and servers for network-based games.  

## Features

This section will go over the functionality of each package.  For additional guidance, see the `doc` directory.

### Command Hierarchy

Lattice2D provides a structure for having hierarchy of objects and for delivering commands to those objects.

The Command class holds the data for each of these commands, and the hierarchy of objects is made up of Nodes with a RootNode at the top.  The RootNode will manage a queue of commands to be handled on an update event, and when they're popped off, they'll be passed down the tree.  Additionally, this RootNode will manage update and draw events to be passed down the tree also.

Command types need to be configured, and for each command type, there is a handler that can be overridden on the Node class.  So a command type of `get_players_in_game` would have a method of `get_players_in_game_handler` on the Node class that can be overridden.

### Client/Server Multiplayer

Lattice2D supports a client and a multi-threaded server. On the client side, the network is just another node that can respond to certain command types.  On the server side, we accept new connections in the server and have a hierarchy structure like the client.  Serialization and deserialization is covered by converting to JSON and back to transmit the commands.  A command from the client to server should have a status of 'pending' and commands from the server to the client should have any other status, indicating success or a specific error.

### Grid

Lattice2D supports grids to be used on both the client and server side.  The TileGrid contains the entire grid, the Tile contains several actors in the scene, and an Actor represents a character, enemy, or any other moving entity.  All of these classes inherit from GridEntity, which maintains a grid position and translation of that grid position to a raw x and y for drawing.

There are a series of useful callbacks for common operations that should be overwritten for the Tile and Actor classes.

When an actor is added to a tile, the following callbacks are called in this order:
- Tile.before_actor_enter
- Actor.on_enter_tile
- Tile.after_actor_enter

When an actor is removed from a tile, the following callbacks are called in this order:
- Tile.before_actor_exit
- Actor.on_exit_tile
- Tile.after_actor_exit

When an actor is moved from one tile to another, the following callbacks are called in this order:
- StartTile.before_actor_exit
- EndTile.before_actor_enter
- Actor.on_exit_tile
- Actor.on_enter_tile
- StartTile.after_actor_exit
- EndTile.after_actor_enter

If any of these callbacks return True or anything truthy, the operation will not continue.

### Component Based Rendering

For rendering, inheriting from the Component class and overriding the `register` function will allow you to simply treat the things you want to draw as Nodes in the hierarchy.

## Example

An example project is located at `https://github.com/pitrak1/betrayal-pyglet`.  This was the project that this library was initially designed for.

## Package Functionality

Documentation for each package is included in the `doc` directory.

## Configuration

Documentation on how to configure Lattice2d is available in `doc/configuration_doc.md`.

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

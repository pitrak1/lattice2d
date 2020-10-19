
# Grid (lattice2d.grid)
## get_distance
This method takes a start and end grid position and finds the distance between them.  It does not account for diagonals.

## get_direction
This method determines the direction from a start to an end grid position, given that they are adjacent.

## reverse_direction
This method takes a direction and reverses it.

## UP, RIGHT, DOWN, LEFT
Four constants; UP, RIGHT, DOWN, and LEFT; correspond to 0, 1, 2, and 3, respectively.  This is simply to make an array of the directions starting pointing up and going clockwise.

## GridEntity Class
- inherits from Node
- method `get_grid_position`
    - gets the position of the entity in the grid
    - arguments: none
- method `set_grid_position`
	- allows setting the position of the entity in the grid
	- arguments: the grid position to set to
- method `adjust_grid_position_handler`
	- a command handler to change the position of the camera
	- arguments: the command containing the adjustment to the camera
- method `adjust_grid_scale_handler`
	- a command handler to change the zoom of the camera
	- arguments: the command containing the adjustment to the camera
- method `get_scaled_position`
	- gives a raw position by applying the camera position and zoom to the grid position
	- arguments: the grid offset and a raw offset

This class is what should make working with the camera as simple as sending `adjust_grid_position` and `adjust_grid_scale` commands.

## Actor Class
- inherits from GridEntity
- method `on_exit_tile`
    - callback when this actor exits a tile
    - arguments: the tile being exited
- method `on_enter_tile`
    - callback when this actor enters a tile
    - arguments: the tile being entered
- method `on_attack`
    - callback when this actor attacks another actor
    - arguments: the actor being attacked by this actor
- method `on_defend`
    - callback when this actor defends an attack from another actor
    - arguments: the actor attacking this actor
    
This class is meant to represent all actors, meaning enemies, player characters, and any other moving units in the tile grid.  This class really does nothing other than define the functions above to be overwritten.

For more information about how specifically the callbacks are used, see the Grid part of the Features section.

## Tile Class
- inherits from GridEntity
- method `get_actor`
    - gets an actor by its key
- method `add_actor`
	- adds an actor to the tile's children and sets the actor's grid position
	- arguments: the actor to add and the key to add it by
- method `remove_actor`
	- removes an actor from the tile's children and clears the actor's grid position
	- arguments: the key of the actor to remove
- method `add_actor_without_callbacks`
    - adds an actor without the callbacks on the tile or actor being called.
    - arguments: the actor to add and the key to add it
- method `remove_actor_without_callbacks`
    - removes an actor without the callbacks on the tile or actor being called
    - arguments: the key of the actor to remove
- method `before_actor_enter`
    - callback for before an actor enters the tile
    - arguments: the actor entering
- method `after_actor_enter`
    - callback for after an actor enters the tile
    - arguments: the actor that entered
- method `before_actor_exit`
    - callback for before an actor leaves the tile
    - arguments: the actor leaving
- method `after_actor_exit`
    - callback for after an actor leaves the tile
    - arguments: the actor that left
    
The Tile class represents all tiles in the grid and provides callbacks for actor management.

## TileGrid Class
- inherits from Node
- virtual method `add_adjacent_links`
	- meant to be overridden to determine what to do to adjacent tiles when a tile is added to the grid
	- arguments: the starting tile that was added and the ending tile that was adjacent to it
- method `add_tile`
	- adds a tile to the grid and calls `add_adjacent_links` on each adjacent tile if present
	- arguments: the position to add a tile and the tile to add
- method `add_actor`
	- adds an actor to the tile at a position
	- arguments: the position to add an actor and the actor to add
- method `move_actor`
	- moves an actor from one tile to another
	- arguments: the position to move the actor to and the actor to move
- method `adjust_grid_position_handler`
	- calculates adjustment to the camera position and then sends it to all the tiles
	- arguments: the command containing the raw camera position adjustment
- method `adjust_grid_scale_handler`
	- calculates adjustment to the camera zoom and then sends it to all the tiles
	- arguments: the command containing the raw camera scale adjustment
- method `mouse_press_handler`
	- calculates updated mouse press position based on camera zoom and position and sends it to the tiles
	- arguments: the command with the raw mouse press position information

This class contains a grid of tiles and hopefully does the heavy lifting in terms of camera adjustments, adding tiles, and moving actors.

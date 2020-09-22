# Grid (lattice2d.grid)
## Actor Class (lattice2d.grid.actor)
- inherits from GridEntity

This is a currently empty class, but is meant to represent any actor in the grid (players, enemies, etc).

## EmptyTile Class (lattice2d.grid.empty_tile)
- inherits from GridEntity

This is a currently empty class, but is meant to represent any spaces that are not occupied in the grid.

## GridEntity Class (lattice2d.grid.grid_entity)
- inherits from Node
- method `set_grid_position`
	- allows setting the position of the entity in the grid
	- arguments: the grid position to set to
- method `adjust_grid_position_handler`
	- a command handler to change the position of the camera
	- arguments: the command containing the adjustment to the camera
- method `adjust_grid_scale_handler`
	- a command handler to change the zoom of the camera
	- arguments: the command containing the adjustment to the camera
- method `get_scaled_x_position`
	- gives a raw x position by applying the camera position and zoom to the grid x position
	- arguments: the grid x position and an offset
- method `get_scaled_y_position`
	- gives a raw y position by applying the camera position and zoom to the grid y position
	- arguments: the grid y position and an offset

This class is what should make working with the camera as simple as sending `adjust_grid_position` and `adjust_grid_scale` commands.

## Grid Navigation (lattice2d.grid.grid_navigation)
### get_distance
This method takes a start and end grid position and finds the distance between them.  It does not account for diagonals.

### get_direction
This method determines the direction from a start to an end grid position, given that they are adjacent.

### reverse_direction
This method takes a direction and reverses it.

### Directions
Four constants; UP, RIGHT, DOWN, and LEFT; correspond to 0, 1, 2, and 3, respectively.  This is simply to make an array of the directions starting pointing up and going clockwise.

## Player (lattice2d.grid.player)
- inherits from Actor

This class is just an actor, but allows setting a name, connection, and game.

## Tile (lattice2d.grid.tile)
- inherits from GridEntity
- method `add_actor`
	- adds an actor to the tile's children and sets the actor's grid position
	- arguments: the actor to add
- method `remove_actor`
	- removes an actor from the tile's children and clears the actor's grid position
	- arguments: the actor to remove

This class is just meant to make adding and removing actors easier.

## TileGrid (lattice2d.grid.tile_grid)
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
	- calcalates updated mouse press position based on camera zoom and position and sends it to the tiles
	- arguments: the command with the raw mouse press position information

This class contains a grid of tiles and hopefully does the heavy lifting in terms of camera adjustments, adding tiles, and moving actors.
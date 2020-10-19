
# Components (lattice2d.client.components)
## Area Class (lattice2d.client.components.area)
- inherits from Node
- method `within_bounds`
	- determines if a position is within the bounds of the shape
	- arguments: the position to check

The Area class draws an arbitrarily sized area using a 9-tile asset.

## Background Class (lattice2d.client.components.background)
- inherits from Node

The Background class is a node that has a sprite that will scale to the full window size based on the configuration.

## Button Class (lattice2d.client.components.button)
- inherits from Node
- method `mouse_press_handler`
	- determines if the position in the command is within bounds, and if so, calls the callback given in the constructor
	- arguments: the command with the position

The Button class is simply an area with a label that allows for a callback to be called when clicked.

## TextBox Class (lattice2d.client.components.text_box)
- inherits from Area

The TextBox class uses a lot of functionality supplied by pyglet to create a clickable, highlightable text box.

# Client (lattice2d.client)
## ClientCore Class (lattice2d.client.client_core)
- inherits from WindowRootNode
- method `set_state`
	- sets the state and populates transitions to future states
	- arguments: the state to transition to and custom data (optional)
- method `on_draw`
	- clears the window and draws all children to the screen
	- arguments: none
- method `run`
	- schedules the `on_update` method to run on an interval and runs it
	- arguments: none

The ClientCore class is intended to allow for a full abstraction of states and networking.  Ideally, this class should be able to be run and hide all the workings of the network and state machine, if configured properly.

## ClientState Class (lattice2d.client.client_state)
- inherits from Node
- virtual method `redraw`
	- adds elements to the Renderer to be drawn
	- arguments: none
- attribute `set_state`
	- callback to change the state
- attribute `add_command`
	- callback to add a command to the command queue
- attribute `renderer`
	- an instance of Renderer() to get the batches and groups from

The client solution allows you to provide a starting class in the configuration and then transition through those classes using the `set_state` callback.  This should be the base class for all the states in your game, or the client of your game if you're using the networked solution.

## ClientTransition Class (lattice2d.client.client_transition)
- method `run`
	- sets the core's state to the contained state
	- arguments: custom data to include (optional)

This class is tiny, but allows us to keep in memory the state transitions for the client state machine.

## Renderer Class (lattice2d.client.renderer)
- method `get_batch`
	- returns the batch for the renderer
	- arguments: none
- method `get_group`
	- returns a specific group by its number and creates it if it's not created yet
	- arguments: the group number of the group to get/create

This class makes managing batches and groups easier.  The only real logic in this class is that groups are only made if they are requested in `get_group`.  That means the number of groups we have are as small as possible.  This class is created in the constructor of `FullClientState` and will also be recreated every time the scene needs to be redrawn (controlled by the `redraw` command).  It would be nice to simply change components and sprites directly instead of scrapping it and readding them, but batched rendering makes this the best solution.

## Components (lattice2d.client.components)
### Area Class (lattice2d.client.components.area)
- inherits from Node
- method `within_bounds`
	- determines if a position is within the bounds of the shape
	- arguments: the position to check

The Area class draws an arbitrarily sized area using a 9-tile asset.

### Background Class (lattice2d.client.components.background)
- inherits from Node

The Background class is a node that has a sprite that will scale to the full window size based on the configuration.

### Button Class (lattice2d.client.components.button)
- inherits from Node
- method `mouse_press_handler`
	- determines if the position in the command is within bounds, and if so, calls the callback given in the constructor
	- arguments: the command with the position

The Button class is simply an area with a label that allows for a callback to be called when clicked.

### TextBox Class (lattice2d.client.components.text_box)
- inherits from Area

The TextBox class uses a lot of functionality supplied by pyglet to create a clickable, highlightable text box.

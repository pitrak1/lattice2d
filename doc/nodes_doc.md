# Nodes (lattice2d.nodes)
## Node Class
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

## RootNode Class
- inherits from Node
- method `add_command`
	- adds a command to the queue
	- arguments: the command to add
- method `on_update`
	- handles all commands in the queue and calls `on_update` on self
	- arguments: the time since last update (optional)

This class is meant to be at the top of the hierarchy of Nodes.  This is because it has a queue (see the `ThreadedQueue` class in the `Utilities` section for details) of commands that are passed to its children during `on_update`.

Additionally, this class contains built in handlers for translating pyglet events into commands.

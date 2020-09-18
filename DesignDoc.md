#Lattice2D

Lattice2D is a game engine for single or multiplayer, turn-based, square or hex grid games.

##Overview
    The focus of Lattice2D is to create a framework for building a particular type of game where you should be able to create it by configuring Lattice2D correctly and describing what you’d like to see.  Additionally, Lattice2D should be extensible by way of inheritance to allow for more advanced features to be implemented.

##Features
###Client and Server

Both the client and the server are controlled by Lattice2D classes: ClientCore and ServerCore.  These two classes take the configuration for your application as an argument to their constructors.  These classes parse the configuration and set up the rest of the framework for you.  Starting a client might look like this:

```
from lattice2d.client.client_core import ClientCore
from config import CONFIG

c = ClientCore(CONFIG)
c.run()
```

###State Machine

A state machine exists for both the client and the server in the context of a game.  States can be created by inheriting from the ClientState or ServerState classes and then configured to be used.  The configuration should allow specifying transitions by identifying a starting state and what method name to call to transition to what state.  An example configuration is:

```
'client_states': {
	'starting_state': FirstClientState,
	'states': [
		{
			'state': FirstClientState,
			'transitions': {
				'to_normal_client_state': SecondClientState,
				'to_alternative_client_state': AlternativeClientState
			}
		},
		{
			'state': SecondClientState,
			'transitions': {}
		},
		{
			'state': AlternativeClientState,
			'transitions': {}
		}
	]
},
'server_states': {
	'starting_state': FirstServerState,
	'states': [
		{
			'state': FirstServerState,
			'transitions': {}
		}
	]
}
```
###Command Structure

On both the client and server side, there is a command structure, allowing for communication throughout the entire hierarchy of objects as well as between the client and server.  A set number of commands will be provided by default for common pyglet and game/player management behavior, but new command types can be registered through configuration.  By default, every node in the hierarchy will have its default handler be to pass that command to its children. This is handled the same way for pyglet draw and update events.  The command structure relies on the Node class to handle everything, and therefore, every element in the hierarchy should inherit from Node or a subclass of Node.  Additionally, the Command and NetworkCommand classes serve as the objects to be passed through the hierarchy.  A Command has a type that will correspond to the handler you should define to catch it (for instance, a Command of type 'mouse_click' will call 'mouse_click_handler' if defined on an object in the hierarchy).  A NetworkCommand is very similar but has a connection (to indictate where the command came from on the server side) and a status.  A RootNode should serve as the first element of your hierarchy, a child to no other Node.  This is because the RootNode class actually manages the queue of commands and handles those commands during an update.  Defining your own command types in the configuration might look like this:

```
'command_types': ['my_command_type', 'my_other_command_type']
```

If configured like this, any Node with `my_command_type_handler` or `my_other_command_type_handler` defined would have those handlers called in the event of that command occurring.

###Asset Management

Lattice2D has built in assets for built in components, but you can additionally configure your own custom assets to be loaded on application start.  It also allows for three different types of assets: single, grid, and gif.  Configuring Lattice2D to load custom assets might look like this: 

```
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
```

Accessing these assets can be done by creating the singleton class and referencing the type and identifier. For example, `Assets().tiles['tile_1']`.

# Server (lattice2d.server)
## ServerCore Class (lattice2d.server.server_core)
- inherits from RootNodeWithHandlers
- method `run`
	- loops in threads to update and receive
	- arguments: none
- method `add_command`
	- adds command to player's game if it exists, otherwise adds to main queue
	- arguments: the command to add
- method `destroy_game`
	- destroys a game by name
	- arguments: the game name to destroy
- method `destroy_game_handler`
	- destroys a game by name
	- arguments: the command with the game name to destroy
- method `create_player_handler`
	- creates a player from name and connection
	- arguments: the command with the player info
- method `create_game_handler`
	- creates a game from name
	- arguments: the command with the game name
- method `get_games_handler`
	- gets the number of players and game name of all games
	- arguments: the command to update and send back
- method `join_game_handler`
	- adds the requesting player to a game by name
	- arguments: the command from the player with the game name
- method `logout_handler`
	- destroys a player by connection
	- arguments: the command from the player

This class takes a more comprehensive approach to a multithreaded server.  It introduces the concept of ServerGames, whose attributes are in the corresponding class below.  This class also allows a command to be added to a ServerGame's queue instead of the main queue if the Player sending it has a ServerGame associated with them.  This separation of reponsibilities (the main queue for server-wide requests, the game queues for commands for that game) allows commands to not filter through every single game every time a game state changes.

## ServerGame Class
- inherits from RootNode
- method `get_current_player`
	- returns the player whose turn it is
	- arguments: none
- method `is_current_player`
	- returns true if it is the given player's turn
	- arguments: the player to check
- method `add_player`
	- adds the given FullPlayer to the game and sets the game and host references for the player
	- arguments: the player to add and whether or not they are host
- method `remove_player`
	- removes the given FullPlayer from the game; destroys the game if empty; broadcasts players left if not
	- arguments: the player to remove
- method `broadcast_players`
	- sends a NetworkCommand of type `broadcast_players_in_game` to every player in the game other than the exception
	- arguments: the player to be excluded from the broadcast

This class is meant to be used in conjunction with the FullServer above, and is meant to make managing players easier.

## ServerState Class
- inherits from Node
- method `broadcast_players_in_game_handler`
	- sends a given command to all the players in the game
	- arguments: the command to send
- method `leave_game_handler`
	- removes the player from the game by connection
	- arguments: the command from the player to remove
- method `get_current_player_handler`
	- sends back `self` if requesting player is current player, otherwise send back player name
	- arguments: the command to update and return

This class hopefully covers the bases for player and game management that FullServer didn't cover.
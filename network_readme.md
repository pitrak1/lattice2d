# Network package (lattice2d.network)
## NetworkCommand Class (lattice2d.network.network_command)
- inherits from Command
- method `update_and_send`
	- updates the status, data, and/or connection and sends using the connection
	- arguments: the status, data, or connection to update
- class method `create_and_send`
	- creates a NetworkCommand and sends using the given connection
	- arguments: the type, status, data, and connection to use to create the NetworkCommand

This class adds the `status` and `connection` attributes to a standard Command as well as means to update, create, and send NetworkCommands easily while serializing/deserializing them properly.

## serialize Function (lattice2d.network.serialize)
- arguments: the command to serialize

This function converts a Command to JSON.

## deserialize Function (lattice2d.network.deserialize)
- arguments: the commmand string to deserialize

This function converts a JSON command string to a Command or NetworkCommand, depending if `connection` and `status` are included.

## Network Class (lattice2d.network.network)
- inherits from Node
- method `receive`
	- reads data from given connection and calls `add_command` given on construction with the result
	- arguments: the connection to read from

This class stores common read functionality for all the following network classes.

## Server Class (lattice2d.network.server)
- inherits from Network
- method `run`
	- accepts incoming connections and creates new threads for each connection
	- arguments: none

This class gives the simplest implementation of a threaded, multiclient server application.

## Client Class (lattice2d.network.client)
- inherits from Network

This class creates a thread to constantly receive.  It is the simplest implementation for a client reading in a new thread.
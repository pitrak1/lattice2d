# Command (lattice2d.command)
## Command Class
- method `update_and_send`
	- updates the status, data, and/or connection and sends using the connection
	- arguments: the status, data, or connection to update
- class method `create_and_send`
	- creates a Command and sends using the given connection
	- arguments: the type, status, data, and connection to use to create the Command

This class is the class that is used to operate the entire command structure.  It has 4 properties: the type, the data, the status, and the connection.  Generally, the status and the connection are only used when sending commands over the network.

## serialize Function
- arguments: the command to serialize

This function converts a Command to JSON.

## deserialize Function
- arguments: the command string to deserialize

This function converts a JSON command string to a Command.

# States (lattice2d.states)
## StateMachine Class
- inherits from RootNode
- method `set_state`
    - sets the current state along with custom data
    - arguments: the state class to set and the custom data to include
    
This class is contains functionality to manage the current state and transition to a new state.

## State Class
- inherits from Node

This class should be the base class for all states.  Managing states requires configuration, so please look at the configuration section below.

## Transition Class
- method `run`
    - sets the current state to the transition's state along with custom data
    - arguments: the custom data to include
    
This class represents a transition from a given state to another and will automatically be generated on state transition from the configuration.

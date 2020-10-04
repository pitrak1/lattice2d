import types
import pytest
from lattice2d.states import StateMachine, State


class MyStateMachine(StateMachine):
	def get_state(self):
		return self._current_state


class MyState(State):
	pass


class MyOtherState(State):
	pass


class MyOtherOtherState(State):
	pass


@pytest.fixture
def create_state_machine():
	def _create_state_machine():
		state_data = {
			'starting_state': MyState,
			'states': [
				{
					'state': MyState,
					'transitions': {
						'go_to_other_state': MyOtherState,
						'go_to_other_other_state': MyOtherOtherState
					}
				},
				{
					'state': MyOtherState,
					'transitions': {
						'go_back': MyState
					}
				},
				{
					'state': MyOtherOtherState,
					'transitions': {}
				}
			]
		}
		return MyStateMachine(state_data)

	return _create_state_machine


class TestStateMachine:
	def test_starts_on_starting_state(self, create_state_machine):
		state_machine = create_state_machine()
		assert isinstance(state_machine.get_state(), MyState)

	def test_transitions_to_other_states(self, create_state_machine):
		state_machine = create_state_machine()
		state_machine.get_state().go_to_other_state()
		assert isinstance(state_machine.get_state(), MyOtherState)

	def test_allows_branching_transitions(self, create_state_machine):
		state_machine = create_state_machine()
		state_machine.get_state().go_to_other_state()
		state_machine.get_state().go_back()
		state_machine.get_state().go_to_other_other_state()
		assert isinstance(state_machine.get_state(), MyOtherOtherState)

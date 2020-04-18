from states import State, StateController

class TestState1(State):
	pass

class TestState2(State):
	pass

class TestStates():
	def test_allows_setting_state(self):
		controller = StateController(State)


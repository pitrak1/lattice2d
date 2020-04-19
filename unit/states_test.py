from states import State, StateController

class TestState1(State):
	__test__ = False

class TestState2(State):
	__test__ = False

class TestStates():
	def test_sets_starting_state(self):
		controller = StateController(TestState1)
		assert isinstance(controller.current_state, TestState1)

	def test_allows_setting_state(self):
		controller = StateController(TestState1)
		controller.set_state(TestState2, {})
		assert isinstance(controller.current_state, TestState2)

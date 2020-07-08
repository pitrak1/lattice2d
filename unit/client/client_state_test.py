import pyglet
from lattice2d.client.client_state import ClientState
from lattice2d.client.renderer import Renderer

class FakeClientState(ClientState):
	def __init__(self, add_command, mocker, custom_data={}):
		self.redraw_stub = mocker.stub()
		super().__init__(add_command, custom_data)

	def redraw(self):
		self.redraw_stub()

class TestClientState():
	class TestConstructor():
		def test_creates_renderer(self, mocker):
			state = FakeClientState(mocker.stub(), mocker)
			assert isinstance(state.renderer, Renderer)

		def test_calls_redraw(self, mocker):
			state = FakeClientState(mocker.stub(), mocker)
			state.redraw_stub.assert_called_once()

	class TestClientRedrawHandler():
		def test_creates_renderer(self, mocker):
			state = FakeClientState(mocker.stub(), mocker)
			state.renderer = None
			state.client_redraw_handler({})
			assert isinstance(state.renderer, Renderer)

		def test_calls_redraw(self, mocker):
			state = FakeClientState(mocker.stub(), mocker)
			state.client_redraw_handler({})
			assert state.redraw_stub.call_count == 2

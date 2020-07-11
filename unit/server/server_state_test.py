import types
from lattice2d.nodes.command import Command
from lattice2d.network.network_command import NetworkCommand
from lattice2d.server.server_state import ServerState

class TestServerState():
	class TestBroadcastPlayersInGameHandler():
		def test_sends_to_all_if_not_given_exception(self, mocker):
			game = types.SimpleNamespace()
			game.broadcast_players = mocker.stub()
			state = ServerState(game)
			command = Command('broadcast_players_in_game')
			state.on_command(command)
			game.broadcast_players.assert_called_once()

		def test_sends_to_all_but_exception_if_given_exception(self, mocker):
			game = types.SimpleNamespace()
			game.broadcast_players = mocker.stub()
			state = ServerState(game)
			command = Command('broadcast_players_in_game', { 'exception': 'player1' })
			state.on_command(command)
			game.broadcast_players.assert_called_once_with('player1')

	class TestGetCurrentPlayerHandler():
		def test_returns_self_in_player_name_if_current_player(self, mocker, get_keyword_args):
			game = types.SimpleNamespace()
			game.is_current_player = lambda player : True
			game.players = []
			state = ServerState(game)
			command = NetworkCommand('get_current_player')
			mocker.patch.object(command, 'update_and_send')
			state.on_command(command)
			command.update_and_send.assert_called_once()
			assert get_keyword_args(command.update_and_send, 0, 'data') == { 'player_name': 'self' }

		def test_returns_player_name_if_not_current_player(self, mocker, get_keyword_args):
			player = types.SimpleNamespace()
			player.name = 'player1'
			game = types.SimpleNamespace()
			game.is_current_player = lambda p : False
			game.get_current_player = lambda : player
			game.players = []
			state = ServerState(game)
			command = NetworkCommand('get_current_player')
			mocker.patch.object(command, 'update_and_send')
			state.on_command(command)
			command.update_and_send.assert_called_once()
			assert get_keyword_args(command.update_and_send, 0, 'data') == { 'player_name': 'player1' }
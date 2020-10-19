import pytest
import types

from lattice2d.command import Command
from lattice2d.server import ServerCore, ServerState, ServerGame, Player
from unit.conftest import TEST_CONFIG


@pytest.fixture
def create_game(mocker, get_keyword_args):
	def __create_game(core, game_name):
		create_game_command = Command('create_game', {'game_name': game_name})
		mocker.patch.object(create_game_command, 'update_and_send')
		core.on_command(create_game_command)
		assert get_keyword_args(create_game_command.update_and_send, 0, 'status') == 'success'

	return __create_game


@pytest.fixture
def get_games(mocker, get_keyword_args):
	def __get_games(core, games):
		get_games_command = Command('get_games')
		mocker.patch.object(get_games_command, 'update_and_send')
		core.on_command(get_games_command)
		assert get_keyword_args(get_games_command.update_and_send, 0, 'status') == 'success'
		assert get_keyword_args(get_games_command.update_and_send, 0, 'data') == {'games': games}

	return __get_games


@pytest.fixture
def create_player(mocker, get_keyword_args):
	def __create_player(core, player_name, player_connection=None):
		create_player_command = Command('create_player', {'player_name': player_name}, connection=player_connection)
		mocker.patch.object(create_player_command, 'update_and_send')
		core.on_command(create_player_command)
		assert get_keyword_args(create_player_command.update_and_send, 0, 'status') == 'success'

	return __create_player


@pytest.fixture
def join_game(mocker, get_keyword_args):
	def __join_game(core, game_name, player_connection):
		join_game_command = Command('join_game', {'game_name': game_name}, connection=player_connection)
		mocker.patch.object(join_game_command, 'update_and_send')
		core.on_command(join_game_command)
		assert get_keyword_args(join_game_command.update_and_send, 0, 'status') == 'success'

	return __join_game

class MyServerGame(ServerGame):
	def __init__(self, name, destroy_game):
		super().__init__(name, destroy_game)
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.players = []

class TestServer:
	class TestServerCore:
		class TestGames:
			def test_creates_and_gets_games(self, mocker, get_keyword_args):
				core = ServerCore(TEST_CONFIG, test=True)

				create_game_command = Command('create_game', {'game_name': 'game name here'})
				mocker.patch.object(create_game_command, 'update_and_send')
				core.on_command(create_game_command)
				assert get_keyword_args(create_game_command.update_and_send, 0, 'status') == 'success'

				get_games_command = Command('get_games')
				mocker.patch.object(get_games_command, 'update_and_send')
				core.on_command(get_games_command)
				assert get_keyword_args(get_games_command.update_and_send, 0, 'status') == 'success'
				assert get_keyword_args(get_games_command.update_and_send, 0, 'data') == {'games': [('game name here', 0)]}

			def test_destroys_games(self, mocker, get_keyword_args, create_game, get_games):
				core = ServerCore(TEST_CONFIG, test=True)
				create_game(core, 'game name here')

				destroy_game_command = Command('destroy_game', {'game_name': 'game name here'})
				mocker.patch.object(destroy_game_command, 'update_and_send')
				core.on_command(destroy_game_command)
				assert get_keyword_args(destroy_game_command.update_and_send, 0, 'status') == 'success'

				get_games(core, [])

			def test_does_not_destroy_games_with_players(self, mocker, get_keyword_args,
			                                             create_game, create_player, join_game):
				core = ServerCore(TEST_CONFIG, test=True)
				create_game(core, 'game name here')
				create_player(core, 'player name here', 'player connection')
				join_game(core, 'game name here', 'player connection')

				destroy_game_command = Command('destroy_game', {'game_name': 'game name here'})
				mocker.patch.object(destroy_game_command, 'update_and_send')
				with pytest.raises(AssertionError):
					core.on_command(destroy_game_command)

			def test_destroys_games_directly(self, get_keyword_args, create_game, get_games):
				core = ServerCore(TEST_CONFIG, test=True)
				create_game(core, 'game name here')
				core.destroy_game('game name here')
				get_games(core, [])

			def test_does_not_directly_destroy_games_with_players(
					self,
					get_keyword_args,
					create_game,
					create_player,
					join_game
			):
				core = ServerCore(TEST_CONFIG, test=True)
				create_game(core, 'game name here')
				create_player(core, 'player name here', 'player connection')
				join_game(core, 'game name here', 'player connection')

				with pytest.raises(AssertionError):
					core.destroy_game('game name here')

		class TestPlayers:
			def test_creates_player(self, create_player):
				core = ServerCore(TEST_CONFIG, test=True)
				create_player(core, 'player name here', 'player connection')

				assert core.players[0].name == 'player name here'
				assert core.players[0].connection == 'player connection'

			def test_logs_out(self, mocker, create_player, get_keyword_args):
				core = ServerCore(TEST_CONFIG, test=True)
				create_player(core, 'player name here', 'player connection')

				logout_command = Command('logout', {}, connection='player connection')
				mocker.patch.object(logout_command, 'update_and_send')
				core.on_command(logout_command)
				assert get_keyword_args(logout_command.update_and_send, 0, 'status') == 'success'

				assert len(core.players) == 0

			def test_fails_if_logging_out_without_matching_connection(self, mocker, create_player, get_keyword_args):
				core = ServerCore(TEST_CONFIG, test=True)
				create_player(core, 'player name here', 'player connection')

				logout_command = Command('logout', {}, connection='other player connection')
				mocker.patch.object(logout_command, 'update_and_send')
				with pytest.raises(StopIteration):
					core.on_command(logout_command)

			def test_allows_player_to_join_game(self, mocker, get_keyword_args, create_player, create_game, get_games):
				core = ServerCore(TEST_CONFIG, test=True)
				create_game(core, 'game name')
				create_player(core, 'player name here', 'player connection')

				join_game_command = Command('join_game', {'game_name': 'game name'}, connection='player connection')
				mocker.patch.object(join_game_command, 'update_and_send')
				core.on_command(join_game_command)
				assert get_keyword_args(join_game_command.update_and_send, 0, 'status') == 'success'

				get_games(core, [('game name', 1)])

	class TestServerGame:
		def test_allows_adding_and_removing_players(self, mocker):
			game = MyServerGame('game name', mocker.stub())
			player = Player('player name', 'connection')
			game.add_player(player)
			game.remove_player(player)
			assert game.players == []

		def test_does_not_allow_adding_existing_players(self, mocker):
			game = MyServerGame('game name', mocker.stub())
			player = Player('player name', 'connection')
			game.add_player(player)
			with pytest.raises(AssertionError):
				game.add_player(player)

		def test_does_not_allow_removing_non_existent_players(self, mocker):
			game = MyServerGame('game name', mocker.stub())
			player = Player('player name', 'connection')
			with pytest.raises(AssertionError):
				game.remove_player(player)

		def test_destroys_game_if_last_player_was_removed(self, mocker):
			game = MyServerGame('game name', mocker.stub())
			player = Player('player name', 'connection')
			game.add_player(player)
			game.remove_player(player)
			game.destroy_game.assert_called_once()


	class TestServerState:
		class TestGetCurrentPlayerHandler:
			def test_returns_self_in_player_name_if_current_player(self, mocker, get_keyword_args):
				game = types.SimpleNamespace()
				game.is_current_player = lambda player: True
				game.players = []
				state = ServerState(game)
				command = Command('get_current_player')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once()
				assert get_keyword_args(command.update_and_send, 0, 'data') == {'player_name': 'self'}

			def test_returns_player_name_if_not_current_player(self, mocker, get_keyword_args):
				player = types.SimpleNamespace()
				player.name = 'player1'
				game = types.SimpleNamespace()
				game.is_current_player = lambda p: False
				game.get_current_player = lambda: player
				game.players = []
				state = ServerState(game)
				command = Command('get_current_player')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once()
				assert get_keyword_args(command.update_and_send, 0, 'data') == {'player_name': 'player1'}

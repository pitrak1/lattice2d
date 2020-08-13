import pytest
from lattice2d.server.server_core import ServerCore
from lattice2d.server.server_game import ServerGame
from lattice2d.grid.player import Player
from lattice2d.network.network_command import NetworkCommand
from lattice2d.nodes.command import Command
from unit.conftest import TEST_CONFIG

@pytest.fixture
def create_game(mocker, get_keyword_args):
	def __create_game(core, game_name):
		create_game_command = NetworkCommand('create_game', { 'game_name': game_name })
		mocker.patch.object(create_game_command, 'update_and_send')
		core.on_command(create_game_command)
		assert get_keyword_args(create_game_command.update_and_send, 0, 'status') == 'success'
	return __create_game

@pytest.fixture
def get_games(mocker, get_keyword_args):
	def __get_games(core, games):
		get_games_command = NetworkCommand('get_games')
		mocker.patch.object(get_games_command, 'update_and_send')
		core.on_command(get_games_command)
		assert get_keyword_args(get_games_command.update_and_send, 0, 'status') == 'success'
		assert get_keyword_args(get_games_command.update_and_send, 0, 'data') == { 'games': games }
	return __get_games

@pytest.fixture
def create_player(mocker, get_keyword_args):
	def __create_player(core, player_name, player_connection=None):
		create_player_command = NetworkCommand('create_player', { 'player_name': player_name }, connection=player_connection)
		mocker.patch.object(create_player_command, 'update_and_send')
		core.on_command(create_player_command)
		assert get_keyword_args(create_player_command.update_and_send, 0, 'status') == 'success'
	return __create_player

@pytest.fixture
def join_game(mocker, get_keyword_args):
	def __join_game(core, game_name, player_connection):
		join_game_command = NetworkCommand('join_game', { 'game_name': game_name }, connection=player_connection)
		mocker.patch.object(join_game_command, 'update_and_send')
		core.on_command(join_game_command)
		assert get_keyword_args(join_game_command.update_and_send, 0, 'status') == 'success'
	return __join_game

class TestServerCore():
	class TestGames():
		def test_creates_and_gets_games(self, mocker, get_keyword_args):
			core = ServerCore(TEST_CONFIG, test=True)

			create_game_command = NetworkCommand('create_game', { 'game_name': 'game name here' })
			mocker.patch.object(create_game_command, 'update_and_send')
			core.on_command(create_game_command)
			assert get_keyword_args(create_game_command.update_and_send, 0, 'status') == 'success'

			get_games_command = NetworkCommand('get_games')
			mocker.patch.object(get_games_command, 'update_and_send')
			core.on_command(get_games_command)
			assert get_keyword_args(get_games_command.update_and_send, 0, 'status') == 'success'
			assert get_keyword_args(get_games_command.update_and_send, 0, 'data') == { 'games': [('game name here', 0)] }

		def test_destroys_games(self, mocker, get_keyword_args, create_game, get_games):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name here')

			destroy_game_command = NetworkCommand('destroy_game', { 'game_name': 'game name here' })
			mocker.patch.object(destroy_game_command, 'update_and_send')
			core.on_command(destroy_game_command)
			assert get_keyword_args(destroy_game_command.update_and_send, 0, 'status') == 'success'

			get_games(core, [])

		def test_does_not_destroy_games_with_players(self, mocker, get_keyword_args, create_game, create_player, join_game):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name here')
			create_player(core, 'player name here', 'player connection')
			join_game(core, 'game name here', 'player connection')

			destroy_game_command = NetworkCommand('destroy_game', { 'game_name': 'game name here' })
			mocker.patch.object(destroy_game_command, 'update_and_send')
			with pytest.raises(AssertionError):
				core.on_command(destroy_game_command)

		def test_destroys_games_directly(self, mocker, get_keyword_args, create_game, get_games):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name here')
			core.destroy_game('game name here')
			get_games(core, [])

		def test_does_not_directly_destroy_games_with_players(self, mocker, get_keyword_args, create_game, create_player, join_game):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name here')
			create_player(core, 'player name here', 'player connection')
			join_game(core, 'game name here', 'player connection')

			with pytest.raises(AssertionError):
				core.destroy_game('game name here')

	class TestPlayers():
		def test_creates_player(self, mocker, create_player):
			core = ServerCore(TEST_CONFIG, test=True)
			create_player(core, 'player name here', 'player connection')

			assert core.players[0].name == 'player name here'
			assert core.players[0].connection == 'player connection'
		

		def test_logs_out(self, mocker, create_player, get_keyword_args):
			core = ServerCore(TEST_CONFIG, test=True)
			create_player(core, 'player name here', 'player connection')

			logout_command = NetworkCommand('logout', {}, connection='player connection')
			mocker.patch.object(logout_command, 'update_and_send')
			core.on_command(logout_command)
			assert get_keyword_args(logout_command.update_and_send, 0, 'status') == 'success'

			assert len(core.players) == 0

		def test_fails_if_logging_out_without_matching_connection(self, mocker, create_player, get_keyword_args):
			core = ServerCore(TEST_CONFIG, test=True)
			create_player(core, 'player name here', 'player connection')

			logout_command = NetworkCommand('logout', {}, connection='other player connection')
			mocker.patch.object(logout_command, 'update_and_send')
			with pytest.raises(StopIteration):
				core.on_command(logout_command)

		def test_allows_player_to_join_game(self, mocker, get_keyword_args, create_player, create_game, get_games):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name')
			create_player(core, 'player name here', 'player connection')

			join_game_command = NetworkCommand('join_game', { 'game_name': 'game name' }, connection='player connection')
			mocker.patch.object(join_game_command, 'update_and_send')
			core.on_command(join_game_command)
			assert get_keyword_args(join_game_command.update_and_send, 0, 'status') == 'success'
			
			get_games(core, [('game name', 1)])
		
	class TestCommands():
		def test_adds_command_to_game_if_connection_in_game(self, mocker, get_keyword_args, create_player, create_game, join_game):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name')
			create_player(core, 'player name here', 'player connection')
			join_game(core, 'game name', 'player connection')

			command = NetworkCommand('fake command', {}, connection='player connection')
			core.add_command(command)

			assert core.children[0].command_queue.popleft() == command

		def test_adds_command_to_core_if_connection_not_in_game(self, mocker, get_keyword_args, create_player, create_game, join_game):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name')
			create_player(core, 'player name here', 'player connection')

			command = NetworkCommand('fake command', {}, connection='player connection')
			core.add_command(command)

			assert core.command_queue.popleft() == command

		def test_adds_command_to_core_if_connection_is_not_found(self, mocker, create_game):
			core = ServerCore(TEST_CONFIG, test=True)
			create_game(core, 'game name')

			command = NetworkCommand('fake command', {}, connection='player connection')
			core.add_command(command)

			assert core.command_queue.popleft() == command

import pytest
from lattice2d.full import FullGame, FullPlayer, FullServer
from lattice2d.network import NetworkCommand

class TestFullGame():
	def test_allows_adding_and_removing_players(self, mocker):
		game = FullGame('game name', mocker.stub())
		player = FullPlayer('player name', 'connection')
		game.add_player(player)
		game.remove_player(player)
		assert game.players == []

	def test_does_not_allow_adding_existing_players(self, mocker):
		game = FullGame('game name', mocker.stub())
		player = FullPlayer('player name', 'connection')
		game.add_player(player)
		with pytest.raises(AssertionError):
			game.add_player(player)

	def test_does_not_allow_removing_non_existent_players(self, mocker):
		game = FullGame('game name', mocker.stub())
		player = FullPlayer('player name', 'connection')
		with pytest.raises(AssertionError):
			game.remove_player(player)

	def test_sends_players_to_all_but_added_after_add(self, mocker):
		game = FullGame('game name', mocker.stub())
		mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
		player1 = FullPlayer('player name 1', 'connection 1')
		game.add_player(player1)
		player2 = FullPlayer('player name 2', 'connection 2')
		game.add_player(player2)
		NetworkCommand.create_and_send.assert_called_once_with(
			'broadcast_players_in_game',
			{ 'players': [('player name 1', False), ('player name 2', False)] },
			'success',
			'connection 1'
		)

	def test_destroys_game_if_last_player_was_removed(self, mocker):
		game = FullGame('game name', mocker.stub())
		player = FullPlayer('player name', 'connection')
		game.add_player(player)
		game.remove_player(player)
		game.destroy_game.assert_called_once()

	def test_sends_players_if_players_remaining_after_removal(self, mocker, get_args):
		game = FullGame('game name', mocker.stub())
		mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
		player1 = FullPlayer('player name 1', 'connection 1')
		game.add_player(player1)
		player2 = FullPlayer('player name 2', 'connection 2')
		game.add_player(player2)
		game.remove_player(player1)
		assert get_args(NetworkCommand.create_and_send, 1) == (
			'broadcast_players_in_game',
			{ 'players': [('player name 2', False)] },
			'success',
			'connection 2'
		)

class TestFullServer():
	class TestAddCommand():
		def test_adds_to_game_queue_if_player_in_game(self, mocker):
			server = FullServer()
			server.create_game('game name')
			server.create_player('player name', 'connection')
			server.add_player_to_game_by_connection('game name', 'connection')
			command = NetworkCommand('command_type', {}, 'pending', 'connection')
			game = next(g for g in server.children if g.name == 'game name')
			server.add_command(command)
			assert game.command_queue.popleft() == command

		def test_adds_to_core_queue_if_player_not_in_game(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			command = NetworkCommand('command_type', {}, 'pending', 'connection')
			server.add_command(command)
			assert server.command_queue.popleft() == command

	class TestCreatePlayer():
		def test_creates_player_and_adds_to_players(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			assert server.players[0].name == 'player name'

	class TestDestroyPlayerByConnection():
		def test_destroys_player(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			server.destroy_player_by_connection('connection')
			assert len(server.players) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			server = FullServer()
			with pytest.raises(AssertionError):
				server.destroy_player_by_connection('connection')

	class TestDestroyPlayerByName():
		def test_destroys_player(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			server.destroy_player_by_name('player name')
			assert len(server.players) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			server = FullServer()
			with pytest.raises(AssertionError):
				server.destroy_player_by_name('player name')

	class TestAddPlayerToGameByConnection():
		def test_adds_player(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			server.create_game('game name')
			server.add_player_to_game_by_connection('game name', 'connection')
			assert server.players[0].name == 'player name'

		def test_throws_error_if_player_non_existent(self, mocker):
			server = FullServer()
			server.create_game('game name')
			with pytest.raises(AssertionError):
				server.add_player_to_game_by_connection('game name', 'connection')

		def test_throws_error_if_game_non_existent(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			with pytest.raises(AssertionError):
				server.add_player_to_game_by_connection('game name', 'connection')

	class TestAddPlayerToGameByName():
		def test_adds_player(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			server.create_game('game name')
			server.add_player_to_game_by_name('game name', 'player name')
			assert server.players[0].name == 'player name'

		def test_throws_error_if_player_non_existent(self, mocker):
			server = FullServer()
			server.create_game('game name')
			with pytest.raises(AssertionError):
				server.add_player_to_game_by_name('game name', 'player name')

		def test_throws_error_if_game_non_existent(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			with pytest.raises(AssertionError):
				server.add_player_to_game_by_name('game name', 'player name')

	class TestCreateGame():
		def test_creates_game(self, mocker):
			server = FullServer()
			server.create_game('game name')
			assert server.children[0].name == 'game name'

		def test_throws_error_if_game_already_exists(self, mocker):
			server = FullServer()
			server.create_game('game name')
			with pytest.raises(AssertionError):
				server.create_game('game name')

	class TestDestroyGame():
		def test_destroys_game(self, mocker):
			server = FullServer()
			server.create_game('game name')
			server.destroy_game('game name')
			assert len(server.children) == 0

		def test_throws_error_if_game_does_not_exist(self, mocker):
			server = FullServer()
			with pytest.raises(AssertionError):
				server.destroy_game('game name')

		def test_throws_error_if_game_has_players(self, mocker):
			server = FullServer()
			server.create_game('game name')
			server.create_player('player name', 'connection')
			server.add_player_to_game_by_connection('game name', 'connection')
			with pytest.raises(AssertionError):
				server.destroy_game('game name')

	class TestFindGameByName():
		def test_returns_game_if_it_exists(self, mocker):
			server = FullServer()
			server.create_game('game name')
			assert server.find_game_by_name('game name').name == 'game name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			server = FullServer()
			assert not server.find_game_by_name('game name')

	class TestFindPlayerByName():
		def test_returns_player_if_it_exists(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			assert server.find_player_by_name('player name').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			server = FullServer()
			assert not server.find_player_by_name('player name')

	class TestFindPlayerByConnection():
		def test_returns_player_if_it_exists(self, mocker):
			server = FullServer()
			server.create_player('player name', 'connection')
			assert server.find_player_by_connection('connection').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			server = FullServer()
			assert not server.find_player_by_connection('connection')

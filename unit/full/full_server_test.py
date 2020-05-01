import pytest
from lattice2d.full.full_server import FullServerGame, FullServerPlayer, FullServer, FullServerPlayerList, FullServerGameList
from lattice2d.network import NetworkCommand

class TestFullServerGame():
	def test_allows_adding_and_removing_players(self, mocker):
		game = FullServerGame('game name', mocker.stub())
		player = FullServerPlayer('player name', 'connection')
		game.current_state.add_player(player)
		game.current_state.remove_player(player)
		assert game.current_state.players == []

	def test_does_not_allow_adding_existing_players(self, mocker):
		game = FullServerGame('game name', mocker.stub())
		player = FullServerPlayer('player name', 'connection')
		game.current_state.add_player(player)
		with pytest.raises(AssertionError):
			game.current_state.add_player(player)

	def test_does_not_allow_removing_non_existent_players(self, mocker):
		game = FullServerGame('game name', mocker.stub())
		player = FullServerPlayer('player name', 'connection')
		with pytest.raises(AssertionError):
			game.current_state.remove_player(player)

	def test_sends_players_to_all_but_added_after_add(self, mocker):
		game = FullServerGame('game name', mocker.stub())
		mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
		player1 = FullServerPlayer('player name 1', 'connection 1')
		game.current_state.add_player(player1)
		player2 = FullServerPlayer('player name 2', 'connection 2')
		game.current_state.add_player(player2)
		NetworkCommand.create_and_send.assert_called_once_with(
			'broadcast_players_in_game',
			{ 'players': [('player name 1', False), ('player name 2', False)] },
			'success',
			'connection 1'
		)

	def test_destroys_game_if_last_player_was_removed(self, mocker):
		game = FullServerGame('game name', mocker.stub())
		player = FullServerPlayer('player name', 'connection')
		game.current_state.add_player(player)
		game.current_state.remove_player(player)
		game.current_state.destroy_game.assert_called_once()

	def test_sends_players_if_players_remaining_after_removal(self, mocker, get_args):
		game = FullServerGame('game name', mocker.stub())
		mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
		player1 = FullServerPlayer('player name 1', 'connection 1')
		game.current_state.add_player(player1)
		player2 = FullServerPlayer('player name 2', 'connection 2')
		game.current_state.add_player(player2)
		game.current_state.remove_player(player1)
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
			server.children.append(FullServerGame('game name', mocker.stub()))
			server.players.append(FullServerPlayer('player name', 'connection'))
			server.children.add_player_to_game('game name', server.players[0])
			command = NetworkCommand('command_type', {}, 'pending', 'connection')
			game = next(g for g in server.children if g.name == 'game name')
			server.add_command(command)
			assert game.command_queue.popleft() == command

		def test_adds_to_core_queue_if_player_not_in_game(self, mocker):
			server = FullServer()
			server.players.append(FullServerPlayer('player name', 'connection'))
			command = NetworkCommand('command_type', {}, 'pending', 'connection')
			server.add_command(command)
			assert server.command_queue.popleft() == command

class TestFullServerPlayerList():
	class TestAppend():
		def test_throws_error_if_duplicate_name(self, mocker):
			player_list = FullServerPlayerList()
			player_list.append(FullServerPlayer('player name', 'connection'))
			with pytest.raises(AssertionError):
				player_list.append(FullServerPlayer('player name', 'connection'))

	class TestDestroyPlayerByConnection():
		def test_destroys_player(self, mocker):
			player_list = FullServerPlayerList()
			player_list.append(FullServerPlayer('player name', 'connection'))
			player_list.destroy_by_connection('connection')
			assert len(player_list) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			player_list = FullServerPlayerList()
			with pytest.raises(AssertionError):
				player_list.destroy_by_connection('connection')

	class TestDestroyByName():
		def test_destroys_player(self, mocker):
			player_list = FullServerPlayerList()
			player_list.append(FullServerPlayer('player name', 'connection'))
			player_list.destroy_by_name('player name')
			assert len(player_list) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			player_list = FullServerPlayerList()
			with pytest.raises(AssertionError):
				player_list.destroy_by_name('player name')

	class TestFindByName():
		def test_returns_player_if_it_exists(self, mocker):
			player_list = FullServerPlayerList()
			player_list.append(FullServerPlayer('player name', 'connection'))
			assert player_list.find_by_name('player name').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			player_list = FullServerPlayerList()
			assert not player_list.find_by_name('player name')

	class TestFindByConnection():
		def test_returns_player_if_it_exists(self, mocker):
			player_list = FullServerPlayerList()
			player_list.append(FullServerPlayer('player name', 'connection'))
			assert player_list.find_by_connection('connection').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			player_list = FullServerPlayerList()
			assert not player_list.find_by_connection('connection')

class TestFullServerGameList():
	class TestAddPlayerToGame():
		def test_adds_player(self, mocker):
			game_list = FullServerGameList()
			player = FullServerPlayer('player name', 'connection')
			game_list.append(FullServerGame('game name', mocker.stub()))
			game_list.add_player_to_game('game name', player)
			assert game_list[0].current_state.players[0].name == 'player name'

		def test_throws_error_if_game_non_existent(self, mocker):
			game_list = FullServerGameList()
			player = FullServerPlayer('player name', 'connection')
			with pytest.raises(AssertionError):
				game_list.add_player_to_game('game name', player)

	class TestAppend():
		def test_throws_error_if_duplicate_name(self, mocker):
			game_list = FullServerGameList()
			game_list.append(FullServerGame('game name', mocker.stub()))
			with pytest.raises(AssertionError):
				game_list.append(FullServerGame('game name', mocker.stub()))

	class TestDestroyGame():
		def test_destroys_game(self, mocker):
			game_list = FullServerGameList()
			game_list.append(FullServerGame('game name', mocker.stub()))
			game_list.destroy('game name')
			assert len(game_list) == 0

		def test_throws_error_if_game_does_not_exist(self, mocker):
			game_list = FullServerGameList()
			with pytest.raises(AssertionError):
				game_list.destroy('game name')

		def test_throws_error_if_game_has_players(self, mocker):
			game_list = FullServerGameList()
			game_list.append(FullServerGame('game name', mocker.stub()))
			player = FullServerPlayer('player name', 'connection')
			game_list.add_player_to_game('game name', player)
			with pytest.raises(AssertionError):
				game_list.destroy('game name')

	class TestFindByName():
		def test_returns_game_if_it_exists(self, mocker):
			game_list = FullServerGameList()
			game_list.append(FullServerGame('game name', mocker.stub()))
			assert game_list.find_by_name('game name').name == 'game name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			game_list = FullServerGameList()
			assert not game_list.find_by_name('game name')

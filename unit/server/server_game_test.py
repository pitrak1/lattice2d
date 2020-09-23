import pytest
from lattice2d.server.server_game import ServerGame
from lattice2d.grid import Player
from lattice2d.command import Command

class MyServerGame(ServerGame):
	def __init__(self, name, destroy_game):
		self.name = name
		self.destroy_game = destroy_game
		self.current_player_index = 0
		self.players = []

class TestServerGame():
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

	def test_sends_players_to_all_but_added_after_add(self, mocker):
		game = MyServerGame('game name', mocker.stub())
		mocker.patch('lattice2d.command.Command.create_and_send')
		player1 = Player('player name 1', 'connection 1')
		game.add_player(player1)
		player2 = Player('player name 2', 'connection 2')
		game.add_player(player2)
		Command.create_and_send.assert_called_once_with(
			'broadcast_players_in_game',
			{ 'players': [('player name 1', False), ('player name 2', False)] },
			'success',
			'connection 1'
		)

	def test_destroys_game_if_last_player_was_removed(self, mocker):
		game = MyServerGame('game name', mocker.stub())
		player = Player('player name', 'connection')
		game.add_player(player)
		game.remove_player(player)
		game.destroy_game.assert_called_once()

	def test_sends_players_if_players_remaining_after_removal(self, mocker, get_positional_args):
		game = MyServerGame('game name', mocker.stub())
		mocker.patch('lattice2d.command.Command.create_and_send')
		player1 = Player('player name 1', 'connection 1')
		game.add_player(player1)
		player2 = Player('player name 2', 'connection 2')
		game.add_player(player2)
		game.remove_player(player1)
		assert get_positional_args(Command.create_and_send, 1) == (
			'broadcast_players_in_game',
			{ 'players': [('player name 2', False)] },
			'success',
			'connection 2'
		)
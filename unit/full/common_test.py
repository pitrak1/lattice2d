import pytest
from lattice2d.full.common import FullPlayerList, FullPlayer

class TestFullPlayerList():
	class TestAppend():
		def test_throws_error_if_duplicate_name(self, mocker):
			player_list = FullPlayerList()
			player_list.append(FullPlayer('player name', 'connection'))
			with pytest.raises(AssertionError):
				player_list.append(FullPlayer('player name', 'connection'))

	class TestDestroyPlayerByConnection():
		def test_destroys_player(self, mocker):
			player_list = FullPlayerList()
			player_list.append(FullPlayer('player name', 'connection'))
			player_list.destroy_by_connection('connection')
			assert len(player_list) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			player_list = FullPlayerList()
			with pytest.raises(AssertionError):
				player_list.destroy_by_connection('connection')

	class TestDestroyByName():
		def test_destroys_player(self, mocker):
			player_list = FullPlayerList()
			player_list.append(FullPlayer('player name', 'connection'))
			player_list.destroy_by_name('player name')
			assert len(player_list) == 0

		def test_throws_error_if_player_non_existent(self, mocker):
			player_list = FullPlayerList()
			with pytest.raises(AssertionError):
				player_list.destroy_by_name('player name')

	class TestFindByName():
		def test_returns_player_if_it_exists(self, mocker):
			player_list = FullPlayerList()
			player_list.append(FullPlayer('player name', 'connection'))
			assert player_list.find_by_name('player name').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			player_list = FullPlayerList()
			assert not player_list.find_by_name('player name')

	class TestFindByConnection():
		def test_returns_player_if_it_exists(self, mocker):
			player_list = FullPlayerList()
			player_list.append(FullPlayer('player name', 'connection'))
			assert player_list.find_by_connection('connection').name == 'player name'

		def test_returns_false_if_it_does_not_exist(self, mocker):
			player_list = FullPlayerList()
			assert not player_list.find_by_connection('connection')
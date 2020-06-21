import pytest
from lattice2d.utilities.keyed_list import KeyedList

class TestKeyedList():
	class TestAddingAndRetreiving():
		def test_adds_and_gets_entries(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			assert keyed_list[0] == 1234

		def test_adds_and_gets_keyed_entries(self):
			keyed_list = KeyedList()
			keyed_list.append_with_key(1234, 'test')
			assert keyed_list.find('test') == 1234

		def test_inserts_entries(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			keyed_list.insert(0, 2345)
			assert keyed_list == [2345, 1234]

		def test_inserts_keyed_entries(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			keyed_list.insert_with_key(0, 2345, 'test')
			assert keyed_list == [2345, 1234]
			assert keyed_list.find('test') == 2345

	class TestSettingAndClearing():
		def test_initializes_from_list(self):
			keyed_list = KeyedList([1234, 2345, 3456])
			assert keyed_list == [1234, 2345, 3456]

		def test_initializes_from_keyed_list(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			keyed_list.append_with_key(2345, 'test')
			other_keyed_list = KeyedList(keyed_list)
			assert other_keyed_list == [1234, 2345]
			assert other_keyed_list.find('test') == 2345

		def test_sets_from_list(self):
			keyed_list = KeyedList()
			keyed_list.set([1234, 2345, 3456])
			assert keyed_list == [1234, 2345, 3456]

		def test_sets_from_keyed_list(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			keyed_list.append_with_key(2345, 'test')
			other_keyed_list = KeyedList()
			other_keyed_list.set(keyed_list)
			assert other_keyed_list == [1234, 2345]
			assert other_keyed_list.find('test') == 2345

		def test_clears(self):
			keyed_list = KeyedList()
			keyed_list.append(1234)
			keyed_list.append_with_key(2345, 'test')
			keyed_list.clear()
			with pytest.raises(IndexError):
				keyed_list[0]
			with pytest.raises(KeyError):
				keyed_list.find('test')

	class TestRemoving():
		def test_removes_entries(self):
			keyed_list = KeyedList([1234, 2345, 3456])
			keyed_list.remove(2345)
			assert keyed_list == [1234, 3456]

		def test_removes_keyed_entries(self):
			keyed_list = KeyedList()
			keyed_list.append_with_key(1234, 'test')
			keyed_list.append_with_key(2345, 'test2')
			keyed_list.remove_with_key('test')
			assert keyed_list == [2345]
			with pytest.raises(KeyError):
				keyed_list.find('test')

		def test_removes_keys_when_removing_by_value(self):
			keyed_list = KeyedList()
			keyed_list.append_with_key(1234, 'test')
			keyed_list.append_with_key(2345, 'test2')
			keyed_list.remove(1234)
			assert keyed_list == [2345]
			with pytest.raises(KeyError):
				keyed_list.find('test')

		def test_removes_entries_by_position(self):
			keyed_list = KeyedList([1234, 2345, 3456])
			keyed_list.pop(1)
			assert keyed_list == [1234, 3456]

		def test_removes_keyed_entries_by_position(self):
			keyed_list = KeyedList()
			keyed_list.append_with_key(1234, 'test')
			keyed_list.append_with_key(2345, 'test2')
			keyed_list.pop(0)
			assert keyed_list == [2345]
			with pytest.raises(KeyError):
				keyed_list.find('test')

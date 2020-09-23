import pytest

from lattice2d.utilities.threaded_queue import ThreadedQueue


class TestThreadedQueue:
	def test_has_no_elements_on_initialization(self):
		queue = ThreadedQueue()
		assert not queue.has_elements()

	def test_allows_adding_elements(self):
		queue = ThreadedQueue()
		queue.append(True)
		assert queue.has_elements()

	def test_allows_popping_elements(self):
		queue = ThreadedQueue()
		queue.append('some command')
		assert queue.popleft() == 'some command'

	def test_raises_error_if_queue_is_empty(self):
		queue = ThreadedQueue()
		with pytest.raises(IndexError):
			queue.popleft()

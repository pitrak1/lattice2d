import pytest

from lattice2d.utilities import \
	within_circle_bounds, \
	within_square_bounds, \
	within_rect_bounds, \
	get_page_info, \
	ThreadedQueue, \
	ThreadedSync


class TestUtilities:
	class TestBounds:
		class TestWithinCircleBounds:
			def test_returns_true_when_position_is_within_bounds(self):
				assert within_circle_bounds((0, 0), (19, 0), 20)
				assert within_circle_bounds((0, 0), (0, 19), 20)
				assert within_circle_bounds((0, 0), (-13, -13), 20)

			def test_returns_false_when_position_is_outside_bounds(self):
				assert not within_circle_bounds((0, 0), (21, 0), 20)
				assert not within_circle_bounds((0, 0), (0, 21), 20)
				assert not within_circle_bounds((0, 0), (-15, -15), 20)

		class TestWithinRectBounds:
			def test_returns_true_when_position_is_within_bounds(self):
				assert within_rect_bounds((0, 0), (19, 0), (40, 20))
				assert within_rect_bounds((0, 0), (0, 9), (40, 20))
				assert within_rect_bounds((0, 0), (-19, -9), (40, 20))

			def test_returns_false_when_position_is_outside_bounds(self):
				assert not within_rect_bounds((0, 0), (21, 0), (40, 20))
				assert not within_rect_bounds((0, 0), (0, 11), (40, 20))
				assert not within_rect_bounds((0, 0), (-21, -11), (40, 20))

		class TestWithinSquareBounds:
			def test_returns_true_when_position_is_within_bounds(self):
				assert within_square_bounds((0, 0), (19, 0), 40)
				assert within_square_bounds((0, 0), (0, 19), 40)
				assert within_square_bounds((0, 0), (-19, -19), 40)

			def test_returns_false_when_position_is_outside_bounds(self):
				assert not within_square_bounds((0, 0), (21, 0), 40)
				assert not within_square_bounds((0, 0), (0, 21), 40)
				assert not within_square_bounds((0, 0), (-21, -21), 40)

	class TestGetPageInfo:
		def test_returns_correct_data_on_first_page(self):
			result = get_page_info(0, 4, 6)
			assert result == [0, 4, True, False]

		def test_returns_correct_data_on_middle_page(self):
			result = get_page_info(1, 4, 10)
			assert result == [4, 8, True, True]

		def test_returns_correct_data_on_last_page(self):
			result = get_page_info(1, 4, 6)
			assert result == [4, 6, False, True]

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

	class TestThreadedSync:
		def test_done_returns_true_on_initialization(self):
			sync = ThreadedSync(3)
			assert sync.done()

		def test_done_returns_false_when_counted(self):
			sync = ThreadedSync(3)
			sync.count()
			assert not sync.done()

		def test_done_returns_true_when_counted_to_max_value(self):
			sync = ThreadedSync(3)
			for i in range(3):
				sync.count()
			assert sync.done()

		def test_done_returns_false_when_counted_to_one_beyond_max(self):
			sync = ThreadedSync(3)
			for i in range(4):
				sync.count()
			assert not sync.done()

		def test_done_returns_true_when_counted_to_multiple_of_max(self):
			sync = ThreadedSync(3)
			for i in range(6):
				sync.count()
			assert sync.done()
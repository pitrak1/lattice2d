from lattice2d.utilities.threaded_sync import ThreadedSync


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

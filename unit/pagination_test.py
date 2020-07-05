from utilities.pagination import get_page_info

class TestPagination():
	def test_returns_correct_data_on_first_page(self):
		result = get_page_info(0, 4, 6)
		assert result == [0, 4, True, False]

	def test_returns_correct_data_on_middle_page(self):
		result = get_page_info(1, 4, 10)
		assert result == [4, 8, True, True]

	def test_returns_correct_data_on_last_page(self):
		result = get_page_info(1, 4, 6)
		assert result == [4, 6, False, True]

def get_page_info(current_page, page_size, total):
	min_ = current_page * page_size
	max_ = min((current_page + 1) * page_size, total)
	down = (current_page + 1) * page_size < total
	up = current_page != 0
	return [min_, max_, down, up]
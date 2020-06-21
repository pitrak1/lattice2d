class KeyedList(list):
	def __init__(self, iterable=None):
		super().__init__()
		self.keys = {}
		if isinstance(iterable, KeyedList) or isinstance(iterable, list):
			self.set(iterable)

	def append_with_key(self, x, key):
		assert key not in self.keys.keys()
		self.keys[key] = len(self)
		super().append(x)

	def extend(self, iterable):
		assert isinstance(iterable, KeyedList)
		super().extend(iterable)
		self.keys.update(iterable.keys)
		return self

	def insert_with_key(self, i, x, key):
		assert key not in self.keys.keys()
		super().insert(i, x)
		self.keys[key] = i

	def remove(self, x):
		index = self.index(x)
		super().remove(x)
		removal_key = next(iter(key for key, value in self.keys.items() if value == index), False)
		if removal_key: del self.keys[removal_key]

	def remove_with_key(self, key):
		index = self.keys[key]
		super().pop(index)
		del self.keys[key]

	def pop(self, i):
		super().pop(i)
		removal_key = next(iter(key for key, value in self.keys.items() if value == i), False)
		if removal_key: del self.keys[removal_key]

	def clear(self):
		super().clear()
		self.keys = {}

	def find(self, key):
		return self[self.keys[key]]

	def set(self, iterable):
		if isinstance(iterable, KeyedList):
			self.clear()
			for value in iterable:
				self.append(value)
			self.keys.update(iterable.keys)
		elif isinstance(iterable, list):
			self.clear()
			for value in iterable:
				self.append(value)
